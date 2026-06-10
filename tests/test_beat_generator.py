"""
tests/test_beat_generator.py — Unit tests for src/music_engine/beat_generator.py

Strategy: bars=1 keeps generated signals short (~1-2s of audio) so tests
run fast. WAV I/O goes through scipy.io.wavfile against tmp_path — no
mocking needed since it's pure local file I/O with no GPU/network deps.
"""
from __future__ import annotations

import numpy as np
import pytest
from unittest.mock import patch
from scipy.io import wavfile

from src.music_engine.beat_generator import (
    BeatGenerator,
    SR,
    _sine,
    _saw,
    _noise,
    _adsr,
    _midi_freq,
    _kick,
    _snare,
    _hihat,
    _bass,
    _pad,
    _mix,
    _chill_hop,
    _afro_house,
)


# ---------------------------------------------------------------------------
# Synth primitives
# ---------------------------------------------------------------------------

class TestSynthPrimitives:
    def test_sine_length_and_amplitude(self):
        sig = _sine(440, 0.5, amp=0.8)
        assert len(sig) == int(SR * 0.5)
        assert np.max(np.abs(sig)) <= 0.8 + 1e-9

    def test_saw_length_and_range(self):
        sig = _saw(220, 0.25, amp=0.5)
        assert len(sig) == int(SR * 0.25)
        assert np.max(np.abs(sig)) <= 0.5 + 1e-9

    def test_noise_range(self):
        sig = _noise(0.1, amp=0.3)
        assert len(sig) == int(SR * 0.1)
        assert np.all(np.abs(sig) <= 0.3 + 1e-9)

    def test_midi_freq_a4(self):
        assert _midi_freq(69) == pytest.approx(440.0)

    def test_midi_freq_octave_doubling(self):
        assert _midi_freq(81) == pytest.approx(_midi_freq(69) * 2)


