"""Organigrama funcional de IM Music: direccion + maquina de captacion de
clientes (automatizacion IA) + equipo humano + resultado (motores de ingreso).
Identidad de marca IM Music: violeta #5E17EB, Sceageus, Anton."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT_DIR = ROOT / "docs" / "saas_plan"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VIOLETA = (0x5E, 0x17, 0xEB)
VIOLETA_OSCURO = (0x3E, 0x0F, 0x9E)
CREMA = (0xF2, 0xED, 0xE5)
BLANCO = (0xFF, 0xFF, 0xFF)

SCEAGEUS = ASSETS / "fonts" / "sceageus.otf"
ANTON = ASSETS / "fonts" / "Anton-Regular.ttf"

W, H = 1800, 2700


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, text, font, y, fill, canvas_w, tracking=0):
    if tracking:
        widths = [draw.textlength(ch, font=font) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (canvas_w - total) / 2
        for ch, cw in zip(text, widths):
            draw.text((x, y), ch, font=font, fill=fill)
            x += cw + tracking
    else:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = (canvas_w - w) / 2
        draw.text((x - bbox[0], y), text, font=font, fill=fill)


def draw_box(draw, x, y, w, h, title, caption, f_title, f_caption,
             fill, border, title_color, caption_color, radius=20, border_w=3):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=border, width=border_w)
    pad = 24
    inner_w = w - 2 * pad

    title_lines = wrap_text(draw, title, f_title, inner_w)
    cap_lines = wrap_text(draw, caption, f_caption, inner_w) if caption else []

    line_h_title = f_title.size + 6
    line_h_cap = f_caption.size + 6
    total_h = len(title_lines) * line_h_title + (10 if cap_lines else 0) + len(cap_lines) * line_h_cap
    ty = y + (h - total_h) / 2

    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=f_title)
        lw = bbox[2] - bbox[0]
        draw.text((x + (w - lw) / 2 - bbox[0], ty), line, font=f_title, fill=title_color)
        ty += line_h_title

    if cap_lines:
        ty += 10
        for line in cap_lines:
            bbox = draw.textbbox((0, 0), line, font=f_caption)
            lw = bbox[2] - bbox[0]
            draw.text((x + (w - lw) / 2 - bbox[0], ty), line, font=f_caption, fill=caption_color)
            ty += line_h_cap


def arrow_down(draw, x, y0, y1, color=BLANCO, width=4, head=14):
    draw.line([(x, y0), (x, y1)], fill=color, width=width)
    draw.polygon([(x - head, y1 - head), (x + head, y1 - head), (x, y1 + 4)], fill=color)


def section_label(draw, text, y, f_section):
    draw_centered(draw, text, f_section, y, BLANCO, W, tracking=2)


def build():
    img = Image.new("RGB", (W, H), VIOLETA)
    draw = ImageDraw.Draw(img)

    f_brand = ImageFont.truetype(str(ANTON), 28)
    f_h1 = ImageFont.truetype(str(SCEAGEUS), 70)
    f_section = ImageFont.truetype(str(SCEAGEUS), 38)
    f_box_title = ImageFont.truetype(str(ANTON), 24)
    f_box_title_sm = ImageFont.truetype(str(ANTON), 21)
    f_box_caption = ImageFont.truetype(str(ANTON), 16)

    # Header
    draw_centered(draw, "IM MUSIC", f_brand, 50, CREMA, W, tracking=8)
    draw_centered(draw, "ORGANIGRAMA FUNCIONAL", f_h1, 110, BLANCO, W)
    draw_centered(draw, "DIRECCION + AUTOMATIZACION IA + EQUIPO + RESULTADO", f_box_title_sm, 205, CREMA, W, tracking=3)

    cx = W // 2
    y = 260

    # ---- CAPA 1: DIRECCION ----
    box_w, box_h = 760, 150
    bx = cx - box_w // 2
    draw_box(
        draw, bx, y, box_w, box_h,
        "CEO / DIRECTOR DEL SELLO Y LA PLATAFORMA",
        "Direccion estrategica, A&R, relacion con artistas e inversionistas",
        f_box_title, f_box_caption,
        fill=BLANCO, border=BLANCO, title_color=VIOLETA, caption_color=VIOLETA_OSCURO,
    )
    y_arrow_start = y + box_h
    y += box_h + 70

    arrow_down(draw, cx, y_arrow_start + 10, y - 10)

    # ---- CAPA 2: MAQUINA DE CAPTACION ----
    section_label(draw, "MAQUINA DE CAPTACION DE CLIENTES (AUTOMATIZACION IA)", y, f_section)
    y += 95

    panel_pad = 40
    panel_top = y
    cell_w, cell_h, gap = 780, 190, 30
    grid_w = cell_w * 2 + gap
    grid_x0 = cx - grid_w // 2

    captacion_items = [
        ("BOT DE WHATSAPP CON IA", "Atiende consultas entrantes, califica leads y agenda reuniones automaticamente"),
        ("DM AUTOMATICO EN REDES SOCIALES", "Cuando alguien nuevo sigue a IM Music en Instagram/TikTok, se le envia un mensaje de apertura al instante"),
        ("EMAIL MARKETING AUTOMATIZADO", "Secuencias de correo que nutren leads hasta convertirlos en clientes o candidatos al roster"),
        ("CONTENT ENGINE PROPIO", "Genera contenido, diseno, video y voz 24/7 a costo marginal casi nulo, alimentando todos los canales anteriores"),
    ]

    positions = [
        (grid_x0, panel_top),
        (grid_x0 + cell_w + gap, panel_top),
        (grid_x0, panel_top + cell_h + gap),
        (grid_x0 + cell_w + gap, panel_top + cell_h + gap),
    ]

    panel_h = cell_h * 2 + gap
    draw.rounded_rectangle(
        [grid_x0 - panel_pad, panel_top - panel_pad, grid_x0 + grid_w + panel_pad, panel_top + panel_h + panel_pad],
        radius=28, outline=CREMA, width=3,
    )

    for (bx2, by2), (title, caption) in zip(positions, captacion_items):
        draw_box(
            draw, bx2, by2, cell_w, cell_h, title, caption,
            f_box_title, f_box_caption,
            fill=CREMA, border=CREMA, title_color=VIOLETA, caption_color=VIOLETA_OSCURO,
        )

    y = panel_top + panel_h + panel_pad + 30
    note = "Alimenta tanto a la plataforma SaaS (suscriptores Basico/Pro) como al roster del sello (candidatos a Elite 360)"
    f_note = ImageFont.truetype(str(ANTON), 18)
    draw_centered(draw, note, f_note, y, CREMA, W)
    y += 50

    arrow_down(draw, cx, y, y + 60)
    y += 90

    # ---- CAPA 3: EQUIPO HUMANO ----
    section_label(draw, "EQUIPO HUMANO (EJECUCION Y RELACION)", y, f_section)
    y += 90

    equipo_items = [
        ("PROGRAMADOR / DESARROLLO", "Mantiene y evoluciona la plataforma (unico dev fijo)"),
        ("PROJECT MANAGER ARTIST DEVELOPMENT", "Entrega el servicio Elite 360 a los 12-15 artistas del roster"),
        ("GERENTE COMERCIAL", "Cierra los leads calificados por la Maquina de Captacion"),
        ("PRODUCTOR E INGENIERO DE SONIDO", "Grabacion, mezcla y masterizacion por proyecto (freelance)"),
        ("CONTADOR (ASESOR EXTERNO)", "Finanzas, impuestos y nomina"),
    ]
    n = len(equipo_items)
    e_gap = 20
    e_w = (W - 2 * 60 - (n - 1) * e_gap) // n
    e_h = 230
    ex0 = 60
    for i, (title, caption) in enumerate(equipo_items):
        bx3 = ex0 + i * (e_w + e_gap)
        draw_box(
            draw, bx3, y, e_w, e_h, title, caption,
            f_box_title_sm, f_box_caption,
            fill=VIOLETA, border=BLANCO, title_color=BLANCO, caption_color=CREMA, border_w=2,
        )
    y += e_h + 70

    arrow_down(draw, cx, y - 50, y - 5)

    # ---- CAPA 4: RESULTADO ----
    section_label(draw, "RESULTADO: 4 MOTORES DE INGRESO", y, f_section)
    y += 90

    resultado_items = [
        ("CLIENTES PLATAFORMA\nBASICO / PRO", "Escala masiva, autoservicio"),
        ("ROSTER DEL SELLO\nELITE 360", "Maximo 12-15 artistas"),
        ("LECTORES DEL LIBRO", "Music Business Para Todos Los Humanos"),
        ("AUDIENCIA CANAL YOUTUBE", "Monetizacion publicitaria propia"),
    ]
    n2 = len(resultado_items)
    r_gap = 24
    r_w = (W - 2 * 60 - (n2 - 1) * r_gap) // n2
    r_h = 220
    rx0 = 60
    for i, (title, caption) in enumerate(resultado_items):
        bx4 = rx0 + i * (r_w + r_gap)
        draw_box(
            draw, bx4, y, r_w, r_h, title.replace("\n", " "), caption,
            f_box_title_sm, f_box_caption,
            fill=CREMA, border=CREMA, title_color=VIOLETA, caption_color=VIOLETA_OSCURO, border_w=2,
        )
    y += r_h + 60

    draw_centered(draw, "NO LANZAMOS MUSICA. JAQUEAMOS MENTES.", f_box_caption, y, CREMA, W, tracking=2)
    y += 40

    final_h = y + 40
    img = img.crop((0, 0, W, final_h))

    out = OUT_DIR / "organigrama_funcional_im_music.png"
    img.save(out)
    print(f"OK: {out} ({out.stat().st_size // 1024}KB) — {W}x{final_h}")


if __name__ == "__main__":
    build()
