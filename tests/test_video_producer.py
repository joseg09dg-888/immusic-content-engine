import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.content_engine.video_producer import (
    BrollFetcher,
    build_slideshow_command,
    burn_subtitles_command,
    check_ffmpeg,
    check_whisper,
    _fmt_time,
)


def test_fmt_time_zero():
    assert _fmt_time(0.0) == "00:00:00,000"


def test_fmt_time_one_hour():
    assert _fmt_time(3661.5) == "01:01:01,500"


def test_fmt_time_minutes():
    assert _fmt_time(90.25) == "00:01:30,250"


def test_build_slideshow_command_structure():
    images = [Path("a.jpg"), Path("b.jpg")]
    cmd = build_slideshow_command(images, audio_path=None, output_path=Path("out.mp4"))
    assert cmd[0] == "ffmpeg"
    assert "out.mp4" in cmd
    assert "-filter_complex" in cmd
    assert "concat" in " ".join(cmd)


def test_build_slideshow_command_with_audio():
    images = [Path("a.jpg")]
    cmd = build_slideshow_command(images, Path("audio.mp3"), Path("out.mp4"))
    assert str(Path("audio.mp3")) in cmd
    assert "-shortest" in cmd


def test_build_slideshow_command_no_audio():
    images = [Path("a.jpg")]
    cmd = build_slideshow_command(images, None, Path("out.mp4"))
    assert "-shortest" not in cmd


def test_burn_subtitles_command_es_white():
    cmd = burn_subtitles_command(Path("v.mp4"), Path("s.srt"), Path("out.mp4"), lang="es")
    assert "FFFFFF" in " ".join(cmd)
    assert "ffmpeg" == cmd[0]


def test_burn_subtitles_command_en_violet():
    cmd = burn_subtitles_command(Path("v.mp4"), Path("s.srt"), Path("out.mp4"), lang="en")
    assert "5E17EB" in " ".join(cmd)


def test_broll_fetcher_no_key_returns_empty():
    fetcher = BrollFetcher(pexels_key="", unsplash_key="")
    assert fetcher.fetch_pexels("music") == []
    assert fetcher.fetch_unsplash("music") == []


def test_broll_fetcher_pexels_mock():
    fetcher = BrollFetcher(pexels_key="fake-key")
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "photos": [{"src": {"large2x": "https://pexels.com/img1.jpg"}}]
    }
    mock_response.raise_for_status = MagicMock()
    with patch("requests.get", return_value=mock_response):
        urls = fetcher.fetch_pexels("music", n=1)
    assert urls == ["https://pexels.com/img1.jpg"]


def test_check_ffmpeg_returns_bool():
    result = check_ffmpeg()
    assert isinstance(result, bool)


def test_check_whisper_returns_bool():
    result = check_whisper()
    assert isinstance(result, bool)
