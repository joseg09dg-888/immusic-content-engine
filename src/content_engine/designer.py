import random
import math
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from src.core.brand import Brand, Dimensions

_ASSETS = Path(__file__).resolve().parent.parent.parent / "assets"
_FONT_DIR = _ASSETS / "fonts"
_LOGO_DIR = _ASSETS / "logo"

# 3 template variants — rotated by hash so same title always gets same template
_TEMPLATES = [
    {"star_density": 3000, "accent_count": 5,  "text_anchor": "top"},
    {"star_density": 2000, "accent_count": 8,  "text_anchor": "center"},
    {"star_density": 4000, "accent_count": 3,  "text_anchor": "bottom"},
]


def _pick_template(seed_str: str) -> dict:
    return _TEMPLATES[hash(seed_str) % len(_TEMPLATES)]


def _load_font(size: int) -> ImageFont.ImageFont:
    for path in sorted(_FONT_DIR.glob("*.ttf")) + sorted(_FONT_DIR.glob("*.otf")):
        try:
            return ImageFont.truetype(str(path), size)
        except Exception:
            continue
    return ImageFont.load_default()


def _galaxy_bg(size: Tuple[int, int], seed: int = 42, template: dict = None) -> Image.Image:
    if template is None:
        template = _TEMPLATES[0]
    img = Image.new("RGB", size, Brand.BLACK)
    draw = ImageDraw.Draw(img)
    rng = random.Random(seed)
    w, h = size

    # Star field — density scales with image area
    n_stars = int(w * h / template["star_density"])
    for _ in range(n_stars):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        r = rng.choices([1, 2, 3], weights=[70, 25, 5])[0]
        brightness = rng.randint(150, 255)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(brightness, brightness, brightness))

    # Violet accent stars
    for _ in range(template["accent_count"]):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        r = rng.randint(3, 6)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=Brand.VIOLET)

    # Constellation lines
    n_pts = 6
    pts = [(rng.randint(w // 4, 3 * w // 4), rng.randint(h // 4, 3 * h // 4)) for _ in range(n_pts)]
    for i in range(n_pts - 1):
        draw.line([pts[i], pts[i + 1]], fill=(98, 0, 255), width=1)
    for px, py in pts:
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=Brand.WHITE)

    return img


def _draw_text_block(
    img: Image.Image,
    title: str,
    subtitle: str = "",
    anchor: str = "top",
    max_width_ratio: float = 0.85,
) -> Image.Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    max_w = int(w * max_width_ratio)
    pad = int(h * 0.06)

    title_font = _load_font(max(18, w // 22))
    sub_font = _load_font(max(14, w // 36))
    label_font = _load_font(max(12, w // 48))

    # Wrap title
    words = title.split()
    lines = []
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=title_font)
        if bbox[2] - bbox[0] <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    line_h = title_font.size + 8
    block_h = line_h * len(lines) + (sub_font.size + 6 if subtitle else 0) + label_font.size + 20

    if anchor == "top":
        y_start = pad
    elif anchor == "center":
        y_start = (h - block_h) // 2
    else:
        y_start = h - block_h - pad

    # Semi-transparent backing strip
    backing = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(backing)
    bd.rectangle([0, y_start - 10, w, y_start + block_h + 10], fill=(0, 0, 0, 160))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, backing).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Title lines
    y = y_start
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=title_font)
        x = (w - (bbox[2] - bbox[0])) // 2
        draw.text((x + 2, y + 2), ln, font=title_font, fill=(0, 0, 0))  # shadow
        draw.text((x, y), ln, font=title_font, fill=Brand.WHITE)
        y += line_h

    # Subtitle
    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        x = (w - (bbox[2] - bbox[0])) // 2
        draw.text((x, y + 4), subtitle, font=sub_font, fill=Brand.VIOLET)
        y += sub_font.size + 10

    # Label
    label = f"{Brand.LABEL} | {Brand.CONCEPT}"
    bbox = draw.textbbox((0, 0), label, font=label_font)
    x = (w - (bbox[2] - bbox[0])) // 2
    draw.text((x, y + 6), label, font=label_font, fill=(180, 180, 180))

    return img


def _paste_logo(img: Image.Image, size: int = 80) -> Image.Image:
    for ext in ("*.png", "*.svg"):
        for path in _LOGO_DIR.glob(ext):
            try:
                logo = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
                w, h = img.size
                img = img.convert("RGBA")
                img.paste(logo, (w - size - 16, h - size - 16), logo)
                return img.convert("RGB")
            except Exception:
                pass
    # No logo file yet — draw IM text as placeholder
    draw = ImageDraw.Draw(img)
    font = _load_font(size // 3)
    w, h = img.size
    draw.text((w - size, h - size // 2), "IM", font=font, fill=Brand.VIOLET)
    return img


class Designer:
    def generate_thumbnail(
        self, title: str, subtitle: str = "", save_path: Optional[Path] = None
    ) -> Image.Image:
        tmpl = _pick_template(title)
        size = Dimensions.YOUTUBE_THUMBNAIL
        img = _galaxy_bg(size, seed=hash(title) & 0xFFFF, template=tmpl)
        img = _draw_text_block(img, title, subtitle, anchor=tmpl["text_anchor"])
        img = _paste_logo(img)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG", optimize=True)
        return img

    def generate_carousel(
        self, slides: List[dict], save_dir: Optional[Path] = None
    ) -> List[Image.Image]:
        """slides: list of {"title": str, "body": str}. Returns 8-10 images."""
        images = []
        size = Dimensions.INSTAGRAM_SQUARE
        for i, slide in enumerate(slides[:10]):
            tmpl = _TEMPLATES[i % len(_TEMPLATES)]
            img = _galaxy_bg(size, seed=i * 137, template=tmpl)
            img = _draw_text_block(img, slide.get("title", ""), slide.get("body", ""), anchor="center")
            img = _paste_logo(img, size=60)
            if save_dir:
                save_dir.mkdir(parents=True, exist_ok=True)
                img.save(save_dir / f"slide_{i+1:02d}.png", "PNG")
            images.append(img)
        return images

    def generate_story(
        self, title: str, subtitle: str = "", save_path: Optional[Path] = None
    ) -> Image.Image:
        tmpl = _pick_template(title + "story")
        size = Dimensions.INSTAGRAM_STORY
        img = _galaxy_bg(size, seed=(hash(title) + 7) & 0xFFFF, template=tmpl)
        img = _draw_text_block(img, title, subtitle, anchor="center")
        img = _paste_logo(img, size=90)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG")
        return img

    def generate_tiktok_cover(
        self, title: str, save_path: Optional[Path] = None
    ) -> Image.Image:
        tmpl = _pick_template(title + "tt")
        size = Dimensions.TIKTOK_COVER
        img = _galaxy_bg(size, seed=(hash(title) + 13) & 0xFFFF, template=tmpl)
        img = _draw_text_block(img, title, anchor="bottom")
        img = _paste_logo(img, size=90)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG")
        return img

    def generate_pack(self, title: str, subtitle: str, save_dir: Path) -> dict:
        """Generates all visual assets for one publication."""
        save_dir.mkdir(parents=True, exist_ok=True)
        return {
            "thumbnail": self.generate_thumbnail(title, subtitle, save_dir / "thumbnail.png"),
            "story": self.generate_story(title, subtitle, save_dir / "story.png"),
            "tiktok_cover": self.generate_tiktok_cover(title, save_dir / "tiktok_cover.png"),
            "carousel": self.generate_carousel(
                [{"title": f"#{i+1}", "body": title} for i in range(8)],
                save_dir / "carousel",
            ),
        }
