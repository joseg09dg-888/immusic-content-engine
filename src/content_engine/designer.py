"""
IM Music Designer — REBEL LUXURY aesthetic.
Visual concept: luxury fashion sketchbook. Pencil/ink sketch marks on dark canvas.
Black (#000000) + Violet (#5E17EB) + Cream (#F2EDE5).
Anton (display) + Segoe UI Bold (body).
NOT smooth, NOT generic. Raw sketch quality IS the luxury statement.
"""
import math
import random
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from src.core.brand import Brand, Dimensions

_WIN_FONTS = Path(r"C:\Windows\Fonts")
_ASSETS    = Path(__file__).resolve().parent.parent.parent / "assets"

_FONT_MAP = {
    "title":   ["Anton-Regular.ttf", "impact.ttf"],
    "bold":    ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"],
    "regular": ["segoeui.ttf",  "arial.ttf",   "calibri.ttf"],
}

_TEMPLATES = [
    {"star_density": 2600, "accent_count": 5, "text_anchor": "bottom"},
    {"star_density": 2000, "accent_count": 8, "text_anchor": "center"},
    {"star_density": 3200, "accent_count": 3, "text_anchor": "bottom"},
]


def _pick_template(key: str) -> dict:
    return _TEMPLATES[hash(key) % len(_TEMPLATES)]


def _font(style: str, size: int) -> ImageFont.FreeTypeFont:
    af = _ASSETS / "fonts"
    for fname in _FONT_MAP.get(style, _FONT_MAP["regular"]):
        for base in (af, _WIN_FONTS):
            p = base / fname
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size=size)


# ── Sketch drawing utilities ────────────────────────────────────────────────

def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _sketchy_line(
    draw: ImageDraw.ImageDraw,
    pt1: Tuple[int, int],
    pt2: Tuple[int, int],
    color: Tuple,
    width: int = 1,
    roughness: int = 2,
    rng: random.Random = None,
):
    """Wobbly line simulating pencil stroke — NOT a computer-straight line."""
    if rng is None:
        rng = random.Random(0)
    x1, y1 = pt1
    x2, y2 = pt2
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    steps = max(int(dist / 6), 2)
    prev = pt1
    for i in range(1, steps + 1):
        t = i / steps
        jx = rng.randint(-roughness, roughness)
        jy = rng.randint(-roughness, roughness)
        nx = int(x1 + (x2 - x1) * t) + jx
        ny = int(y1 + (y2 - y1) * t) + jy
        # Occasionally break stroke (pencil lift)
        if rng.random() > 0.06:
            draw.line([prev, (nx, ny)], fill=color, width=width)
        prev = (nx, ny)


def _sketch_star(
    draw: ImageDraw.ImageDraw,
    x: int, y: int,
    size: int = 3,
    color: Tuple = (220, 220, 220),
    rng: random.Random = None,
    style: str = "cross",
):
    """Draw a sketch-style star mark instead of a filled circle."""
    if rng is None:
        rng = random.Random(0)
    if style == "cross":
        draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
        draw.line([(x, y - size), (x, y + size)], fill=color, width=1)
    elif style == "dot":
        draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=color)
    else:  # diamond
        draw.line([(x, y - size), (x + size, y)], fill=color, width=1)
        draw.line([(x + size, y), (x, y + size)], fill=color, width=1)
        draw.line([(x, y + size), (x - size, y)], fill=color, width=1)
        draw.line([(x - size, y), (x, y - size)], fill=color, width=1)


def _add_grain(img: Image.Image, intensity: int = 12, seed: int = 0) -> Image.Image:
    """Add paper-grain texture for analog/sketch feel."""
    rng = random.Random(seed)
    w, h = img.size
    grain = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    for _ in range(int(w * h * 0.015)):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        v = 128 + rng.randint(-intensity, intensity)
        alpha = rng.randint(8, 30)
        gd.point((x, y), fill=(v, v, v, alpha))
    img = img.convert("RGBA")
    return Image.alpha_composite(img, grain).convert("RGB")


