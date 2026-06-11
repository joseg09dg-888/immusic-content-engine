"""
IM Music Designer — REBEL LUXURY aesthetic.

Visual system derived from @immusicsello feed:
  - Background: solid electric violet #5E17EB ALWAYS (never black, never gradient)
  - Illustration: black ink/engraving PNG centered on violet
  - Typography: Sceageus HUGE (main statement) + Anton small (context + CTA)
  - Palette: violet #5E17EB | white #FFFFFF | black #000000 | cream #F2EDE5
  - NO galaxies, NO gradients, NO grid/star overlays. Raw. Bold. Luxury.

The ONLY exception is the closing/outro card: pure black background with
the IM Music logo centered and "MUSIC" in cream — used as the carousel
closer, never as a backdrop for headline content or thumbnails.
"""
import random
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from src.core.brand import Brand, Dimensions

_WIN_FONTS  = Path(r"C:\Windows\Fonts")
_ASSETS     = Path(__file__).resolve().parent.parent.parent / "assets"
_ILLUS_DIR  = _ASSETS / "illustrations"
_LOGO_PATH  = _ASSETS / "logo" / "logo_immusic.png"

_VIOLET_RGB = (94, 23, 235)  # #5E17EB — brand.py canonical violet
_BLACK_RGB  = (0, 0, 0)
_WHITE_RGB  = (255, 255, 255)
_CREAM_RGB  = (242, 237, 229) # #F2EDE5

