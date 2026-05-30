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


class InstagramPublisher:
    """Posts to Instagram via Meta Graph API (requires Business account)."""

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
        """Posts a single image to feed. image_url must be publicly accessible."""
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
            logger.info(f"Posted to Instagram: {media_id}")
            return media_id
        except Exception as e:
            logger.error(f"Instagram post failed: {e}")
            return None

    def post_carousel(self, image_urls: List[str], caption: str) -> Optional[str]:
        """Posts a carousel (up to 10 images)."""
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
            logger.error(f"Instagram carousel failed: {e}")
            return None
