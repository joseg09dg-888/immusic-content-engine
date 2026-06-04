"""
IM Music Beat Generator — REBEL LUXURY
Genera beats procedurales en Chill Hop y Afro House listos para produccion.
Sin dependencias externas de GPU — funciona en cualquier maquina.
"""
import random, logging, math
import numpy as np
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)
SR = 44100

# ── Synth primitives ─────────────────────────────────────────────────────────

def _sine(freq, dur, amp=0.8):
    t = np.linspace(0, dur, int(SR*dur), endpoint=False)
    return amp * np.sin(2*np.pi*freq*t)

def _saw(freq, dur, amp=0.5):
    t = np.linspace(0, dur, int(SR*dur), endpoint=False)
    return amp * (2*(t*freq - np.floor(t*freq+0.5)))

def _noise(dur, amp=0.3):
    return amp * (2*np.random.random(int(SR*dur))-1)

def _adsr(sig, a, d, s, r):
    n=len(sig); env=np.ones(n)
    A=int(a*SR); D=int(d*SR); R=int(r*SR)
    if A>0: env[:min(A,n)]=np.linspace(0,1,min(A,n))
    if D>0 and A<n: env[A:min(A+D,n)]=np.linspace(1,s,min(A+D,n)-A)
    if A+D<n: env[A+D:max(n-R,A+D)]=s
    if R>0: env[max(0,n-R):]=np.linspace(s,0,min(R,n))
    return sig*env

def _midi_freq(n): return 440.0*2**((n-69)/12)

# ── Drum sounds ──────────────────────────────────────────────────────────────

def _kick(dur=0.35):
    t=np.linspace(0,dur,int(SR*dur),endpoint=False)
    freq=150*np.exp(-t*25)+40
    body=np.sin(2*np.pi*np.cumsum(freq)/SR)
    click=_noise(0.005, amp=0.8); cp=np.zeros(int(SR*dur)); cp[:len(click)]=click
    return _adsr(0.9*body+0.3*cp, 0.001,0.05,0.3,0.1)

def _snare(dur=0.25):
    wave=_noise(dur,0.7)+_sine(200,dur,0.3)
    return _adsr(wave, 0.002,0.04,0.2,0.15)

def _hihat(dur=0.08, open_=False):
    d=dur if not open_ else 0.35
    return _adsr(_noise(d,0.4), 0.001,0.01,0.1,0.08 if open_ else 0.04)

def _bass(freq, dur=0.3):
    wave=_saw(freq,dur,0.6)+_saw(freq*1.003,dur,0.3)+_sine(freq*2,dur,0.2)
    return _adsr(wave, 0.005,0.05,0.7,0.1)

def _pad(freqs, dur=1.0):
    wave=np.zeros(int(SR*dur))
    for f in freqs:
        wave+=_sine(f,dur,0.18)+_sine(f*1.002,dur,0.09)
    return _adsr(wave, 0.2,0.1,0.6,0.4)

# ── Sequencers ───────────────────────────────────────────────────────────────

MINOR=[0,2,3,5,7,8,10]
PENTA=[0,3,5,7,10]

