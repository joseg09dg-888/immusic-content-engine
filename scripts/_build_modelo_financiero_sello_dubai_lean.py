"""Modelo financiero IM Music - Sello, escenario Dubai LEAN/POR FASES.
Alternativa al modelo Dubai completo (modelo_financiero_sello.xlsx): el fundador
SI se radica en Dubai y SI monta estudio+oficina, pero por fases, escalando
solo cuando los ingresos/flujo de caja validen la inversion adicional.
No modifica el modelo completo -- es un documento aparte para comparar.

v4: el servicio 360 de marca tiene un PRECIO REAL ya definido en la plataforma
-- plan "ELITE 360" a USD $2,999.99/mes por artista (PM dedicado, manager
musical, videos musicales, branding, Meta Ads, campamentos musicales, red de
industria). Roster con tope duro (12 en este escenario Dubai) y tasa de
ocupacion estimada (no 100% de los cupos facturan el full fee todo el tiempo).
"Ingreso de catalogo" y "regalias de proyectos especiales" son LA MISMA linea:
retorno via Nexus (8% comision) de canciones/EPs/albumes que el sello financio
con capital propio, con % de regalia negociado caso por caso -- no recurrente
garantizado, no es un ingreso automatico por artista del roster.
Mas: YouTube propio, ingreso ya validado del libro, costo legal casi a cero.
"""
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "sello_plan" / "modelo_financiero_sello_dubai_lean.xlsx"

VIOLETA = "5E17EB"
FILL_HEAD = PatternFill("solid", fgColor=VIOLETA)
FONT_HEAD = Font(color="FFFFFF", bold=True)
FONT_TITLE = Font(color=VIOLETA, bold=True, size=14)
FONT_BOLD = Font(bold=True)
FONT_FLAG = Font(color="B00000", italic=True)

# Resultados del modelo Dubai COMPLETO (modelo_financiero_sello.xlsx) para la
# pestana comparativa, tal como se conocian al momento de construir este
# documento -- si ese modelo fue corregido en paralelo con el mismo precio
# ELITE 360, estas cifras de referencia pueden haber cambiado.
COMPLETO = {
    "nti": 318_259,
    "ebitda_anio": [-327_892, None, None, None, -247_663],
    "van": -1_133_096,
    "tir": None,
}

FX_USD_AED = 3.6725

