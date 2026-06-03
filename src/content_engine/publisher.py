import json
import logging
import os
from pathlib import Path
from typing import Optional, List
import requests
from src.core.brand import Brand
from src.content_engine.writer import PublicationPackage

logger = logging.getLogger(__name__)

_YT_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]
_YT_TOKEN_FILE = Path(__file__).resolve().parent.parent.parent / ".youtube_token.json"
_CREDENTIALS_FILE = Path(__file__).resolve().parent.parent.parent / "credentials.json"


# ---------------------------------------------------------------------------
# YouTube helpers
# ---------------------------------------------------------------------------

def _build_yt_client():
    """Returns authenticated YouTube resource. Runs local OAuth flow if needed."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None

    if _YT_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(_YT_TOKEN_FILE), _YT_SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        _YT_TOKEN_FILE.write_text(creds.to_json())

    if not creds or not creds.valid:
        if not _CREDENTIALS_FILE.exists():
            raise RuntimeError(
                "credentials.json not found. Download OAuth client credentials "
                "from Google Console and place at project root."
            )
        flow = InstalledAppFlow.from_client_secrets_file(
            str(_CREDENTIALS_FILE), _YT_SCOPES
        )
        creds = flow.run_local_server(port=8080, open_browser=True)
        _YT_TOKEN_FILE.write_text(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def build_video_metadata(
    pkg: PublicationPackage,
    is_short: bool = False,
    genre: str = "Content",
) -> dict:
    title = pkg.youtube_titles[0] if pkg.youtube_titles else pkg.brief.get("titulo_principal", "")
    if is_short and "#Shorts" not in title:
        title = (title[:91] + " #Shorts") if len(title) > 91 else title + " #Shorts"

    tags = [
        "IM Music", "REBEL LUXURY", "marketing", "neurociencia",
        "music business", "industria musical", "Colombia",
    ]
    if is_short:
        tags.append("Shorts")

    description = pkg.youtube_description[:5000]

    return {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "10",
            "defaultLanguage": "es",
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
        },
    }


# ---------------------------------------------------------------------------
# YouTube Publisher
# ---------------------------------------------------------------------------

class YouTubePublisher:
    def __init__(self, client_id: str = "", client_secret: str = "", channel_id: str = ""):
        self._channel_id = channel_id
        self._yt = None

    def _get_client(self):
        if self._yt is None:
            self._yt = _build_yt_client()
        return self._yt

    def upload_video(
        self,
        video_path: Path,
        pkg: PublicationPackage,
        thumbnail_path: Optional[Path] = None,
        is_short: bool = False,
    ) -> Optional[str]:
        """Uploads video to YouTube. Returns video_id or None on failure."""
        from googleapiclient.http import MediaFileUpload

        yt = self._get_client()
        metadata = build_video_metadata(pkg, is_short=is_short)
        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
        try:
            req = yt.videos().insert(part="snippet,status", body=metadata, media_body=media)
            response = None
            while response is None:
                status_obj, response = req.next_chunk()
            video_id = response["id"]
            logger.info("Uploaded to YouTube: https://youtu.be/%s", video_id)

            if thumbnail_path and thumbnail_path.exists():
                try:
                    yt.thumbnails().set(
                        videoId=video_id,
                        media_body=MediaFileUpload(str(thumbnail_path)),
                    ).execute()
                except Exception as thumb_err:
                    # Requires 1000+ subscribers or YouTube manual verification
                    logger.warning("Thumbnail not set (permissions): %s", thumb_err)

            return video_id
        except Exception as e:
            logger.error("YouTube upload failed: %s", e)
            return None

    def upload_short(
        self,
        video_path: Path,
        pkg: PublicationPackage,
        thumbnail_path: Optional[Path] = None,
    ) -> Optional[str]:
        """Uploads a YouTube Short (max 60s). Sets #Shorts tag automatically."""
        return self.upload_video(video_path, pkg, thumbnail_path, is_short=True)

    def add_to_playlist(self, video_id: str, playlist_id: str) -> bool:
        yt = self._get_client()
        try:
            yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id},
                    }
                },
            ).execute()
            return True
        except Exception as e:
            logger.error("Playlist add failed: %s", e)
            return False

    def set_video_public(self, video_id: str) -> bool:
        """Changes video privacy from private to public."""
        yt = self._get_client()
        try:
            yt.videos().update(
                part="status",
                body={"id": video_id, "status": {"privacyStatus": "public"}},
            ).execute()
            logger.info("Video %s is now public", video_id)
            return True
        except Exception as e:
            logger.error("Failed to make video public: %s", e)
            return False


# ---------------------------------------------------------------------------
# Instagram — Meta Graph API (Business account required)
# ---------------------------------------------------------------------------

