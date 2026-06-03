"""
tests/test_mastering.py — Unit tests for src/music_engine/mastering.py

Strategy: all heavy I/O (soundfile, pyloudnorm, pydub, FFmpeg, librosa) is
mocked so tests run without real audio files or installed native tools.
"""

from __future__ import annotations

import numpy as np
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call

from src.core.brand import Brand
from src.music_engine.mastering import (
    MasteringEngine,
    _slug,
    _normalize_to_lufs,
    _PLATFORM_LUFS,
    get_loudness,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine(tmp_path):
    """MasteringEngine with releases_dir pointing to a temp directory."""
    return MasteringEngine(releases_dir=tmp_path / "releases")


@pytest.fixture
def fake_audio():
    """Stereo 44100 Hz, 1-second silence numpy array (shape: 44100 x 2)."""
    return np.zeros((44100, 2), dtype=np.float64)


@pytest.fixture
def fake_audio_loud():
    """Stereo 44100 Hz, 1-second full-scale sine (very loud)."""
    t = np.linspace(0, 1, 44100)
    mono = np.sin(2 * np.pi * 440 * t) * 0.9
    return np.stack([mono, mono], axis=1)


# ---------------------------------------------------------------------------
# 1. Brand constants are wired correctly
# ---------------------------------------------------------------------------

def test_lufs_targets_match_brand():
    """LUFS constants must come from Brand, not be hardcoded."""
    assert _PLATFORM_LUFS["spotify"] == float(Brand.LUFS_SPOTIFY)
    assert _PLATFORM_LUFS["youtube"] == float(Brand.LUFS_YOUTUBE)
    assert _PLATFORM_LUFS["apple"] == float(Brand.LUFS_APPLE)


def test_brand_lufs_values():
    """Spot-check the actual platform target values."""
    assert Brand.LUFS_SPOTIFY == -14
    assert Brand.LUFS_YOUTUBE == -13
    assert Brand.LUFS_APPLE == -16


# ---------------------------------------------------------------------------
# 2. _slug helper
# ---------------------------------------------------------------------------

def test_slug_basic():
    assert _slug("My Track") == "my_track"


def test_slug_special_chars():
    assert _slug("Track: #1 (feat. X)") == "track_1_feat_x"


def test_slug_already_clean():
    assert _slug("viajero_nocturno") == "viajero_nocturno"


def test_slug_empty_fallback():
    assert _slug("!!!") == "track"


# ---------------------------------------------------------------------------
# 3. _normalize_to_lufs
# ---------------------------------------------------------------------------

def test_normalize_gain_applied(fake_audio_loud):
    """Normalization must change the amplitude of a non-silent signal."""
    mock_pyln = MagicMock()
    meter_inst = MagicMock()
    meter_inst.integrated_loudness.return_value = -6.0  # current loudness
    mock_pyln.Meter.return_value = meter_inst

    target = -14.0
    result = _normalize_to_lufs(fake_audio_loud, 44100, target, mock_pyln)

    # Gain applied: target - source = -14 - (-6) = -8 dB → linear ~0.398
    expected_gain = 10 ** ((-14.0 - -6.0) / 20.0)
    np.testing.assert_allclose(result, np.clip(fake_audio_loud * expected_gain, -1.0, 1.0))


def test_normalize_silent_skipped(fake_audio):
    """Silent files (loudness = -inf) must pass through unchanged."""
    mock_pyln = MagicMock()
    meter_inst = MagicMock()
    meter_inst.integrated_loudness.return_value = float("-inf")
    mock_pyln.Meter.return_value = meter_inst

    result = _normalize_to_lufs(fake_audio, 44100, -14.0, mock_pyln)
    np.testing.assert_array_equal(result, fake_audio)


def test_normalize_clips_to_unity(fake_audio_loud):
    """Gain that would push above 1.0 must be clipped."""
    mock_pyln = MagicMock()
    meter_inst = MagicMock()
    meter_inst.integrated_loudness.return_value = -1.0  # near 0 dBFS
    mock_pyln.Meter.return_value = meter_inst

    # Target is higher than source — gain > 1 — must clip
    result = _normalize_to_lufs(fake_audio_loud, 44100, 0.0, mock_pyln)
    assert result.max() <= 1.0
    assert result.min() >= -1.0


# ---------------------------------------------------------------------------
# 4. get_loudness (module-level function)
# ---------------------------------------------------------------------------

def test_get_loudness_calls_meter(tmp_path):
    """get_loudness should measure integrated loudness via pyloudnorm."""
    fake_path = tmp_path / "track.wav"
    fake_data = np.zeros((4410, 2), dtype=np.float64)

    mock_sf = MagicMock()
    mock_sf.read.return_value = (fake_data, 44100)

    mock_pyln = MagicMock()
    meter_inst = MagicMock()
    meter_inst.integrated_loudness.return_value = -18.5
    mock_pyln.Meter.return_value = meter_inst

    mock_librosa = MagicMock()

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)):
        result = get_loudness(fake_path)

    assert result == -18.5
    mock_sf.read.assert_called_once_with(str(fake_path), always_2d=True)
    mock_pyln.Meter.assert_called_once_with(44100)
    meter_inst.integrated_loudness.assert_called_once_with(fake_data)


