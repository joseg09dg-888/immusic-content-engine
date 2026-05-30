import pytest
from unittest.mock import MagicMock, patch
from src.content_engine.publisher import (
    YouTubePublisher,
    InstagramPublisher,
    build_video_metadata,
)
from src.content_engine.writer import PublicationPackage


_PKG = PublicationPackage(
    brief={"titulo_principal": "Test Title", "angulo_neurociencia": "X",
           "hook_apertura": "H", "datos_clave": [], "controversia": "C", "fuentes": []},
    script_es="Script aquí.",
    captions_instagram="Caption IG #RebelLuxury",
    caption_tiktok="TikTok caption",
    youtube_titles=["Título SEO 1", "Título SEO 2", "Título SEO 3"],
    youtube_description="Descripción completa de YouTube.",
)


def test_build_video_metadata_structure():
    meta = build_video_metadata(_PKG)
    assert "snippet" in meta
    assert "status" in meta
    assert meta["snippet"]["title"] == "Título SEO 1"
    assert len(meta["snippet"]["title"]) <= 100
    assert "IM Music" in meta["snippet"]["tags"]
    assert meta["status"]["privacyStatus"] == "private"


def test_build_video_metadata_description():
    meta = build_video_metadata(_PKG)
    assert meta["snippet"]["description"] == "Descripción completa de YouTube."


def test_build_video_metadata_language():
    meta = build_video_metadata(_PKG)
    assert meta["snippet"]["defaultLanguage"] == "es"


def test_build_video_metadata_empty_titles():
    pkg = PublicationPackage(
        brief={"titulo_principal": "Fallback Title", "angulo_neurociencia": "",
               "hook_apertura": "", "datos_clave": [], "controversia": "", "fuentes": []},
        script_es="", captions_instagram="", caption_tiktok="",
        youtube_titles=[],
        youtube_description="",
    )
    meta = build_video_metadata(pkg)
    assert meta["snippet"]["title"] == "Fallback Title"


def test_youtube_publisher_no_credentials_raises():
    yt = YouTubePublisher(client_id="", client_secret="")
    with pytest.raises(RuntimeError, match="GOOGLE_CLIENT_ID"):
        yt._get_client()


def test_instagram_publisher_post_mock():
    ig = InstagramPublisher(access_token="fake-token", ig_account_id="123456")
    mock_response = MagicMock()
    mock_response.json.side_effect = [{"id": "container_1"}, {"id": "media_1"}]
    mock_response.raise_for_status = MagicMock()
    with patch("requests.post", return_value=mock_response):
        result = ig.post_single("https://example.com/img.jpg", "Caption #IMMusic")
    assert result == "media_1"


def test_instagram_publisher_carousel_mock():
    ig = InstagramPublisher(access_token="fake-token", ig_account_id="123456")
    call_count = 0

    def mock_post(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        m = MagicMock()
        m.json.return_value = {"id": f"id_{call_count}"}
        m.raise_for_status = MagicMock()
        return m

    with patch("requests.post", side_effect=mock_post):
        result = ig.post_carousel(
            ["https://example.com/1.jpg", "https://example.com/2.jpg"],
            "Carousel caption",
        )
    assert result is not None
