"""Test real YouTube upload — uploads test_video.mp4 as private."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.config import Config
from src.content_engine.publisher import YouTubePublisher, build_video_metadata
from src.content_engine.writer import PublicationPackage

VIDEO = Path(__file__).resolve().parent.parent / "logs" / "test_video.mp4"
THUMB = Path(__file__).resolve().parent.parent / "logs" / "test_fix" / "thumb_test.png"

pkg = PublicationPackage(
    brief={
        "titulo_principal": "TEST IM Music",
        "angulo_neurociencia": "Test upload",
        "hook_apertura": "Test",
        "datos_clave": [],
        "controversia": "",
        "fuentes": [],
    },
    script_es="Test video IM Music content engine.",
    captions_instagram="",
    caption_tiktok="",
    youtube_titles=["[TEST] IM Music Content Engine — REBEL LUXURY"],
    youtube_description="Video de prueba. Privado. IM Music sello discografico.",
)

print("=" * 50)
print("YOUTUBE — subida real")
print("=" * 50)
print(f"Canal:  {Config.YOUTUBE_CHANNEL_ID}")
print(f"Video:  {VIDEO}")
print(f"Thumb:  {THUMB}")
print()

if not VIDEO.exists():
    print("ERROR: video no encontrado")
    sys.exit(1)

yt = YouTubePublisher(channel_id=Config.YOUTUBE_CHANNEL_ID)

# Verify auth first
print("Verificando autenticacion...")
client = yt._get_client()
result = client.channels().list(part="snippet", mine=True).execute()
channels = result.get("items", [])
if channels:
    print(f"OK - Canal: {channels[0]['snippet']['title']}")
else:
    print("WARN - Autenticado pero sin canal")

# Upload
print()
print("Subiendo video (privado)...")
video_id = yt.upload_video(
    video_path=VIDEO,
    pkg=pkg,
    thumbnail_path=THUMB if THUMB.exists() else None,
    is_short=False,
)

if video_id:
    print(f"OK - PUBLICADO (privado): https://studio.youtube.com/video/{video_id}/edit")
    print(f"     Video ID: {video_id}")
else:
    print("ERROR - Upload fallido")
    sys.exit(1)
