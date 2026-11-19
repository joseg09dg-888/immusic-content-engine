# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

VIOLETA = RGBColor(0x5E, 0x17, 0xEB)
NEGRO = RGBColor(0x00, 0x00, 0x00)
GRIS_TEXTO = RGBColor(0x22, 0x22, 0x22)
GRIS_FOOTER = RGBColor(0x66, 0x66, 0x66)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)


def add(doc, text, font="Georgia", size=11, color=GRIS_TEXTO, bold=False, align=None, space_after=10, italic=False):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    r = p.add_run(text)
    r.font.name = font
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.bold = bold
    r.italic = italic
    p.paragraph_format.space_after = Pt(space_after)
    return p


def add_lyrics(doc, lines, space_after=14):
    for line in lines:
        p = doc.add_paragraph()
        r = p.add_run(line)
        r.font.name = "Georgia"
        r.font.size = Pt(11)
        r.font.color.rgb = NEGRO
        r.italic = True
        p.paragraph_format.space_after = Pt(2)
    doc.paragraphs[-1].paragraph_format.space_after = Pt(space_after)


def shade_cell(cell, hex_color):
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def set_cell_text(cell, text, bold=False, color=NEGRO, size=10, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    if align:
        p.alignment = align
    r = p.add_run(text)
    r.font.name = "Georgia"
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.bold = bold


def build():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Georgia"
    style.font.size = Pt(11)

    add(doc, "IM MUSIC", "Bahnschrift", 16, VIOLETA, True, WD_ALIGN_PARAGRAPH.CENTER, 2)
    add(doc, "PROPUESTA EJECUTIVA DE COPRODUCCIÓN E INVERSIÓN", "Bahnschrift", 20, NEGRO, True, WD_ALIGN_PARAGRAPH.CENTER, 2)
    add(doc, '"CAÑA BRAVA" — MOSCO', "Bahnschrift", 16, VIOLETA, True, WD_ALIGN_PARAGRAPH.CENTER, 6)
    add(doc,
        "Artista principal: Mosco (Caña Brava)  ·  Producción: CH The Producer  ·  Sello e inversionista: IM Music  ·  "
        "Duración calibrada: 02:30 min  ·  Medellín, Colombia",
        "Georgia", 10, GRIS_FOOTER, False, WD_ALIGN_PARAGRAPH.CENTER, 20)

    # 1. Carta de presentación
    add(doc, "1. POR QUÉ ESTA PROPUESTA", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc,
        "Mosco: esta es la propuesta formal de IM Music para coproducir, financiar e impulsar \"Caña Brava\" como tu próximo sencillo. "
        "No es solo una canción — es la aplicación completa de nuestra metodología de composición basada en neurociencia y psicología del "
        "comportamiento, pensada específicamente para tu voz, tu identidad y la jerga real de Medellín. IM Music asume el 100% del riesgo "
        "financiero del proyecto: producción, grabación, mezcla, máster, video oficial y campaña de lanzamiento. Tú aportas lo que nadie "
        "más puede aportar — tu interpretación, tu imagen y la autenticidad de Caña Brava.",
        space_after=16)

    # 2. Ingeniería de composición
    add(doc, "2. LA INGENIERÍA DETRÁS DE LA CANCIÓN", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc,
        "\"Caña Brava\" no se escribió a partir de la intuición únicamente. Se construyó con una arquitectura compositiva deliberada, basada en "
        "cómo el cerebro humano procesa, retiene y comparte un estímulo sonoro. Cada decisión de la letra responde a un principio específico:",
        space_after=10)

    tecnicas = [
        ("Eliminación de intro y \"open loop\" de expectativa (0:00–0:05)",
         "El cerebro decide en menos de 3 segundos si descarta una canción. Por eso no hay preámbulo instrumental: arrancamos directo con una "
         "brecha de curiosidad (\"si usted supiera qué vuelta pasa cuando cierro esta puerta...\") que obliga a quedarse para descubrir qué sigue."),
        ("Arquitectura de dopamina (anticipación y descarga)",
         "La dopamina alcanza su pico durante la anticipación, no solo en el clímax. Las rimas internas encadenadas y la cadencia percusiva "
         "mantienen el sistema nervioso en alerta creciente hasta liberar la tensión en el estribillo."),
        ("Efecto espejo e identificación cultural (jerga paisa real)",
         "Expresiones auténticas de Medellín (qué vuelta, parcero, cucha, visajes, niño, coronar, chicharrón, zornero, haragán) desactivan el "
         "filtro crítico del oyente. Al escuchar su propio lenguaje sin filtros, se activan las neuronas espejo: empatía inmediata e impulso de compartir."),
        ("Bucle fonológico (recordación en memoria de trabajo)",
         "Consonantes explosivas y repetición estratégica de imágenes sensoriales (\"el eco retumba en las paredes del pasillo / tengo el alma "
         "vuelta nada y el corazón en un cuchillo\") crean un circuito de reverberación auditiva que se queda sonando en la mente del oyente."),
        ("Efecto Zeigarnik y cierre incompleto (adicción y replay)",
         "El cerebro tolera mal las historias inconclusas. Al cortar el último verso antes de resolver la rima esperada, seguido de silencio seco, "
         "se genera tensión cognitiva que empuja al oyente a darle replay de inmediato."),
    ]
    for titulo, cuerpo in tecnicas:
        add(doc, titulo, "Georgia", 11, VIOLETA, True, None, 2)
        add(doc, cuerpo, "Georgia", 11, GRIS_TEXTO, False, None, 10)

    add(doc, "Arquitectura de retención para TikTok, Reels y Spotify", "Georgia", 11, VIOLETA, True, None, 4)
    add(doc,
        "La duración exacta de 2:30 está calibrada para los algoritmos actuales: hook de detención de scroll en los primeros 3 segundos, cero "
        "versos de relleno (cada par de barras sube la intensidad dramática), tres soundbites virales pre-diseñados de 15-20 segundos "
        "(Sección 1, Sección 3 y el clímax) listos para usarse como audio tendencia, y un bucle circular donde la última frase inconclusa "
        "conecta temática y rítmicamente con la apertura, favoreciendo la reproducción en bucle en Spotify y TikTok.",
        space_after=16)

    # 3. Mapa de estructura
    add(doc, "3. MAPA DE ESTRUCTURA Y TIEMPOS (02:30)", "Bahnschrift", 15, VIOLETA, True, None, 8)
    tabla_estructura = [
        ("Tiempo", "Sección", "Gatillo neuro-psicológico", "Dirección vocal en cabina"),
        ("0:00–0:30", "Sección 1: Ataque + Expectativa", "Open Loop y Pattern Interrupt. Abre brecha de curiosidad sin intro.",
         "Voz seca, cercana al micrófono, tono de advertencia cruda."),
        ("0:30–1:10", "Sección 2: Desarrollo e Inmersión", "Efecto espejo y carga dopaminérgica creciente mediante jerga real.",
         "Cadencia firme y pesada, marcando cada rima interna."),
        ("1:10–1:45", "Sección 3: Puente de Tensión", "Ruptura de monotonía; pico de adrenalina y soundbite viral.",
         "Aceleración del flow, proyección agresiva y urgencia."),
        ("1:45–2:30", "Sección 4: Clímax y Cierre Adictivo", "Descarga máxima y Efecto Zeigarnik (corte seco inconcluso).",
         "Explosión total; corte abrupto en la última palabra."),
    ]
    t = doc.add_table(rows=len(tabla_estructura), cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True
    for i, row in enumerate(tabla_estructura):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            set_cell_text(cell, val, bold=(i == 0), color=(BLANCO if i == 0 else NEGRO), size=9)
            if i == 0:
                shade_cell(cell, "5E17EB")
            elif i % 2 == 0:
                shade_cell(cell, "F2EDE5")
    add(doc, "", space_after=16)

    # 4. Letra completa
    add(doc, "4. LETRA COMPLETA CALIBRADA", "Bahnschrift", 15, VIOLETA, True, None, 4)
    add(doc, "Intérprete: Mosco (Caña Brava)  ·  Beat y producción: CH The Producer  ·  Referencia rítmica: cadencia implacable estilo "
              "\"The Way I Am\" (Eminem), adaptada al acento, fraseo y peso callejero de Medellín.",
        "Georgia", 10, GRIS_FOOTER, False, None, 10)

    add(doc, "[SECCIÓN 1 — EL ATAQUE DIRECTO + EXPECTATIVA · 0:00–0:30]", "Georgia", 10, VIOLETA, True, None, 4)
    add_lyrics(doc, [
        "Si usted supiera qué vuelta pasa cuando cierro esta puerta... (pausa breve)",
        "entendería por qué el alma ya ni aguanta ni despierta.",
        "El aire aquí adentro se pone bien denso,",
        "metido en esta película de la que no me dispenso.",
        "¿Por qué a mí, parcero? Es la pregunta que quema en el pecho,",
        "mientras veo cómo el techo se me cae encima del lecho.",
        "Una casa que es un infierno, un rancho que ya no abriga,",
        "donde el vicio y la mentira son la única fatiga.",
    ])

    add(doc, "[SECCIÓN 2 — RETENCIÓN Y DESARROLLO · 0:30–1:10]", "Georgia", 10, VIOLETA, True, None, 4)
    add_lyrics(doc, [
        "Mi cucha se ahoga en su mundo, no sabe ni qué decir,",
        "mientras todo se vuelve mierda y yo solo quiero abrirme de aquí.",
        "¿Dónde están los valores? ¿Dónde quedó la familia?",
        "Solo hay gritos, dolor, visajes y esta maldita vigilia.",
        "Un niño que creció a los golpes de la realidad,",
        "viendo cómo el amor se muere en medio de esta tempestad.",
        "Y el eco retumba en las paredes del pasillo,",
        "tengo el alma vuelta nada y el corazón en un cuchillo.",
    ])

    add(doc, "[SECCIÓN 3 — PUENTE DE MÁXIMA TENSIÓN / GIRO · 1:10–1:45]", "Georgia", 10, VIOLETA, True, None, 4)
    add_lyrics(doc, [
        "Un fantasma en la sala que mira sin ver,",
        "a su propia sangre cayendo en la red.",
        "Y yo aquí, queriendo coronar, queriendo volar,",
        "con las manos amarradas sin poderme escapar.",
        "Me dicen \"aguante, niño\", pero el alma se desgasta y se rompe,",
        "cada día es un chicharrón que me azota y me interrumpe.",
        "Hay mucho zornero y haragán que vive de pura apariencia,",
        "vendiendo la paz por veneno y ensuciando su conciencia,",
        "¡y yo atrapado en este fango sintiendo que ya no freno!",
    ])

    add(doc, "[SECCIÓN 4 — CLÍMAX Y CIERRE ADICTIVO EN LOOP · 1:45–2:30]", "Georgia", 10, VIOLETA, True, None, 4)
    add_lyrics(doc, [
        "Me duele el pecho, me quema la rabia por dentro,",
        "cansado de ser el que siempre le pone el pecho al encuentro",
        "con esta miseria que otros sembraron por mí...",
        "¡Joder, parcero, yo no pedí nacer pa' sufrir así!",
        "",
        "Y el eco rebota en las paredes del pasillo,",
        "tengo el alma vuelta nada y el corazón en un cuchillo.",
        "Siempre me toca cargar con esta cruz,",
        "y en esta maldita casa ya se apagó la luz.",
        "Oscuridad, puro peso en la espalda,",
        "mientras tanto zornero se esconde... y no ensucia su falda.",
        "Y grito al vacío, esperando que alguien me responda...",
        "pero detrás de esa puerta solo queda... (corte seco — silencio total)",
    ], space_after=18)

    # 5. Reparto de roles
    add(doc, "5. QUIÉN APORTA QUÉ", "Bahnschrift", 15, VIOLETA, True, None, 8)
    tabla_roles = [
        ("Parte", "Aporte financiero, creativo y operativo", "Rol en el proyecto"),
        ("IM Music\n(Sello / Inversionista)",
         "Autoría 100% de la letra (neurociencia + jerga paisa). Financiación total del beat, estudio, mezcla y máster (con CH The Producer). "
         "Financiación 100% del video musical oficial. Estrategia y pauta de lanzamiento viral en redes.",
         "Inversionista ejecutivo, compositor y sello titular del lanzamiento."),
        ("Mosco\n(Caña Brava)",
         "Interpretación vocal de la obra en estudio. Aporte de su imagen, identidad de Caña Brava, presencia escénica en el videoclip y "
         "difusión oficial.",
         "Intérprete principal e imagen del sencillo."),
        ("CH The Producer\n(Productor Musical)",
         "Creación instrumental del beat original. Ingeniería de mezcla y masterización con estándares profesionales de streaming.",
         "Productor musical aliado."),
    ]
    t2 = doc.add_table(rows=len(tabla_roles), cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(tabla_roles):
        for j, val in enumerate(row):
            cell = t2.cell(i, j)
            set_cell_text(cell, val, bold=(i == 0), color=(BLANCO if i == 0 else NEGRO), size=9)
            if i == 0:
                shade_cell(cell, "5E17EB")
            elif i % 2 == 0:
                shade_cell(cell, "F2EDE5")
    add(doc, "", space_after=16)

    # 6. Estructura de negociación
    add(doc, "6. ESTRUCTURA DE NEGOCIACIÓN: PUBLISHING Y MÁSTER", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc,
        "IM Music asume el 100% de la inversión económica (pago a CH The Producer por el beat, mezcla y máster, rodaje del video oficial y "
        "pauta de lanzamiento), además de aportar el concepto integral y la letra calibrada. Mosco participa aportando su interpretación "
        "vocal, imagen y el respaldo de Caña Brava, sin riesgo financiero para él. Sobre esa base se establece la siguiente distribución:",
        space_after=10)

    add(doc, "Publishing (derechos editoriales — 100% de la composición musical y lírica)", "Georgia", 11, VIOLETA, True, None, 4)
    tabla_publishing = [
        ("Titular", "Porcentaje", "Justificación"),
        ("IM Music / equipo compositor (autoría 100% de letra y concepto)", "60% – 70%",
         "Por aportar el 100% de la letra, el concepto creativo y financiar íntegramente el desarrollo de la obra."),
        ("CH The Producer (creación instrumental / beat)", "30% – 40%",
         "Por la creación musical del beat original (se recomienda 70/30 o 60/40 IM Music / CH The Producer)."),
    ]
    t3 = doc.add_table(rows=len(tabla_publishing), cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(tabla_publishing):
        for j, val in enumerate(row):
            cell = t3.cell(i, j)
            set_cell_text(cell, val, bold=(i == 0), color=(BLANCO if i == 0 else NEGRO), size=9)
            if i == 0:
                shade_cell(cell, "5E17EB")
            elif i % 2 == 0:
                shade_cell(cell, "F2EDE5")
    add(doc, "Formalizado mediante Split Sheet firmado antes de la entrega de masters. Registro editorial ante SAYCO.", "Georgia", 9, GRIS_FOOTER, False, None, 14)

    add(doc, "Máster (derechos fonográficos y explotación audiovisual — 100% del fonograma)", "Georgia", 11, VIOLETA, True, None, 4)
    tabla_master = [
        ("Fase / concepto", "Reparto del máster", "Condiciones"),
        ("Fase 1: Recuperación de inversión (recoupment de producción y video)", "80% IM Music / 20% Mosco",
         "IM Music recibe el 80% de las regalías netas del máster hasta recuperar el 100% del capital invertido en beat, estudio, video y "
         "pauta. Mosco recibe un 20% desde el día uno."),
        ("Fase 2: Regalías post-recuperación (esquema estándar vitalicio)", "65% IM Music / 35% Mosco (negociable hasta 60/40)",
         "Una vez recuperada la inversión inicial, las regalías netas del fonograma y la monetización del videoclip se dividen en esta proporción."),
        ("Shows en vivo y sincronizaciones", "100% Mosco (shows) · 65/35 máster y 70/30 publishing (sync TV/cine)",
         "Mosco conserva el 100% de los ingresos de sus conciertos y giras donde interprete el tema. En licencias para cine, series o "
         "publicidad, se respeta el reparto ya definido de máster y publishing."),
    ]
    t4 = doc.add_table(rows=len(tabla_master), cols=3)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(tabla_master):
        for j, val in enumerate(row):
            cell = t4.cell(i, j)
            set_cell_text(cell, val, bold=(i == 0), color=(BLANCO if i == 0 else NEGRO), size=9)
            if i == 0:
                shade_cell(cell, "5E17EB")
            elif i % 2 == 0:
                shade_cell(cell, "F2EDE5")
    add(doc, "", space_after=16)

    # 7. Protección de la metodología — the key IP clause
    add(doc, "7. SOBRE LA METODOLOGÍA DE COMPOSICIÓN", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc,
        "Hay una distinción importante que queremos dejar clara desde el inicio de esta alianza, en buenos términos: esta propuesta te "
        "entrega \"Caña Brava\" como canción terminada — la letra, la dirección vocal, el concepto y los derechos ya descritos arriba. "
        "Lo que no se transfiere ni se licencia es la arquitectura compositiva en sí misma: el método de neurociencia y psicología del "
        "comportamiento que usamos para construir la canción (eliminación de intro, apertura de bucles de expectativa, arquitectura de "
        "dopamina, efecto espejo, bucle fonológico, efecto Zeigarnik, y el sistema de calibración de tiempos que ves en la Sección 3).",
        space_after=10)
    add(doc,
        "Esa arquitectura es una metodología propietaria de IM Music, desarrollada y documentada internamente antes de este proyecto, y "
        "aplicada aquí como parte del servicio que te estamos prestando — no como conocimiento que se transfiere contigo al final de la "
        "colaboración. Está protegida como secreto empresarial bajo la Decisión 486 de 2000 de la Comunidad Andina (artículos 260 a 266), "
        "y el documento que la formaliza internamente tiene un registro con fecha cierta. Esto significa, en términos prácticos, que "
        "\"Caña Brava\" es tuya para interpretar, promocionar y vivir de ella según los porcentajes ya acordados — pero el método en sí "
        "no queda habilitado para que lo repliques, lo enseñes o lo compartas con otro productor o sello sin autorización de IM Music.",
        space_after=10)
    add(doc,
        "No lo mencionamos como advertencia, sino porque creemos en ser transparentes desde el primer documento: así como tú proteges tu "
        "imagen y tu nombre como Caña Brava, nosotros protegemos el método que hace que esta canción esté diseñada para pegar. Es una "
        "condición estándar en cualquier alianza de este tipo, y no te quita nada de lo que ya es tuyo por derecho en este proyecto.",
        space_after=18)

    # 8. Cierre
    add(doc, "8. CIERRE Y PRÓXIMO PASO", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc,
        "Estamos listos para reunirnos contigo y con CH The Producer, presentar el presupuesto de producción, firmar el acuerdo ejecutivo "
        "(incluye Split Sheet editorial y contrato de inversión fonográfica) y arrancar la grabación y el rodaje de este sencillo.",
        space_after=20)

    add(doc, "IM Music · Medellín, Colombia", "Georgia", 9, GRIS_FOOTER, False, WD_ALIGN_PARAGRAPH.CENTER, 0)

    out_docx = "docs/sello_plan/legal_referencia/propuesta_mosco_cana_brava_FINAL.docx"
    doc.save(out_docx)
    print("Guardado:", out_docx)


if __name__ == "__main__":
    build()