class InstagramPublisher:
    """Posts to Instagram via Meta Graph API (Business account + Page required)."""

    def __init__(self, access_token: str, ig_account_id: str):
        self._token = access_token
        self._account_id = ig_account_id
        self._base = "https://graph.facebook.com/v19.0"

    def _post(self, endpoint: str, data: dict) -> dict:
        r = requests.post(
            f"{self._base}/{endpoint}",
            params={"access_token": self._token},
            json=data,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def post_single(self, image_url: str, caption: str) -> Optional[str]:
        """Posts single image. image_url must be publicly accessible."""
        try:
            container = self._post(
                f"{self._account_id}/media",
                {"image_url": image_url, "caption": caption[:2200]},
            )
            result = self._post(
                f"{self._account_id}/media_publish",
                {"creation_id": container["id"]},
            )
            media_id = result.get("id")
            logger.info("Posted to Instagram (Graph API): %s", media_id)
            return media_id
        except Exception as e:
            logger.error("Instagram Graph post failed: %s", e)
            return None

    def post_carousel(self, image_urls: List[str], caption: str) -> Optional[str]:
        """Posts carousel (up to 10 images)."""
        try:
            children = []
            for url in image_urls[:10]:
                c = self._post(
                    f"{self._account_id}/media",
                    {"image_url": url, "is_carousel_item": True},
                )
                children.append(c["id"])

            container = self._post(
                f"{self._account_id}/media",
                {"media_type": "CAROUSEL", "children": children, "caption": caption[:2200]},
            )
            result = self._post(
                f"{self._account_id}/media_publish",
                {"creation_id": container["id"]},
            )
            return result.get("id")
        except Exception as e:
            logger.error("Instagram carousel (Graph API) failed: %s", e)
            return None


# ---------------------------------------------------------------------------
# Instagram — instagrapi (direct login, personal/creator accounts)
# ---------------------------------------------------------------------------

_IG_SESSION_FILE = Path(__file__).resolve().parent.parent.parent / ".instagram_session.json"


class InstagrapiPublisher:
    """
    Posts to Instagram via instagrapi (direct login).
    Use this when Meta Graph API is not available (personal/creator accounts).
    Session is cached in .instagram_session.json after first login.
    """

    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client

        from instagrapi import Client
        cl = Client()
        cl.delay_range = [1, 3]

        if _IG_SESSION_FILE.exists():
            try:
                cl.load_settings(_IG_SESSION_FILE)
                cl.login(self._username, self._password)
                logger.info("Instagram session loaded from cache")
                self._client = cl
                return cl
            except Exception:
                logger.warning("Cached session invalid, re-logging in")

        cl.login(self._username, self._password)
        cl.dump_settings(_IG_SESSION_FILE)
        logger.info("Instagram login OK, session saved")
        self._client = cl
        return cl

    def post_photo(self, image_path: Path, caption: str) -> Optional[str]:
        """Posts a single photo to feed."""
        try:
            cl = self._get_client()
            media = cl.photo_upload(str(image_path), caption[:2200])
            media_id = str(media.pk)
            logger.info("Posted to Instagram (instagrapi): %s", media_id)
            return media_id
        except Exception as e:
            logger.error("Instagram photo post failed: %s", e)
            return None

    def post_carousel(self, image_paths: List[Path], caption: str) -> Optional[str]:
        """Posts a carousel (up to 10 local images)."""
        try:
            cl = self._get_client()
            paths = [str(p) for p in image_paths[:10]]
            media = cl.album_upload(paths, caption[:2200])
            media_id = str(media.pk)
            logger.info("Posted carousel to Instagram: %s", media_id)
            return media_id
        except Exception as e:
            logger.error("Instagram carousel (instagrapi) failed: %s", e)
            return None

    def post_reel(self, video_path: Path, caption: str, thumbnail_path: Optional[Path] = None) -> Optional[str]:
        """Posts a Reel (short video)."""
        try:
            cl = self._get_client()
            extra = {}
            if thumbnail_path and thumbnail_path.exists():
                extra["thumbnail"] = str(thumbnail_path)
            media = cl.clip_upload(str(video_path), caption[:2200], **extra)
            media_id = str(media.pk)
            logger.info("Posted Reel to Instagram: %s", media_id)
            return media_id
        except Exception as e:
            logger.error("Instagram Reel post failed: %s", e)
            return None


# ---------------------------------------------------------------------------
# TikTok Publisher — tiktok-uploader (cookie-based)
# ---------------------------------------------------------------------------

_TIKTOK_COOKIES_FILE = Path(__file__).resolve().parent.parent.parent / ".tiktok_cookies.json"


class TikTokPublisher:
    """
    Posts to TikTok via tiktok-uploader (uses browser cookies for auth).
    Cookies file must be exported from a logged-in TikTok session.
    Run: python scripts/get_tiktok_cookies.py to generate .tiktok_cookies.json
    """

    def __init__(self, cookies_file: Optional[Path] = None):
        self._cookies = str(cookies_file or _TIKTOK_COOKIES_FILE)

    def _check_cookies(self) -> bool:
        p = Path(self._cookies)
        if not p.exists():
            logger.error(
                "TikTok cookies not found at %s. "
                "Run: python scripts/get_tiktok_cookies.py",
                self._cookies,
            )
            return False
        return True

    def upload(
        self,
        video_path: Path,
        caption: str,
        tags: Optional[List[str]] = None,
        schedule: Optional[str] = None,
    ) -> bool:
        """
        Uploads video to TikTok.
        caption: max ~150 chars + hashtags
        tags: list of hashtag strings without #
        schedule: ISO datetime string for scheduled posting (optional)
        """
        if not self._check_cookies():
            return False

        try:
            from tiktok_uploader.upload import upload_video as tiktok_upload

            full_caption = caption[:150]
            if tags:
                hashtags = " ".join(f"#{t.strip('#')}" for t in tags[:5])
                full_caption = f"{full_caption} {hashtags}"

            tiktok_upload(
                str(video_path),
                description=full_caption,
                cookies=self._cookies,
                schedule=schedule,
            )
            logger.info("Posted to TikTok: %s", video_path.name)
            return True
        except Exception as e:
            logger.error("TikTok upload failed: %s", e)
            return False
