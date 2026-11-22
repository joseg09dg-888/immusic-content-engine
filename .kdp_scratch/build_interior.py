# -*- coding: utf-8 -*-
"""Genera el interior del libro para KDP (6x9", pasta blanda) a partir del .docx."""
import os
from docx import Document
from reportlab.lib.units import inch as INCH
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Flowable,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = r"C:\Users\JOSÉ\Projects\immusic-content-engine"
FONTS = os.path.join(ROOT, "assets", "fonts")
DOCX_PATH = os.path.join(ROOT, "docs", "libro", "Music_Business_Para_Todos_Los_Humanos_IM_Music.docx")
OUT_DIR = os.path.join(ROOT, "docs", "libro", "kdp_output")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PDF = os.path.join(OUT_DIR, "interior_ES_6x9.pdf")

PAGE_W, PAGE_H = 6 * INCH, 9 * INCH
# Margen simetrico usando el valor "inside" (el mas estricto) en ambos lados -> siempre cumple
SIDE_MARGIN = 0.5 * INCH
TOP_MARGIN = 0.65 * INCH
BOTTOM_MARGIN = 0.65 * INCH

VIOLET = colors.HexColor("#5E17EB")

# Nota: sceageus.otf usa contornos PostScript (CFF), que reportlab no soporta para incrustar
# (TTFError: "postscript outlines are not supported"). Se usa Anton (TrueType) para todos los
# titulos del interior impreso como fallback explicito -- limitacion real, no un descuido.
pdfmetrics.registerFont(TTFont("Anton", os.path.join(FONTS, "Anton-Regular.ttf")))

styles = {
    "body": ParagraphStyle("body", fontName="Times-Roman", fontSize=10.5, leading=14.5,
                            alignment=TA_JUSTIFY, spaceAfter=7),
    "bullet": ParagraphStyle("bullet", fontName="Times-Roman", fontSize=10.5, leading=14.5,
                              alignment=TA_JUSTIFY, leftIndent=14, spaceAfter=4),
    "part": ParagraphStyle("part", fontName="Anton", fontSize=22, leading=26,
                            textColor=VIOLET, alignment=TA_LEFT, spaceBefore=0, spaceAfter=18),
    "chapter": ParagraphStyle("chapter", fontName="Anton", fontSize=16, leading=19,
                               textColor=colors.black, alignment=TA_LEFT, spaceBefore=4, spaceAfter=12),
    "subhead": ParagraphStyle("subhead", fontName="Times-Bold", fontSize=11.5, leading=15,
                               textColor=colors.black, alignment=TA_LEFT, spaceBefore=10, spaceAfter=6),
    "titlepage_title": ParagraphStyle("tt", fontName="Anton", fontSize=30, leading=34,
                                       textColor=VIOLET, alignment=TA_CENTER, spaceAfter=10),
    "titlepage_sub": ParagraphStyle("ts", fontName="Times-Italic", fontSize=13, leading=17,
                                     alignment=TA_CENTER, spaceAfter=6),
    "titlepage_author": ParagraphStyle("ta", fontName="Anton", fontSize=14, leading=18,
                                        textColor=VIOLET, alignment=TA_CENTER, spaceBefore=40),
    "copyright": ParagraphStyle("cp", fontName="Times-Roman", fontSize=9, leading=13,
                                 alignment=TA_LEFT, spaceAfter=8),
    "toc_title": ParagraphStyle("toct", fontName="Anton", fontSize=18, leading=22,
                                 textColor=VIOLET, alignment=TA_LEFT, spaceAfter=14),
}

toc_style_l1 = ParagraphStyle("toc1", fontName="Times-Bold", fontSize=11, leading=16, textColor=VIOLET)
toc_style_l2 = ParagraphStyle("toc2", fontName="Times-Roman", fontSize=10, leading=14, leftIndent=14)

CHAPTER_PREFIXES = ("CAPÍTULO", "CAPITULO")
CHAPTER_EXACT_STARTS = (
    "28.", "29.", "30.", "31.", "32.",
    "METODOLOGÍA IM MUSIC", "HERRAMIENTAS RÁPIDAS", "HISTORIAS DE LA INDUSTRIA",
    "RECURSOS Y PRÓXIMOS PASOS",
)


class _Marker(Flowable):
    """Flowable invisible que solo sirve para notificar el TOC con la pagina real."""
    def __init__(self, level, text):
        Flowable.__init__(self)
        self.level = level
        self.text = text
        self.width = 0
        self.height = 0

    def draw(self):
        pass


def is_bold(p):
    runs = [r for r in p.runs if r.text.strip()]
    return bool(runs) and all(r.bold for r in runs)


def clean(text):
    return (text.replace("\u2013", "-").replace("\u2014", "--")
                .replace("\u2018", "'").replace("\u2019", "'")
                .replace("\u201c", '"').replace("\u201d", '"')
                .replace("&", "&amp;"))


def classify(text, bold):
    t = text.strip()
    if not bold:
        return "body"
    tu = t.upper()
    if tu.startswith("PARTE "):
        return "part"
    if tu.startswith(CHAPTER_PREFIXES) or tu == "CIERRE" or any(tu.startswith(s) for s in CHAPTER_EXACT_STARTS):
        return "chapter"
    return "subhead"


