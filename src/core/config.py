import os
from pathlib import Path
from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_ROOT / ".env")


def _require(key: str) -> str:
    val = os.getenv(key, "").strip()
    if not val:
        raise EnvironmentError(f"Required env var missing: {key}")
    return val


def _optional(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


class Config:
    ANTHROPIC_API_KEY: str = _require("ANTHROPIC_API_KEY")
    IM_MUSIC_EMAIL: str = _optional("IM_MUSIC_EMAIL", "immusicsello@gmail.com")

    ASSETS_DIR: Path = _ROOT / "assets"
    RELEASES_DIR: Path = _ROOT / "releases"
    LOGS_DIR: Path = _ROOT / "logs"

    GOOGLE_CLIENT_ID: str = _optional("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = _optional("GOOGLE_CLIENT_SECRET")
    YOUTUBE_CHANNEL_ID: str = _optional("YOUTUBE_CHANNEL_ID")
    META_ACCESS_TOKEN: str = _optional("META_ACCESS_TOKEN")
    TIKTOK_ACCESS_TOKEN: str = _optional("TIKTOK_ACCESS_TOKEN")
    ELEVENLABS_API_KEY: str = _optional("ELEVENLABS_API_KEY")
    PEXELS_API_KEY: str = _optional("PEXELS_API_KEY")

    CLAUDE_MODEL: str = "claude-sonnet-4-6"


config = Config()
