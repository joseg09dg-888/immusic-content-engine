"""
beat_generator.py — REBEL LUXURY Beat Generator
================================================
Wraps AudioCraft/MusicGen to generate Chill Hop and Afro House beats
for IM Music (@immusicsello).

Installation (requires GPU recommended):
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip install audiocraft

Supported genres:
    - chill_hop  : 85-95 BPM | El Viajero Nocturno
    - afro_house : 120-128 BPM | El Ser Galáctico
"""

from __future__ import annotations

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

# Default BPM per genre (centre of the official range)
_GENRE_DEFAULTS: dict[str, dict] = {
    "chill_hop": {
        "bpm": 90,
        "prompt": (
            "chill hop beat, lo-fi, 90bpm, dreamy, nocturnal city vibes, vinyl crackle"
        ),
    },
    "afro_house": {
        "bpm": 124,
        "prompt": (
            "afro house beat, 124bpm, deep bass, tribal percussion, galactic atmosphere"
        ),
    },
}

_AUDIOCRAFT_MISSING_MSG = (
    "AudioCraft not installed. Run:\n"
    "  pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118\n"
    "  pip install audiocraft"
)


class BeatGenerator:
    """
    Generate beats for IM Music using Meta's MusicGen model (AudioCraft).

    Usage
    -----
    >>> gen = BeatGenerator()
    >>> if gen.is_available():
    ...     path = gen.generate("chill_hop", bpm=90, duration_sec=170)
    ...     print(path)

    Notes
    -----
    - AudioCraft requires PyTorch. If not installed, `generate()` raises RuntimeError.
    - Default model: "facebook/musicgen-medium" (good balance of quality/VRAM).
    - Output is a 32-bit float WAV file ready for mastering.
    """

    def __init__(self, model_name: str = "facebook/musicgen-medium") -> None:
        self._model_name = model_name
        self._model = None  # lazy-loaded on first generate()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """Return True if AudioCraft/MusicGen can be imported, False otherwise."""
        try:
            import audiocraft.models  # noqa: F401
            return True
        except ImportError:
            return False

    def generate(
        self,
        genre: str,
        bpm: Optional[int] = None,
        duration_sec: int = 170,
        output_dir: Optional[Path | str] = None,
    ) -> Path:
        """
        Generate a beat for the given genre and save it as a WAV file.

        Parameters
        ----------
        genre : str
            One of "chill_hop" or "afro_house".
        bpm : int, optional
            Desired BPM. Falls back to genre default if not provided.
        duration_sec : int
            Length in seconds (default 170 — max song length per brand.py).
        output_dir : Path or str, optional
            Directory to write the output WAV. Defaults to ``releases/beats/``.

        Returns
        -------
        Path
            Absolute path to the generated WAV file.

        Raises
        ------
        RuntimeError
            If AudioCraft/PyTorch is not installed.
        ValueError
            If an unsupported genre is requested.
        """
        # Guard: AudioCraft must be available
        try:
            from audiocraft.models import MusicGen
        except ImportError:
            raise RuntimeError(_AUDIOCRAFT_MISSING_MSG)

        # Validate genre
        genre_key = genre.lower().replace(" ", "_").replace("-", "_")
        if genre_key not in _GENRE_DEFAULTS:
            raise ValueError(
                f"Unsupported genre '{genre}'. Choose from: {list(_GENRE_DEFAULTS)}"
            )

        cfg = _GENRE_DEFAULTS[genre_key]
        effective_bpm = bpm if bpm is not None else cfg["bpm"]

        # Build prompt — inject actual BPM if caller overrides default
        prompt = cfg["prompt"]
        if bpm is not None:
            # Replace the BPM token in the prompt so MusicGen sees the right value
            import re
            prompt = re.sub(r"\d+bpm", f"{bpm}bpm", prompt)

        logger.info(
            "Generating %s beat | BPM=%d | duration=%ds | model=%s",
            genre_key,
            effective_bpm,
            duration_sec,
            self._model_name,
        )

        # Lazy-load model
        if self._model is None:
            logger.info("Loading MusicGen model '%s' …", self._model_name)
            self._model = MusicGen.get_pretrained(self._model_name)

        self._model.set_generation_params(duration=duration_sec)
        wav = self._model.generate([prompt])  # shape: (1, channels, samples)

        # Resolve output directory
        if output_dir is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            output_dir = project_root / "releases" / "beats"
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{genre_key}_{effective_bpm}bpm_{timestamp}.wav"
        output_path = output_dir / filename

        # Save with audiocraft utility
        from audiocraft.data.audio import audio_write

        stem = output_path.with_suffix("")  # audio_write appends .wav itself
        audio_write(
            str(stem),
            wav[0].cpu(),
            self._model.sample_rate,
            strategy="loudness",
            loudness_compressor=True,
        )

        logger.info("Beat saved: %s", output_path)
        return output_path
