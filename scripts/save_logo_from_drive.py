"""
Saves the IM Music logo from Google Drive base64 content to assets/logo/logo_white.png
Run once after downloading content from Drive.
"""
import base64
import sys
from pathlib import Path

# Full base64 content from Drive file proximamente (1).png
# Paste the full base64 string here
B64_CONTENT = sys.argv[1] if len(sys.argv) > 1 else ""

if not B64_CONTENT:
    print("Usage: python save_logo_from_drive.py <base64_string>")
    sys.exit(1)

out = Path(__file__).resolve().parent.parent / "assets" / "logo" / "logo_white.png"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(base64.b64decode(B64_CONTENT))
print(f"[OK] Saved {out.stat().st_size} bytes -> {out}")

# Verify
from PIL import Image
img = Image.open(out)
print(f"     Size: {img.size}  Mode: {img.mode}")