DXB_LEAN = {
    "moneda": "AED",
    "fx_nota": f"1 USD ~ {FX_USD_AED} AED (paridad oficial). Cifras de CAPEX/estudio/arriendo heredadas del modelo Dubai completo via conversion de Colombia -- MARCADORES, no cotizaciones locales, salvo donde se indique 'CONFIRMADO'. El precio del servicio 360 (ver abajo) SI es un dato real de la plataforma, no una conversion.",
    "tasa_descuento": 0.25,
    "umbral_exento": 375_000,
    "tasa_impuesto": 0.09,
    "nexus_comision": 0.08,

    "capex": [
        ("Estudio modesto (home/project studio: mics basicos + interfaz + monitores + tratamiento acustico de 1 cuarto)", 22_953,
         "NO CONFIRMADO: reduccion deliberada de 50% vs. el estudio del modelo completo (AED 45,906) -- setup minimo para empezar a grabar/mezclar, no un estudio profesional completo. Cotizar localmente antes de usar."),
        ("Kit audiovisual minimo (camara basica + 1 luz + mic lapel, sin kit de cine)", 8_089,
         "NO CONFIRMADO: reduccion de 50% vs. el kit del modelo completo (AED 16,177) -- el Content Engine ya cubre grafica/edicion, solo se necesita lo minimo para filmar en vivo."),
        ("Equipo (1 laptop, sin mobiliario de oficina dedicado)", 4_591,
         "NO CONFIRMADO: reduccion de 50% vs. el equipo del modelo completo (AED 9,181) -- un solo equipo, sin oficina fisica que amueblar en Ano 1."),
        ("Arancel de importacion 5% CIF sobre equipo importado", 1_782,
         "CONFIRMADO: tasa general EAU de 5% sobre CIF (u.ae). Base = suma de las 3 lineas anteriores x 5%."),
        ("Licencia zona franca (IFZA, paquete mas economico)", 12_900,
         "Igual al modelo completo -- la licencia es necesaria para operar legalmente sin importar la escala. Estimacion de consultora, no tarifa oficial de gobierno."),
        ("Visa de inversionista (fundador) -- SIN visa de empleado en Ano 1", 13_500,
         "NO CONFIRMADO: punto medio del rango AED 7,000-20,000+ de fuentes de baja confiabilidad. Se omite la visa de empleado del modelo completo porque no hay contratacion local en Ano 1."),
    ],
    "imprevistos_pct": 0.15,
    "capital_trabajo_meses": 6,

    "opex_mensual_lean": [
        ("CEO / Director del Sello (fundador radicado en Dubai)", 12_000, "Igual al modelo completo -- es el costo fijo que SI se mantiene porque el fundador vive y opera alla."),
        ("Asesoria legal (reducida casi a cero -- el fundador cubre la funcion legal directamente)", 200,
         "Instruccion explicita del coordinador: eliminar/reducir a casi cero el costo de abogado externo. Se deja un minimo residual para notariado/tramites puntuales que el fundador no puede hacer el mismo."),
        ("Contador (retainer externo, reducido)", 1_000, "NO CONFIRMADO: reducido vs. AED 1,200 del modelo completo."),
        ("Espacio de trabajo compartido / coworking (en lugar de oficina dedicada)", 800, "NO CONFIRMADO: estimacion propia de un escritorio de coworking en Dubai; reemplaza el arriendo de AED 3,575/mes del modelo completo."),
        ("Herramientas tecnologicas", 400, "Igual al modelo completo, redondeado."),
        ("Marketing y promocion (bootstrap)", 1_000, "NO CONFIRMADO: reducido vs. AED 2,000 del modelo completo -- presupuesto minimo de arranque."),
        ("Administrativos y generales", 500, "NO CONFIRMADO: reducido vs. AED 800 del modelo completo."),
    ],
    "opex_mensual_escalado_extra": [
        ("Gerente Comercial / Social Media Manager (primera contratacion local)", 5_750, "CONFIRMADO como rango de mercado (GulfTalent/Payscale, AED 5,500-6,000) para el rol mas cercano -- se activa solo si se cumple el gatillo de escalamiento."),
        ("Upgrade de arriendo a oficina/estudio dedicado pequeno (~150 sqft)", 2_775, "Diferencial vs. el coworking lean (AED 3,575 oficina dedicada - AED 800 coworking); tarifa por sqft CONFIRMADA (Nikoliers 2024), tamano supuesto."),
    ],
    "opex_crecimiento_anual": 0.06,
    "gatillo_ingresos_anuales": 150_000,
    "gatillo_nota": "Gatillo de escalamiento: se activa la primera contratacion local + upgrade de oficina a partir del primer Ano en que los ingresos anuales superen AED 150,000 Y el EBITDA de ese mismo ano sea >= 0. Si nunca se cumple en el horizonte de 5 anos, el modelo se queda lean todo el periodo.",

    # --- ROSTER: tope duro, curva de ocupacion gradual (no 12 desde el mes 1) ---
    "roster_tope": 12,
    "roster_fin_de_anio": [1, 3, 6, 9, 12],
    "roster_nota": "Tope duro de 12 artistas firmados en Dubai (extremo bajo del rango 12-15 instruido, por ser mercado sin validar). Curva de ocupacion gradual 0->1->3->6->9->12 en 5 anos, NO 12 desde el mes 1.",
    "tasa_ocupacion_roster": 0.85,
    "tasa_ocupacion_nota": "ESTIMACION: no todos los cupos firmados facturan el fee completo todos los meses (onboarding, pausas, renegociaciones) -- se asume 85% de ocupacion efectiva sobre el promedio de artistas activos. Sin dato real de retencion/ocupacion de un roster propio todavia.",

    "servicio_360_nota": (
        "Precio REAL ya definido en la plataforma (no una estimacion): plan 'ELITE 360' a USD $2,999.99/mes "
        "por artista -- incluye Project Manager dedicado, manager musical, videos musicales, branding, gestion "
        "de Meta Ads, campamentos musicales y red de industria. Convertido a AED a la tasa de referencia. "
        "El '360' es el ALCANCE DEL SERVICIO (marketing y marca), NO un reparto de ingresos de streaming/shows/"
        "merch/patrocinios del artista. NO ESTA CLARO si el presupuesto de pauta de Meta Ads esta incluido en "
        "este fee o se factura aparte -- este modelo ASUME que esta incluido como servicio de gestion (no como "
        "presupuesto de pauta pasado 1:1), lo cual implica un costo de entrega significativo, modelado abajo."
    ),
    "fee_360_usd_mensual": 2_999.99,
    "cogs_360_pct_nota": (
        "RIESGO OPERATIVO A VALIDAR: el servicio ELITE 360 (PM dedicado, videos musicales, campamentos) es de "
        "alto contacto y normalmente requeriria mas que 1 persona (el fundador) para entregarlo a varios "
        "artistas en simultaneo. Este modelo lean asume que el Content Engine + freelancers por proyecto (ya "
        "contemplados en 'Produccion a terceros') cubren parte de la entrega, pero sigue siendo una tension "
        "real entre el modelo 'lean sin contrataciones' y la promesa de un plan premium de alto contacto -- "
        "debe validarse operativamente, no solo financieramente, antes de vender este plan a escala."
    ),
    "cogs_360_pct": 0.40,

    "produccion": {
        "precio_unit": 3_500, "cvu": 1_750,
        "vol_mensual_por_anio": [1, 1.5, 2, 2.5, 3],
        "nota": "Servicio de produccion musical (cubre clientes externos y produccion puntual para el roster cuando aplica, fuera del scope del plan ELITE 360) -- identico al modelo Dubai completo.",
    },

    "youtube_mensual_por_anio": [500, 800, 1_200, 1_800, 2_500],
    "youtube_nota": "NO CONFIRMADO: ingreso de AdSense/Content ID del canal propio de YouTube, sin datos reales de vistas/suscriptores del canal -- supuesto conservador de arranque a validar con YouTube Analytics real.",

    "libro_copias_mes_anio1": 10,
    "libro_crecimiento_anual": 0.20,
    "libro_margen_usd": 8.0,
    "libro_nota": "INGRESO YA VALIDADO (no es un supuesto de mercado): el libro 'Music Business Para Todos Los Humanos' ya esta en venta real en Hotmart en ES/EN/PT a USD $16.90. Lo que SI es supuesto es el VOLUMEN de copias/mes (10/mes Ano 1, sin dato de ventas real reportado) y el margen neto promedio por copia (USD $8) -- la existencia del producto y su precio son reales, el volumen de ventas no.",

    "regalias_catalogo_por_anio": [3_000, 5_000, 8_000, 12_000, 18_000],
    "regalias_catalogo_nota": (
        "Regalias de catalogo = retorno (via Nexus, 8% de comision) de las canciones/EPs/albumes en los que "
        "el sello invirtio CAPITAL PROPIO para financiar su produccion, con % de regalia negociado CASO POR "
        "CASO con cada artista/proyecto -- esta es LA MISMA linea que 'regalias de proyectos especiales', no "
        "dos lineas distintas. NO es un ingreso automatico por artista del roster (eso ya se elimino de este "
        "modelo) ni es recurrente garantizado -- depende de que el sello decida financiar proyectos especificos "
        "y de que esos proyectos generen streams reales. Montos NO CONFIRMADOS, estimacion propia conservadora "
        "y creciente, sin pipeline de proyectos especiales confirmado todavia."
    ),

    "depreciacion_anios": 5,
}


