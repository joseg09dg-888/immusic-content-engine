"""IM Music Visualizer — REBEL LUXURY audio-reactive with Manim."""
from pathlib import Path
from typing import Optional
import numpy as np


class Visualizer:
    def __init__(self, quality: str = "medium_quality"):
        self.quality = quality

    def is_available(self) -> bool:
        try:
            import manim  # noqa
            return True
        except ImportError:
            return False

    def generate(self, audio_path: Path, genre: str = "chill_hop",
                 output_path: Optional[Path] = None, duration_sec: Optional[float] = None) -> Path:
        try:
            import manim  # noqa
        except ImportError:
            raise RuntimeError("Manim not installed. Run: pip install manim")
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio not found: {audio_path}")
        beats, tempo, waveform, sr = self._analyze_audio(audio_path, duration_sec)
        if genre == "chill_hop":
            return self._render_chill_hop(audio_path, beats, tempo, waveform, sr, output_path)
        elif genre == "afro_house":
            return self._render_afro_house(audio_path, beats, tempo, waveform, sr, output_path)
        else:
            raise ValueError(f"Invalid genre: {genre}. Use 'chill_hop' or 'afro_house'")

    def _analyze_audio(self, audio_path: Path, duration_sec: Optional[float]) -> tuple:
        import librosa
        y, sr = librosa.load(str(audio_path), duration=duration_sec, mono=True)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        return beat_times, float(tempo), y, sr

    def _compute_rms_envelope(self, waveform: np.ndarray, sr: int, n_points: int = 100) -> np.ndarray:
        import librosa
        rms = librosa.feature.rms(y=waveform, frame_length=2048, hop_length=512)[0]
        rms_norm = (rms - rms.min()) / (rms.max() - rms.min() + 1e-8)
        indices = np.linspace(0, len(rms_norm) - 1, n_points, dtype=int)
        return rms_norm[indices]

    def _render_chill_hop(self, audio_path, beats, tempo, waveform, sr, output_path) -> Path:
        output_path = Path(output_path) if output_path else Path("releases/visualizers/chill_hop_visualizer.mp4")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        script = self._build_manim_script_chill_hop(beats, tempo, waveform, sr, audio_path)
        script_path = output_path.parent / "scene_chill_hop.py"
        script_path.write_text(script, encoding="utf-8")
        import subprocess
        cmd = ["manim", f"--{self.quality}", str(script_path), "ChillHopScene", "-o", str(output_path.name)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(output_path.parent))
        if result.returncode != 0:
            raise RuntimeError(f"Manim render failed:\n{result.stderr[-500:]}")
        return output_path

    def _render_afro_house(self, audio_path, beats, tempo, waveform, sr, output_path) -> Path:
        output_path = Path(output_path) if output_path else Path("releases/visualizers/afro_house_visualizer.mp4")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        script = self._build_manim_script_afro_house(beats, tempo, waveform, sr, audio_path)
        script_path = output_path.parent / "scene_afro_house.py"
        script_path.write_text(script, encoding="utf-8")
        import subprocess
        cmd = ["manim", f"--{self.quality}", str(script_path), "AfroHouseScene", "-o", str(output_path.name)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(output_path.parent))
        if result.returncode != 0:
            raise RuntimeError(f"Manim render failed:\n{result.stderr[-500:]}")
        return output_path

    def _build_manim_script_chill_hop(self, beats, tempo, waveform, sr, audio_path) -> str:
        beat_list = list(beats[:50].tolist())
        return f'''from manim import *
import numpy as np

VIOLET = "#5E17EB"
CREAM = "#F2EDE5"

class ChillHopScene(Scene):
    """El Viajero Nocturno - ciudad nocturna, neon violeta, constelaciones IM Music."""
    BEAT_TIMES = {beat_list}
    TEMPO = {tempo:.1f}

    def construct(self):
        self.camera.background_color = "#000000"
        stars = VGroup(*[Dot([np.random.uniform(-7,7), np.random.uniform(-4,4), 0],
            radius=np.random.uniform(0.01, 0.04), color=CREAM,
            fill_opacity=np.random.uniform(0.3, 1.0)) for _ in range(300)])
        self.add(stars)
        pts = [LEFT*2+UP*1.5, LEFT*1+UP*0.5, ORIGIN, RIGHT*1+UP*0.5, RIGHT*2+UP*1.5]
        cdots = VGroup(*[Dot(p, radius=0.06, color=VIOLET) for p in pts])
        clines = VGroup(*[Line(pts[i], pts[i+1], stroke_color=VIOLET, stroke_width=1, stroke_opacity=0.5) for i in range(len(pts)-1)])
        title = Text("REBEL LUXURY", font_size=36, color=CREAM).to_edge(DOWN, buff=0.8)
        subtitle = Text("IM Music", font_size=24, color=VIOLET).next_to(title, DOWN, buff=0.2)
        pulse = Circle(radius=0.5, color=VIOLET, stroke_width=3, fill_opacity=0)
        self.play(FadeIn(cdots), FadeIn(clines), FadeIn(title), FadeIn(subtitle), run_time=2)
        for i, bt in enumerate(self.BEAT_TIMES[:15]):
            wait_t = bt - (self.BEAT_TIMES[i-1] if i > 0 else 0) - 0.1
            if wait_t > 0.05: self.wait(max(0.05, wait_t))
            p2 = pulse.copy()
            self.play(p2.animate.scale(3).set_opacity(0), run_time=0.15)
            self.remove(p2)
        self.wait(2)
'''

    def _build_manim_script_afro_house(self, beats, tempo, waveform, sr, audio_path) -> str:
        beat_list = list(beats[:50].tolist())
        rms_vals = list(self._compute_rms_envelope(waveform, sr, 50).tolist())
        return f'''from manim import *
import numpy as np

VIOLET = "#5E17EB"
CREAM = "#F2EDE5"

class AfroHouseScene(Scene):
    """El Ser Galactico - galaxia, nebulosas, particulas que vibran con el beat."""
    BEAT_TIMES = {beat_list}
    RMS = {rms_vals}
    TEMPO = {tempo:.1f}

    def construct(self):
        self.camera.background_color = "#000000"
        nebula = Ellipse(width=10, height=6, color=VIOLET, fill_opacity=0.08, stroke_opacity=0)
        self.add(nebula)
        particles = VGroup(*[Dot([np.random.uniform(-6,6), np.random.uniform(-3.5,3.5), 0],
            radius=np.random.uniform(0.015, 0.06),
            color=VIOLET if np.random.random()>0.5 else CREAM,
            fill_opacity=np.random.uniform(0.4,1.0)) for _ in range(150)])
        self.add(particles)
        center = Dot(ORIGIN, radius=0.3, color=VIOLET, fill_opacity=1)
        glow = Circle(radius=0.8, color=VIOLET, stroke_width=2, stroke_opacity=0.6)
        title = Text("REBEL LUXURY", font_size=32, color=CREAM).to_edge(DOWN, buff=0.8)
        subtitle = Text("IM Music", font_size=20, color=VIOLET).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(center), FadeIn(glow), FadeIn(title), FadeIn(subtitle), run_time=2)
        for i, bt in enumerate(self.BEAT_TIMES[:15]):
            wait_t = bt - (self.BEAT_TIMES[i-1] if i > 0 else 0) - 0.08
            if wait_t > 0.05: self.wait(max(0.05, wait_t))
            rms = self.RMS[i % len(self.RMS)] if self.RMS else 0.5
            s = 1.0 + rms * 2.0
            self.play(center.animate.scale(s), glow.animate.scale(s).set_opacity(0.3), run_time=0.12)
            self.play(center.animate.scale(1/s), glow.animate.scale(1/s).set_opacity(0.6), run_time=0.08)
        self.wait(2)
'''
