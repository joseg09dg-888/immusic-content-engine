"""
IM Music Designer — REBEL LUXURY aesthetic.
Electric violet background + vintage engraving illustration + bold display text.
Matches @immusicsello Instagram visual identity exactly.

Required assets: assets/engravings/*.png or *.jpg (B&W public-domain engravings)
Run scripts/download_engravings.py to populate the folder.
"""
import random
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
from src.core.brand import Brand, Dimensions

_WIN_FONTS  = Path(r"C:\Windows\Fonts")
_ASSETS     = Path(__file__).resolve().parent.parent.parent / "assets"
_ENGRAVINGS = _ASSETS / "engravings"

_FONT_MAP = {
    "title":    ["Anton-Regular.ttf", "impact.ttf"],
    "subtitle": ["Anton-Regular.ttf", "impact.ttf"],
    "bold":     ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"],
    "regular":  ["segoeui.ttf",  "arial.ttf",   "calibri.ttf"],
}


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _font(style: str, size: int) -> ImageFont.FreeTypeFont:
    af = _ASSETS / "fonts"
    for fname in _FONT_MAP.get(style, _FONT_MAP["regular"]):
        for base in (af, _WIN_FONTS):
            p = base / fname
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size=size)


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


def _pick_engraving(seed: int = 0) -> Optional[Path]:
    """Pick a vintage engraving from assets/engravings/ deterministically by seed."""
    files = sorted(
        list(_ENGRAVINGS.glob("*.png")) + list(_ENGRAVINGS.glob("*.jpg"))
    )
    if not files:
        return None
    return files[seed % len(files)]


def _rebel_luxury_bg(
    size: Tuple[int, int],
    engraving_path: Optional[Path] = None,
    seed: int = 0,
) -> Image.Image:
    """
    REBEL LUXURY background: solid electric violet + large vintage engraving overlay.
    Engraving is rendered as pure black line art on the violet. Matches @immusicsello exactly.
    """
    w, h = size
    violet_rgb = _hex_to_rgb(Brand.VIOLET)
    img = Image.new("RGB", size, violet_rgb)

    eng_path = engraving_path or _pick_engraving(seed)
    if eng_path and Path(eng_path).exists():
        try:
            eng_gray = Image.open(eng_path).convert("L")
            ew, eh = eng_gray.size

            # Scale: cover mode — fill ~88% of height or full width, whichever is larger
            scale_h = (h * 0.88) / eh
            scale_w = w / ew
            scale = max(scale_h, scale_w)
            new_w = int(ew * scale)
            new_h = int(eh * scale)
            eng_gray = eng_gray.resize((new_w, new_h), Image.LANCZOS)

            # Boost contrast so ink lines are crisp and clean
            eng_gray = ImageEnhance.Contrast(eng_gray).enhance(1.9)

            # Convert to RGBA: dark pixels → black opaque, white → transparent
            inverted = ImageOps.invert(eng_gray)
            eng_rgba = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 255))
            eng_rgba.putalpha(inverted)

            # Center horizontally, minimal top offset
            x_off = (w - new_w) // 2
            y_off = max(0, int(h * 0.01))
            img = img.convert("RGBA")
            img.paste(eng_rgba, (x_off, y_off), eng_rgba)
            img = img.convert("RGB")
        except Exception:
            pass  # graceful fallback to pure violet

    return img