def compute(p):
    n = 5
    capex_subtotal = sum(x[1] for x in p["capex"])
    imprevistos = capex_subtotal * p["imprevistos_pct"]
    capex_total = capex_subtotal + imprevistos
    opex_mes1 = sum(x[1] for x in p["opex_mensual_lean"])
    capital_trabajo = opex_mes1 * p["capital_trabajo_meses"]
    nti = capex_total + capital_trabajo

    # --- Produccion (externos + roster puntual) ---
    ing_prod, cog_prod = [], []
    for vol in p["produccion"]["vol_mensual_por_anio"]:
        ing_prod.append(vol * p["produccion"]["precio_unit"] * 12)
        cog_prod.append(vol * p["produccion"]["cvu"] * 12)

    # --- Roster: servicio ELITE 360 (precio real), con tasa de ocupacion ---
    fin = p["roster_fin_de_anio"]
    inicio = [0] + fin[:-1]
    promedio_artistas = [(inicio[i] + fin[i]) / 2 for i in range(n)]
    ocupacion = p["tasa_ocupacion_roster"]
    artistas_pagantes = [art * ocupacion for art in promedio_artistas]

    fee_360_anual_aed = p["fee_360_usd_mensual"] * FX_USD_AED * 12
    ing_roster_360 = [art * fee_360_anual_aed for art in artistas_pagantes]
    cog_roster_360 = [ing * p["cogs_360_pct"] for ing in ing_roster_360]

    # --- YouTube propio ---
    ing_youtube = [v * 12 for v in p["youtube_mensual_por_anio"]]

    # --- Libro (ya validado, volumen supuesto) ---
    copias_mes = p["libro_copias_mes_anio1"]
    ing_libro = []
    for i in range(n):
        ing_anio = copias_mes * 12 * p["libro_margen_usd"] * FX_USD_AED
        ing_libro.append(ing_anio)
        copias_mes *= (1 + p["libro_crecimiento_anual"])

    # --- Regalias de catalogo / proyectos especiales (unica linea, ya neta) ---
    reg_catalogo = p["regalias_catalogo_por_anio"]

    depre_anual = capex_total / p["depreciacion_anios"]
    tasa_imp = p["tasa_impuesto"]
    umbral = p["umbral_exento"]
    extra_mensual = sum(x[1] for x in p["opex_mensual_escalado_extra"])

    filas = []
    fc = [-nti]
    opex_anual_base = opex_mes1 * 12
    escalado_activo = False
    anio_activacion = None
    opex_anual_prev = opex_anual_base
    for i in range(n):
        ingresos = ing_prod[i] + ing_roster_360[i] + ing_youtube[i] + ing_libro[i] + reg_catalogo[i]
        cogs = cog_prod[i] + cog_roster_360[i]
        ub = ingresos - cogs

        if i == 0:
            opex = opex_anual_base
        else:
            opex = opex_anual_prev * (1 + p["opex_crecimiento_anual"])
            if escalado_activo:
                opex += extra_mensual * 12

        ebitda_preliminar = ub - opex
        if not escalado_activo and ingresos > p["gatillo_ingresos_anuales"] and ebitda_preliminar >= 0:
            escalado_activo = True
            anio_activacion = i + 2

        ebitda = ebitda_preliminar
        opex_anual_prev = opex if i > 0 else opex_anual_base

        uai = ebitda - depre_anual
        base_gravable = max(uai - umbral, 0)
        impuesto = base_gravable * tasa_imp if uai > 0 else 0
        un = uai - impuesto
        filas.append(dict(
            ano=i + 1,
            artistas_fin=fin[i], artistas_promedio=round(promedio_artistas[i], 2),
            artistas_pagantes=round(artistas_pagantes[i], 2),
            ing_prod=ing_prod[i], cog_prod=cog_prod[i],
            ing_roster_360=ing_roster_360[i], cog_roster_360=cog_roster_360[i],
            ing_youtube=ing_youtube[i], ing_libro=ing_libro[i], reg_catalogo=reg_catalogo[i],
            ingresos=ingresos, cogs=cogs, utilidad_bruta=ub, opex=opex,
            ebitda=ebitda, depreciacion=depre_anual, uai=uai, impuesto=impuesto,
            utilidad_neta=un,
            escalado_este_anio=escalado_activo and (anio_activacion is not None and i + 1 >= anio_activacion),
        ))
        fc.append(un + depre_anual)

    def npv(rate):
        return sum(cf / (1 + rate) ** t for t, cf in enumerate(fc))

    van = npv(p["tasa_descuento"])
    try:
        if npv(0.001) > 0 and npv(5.0) < 0:
            tir = brentq(npv, 0.001, 5.0)
        elif npv(0.001) < 0 and npv(5.0) > 0:
            tir = brentq(npv, 0.001, 5.0)
        else:
            tir = None
    except Exception:
        tir = None

    return dict(
        capex_subtotal=capex_subtotal, imprevistos=imprevistos, capex_total=capex_total,
        capital_trabajo=capital_trabajo, nti=nti, opex_mes1=opex_mes1,
        filas=filas, fc=fc, van=van, tir=tir, depre_anual=depre_anual,
        anio_activacion_gatillo=anio_activacion,
    )