def _chill_hop(bpm=90, bars=16, seed=0):
    rng=random.Random(seed); bd=60/bpm; bar=bd*4
    out=np.zeros(int(SR*bar*bars)); root=45  # A2

    for b in range(bars):
        bo=int(b*bar*SR)
        # Kick: 1 and sometimes 3
        for beat in ([0,2] if rng.random()>0.3 else [0]):
            _mix(out, _kick(), bo+int(beat*bd*SR))
        # Snare: 2,4
        for beat in [1,3]:
            _mix(out, _snare()*0.8, bo+int(beat*bd*SR))
        # Hi-hat: 8th swung
        for e in range(8):
            sw=0.04*bd if e%2==1 else 0
            amp=0.5+rng.random()*0.5
            h=_hihat(open_=(rng.random()>0.85))
            _mix(out, h*amp, bo+int((e*bd/2+sw)*SR))
        # Bass: syncopated melody in pentatonic
        steps=[(0,0.4),(None,0),(3,0.3),(None,0),(5,0.35),(None,0),(7,0.25),(None,0)]
        for i,(deg,dur_mult) in enumerate(steps):
            if deg is None: continue
            freq=_midi_freq(root+PENTA[deg%len(PENTA)])
            note=_bass(freq, bd*max(0.2,dur_mult+rng.random()*0.2))
            _mix(out, note*0.7, bo+int(i*bd/2*SR))
        # Pad chord every 2 bars
        if b%2==0:
            prog=[(0,[0,3,7]),(5,[0,4,7]),(3,[0,3,7]),(7,[0,3,6])]
            rd,ivs=prog[(b//2)%len(prog)]
            rf=_midi_freq(root+12+MINOR[rd%7])
            freqs=[rf*2**(i/12) for i in ivs]
            _mix(out, _pad(freqs,bar*2)*0.5, bo)
    return out

def _afro_house(bpm=124, bars=16, seed=0):
    rng=random.Random(seed); bd=60/bpm; bar=bd*4
    out=np.zeros(int(SR*bar*bars)); root=40  # E2

    for b in range(bars):
        bo=int(b*bar*SR)
        # 4-on-floor kick
        for beat in range(4):
            _mix(out, _kick(0.3), bo+int(beat*bd*SR))
        # Clap 2,4
        for beat in [1,3]:
            _mix(out, _snare(0.2)*1.1, bo+int(beat*bd*SR))
        # 16th hi-hats
        for s16 in range(16):
            amp=0.8 if s16%4==0 else 0.35+(rng.random()*0.2)
            h=_hihat(0.06, open_=(s16%8==6))
            _mix(out, h*amp, bo+int(s16*bd/4*SR))
        # Driving bass
        for i,(deg,dm) in enumerate([(0,0.7),(0,0.25),(7,0.4),(5,0.5)]):
            freq=_midi_freq(root+MINOR[deg%7])
            note=_bass(freq, bd*dm)
            _mix(out, note*0.85, bo+int(i*bd*SR))
        # Stab chord
        if b%4==0:
            rf=_midi_freq(root+12)
            freqs=[rf,rf*1.189,rf*1.498]
            stab=_pad(freqs, bar*0.4)*0.5
            _mix(out, stab, bo+int(1.5*bd*SR))
    return out

def _mix(buf, sig, offset):
    end=min(offset+len(sig), len(buf))
    if end>offset:
        buf[offset:end]+=sig[:end-offset]

# ── Public API ────────────────────────────────────────────────────────────────

class BeatGenerator:
    """Beat generator para IM Music — REBEL LUXURY."""

    def generate_chill_hop(self, bpm=90, bars=16, output_path=None, seed=0):
        bpm=max(85,min(95,bpm))
        wav=_chill_hop(bpm=bpm, bars=bars, seed=seed)
        return self._save(wav, output_path or Path(f"releases/chill_hop_{bpm}bpm.wav"))

    def generate_afro_house(self, bpm=124, bars=16, output_path=None, seed=0):
        bpm=max(120,min(128,bpm))
        wav=_afro_house(bpm=bpm, bars=bars, seed=seed)
        return self._save(wav, output_path or Path(f"releases/afro_house_{bpm}bpm.wav"))

    def _save(self, signal, path, sr=SR):
        from scipy.io import wavfile
        path=Path(path); path.parent.mkdir(parents=True, exist_ok=True)
        peak=np.max(np.abs(signal))
        if peak>0: signal=signal/peak*0.70
        wavfile.write(str(path), sr, (signal*32767).astype(np.int16))
        size_mb=path.stat().st_size/1e6
        logger.info("Beat: %s (%.1fs, %.1fMB)", path.name, len(signal)/sr, size_mb)
        print(f"  Beat: {path.name} ({len(signal)/sr:.0f}s, {size_mb:.1f}MB)")
        return path