class TestADSR:
    def test_envelope_starts_and_ends_near_zero(self):
        sig = np.ones(SR)  # 1s constant signal
        env = _adsr(sig, a=0.1, d=0.1, s=0.5, r=0.1)
        assert env[0] == pytest.approx(0.0, abs=1e-6)
        assert env[-1] == pytest.approx(0.0, abs=1e-6)

    def test_envelope_sustains_at_level(self):
        sig = np.ones(SR)
        env = _adsr(sig, a=0.1, d=0.1, s=0.5, r=0.1)
        assert env[SR // 2] == pytest.approx(0.5, abs=1e-6)

    def test_envelope_preserves_length(self):
        sig = np.ones(1000)
        env = _adsr(sig, a=0.01, d=0.01, s=0.5, r=0.01)
        assert len(env) == 1000


class TestDrumAndInstrumentSounds:
    def test_kick_nonempty_and_bounded(self):
        sig = _kick()
        assert len(sig) == int(SR * 0.35)
        assert np.max(np.abs(sig)) <= 2.0

    def test_snare_nonempty(self):
        sig = _snare()
        assert len(sig) == int(SR * 0.25)

    def test_hihat_open_is_longer_than_closed(self):
        closed = _hihat(open_=False)
        opened = _hihat(open_=True)
        assert len(opened) > len(closed)

    def test_bass_length(self):
        sig = _bass(110.0, dur=0.3)
        assert len(sig) == int(SR * 0.3)

    def test_pad_length(self):
        sig = _pad([110.0, 220.0], dur=0.5)
        assert len(sig) == int(SR * 0.5)


class TestMix:
    def test_mix_adds_at_offset(self):
        buf = np.zeros(100)
        sig = np.ones(10)
        _mix(buf, sig, 5)
        assert np.all(buf[5:15] == 1.0)
        assert np.all(buf[:5] == 0.0)
        assert np.all(buf[15:] == 0.0)

    def test_mix_clips_to_buffer_end(self):
        buf = np.zeros(10)
        sig = np.ones(20)
        _mix(buf, sig, 5)
        assert np.all(buf[5:] == 1.0)

    def test_mix_offset_past_end_is_noop(self):
        buf = np.zeros(10)
        sig = np.ones(5)
        _mix(buf, sig, 20)
        assert np.all(buf == 0.0)


class TestSequencers:
    def test_chill_hop_output_length(self):
        bpm, bars = 90, 1
        bd = 60 / bpm
        bar = bd * 4
        expected = int(SR * bar * bars)
        out = _chill_hop(bpm=bpm, bars=bars, seed=0)
        assert len(out) == expected

    def test_afro_house_output_length(self):
        bpm, bars = 124, 1
        bd = 60 / bpm
        bar = bd * 4
        expected = int(SR * bar * bars)
        out = _afro_house(bpm=bpm, bars=bars, seed=0)
        assert len(out) == expected

    def test_chill_hop_seed_changes_output(self):
        a = _chill_hop(bpm=90, bars=1, seed=1)
        b = _chill_hop(bpm=90, bars=1, seed=2)
        assert not np.array_equal(a, b)

    def test_chill_hop_produces_sound(self):
        out = _chill_hop(bpm=90, bars=1, seed=0)
        assert np.max(np.abs(out)) > 0

    def test_afro_house_produces_sound(self):
        out = _afro_house(bpm=124, bars=1, seed=0)
        assert np.max(np.abs(out)) > 0


class TestBeatGeneratorPublicAPI:
    def test_generate_chill_hop_writes_valid_wav(self, tmp_path):
        out_path = tmp_path / "chill.wav"
        bg = BeatGenerator()
        result = bg.generate_chill_hop(bpm=90, bars=1, output_path=out_path, seed=0)
        assert result == out_path
        assert out_path.exists()
        sr, data = wavfile.read(str(out_path))
        assert sr == SR
        assert data.dtype == np.int16
        assert len(data) > 0

    def test_generate_afro_house_writes_valid_wav(self, tmp_path):
        out_path = tmp_path / "afro.wav"
        bg = BeatGenerator()
        result = bg.generate_afro_house(bpm=124, bars=1, output_path=out_path, seed=0)
        assert result == out_path
        assert out_path.exists()
        sr, data = wavfile.read(str(out_path))
        assert sr == SR
        assert data.dtype == np.int16

    def test_generate_chill_hop_clamps_bpm_above_range(self, tmp_path):
        out_path = tmp_path / "chill_fast.wav"
        bg = BeatGenerator()
        with patch("src.music_engine.beat_generator._chill_hop", wraps=_chill_hop) as spy:
            bg.generate_chill_hop(bpm=200, bars=1, output_path=out_path, seed=0)
        assert spy.call_args.kwargs["bpm"] == 95

    def test_generate_chill_hop_clamps_bpm_below_range(self, tmp_path):
        out_path = tmp_path / "chill_slow.wav"
        bg = BeatGenerator()
        with patch("src.music_engine.beat_generator._chill_hop", wraps=_chill_hop) as spy:
            bg.generate_chill_hop(bpm=10, bars=1, output_path=out_path, seed=0)
        assert spy.call_args.kwargs["bpm"] == 85

    def test_generate_afro_house_clamps_bpm_above_range(self, tmp_path):
        out_path = tmp_path / "afro_fast.wav"
        bg = BeatGenerator()
        with patch("src.music_engine.beat_generator._afro_house", wraps=_afro_house) as spy:
            bg.generate_afro_house(bpm=200, bars=1, output_path=out_path, seed=0)
        assert spy.call_args.kwargs["bpm"] == 128

    def test_generate_afro_house_clamps_bpm_below_range(self, tmp_path):
        out_path = tmp_path / "afro_slow.wav"
        bg = BeatGenerator()
        with patch("src.music_engine.beat_generator._afro_house", wraps=_afro_house) as spy:
            bg.generate_afro_house(bpm=50, bars=1, output_path=out_path, seed=0)
        assert spy.call_args.kwargs["bpm"] == 120

    def test_generate_chill_hop_creates_parent_dirs(self, tmp_path):
        out_path = tmp_path / "nested" / "dir" / "beat.wav"
        bg = BeatGenerator()
        bg.generate_chill_hop(bpm=90, bars=1, output_path=out_path, seed=0)
        assert out_path.exists()


class TestSave:
    def test_save_normalizes_peak_to_70_percent(self, tmp_path):
        bg = BeatGenerator()
        signal = np.array([2.0, -2.0, 1.0, -1.0])
        out_path = tmp_path / "normalized.wav"
        bg._save(signal, out_path)
        sr, data = wavfile.read(str(out_path))
        expected_peak = int(0.70 * 32767)
        actual_peak = max(abs(int(data.max())), abs(int(data.min())))
        assert actual_peak == pytest.approx(expected_peak, abs=1)

    def test_save_handles_silence_without_division_by_zero(self, tmp_path):
        bg = BeatGenerator()
        signal = np.zeros(100)
        out_path = tmp_path / "silence.wav"
        bg._save(signal, out_path)
        assert out_path.exists()