dxb = compute(DXB_LEAN)

wb = openpyxl.Workbook()
wb.remove(wb.active)


def style_title(ws, text, row=1, span=6):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    c = ws.cell(row=row, column=1, value=text)
    c.font = FONT_TITLE


def style_header_row(ws, row, headers, start_col=1):
    for j, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col + j, value=h)
        c.fill = FILL_HEAD
        c.font = FONT_HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center")


def autosize(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def sheet_comparativo():
    ws = wb.create_sheet("Comparativo_vs_Completo", 0)
    style_title(ws, "DUBAI: MODELO LEAN/POR FASES vs. MODELO COMPLETO (v4 -- precio real ELITE 360)", span=3)
    ws.cell(row=2, column=1, value="v4: servicio 360 de marca con precio REAL de la plataforma (USD $2,999.99/mes/artista, plan ELITE 360), roster con tope de 12 y curva de ocupacion gradual (85% estimado), regalias de catalogo como UNICA linea de 'proyectos especiales' (no duplicada), YouTube propio, libro ya validado, legal casi a cero. Los numeros 'Modelo Completo' de referencia son los conocidos ANTES de esta correccion.").font = FONT_FLAG
    row = 4
    style_header_row(ws, row, ["Indicador", "Modelo Completo (AED, referencia pre-correccion)", "Modelo Lean/Por Fases v4 (AED)"])
    row += 1
    datos = [
        ("Necesidad Total de Inversion (NTI)", COMPLETO["nti"], dxb["nti"]),
        ("EBITDA Ano 1", COMPLETO["ebitda_anio"][0], dxb["filas"][0]["ebitda"]),
        ("EBITDA Ano 5", COMPLETO["ebitda_anio"][4], dxb["filas"][4]["ebitda"]),
        ("VAN (NPV)", COMPLETO["van"], dxb["van"]),
    ]
    for label, v1, v2 in datos:
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=2, value=round(v1) if v1 is not None else "N/D")
        ws.cell(row=row, column=3, value=round(v2) if v2 is not None else "N/D")
        row += 1
    ws.cell(row=row, column=1, value="TIR (IRR)")
    ws.cell(row=row, column=2, value="NO CALCULABLE (ref. pre-correccion)")
    ws.cell(row=row, column=3, value=round(dxb["tir"], 4) if dxb["tir"] is not None else "NO CALCULABLE")
    row += 2
    gat = dxb["anio_activacion_gatillo"]
    gat_txt = f"Se activo en el Ano {gat}" if gat else "NUNCA se activo en el horizonte de 5 anos bajo estos supuestos -- el escenario se queda lean todo el periodo."
    ws.cell(row=row, column=1, value="Estado del gatillo de escalamiento (ingresos > AED 150,000/ano y EBITDA >= 0)")
    ws.cell(row=row, column=2, value=gat_txt).font = FONT_FLAG
    row += 2
    if dxb["van"] < 0:
        lectura = ("Lectura honesta: incluso con el precio real del plan ELITE 360 (USD $2,999.99/mes/artista, "
                   "muy superior a la tarifa estimada que se uso antes), el VAN del escenario lean sigue siendo "
                   "negativo bajo una curva de ocupacion gradual y conservadora del roster -- el roster tarda "
                   "en llenarse (tope 12, curva 1->3->6->9->12) y el costo de entregar un servicio de alto "
                   "contacto (PM dedicado, videos, campamentos) sin contrataciones adicionales (modelo lean) es "
                   "una tension real que este modelo asume resuelta con freelancers por proyecto, no con equipo "
                   "fijo -- ver nota de riesgo operativo en Supuestos.")
    else:
        lectura = ("Lectura honesta: con el precio real del plan ELITE 360 (USD $2,999.99/mes/artista), el VAN "
                   "del escenario lean SI se vuelve positivo bajo la curva de ocupacion gradual del roster -- "
                   "el precio premium real cambia la viabilidad financiera frente al modelo anterior con tarifa "
                   "estimada mas baja. Esto depende criticamente de poder entregar el servicio de alto contacto "
                   "sin contrataciones fijas -- ver nota de riesgo operativo en Supuestos antes de comprometerse "
                   "con este numero frente a un inversionista.")
    ws.cell(row=row, column=1, value=lectura).font = FONT_FLAG
    autosize(ws, [55, 36, 32])


