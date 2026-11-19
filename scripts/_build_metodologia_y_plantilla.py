"""Genera 2 documentos de marca/IP para el Data Room del sello:
1) Metodologia_Composicion_Neurociencia_IM_Music.docx — la metodología propia
   de composición formalizada (generalizada, no atada a una canción específica).
2) Plantilla_Estructura_Inversion_Proyecto_Musical_IM_Music.docx — la plantilla
   reutilizable de estructura de inversión/reparto cuando el sello financia
   100% un proyecto con un artista/productor externo.
Estilo de marca: Bahnschrift violeta para encabezados, Georgia para cuerpo."""
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "sello_plan" / "data_room"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VIOLETA = RGBColor(0x5E, 0x17, 0xEB)
NEGRO = RGBColor(0x00, 0x00, 0x00)
GRIS_TEXTO = RGBColor(0x22, 0x22, 0x22)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)
ROJO = RGBColor(0xB0, 0x20, 0x20)

HEADING_FONT = "Bahnschrift"
BODY_FONT = "Georgia"


def set_cell_background(cell, hex_color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(shd)


def style_heading(doc, text, size, color=VIOLETA, font=HEADING_FONT, space_before=18, space_after=8, align_center=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = color
    r.font.name = font
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if align_center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p


def add_body(doc, text, size=11, italic=False, bold=False, color=GRIS_TEXTO, space_after=8):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = BODY_FONT
    r.font.size = Pt(size)
    r.font.italic = italic
    r.font.bold = bold
    r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(space_after)
    return p


def add_bullet(doc, text, size=11, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet")
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
        r.font.name = BODY_FONT
        r.font.size = Pt(size)
        r.font.color.rgb = VIOLETA
    r = p.add_run(text)
    r.font.name = BODY_FONT
    r.font.size = Pt(size)
    r.font.color.rgb = GRIS_TEXTO
    return p


def add_disclaimer_box(doc, text):
    p = doc.add_paragraph()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), "FBEAEA")
    p._p.get_or_add_pPr().append(shd)
    r = p.add_run(text)
    r.font.name = BODY_FONT
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = ROJO
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(16)


def add_table(doc, header, rows, widths=None):
    n_cols = len(header)
    table = doc.add_table(rows=0, cols=n_cols)
    table.style = "Light Grid Accent 1"
    hdr_cells = table.add_row().cells
    for j, val in enumerate(header):
        hdr_cells[j].text = ""
        p = hdr_cells[j].paragraphs[0]
        r = p.add_run(val)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.name = BODY_FONT
        r.font.color.rgb = BLANCO
        set_cell_background(hdr_cells[j], "5E17EB")
    for row in rows:
        cells = table.add_row().cells
        for j, val in enumerate(row):
            cells[j].text = ""
            p = cells[j].paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            r.font.name = BODY_FONT
            r.font.color.rgb = GRIS_TEXTO
    doc.add_paragraph()


def cover(doc, title, subtitle):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("IM MUSIC")
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.name = HEADING_FONT
    r.font.color.rgb = VIOLETA
    p.paragraph_format.space_after = Pt(4)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run(title)
    r2.font.size = Pt(22)
    r2.font.bold = True
    r2.font.name = HEADING_FONT
    r2.font.color.rgb = NEGRO
    p2.paragraph_format.space_after = Pt(4)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run(subtitle)
    r3.font.size = Pt(11)
    r3.font.italic = True
    r3.font.name = BODY_FONT
    r3.font.color.rgb = GRIS_TEXTO
    p3.paragraph_format.space_after = Pt(20)


DISCLAIMER_METODOLOGIA = (
    "ACTIVO DE MARCA / PROPIEDAD INTELECTUAL INTERNA — NO DISTRIBUIR EXTERNAMENTE SIN REVISIÓN DEL FUNDADOR. "
    "Este documento formaliza, para fines de consistencia operativa y de debida diligencia ante inversionistas, "
    "una metodología que ya se ha aplicado en al menos un caso real (ver Caso_Real_Mosco_Cana_Brava en este mismo "
    "Data Room). No es una obra con derechos de autor registrados a la fecha; su protección hoy es de secreto "
    "comercial/know-how interno, no de propiedad intelectual formalizada. Si se quiere proteger formalmente (registro "
    "de derechos de autor sobre el documento metodológico, marca, o patente de proceso si aplica), un abogado "
    "especializado en propiedad intelectual debe evaluarlo — no se ha hecho todavía."
)

DISCLAIMER_PLANTILLA = (
    "BORRADOR DE PLANTILLA — PENDIENTE DE CONFIRMACIÓN LEGAL DE LA ADAPTACIÓN, NO DEL CONTENIDO BASE. "
    "Los porcentajes y la mecánica de recoupment de este documento provienen de UN acuerdo real ya ejecutado "
    "(el caso Mosco / Caña Brava, ver Caso_Real_Mosco_Cana_Brava en este Data Room), no de una plantilla redactada "
    "por un abogado desde cero para uso general. Antes de usar esta plantilla con un artista o productor real, un "
    "abogado colombiano especializado en entretenimiento/propiedad intelectual debe confirmar que generalizar este "
    "acuerdo puntual a una plantilla estándar es correcto, y ajustar cualquier cláusula que dependía de las "
    "circunstancias específicas del caso original. Para operaciones en Dubái/EAU no existe ningún documento base "
    "revisado para esa jurisdicción."
)


def build_metodologia():
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(11)

    cover(
        doc,
        "METODOLOGÍA DE COMPOSICIÓN CON NEUROCIENCIA",
        "Arquitectura de un hit: neurociencia, psicología del comportamiento y retención algorítmica aplicadas a la composición musical",
    )
    add_disclaimer_box(doc, DISCLAIMER_METODOLOGIA)

    style_heading(doc, "0. QUÉ ES ESTE DOCUMENTO", 15)
    add_body(
        doc,
        "El plan de negocios del sello (Sección 3.1 y DOFA) hace referencia constante a “la metodología propia "
        "de desarrollo de marca y de artista del fundador” como el activo diferencial del negocio. Este documento "
        "es lo que convierte esa afirmación en algo concreto y revisable por un inversionista: la metodología real, "
        "ya aplicada, que IM Music usa para componer canciones diseñadas deliberadamente para capturar atención, "
        "generar identificación emocional y maximizar reproducción repetida. No está atada a un género ni a un "
        "artista en particular — se diseñó para un caso de rap/trap urbano con jerga de Medellín, pero los cinco "
        "principios que la componen son agnósticos al género, consistente con la vocación multigénero y multiidioma "
        "del sello (ver Sección 2 del plan de negocios).",
    )

    style_heading(doc, "1. LOS 5 PRINCIPIOS DE NEUROCIENCIA APLICADA", 15)

    add_bullet(
        doc,
        "El cerebro humano decide si descarta un estímulo auditivo en los primeros 0 a 3 segundos. La metodología "
        "elimina cualquier preámbulo instrumental y abre directamente con una brecha de curiosidad o una pregunta "
        "incómoda que obliga a la corteza prefrontal a quedarse para resolverla, en vez de pasar a la siguiente "
        "canción (skip).",
        bold_lead="1. Eliminación de intro / “Open Loop” de expectativa (Pattern Interrupt). ",
    )
    add_bullet(
        doc,
        "La dopamina, el neurotransmisor del deseo y la recompensa, alcanza su pico durante la anticipación, no solo "
        "en el clímax. Rimas internas encadenadas y una cadencia creciente mantienen al sistema nervioso en alerta "
        "progresiva hasta liberar la tensión en el estribillo o clímax.",
        bold_lead="2. Arquitectura de dopamina (anticipación y descarga). ",
    )
    add_bullet(
        doc,
        "Usar el lenguaje real, auténtico y sin filtro del público objetivo (jerga local, expresiones propias de su "
        "cultura o comunidad) desactiva el filtro crítico del oyente. Al reconocer su propio lenguaje, se activan las "
        "neuronas espejo, generando empatía inmediata y el impulso de compartir la pieza. Este principio se adapta al "
        "idioma, dialecto o jerga de cada mercado objetivo — no está atado al paisa de Medellín, es el mecanismo el "
        "que se repite, no la jerga específica.",
        bold_lead="3. Efecto espejo e identificación cultural. ",
    )
    add_bullet(
        doc,
        "Consonantes explosivas y la repetición estratégica de imágenes sensoriales crean un circuito de "
        "reverberación auditiva en la memoria de trabajo, haciendo que frases clave se queden sonando en la mente "
        "del oyente durante horas después de escuchar la canción.",
        bold_lead="4. Bucle fonológico (recordación en memoria de trabajo). ",
    )
    add_bullet(
        doc,
        "El cerebro humano tolera mal las historias inconclusas o los patrones rítmicos interrumpidos. Cortar el "
        "último verso antes de resolver la rima esperada, con un corte seco a silencio, genera una tensión cognitiva "
        "que induce al oyente a darle replay de inmediato.",
        bold_lead="5. Efecto Zeigarnik y cierre incompleto (adicción y replay). ",
    )

    style_heading(doc, "2. ARQUITECTURA DE RETENCIÓN PARA TIKTOK, REELS Y SPOTIFY", 15)
    add_body(
        doc,
        "Una canción diseñada con esta metodología se construye con la misma ingeniería de retención que un video "
        "viral de alto rendimiento, no solo como pieza musical:",
    )
    add_bullet(
        doc,
        "El arranque vocal frontal, sin preámbulo, funciona como un golpe visual/auditivo que frena el desplazamiento "
        "del dedo en TikTok e Instagram Reels.",
        bold_lead="Hook de detención de scroll (primeros 3 segundos). ",
    )
    add_bullet(
        doc,
        "Cada par de versos cambia de plano narrativo o sube la intensidad dramática, simulando cortes de edición "
        "dinámicos en video, para evitar caídas en la curva de retención a mitad del track.",
        bold_lead="Cero versos de relleno. ",
    )
    add_bullet(
        doc,
        "La canción incluye 2 a 3 segmentos independientes de 15 a 20 segundos, diseñados para funcionar como audios "
        "tendencia recortables en TikTok e Instagram.",
        bold_lead="Soundbites virales pre-diseñados. ",
    )
    add_bullet(
        doc,
        "La última línea, incompleta, enlaza temática y rítmicamente con la apertura de la canción, favoreciendo la "
        "reproducción en bucle continuo.",
        bold_lead="Bucle circular (loop infinito). ",
    )
    add_bullet(
        doc,
        "La duración estándar de referencia usada hasta ahora es 2:30 minutos: suficiente para desarrollar una "
        "narrativa completa, pero ágil para mantener la curva de retención alta. Es un punto de partida, no una regla "
        "fija — se ajusta según plataforma y género.",
        bold_lead="Duración calibrada. ",
    )

    style_heading(doc, "3. VALIDACIÓN: CASO APLICADO REAL", 15)
    add_body(
        doc,
        "Esta metodología ya se aplicó íntegramente en una propuesta ejecutiva real de coproducción 100% financiada "
        "por IM Music para el artista Mosco (Caña Brava), con producción instrumental de CH The Producer, usando "
        "jerga paisa auténtica de Medellín y una referencia rítmica estilo ‘The Way I Am’ (Eminem). El documento "
        "completo de esa propuesta, incluyendo la letra calibrada bajo los 5 principios, está archivado por separado "
        "en este Data Room (Caso_Real_Mosco_Cana_Brava_Propuesta_Original.docx) y no se reproduce aquí porque es obra "
        "creativa específica de ese proyecto, no parte de la metodología generalizada. La estructura de inversión y "
        "reparto de derechos usada en ese caso real se formalizó, también de forma generalizada, en el documento "
        "Plantilla_Estructura_Inversion_Proyecto_Musical_IM_Music.docx, el compañero financiero de este documento.",
    )

    doc.save(str(OUT_DIR / "Metodologia_Composicion_Neurociencia_IM_Music.docx"))
    print("OK:", OUT_DIR / "Metodologia_Composicion_Neurociencia_IM_Music.docx")


def build_plantilla():
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(11)

    cover(
        doc,
        "PLANTILLA: ESTRUCTURA DE INVERSIÓN EN PROYECTO MUSICAL",
        "Reparto de publishing, máster y regalías cuando IM Music financia 100% un proyecto con un artista o productor externo",
    )
    add_disclaimer_box(doc, DISCLAIMER_PLANTILLA)

    style_heading(doc, "0. CUÁNDO SE USA ESTA PLANTILLA", 15)
    add_body(
        doc,
        "Esta es la mecánica concreta detrás de lo que el plan de negocios del sello (Sección 10, línea de "
        "“Regalías de catálogo propio”) describe como “inversión activa del sello en el desarrollo de sus "
        "propios artistas” y “regalías negociadas caso por caso cuando el sello invierte capital en un proyecto "
        "específico”. Se aplica cuando IM Music decide financiar íntegramente la producción de una canción con un "
        "artista (del roster o externo) y, normalmente, un productor musical externo que aporta el beat/instrumental. "
        "Cada proyecto se negocia caso por caso — los porcentajes de abajo son el punto de partida de referencia, no "
        "una tarifa fija.",
    )

    style_heading(doc, "1. QUIÉN APORTA QUÉ", 15)
    add_table(
        doc,
        ["Parte", "Aporte", "Riesgo financiero"],
        [
            [
                "IM Music (sello)",
                "Concepto y letra (metodología propia de composición con neurociencia), financiación 100% del beat/"
                "producción, estudio, mezcla, máster, video oficial y pauta de lanzamiento.",
                "Asume el 100% del riesgo financiero del proyecto.",
            ],
            [
                "Artista",
                "Interpretación vocal, imagen, identidad pública, difusión del lanzamiento en sus propios canales.",
                "Sin riesgo financiero.",
            ],
            [
                "Productor musical externo",
                "Creación instrumental del beat, ingeniería de mezcla y masterización.",
                "Sin riesgo financiero (cobra honorarios fijos por el trabajo, no participa de la inversión).",
            ],
        ],
    )

    style_heading(doc, "2. REPARTO DE PUBLISHING (AUTORÍA DE LETRA Y MÚSICA)", 15)
    add_body(
        doc,
        "El publishing remunera la autoría intelectual de la obra (letra y música) ante las sociedades de gestión "
        "colectiva (SAYCO en Colombia; BMI/ASCAP u homólogas en otras jurisdicciones). Reparto de referencia, a "
        "formalizar siempre mediante un Split Sheet firmado antes de la entrega de los másters:",
    )
    add_table(
        doc,
        ["Titular", "Participación de referencia", "Justificación"],
        [
            [
                "IM Music (concepto + letra + financiación)",
                "60% – 70%",
                "Por aportar el 100% de la letra y el concepto creativo (la metodología de composición con "
                "neurociencia) y financiar íntegramente el desarrollo de la obra.",
            ],
            [
                "Productor musical externo (beat)",
                "30% – 40%",
                "Por la creación musical del instrumental original. [PORCENTAJE EXACTO — A NEGOCIAR POR PROYECTO, "
                "referencia de caso real: 70/30 o 60/40]",
            ],
        ],
    )

    style_heading(doc, "3. REPARTO DEL MÁSTER (FONOGRAMA): EL MECANISMO DE RECOUPMENT", 15)
    add_body(
        doc,
        "En la industria discográfica, quien financia la grabación, mezcla, máster y videoclip ostenta la titularidad "
        "del máster (fonograma) hasta recuperar su inversión. Esto se hace en DOS fases, y es importante entender la "
        "diferencia porque son mecánicas distintas, no un solo porcentaje fijo:",
    )
    add_bullet(
        doc,
        "Mientras no se haya recuperado el 100% del capital invertido (honorarios del productor, estudio, video, "
        "pauta de lanzamiento), IM Music recibe el 80% de las regalías netas del máster (Spotify, Apple Music, "
        "YouTube, etc.), y el artista recibe 20% desde el primer día — el artista no espera a que se recupere la "
        "inversión para empezar a cobrar, solo cobra una porción menor mientras tanto.",
        bold_lead="Fase 1 — Recoupment (recuperación de inversión). ",
    )
    add_bullet(
        doc,
        "Una vez IM Music recupera el 100% de lo invertido, el reparto cambia a un esquema estándar vitalicio: 65% "
        "IM Music (titular del máster) y 35% artista, negociable hasta 60/40 según el caso.",
        bold_lead="Fase 2 — Post-recoupment (esquema vitalicio). ",
    )
    add_body(
        doc,
        "[EL MOMENTO EXACTO EN QUE SE CONSIDERA “RECUPERADA” LA INVERSIÓN — bruto vs. neto de comisión de "
        "distribución — DEBE QUEDAR EXPLÍCITO EN CADA CONTRATO INDIVIDUAL, A DEFINIR CON ASESOR LEGAL, PARA EVITAR "
        "DISPUTAS SOBRE CUÁNDO EMPIEZA LA FASE 2.]",
        italic=True,
        size=10,
    )

    style_heading(doc, "4. SHOWS EN VIVO Y SINCRONIZACIÓN (SYNC)", 15)
    add_table(
        doc,
        ["Fuente de ingreso", "Reparto de referencia"],
        [
            ["Shows en vivo / giras", "100% artista — IM Music no participa de los ingresos de conciertos donde se interprete el tema."],
            ["Sincronización (cine, series, publicidad)", "Sigue el reparto del máster (65/35, fase post-recoupment) y del publishing (70/30 de referencia)."],
        ],
    )

    style_heading(doc, "5. SECUENCIA DE FORMALIZACIÓN", 15)
    add_bullet(doc, "Firma del contrato de inversión fonográfica (titularidad del máster) y del Split Sheet editorial con el productor externo, antes de entrar a estudio.", bold_lead="1. ")
    add_bullet(doc, "IM Music desembolsa los honorarios del productor y financia el rodaje del video oficial.", bold_lead="2. Producción. ")
    add_bullet(doc, "Distribución bajo el catálogo de IM Music (vía Nexus, 8% de comisión), con estrategia de lanzamiento coordinada con el artista.", bold_lead="3. Lanzamiento. ")

    doc.save(str(OUT_DIR / "Plantilla_Estructura_Inversion_Proyecto_Musical_IM_Music.docx"))
    print("OK:", OUT_DIR / "Plantilla_Estructura_Inversion_Proyecto_Musical_IM_Music.docx")


if __name__ == "__main__":
    build_metodologia()
    build_plantilla()