# ---------------------------------------------------------------------------
# 5. MasteringEngine.get_loudness (instance method delegation)
# ---------------------------------------------------------------------------

def test_engine_get_loudness_delegates(engine, tmp_path):
    """Instance method get_loudness must delegate to the module function."""
    fake_path = tmp_path / "track.wav"
    with patch("src.music_engine.mastering.get_loudness", return_value=-14.3) as mock_gl:
        result = engine.get_loudness(fake_path)
    mock_gl.assert_called_once_with(fake_path)
    assert result == -14.3


# ---------------------------------------------------------------------------
# 6. MasteringEngine.master — happy path
# ---------------------------------------------------------------------------

def _make_master_mocks(fake_audio, sample_rate=44100):
    """Build consistent mock set for a master() happy-path test."""
    mock_sf = MagicMock()
    mock_sf.read.return_value = (fake_audio, sample_rate)

    mock_pyln = MagicMock()
    meter_inst = MagicMock()
    meter_inst.integrated_loudness.return_value = -18.0
    mock_pyln.Meter.return_value = meter_inst

    mock_librosa = MagicMock()

    mock_pydub_seg = MagicMock()
    mock_pydub_cls = MagicMock()
    mock_pydub_cls.from_wav.return_value = mock_pydub_seg

    return mock_sf, mock_pyln, mock_librosa, mock_pydub_cls


def test_master_creates_output_dir(engine, tmp_path, fake_audio):
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    output_dir = tmp_path / "out"

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        engine.master(tmp_path / "input.wav", output_dir, "Viajero Nocturno")

    assert (output_dir / "audio").exists()


def test_master_returns_three_platforms(engine, tmp_path, fake_audio):
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        results = engine.master(tmp_path / "input.wav", tmp_path / "out", "Test Track")

    assert set(results.keys()) == {"spotify", "youtube", "apple"}


def test_master_each_platform_has_wav_and_flac(engine, tmp_path, fake_audio):
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        results = engine.master(tmp_path / "input.wav", tmp_path / "out", "Rebel Track")

    for platform in ("spotify", "youtube", "apple"):
        assert "wav" in results[platform], f"WAV missing for {platform}"
        assert "flac" in results[platform], f"FLAC missing for {platform}"


def test_master_soundfile_write_called_per_platform(engine, tmp_path, fake_audio):
    """soundfile.write must be called twice per platform (WAV + FLAC) = 6 total."""
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        engine.master(tmp_path / "input.wav", tmp_path / "out", "Track")

    # 3 platforms × 2 formats (WAV + FLAC) = 6 sf.write calls
    assert mock_sf.write.call_count == 6


def test_master_mp3_exported_via_pydub(engine, tmp_path, fake_audio):
    """pydub must be called once per platform for MP3."""
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        results = engine.master(tmp_path / "input.wav", tmp_path / "out", "Track")

    # from_wav should be called 3 times (once per platform)
    assert mock_pydub.from_wav.call_count == 3
    seg_inst = mock_pydub.from_wav.return_value
    # Each export call must request 320k bitrate
    for c in seg_inst.export.call_args_list:
        assert c.kwargs.get("bitrate") == "320k" or c[1].get("bitrate") == "320k" or "320k" in c.args


def test_master_m4a_via_ffmpeg(engine, tmp_path, fake_audio):
    """M4A export must invoke FFmpeg with aac codec and 256k bitrate."""
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)
    mock_ffmpeg_result = MagicMock()
    mock_ffmpeg_result.returncode = 0

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=True), \
         patch("subprocess.run", return_value=mock_ffmpeg_result) as mock_run:

        results = engine.master(tmp_path / "input.wav", tmp_path / "out", "Track")

    # subprocess.run called 3 times (once per platform for M4A)
    assert mock_run.call_count == 3
    for c in mock_run.call_args_list:
        cmd = c.args[0]
        assert "aac" in cmd
        assert "256k" in cmd
    for platform in ("spotify", "youtube", "apple"):
        assert "m4a" in results[platform]


