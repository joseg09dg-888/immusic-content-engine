import pytest, sys, numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock
sys.path.insert(0, "src")
from music_engine.visualizer import Visualizer

def test_default_quality():
    assert Visualizer().quality == "medium_quality"

def test_invalid_genre_raises():
    v = Visualizer()
    with patch.dict("sys.modules", {"manim": MagicMock()}):
        with patch.object(v, "_analyze_audio", return_value=(np.array([1.0]), 90.0, np.zeros(100), 44100)):
            with patch("pathlib.Path.exists", return_value=True):
                with pytest.raises(ValueError, match="Invalid genre"):
                    v.generate(Path("fake.wav"), genre="jazz")

def test_missing_audio_raises():
    v = Visualizer()
    with patch.dict("sys.modules", {"manim": MagicMock()}):
        with pytest.raises(FileNotFoundError):
            v.generate(Path("nonexistent_audio_file.wav"))

def test_rms_envelope_length():
    v = Visualizer()
    waveform = np.random.randn(44100)
    result = v._compute_rms_envelope(waveform, sr=44100, n_points=50)
    assert len(result) == 50
    assert result.min() >= 0.0 and result.max() <= 1.0

def test_chill_hop_script_content():
    v = Visualizer()
    beats = np.array([0.5, 1.0, 1.5])
    script = v._build_manim_script_chill_hop(beats, 90.0, np.zeros(44100), 44100, Path("f.wav"))
    assert "ChillHopScene" in script and "#5E17EB" in script

def test_afro_house_script_content():
    v = Visualizer()
    beats = np.array([0.5, 1.0])
    script = v._build_manim_script_afro_house(beats, 124.0, np.zeros(44100), 44100, Path("f.wav"))
    assert "AfroHouseScene" in script and "#5E17EB" in script