def _draw_rebel_text(
    img: Image.Image,
    context: str = "",
    headline: str = "",
    subtitle: str = "",
    cta: str = "",
) -> Image.Image:
    """
    REBEL LUXURY text hierarchy — matches @immusicsello exactly:
      [small CONTEXT TEXT]       ~48-52% vertical
      [MASSIVE WHITE HEADLINE]   ~53-68% vertical
      [small SUBTITLE]           ~68-72% vertical
      [small CTA]                ~87-89% vertical (always near bottom)
    All text: pure white, centered, uppercase Anton.
    """
    w, h = img.size
    draw = ImageDraw.Draw(img)

    ctx_sz  = max(22, w // 56)   # ~26px @ 1440w
    head_sz = max(88, w // 10)   # ~144px @ 1440w — fills most of width
    sub_sz  = max(22, w // 56)
    cta_sz  = max(18, w // 70)

    ctx_font  = _font("title",   ctx_sz)
    head_font = _font("title",   head_sz)
    sub_font  = _font("title",   sub_sz)
    cta_font  = _font("regular", cta_sz)

    max_w_head = int(w * 0.93)
    max_w_ctx  = int(w * 0.88)

    head_lines = _wrap_text(draw, headline.upper(), head_font, max_w_head) if headline else []
    head_lh    = int(head_sz * 0.97)  # tight leading for display font

    # Block start position: ~50% down (context pushes it up slightly)
    y = int(h * 0.50)
    if context:
        y = int(h * 0.47)

    # Small context text (above headline)
    if context:
        ctx_lines = _wrap_text(draw, context.upper(), ctx_font, max_w_ctx)
        for ln in ctx_lines:
            bx = draw.textbbox((0, 0), ln, font=ctx_font)
            x = (w - (bx[2] - bx[0])) // 2
            draw.text((x, y), ln, font=ctx_font, fill=(255, 255, 255))
            y += ctx_sz + 3
        y += 8

    # MASSIVE headline — the hero element
    for ln in head_lines:
        bx = draw.textbbox((0, 0), ln, font=head_font)
        lw = bx[2] - bx[0]
        x = (w - lw) // 2
        # Black shadow for legibility on engraving
        draw.text((x + 4, y + 4), ln, font=head_font, fill=(0, 0, 0))
        draw.text((x,     y    ), ln, font=head_font, fill=(255, 255, 255))
        y += head_lh

    y += 10

    # Small subtitle below headline
    if subtitle:
        sub_lines = _wrap_text(draw, subtitle.upper(), sub_font, max_w_ctx)
        for ln in sub_lines:
            bx = draw.textbbox((0, 0), ln, font=sub_font)
            x = (w - (bx[2] - bx[0])) // 2
            draw.text((x, y), ln, font=sub_font, fill=(255, 255, 255))
            y += sub_sz + 4

    # CTA — fixed near bottom (88% vertical)
    if cta:
        cta_bx = draw.textbbox((0, 0), cta.upper(), font=cta_font)
        cta_x = (w - (cta_bx[2] - cta_bx[0])) // 2
        cta_y = int(h * 0.878)
        draw.text((cta_x, cta_y), cta.upper(), font=cta_font, fill=(255, 255, 255))

    return img


def _generate_brand_card(
    size: Tuple[int, int],
    save_path: Optional[Path] = None,
) -> Image.Image:
    """
    Closing slide: pure black + centered IM Music logo (mark + MUSIC).
    Uses logo_immusic.png (1080x1350 RGB, black bg, violet mark) — the real brand identity.
    Identical to the last slide of every @immusicsello carousel.
    """
    w, h = size

    # Try logo_immusic.png first (real logo, RGB, black bg)
    for logo_name in ("logo_immusic.png", "logo_white.png"):
        logo_path = _ASSETS / "logo" / logo_name
        if not logo_path.exists():
            continue
        try:
            logo = Image.open(logo_path).convert("RGB")
            logo.load()  # verify not corrupted

            # The logo image is already black bg + violet mark + MUSIC
            # Crop to the mark area and scale to fit the card
            lw, lh = logo.size
            target_w = int(w * 0.52)
            scale = target_w / lw
            logo = logo.resize((target_w, int(lh * scale)), Image.LANCZOS)

            # Create black canvas, paste logo centered
            img = Image.new("RGB", size, (0, 0, 0))
            lx = (w - logo.width) // 2
            ly = (h - logo.height) // 2
            img.paste(logo, (lx, ly))

            if save_path:
                save_path.parent.mkdir(parents=True, exist_ok=True)
                img.save(save_path, "PNG")
            return img
        except Exception:
            continue

    # Fallback: text-only brand card
    violet_rgb = _hex_to_rgb(Brand.VIOLET)
    img = Image.new("RGB", size, (0, 0, 0))
    draw = ImageDraw.Draw(img)
    im_sz   = max(120, w // 7)
    im_font = _font("title", im_sz)
    ib = draw.textbbox((0, 0), "IM", font=im_font)
    draw.text(((w - (ib[2] - ib[0])) // 2, h // 2 - 80), "IM", font=im_font, fill=violet_rgb)
    ms_sz   = max(36, w // 24)
    ms_font = _font("bold", ms_sz)
    mb = draw.textbbox((0, 0), "MUSIC", font=ms_font)
    draw.text(((w - (mb[2] - mb[0])) // 2, h // 2 + 60), "MUSIC", font=ms_font, fill=Brand.CREAM)
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(save_path, "PNG")
    return img


def _draw_logo_badge(img: Image.Image, badge_h: int = 72) -> Image.Image:
    """IM MUSIC logo badge — bottom-right corner. Square 500×500 logo, never stretched."""
    w, h = img.size
    margin = int(w * 0.022)
    badge_w = badge_h  # logo_white.png is 500×500 square
    x0 = w - badge_w - margin
    y0 = h - badge_h - margin

    logo_path = _ASSETS / "logo" / "logo_white.png"
    if logo_path.exists():
        try:
            logo = Image.open(logo_path).convert("RGBA").resize((badge_w, badge_h), Image.LANCZOS)
            img = img.convert("RGBA")
            img.paste(logo, (x0, y0), logo)
            return img.convert("RGB")
        except Exception:
            pass

    # Fallback: drawn text badge
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    violet_rgb = _hex_to_rgb(Brand.VIOLET)
    od.rectangle([x0, y0, x0 + badge_w, y0 + badge_h], fill=(0, 0, 0, 200))
    od.rectangle([x0, y0, x0 + badge_w, y0 + badge_h], outline=violet_rgb + (220,), width=2)
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    im_f = _font("title",   int(badge_h * 0.52))
    ms_f = _font("regular", int(badge_h * 0.25))
    ib = draw.textbbox((0, 0), "IM",    font=im_f)
    mb = draw.textbbox((0, 0), "MUSIC", font=ms_f)
    iy = y0 + (badge_h - (ib[3] - ib[1]) - (mb[3] - mb[1]) - 4) // 2
    draw.text((x0 + (badge_w - (ib[2] - ib[0])) // 2, iy),                           "IM",    font=im_f, fill=Brand.CREAM)
    draw.text((x0 + (badge_w - (mb[2] - mb[0])) // 2, iy + (ib[3] - ib[1]) + 2),    "MUSIC", font=ms_f, fill=Brand.VIOLET)
    return img


# ── Public API ───────────────────────────────────────────────────────────────

class Designer:
    def generate_thumbnail(
        self, title: str, subtitle: str = "", save_path: Optional[Path] = None
    ) -> Image.Image:
        img = _rebel_luxury_bg(Dimensions.YOUTUBE_THUMBNAIL, seed=hash(title) & 0xFFFF)
        img = _draw_rebel_text(img, headline=title, subtitle=subtitle)
        img = _draw_logo_badge(img, badge_h=68)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG", optimize=True)
        return img

    def generate_carousel(
        self, slides: List[dict], save_dir: Optional[Path] = None
    ) -> List[Image.Image]:
        """
        Instagram carousel: N content slides + 1 closing brand card.
        Each content slide: violet BG + vintage engraving + REBEL LUXURY text.
        Final slide: black BG + centered violet logo + MUSIC.
        """
        size = Dimensions.INSTAGRAM_SQUARE
        images = []
        content_slides = slides[:9]  # max 9 content + 1 brand card = 10

        for i, slide in enumerate(content_slides):
            img = _rebel_luxury_bg(size, seed=i)
            img = _draw_rebel_text(
                img,
                context=slide.get("context", slide.get("supra", "")),
                headline=slide.get("title", slide.get("titulo", "")),
                subtitle=slide.get("subtitle", slide.get("subtitulo", slide.get("body", ""))),
                cta=slide.get("cta", "DESCUBRE MÁS EN NUESTRO CANAL"),
            )
            if save_dir:
                save_dir.mkdir(parents=True, exist_ok=True)
                img.save(save_dir / f"slide_{i+1:02d}.png", "PNG")
            images.append(img)

        # Always append closing brand card
        brand_path = (save_dir / f"slide_{len(images)+1:02d}.png") if save_dir else None
        images.append(_generate_brand_card(size, brand_path))
        return images

    def generate_story(
        self, title: str, subtitle: str = "", save_path: Optional[Path] = None
    ) -> Image.Image:
        img = _rebel_luxury_bg(Dimensions.INSTAGRAM_STORY, seed=(hash(title) + 7) & 0xFFFF)
        img = _draw_rebel_text(img, headline=title, subtitle=subtitle)
        img = _draw_logo_badge(img, badge_h=62)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG")
        return img

    def generate_tiktok_cover(
        self, title: str, save_path: Optional[Path] = None
    ) -> Image.Image:
        img = _rebel_luxury_bg(Dimensions.TIKTOK_COVER, seed=(hash(title) + 13) & 0xFFFF)
        img = _draw_rebel_text(img, headline=title)
        img = _draw_logo_badge(img, badge_h=62)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG")
        return img

    def generate_youtube_short_thumbnail(
        self, title: str, subtitle: str = "", save_path: Optional[Path] = None
    ) -> Image.Image:
        img = _rebel_luxury_bg(Dimensions.YOUTUBE_SHORT, seed=(hash(title) + 17) & 0xFFFF)
        w, h = img.size
        # Violet bar at top with SHORTS label
        bar_h = max(60, h // 15)
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        violet_rgb = _hex_to_rgb(Brand.VIOLET)
        od.rectangle([0, 0, w, bar_h], fill=violet_rgb + (255,))
        img = img.convert("RGBA")
        img = Image.alpha_composite(img, overlay).convert("RGB")
        draw = ImageDraw.Draw(img)
        sf = _font("title", max(28, h // 24))
        sb = draw.textbbox((0, 0), "SHORTS", font=sf)
        draw.text(
            ((w - (sb[2] - sb[0])) // 2, (bar_h - (sb[3] - sb[1])) // 2),
            "SHORTS", font=sf, fill=Brand.CREAM,
        )
        img = _draw_rebel_text(img, headline=title, subtitle=subtitle)
        img = _draw_logo_badge(img, badge_h=62)
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG")
        return img

    def generate_tiktok_carousel_slides(
        self, slides_data: list, save_dir: Optional[Path] = None
    ) -> list:
        size = Dimensions.TIKTOK_CAROUSEL
        images = []
        for i, slide in enumerate(slides_data):
            img = _rebel_luxury_bg(size, seed=i + 50)
            titulo   = slide.get("titulo", slide.get("title", ""))
            subtitulo = slide.get("subtitulo", slide.get("subtitle", slide.get("dato", "")))
            img = _draw_rebel_text(img, headline=titulo, subtitle=subtitulo)
            img = _draw_logo_badge(img, badge_h=48)
            if save_dir:
                save_dir.mkdir(parents=True, exist_ok=True)
                img.save(save_dir / f"tiktok_slide_{i+1:02d}.png", "PNG")
            images.append(img)
        return images

    def generate_pinterest_pin(
        self, title: str, subtitle: str = "", save_path: Optional[Path] = None
    ) -> Image.Image:
        img = _rebel_luxury_bg(Dimensions.PINTEREST_PIN, seed=(hash(title) + 23) & 0xFFFF)
        img = _draw_rebel_text(img, headline=title, subtitle=subtitle)
        img = _draw_logo_badge(img, badge_h=60)
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