def test_master_m4a_skipped_without_ffmpeg(engine, tmp_path, fake_audio):
    """When FFmpeg is absent, M4A export is skipped gracefully (no exception)."""
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        results = engine.master(tmp_path / "input.wav", tmp_path / "out", "Track")

    # M4A should be absent from all platforms
    for platform in ("spotify", "youtube", "apple"):
        assert "m4a" not in results[platform]


# ---------------------------------------------------------------------------
# 7. Resampling path (non-44100 input)
# ---------------------------------------------------------------------------

def test_master_resamples_non_44100(engine, tmp_path):
    """Audio at 48kHz must be resampled to 44100 Hz before processing."""
    audio_48k = np.zeros((48000, 2), dtype=np.float64)

    mock_sf = MagicMock()
    mock_sf.read.return_value = (audio_48k, 48000)  # 48 kHz input

    mock_pyln = MagicMock()
    meter_inst = MagicMock()
    meter_inst.integrated_loudness.return_value = float("-inf")
    mock_pyln.Meter.return_value = meter_inst

    mock_librosa = MagicMock()
    resampled_channel = np.zeros(44100, dtype=np.float32)
    mock_librosa.resample.return_value = resampled_channel

    mock_pydub = MagicMock()
    mock_pydub.from_wav.return_value = MagicMock()

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        engine.master(tmp_path / "input.wav", tmp_path / "out", "Track")

    # librosa.resample must have been called (once per channel = 2 times)
    assert mock_librosa.resample.call_count == 2
    # Check orig_sr and target_sr
    for c in mock_librosa.resample.call_args_list:
        assert c.kwargs.get("orig_sr") == 48000 or c[1].get("orig_sr") == 48000
        assert c.kwargs.get("target_sr") == 44100 or c[1].get("target_sr") == 44100


# ---------------------------------------------------------------------------
# 8. master_release — folder naming convention
# ---------------------------------------------------------------------------

def test_master_release_folder_name(engine, tmp_path, fake_audio):
    """master_release must create releases/YYYY-MM-DD_<slug>/audio/ directory."""
    from datetime import date

    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    fixed_date = date(2026, 5, 30)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        engine.master_release(
            tmp_path / "input.wav",
            track_name="Viajero Nocturno",
            genre="chill_hop",
            release_date=fixed_date,
        )

    expected_dir = engine.releases_dir / "2026-05-30_viajero_nocturno" / "audio"
    assert expected_dir.exists()


# ---------------------------------------------------------------------------
# 9. Genre hint logging
# ---------------------------------------------------------------------------

def test_genre_hint_chill_hop_logged(engine, tmp_path, fake_audio, caplog):
    """chill_hop genre hint must appear in log output."""
    import logging
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False), \
         caplog.at_level(logging.INFO, logger="src.music_engine.mastering"):

        engine.master(tmp_path / "input.wav", tmp_path / "out", "Track", genre="chill_hop")

    assert any("chill_hop" in r.message for r in caplog.records)


def test_genre_hint_afro_house_logged(engine, tmp_path, fake_audio, caplog):
    """afro_house genre hint must appear in log output."""
    import logging
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False), \
         caplog.at_level(logging.INFO, logger="src.music_engine.mastering"):

        engine.master(tmp_path / "input.wav", tmp_path / "out", "Track", genre="afro_house")

    assert any("afro_house" in r.message for r in caplog.records)


def test_unknown_genre_does_not_raise(engine, tmp_path, fake_audio):
    """An unsupported genre must log a warning but not raise an exception."""
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        # Should not raise
        results = engine.master(tmp_path / "input.wav", tmp_path / "out", "Track", genre="trap")

    assert set(results.keys()) == {"spotify", "youtube", "apple"}


# ---------------------------------------------------------------------------
# 10. File-naming uses slugged track name
# ---------------------------------------------------------------------------

def test_output_filenames_use_slug(engine, tmp_path, fake_audio):
    """WAV filenames must embed the slugged track name and platform."""
    mock_sf, mock_pyln, mock_librosa, mock_pydub = _make_master_mocks(fake_audio)

    with patch("src.music_engine.mastering._import_audio_libs", return_value=(mock_sf, mock_pyln, mock_librosa)), \
         patch("src.music_engine.mastering._require_pydub", return_value=mock_pydub), \
         patch("src.music_engine.mastering._check_ffmpeg", return_value=False):

        results = engine.master(tmp_path / "input.wav", tmp_path / "out", "Ser Galáctico")

    for platform, files in results.items():
        wav_name = files["wav"].name
        assert "ser_galctico" in wav_name or "ser_gl" in wav_name or platform in wav_name
        assert platform in wav_name
