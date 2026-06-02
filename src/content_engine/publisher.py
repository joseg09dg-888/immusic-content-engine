import json
import logging
import os
from pathlib import Path
from typing import Optional, List
import requests
from src.core.brand import Brand
from src.content_engine.writer import PublicationPackage

logger = logging.getLogger(__name__)

_YT_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
_YT_TOKEN_FILE = Path(__file__).resolve().parent.parent.parent / ".youtube_token.json"


def _build_yt_client(client_id: str, client_secret: str):
    """Returns authenticated YouTube resource. Runs local OAuth flow if needed."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    if _YT_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(_YT_TOKEN_FILE), [_YT_SCOPE])
        if creds and creds.valid:
            return build("youtube", "v3", credentials=creds)

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=[_YT_SCOPE],
    )
    creds = flow.run_local_server(port=8080, open_browser=True)
    _YT_TOKEN_FILE.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def build_video_metadata(pkg: PublicationPackage, genre: str = "Content") -> dict:
    title = pkg.youtube_titles[0] if pkg.youtube_titles else pkg.brief.get("titulo_principal", "")
    tags = [
        "IM Music", "REBEL LUXURY", "marketing", "neurociencia",
        "music business", "industria musical", "Colombia",
    ]
    return {
        "snippet": {
            "title": title[:100],
            "description": pkg.youtube_description[:5000],
            "tags": tags,
            "categoryId": "10",  # Music category
            "defaultLanguage": "es",
        },
        "status": {
            "privacyStatus": "private",  # user reviews before making public
            "selfDeclaredMadeForKids": False,
        },
    }


class YouTubePublisher:
    def __init__(self, client_id: str, client_secret: str, channel_id: str = ""):
        self._client_id = client_id
        self._client_secret = client_secret
        self._channel_id = channel_id
        self._yt = None

    def _get_client(self):
        if self._yt is None:
            if not self._client_id:
                raise RuntimeError("GOOGLE_CLIENT_ID not set in .env")
            self._yt = _build_yt_client(self._client_id, self._client_secret)
        return self._yt

    def upload_video(
        self,
        video_path: Path,
        pkg: PublicationPackage,
        thumbnail_path: Optional[Path] = None,
    ) -> Optional[str]:
        """Uploads video. Returns video_id or None on failure."""
        from googleapiclient.http import MediaFileUpload

        yt = self._get_client()
        metadata = build_video_metadata(pkg)
        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
        try:
            req = yt.videos().insert(part="snippet,status", body=metadata, media_body=media)
            response = None
            while response is None:
                status, response = req.next_chunk()
            video_id = response["id"]
            logger.info(f"Uploaded to YouTube: https://youtu.be/{video_id}")

            if thumbnail_path and thumbnail_path.exists():
                yt.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(str(thumbnail_path)),
                ).execute()

            return video_id
        except Exception as e:
            logger.error(f"YouTube upload failed: {e}")
            return None

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
            logger.error(f"Playlist add failed: {e}")
            return False


_IG_SESSION_FILE  = Path(__file__).resolve().parent.parent.parent / ".instagram_session.json"
_TK_COOKIES_FILE  = Path(__file__).resolve().parent.parent.parent / ".tiktok_cookies.json"


class InstagramPublisher:
    """Posts to Instagram via instagrapi (private API, session-based)."""

    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._cl = None

    def _get_client(self):
        if self._cl is not None:
            return self._cl
        from instagrapi import Client
        cl = Client()
        if _IG_SESSION_FILE.exists():
            cl.load_settings(_IG_SESSION_FILE)
            cl.login(self._username, self._password)
        else:
            cl.login(self._username, self._password)
            cl.dump_settings(_IG_SESSION_FILE)
        self._cl = cl
        return cl

    def post_single(self, image_path: Path, caption: str) -> Optional[str]:
        """Posts a single image from local path to feed."""
        try:
            cl = self._get_client()
            media = cl.photo_upload(image_path, caption=caption[:2200])
            media_id = str(media.pk)
            logger.info(f"Posted to Instagram: {media_id}")
            cl.dump_settings(_IG_SESSION_FILE)
            return media_id
        except Exception as e:
            logger.error(f"Instagram post failed: {e}")
            return None

    def post_reel(self, video_path: Path, caption: str, thumbnail_path: Optional[Path] = None) -> Optional[str]:
        """Posts a Reel from local video file."""
        try:
            cl = self._get_client()
            extra = {"thumbnail": thumbnail_path} if thumbnail_path and thumbnail_path.exists() else {}
            media = cl.clip_upload(video_path, caption=caption[:2200], **extra)
            media_id = str(media.pk)
            logger.info(f"Posted Reel to Instagram: {media_id}")
            cl.dump_settings(_IG_SESSION_FILE)
            return media_id
        except Exception as e:
            logger.error(f"Instagram reel failed: {e}")
            return None

    def post_carousel(self, image_paths: List[Path], caption: str) -> Optional[str]:
        """Posts a carousel from local image files (up to 10)."""
        try:
            cl = self._get_client()
            media = cl.album_upload(image_paths[:10], caption=caption[:2200])
            media_id = str(media.pk)
            logger.info(f"Posted carousel to Instagram: {media_id}")
            cl.dump_settings(_IG_SESSION_FILE)
            return media_id
        except Exception as e:
            logger.error(f"Instagram carousel failed: {e}")
            return None


class TikTokPublisher:
    """Posts to TikTok via tiktok-uploader using session cookies from .tiktok_cookies.json."""

    def _cookies_path(self) -> Optional[str]:
        if _TK_COOKIES_FILE.exists():
            return str(_TK_COOKIES_FILE)
        raise RuntimeError(
            "TikTok cookies not found. Run: python scripts/get_tiktok_cookies.py"
        )

    def post_video(
        self,
        video_path: Path,
        caption: str,
        thumbnail_path: Optional[Path] = None,
    ) -> Optional[str]:
        """Upload a video to TikTok as a regular post."""
        try:
            from tiktok_uploader.upload import upload_video
            cookies = self._cookies_path()
            result = upload_video(
                filename=str(video_path),
                description=caption[:2200],
                cookies=cookies,
            )
            logger.info(f"Posted to TikTok: {result}")
            return str(result) if result else "ok"
        except Exception as e:
            logger.error(f"TikTok upload failed: {e}")
            return None

    def post_photos(
        self,
        image_paths: List[Path],
        caption: str,
    ) -> Optional[str]:
        """Upload a photo carousel (slideshow) to TikTok."""
        try:
            from tiktok_uploader.upload import upload_videos
            cookies = self._cookies_path()
            # tiktok-uploader handles photo posts via upload_video with images
            result = upload_video(
                filename=str(image_paths[0]),
                description=caption[:2200],
                cookies=cookies,
            )
            logger.info(f"Posted photos to TikTok: {result}")
            return str(result) if result else "ok"
        except Exception as e:
            logger.error(f"TikTok photo post failed: {e}")
            return None
