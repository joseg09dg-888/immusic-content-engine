# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

VIOLETA = colors.HexColor("#5E17EB")
NEGRO = colors.HexColor("#000000")
GRIS = colors.HexColor("#222222")
GRISFOOT = colors.HexColor("#666666")
CREMA = colors.HexColor("#F2EDE5")
BLANCO = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("Brand", fontName="Helvetica-Bold", fontSize=15, textColor=VIOLETA, alignment=TA_CENTER, spaceAfter=3))
styles.add(ParagraphStyle("PropTitle", fontName="Helvetica-Bold", fontSize=19, textColor=NEGRO, alignment=TA_CENTER, spaceAfter=3))
styles.add(ParagraphStyle("Subtitle", fontName="Helvetica-Bold", fontSize=15, textColor=VIOLETA, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle("Meta", fontName="Times-Roman", fontSize=9.5, textColor=GRISFOOT, alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=13.5, textColor=VIOLETA, alignment=TA_LEFT, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle("H3", fontName="Times-Bold", fontSize=10.5, textColor=VIOLETA, alignment=TA_LEFT, spaceBefore=6, spaceAfter=3))
styles.add(ParagraphStyle("Body", fontName="Times-Roman", fontSize=10.3, textColor=GRIS, alignment=TA_LEFT, spaceAfter=8, leading=14))
styles.add(ParagraphStyle("Lyric", fontName="Times-Italic", fontSize=10.3, textColor=NEGRO, alignment=TA_LEFT, spaceAfter=2, leading=13))
styles.add(ParagraphStyle("LyricHead", fontName="Times-Bold", fontSize=9.5, textColor=VIOLETA, alignment=TA_LEFT, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle("FooterNote", fontName="Times-Roman", fontSize=8.5, textColor=GRISFOOT, alignment=TA_LEFT, spaceAfter=12))
styles.add(ParagraphStyle("Final", fontName="Times-Roman", fontSize=9, textColor=GRISFOOT, alignment=TA_CENTER, spaceBefore=16))

CELL = ParagraphStyle("Cell", fontName="Times-Roman", fontSize=8.3, textColor=NEGRO, leading=10.5)
CELLH = ParagraphStyle("CellH", fontName="Helvetica-Bold", fontSize=8.3, textColor=BLANCO, leading=10.5)


def P(text, style="Body"):
    return Paragraph(text, styles[style])


def table_block(rows, col_widths, header=True):
    data = []
    for i, row in enumerate(rows):
        st = CELLH if (i == 0 and header) else CELL
        data.append([Paragraph(c, st) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style_cmds = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        style_cmds.append(("BACKGROUND", (0, 0), (-1, 0), VIOLETA))
    for i in range(1 if header else 0, len(rows)):
        if (i - (1 if header else 0)) % 2 == 1:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), CREMA))
    t.setStyle(TableStyle(style_cmds))
    return t


def build():
    out_pdf = "docs/sello_plan/legal_referencia/propuesta_mosco_cana_brava_FINAL.pdf"
    doc = SimpleDocTemplate(out_pdf, pagesize=LETTER,
                             leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                             topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    el = []

    el.append(P("IM MUSIC", "Brand"))
    el.append(P("PROPUESTA EJECUTIVA DE COPRODUCCIÓN E INVERSIÓN", "PropTitle"))
    el.append(P('"CAÑA BRAVA" — MOSCO', "Subtitle"))
    el.append(P("Artista principal: Mosco (Caña Brava) &middot; Producción: CH The Producer &middot; Sello e inversionista: IM Music "
                "&middot; Duración calibrada: 02:30 min &middot; Medellín, Colombia", "Meta"))
    el.append(HRFlowable(width="100%", thickness=1.2, color=VIOLETA, spaceAfter=10))

    el.append(P("1. POR QUÉ ESTA PROPUESTA", "H2"))
    el.append(P('Mosco: esta es la propuesta formal de IM Music para coproducir, financiar e impulsar "Caña Brava" como tu próximo '
                "sencillo. No es solo una canción — es la aplicación completa de nuestra metodología de composición basada en "
                "neurociencia y psicología del comportamiento, pensada específicamente para tu voz, tu identidad y la jerga real de "
                "Medellín. IM Music asume el 100% del riesgo financiero del proyecto: producción, grabación, mezcla, máster, video "
                "oficial y campaña de lanzamiento. Tú aportas lo que nadie más puede aportar — tu interpretación, tu imagen y la "
                "autenticidad de Caña Brava.", "Body"))

    el.append(P("2. LA INGENIERÍA DETRÁS DE LA CANCIÓN", "H2"))
    el.append(P('"Caña Brava" no se escribió a partir de la intuición únicamente. Se construyó con una arquitectura compositiva '
                "deliberada, basada en cómo el cerebro humano procesa, retiene y comparte un estímulo sonoro. Cada decisión de la letra "
                "responde a un principio específico:", "Body"))

    tecnicas = [
        ("Eliminación de intro y &quot;open loop&quot; de expectativa (0:00&ndash;0:05)",
         "El cerebro decide en menos de 3 segundos si descarta una canción. Por eso no hay preámbulo instrumental: arrancamos directo "
         'con una brecha de curiosidad ("si usted supiera qué vuelta pasa cuando cierro esta puerta...") que obliga a quedarse para '
         "descubrir qué sigue."),
        ("Arquitectura de dopamina (anticipación y descarga)",
         "La dopamina alcanza su pico durante la anticipación, no solo en el clímax. Las rimas internas encadenadas y la cadencia "
         "percusiva mantienen el sistema nervioso en alerta creciente hasta liberar la tensión en el estribillo."),
        ("Efecto espejo e identificación cultural (jerga paisa real)",
         "Expresiones auténticas de Medellín (qué vuelta, parcero, cucha, visajes, niño, coronar, chicharrón, zornero, haragán) "
         "desactivan el filtro crítico del oyente. Al escuchar su propio lenguaje sin filtros, se activan las neuronas espejo: "
         "empatía inmediata e impulso de compartir."),
        ("Bucle fonológico (recordación en memoria de trabajo)",
         "Consonantes explosivas y repetición estratégica de imágenes sensoriales (&quot;el eco retumba en las paredes del pasillo / "
         "tengo el alma vuelta nada y el corazón en un cuchillo&quot;) crean un circuito de reverberación auditiva que se queda "
         "sonando en la mente del oyente."),
        ("Efecto Zeigarnik y cierre incompleto (adicción y replay)",
         "El cerebro tolera mal las historias inconclusas. Al cortar el último verso antes de resolver la rima esperada, seguido de "
         "silencio seco, se genera tensión cognitiva que empuja al oyente a darle replay de inmediato."),
    ]
    for titulo, cuerpo in tecnicas:
        el.append(P(titulo, "H3"))
        el.append(P(cuerpo, "Body"))

    el.append(P("Arquitectura de retención para TikTok, Reels y Spotify", "H3"))
    el.append(P("La duración exacta de 2:30 está calibrada para los algoritmos actuales: hook de detención de scroll en los primeros "
                "3 segundos, cero versos de relleno (cada par de barras sube la intensidad dramática), tres soundbites virales "
                "pre-diseñados de 15-20 segundos (Sección 1, Sección 3 y el clímax) listos para usarse como audio tendencia, y un "
                "bucle circular donde la última frase inconclusa conecta temática y rítmicamente con la apertura, favoreciendo la "
                "reproducción en bucle en Spotify y TikTok.", "Body"))

    el.append(P("3. MAPA DE ESTRUCTURA Y TIEMPOS (02:30)", "H2"))
    rows_estructura = [
        ["Tiempo", "Sección", "Gatillo neuro-psicológico", "Dirección vocal en cabina"],
        ["0:00&ndash;0:30", "Sección 1: Ataque + Expectativa", "Open Loop y Pattern Interrupt. Abre brecha de curiosidad sin intro.",
         "Voz seca, cercana al micrófono, tono de advertencia cruda."],
        ["0:30&ndash;1:10", "Sección 2: Desarrollo e Inmersión", "Efecto espejo y carga dopaminérgica creciente mediante jerga real.",
         "Cadencia firme y pesada, marcando cada rima interna."],
        ["1:10&ndash;1:45", "Sección 3: Puente de Tensión", "Ruptura de monotonía; pico de adrenalina y soundbite viral.",
         "Aceleración del flow, proyección agresiva y urgencia."],
        ["1:45&ndash;2:30", "Sección 4: Clímax y Cierre Adictivo", "Descarga máxima y Efecto Zeigarnik (corte seco inconcluso).",
         "Explosión total; corte abrupto en la última palabra."],
    ]
    el.append(table_block(rows_estructura, [0.7 * inch, 1.55 * inch, 2.3 * inch, 1.85 * inch]))
    el.append(Spacer(1, 14))

    el.append(P("4. LETRA COMPLETA CALIBRADA", "H2"))
    el.append(P("Intérprete: Mosco (Caña Brava) &middot; Beat y producción: CH The Producer &middot; Referencia rítmica: cadencia "
                'implacable estilo "The Way I Am" (Eminem), adaptada al acento, fraseo y peso callejero de Medellín.', "FooterNote"))

    secciones_letra = [
        ("[SECCIÓN 1 &mdash; EL ATAQUE DIRECTO + EXPECTATIVA &middot; 0:00&ndash;0:30]", [
            "Si usted supiera qué vuelta pasa cuando cierro esta puerta... (pausa breve)",
            "entendería por qué el alma ya ni aguanta ni despierta.",
            "El aire aquí adentro se pone bien denso,",
            "metido en esta película de la que no me dispenso.",
            "¿Por qué a mí, parcero? Es la pregunta que quema en el pecho,",
            "mientras veo cómo el techo se me cae encima del lecho.",
            "Una casa que es un infierno, un rancho que ya no abriga,",
            "donde el vicio y la mentira son la única fatiga.",
        ]),
        ("[SECCIÓN 2 &mdash; RETENCIÓN Y DESARROLLO &middot; 0:30&ndash;1:10]", [
            "Mi cucha se ahoga en su mundo, no sabe ni qué decir,",
            "mientras todo se vuelve mierda y yo solo quiero abrirme de aquí.",
            "¿Dónde están los valores? ¿Dónde quedó la familia?",
            "Solo hay gritos, dolor, visajes y esta maldita vigilia.",
            "Un niño que creció a los golpes de la realidad,",
            "viendo cómo el amor se muere en medio de esta tempestad.",
            "Y el eco retumba en las paredes del pasillo,",
            "tengo el alma vuelta nada y el corazón en un cuchillo.",
        ]),
        ("[SECCIÓN 3 &mdash; PUENTE DE MÁXIMA TENSIÓN / GIRO &middot; 1:10&ndash;1:45]", [
            "Un fantasma en la sala que mira sin ver,",
            "a su propia sangre cayendo en la red.",
            "Y yo aquí, queriendo coronar, queriendo volar,",
            "con las manos amarradas sin poderme escapar.",
            "Me dicen &quot;aguante, niño&quot;, pero el alma se desgasta y se rompe,",
            "cada día es un chicharrón que me azota y me interrumpe.",
            "Hay mucho zornero y haragán que vive de pura apariencia,",
            "vendiendo la paz por veneno y ensuciando su conciencia,",
            "¡y yo atrapado en este fango sintiendo que ya no freno!",
        ]),
        ("[SECCIÓN 4 &mdash; CLÍMAX Y CIERRE ADICTIVO EN LOOP &middot; 1:45&ndash;2:30]", [
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
            "pero detrás de esa puerta solo queda... (corte seco &mdash; silencio total)",
        ]),
    ]
    for head, lines in secciones_letra:
        el.append(P(head, "LyricHead"))
        for line in lines:
            el.append(P(line if line else "&nbsp;", "Lyric"))
        el.append(Spacer(1, 6))

    el.append(P("5. QUIÉN APORTA QUÉ", "H2"))
    rows_roles = [
        ["Parte", "Aporte financiero, creativo y operativo", "Rol en el proyecto"],
        ["IM Music<br/>(Sello / Inversionista)",
         "Autoría 100% de la letra (neurociencia + jerga paisa). Financiación total del beat, estudio, mezcla y máster (con CH The "
         "Producer). Financiación 100% del video musical oficial. Estrategia y pauta de lanzamiento viral en redes.",
         "Inversionista ejecutivo, compositor y sello titular del lanzamiento."],
        ["Mosco<br/>(Caña Brava)",
         "Interpretación vocal de la obra en estudio. Aporte de su imagen, identidad de Caña Brava, presencia escénica en el "
         "videoclip y difusión oficial.",
         "Intérprete principal e imagen del sencillo."],
        ["CH The Producer<br/>(Productor Musical)",
         "Creación instrumental del beat original. Ingeniería de mezcla y masterización con estándares profesionales de streaming.",
         "Productor musical aliado."],
    ]
    el.append(table_block(rows_roles, [1.3 * inch, 3.6 * inch, 1.5 * inch]))
    el.append(Spacer(1, 14))

    el.append(P("6. ESTRUCTURA DE NEGOCIACIÓN: PUBLISHING Y MÁSTER", "H2"))
    el.append(P("IM Music asume el 100% de la inversión económica (pago a CH The Producer por el beat, mezcla y máster, rodaje del "
                "video oficial y pauta de lanzamiento), además de aportar el concepto integral y la letra calibrada. Mosco participa "
                "aportando su interpretación vocal, imagen y el respaldo de Caña Brava, sin riesgo financiero para él. Sobre esa base "
                "se establece la siguiente distribución:", "Body"))

    el.append(P("Publishing (derechos editoriales &mdash; 100% de la composición musical y lírica)", "H3"))
    rows_pub = [
        ["Titular", "Porcentaje", "Justificación"],
        ["IM Music / equipo compositor (autoría 100% de letra y concepto)", "60% &ndash; 70%",
         "Por aportar el 100% de la letra, el concepto creativo y financiar íntegramente el desarrollo de la obra."],
        ["CH The Producer (creación instrumental / beat)", "30% &ndash; 40%",
         "Por la creación musical del beat original (se recomienda 70/30 o 60/40 IM Music / CH The Producer)."],
    ]
    el.append(table_block(rows_pub, [2.6 * inch, 1.0 * inch, 2.8 * inch]))
    el.append(P("Formalizado mediante Split Sheet firmado antes de la entrega de masters. Registro editorial ante SAYCO.", "FooterNote"))

    el.append(P("Máster (derechos fonográficos y explotación audiovisual &mdash; 100% del fonograma)", "H3"))
    rows_master = [
        ["Fase / concepto", "Reparto del máster", "Condiciones"],
        ["Fase 1: Recuperación de inversión (recoupment de producción y video)", "80% IM Music / 20% Mosco",
         "IM Music recibe el 80% de las regalías netas del máster hasta recuperar el 100% del capital invertido en beat, estudio, "
         "video y pauta. Mosco recibe un 20% desde el día uno."],
        ["Fase 2: Regalías post-recuperación (esquema estándar vitalicio)", "65% IM Music / 35% Mosco (negociable hasta 60/40)",
         "Una vez recuperada la inversión inicial, las regalías netas del fonograma y la monetización del videoclip se dividen en "
         "esta proporción."],
        ["Shows en vivo y sincronizaciones", "100% Mosco (shows) &middot; 65/35 máster y 70/30 publishing (sync TV/cine)",
         "Mosco conserva el 100% de los ingresos de sus conciertos y giras donde interprete el tema. En licencias para cine, series "
         "o publicidad, se respeta el reparto ya definido de máster y publishing."],
    ]
    el.append(table_block(rows_master, [2.2 * inch, 1.6 * inch, 2.6 * inch]))
    el.append(Spacer(1, 14))

    el.append(P("7. SOBRE LA METODOLOGÍA DE COMPOSICIÓN", "H2"))
    el.append(P("Hay una distinción importante que queremos dejar clara desde el inicio de esta alianza, en buenos términos: esta "
                'propuesta te entrega "Caña Brava" como canción terminada &mdash; la letra, la dirección vocal, el concepto y los '
                "derechos ya descritos arriba. Lo que no se transfiere ni se licencia es la arquitectura compositiva en sí misma: el "
                "método de neurociencia y psicología del comportamiento que usamos para construir la canción (eliminación de intro, "
                "apertura de bucles de expectativa, arquitectura de dopamina, efecto espejo, bucle fonológico, efecto Zeigarnik, y el "
                "sistema de calibración de tiempos que ves en la Sección 3).", "Body"))
    el.append(P("Esa arquitectura es una metodología propietaria de IM Music, desarrollada y documentada internamente antes de este "
                "proyecto, y aplicada aquí como parte del servicio que te estamos prestando &mdash; no como conocimiento que se "
                "transfiere contigo al final de la colaboración. Está protegida como secreto empresarial bajo la Decisión 486 de 2000 "
                "de la Comunidad Andina (artículos 260 a 266), y el documento que la formaliza internamente tiene un registro con "
                'fecha cierta. Esto significa, en términos prácticos, que "Caña Brava" es tuya para interpretar, promocionar y vivir '
                "de ella según los porcentajes ya acordados &mdash; pero el método en sí no queda habilitado para que lo repliques, lo "
                "enseñes o lo compartas con otro productor o sello sin autorización de IM Music.", "Body"))
    el.append(P("No lo mencionamos como advertencia, sino porque creemos en ser transparentes desde el primer documento: así como tú "
                "proteges tu imagen y tu nombre como Caña Brava, nosotros protegemos el método que hace que esta canción esté "
                "diseñada para pegar. Es una condición estándar en cualquier alianza de este tipo, y no te quita nada de lo que ya es "
                "tuyo por derecho en este proyecto.", "Body"))

    el.append(P("8. CIERRE Y PRÓXIMO PASO", "H2"))
    el.append(P("Estamos listos para reunirnos contigo y con CH The Producer, presentar el presupuesto de producción, firmar el "
                "acuerdo ejecutivo (incluye Split Sheet editorial y contrato de inversión fonográfica) y arrancar la grabación y el "
                "rodaje de este sencillo.", "Body"))

    el.append(Spacer(1, 10))
    el.append(P("IM Music &middot; Medellín, Colombia", "Final"))

    doc.build(el)
    print("Guardado:", out_pdf)


if __name__ == "__main__":
    build()
