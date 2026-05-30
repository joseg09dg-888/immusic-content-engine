import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional
import requests
from src.core.brand import Brand, ContentDurations

logger = logging.getLogger(__name__)

_PEXELS_BASE = "https://api.pexels.com/v1"
_UNSPLASH_BASE = "https://api.unsplash.com"


def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def check_whisper() -> bool:
    try:
        import whisper  # noqa: F401
        return True
    except ImportError:
        return False


def _require_ffmpeg():
    if not check_ffmpeg():
        raise RuntimeError(
            "FFmpeg not found. Install: winget install Gyan.FFmpeg  "
            "then restart your terminal."
        )


class BrollFetcher:
    def __init__(self, pexels_key: str = "", unsplash_key: str = ""):
        self._pexels = pexels_key
        self._unsplash = unsplash_key

    def fetch_pexels(self, query: str, n: int = 10) -> List[str]:
        if not self._pexels:
            logger.warning("PEXELS_API_KEY not set — skipping Pexels fetch.")
            return []
        try:
            r = requests.get(
                f"{_PEXELS_BASE}/search",
                headers={"Authorization": self._pexels},
                params={"query": query, "per_page": n, "orientation": "landscape"},
                timeout=10,
            )
            r.raise_for_status()
            return [p["src"]["large2x"] for p in r.json().get("photos", [])]
        except Exception as e:
            logger.warning(f"Pexels fetch failed: {e}")
            return []

    def fetch_unsplash(self, query: str, n: int = 10) -> List[str]:
        if not self._unsplash:
            logger.warning("UNSPLASH_ACCESS_KEY not set — skipping Unsplash fetch.")
            return []
        try:
            r = requests.get(
                f"{_UNSPLASH_BASE}/search/photos",
                headers={"Authorization": f"Client-ID {self._unsplash}"},
                params={"query": query, "per_page": n},
                timeout=10,
            )
            r.raise_for_status()
            return [p["urls"]["regular"] for p in r.json().get("results", [])]
        except Exception as e:
            logger.warning(f"Unsplash fetch failed: {e}")
            return []

    def download_images(self, urls: List[str], dest_dir: Path, max_n: int = 10) -> List[Path]:
        dest_dir.mkdir(parents=True, exist_ok=True)
        paths = []
        for i, url in enumerate(urls[:max_n]):
            try:
                r = requests.get(url, timeout=15)
                r.raise_for_status()
                p = dest_dir / f"broll_{i:03d}.jpg"
                p.write_bytes(r.content)
                paths.append(p)
            except Exception as e:
                logger.warning(f"Image download failed [{url}]: {e}")
        return paths


def build_slideshow_command(
    image_paths: List[Path],
    audio_path: Optional[Path],
    output_path: Path,
    duration_per_image: float = 5.0,
    size: tuple = (1920, 1080),
) -> List[str]:
    """Returns the FFmpeg command list (does not execute)."""
    cmd = ["ffmpeg", "-y"]
    for p in image_paths:
        cmd += ["-loop", "1", "-t", str(duration_per_image), "-i", str(p)]
    if audio_path:
        cmd += ["-i", str(audio_path)]

    # Filter: scale + pad each image to target size, then concat
    n = len(image_paths)
    scale_filter = "".join(
        f"[{i}:v]scale={size[0]}:{size[1]}:force_original_aspect_ratio=decrease,"
        f"pad={size[0]}:{size[1]}:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}];"
        for i in range(n)
    )
    concat_inputs = "".join(f"[v{i}]" for i in range(n))
    filter_complex = f"{scale_filter}{concat_inputs}concat=n={n}:v=1:a=0[vout]"

    cmd += ["-filter_complex", filter_complex, "-map", "[vout]"]
    if audio_path:
        cmd += ["-map", f"{n}:a", "-shortest"]
    cmd += ["-c:v", "libx264", "-crf", "23", "-preset", "fast", str(output_path)]
    return cmd


def burn_subtitles_command(
    video_path: Path,
    srt_path: Path,
    output_path: Path,
    lang: str = "es",
) -> List[str]:
    """Returns FFmpeg command to burn subtitles onto video."""
    from src.core.brand import Brand
    color = "FFFFFF" if lang == "es" else Brand.VIOLET.lstrip("#")
    return [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"subtitles={str(srt_path)}:force_style='FontSize=24,PrimaryColour=&H{color}&'",
        "-c:a", "copy",
        str(output_path),
    ]


def transcribe_to_srt(audio_path: Path, output_srt: Path, language: str = "en") -> Path:
    """Transcribes audio to SRT using Whisper. Requires whisper package."""
    if not check_whisper():
        raise RuntimeError("Whisper not installed. Run: pip install openai-whisper")
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(str(audio_path), language=language, task="transcribe")
    _write_srt(result["segments"], output_srt)
    return output_srt


def _write_srt(segments: list, path: Path):
    lines = []
    for i, seg in enumerate(segments, 1):
        start = _fmt_time(seg["start"])
        end = _fmt_time(seg["end"])
        lines.append(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n")
    path.write_text("\n".join(lines), encoding="utf-8")


def _fmt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


class VideoProducer:
    def __init__(self, pexels_key: str = "", unsplash_key: str = ""):
        self.fetcher = BrollFetcher(pexels_key, unsplash_key)

    def produce_youtube(
        self,
        title: str,
        script: str,
        audio_path: Optional[Path],
        work_dir: Path,
    ) -> Optional[Path]:
        """
        Full pipeline: fetch broll → slideshow → burn subtitles → YouTube MP4.
        Returns output path or None if FFmpeg missing.
        """
        if not check_ffmpeg():
            logger.warning("FFmpeg not installed — skipping video production.")
            return None

        work_dir.mkdir(parents=True, exist_ok=True)

        # Fetch B-roll
        query = " ".join(title.split()[:4])
        urls = self.fetcher.fetch_pexels(query, n=12) or self.fetcher.fetch_unsplash(query, n=12)
        img_dir = work_dir / "broll"
        images = self.fetcher.download_images(urls, img_dir, max_n=10) if urls else []

        if not images:
            logger.warning("No B-roll images found — using galaxy placeholder.")
            from src.content_engine.designer import Designer
            placeholder = work_dir / "placeholder.png"
            Designer().generate_thumbnail(title, save_path=placeholder)
            images = [placeholder]

        # Build video
        raw_video = work_dir / "raw.mp4"
        cmd = build_slideshow_command(images, audio_path, raw_video)
        subprocess.run(cmd, check=True, capture_output=True)

        # Subtitles (EN only — ES requires audio/voiceover)
        final_video = work_dir / "youtube_final.mp4"
        if audio_path and check_whisper():
            srt_en = work_dir / "subtitles_en.srt"
            try:
                transcribe_to_srt(audio_path, srt_en, language="en")
                cmd_sub = burn_subtitles_command(raw_video, srt_en, final_video, lang="en")
                subprocess.run(cmd_sub, check=True, capture_output=True)
            except Exception as e:
                logger.warning(f"Subtitle burn failed: {e} — using raw video.")
                final_video = raw_video
        else:
            final_video = raw_video

        logger.info(f"Video produced: {final_video}")
        return final_video
