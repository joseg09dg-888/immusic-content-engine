"""
mastering.py — Audio mastering pipeline for IM Music / REBEL LUXURY.

LUFS targets (from Brand):
  Spotify    : -14 LUFS (streaming norm — balanced, consumer-focused)
  YouTube    : -13 LUFS (slightly louder due to normalization headroom)
  Apple Music: -16 LUFS (highest quality bar, wider dynamic range)

Genre-specific EQ guidance (applied as comments / future DSP hooks):
  chill_hop  (85-95 BPM) — "El Viajero Nocturno"
    • Boost sub-bass 40-60 Hz (+2 dB shelf) for warmth
    • Gentle high-shelf cut 12 kHz (-1.5 dB) for lo-fi texture
    • Mid scoop 300-500 Hz (-1 dB) to avoid boxiness
    • Stereo width: moderate (not mono-collapsed, not hyper-wide)

  afro_house (120-128 BPM) — "El Ser Galáctico"
    • Tight kick punch: boost 80-100 Hz (+3 dB), cut 200-300 Hz (-2 dB)
    • Presence boost 3-5 kHz (+1.5 dB) for percussive clarity
    • Air shelf 16 kHz (+1 dB) for spatial nebula feel
    • Stereo width: wide (>30% Haas delay on pads)

Stack: librosa, pydub, pyloudnorm, soundfile, numpy
"""

from __future__ import annotations

import logging
import subprocess
import shutil
from datetime import date
from pathlib import Path
from typing import Dict, Optional

import numpy as np

from src.core.brand import Brand

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Optional heavy imports — fail gracefully if missing in test environments
# ---------------------------------------------------------------------------

def _import_audio_libs():
    """Lazy import of heavy audio libs so the module loads even without them."""
    try:
        import soundfile as sf
        import pyloudnorm as pyln
        import librosa
        return sf, pyln, librosa
    except ImportError as exc:
        raise ImportError(
            f"Audio processing library missing: {exc}. "
            "Install: pip install soundfile pyloudnorm librosa"
        ) from exc


def _require_pydub():
    try:
        from pydub import AudioSegment
        return AudioSegment
    except ImportError as exc:
        raise ImportError(
            "pydub missing. Install: pip install pydub"
        ) from exc


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PLATFORM_LUFS: Dict[str, float] = {
    "spotify": float(Brand.LUFS_SPOTIFY),   # -14
    "youtube": float(Brand.LUFS_YOUTUBE),   # -13
    "apple":   float(Brand.LUFS_APPLE),     # -16
}

_SUPPORTED_GENRES = {"chill_hop", "afro_house"}


def _check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def _normalize_to_lufs(
    samples: np.ndarray,
    sample_rate: int,
    target_lufs: float,
    pyln_module,
) -> np.ndarray:
    """
    Normalize *samples* to *target_lufs* using pyloudnorm integrated loudness.
    Returns float64 numpy array clipped to [-1.0, 1.0].
    """
    meter = pyln_module.Meter(sample_rate)
    # pyloudnorm expects shape (samples, channels) — already correct for 2D input
    audio_2d = samples if samples.ndim == 2 else samples[:, np.newaxis]
    loudness = meter.integrated_loudness(audio_2d)

    if loudness == float("-inf"):
        logger.warning("Integrated loudness is -inf — silent file, skipping gain.")
        return samples

    gain_db = target_lufs - loudness
    gain_linear = 10 ** (gain_db / 20.0)
    normalized = samples * gain_linear
    return np.clip(normalized, -1.0, 1.0)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_loudness(audio_path: str | Path) -> float:
    """
    Measure integrated loudness of *audio_path* in LUFS.

    Parameters
    ----------
    audio_path : str or Path
        Path to any audio file supported by soundfile (WAV, FLAC, AIFF, OGG…).

    Returns
    -------
    float
        Integrated loudness in LUFS. Returns -inf for silent files.
    """
    sf, pyln, _ = _import_audio_libs()
    audio_path = Path(audio_path)
    data, sr = sf.read(str(audio_path), always_2d=True)
    meter = pyln.Meter(sr)
    return meter.integrated_loudness(data)


