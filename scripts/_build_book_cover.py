"""Genera la portada del libro como imagen PNG con identidad de marca real
(violeta #5E17EB, Sceageus, Anton, logo IM Music) — 1800x2700 (6x9in @300dpi)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT_PATH = ROOT / "docs" / "libro" / "portada_music_business.png"

W, H = 1800, 2700
VIOLETA = (0x5E, 0x17, 0xEB)
CREMA = (0xF2, 0xED, 0xE5)
BLANCO = (0xFF, 0xFF, 0xFF)

SCEAGEUS = ASSETS / "fonts" / "sceageus.otf"
ANTON = ASSETS / "fonts" / "Anton-Regular.ttf"
LOGO = ASSETS / "logo" / "logo_immusic.png"


def white_logo(path, target_w):
    im = Image.open(path).convert("RGBA")
    alpha = im.split()[3]
    white = Image.new("RGBA", im.size, (255, 255, 255, 0))
    white.putalpha(alpha)
    ratio = target_w / im.width
    return white.resize((target_w, int(im.height * ratio)), Image.LANCZOS)


def draw_centered(draw, text, font, y, fill, canvas_w=W, tracking=0):
    if tracking:
        widths = [draw.textlength(ch, font=font) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (canvas_w - total) / 2
        for ch, w in zip(text, widths):
            draw.text((x, y), ch, font=font, fill=fill)
            x += w + tracking
    else:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = (canvas_w - w) / 2
        draw.text((x - bbox[0], y), text, font=font, fill=fill)


def main():
    img = Image.new("RGB", (W, H), VIOLETA)
    draw = ImageDraw.Draw(img)

    logo = white_logo(LOGO, target_w=520)
    logo_x = (W - logo.width) // 2
    logo_y = 260
    img.paste(logo, (logo_x, logo_y), logo)

    f_kicker = ImageFont.truetype(str(ANTON), 46)
    f_title = ImageFont.truetype(str(SCEAGEUS), 128)
    f_sub = ImageFont.truetype(str(ANTON), 44)
    f_foot = ImageFont.truetype(str(ANTON), 34)

    y = logo_y + logo.height + 90
    draw_centered(draw, "IM MUSIC", f_kicker, y, CREMA, tracking=10)
    y += 100

    draw_centered(draw, "MUSIC BUSINESS", f_title, y, BLANCO)
    y += 150
    draw_centered(draw, "PARA TODOS", f_title, y, BLANCO)
    y += 150
    f_title_sm = ImageFont.truetype(str(SCEAGEUS), 92)
    draw_centered(draw, "LOS HUMANOS", f_title_sm, y, BLANCO)
    y += 170

    # Divider line
    line_w = 340
    draw.line([((W - line_w) / 2, y), ((W + line_w) / 2, y)], fill=CREMA, width=3)
    y += 60

    draw_centered(draw, "LA GUIA REBEL LUXURY DE LA", f_sub, y, CREMA, tracking=3)
    y += 58
    draw_centered(draw, "INDUSTRIA MUSICAL", f_sub, y, CREMA, tracking=3)

    y_foot = H - 260
    draw_centered(draw, "NO LANZAMOS MUSICA. JAQUEAMOS MENTES.", f_foot, y_foot, CREMA, tracking=2)
    draw_centered(draw, "@IMMUSICSELLO", f_foot, y_foot + 60, CREMA, tracking=2)

    img.save(OUT_PATH)
    print(f"OK: {OUT_PATH} ({OUT_PATH.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