def _sketch_galaxy_bg(size: Tuple[int, int], seed: int = 42, template: dict = None) -> Image.Image:
    """
    REBEL LUXURY background: deep black canvas + pencil sketch marks.
    Stars as cross/diamond glyphs. Constellation as wobbly ink lines.
    """
    if template is None:
        template = _TEMPLATES[0]
    rng = random.Random(seed)
    w, h = size
    img = Image.new("RGB", size, (4, 2, 8))  # near-black with very slight violet tint
    draw = ImageDraw.Draw(img)

    violet_rgb = _hex_to_rgb(Brand.VIOLET)
    cream_rgb  = _hex_to_rgb(Brand.CREAM)

    # Star field: mix of sketch marks
    n_stars = int(w * h / template["star_density"])
    styles  = ["cross", "dot", "dot", "dot", "diamond"]
    for _ in range(n_stars):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        size_star = rng.choices([1, 2, 3, 4], weights=[55, 28, 13, 4])[0]
        brightness = rng.randint(80, 200)
        # Most stars white/cream, few warm/cool
        tint = rng.choices(["cream", "white", "dim"], weights=[20, 50, 30])[0]
        if tint == "cream":
            c = (min(255, cream_rgb[0] - 40 + brightness // 4),
                 min(255, cream_rgb[1] - 40 + brightness // 4),
                 min(255, cream_rgb[2] - 40 + brightness // 4))
        elif tint == "dim":
            c = (brightness // 2, brightness // 2, brightness // 2)
        else:
            c = (brightness, brightness, brightness)
        style = rng.choice(styles)
        _sketch_star(draw, x, y, size_star, c, rng, style)

    # Violet accent marks (brand color)
    for _ in range(template["accent_count"]):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        r = rng.randint(3, 7)
        _sketch_star(draw, x, y, r, violet_rgb, rng, "cross")
        # Tiny bright center
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(160, 120, 255))

    # Constellation: wobbly pencil lines connecting 5-7 points
    n_pts = rng.randint(5, 7)
    pts = [
        (rng.randint(w // 6, 5 * w // 6), rng.randint(h // 6, 5 * h // 6))
        for _ in range(n_pts)
    ]
    # Draw lines in layers: faint outer, then precise inner
    for i in range(len(pts) - 1):
        dim_violet = (violet_rgb[0]//4, violet_rgb[1]//4, violet_rgb[2]//4)
        _sketchy_line(draw, pts[i], pts[i+1], dim_violet, width=2, roughness=3, rng=rng)
        _sketchy_line(draw, pts[i], pts[i+1], violet_rgb,  width=1, roughness=1, rng=rng)

    # Small circle at each constellation node (like dots on a map)
    for px, py in pts:
        draw.ellipse([px-4, py-4, px+4, py+4], outline=violet_rgb, width=1)
        draw.ellipse([px-1, py-1, px+1, py+1], fill=(200, 180, 255))

    # Paper grain
    img = _add_grain(img, intensity=14, seed=seed + 1)
    return img


# ── Text rendering ───────────────────────────────────────────────────────────

def _wrap_text(draw, text: str, font, max_w: int) -> List[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def _draw_text_block(
    img: Image.Image,
    title: str,
    subtitle: str = "",
    anchor: str = "bottom",
    max_width_ratio: float = 0.86,
) -> Image.Image:
    w, h = img.size
    draw = ImageDraw.Draw(img)
    max_w   = int(w * max_width_ratio)
    pad     = int(h * 0.055)

    title_sz = max(44, w // 13)
    sub_sz   = max(22, w // 28)
    label_sz = max(13, w // 54)

    t_font = _font("title",   title_sz)
    s_font = _font("bold",    sub_sz)
    l_font = _font("regular", label_sz)

    lines   = _wrap_text(draw, title.upper(), t_font, max_w)
    line_h  = int(title_sz * 1.15)
    block_h = line_h * len(lines) + ((sub_sz + 10) if subtitle else 0) + label_sz + 28

    y_start = {
        "top":    pad * 2,
        "center": max(pad, (h - block_h) // 2),
    }.get(anchor, h - block_h - pad * 2)

    # Dark strip behind text — spans full width
    strip = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(strip)
    sd.rectangle([0, y_start - 16, w, y_start + block_h + 16], fill=(0, 0, 0, 205))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, strip).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Thin violet line above text strip (brand accent)
    draw.rectangle([0, y_start - 16, w, y_start - 14], fill=Brand.VIOLET)

    y = y_start
    for ln in lines:
        bx = draw.textbbox((0, 0), ln, font=t_font)
        x  = (w - (bx[2] - bx[0])) // 2
        # Subtle shadow
        draw.text((x + 2, y + 2), ln, font=t_font, fill=(0, 0, 0))
        # Cream-white main text (not pure white — cream is warmer, luxury)
        draw.text((x, y), ln, font=t_font, fill=Brand.CREAM)
        y += line_h

    if subtitle:
        bx = draw.textbbox((0, 0), subtitle, font=s_font)
        x  = (w - (bx[2] - bx[0])) // 2
        draw.text((x, y + 5), subtitle, font=s_font, fill=Brand.VIOLET)
        y += sub_sz + 13

    label = "IM MUSIC  ·  REBEL LUXURY"
    bx = draw.textbbox((0, 0), label, font=l_font)
    x  = (w - (bx[2] - bx[0])) // 2
    draw.text((x, y + 8), label, font=l_font, fill=(140, 130, 120))

    return img


def _draw_logo_badge(img: Image.Image, badge_h: int = 72) -> Image.Image:
    """Minimal geometric IM MUSIC badge — sketch-style, bottom-right corner."""
    w, h = img.size
    margin  = int(w * 0.018)
    badge_w = int(badge_h * 2.2)
    x0 = w - badge_w - margin
    y0 = h - badge_h - margin

    # Try logo file first
    for path in (_ASSETS / "logo").glob("*.png"):
        try:
            logo = Image.open(path).convert("RGBA").resize((badge_w, badge_h), Image.LANCZOS)
            img  = img.convert("RGBA")
            img.paste(logo, (x0, y0), logo)
            return img.convert("RGB")
        except Exception:
            pass

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Sketch-style border instead of solid fill — more in line with the aesthetic
    od.rectangle([x0, y0, x0 + badge_w, y0 + badge_h], fill=(0, 0, 0, 200))
    od.rectangle([x0, y0, x0 + badge_w, y0 + badge_h], outline=_hex_to_rgb(Brand.VIOLET) + (220,), width=2)
    # Top violet accent stripe
    od.rectangle([x0, y0, x0 + badge_w, y0 + 3], fill=_hex_to_rgb(Brand.VIOLET) + (255,))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    im_font    = _font("title",   int(badge_h * 0.52))
    music_font = _font("regular", int(badge_h * 0.25))

    im_b  = draw.textbbox((0, 0), "IM",    font=im_font)
    ms_b  = draw.textbbox((0, 0), "MUSIC", font=music_font)
    im_w, im_h = im_b[2] - im_b[0], im_b[3] - im_b[1]
    ms_w       = ms_b[2] - ms_b[0]
    total_h    = im_h + int(badge_h * 0.25) + 4
    iy = y0 + (badge_h - total_h) // 2 + 4

    draw.text((x0 + (badge_w - im_w) // 2, iy),           "IM",    font=im_font,    fill=Brand.CREAM)
    draw.text((x0 + (badge_w - ms_w) // 2, iy + im_h + 2), "MUSIC", font=music_font, fill=Brand.VIOLET)
    return img


# ── Public API ───────────────────────────────────────────────────────────────

class Designer:
    def generate_thumbnail(
        self, title: str, subtitle: str = "", save_path: Optional[Path] = None
    ) -> Image.Image:
        tmpl = _pick_template(title)
        img  = _sketch_galaxy_bg(Dimensions.YOUTUBE_THUMBNAIL, seed=hash(title) & 0xFFFF, template=tmpl)
        img  = _draw_text_block(img, title, subtitle, anchor=tmpl["text_anchor"])
        img  = _draw_logo_badge(img, badge_h=68)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG", optimize=True)
        return img

    def generate_carousel(
        self, slides: List[dict], save_dir: Optional[Path] = None
    ) -> List[Image.Image]:
        size = Dimensions.INSTAGRAM_SQUARE
        w, h = size
        images = []
        n = min(len(slides), 10)
        for i, slide in enumerate(slides[:10]):
            tmpl = _TEMPLATES[i % len(_TEMPLATES)]
            img  = _sketch_galaxy_bg(size, seed=i * 137 + 3, template=tmpl)

            # Bottom gradient strip for text
            grad = Image.new("RGBA", size, (0, 0, 0, 0))
            gd   = ImageDraw.Draw(grad)
            strip_h = h // 2
            for band in range(strip_h):
                alpha = int(220 * band / strip_h)
                gd.rectangle([0, h - strip_h + band, w, h - strip_h + band + 1], fill=(0, 0, 0, alpha))
            img = img.convert("RGBA")
            img = Image.alpha_composite(img, grad).convert("RGB")
            draw = ImageDraw.Draw(img)

            # Slide counter — top left, minimal
            num_f = _font("regular", max(16, w // 40))
            draw.text((28, 28), f"{i+1}/{n}", font=num_f, fill=(90, 80, 80))

            # Horizontal violet rule under counter
            draw.rectangle([28, 28 + max(16, w//40) + 6, 80, 28 + max(16, w//40) + 8], fill=Brand.VIOLET)

            # Title — large Anton, lower half
            t_f     = _font("title",   max(38, w // 14))
            b_f     = _font("regular", max(20, w // 32))
            t_lines = _wrap_text(draw, slide.get("title", "").upper(), t_f, int(w * 0.86))
            b_lines = _wrap_text(draw, slide.get("body", ""), b_f, int(w * 0.86))
            t_lh    = int(w // 14 * 1.15)
            b_lh    = int(w // 32 * 1.3)
            total   = t_lh * len(t_lines) + b_lh * len(b_lines) + 24
            y       = h - total - 72

            for ln in t_lines:
                bx = draw.textbbox((0, 0), ln, font=t_f)
                x  = (w - (bx[2] - bx[0])) // 2
                draw.text((x + 2, y + 2), ln, font=t_f, fill=(0, 0, 0))
                draw.text((x, y), ln, font=t_f, fill=Brand.CREAM)
                y += t_lh
            y += 10
            for ln in b_lines:
                bx = draw.textbbox((0, 0), ln, font=b_f)
                x  = (w - (bx[2] - bx[0])) // 2
                draw.text((x, y), ln, font=b_f, fill=(190, 185, 175))
                y += b_lh

            img = _draw_logo_badge(img, badge_h=50)
            if save_dir:
                save_dir.mkdir(parents=True, exist_ok=True)
                img.save(save_dir / f"slide_{i+1:02d}.png", "PNG")
            images.append(img)
        return images

    def generate_story(
        self, title: str, subtitle: str = "", save_path: Optional[Path] = None
    ) -> Image.Image:
        tmpl = _pick_template(title + "s")
        img  = _sketch_galaxy_bg(Dimensions.INSTAGRAM_STORY, seed=(hash(title) + 7) & 0xFFFF, template=tmpl)
        img  = _draw_text_block(img, title, subtitle, anchor="center", max_width_ratio=0.80)
        img  = _draw_logo_badge(img, badge_h=62)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG")
        return img

    def generate_tiktok_cover(
        self, title: str, save_path: Optional[Path] = None
    ) -> Image.Image:
        tmpl = _pick_template(title + "t")
        img  = _sketch_galaxy_bg(Dimensions.TIKTOK_COVER, seed=(hash(title) + 13) & 0xFFFF, template=tmpl)
        img  = _draw_text_block(img, title, anchor="bottom", max_width_ratio=0.80)
        img  = _draw_logo_badge(img, badge_h=62)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG")
        return img

    def generate_pack(self, title: str, subtitle: str, save_dir: Path) -> dict:
        save_dir.mkdir(parents=True, exist_ok=True)
        return {
            "thumbnail":    self.generate_thumbnail(title, subtitle, save_dir / "thumbnail.png"),
            "story":        self.generate_story(title, subtitle, save_dir / "story.png"),
            "tiktok_cover": self.generate_tiktok_cover(title, save_dir / "tiktok_cover.png"),
            "carousel":     self.generate_carousel(
                [{"title": f"Punto {i+1}", "body": title} for i in range(8)],
                save_dir / "carousel",
            ),
        }