_FONT_MAP = {
    "hero":    ["Sceageus-Regular.otf", "Anton-Regular.ttf", "impact.ttf"],
    "label":   ["Anton-Regular.ttf", "segoeuib.ttf", "arialbd.ttf"],
    "body":    ["segoeui.ttf", "arial.ttf", "calibri.ttf"],
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _font(style: str, size: int) -> ImageFont.FreeTypeFont:
    af = _ASSETS / "fonts"
    for fname in _FONT_MAP.get(style, _FONT_MAP["body"]):
        for base in (af, _WIN_FONTS):
            p = base / fname
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size=size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> List[str]:
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
    return lines or [""]


# Files with an opaque (non-transparent, non-white) canvas baked in — pasting
# these onto the violet background produces a visible black box, breaking
# "el violeta SIEMPRE debe ser visible a traves de la ilustracion" (CLAUDE.md).
_ILLUS_BLACKLIST = {
    "_burj_high_contrast.png",
    "_burj_lines_only.png",
    "illus_angel_sm.png",
    "illus_bandana.png",
    "illus_mic_sm.png",
    "illus_money_sm.png",
    "illus_ring.png",
}


def _pick_illustration(seed: int) -> Optional[Path]:
    """Pick a random illustration from the library."""
    illus = sorted(_ILLUS_DIR.glob("*.png")) + sorted(_ILLUS_DIR.glob("*.webp"))
    illus = [p for p in illus if p.name not in _ILLUS_BLACKLIST]
    if not illus:
        return None
    return illus[seed % len(illus)]


def _load_illustration(path: Path, target_size: Tuple[int, int]) -> Optional[Image.Image]:
    """
    Load a black-ink illustration PNG and scale it to fill target_size.
    White/near-white backgrounds are made transparent using numpy (fast).
    """
    try:
        import numpy as np
        illus = Image.open(path).convert("RGBA")
        iw, ih = illus.size

        # Vectorized white-background removal
        arr = np.array(illus)
        mask = (arr[:, :, 0] > 220) & (arr[:, :, 1] > 220) & (arr[:, :, 2] > 220)
        arr[mask, 3] = 0
        illus = Image.fromarray(arr, "RGBA")

        # Scale illustration to 85% of target width for breathing room
        tw, th = target_size
        scale = (tw * 0.85) / iw
        new_h = int(ih * scale)
        illus = illus.resize((int(iw * scale), new_h), Image.LANCZOS)
        return illus
    except Exception:
        return None


def _add_noise(img: Image.Image, amount: int = 8, seed: int = 0) -> Image.Image:
    """Subtle film grain — analog texture, not smooth digital."""
    rng = random.Random(seed)
    w, h = img.size
    noise = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    nd = ImageDraw.Draw(noise)
    for _ in range(w * h // 80):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        v = rng.randint(200, 255)
        a = rng.randint(5, amount)
        nd.point((x, y), fill=(v, v, v, a))
    return Image.alpha_composite(img.convert("RGBA"), noise).convert("RGB")


# ── Background builders ───────────────────────────────────────────────────────

def _violet_bg(size: Tuple[int, int], seed: int = 0) -> Image.Image:
    """
    Solid electric violet background — the signature IM Music canvas.
    Pure solid #5E17EB + subtle film grain only. NO gradients, NO overlay
    patterns — matches the verified @immusicsello brand identity.
    """
    img = Image.new("RGB", size, _VIOLET_RGB)
    return _add_noise(img, amount=10, seed=seed)


def _black_bg(size: Tuple[int, int], seed: int = 0) -> Image.Image:
    """Pure black background — used ONLY for the closing/outro card."""
    img = Image.new("RGB", size, _BLACK_RGB)
    return _add_noise(img, amount=6, seed=seed)


def _closing_card(size: Tuple[int, int], seed: int = 0) -> Image.Image:
    """Closing/outro card: pure black bg + centered logo + 'MUSIC' in cream."""
    img = _black_bg(size, seed=seed)
    if not _LOGO_PATH.exists():
        return img

    logo = Image.open(_LOGO_PATH).convert("RGBA")
    lw, lh = logo.size
    target_w = int(size[0] * 0.45)
    scale = target_w / lw
    logo = logo.resize((target_w, int(lh * scale)), Image.LANCZOS)
    lw, lh = logo.size
    lx = (size[0] - lw) // 2
    ly = (size[1] - lh) // 2 - size[1] // 14

    result = img.convert("RGBA")
    result.paste(logo, (lx, ly), logo)
    img = result.convert("RGB")

    draw = ImageDraw.Draw(img)
    music_font = _font("hero", size[0] // 7)
    music_text = "MUSIC"
    bx = draw.textbbox((0, 0), music_text, font=music_font)
    tw = bx[2] - bx[0]
    tx = (size[0] - tw) // 2
    ty = ly + lh + int(size[1] * 0.015)
    draw.text((tx, ty), music_text, font=music_font, fill=_CREAM_RGB)
    return img


# ── Illustration layer ────────────────────────────────────────────────────────

def _paste_illustration(
    bg: Image.Image,
    illus_path: Path,
    position: str = "top",  # "top" | "center" | "full"
    opacity: float = 0.92,
) -> Image.Image:
    """
    Paste black-ink engraving onto background.
    'top' fills upper 65% — text lives in center/bottom area.
    'center' centers illustration — text overlaps it.
    'full' fills entire frame — dramatic full-bleed.
    """
    try:
        import numpy as np
        illus_raw = Image.open(illus_path).convert("RGBA")
        orig_w, orig_h = illus_raw.size
    except Exception:
        return bg

    w, h = bg.size
    aspect = orig_w / orig_h  # > 1 = wide, < 1 = tall

    if position == "top":
        if aspect >= 0.85:
            # Wide/square illustration (diamond, starburst, rose, crown):
            # Cap width at 62% of image width to not overwhelm text area
            target_w = int(w * 0.62)
            scale = target_w / orig_w
        else:
            # Tall illustration (baroque engravings, angel, mic, money):
            # Fill upper 68% of height
            target_h = int(h * 0.68)
            scale = min(w / orig_w, target_h / orig_h)
    elif position == "full":
        scale = max(w / orig_w, h / orig_h)
    else:  # center
        scale = min(w / orig_w, h / orig_h) * 0.90

    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    illus = illus_raw.resize((new_w, new_h), Image.LANCZOS)

    # Remove near-white backgrounds (for non-removebg illustrations)
    arr = np.array(illus)
    white_mask = (arr[:, :, 0] > 210) & (arr[:, :, 1] > 210) & (arr[:, :, 2] > 210)
    arr[white_mask, 3] = 0
    illus = Image.fromarray(arr, "RGBA")

    # Position
    x = (w - new_w) // 2
    if position == "top":
        # Baroque engravings bleed at top; geometric shapes sit fully visible
        y = -new_h // 12 if aspect < 0.85 else int(h * 0.02)
    elif position == "full":
        y = (h - new_h) // 2
    else:  # center
        y = (h - new_h) // 2 - h // 14

    # Apply opacity
    if opacity < 1.0:
        r, g, b, a = illus.split()
        a = a.point(lambda p: int(p * opacity))
        illus = Image.merge("RGBA", (r, g, b, a))

    result = bg.convert("RGBA")
    result.paste(illus, (x, y), illus)
    return result.convert("RGB")


# ── Logo badge ────────────────────────────────────────────────────────────────

def _paste_logo(img: Image.Image, size: int = 80, corner: str = "top-left") -> Image.Image:
    """Small IM Music logo badge — minimal, never dominant."""
    if not _LOGO_PATH.exists():
        # Try any PNG in logo dir
        logos = list((_ASSETS / "logo").glob("*.png"))
        if not logos:
            return img
        logo_path = logos[0]
    else:
        logo_path = _LOGO_PATH

    try:
        logo = Image.open(logo_path).convert("RGBA")
        lw, lh = logo.size
        scale = size / max(lw, lh)
        logo = logo.resize((int(lw * scale), int(lh * scale)), Image.LANCZOS)
        lw, lh = logo.size

        w, h = img.size
        margin = int(w * 0.04)
        positions = {
            "top-left":     (margin, margin),
            "top-right":    (w - lw - margin, margin),
            "bottom-left":  (margin, h - lh - margin),
            "bottom-right": (w - lw - margin, h - lh - margin),
        }
        x, y = positions.get(corner, positions["top-left"])

        result = img.convert("RGBA")
        result.paste(logo, (x, y), logo)
        return result.convert("RGB")
    except Exception:
        return img


# ── Text layout — THE REBEL LUXURY 3-TIER SYSTEM ─────────────────────────────

def _draw_rebel_text(
    img: Image.Image,
    hook: str,
    headline: str,
    cta: str = "",
    sub_text: str = "",
    invert: bool = False,
) -> Image.Image:
    """
    4-tier text system matching @immusicsello Canva feed EXACTLY:
      [small Anton — context/hook]
      [ENORMOUS Sceageus — the statement, CENTERED in image]
      [small Anton — sub_text below headline (e.g. MENTES, CAMBIO)]
      ── fixed bottom ──
      [small Anton — CTA always at base]

    Main block (hook + headline + sub_text) centers around 56% of image height.
    CTA is a fixed independent element at the bottom.
    """
    w, h = img.size
    draw = ImageDraw.Draw(img)

    text_color   = _WHITE_RGB
    shadow_color = _BLACK_RGB
    label_size   = max(22, w // 30)
    label_font   = _font("label", label_size)
    hero_max_w   = int(w * 0.82)  # 9% margin each side — text never touches edges

    hook_lines = _wrap(draw, hook.upper(), label_font, int(w * 0.86)) if hook else []

    # Shrink hero font until main block fits within 68% of height (leaves room for illus + cta)
    hero_size = w // 3
    while hero_size > 18:
        hero_font  = _font("hero", hero_size)
        hero_lines = _wrap(draw, headline.upper(), hero_font, hero_max_w)
        hero_lh    = int(hero_size * 1.08)
        hero_block = hero_lh * len(hero_lines)
        hook_block = (label_size + 4) * len(hook_lines) + 10 if hook_lines else 0
        main_block = hook_block + hero_block
        max_line_w = max(
            draw.textbbox((0, 0), ln, font=hero_font)[2] for ln in hero_lines
        )
        if main_block <= int(h * 0.64) and max_line_w <= int(w * 0.82):
            break
        hero_size -= 6

    # Recompute final values
    hero_font  = _font("hero", hero_size)
    hero_lines = _wrap(draw, headline.upper(), hero_font, hero_max_w)
    hero_lh    = int(hero_size * 1.08)
    hero_block = hero_lh * len(hero_lines)
    hook_block = (label_size + 4) * len(hook_lines) + 10 if hook_lines else 0
    main_block = hook_block + hero_block

    # Center the main block around 56% of image height
    center_y = int(h * 0.56)
    y = center_y - main_block // 2
    y = max(int(h * 0.08), y)

    # ── Hook lines ──
    for ln in hook_lines:
        bx = draw.textbbox((0, 0), ln, font=label_font)
        x  = (w - (bx[2] - bx[0])) // 2
        draw.text((x + 1, y + 1), ln, font=label_font, fill=shadow_color)
        draw.text((x, y), ln, font=label_font, fill=text_color)
        y += label_size + 4
    if hook_lines:
        y += 10

    # ── Hero headline ──
    for ln in hero_lines:
        bx = draw.textbbox((0, 0), ln, font=hero_font)
        tw = bx[2] - bx[0]
        x  = (w - tw) // 2
        for dx, dy in [(-2, 3), (2, 3), (0, 4)]:
            draw.text((x + dx, y + dy), ln, font=hero_font, fill=shadow_color)
        draw.text((x, y), ln, font=hero_font, fill=text_color)
        y += hero_lh

    # ── Sub text — small label below headline (e.g. MENTES, CAMBIO) ──
    if sub_text:
        y += 8
        sub_lines = _wrap(draw, sub_text.upper(), label_font, int(w * 0.84))
        for ln in sub_lines:
            bx = draw.textbbox((0, 0), ln, font=label_font)
            x  = (w - (bx[2] - bx[0])) // 2
            draw.text((x + 1, y + 1), ln, font=label_font, fill=shadow_color)
            draw.text((x, y), ln, font=label_font, fill=text_color)
            y += label_size + 4

    # ── CTA — fixed at bottom, independent of main block ──
    if cta:
        cta_y = h - label_size - int(h * 0.05)
        bx = draw.textbbox((0, 0), cta.upper(), font=label_font)
        x  = (w - (bx[2] - bx[0])) // 2
        draw.text((x + 1, cta_y + 1), cta.upper(), font=label_font, fill=shadow_color)
        draw.text((x, cta_y), cta.upper(), font=label_font, fill=text_color)

    return img


# ── Public API ────────────────────────────────────────────────────────────────

class Designer:

    def generate_post(
        self,
        hook: str,
        headline: str,
        cta: str = "DESCUBRE COMO EN NUESTRO CANAL",
        sub_text: str = "",
        save_path: Optional[Path] = None,
        seed: int = 0,
    ) -> Image.Image:
        """
        Instagram post (1080×1350, 4:5 portrait) — REBEL LUXURY style.
        Identical to Canva DAHFZBTb7g0: illustration top + centered text + CTA at base.
        sub_text: small label below headline (e.g. 'MENTES', 'CAMBIO').
        """
        size  = Dimensions.INSTAGRAM_POST
        bg    = _violet_bg(size, seed=seed)
        illus = _pick_illustration(seed)
        if illus:
            bg = _paste_illustration(bg, illus, position="top", opacity=0.92)
        bg = _draw_rebel_text(bg, hook, headline, cta, sub_text)
        bg = _paste_logo(bg, size=int(size[0] * 0.09), corner="top-left")
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            bg.save(save_path, "PNG", optimize=True)
        return bg

    def generate_story(
        self,
        hook: str,
        headline: str,
        cta: str = "VER EN NUESTRO CANAL",
        save_path: Optional[Path] = None,
        seed: int = 0,
    ) -> Image.Image:
        """Instagram Story / TikTok cover (1080×1920)."""
        size  = Dimensions.INSTAGRAM_STORY
        bg    = _violet_bg(size, seed=seed + 7)
        illus = _pick_illustration(seed + 1)
        if illus:
            bg = _paste_illustration(bg, illus, position="top", opacity=0.88)
        bg = _draw_rebel_text(bg, hook, headline, cta)
        bg = _paste_logo(bg, size=int(size[0] * 0.10), corner="top-left")
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            bg.save(save_path, "PNG")
        return bg

    def generate_tiktok_cover(
        self,
        hook: str,
        headline: str,
        save_path: Optional[Path] = None,
        seed: int = 0,
    ) -> Image.Image:
        """TikTok vertical cover (1080×1920)."""
        return self.generate_story(hook, headline, cta="@IMMUSICSELLO",
                                   save_path=save_path, seed=seed + 13)

    def generate_thumbnail(
        self,
        hook: str,
        headline: str,
        cta: str = "",
        save_path: Optional[Path] = None,
        seed: int = 0,
    ) -> Image.Image:
        """
        YouTube thumbnail (1280×720) — solid violet bg, brand-consistent.
        """
        size  = Dimensions.YOUTUBE_THUMBNAIL
        bg    = _violet_bg(size, seed=seed + 3)
        illus = _pick_illustration(seed + 2)
        if illus:
            bg = _paste_illustration(bg, illus, position="top", opacity=0.92)

        # Black bar at bottom — brand contrast accent
        w, h = size
        draw = ImageDraw.Draw(bg)
        draw.rectangle([0, h - 8, w, h], fill=_BLACK_RGB)

        bg = _draw_rebel_text(bg, hook, headline, cta)
        bg = _paste_logo(bg, size=int(size[0] * 0.08), corner="top-left")
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            bg.save(save_path, "PNG", optimize=True)
        return bg

    def generate_carousel(
        self,
        slides: List[dict],
        save_dir: Optional[Path] = None,
        seed: int = 0,
    ) -> List[Path]:
        """
        Carousel slides (1080×1920, 9:16) — para Reels y TikTok.
        Cada slide tiene fondo distinto: ilustracion + elementos urban-luxury variados.
        Returns list of saved paths.
        """
        size   = Dimensions.INSTAGRAM_REEL  # 9:16 vertical
        paths  = []
        n      = min(len(slides), 10)

        for i, slide in enumerate(slides[:10]):
            hook     = slide.get("hook", "")
            headline = slide.get("headline", slide.get("title", ""))
            body     = slide.get("body", "")
            cta      = slide.get("cta", f"{i+1}/{n}")

            s = seed + i * 17

            if i == n - 1:
                # Closing slide: pure black + logo + "MUSIC" — brand outro
                bg = _closing_card(size, seed=s)
            else:
                bg = _violet_bg(size, seed=s)
                illus = _pick_illustration(s + i)
                if illus:
                    bg = _paste_illustration(bg, illus, position="center", opacity=0.85)

                # For slides with body text, use it as hook
                effective_hook = hook or body[:80]
                bg = _draw_rebel_text(bg, effective_hook, headline, cta)
                bg = _paste_logo(bg, size=int(size[0] * 0.10), corner="top-left")

            if save_dir:
                save_dir.mkdir(parents=True, exist_ok=True)
                out_path = save_dir / f"slide_{i+1:02d}.png"
                bg.save(out_path, "PNG")
                paths.append(out_path)

        return paths

    def generate_youtube_banner(
        self,
        tagline: str = "NO LANZAMOS MUSICA. JAQUEAMOS MENTES.",
        handle: str = "@IMMUSICSELLO",
        save_path: Optional[Path] = None,
        seed: int = 0,
    ) -> Image.Image:
        """
        YouTube channel art — 2560x1440 px.
        Safe zone center (1546x423) contains all critical text.
        Left/right edges are cut on TV — keep text in center 60%.
        """
        W, H = 2560, 1440
        img = Image.new("RGB", (W, H), _VIOLET_RGB)

        # Subtle darker bottom band
        draw_tmp = ImageDraw.Draw(img)
        for i in range(H // 5):
            factor = i / (H // 5)
            r = int(_VIOLET_RGB[0] * (1 - 0.15 * factor))
            g = int(_VIOLET_RGB[1] * (1 - 0.15 * factor))
            b = int(_VIOLET_RGB[2] * (1 - 0.05 * factor))
            draw_tmp.rectangle([0, H - i - 1, W, H - i], fill=(r, g, b))

        img = _add_noise(img, amount=8, seed=seed)

        # Illustration — subtle, LEFT side (safe zone center carries text)
        illus_path = _pick_illustration(seed)
        if illus_path:
            try:
                import numpy as np
                illus_raw = Image.open(illus_path).convert("RGBA")
                ow, oh = illus_raw.size
                target_w = int(W * 0.30)
                scale = target_w / ow
                illus = illus_raw.resize((target_w, int(oh * scale)), Image.LANCZOS)
                arr = np.array(illus)
                white_mask = (arr[:,:,0] > 210) & (arr[:,:,1] > 210) & (arr[:,:,2] > 210)
                arr[white_mask, 3] = 0
                arr[:,:,3] = (arr[:,:,3] * 0.35).astype(np.uint8)
                illus = Image.fromarray(arr, "RGBA")
                iw, ih = illus.size
                x = int(W * 0.01)
                y = (H - ih) // 2
                result = img.convert("RGBA")
                result.paste(illus, (x, y), illus)
                img = result.convert("RGB")
            except Exception:
                pass

        # Recreate draw on the final img (after noise + illustration)
        draw = ImageDraw.Draw(img)

        # IM MUSIC logotype — huge, centered
        logo_font_size = W // 8
        logo_font = _font("hero", logo_font_size)
        logo_text = "IM MUSIC"
        bx = draw.textbbox((0, 0), logo_text, font=logo_font)
        tw = bx[2] - bx[0]
        lx = (W - tw) // 2
        ly = H // 2 - logo_font_size // 2 - H // 12

        # Shadow
        for dx, dy in [(-4, 4), (4, 4), (0, 6)]:
            draw.text((lx + dx, ly + dy), logo_text, font=logo_font, fill=_BLACK_RGB)
        draw.text((lx, ly), logo_text, font=logo_font, fill=_WHITE_RGB)

        # Tagline — small, below logo
        tag_size = max(36, W // 48)
        tag_font = _font("label", tag_size)
        tag_lines = _wrap(draw, tagline.upper(), tag_font, int(W * 0.55))
        ty = ly + logo_font_size + 20
        for ln in tag_lines:
            bx = draw.textbbox((0, 0), ln, font=tag_font)
            tx = (W - (bx[2] - bx[0])) // 2
            draw.text((tx + 1, ty + 1), ln, font=tag_font, fill=_BLACK_RGB)
            draw.text((tx, ty), ln, font=tag_font, fill=_WHITE_RGB)
            ty += tag_size + 6

        # Handle — bottom center
        handle_size = max(28, W // 60)
        handle_font = _font("label", handle_size)
        bx = draw.textbbox((0, 0), handle.upper(), font=handle_font)
        hx = (W - (bx[2] - bx[0])) // 2
        hy = H - handle_size - int(H * 0.06)
        draw.text((hx + 1, hy + 1), handle.upper(), font=handle_font, fill=_BLACK_RGB)
        draw.text((hx, hy), handle.upper(), font=handle_font, fill=_WHITE_RGB)

        # Bottom violet accent bar
        draw.rectangle([0, H - 6, W, H], fill=_VIOLET_RGB)

        img = _paste_logo(img, size=int(W * 0.04), corner="top-left")

        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path, "PNG", optimize=True)
        return img

    def generate_pack(
        self,
        brief: dict,
        save_dir: Path,
        seed: int = 0,
    ) -> dict:
        """
        Full content pack from a research brief.
        Returns dict with all saved paths.
        """
        save_dir.mkdir(parents=True, exist_ok=True)
        (save_dir / "carousel").mkdir(exist_ok=True)

        title    = brief.get("titulo_principal", "")
        hook     = brief.get("hook_apertura", "")
        subtitle = brief.get("angulo_neurociencia", "")
        datos    = brief.get("datos_clave", [])

        # Carousel slides — one per dato + intro + outro
        slides = [{"hook": hook, "headline": title, "cta": "DESLIZA →"}]
        for dato in datos[:6]:
            words = dato.split()
            hl    = " ".join(words[:4]).upper() if len(words) > 4 else dato.upper()
            slides.append({"hook": dato, "headline": hl, "cta": "SIGUIENTE →"})
        slides.append({
            "hook": "¿QUIERES SABER MÁS?",
            "headline": "SÍGUENOS",
            "cta": "@IMMUSICSELLO",
        })

        post_path  = save_dir / "post.png"
        story_path = save_dir / "story.png"
        tiktok_path= save_dir / "tiktok.png"
        thumb_path = save_dir / "thumbnail.png"

        return {
            "post":      self.generate_post(hook, title, save_path=post_path, seed=seed),
            "story":     self.generate_story(hook, title, save_path=story_path, seed=seed),
            "tiktok":    self.generate_tiktok_cover(hook, title, save_path=tiktok_path, seed=seed),
            "thumbnail": self.generate_thumbnail(hook, title, cta=subtitle[:60], save_path=thumb_path, seed=seed),
            "carousel":  self.generate_carousel(slides, save_dir / "carousel", seed=seed),
        }
