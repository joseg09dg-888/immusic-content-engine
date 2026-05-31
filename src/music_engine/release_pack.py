"""
release_pack.py — Release Pack Generator
=========================================
Creates a fully-structured release folder ready for Nexus distribution.

Folder layout
-------------
releases/YYYY-MM-DD_<track-slug>/
    audio/          ← master audio file(s) go here
    artwork/        ← cover art (3000×3000 JPEG/PNG)
    metadata/
        nexus_delivery.json   ← distributor delivery manifest

Nexus details (from brand.py)
    Distributor : Nexus
    Royalty cut : 8%
    Platforms   : Spotify, Apple Music, YouTube Music, Deezer
"""

from __future__ import annotations

import json
import logging
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_PLATFORMS = ["spotify", "apple_music", "youtube_music", "deezer"]


def _slugify(text: str) -> str:
    """Convert a track name to a filesystem-safe lowercase slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


class ReleasePackGenerator:
    """
    Build a standard release pack folder structure for Nexus delivery.

    Usage
    -----
    >>> gen = ReleasePackGenerator()
    >>> release_dir = gen.generate(
    ...     track_name="Noche Galática",
    ...     audio_dir=Path("releases/beats"),
    ...     artwork_path=Path("assets/covers/night.jpg"),
    ... )
    >>> print(release_dir)
    releases/2026-05-30_noche-galatica/
    """

    def __init__(self, releases_root: Optional[Path | str] = None) -> None:
        if releases_root is None:
            releases_root = Path(__file__).resolve().parent.parent.parent / "releases"
        self._releases_root = Path(releases_root)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        track_name: str,
        audio_dir: Path | str,
        artwork_path: Optional[Path | str] = None,
        genre: str = "",
        bpm: Optional[int] = None,
    ) -> Path:
        """
        Create the release folder, copy audio and artwork, write metadata.

        Parameters
        ----------
        track_name : str
            Human-readable track name (used in folder name and metadata).
        audio_dir : Path or str
            Directory containing the generated beat/audio file(s).
            All WAV/MP3/FLAC files found here are copied to ``audio/``.
        artwork_path : Path or str, optional
            Path to the cover art file. Copied to ``artwork/`` if provided.
        genre : str, optional
            Genre label stored in nexus_delivery.json.
        bpm : int, optional
            BPM stored in nexus_delivery.json.

        Returns
        -------
        Path
            Absolute path of the created release folder.
        """
        audio_dir = Path(audio_dir)
        today = date.today().isoformat()  # YYYY-MM-DD
        slug = _slugify(track_name)
        folder_name = f"{today}_{slug}"
        release_dir = self._releases_root / folder_name

        # ── Create folder structure ─────────────────────────────────────
        for sub in ("audio", "artwork", "metadata"):
            (release_dir / sub).mkdir(parents=True, exist_ok=True)

        logger.info("Created release folder: %s", release_dir)

        # ── Copy audio files ────────────────────────────────────────────
        audio_extensions = {".wav", ".mp3", ".flac", ".aif", ".aiff"}
        audio_files_found = 0
        if audio_dir.is_dir():
            for f in audio_dir.iterdir():
                if f.suffix.lower() in audio_extensions:
                    dest = release_dir / "audio" / f.name
                    shutil.copy2(f, dest)
                    audio_files_found += 1
                    logger.info("Copied audio: %s → %s", f.name, dest)
        else:
            logger.warning("audio_dir does not exist or is not a directory: %s", audio_dir)

        if audio_files_found == 0:
            logger.warning("No audio files found in %s", audio_dir)

        # ── Copy artwork ────────────────────────────────────────────────
        if artwork_path is not None:
            artwork_path = Path(artwork_path)
            if artwork_path.exists():
                dest = release_dir / "artwork" / artwork_path.name
                shutil.copy2(artwork_path, dest)
                logger.info("Copied artwork: %s", artwork_path.name)
            else:
                logger.warning("Artwork not found: %s", artwork_path)

        # ── Write Nexus delivery manifest ───────────────────────────────
        metadata = self._build_nexus_manifest(track_name, genre, bpm)
        manifest_path = release_dir / "metadata" / "nexus_delivery.json"
        manifest_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
        logger.info("Nexus manifest written: %s", manifest_path)

        return release_dir

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_nexus_manifest(
        track_name: str,
        genre: str,
        bpm: Optional[int],
    ) -> dict:
        """Return the nexus_delivery.json payload."""
        return {
            "track_name": track_name,
            "isrc_placeholder": "PENDING_ISRC",
            "genre": genre,
            "bpm": bpm,
            "distributor": "Nexus",
            "royalty_cut": 0.08,
            "platforms": _PLATFORMS,
            "label": "IM Music",
            "brand_concept": "REBEL LUXURY",
            "release_date": date.today().isoformat(),
        }
