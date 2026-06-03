"""Diagnóstico AudioCraft — captura error exacto de pip install."""
import subprocess, sys, json
from pathlib import Path

LOG = Path(r"C:\Users\jose-\projects\immusic-content-engine\logs\audiocraft_debug.txt")
LOG.parent.mkdir(parents=True, exist_ok=True)

lines = []

def run(cmd, label=""):
    lines.append(f"\n{'='*60}\n{label}: {' '.join(cmd)}\n{'='*60}")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300,
                       env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "PIP_DISABLE_PIP_VERSION_CHECK": "1"})
    lines.append(f"EXIT: {r.returncode}")
    lines.append("STDOUT:\n" + r.stdout[-3000:])
    lines.append("STDERR:\n" + r.stderr[-3000:])
    return r.returncode

# 1. Versión de Python y pip
run([sys.executable, "--version"], "Python version")
run([sys.executable, "-m", "pip", "--version"], "pip version")

# 2. Versiones de torch instaladas
run([sys.executable, "-c", "import torch; print('torch', torch.__version__); print('CUDA:', torch.cuda.is_available())"], "torch check")

# 3. Ver qué requiere audiocraft exactamente
run([sys.executable, "-m", "pip", "install", "audiocraft", "--dry-run", "--no-deps"], "audiocraft dry-run no-deps")
run([sys.executable, "-m", "pip", "install", "audiocraft", "--dry-run"], "audiocraft dry-run full")

# 4. Intento real con verbose
run([sys.executable, "-m", "pip", "install", "audiocraft", "-v", "--no-build-isolation"], "audiocraft install verbose")

output = "\n".join(lines)
LOG.write_text(output, encoding="utf-8")
print(output[-5000:])  # print last 5000 chars
