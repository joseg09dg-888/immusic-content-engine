"""
IM Music — Illustration Fetcher + Generator
Descarga grabados de dominio publico y genera elementos urban-luxury programaticos.

Uso:
    python scripts/fetch_illustrations.py          # todo
    python scripts/fetch_illustrations.py --generate-only   # solo programaticos
    python scripts/fetch_illustrations.py --download-only   # solo descargas
"""
import sys
import io
import argparse
import logging
import urllib.request
import urllib.parse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("illustrations")

ILLUS_DIR = ROOT / "assets" / "illustrations"
ILLUS_DIR.mkdir(parents=True, exist_ok=True)

try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    log.error("PIL no instalado — pip install Pillow numpy")


# ── Programmatic Urban-Luxury Illustrations ───────────────────────────────────

def _save_illus(arr, name: str) -> Path:
    """Save RGBA numpy array as PNG illustration."""
    img = Image.fromarray(arr.astype(np.uint8), "RGBA")
    p = ILLUS_DIR / name
    img.save(p, "PNG")
    log.info("Generated: %s (%dKB)", name, p.stat().st_size // 1024)
    return p


def gen_crown(size: int = 800) -> Path:
    """Royal crown — luxury symbol. Proper 3-spike crown shape."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size

    def p(rx, ry):  # relative coords helper
        return (int(rx * s), int(ry * s))

    # Full crown shape as one polygon
    # Base band bottom: y=0.88, top: y=0.72
    # Crown body: y=0.72 trapezoid
    # Three spikes: left (y=0.22), center (y=0.04), right (y=0.22)
    crown_pts = [
        p(0.10, 0.88),  # base bottom-left
        p(0.90, 0.88),  # base bottom-right
        p(0.90, 0.72),  # base top-right
        p(0.84, 0.72),  # right spike base-right
        p(0.75, 0.22),  # right spike tip
        p(0.66, 0.72),  # right spike base-left / center spike base-right
        p(0.50, 0.04),  # center spike tip (tallest)
        p(0.34, 0.72),  # center spike base-left / left spike base-right
        p(0.25, 0.22),  # left spike tip
        p(0.16, 0.72),  # left spike base-left
        p(0.10, 0.72),  # base top-left
    ]
    d.polygon(crown_pts, fill=(0, 0, 0, 255))

    # Decorative gems (cutouts)
    for cx_r, cy_r in [(0.25, 0.80), (0.50, 0.80), (0.75, 0.80)]:
        cx, cy = int(cx_r * s), int(cy_r * s)
        r = max(4, int(s * 0.035))
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(0, 0, 0, 0))

    # Thin outline on spike tips for detail
    for tip_x, tip_y in [p(0.25, 0.22), p(0.50, 0.04), p(0.75, 0.22)]:
        r = max(3, int(s * 0.025))
        d.ellipse([tip_x-r, tip_y-r, tip_x+r, tip_y+r], fill=(0, 0, 0, 255))

    return _save_illus(np.array(img), "illus_crown.png")


def gen_lightning(size: int = 600) -> Path:
    """Lightning bolt — urban energy."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    cx = s // 2
    thick = max(8, s // 20)

    # Bold lightning bolt
    points = [
        (cx + s//8,  s//10),
        (cx - s//12, s//2 - s//20),
        (cx + s//10, s//2 - s//20),
        (cx - s//8,  s - s//10),
        (cx + s//12, s//2 + s//20),
        (cx - s//10, s//2 + s//20),
    ]
    d.polygon(points, fill=(0, 0, 0, 255))
    # Stroke outline
    for i in range(-2, 3):
        for j in range(-2, 3):
            if abs(i) + abs(j) <= 2:
                shifted = [(x+i, y+j) for x, y in points]
                d.polygon(shifted, outline=(0, 0, 0, 255))
    return _save_illus(np.array(img), "illus_lightning.png")


def gen_star_burst(size: int = 700) -> Path:
    """Starburst / sun rays — luxury radiance."""
    import math
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    cx, cy = s // 2, s // 2
    rays = 16
    outer_r = int(s * 0.46)
    inner_r = int(s * 0.18)
    center_r = int(s * 0.08)

    points = []
    for i in range(rays * 2):
        angle = math.pi * 2 * i / (rays * 2) - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle))
        points.append((x, y))

    d.polygon(points, fill=(0, 0, 0, 255))
    d.ellipse([cx-center_r, cy-center_r, cx+center_r, cy+center_r], fill=(0, 0, 0, 0))
    return _save_illus(np.array(img), "illus_starburst.png")


def gen_rose(size: int = 700) -> Path:
    """Abstract rose — bold silhouette, luxury/street art. Fully centered."""
    import math
    s = size
    cx, cy = s // 2, s // 2

    def rotated_ellipse_pts(ecx, ecy, a, b, theta, n=32):
        """Polygon approximation of rotated ellipse."""
        pts = []
        for i in range(n):
            t = 2 * math.pi * i / n
            x = ecx + a * math.cos(t) * math.cos(theta) - b * math.sin(t) * math.sin(theta)
            y = ecy + a * math.cos(t) * math.sin(theta) + b * math.sin(t) * math.cos(theta)
            pts.append((int(x), int(y)))
        return pts

    result = Image.new("RGBA", (s, s), (0, 0, 0, 0))

    # Outer petals (6 petals, large)
    petal_count = 6
    a = int(s * 0.14)   # semi-minor (width of petal)
    b = int(s * 0.32)   # semi-major (length of petal)
    offset = int(s * 0.14)

    for i in range(petal_count):
        angle = math.pi * 2 * i / petal_count
        px = cx + int(offset * math.sin(angle))
        py = cy - int(offset * math.cos(angle))
        pts = rotated_ellipse_pts(px, py, a, b, angle)
        pimg = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        ImageDraw.Draw(pimg).polygon(pts, fill=(0, 0, 0, 240))
        result = Image.alpha_composite(result, pimg)

    # Inner petals (6 petals, rotated 30°, smaller)
    a2, b2 = int(s * 0.09), int(s * 0.20)
    off2 = int(s * 0.08)
    for i in range(petal_count):
        angle = math.pi * 2 * i / petal_count + math.pi / 6
        px = cx + int(off2 * math.sin(angle))
        py = cy - int(off2 * math.cos(angle))
        pts = rotated_ellipse_pts(px, py, a2, b2, angle)
        pimg = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        ImageDraw.Draw(pimg).polygon(pts, fill=(0, 0, 0, 220))
        result = Image.alpha_composite(result, pimg)

    # Center circle
    d2 = ImageDraw.Draw(result)
    cr = int(s * 0.08)
    d2.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(0, 0, 0, 255))

    return _save_illus(np.array(result), "illus_rose.png")


def gen_music_wave(size: int = 800) -> Path:
    """Sound wave visualization — music identity."""
    import math
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    cy = s // 2
    bars = 24
    bar_w = s // (bars * 2)

    for i in range(bars):
        t = i / bars
        height_factor = math.sin(math.pi * t) * 0.8 + 0.2
        # Add some irregularity for organic feel
        height_factor *= (0.7 + 0.3 * math.sin(t * 11))
        bar_h = int(s * 0.40 * height_factor)
        x = int(i * s / bars) + bar_w // 2
        thickness = max(4, bar_w - 4)
        d.rectangle([x, cy - bar_h, x + thickness, cy + bar_h],
                    fill=(0, 0, 0, 255))

    return _save_illus(np.array(img), "illus_wave.png")


def gen_diamond(size: int = 600) -> Path:
    """Diamond shape — REBEL LUXURY signature."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    m = s // 8
    cx, cy = s // 2, s // 2

    # Outer diamond
    d.polygon([
        (cx, m),
        (s - m, cy),
        (cx, s - m),
        (m, cy),
    ], outline=(0, 0, 0, 255), width=max(6, s // 40))

    # Inner diamond
    inner_m = int(s * 0.22)
    d.polygon([
        (cx, inner_m),
        (s - inner_m, cy),
        (cx, s - inner_m),
        (inner_m, cy),
    ], outline=(0, 0, 0, 255), width=max(3, s // 80))

    # Facet lines
    d.line([(cx, m), (s - inner_m, cy)], fill=(0, 0, 0, 180), width=2)
    d.line([(cx, m), (inner_m, cy)], fill=(0, 0, 0, 180), width=2)
    d.line([(cx, m), (s - inner_m, int(cy * 0.7))], fill=(0, 0, 0, 180), width=2)
    d.line([(cx, m), (inner_m, int(cy * 0.7))], fill=(0, 0, 0, 180), width=2)

    return _save_illus(np.array(img), "illus_diamond.png")


GENERATORS = [
    ("illus_crown.png",     gen_crown),
    ("illus_lightning.png", gen_lightning),
    ("illus_starburst.png", gen_star_burst),
    ("illus_rose.png",      gen_rose),
    ("illus_wave.png",      gen_music_wave),
    ("illus_diamond.png",   gen_diamond),
]


# ── Public Domain Downloads ───────────────────────────────────────────────────
# Grabados de dominio publico de Wikimedia Commons y archive.org

PUBLIC_DOMAIN_URLS = [
    # Baroque/classical engravings — public domain (Gustave Dore, etc.)
    ("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Floral_decorative_element.png/800px-Floral_decorative_element.png",
     "illus_floral.png"),
]


def _remove_white_bg(src: Path, dst: Path) -> bool:
    """Remove white background from PNG, keep dark/black ink."""
    try:
        img = Image.open(src).convert("RGBA")
        arr = np.array(img, dtype=np.float32)
        R, G, B = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        darkness = (R + G + B) / 3.0
        alpha = np.clip((160 - darkness) / 160.0, 0, 1)
        is_white = darkness > 200
        alpha[is_white] = 0
        # Violet bg removal
        violetness = B - G * 0.5 - R * 0.2
        is_violet = (violetness > 80) & (darkness > 80)
        alpha[is_violet] = 0
        result = np.zeros((*R.shape, 4), dtype=np.uint8)
        result[:,:,3] = (alpha * 255).astype(np.uint8)
        Image.fromarray(result, "RGBA").save(dst, "PNG")
        return True
    except Exception as e:
        log.warning("bg removal failed %s: %s", src.name, e)
        return False


def download_illustrations() -> int:
    count = 0
    for url, fname in PUBLIC_DOMAIN_URLS:
        dst = ILLUS_DIR / fname
        if dst.exists():
            log.info("Already exists: %s", fname)
            count += 1
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            tmp = ILLUS_DIR / f"_tmp_{fname}"
            with urllib.request.urlopen(req, timeout=15) as r:
                tmp.write_bytes(r.read())
            if _remove_white_bg(tmp, dst):
                tmp.unlink(missing_ok=True)
                log.info("Downloaded: %s (%dKB)", fname, dst.stat().st_size // 1024)
                count += 1
            else:
                tmp.rename(dst)
                count += 1
        except Exception as e:
            log.warning("Download failed %s: %s", fname, e)
    return count


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if not HAS_PIL:
        return

    p = argparse.ArgumentParser()
    p.add_argument("--generate-only", action="store_true")
    p.add_argument("--download-only", action="store_true")
    args = p.parse_args()

    total = 0

    if not args.download_only:
        print("\nGenerando ilustraciones urban-luxury...")
        for fname, fn in GENERATORS:
            dst = ILLUS_DIR / fname
            if dst.exists() and dst.stat().st_size > 5000:
                log.info("Already exists: %s", fname)
                total += 1
                continue
            try:
                fn()
                total += 1
            except Exception as e:
                log.warning("Generator failed %s: %s", fname, e)

    if not args.generate_only:
        print("\nDescargando grabados de dominio publico...")
        total += download_illustrations()

    print(f"\nTotal ilustraciones disponibles: {total}")
    existing = sorted(ILLUS_DIR.glob("*.png"))
    print(f"En assets/illustrations/: {len(existing)} archivos")
    for f in existing:
        print(f"  {f.name} ({f.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
