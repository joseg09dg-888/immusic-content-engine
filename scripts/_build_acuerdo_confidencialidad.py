# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

VIOLETA = RGBColor(0x5E, 0x17, 0xEB)
NEGRO = RGBColor(0x00, 0x00, 0x00)
GRIS_TEXTO = RGBColor(0x22, 0x22, 0x22)
ROJO = RGBColor(0xB0, 0x20, 0x20)
GRIS_FOOTER = RGBColor(0x66, 0x66, 0x66)


def add(doc, text, font="Georgia", size=11, color=GRIS_TEXTO, bold=False, align=None, space_after=10):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    r = p.add_run(text)
    r.font.name = font
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.bold = bold
    p.paragraph_format.space_after = Pt(space_after)
    return p


def heading(doc, text):
    return add(doc, text, "Bahnschrift", 14.5, VIOLETA, True, None, 8)


def build():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Georgia"
    style.font.size = Pt(11)

    add(doc, "ACUERDO DE CONFIDENCIALIDAD — IM MUSIC", "Bahnschrift", 20, VIOLETA, True, WD_ALIGN_PARAGRAPH.CENTER, 10)

    add(doc, "⚠ ADVERTENCIA LEGAL — PLANTILLA NUEVA, SIN REVISIÓN DE ABOGADO", "Georgia", 10.5, ROJO, True, None, 2)
    add(doc,
        "A diferencia de los otros 6 contratos de este Data Room, este NO es la adaptación de una plantilla previamente revisada por un abogado — se "
        "redactó directamente para este propósito, con asistencia de IA, con fundamento en la Decisión 486 de 2000 de la Comunidad Andina (artículos 260 "
        "a 266) y la Ley 256 de 1996. No ha sido revisado por ningún abogado todavía. Antes de firmarlo con cualquier persona —planta fija o freelance— "
        "un abogado colombiano especializado en propiedad intelectual y derecho laboral/comercial debe revisarlo completo, no solo los cambios frente a "
        "un original, porque aquí no hay un original previamente aprobado.",
        "Georgia", 10.5, ROJO, True, None, 16)

    add(doc,
        "Entre IM MUSIC S.A.S. (en adelante, \"EL SELLO\"), identificada con NIT [NIT], domiciliada en Medellín, Colombia, representada por [NOMBRE DEL "
        "REPRESENTANTE LEGAL], y [NOMBRE DE LA PERSONA], identificado(a) con cédula de ciudadanía [NÚMERO], en adelante \"EL RECEPTOR\", quien presta "
        "servicios a EL SELLO como [ROL — planta fija o contratista freelance, según corresponda], se celebra el presente Acuerdo de Confidencialidad, "
        "que se regirá por las siguientes cláusulas:",
        space_after=14)

    heading(doc, "1. OBJETO")
    add(doc,
        "El presente acuerdo tiene por objeto proteger la información confidencial de EL SELLO a la que EL RECEPTOR tenga o pueda tener acceso en razón "
        "de su cargo, rol o relación contractual con EL SELLO, imponiendo deberes de no divulgación y no uso no autorizado, conforme al régimen de "
        "secretos empresariales previsto en la Decisión 486 de 2000 de la Comunidad Andina.",
        space_after=14)

    heading(doc, "2. INFORMACIÓN CONFIDENCIAL DEFINIDA")
    add(doc,
        "Para efectos de este acuerdo, se considera información confidencial, de forma no taxativa:",
        space_after=6)
    add(doc, "a. La metodología de construcción de marca de artista del sello (diagnóstico, investigación, lenguaje y comunicación, identidad, contenido, marketing y pauta).", space_after=4)
    add(doc, "b. La metodología de composición musical con neurociencia y psicología del comportamiento aplicada.", space_after=4)
    add(doc, "c. La metodología de lanzamiento de canciones (arquitectura de fases, estrategia de plataformas y algoritmos).", space_after=4)
    add(doc, "d. Cualquier documento financiero interno: modelos financieros, proyecciones, estructura de costos, tarifas negociadas con artistas o terceros.", space_after=4)
    add(doc, "e. Cualquier documento estratégico interno: plan de negocios, matriz de riesgos, manual de funciones, contratos vigentes, catálogo de artistas y sus términos.", space_after=4)
    add(doc,
        "No se considera confidencial la información que sea de dominio público sin incumplimiento de este acuerdo, que EL RECEPTOR ya conociera "
        "lícitamente antes de esta relación con evidencia escrita de ello, o que deba revelarse por orden de autoridad competente.",
        space_after=14)

    heading(doc, "3. OBLIGACIONES DE EL RECEPTOR")
    add(doc,
        "EL RECEPTOR se obliga a: no divulgar la información confidencial a ningún tercero sin autorización previa y escrita de EL SELLO; no usarla para "
        "ningún fin distinto al cumplimiento de sus funciones dentro de EL SELLO; no reproducirla, copiarla o extraerla fuera de las herramientas "
        "autorizadas por EL SELLO (Notion, Google Drive corporativo) sin autorización; y devolver o destruir, a solicitud de EL SELLO o a la terminación "
        "de su relación con este, cualquier copia física o digital en su poder. Esta obligación aplica por igual sea EL RECEPTOR personal de planta fija "
        "o contratista freelance — la naturaleza de la relación laboral o comercial no modifica el alcance de este deber.",
        space_after=14)

    heading(doc, "4. EXCEPCIONES")
    add(doc,
        "EL RECEPTOR podrá divulgar información confidencial cuando así lo exija una autoridad judicial o administrativa competente, siempre que notifique "
        "a EL SELLO con antelación razonable cuando la ley lo permita, para que este pueda tomar las medidas de protección que considere pertinentes.",
        space_after=14)

    heading(doc, "5. DURACIÓN DE LA OBLIGACIÓN")
    add(doc,
        "El deber de confidencialidad aquí establecido permanece vigente durante toda la relación de EL RECEPTOR con EL SELLO, y continúa indefinidamente "
        "después de su terminación, en tanto la información conserve su carácter de secreta y su valor comercial para EL SELLO.",
        space_after=14)

    heading(doc, "6. FUNDAMENTO LEGAL")
    add(doc,
        "Este acuerdo se fundamenta en el régimen de secretos empresariales de la Decisión 486 de 2000 de la Comunidad Andina, artículos 260 a 266 — en "
        "particular el artículo 265, que impone el deber de no divulgar ni usar información confidencial a quien accedió a ella por razón de su cargo, "
        "profesión o relación comercial — y en la Ley 256 de 1996 sobre competencia desleal, en lo que resulte aplicable.",
        space_after=14)

    heading(doc, "7. CONSECUENCIAS DEL INCUMPLIMIENTO")
    add(doc,
        "El incumplimiento de este acuerdo por parte de EL RECEPTOR da lugar a las acciones civiles y, cuando corresponda, las acciones por competencia "
        "desleal que la ley colombiana prevea, incluyendo la reparación de los perjuicios que el incumplimiento cause a EL SELLO. [DEFINIR CON EL ABOGADO "
        "SI SE INCLUYE UNA CLÁUSULA PENAL PECUNIARIA ESPECÍFICA Y SU MONTO — NO SE FIJA AQUÍ UNA CIFRA SIN ESA REVISIÓN].",
        space_after=14)

    heading(doc, "8. LEY APLICABLE Y JURISDICCIÓN")
    add(doc,
        "Este acuerdo se rige por las leyes de la República de Colombia. Las partes se someten a los jueces civiles del circuito de Medellín, Antioquia, "
        "para la resolución de cualquier controversia derivada de este acuerdo.",
        space_after=18)

    heading(doc, "9. FIRMAS")
    add(doc, "POR EL SELLO: _________________________ Nombre: [NOMBRE] — C.C./NIT: [NÚMERO]", "Georgia", 11, VIOLETA, True, None, 8)
    add(doc, "EL RECEPTOR: _________________________ Nombre: [NOMBRE] — C.C.: [NÚMERO]", "Georgia", 11, VIOLETA, True, None, 20)

    add(doc,
        "Redactado desde cero con asistencia de IA para IM Music, a partir del régimen de secretos empresariales de la Decisión 486 de 2000 y la Ley 256 "
        "de 1996 — no es la adaptación de una plantilla previamente revisada por un abogado, como sí lo son los otros 6 contratos de este Data Room.",
        "Georgia", 9.5, GRIS_FOOTER, False, None, 0)

    doc.save("docs/sello_plan/data_room/Acuerdo_de_Confidencialidad_IM_Music.docx")
    print("OK: Acuerdo_de_Confidencialidad_IM_Music.docx")


if __name__ == "__main__":
    build()
