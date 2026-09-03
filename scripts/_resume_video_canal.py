"""Resume: re-renderiza solo video_canal.mp4 de un run que quedo cortado,
reusando slides/audio/captions ya generados (evita repetir research/imagenes/TTS)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402

work_dir = ROOT / "releases" / "run_20260903_112251"
canal_dir = work_dir / "canal_slides"
audio_canal = work_dir / "narration_canal.mp3"
captions_canal = work_dir / "narration_canal.ass"
long_path = work_dir / "video_canal.mp4"

canal_slide_paths = sorted(canal_dir.glob("slide_*.png"))
secs_per_slide = max(18.0, 520.0 / max(len(canal_slide_paths), 1))

print(f"Slides: {len(canal_slide_paths)}, secs/slide: {secs_per_slide:.1f}")
print(f"Captions ass exists: {captions_canal.exists()}")

ok = pipeline.create_long_video(
    canal_slide_paths, audio_canal, long_path,
    secs=secs_per_slide,
    captions_ass=captions_canal if captions_canal.exists() else None,
)
print(f"OK: {ok}, size: {long_path.stat().st_size // 1024 // 1024 if long_path.exists() else 0}MB")
