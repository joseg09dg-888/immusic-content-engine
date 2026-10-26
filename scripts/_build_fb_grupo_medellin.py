"""Genera 2 piezas para el grupo de Facebook 'Red de Musicos en Medellin':
1) Banner/portada de Facebook (1640x624, 2x de 820x312)
2) Imagen cuadrada para publicar dentro del grupo (1080x1080)
Identidad de marca IM Music: violeta #5E17EB, Sceageus, Anton, grabado de microfono."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT_DIR = ROOT / "docs" / "libro"

VIOLETA = (0x5E, 0x17, 0xEB)
CREMA = (0xF2, 0xED, 0xE5)
BLANCO = (0xFF, 0xFF, 0xFF)

SCEAGEUS = ASSETS / "fonts" / "sceageus.otf"
ANTON = ASSETS / "fonts" / "Anton-Regular.ttf"
LOGO = ASSETS / "logo" / "logo_immusic.png"
MIC_ILLUS = ASSETS / "illustrations" / "illus_mic.png"


def load_illustration_as_black_alpha(path, opacity=1.0):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    arr[:, :, 3] = (arr[:, :, 3].astype(float) * opacity).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def white_logo(path, target_w):
    im = Image.open(path).convert("RGBA")
    alpha = im.split()[3]
    white = Image.new("RGBA", im.size, (255, 255, 255, 0))
    white.putalpha(alpha)
    ratio = target_w / im.width
    return white.resize((target_w, int(im.height * ratio)), Image.LANCZOS)


def draw_centered(draw, text, font, y, fill, canvas_w, tracking=0):
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


def build_banner():
    W, H = 1640, 624
    img = Image.new("RGB", (W, H), VIOLETA)

    mic = load_illustration_as_black_alpha(MIC_ILLUS, opacity=0.28)
    mic_h = int(H * 1.15)
    ratio = mic_h / mic.height
    mic = mic.resize((int(mic.width * ratio), mic_h), Image.LANCZOS)
    mic_x = W - int(mic.width * 0.62)
    mic_y = H - mic.height + 40
    img.paste(mic, (mic_x, mic_y), mic)

    draw = ImageDraw.Draw(img)

    logo = white_logo(LOGO, target_w=80)
    pad = 40
    img.paste(logo, (pad, pad), logo)

    f_kicker = ImageFont.truetype(str(ANTON), 22)
    f_greet = ImageFont.truetype(str(ANTON), 28)
    f_title = ImageFont.truetype(str(SCEAGEUS), 64)
    f_cta = ImageFont.truetype(str(ANTON), 24)

    tx = pad
    ty = pad + logo.height + 18

    draw.text((tx, ty), "IM MUSIC", font=f_kicker, fill=CREMA)
    ty += 34
    draw.text((tx, ty), "HOLA, RED DE MUSICOS DE MEDELLIN", font=f_greet, fill=CREMA)
    ty += 50
    draw.text((tx, ty), "MUSIC BUSINESS", font=f_title, fill=BLANCO)
    ty += 70
    draw.text((tx, ty), "PARA TODOS LOS HUMANOS", font=f_title, fill=BLANCO)
    ty += 82
    draw.text((tx, ty), "YA DISPONIBLE · $16,90 USD · LINK EN COMENTARIOS", font=f_cta, fill=CREMA)

    # Nota: todo el texto queda en el 65% superior del banner para no
    # quedar tapado por la foto de perfil que Facebook superpone abajo.

    out = OUT_DIR / "fb_banner_grupo_medellin.png"
    img.save(out)
    print(f"OK: {out} ({out.stat().st_size // 1024}KB) — {W}x{H}")


def build_square():
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), VIOLETA)

    mic = load_illustration_as_black_alpha(MIC_ILLUS, opacity=0.4)
    mic_w = int(W * 0.95)
    ratio = mic_w / mic.width
    mic = mic.resize((mic_w, int(mic.height * ratio)), Image.LANCZOS)
    mic_x = (W - mic.width) // 2
    mic_y = 10
    img.paste(mic, (mic_x, mic_y), mic)

    draw = ImageDraw.Draw(img)

    logo = white_logo(LOGO, target_w=220)
    logo_x = (W - logo.width) // 2
    logo_y = 70
    img.paste(logo, (logo_x, logo_y), logo)

    f_kicker = ImageFont.truetype(str(ANTON), 26)
    f_title = ImageFont.truetype(str(SCEAGEUS), 64)
    f_title_sm = ImageFont.truetype(str(SCEAGEUS), 50)
    f_sub = ImageFont.truetype(str(ANTON), 24)
    f_price = ImageFont.truetype(str(SCEAGEUS), 48)
    f_cta = ImageFont.truetype(str(ANTON), 28)

    y = logo_y + logo.height + 42
    draw_centered(draw, "IM MUSIC", f_kicker, y, CREMA, W, tracking=6)
    y += 50

    draw_centered(draw, "MUSIC BUSINESS", f_title, y, BLANCO, W)
    y += 72
    draw_centered(draw, "PARA TODOS", f_title, y, BLANCO, W)
    y += 72
    draw_centered(draw, "LOS HUMANOS", f_title_sm, y, BLANCO, W)
    y += 80

    line_w = 260
    draw.line([((W - line_w) / 2, y), ((W + line_w) / 2, y)], fill=CREMA, width=3)
    y += 36

    draw_centered(draw, "PARA LA RED DE MUSICOS DE MEDELLIN", f_sub, y, CREMA, W, tracking=2)
    y += 60

    # Price badge
    badge_w, badge_h = 420, 150
    bx = (W - badge_w) // 2
    by = y
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=18, fill=CREMA)
    bd = draw.textbbox((0, 0), "$16,90 USD", font=f_price)
    btw = bd[2] - bd[0]
    draw.text((bx + (badge_w - btw) / 2 - bd[0], by + 22), "$16,90 USD", font=f_price, fill=VIOLETA)
    cta_text = "COMPRA AQUI — LINK EN COMENTARIOS"
    cd = draw.textbbox((0, 0), cta_text, font=f_cta)
    ctw = cd[2] - cd[0]
    draw.text((bx + (badge_w - ctw) / 2 - cd[0], by + 96), cta_text, font=f_cta, fill=VIOLETA)
    y = by + badge_h + 50

    draw_centered(draw, "92 PAGINAS · DERECHOS, CONTRATOS Y REGALIAS", f_sub, y, CREMA, W, tracking=1)

    y_foot = H - 90
    draw_centered(draw, "NO LANZAMOS MUSICA. JAQUEAMOS MENTES.", ImageFont.truetype(str(ANTON), 22), y_foot, CREMA, W, tracking=1)
    draw_centered(draw, "@IMMUSICSELLO", ImageFont.truetype(str(ANTON), 22), y_foot + 32, CREMA, W, tracking=1)

    out = OUT_DIR / "fb_post_grupo_medellin.png"
    img.save(out)
    print(f"OK: {out} ({out.stat().st_size // 1024}KB) — {W}x{H}")


if __name__ == "__main__":
    build_banner()
    build_square()
