# -*- coding: utf-8 -*-
"""Convierte un .docx a un .pdf legible (sin Word/LibreOffice), para deposito ante la DNDA."""
import sys
import docx
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from xml.sax.saxutils import escape

SRC = sys.argv[1]
OUT = sys.argv[2]

d = docx.Document(SRC)

normal = ParagraphStyle("normal", fontName="Helvetica", fontSize=10.5, leading=14.5,
                         alignment=TA_LEFT, spaceAfter=8, textColor=colors.black)
heading = ParagraphStyle("heading", fontName="Helvetica-Bold", fontSize=13, leading=17,
                          alignment=TA_LEFT, spaceBefore=14, spaceAfter=8, textColor=colors.black)
title = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=17, leading=22,
                        alignment=TA_LEFT, spaceAfter=10, textColor=colors.black)

story = []
for p in d.paragraphs:
    text = p.text.strip()
    if not text:
        story.append(Spacer(1, 6))
        continue
    is_bold_run = any(r.bold for r in p.runs if r.text.strip())
    size = max([r.font.size.pt if r.font.size else 0 for r in p.runs] or [0])
    safe = escape(text)
    for r in p.runs:
        if r.bold and r.text.strip() and r.text in text:
            safe = safe.replace(escape(r.text), f"<b>{escape(r.text)}</b>")
    if size >= 16 or (is_bold_run and size >= 14):
        story.append(Paragraph(safe, title))
    elif is_bold_run and size >= 12:
        story.append(Paragraph(safe, heading))
    else:
        story.append(Paragraph(safe, normal))

doc = SimpleDocTemplate(OUT, pagesize=LETTER,
                         leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                         topMargin=0.8 * inch, bottomMargin=0.8 * inch)
doc.build(story)
print("OK ->", OUT, "| parrafos:", len(d.paragraphs))