def sheet_supuestos():
    ws = wb.create_sheet("Supuestos")
    style_title(ws, "SUPUESTOS -- DUBAI LEAN/POR FASES (v4)", span=4)
    ws.cell(row=2, column=1, value=DXB_LEAN["fx_nota"]).font = FONT_FLAG
    ws.cell(row=3, column=1, value=DXB_LEAN["gatillo_nota"]).font = FONT_FLAG
    ws.cell(row=4, column=1, value=DXB_LEAN["roster_nota"]).font = FONT_FLAG
    ws.cell(row=5, column=1, value=DXB_LEAN["tasa_ocupacion_nota"]).font = FONT_FLAG
    ws.cell(row=6, column=1, value=DXB_LEAN["servicio_360_nota"]).font = FONT_FLAG
    ws.cell(row=7, column=1, value=DXB_LEAN["cogs_360_pct_nota"]).font = FONT_FLAG
    ws.cell(row=8, column=1, value=DXB_LEAN["regalias_catalogo_nota"]).font = FONT_FLAG
    row = 10
    style_header_row(ws, row, ["Rubro", "Valor", "Unidad", "Fuente / Supuesto a validar"])
    row += 1
    for label, val, nota in DXB_LEAN["capex"]:
        ws.cell(row=row, column=1, value="CAPEX: " + label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value="AED")
        c = ws.cell(row=row, column=4, value=nota)
        if "NO CONFIRMADO" in nota:
            c.font = FONT_FLAG
        row += 1
    for label, val, nota in DXB_LEAN["opex_mensual_lean"]:
        ws.cell(row=row, column=1, value="OPEX mensual (lean, Ano 1): " + label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value="AED/mes")
        c = ws.cell(row=row, column=4, value=nota)
        if "NO CONFIRMADO" in nota:
            c.font = FONT_FLAG
        row += 1
    for label, val, nota in DXB_LEAN["opex_mensual_escalado_extra"]:
        ws.cell(row=row, column=1, value="OPEX mensual ADICIONAL tras gatillo: " + label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value="AED/mes")
        ws.cell(row=row, column=4, value=nota)
        row += 1
    ws.cell(row=row, column=1, value="Roster: tope de artistas firmados")
    ws.cell(row=row, column=2, value=DXB_LEAN["roster_tope"])
    ws.cell(row=row, column=4, value=DXB_LEAN["roster_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Roster: artistas firmados fin de ano 1-5")
    ws.cell(row=row, column=2, value=str(DXB_LEAN["roster_fin_de_anio"]))
    row += 1
    ws.cell(row=row, column=1, value="Tasa de ocupacion del roster (estimada)")
    ws.cell(row=row, column=2, value=DXB_LEAN["tasa_ocupacion_roster"])
    ws.cell(row=row, column=4, value=DXB_LEAN["tasa_ocupacion_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Plan ELITE 360: fee mensual por artista (USD, PRECIO REAL)")
    ws.cell(row=row, column=2, value=DXB_LEAN["fee_360_usd_mensual"])
    ws.cell(row=row, column=3, value="USD/mes")
    ws.cell(row=row, column=4, value=DXB_LEAN["servicio_360_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Costo de entrega del plan ELITE 360 (% del fee)")
    ws.cell(row=row, column=2, value=DXB_LEAN["cogs_360_pct"])
    ws.cell(row=row, column=4, value=DXB_LEAN["cogs_360_pct_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Produccion (externos + roster puntual): precio unitario / volumen mensual por ano")
    ws.cell(row=row, column=2, value=f"{DXB_LEAN['produccion']['precio_unit']} / {DXB_LEAN['produccion']['vol_mensual_por_anio']}")
    ws.cell(row=row, column=3, value="AED")
    ws.cell(row=row, column=4, value=DXB_LEAN["produccion"]["nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="YouTube propio: ingreso mensual por ano")
    ws.cell(row=row, column=2, value=str(DXB_LEAN["youtube_mensual_por_anio"]))
    ws.cell(row=row, column=3, value="AED/mes")
    ws.cell(row=row, column=4, value=DXB_LEAN["youtube_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Libro 'Music Business Para Todos Los Humanos': copias/mes Ano1, crecimiento anual, margen/copia USD")
    ws.cell(row=row, column=2, value=f"{DXB_LEAN['libro_copias_mes_anio1']} / {DXB_LEAN['libro_crecimiento_anual']} / ${DXB_LEAN['libro_margen_usd']}")
    ws.cell(row=row, column=4, value=DXB_LEAN["libro_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Regalias de catalogo / proyectos especiales por ano (UNICA linea)")
    ws.cell(row=row, column=2, value=str(DXB_LEAN["regalias_catalogo_por_anio"]))
    ws.cell(row=row, column=3, value="AED/ano")
    ws.cell(row=row, column=4, value=DXB_LEAN["regalias_catalogo_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Tasa de descuento (TIR/VAN)")
    ws.cell(row=row, column=2, value=DXB_LEAN["tasa_descuento"])
    row += 1
    autosize(ws, [58, 30, 14, 85])
    ws.freeze_panes = "A10"


def sheet_capex():
    ws = wb.create_sheet("CAPEX")
    style_title(ws, "CAPEX -- DUBAI LEAN (ANO 1)", span=3)
    row = 3
    style_header_row(ws, row, ["Rubro", "Valor (AED)", "Nota"])
    row += 1
    for label, val, nota in DXB_LEAN["capex"]:
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value=nota)
        row += 1
    ws.cell(row=row, column=1, value="SUBTOTAL CAPEX").font = FONT_BOLD
    ws.cell(row=row, column=2, value=dxb["capex_subtotal"]).font = FONT_BOLD
    row += 1
    ws.cell(row=row, column=1, value="Imprevistos (15%)")
    ws.cell(row=row, column=2, value=dxb["imprevistos"])
    row += 1
    ws.cell(row=row, column=1, value="TOTAL CAPEX CON IMPREVISTOS").font = FONT_BOLD
    ws.cell(row=row, column=2, value=dxb["capex_total"]).font = FONT_BOLD
    row += 2
    ws.cell(row=row, column=1, value="Capital de trabajo (6 meses de OPEX lean)")
    ws.cell(row=row, column=2, value=dxb["capital_trabajo"])
    row += 1
    ws.cell(row=row, column=1, value="NECESIDAD TOTAL DE INVERSION (NTI)").font = FONT_BOLD
    ws.cell(row=row, column=2, value=dxb["nti"]).font = FONT_BOLD
    autosize(ws, [65, 18, 80])


def sheet_opex():
    ws = wb.create_sheet("OPEX")
    style_title(ws, "OPEX -- DUBAI LEAN (ANO 1) + ESCALAMIENTO POR FASES", span=3)
    row = 3
    style_header_row(ws, row, ["Rubro", "Valor mensual (AED)", "Nota"])
    row += 1
    for label, val, nota in DXB_LEAN["opex_mensual_lean"]:
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value=nota)
        row += 1
    ws.cell(row=row, column=1, value="TOTAL OPEX MENSUAL (LEAN)").font = FONT_BOLD
    ws.cell(row=row, column=2, value=dxb["opex_mes1"]).font = FONT_BOLD
    row += 2
    ws.cell(row=row, column=1, value="Adicional tras gatillo de escalamiento:").font = FONT_BOLD
    row += 1
    for label, val, nota in DXB_LEAN["opex_mensual_escalado_extra"]:
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value=nota)
        row += 1
    row += 1
    style_header_row(ws, row, ["Ano", "OPEX anual total", "Escalamiento activo este ano?"])
    row += 1
    for f in dxb["filas"]:
        ws.cell(row=row, column=1, value=f"Ano {f['ano']}")
        ws.cell(row=row, column=2, value=round(f["opex"]))
        ws.cell(row=row, column=3, value="SI" if f["escalado_este_anio"] else "NO")
        row += 1
    autosize(ws, [65, 22, 80])


def sheet_roster():
    ws = wb.create_sheet("Roster_ELITE360")
    style_title(ws, "ROSTER Y SERVICIO ELITE 360 POR ANO -- DUBAI LEAN", span=6)
    ws.cell(row=2, column=1, value=DXB_LEAN["servicio_360_nota"]).font = FONT_FLAG
    row = 4
    style_header_row(ws, row, ["Concepto"] + [f"Ano {i+1}" for i in range(5)])
    row += 1
    labels = [
        ("Artistas firmados (fin de ano)", "artistas_fin"),
        ("Artistas activos (promedio del ano)", "artistas_promedio"),
        ("Artistas pagantes (promedio x 85% ocupacion)", "artistas_pagantes"),
        ("Ingreso -- plan ELITE 360 (USD $2,999.99/mes/artista pagante)", "ing_roster_360"),
        ("(-) Costo de entrega del plan ELITE 360 (40% del fee)", "cog_roster_360"),
    ]
    for label, key in labels:
        ws.cell(row=row, column=1, value=label)
        for i, fila in enumerate(dxb["filas"]):
            v = fila[key]
            ws.cell(row=row, column=2 + i, value=v if key in ("artistas_promedio", "artistas_pagantes") else round(v))
        row += 1
    autosize(ws, [55, 16, 16, 16, 16, 16])


def sheet_resultados():
    ws = wb.create_sheet("EstadoResultados")
    style_title(ws, "ESTADO DE RESULTADOS PROYECTADO 5 ANOS -- DUBAI LEAN (v4)", span=6)
    row = 3
    labels = [
        ("Ingresos -- Produccion musical (terceros + roster puntual)", "ing_prod"),
        ("Ingresos -- Plan ELITE 360 (roster)", "ing_roster_360"),
        ("Ingresos -- YouTube propio", "ing_youtube"),
        ("Ingresos -- Libro 'Music Business Para Todos Los Humanos'", "ing_libro"),
        ("Ingresos -- Regalias de catalogo / proyectos especiales", "reg_catalogo"),
        ("INGRESOS TOTALES", "ingresos"),
        ("(-) COGS produccion", "cog_prod"),
        ("(-) COGS plan ELITE 360", "cog_roster_360"),
        ("(-) COGS TOTAL", "cogs"),
        ("UTILIDAD BRUTA", "utilidad_bruta"),
        ("(-) OPEX (lean, con escalamiento si se activa)", "opex"),
        ("EBITDA", "ebitda"),
        ("(-) Depreciacion", "depreciacion"),
        ("UTILIDAD ANTES DE IMPUESTOS (UAI)", "uai"),
        ("(-) Impuestos", "impuesto"),
        ("UTILIDAD NETA", "utilidad_neta"),
    ]
    style_header_row(ws, row, ["Rubro"] + [f"Ano {i+1}" for i in range(5)])
    row += 1
    bold_rows = {"INGRESOS TOTALES", "UTILIDAD BRUTA", "EBITDA", "UTILIDAD NETA"}
    for label, key in labels:
        ws.cell(row=row, column=1, value=label)
        if label in bold_rows:
            ws.cell(row=row, column=1).font = FONT_BOLD
        for i, fila in enumerate(dxb["filas"]):
            c = ws.cell(row=row, column=2 + i, value=round(fila[key]))
            if label in bold_rows:
                c.font = FONT_BOLD
        row += 1
    autosize(ws, [55, 16, 16, 16, 16, 16])


def sheet_flujo():
    ws = wb.create_sheet("FlujoCaja_TIR_VAN")
    style_title(ws, "FLUJO DE CAJA / TIR / VAN -- DUBAI LEAN (v4)", span=7)
    row = 3
    style_header_row(ws, row, ["Ano 0"] + [f"Ano {i}" for i in range(1, 6)])
    row += 1
    ws.cell(row=row, column=1, value="Flujo de caja neto")
    for i, v in enumerate(dxb["fc"]):
        ws.cell(row=row, column=2 + i, value=round(v))
    row += 3
    ws.cell(row=row, column=1, value="NTI (inversion inicial, Ano 0)").font = FONT_BOLD
    ws.cell(row=row, column=2, value=round(dxb["nti"])).font = FONT_BOLD
    row += 1
    ws.cell(row=row, column=1, value="Tasa de descuento usada")
    ws.cell(row=row, column=2, value=DXB_LEAN["tasa_descuento"])
    row += 1
    ws.cell(row=row, column=1, value="VAN (NPV)").font = FONT_BOLD
    ws.cell(row=row, column=2, value=round(dxb["van"])).font = FONT_BOLD
    row += 1
    ws.cell(row=row, column=1, value="TIR (IRR)").font = FONT_BOLD
    if dxb["tir"] is not None:
        ws.cell(row=row, column=2, value=round(dxb["tir"], 4)).font = FONT_BOLD
    else:
        c = ws.cell(row=row, column=2, value="NO CALCULABLE bajo estos supuestos")
        c.font = FONT_FLAG
    autosize(ws, [45, 16, 16, 16, 16, 16, 16])


sheet_comparativo()
sheet_supuestos()
sheet_capex()
sheet_opex()
sheet_roster()
sheet_resultados()
sheet_flujo()

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(str(OUT))

print("OK", OUT, OUT.stat().st_size, "bytes")
print()
print("=== DUBAI LEAN v4 (precio real ELITE 360 = USD 2,999.99/mes) ===")
print("NTI:", round(dxb["nti"]), "(vs. completo pre-correccion:", COMPLETO["nti"], ")")
for f in dxb["filas"]:
    print(f"Ano {f['ano']}: artistas_fin={f['artistas_fin']} pagantes={f['artistas_pagantes']} "
          f"Ingresos={round(f['ingresos'])} (prod={round(f['ing_prod'])} elite360={round(f['ing_roster_360'])} "
          f"yt={round(f['ing_youtube'])} libro={round(f['ing_libro'])} catalogo={round(f['reg_catalogo'])}) "
          f"OPEX={round(f['opex'])} EBITDA={round(f['ebitda'])} UtilNeta={round(f['utilidad_neta'])} "
          f"Escalado={f['escalado_este_anio']}")
print("VAN:", round(dxb["van"]), "TIR:", dxb["tir"])
print("Gatillo de escalamiento activado en Ano:", dxb["anio_activacion_gatillo"])