def build_story():
    doc = Document(DOCX_PATH)
    paras = doc.paragraphs

    count_parte1 = 0
    first_parte1 = None
    for i, p in enumerate(paras):
        if p.text.strip().upper().startswith("PARTE 1"):
            count_parte1 += 1
            if count_parte1 == 2:
                first_parte1 = i
                break
    assert first_parte1 is not None, "No se encontro el segundo PARTE 1"

    intro_start = next(i for i, p in enumerate(paras) if p.text.strip().upper() == "INTRODUCCIÓN")
    indice_label_idx = next(
        (i for i in range(intro_start, first_parte1) if paras[i].text.strip().upper() == "ÍNDICE"),
        first_parte1,
    )

    title_text = paras[4].text.strip()
    subtitle_text = paras[5].text.strip()
    author_text = paras[6].text.strip()

    story = []

    # Portada interior
    story.append(Spacer(1, 1.8 * INCH))
    story.append(Paragraph(clean(title_text), styles["titlepage_title"]))
    story.append(Paragraph(clean(subtitle_text), styles["titlepage_sub"]))
    story.append(Paragraph(clean(author_text), styles["titlepage_author"]))
    story.append(PageBreak())

    # Copyright
    copy_lines = [
        "MUSIC BUSINESS PARA TODOS LOS HUMANOS",
        "La guía REBEL LUXURY de la industria musical",
        "",
        "(c) 2026 IM Music. Todos los derechos reservados.",
        "",
        "Ninguna parte de este libro puede ser reproducida, distribuida o transmitida en ninguna "
        "forma ni por ningun medio, incluyendo fotocopiado, grabacion u otros metodos electronicos "
        "o mecanicos, sin el permiso previo por escrito de IM Music, excepto en el caso de citas "
        "breves incorporadas en resenas criticas y ciertos otros usos no comerciales permitidos por "
        "la ley de derechos de autor.",
        "",
        "Aviso sobre contenido asistido por inteligencia artificial: partes de este libro "
        "(incluyendo investigacion de apoyo, edicion, y las traducciones a ingles y portugues de la "
        "edicion original en espanol) fueron elaboradas con asistencia de herramientas de "
        "inteligencia artificial, bajo direccion y revision editorial humana de IM Music. El "
        "contenido, la metodologia y las opiniones expresadas son de autoria y responsabilidad de "
        "IM Music.",
        "",
        "Primera edicion: 2026.",
        "",
        "IM Music -- REBEL LUXURY",
        "Medellin, Colombia",
    ]
    for line in copy_lines:
        if line == "":
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph(clean(line), styles["copyright"]))
    story.append(PageBreak())

    # TOC
    toc = TableOfContents()
    toc.levelStyles = [toc_style_l1, toc_style_l2]
    story.append(Paragraph("INDICE", styles["toc_title"]))
    story.append(toc)
    story.append(PageBreak())

    def emit_range(lo, hi):
        i = lo
        while i < hi:
            p = paras[i]
            text = p.text.strip()
            if not text:
                i += 1
                continue
            bold = is_bold(p)
            kind = classify(text, bold)
            style_name = p.style.name
            if kind == "part":
                story.append(PageBreak())
                story.append(Paragraph(clean(text), styles["part"]))
                story.append(_Marker(0, clean(text)))
            elif kind == "chapter":
                story.append(Spacer(1, 14))
                story.append(Paragraph(clean(text), styles["chapter"]))
                story.append(_Marker(1, clean(text)))
            elif kind == "subhead":
                story.append(Paragraph(clean(text), styles["subhead"]))
            else:
                if style_name == "List Bullet":
                    story.append(Paragraph("&#8226;&nbsp;&nbsp;" + clean(text), styles["bullet"]))
                else:
                    story.append(Paragraph(clean(text), styles["body"]))
            i += 1

    emit_range(intro_start, indice_label_idx)
    story.append(PageBreak())
    emit_range(first_parte1, len(paras))

    return story


def make_doc():
    doc = BaseDocTemplate(
        OUT_PDF, pagesize=(PAGE_W, PAGE_H),
        title="Music Business Para Todos Los Humanos",
        author="IM Music",
        leftMargin=SIDE_MARGIN, rightMargin=SIDE_MARGIN,
        topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
    )

    def on_page(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Times-Roman", 9)
        canvas.drawCentredString(PAGE_W / 2, 0.35 * INCH, str(doc_.page))
        canvas.restoreState()

    frame = Frame(SIDE_MARGIN, BOTTOM_MARGIN,
                  PAGE_W - 2 * SIDE_MARGIN, PAGE_H - TOP_MARGIN - BOTTOM_MARGIN, id="body")
    doc.addPageTemplates([PageTemplate(id="body", frames=[frame], onPage=on_page)])

    def after_flowable(flowable):
        if isinstance(flowable, _Marker):
            doc.notify("TOCEntry", (flowable.level, flowable.text, doc.page))

    doc.afterFlowable = after_flowable
    return doc


if __name__ == "__main__":
    story = build_story()
    doc = make_doc()
    doc.multiBuild(story)
    from pypdf import PdfReader
    n = len(PdfReader(OUT_PDF).pages)
    print("OK ->", OUT_PDF, "paginas:", n)
