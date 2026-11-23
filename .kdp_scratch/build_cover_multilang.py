# -*- coding: utf-8 -*-
"""Portada completa (contraportada + lomo + portada) para pasta blanda KDP, 6x9", EN/PT."""
import os
import sys
from reportlab.lib.units import inch as INCH
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

LANG = sys.argv[1] if len(sys.argv) > 1 else "EN"
assert LANG in ("EN", "PT")

ROOT = r"C:\Users\JOSÉ\Projects\immusic-content-engine"
FONTS = os.path.join(ROOT, "assets", "fonts")
OUT_DIR = os.path.join(ROOT, "docs", "libro", "kdp_output")

VIOLET = colors.HexColor("#5E17EB")
CREAM = colors.HexColor("#F2EDE5")

pdfmetrics.registerFont(TTFont("Anton", os.path.join(FONTS, "Anton-Regular.ttf")))

CONFIG = {
    "EN": dict(
        front_img=os.path.join(ROOT, "docs", "libro", "portada_music_business_EN.png"),
        interior_pdf=os.path.join(OUT_DIR, "interior_EN_6x9.pdf"),
        out=os.path.join(OUT_DIR, "portada_completa_EN.pdf"),
        spine_text="MUSIC BUSINESS FOR EVERY HUMAN -- IM MUSIC",
        barcode_note="Zone reserved for barcode (KDP)",
        back=dict(
            headline="Do you know how much money from your music is slipping away right now, without you even knowing it?",
            body=(
                "Every time your song plays in a bar, on the radio, in a commercial -- there's a "
                "payment that's legally yours. Most independent artists never collect it.\n\n"
                "MUSIC BUSINESS FOR EVERY HUMAN is the guide an independent record label wrote after "
                "watching too many artists sign contracts blind, give away their rights out of fear, "
                "and lose money that was legally already theirs.\n\n"
                "It's not a 500-page legal manual for lawyers. It's what you should have been told on "
                "day one: what to sign and what not to sign, how streaming money is really split, how "
                "to build a brand that doesn't look like everyone else's, and how to diversify your "
                "income so your career doesn't depend on a single algorithm.\n\n"
                "If you make music -- or you manage someone who does -- this is what you needed to "
                "read before your next release, not after."
            ),
            imprint="IM MUSIC -- REBEL LUXURY",
        ),
    ),
    "PT": dict(
        front_img=os.path.join(ROOT, "docs", "libro", "portada_music_business_PT.png"),
        interior_pdf=os.path.join(OUT_DIR, "interior_PT_6x9.pdf"),
        out=os.path.join(OUT_DIR, "portada_completa_PT.pdf"),
        spine_text="MUSIC BUSINESS PARA TODOS OS HUMANOS -- IM MUSIC",
        barcode_note="Área reservada para código de barras (KDP)",
        back=dict(
            headline="Você sabe quanto dinheiro da sua música está ficando pelo caminho agora mesmo, sem que você saiba?",
            body=(
                "Toda vez que sua música toca em um bar, numa rádio, num comercial -- existe um "
                "pagamento que é seu por direito. A maioria dos artistas independentes nunca recebe "
                "esse valor.\n\n"
                "MUSIC BUSINESS PARA TODOS OS HUMANOS é o guia que um selo discográfico independente "
                "escreveu depois de ver outros artistas assinarem contratos às cegas, abrirem mão de "
                "seus direitos por medo, e perderem dinheiro que já era legalmente deles.\n\n"
                "Não é um manual jurídico de 500 páginas para advogados. É o que deveriam ter te "
                "explicado no primeiro dia: o que assinar e o que não assinar, como o dinheiro do "
                "streaming é realmente dividido, como construir uma marca que não pareça igual à de "
                "todo mundo, e como diversificar sua renda para que sua carreira não dependa de um "
                "único algoritmo.\n\n"
                "Se você faz música -- ou gerencia alguém que faz -- isto é o que você precisava ler "
                "antes do seu próximo lançamento, não depois."
            ),
            imprint="IM MUSIC -- REBEL LUXURY",
        ),
    ),
}

cfg = CONFIG[LANG]

PAGE_COUNT = len(PdfReader(cfg["interior_pdf"]).pages)
SPINE_IN = round(PAGE_COUNT * 0.002252, 4)  # papel blanco
BLEED_IN = 0.125
TRIM_W, TRIM_H = 6.0, 9.0

FULL_W_IN = BLEED_IN + TRIM_W + SPINE_IN + TRIM_W + BLEED_IN
FULL_H_IN = BLEED_IN + TRIM_H + BLEED_IN

PAGE_W = FULL_W_IN * INCH
PAGE_H = FULL_H_IN * INCH

x_back_start = 0
x_back_end = (BLEED_IN + TRIM_W) * INCH
x_spine_start = x_back_end
x_spine_end = x_spine_start + SPINE_IN * INCH
x_front_start = x_spine_end


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    c = pdfcanvas.Canvas(cfg["out"], pagesize=(PAGE_W, PAGE_H))

    c.setFillColor(VIOLET)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

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
    story_back = [Paragraph(cfg["back"]["headline"], styles_back_head), Spacer(1, 14)]
    for para in cfg["back"]["body"].split("\n\n"):
        story_back.append(Paragraph(para.replace("\n", "<br/>"), styles_back_body))
    story_back.append(Spacer(1, 10))
    story_back.append(Paragraph(cfg["back"]["imprint"], styles_back_imprint))
    frame_back.addFromList(story_back, c)

    bc_w, bc_h = 2.0 * INCH, 1.2 * INCH
    bc_x = x_back_end - BLEED_IN * INCH - bc_w - 0.25 * INCH
    bc_y = BLEED_IN * INCH + 0.25 * INCH
    c.setFillColor(colors.white)
    c.rect(bc_x, bc_y, bc_w, bc_h, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#999999"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(bc_x + bc_w / 2, bc_y + bc_h / 2, cfg["barcode_note"])

    # Lomo sin texto: a este numero de paginas el lomo mide menos de 0.19", y KDP
    # exige 0.0625" de margen a cada lado del texto, dejando menos de 5pt utiles.
    # Cualquier texto legible viola ese margen y KDP lo rechaza en revision.

    img_path = cfg["front_img"]
    c.drawImage(img_path, x_front_start, BLEED_IN * INCH, width=(TRIM_W + BLEED_IN) * INCH,
                height=TRIM_H * INCH + BLEED_IN * INCH, preserveAspectRatio=False, mask="auto")

    c.showPage()
    c.save()
    print("OK ->", cfg["out"])
    print("Paginas interior:", PAGE_COUNT)
    print("Ancho lomo (in):", SPINE_IN)
    print("Dimension total portada (in): %.4f x %.4f" % (FULL_W_IN, FULL_H_IN))


if __name__ == "__main__":
    build()