class MasteringEngine:
    """
    Complete audio mastering pipeline for IM Music REBEL LUXURY releases.

    Workflow
    --------
    1. Load audio via soundfile (preserves bit depth).
    2. Measure current LUFS with pyloudnorm.
    3. For each platform, normalize to target LUFS.
    4. Export to all 4 formats (WAV 24-bit 44.1kHz, MP3 320kbps, FLAC, M4A 256kbps).
    5. Save under ``releases/YYYY-MM-DD_<track-name>/audio/``.

    Parameters
    ----------
    releases_dir : Path, optional
        Root releases directory. Defaults to ``<project_root>/releases``.
    """

    def __init__(self, releases_dir: Optional[Path] = None):
        if releases_dir is None:
            # Infer project root from this file's location (src/music_engine/)
            releases_dir = Path(__file__).resolve().parent.parent.parent / "releases"
        self.releases_dir = Path(releases_dir)

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def get_loudness(self, audio_path: str | Path) -> float:
        """Measure integrated loudness (LUFS). Convenience wrapper."""
        return get_loudness(audio_path)

    def master(
        self,
        input_path: str | Path,
        output_dir: str | Path,
        track_name: str,
        genre: str = "chill_hop",
    ) -> Dict[str, Dict[str, Path]]:
        """
        Full mastering pipeline.

        Parameters
        ----------
        input_path  : Path to source audio (WAV/FLAC/AIFF/OGG).
        output_dir  : Base directory for this release.
                      Actual audio files land in ``output_dir/audio/``.
        track_name  : Human-readable track name (used in filenames).
        genre       : "chill_hop" or "afro_house" (affects future EQ hooks).

        Returns
        -------
        dict
            Nested dict keyed by platform → format → Path.
            Example::

                {
                  "spotify": {"wav": Path("…/spotify_master.wav"), "mp3": …},
                  "youtube": {…},
                  "apple":   {…},
                }
        """
        input_path = Path(input_path)
        output_dir = Path(output_dir)
        audio_dir = output_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        if genre not in _SUPPORTED_GENRES:
            logger.warning(
                f"Unknown genre '{genre}'. Falling back to default mastering. "
                f"Supported: {_SUPPORTED_GENRES}"
            )

        sf, pyln, librosa = _import_audio_libs()

        # 1. Load source
        logger.info(f"Loading: {input_path}")
        data, sr = sf.read(str(input_path), always_2d=True)
        # data shape: (samples, channels) — float64

        # 2. Resample to 44100 Hz if needed
        if sr != 44100:
            logger.info(f"Resampling {sr} Hz → 44100 Hz")
            # librosa works on (channels, samples) mono or (samples,) shape
            data_resampled = []
            for ch in range(data.shape[1]):
                data_resampled.append(
                    librosa.resample(data[:, ch].astype(np.float32), orig_sr=sr, target_sr=44100)
                )
            data = np.stack(data_resampled, axis=1).astype(np.float64)
            sr = 44100

        # 3. Measure source loudness
        meter = pyln.Meter(sr)
        source_lufs = meter.integrated_loudness(data)
        logger.info(f"Source LUFS: {source_lufs:.2f}")

        # 4. Apply genre-specific hints (logged; DSP hooks can be wired here)
        self._log_genre_hints(genre)

        # 5. Normalize per platform and export all formats
        results: Dict[str, Dict[str, Path]] = {}

        for platform, target_lufs in _PLATFORM_LUFS.items():
            normalized = _normalize_to_lufs(data, sr, target_lufs, pyln)
            stem = f"{_slug(track_name)}_{platform}"

            platform_files = self._export_all_formats(
                audio=normalized,
                sr=sr,
                audio_dir=audio_dir,
                stem=stem,
                sf_module=sf,
            )
            results[platform] = platform_files
            logger.info(
                f"[{platform}] normalized to {target_lufs} LUFS → "
                + ", ".join(str(p.name) for p in platform_files.values())
            )

        return results

    # ------------------------------------------------------------------
    # Convenience factory: build output_dir from releases root + today
    # ------------------------------------------------------------------

    def master_release(
        self,
        input_path: str | Path,
        track_name: str,
        genre: str = "chill_hop",
        release_date: Optional[date] = None,
    ) -> Dict[str, Dict[str, Path]]:
        """
        Like :meth:`master` but auto-creates ``releases/YYYY-MM-DD_<track-name>/``.

        Parameters
        ----------
        input_path   : Source audio path.
        track_name   : Track name (used in directory + file names).
        genre        : "chill_hop" or "afro_house".
        release_date : Defaults to today.

        Returns
        -------
        Same nested dict as :meth:`master`.
        """
        if release_date is None:
            release_date = date.today()
        date_str = release_date.strftime("%Y-%m-%d")
        folder_name = f"{date_str}_{_slug(track_name)}"
        output_dir = self.releases_dir / folder_name
        return self.master(input_path, output_dir, track_name, genre)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _export_all_formats(
        self,
        audio: np.ndarray,
        sr: int,
        audio_dir: Path,
        stem: str,
        sf_module,
    ) -> Dict[str, Path]:
        """
        Export *audio* to WAV 24-bit, MP3 320kbps, FLAC, and M4A 256kbps.

        Returns dict mapping format key → output Path.
        """
        files: Dict[str, Path] = {}

        # --- WAV 24-bit 44.1kHz ---
        wav_path = audio_dir / f"{stem}.wav"
        sf_module.write(str(wav_path), audio, sr, subtype="PCM_24")
        files["wav"] = wav_path

        # --- FLAC (lossless) ---
        flac_path = audio_dir / f"{stem}.flac"
        sf_module.write(str(flac_path), audio, sr, format="FLAC", subtype="PCM_24")
        files["flac"] = flac_path

        # --- MP3 320kbps via pydub ---
        mp3_path = audio_dir / f"{stem}.mp3"
        try:
            AudioSegment = _require_pydub()
            mp3_path = self._wav_to_mp3(wav_path, mp3_path, AudioSegment)
            files["mp3"] = mp3_path
        except Exception as e:
            logger.warning(f"MP3 export failed: {e}")

        # --- M4A 256kbps via FFmpeg ---
        m4a_path = audio_dir / f"{stem}.m4a"
        try:
            m4a_path = self._wav_to_m4a(wav_path, m4a_path)
            files["m4a"] = m4a_path
        except Exception as e:
            logger.warning(f"M4A export failed: {e}")

        return files

    @staticmethod
    def _wav_to_mp3(wav_path: Path, mp3_path: Path, AudioSegment) -> Path:
        """Convert WAV → MP3 320kbps using pydub."""
        seg = AudioSegment.from_wav(str(wav_path))
        seg.export(str(mp3_path), format="mp3", bitrate="320k")
        return mp3_path

    @staticmethod
    def _wav_to_m4a(wav_path: Path, m4a_path: Path) -> Path:
        """Convert WAV → M4A 256kbps using FFmpeg (AAC codec)."""
        if not _check_ffmpeg():
            raise RuntimeError(
                "FFmpeg not found — required for M4A export. "
                "Install: winget install Gyan.FFmpeg"
            )
        cmd = [
            "ffmpeg", "-y",
            "-i", str(wav_path),
            "-c:a", "aac",
            "-b:a", "256k",
            str(m4a_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg M4A conversion failed:\n{result.stderr}")
        return m4a_path

    @staticmethod
    def _log_genre_hints(genre: str) -> None:
        """
        Log genre-specific EQ/mastering hints for this session.
        These are advisory only; actual DSP is deferred to the beat generator.

        chill_hop  — warm low-end, lo-fi texture, moderate stereo width
        afro_house — punchy kick, percussive presence, wide pads
        """
        hints = {
            "chill_hop": (
                "EQ: +2 dB sub-bass 40-60 Hz | "
                "-1.5 dB hi-shelf 12 kHz | "
                "-1 dB mid scoop 300-500 Hz | "
                "Stereo: moderate width"
            ),
            "afro_house": (
                "EQ: +3 dB kick 80-100 Hz | "
                "-2 dB 200-300 Hz | "
                "+1.5 dB presence 3-5 kHz | "
                "+1 dB air 16 kHz | "
                "Stereo: wide pads"
            ),
        }
        hint = hints.get(genre, "No genre-specific EQ hint available.")
        logger.info(f"Genre hint [{genre}]: {hint}")


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def _slug(name: str) -> str:
    """Convert track name to a filesystem-safe slug."""
    import re
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "_", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("_-") or "track"
