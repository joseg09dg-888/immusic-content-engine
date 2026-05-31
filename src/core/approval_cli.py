"""
approval_cli.py — Manual Beat Approval (A&R Gate)
==================================================
IM Music rule: ALL beats require manual human approval before entering
the release pipeline. This module provides the terminal-based approval
flow. The user is always the A&R.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def approve_beat(
    audio_path: str | Path,
    track_name: str,
    genre: str,
    bpm: int,
) -> bool:
    """
    Present beat info in the terminal and ask the user for approval.

    Attempts to play a preview via pydub/simpleaudio if available;
    otherwise prints the file path so the user can open it manually.

    Parameters
    ----------
    audio_path : str or Path
        Path to the generated audio file (WAV/MP3).
    track_name : str
        Human-readable name for the track.
    genre : str
        Genre label (e.g. "Chill Hop", "Afro House").
    bpm : int
        Beats per minute of the track.

    Returns
    -------
    bool
        True if the user approves (enters 'y'), False otherwise.
    """
    audio_path = Path(audio_path)

    # ── Print track card ────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("  IM MUSIC — REBEL LUXURY  |  A&R Beat Approval Gate")
    print("=" * 60)
    print(f"  Track     : {track_name}")
    print(f"  Genre     : {genre}")
    print(f"  BPM       : {bpm}")
    print(f"  File      : {audio_path}")
    print(f"  Exists    : {'YES' if audio_path.exists() else 'NO — check path'}")
    print("=" * 60)

    # ── Attempt audio preview ───────────────────────────────────────────
    _try_play_preview(audio_path)

    # ── Prompt ─────────────────────────────────────────────────────────
    try:
        answer = _prompt_user()
    except KeyboardInterrupt:
        print("\n[Approval interrupted — beat REJECTED]")
        logger.warning("Beat approval interrupted by user (KeyboardInterrupt).")
        return False

    approved = answer.strip().lower() in {"y", "yes", "s", "si", "sí"}

    status = "APPROVED" if approved else "REJECTED"
    print(f"\n  Beat {status}: {track_name}")
    print()
    logger.info("Beat '%s' %s by A&R.", track_name, status.lower())

    return approved


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _try_play_preview(audio_path: Path, max_seconds: int = 30) -> None:
    """
    Try to play up to `max_seconds` of audio using pydub + simpleaudio.
    Gracefully skips if the libraries or the file are unavailable.
    """
    if not audio_path.exists():
        print("  [Preview] File not found — open it manually to listen.")
        return

    try:
        from pydub import AudioSegment
        from pydub.playback import play

        print(f"  [Preview] Playing first {max_seconds}s …  (Ctrl+C to skip)")
        audio = AudioSegment.from_file(str(audio_path))
        snippet = audio[: max_seconds * 1000]
        play(snippet)
        print("  [Preview] Done.")
    except KeyboardInterrupt:
        print("\n  [Preview] Skipped.")
    except ImportError:
        print(
            "  [Preview] pydub not installed — open the file manually:\n"
            f"    {audio_path}"
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  [Preview] Could not play audio ({exc}).")
        print(f"    Open manually: {audio_path}")


def _prompt_user() -> str:
    """Display the yes/no prompt and return raw input."""
    print()
    return input("  Approve this beat? [y/n] → ").strip()
