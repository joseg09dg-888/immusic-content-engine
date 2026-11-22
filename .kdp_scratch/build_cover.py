# -*- coding: utf-8 -*-
"""Portada completa (contraportada + lomo + portada) para pasta blanda KDP, 6x9", 83 paginas."""
import os
from reportlab.lib.units import inch as INCH
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

ROOT = r"C:\Users\JOSÉ\Projects\immusic-content-engine"
FONTS = os.path.join(ROOT, "assets", "fonts")
OUT_DIR = os.path.join(ROOT, "docs", "libro", "kdp_output")
FRONT_IMG = os.path.join(ROOT, "docs", "libro", "portada_music_business.png")
OUT_PDF = os.path.join(OUT_DIR, "portada_completa_ES.pdf")

VIOLET = colors.HexColor("#5E17EB")
CREAM = colors.HexColor("#F2EDE5")

pdfmetrics.registerFont(TTFont("Anton", os.path.join(FONTS, "Anton-Regular.ttf")))

PAGE_COUNT = 83
SPINE_IN = round(PAGE_COUNT * 0.002252, 4)  # papel blanco
BLEED_IN = 0.125
TRIM_W, TRIM_H = 6.0, 9.0

FULL_W_IN = BLEED_IN + TRIM_W + SPINE_IN + TRIM_W + BLEED_IN
FULL_H_IN = BLEED_IN + TRIM_H + BLEED_IN

PAGE_W = FULL_W_IN * INCH
PAGE_H = FULL_H_IN * INCH

# x de cada panel (en puntos), origen 0 = borde izquierdo con sangrado
x_back_start = 0
x_back_end = (BLEED_IN + TRIM_W) * INCH
x_spine_start = x_back_end
x_spine_end = x_spine_start + SPINE_IN * INCH
x_front_start = x_spine_end
x_front_end = PAGE_W

back_copy = {
    "headline": "¿Sabes cuánto dinero de tu música se está quedando en el camino ahora mismo, sin que tú te enteres?",
    "body": (
        "Cada vez que tu canción suena en un bar, en una radio, en un comercial -- hay un pago "
        "que te corresponde por ley. La mayoría de artistas independientes nunca lo cobra.\n\n"
        "MUSIC BUSINESS PARA TODOS LOS HUMANOS es la guía que un sello discográfico independiente "
        "escribió para dejar de ver a otros artistas firmar contratos a ciegas, regalar sus "
        "derechos por miedo, y perder dinero que legalmente ya era suyo.\n\n"
        "No es un manual legal de 500 páginas para abogados. Es lo que te hubieran explicado el "
        "primer día: qué firmar y qué no firmar, cómo se reparte de verdad el dinero del "
        "streaming, cómo construir una marca que no se vea igual a la de todos los demás, y cómo "
        "diversificar tus ingresos para que tu carrera no dependa de un solo algoritmo.\n\n"
        "Si haces música -- o si diriges a alguien que la hace -- esto es lo que necesitabas leer "
        "antes de tu próximo lanzamiento, no después."
    ),
    "imprint": "IM MUSIC -- REBEL LUXURY",
}


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    c = pdfcanvas.Canvas(OUT_PDF, pagesize=(PAGE_W, PAGE_H))

    # Fondo violeta en todo el lienzo (cubre sangrado y lomo)
    c.setFillColor(VIOLET)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # --- Contraportada (texto) ---
    margin = 0.5 * INCH
    back_x = x_back_start + BLEED_IN * INCH + margin
    back_w = (x_back_end - (x_back_start + BLEED_IN * INCH)) - 2 * margin
    back_y = BLEED_IN * INCH + margin
    back_h = TRIM_H * INCH - 2 * margin

    styles_back_head = ParagraphStyle(
        "bh", fontName="Anton", fontSize=15, leading=19, textColor=colors.white, alignment=TA_LEFT
    )
    styles_back_body = ParagraphStyle(
        "bb", fontName="Helvetica", fontSize=9.3, leading=13.2, textColor=CREAM, alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    styles_back_imprint = ParagraphStyle(
        "bi", fontName="Anton", fontSize=10, leading=13, textColor=CREAM, alignment=TA_LEFT
    )

    frame_back = Frame(back_x, back_y, back_w, back_h, showBoundary=0,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    story_back = [Paragraph(back_copy["headline"], styles_back_head)]
    story_back.append(_spacer(14))
    for para in back_copy["body"].split("\n\n"):
        story_back.append(Paragraph(para.replace("\n", "<br/>"), styles_back_body))
    story_back.append(_spacer(10))
    story_back.append(Paragraph(back_copy["imprint"], styles_back_imprint))
    frame_back.addFromList(story_back, c)

    # Barcode placeholder box (KDP pone su propio codigo de barras; dejamos zona en blanco segura)
    bc_w, bc_h = 2.0 * INCH, 1.2 * INCH
    bc_x = x_back_end - BLEED_IN * INCH - bc_w - 0.25 * INCH
    bc_y = BLEED_IN * INCH + 0.25 * INCH
    c.setFillColor(colors.white)
    c.rect(bc_x, bc_y, bc_w, bc_h, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#999999"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(bc_x + bc_w / 2, bc_y + bc_h / 2, "Zona reservada para codigo de barras (KDP)")

    # --- Lomo ---
    c.saveState()
    c.translate(x_spine_start + (SPINE_IN * INCH) / 2, PAGE_H / 2)
    c.rotate(90)
    c.setFillColor(colors.white)
    c.setFont("Anton", 11)
    c.drawCentredString(0, -4, "MUSIC BUSINESS PARA TODOS LOS HUMANOS -- IM MUSIC")
    c.restoreState()

    # --- Portada frontal (reutiliza el arte ya existente) ---
    img = Image.open(FRONT_IMG)
    c.drawImage(FRONT_IMG, x_front_start, BLEED_IN * INCH, width=(TRIM_W + BLEED_IN) * INCH,
                height=TRIM_H * INCH + BLEED_IN * INCH, preserveAspectRatio=False, mask="auto")

    c.showPage()
    c.save()
    print("OK ->", OUT_PDF)
    print("Paginas interior usadas:", PAGE_COUNT)
    print("Ancho lomo (in):", SPINE_IN)
    print("Dimension total portada (in): %.4f x %.4f" % (FULL_W_IN, FULL_H_IN))
    print("Dimension total portada (px @300dpi): %d x %d" % (FULL_W_IN * 300, FULL_H_IN * 300))


def _spacer(h):
    from reportlab.platypus import Spacer
    return Spacer(1, h)


if __name__ == "__main__":
    build()
