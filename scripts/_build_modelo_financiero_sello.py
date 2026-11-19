"""Modelo financiero IM Music - Sello (standalone, sin agencia).
Dos escenarios paralelos: Medellin/Colombia (COP) y Dubai/EAU (AED).
Construido 100% desde supuestos explicitos (ver dicts COL/DXB) -- cada
cifra sin fuente verificada queda marcada en la pestana Supuestos.
"""
import math
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "sello_plan" / "modelo_financiero_sello.xlsx"

VIOLETA = "5E17EB"
CREMA = "F2EDE5"
GRIS = "222222"

FILL_HEAD = PatternFill("solid", fgColor=VIOLETA)
FONT_HEAD = Font(color="FFFFFF", bold=True)
FONT_TITLE = Font(color=VIOLETA, bold=True, size=14)
FONT_BOLD = Font(bold=True)
FONT_FLAG = Font(color="B00000", italic=True)

# ---------------------------------------------------------------------------
# SUPUESTOS -- Colombia (COP) y Dubai (AED)
# ---------------------------------------------------------------------------

COL = {
    "moneda": "COP",
    "fx_nota": "1 USD ~ 4,200 COP (referencia aproximada, no una tasa fija contractual)",
    "fx_usd": 4200,
    "tasa_descuento": 0.30,
    "tasa_impuesto": 0.35,
    "nexus_comision": 0.08,
    "capex": [
        ("Tratamiento acustico estudio (punto medio rango $25M-$50M COP)", 37_500_000,
         "Supuesto a validar: heredado del plan anterior, sin cotizacion local 2025/2026. Cotizar con DBA Acustica / 574 / The Icon."),
        ("Microfonos + interfaz de audio + monitores + licencia DAW", 15_000_000,
         "Supuesto a validar: sin fuente de precio colombiano verificado para este paquete."),
        ("Kit audiovisual basico (camara hibrida + 1 lente + luces 2-3 + tripode + mic lapel)", 18_500_000,
         "Reduccion deliberada vs. el kit de cine del plan anterior ($27M-$45M): el Content Engine propio ya cubre grafica/video editado/voz a costo marginal casi nulo; solo se necesita equipo para filmar en vivo."),
        ("Equipo de oficina (2 PCs)", 5_500_000,
         "Anclado en precio unitario del plan anterior ($2.75M c/u); se excluye la estacion de edicion dedicada de $10M porque la edicion ya esta scripteada/automatizada."),
        ("Adecuacion basica de oficina (mobiliario)", 5_000_000,
         "Supuesto a validar: estimacion propia, sin cotizacion."),
        ("Alianza con streamer: setup de transmision (camara + capturadora + microfono + kit de luces)", 3_000_000,
         "SUPUESTO CONSERVADOR: no hay streamer identificado ni cotizacion real -- es una estimacion generica de equipo basico de streaming. El retorno esperado de esta inversion es exposicion de marca/roster en contenido en vivo (cualitativo), NO un ingreso garantizado. Ver linea de upside opcional no garantizado en Ingresos."),
    ],
    "imprevistos_pct": 0.15,
    "capital_trabajo_meses": 6,
    "opex_mensual": [
        ("CEO / Director del Sello", 4_500_000, "Heredado del plan anterior (rol 'Dir. Sello', salario+prestaciones), sin verificacion independiente 2025/2026."),
        ("Gerente Comercial", 2_700_000, "Heredado del rol mas cercano del plan anterior (Asistente de Ventas); no hay cifra propia para 'gerente comercial' de sello."),
        ("Social Media Manager (curaduria, no produccion desde cero)", 2_000_000, "Dentro del rango VERIFICADO 2025 ($1.8M-$3.5M COP/mes, Computrabajo/El Empleo), elegido en el extremo bajo por ser rol part-time de curaduria."),
        ("Contador (retainer externo)", 800_000, "Supuesto a validar: sin cotizacion real."),
        ("Arriendo (espacio reducido vs. oficina+estudio de agencia)", 2_000_000, "Reducido vs. los $6.5M/mes del plan anterior (escala de agencia); supuesto a validar."),
        ("Herramientas tecnologicas", 400_000, "Minimo: el Content Engine usa stack ya construido y gratuito (Pillow/FFmpeg/edge-tts); no se repiten las herramientas SaaS de la agencia ($10M/mes)."),
        ("Marketing y promocion (catalogo propio, escalable)", 1_500_000, "Supuesto a validar: presupuesto de pauta modesto, no el presupuesto masivo de agencia ($31.2M/mes)."),
        ("Administrativos y generales", 1_000_000, "Heredado/ajustado del plan anterior."),
    ],
    "opex_crecimiento_anual": 0.08,
    "opex_step_up_anio": 3,
    "opex_step_up_valor_anual": 2_700_000 * 12,
    "opex_step_up_nota": "Nuevo Gerente Comercial de tiempo completo desde Año 3, segun el gatillo de escalamiento definido en el plan de negocios (>4-5 proyectos/mes sostenidos).",
    "produccion": {
        "precio_unit": 4_000_000, "cvu": 2_000_000,
        "vol_mensual_por_anio": [3, 4, 5, 6, 6],
        "nota": "Precio y costo variable anclados en la linea 'PRODUCCION MUSICAL' del plan anterior (supuesto a validar con cotizaciones reales). Volumen reducido de 100/mes (escala agencia) a 2-4 proyectos/mes reales de un sello boutique.",
    },
    "marca_personal": {
        "precio_unit": 11_000_000, "cvu": 3_500_000,
        "vol_mensual_por_anio": [1.5, 2, 2.5, 3, 3],
        "nota": "Precio anclado en 'ARTISTA TRADICIONAL PERSONALIZADO' del plan anterior. CVU reducido fuertemente (31.8% vs 69% del plan anterior) porque el Content Engine propio sustituye al equipo creativo humano que encarecia este servicio en el modelo de agencia -- ventaja de costo real, no supuesto optimista sin base.",
    },
    "roster_cap": 15,
    "roster_por_anio": [2, 4, 7, 11, 15],
    "roster_nota": "Tope duro de roster: maximo 15 artistas firmados en total (techo de largo plazo). Curva de crecimiento desde 1 artista actual hasta el techo a lo largo de 5 anos -- NO se asume crecimiento ilimitado del catalogo. Volumen mas alla de este techo (ej. cientos de usuarios de produccion/distribucion) pertenece al modelo financiero separado de la plataforma SaaS, no a este documento.",
    "marca_360": {
        "precio_mensual_usd": 2999.99,
        "ocupacion_pct_por_anio": [0.30, 0.45, 0.55, 0.65, 0.70],
        "nota": "PRECIO REAL Y CONFIRMADO: plan 'ELITE 360 / ARTIST DEVELOPMENT 360' ya definido en el codigo de la plataforma IM Music (Project Manager dedicado, manager musical, produccion de videos musicales, branding, Meta Ads gestionado, campamentos musicales, red de industria) -- USD $2,999.99/mes por artista activo del roster. Convertido a moneda local con la tasa de referencia de este modelo. Lo que SI es supuesto propio (no dato de mercado) es la OCUPACION: no se asume que todo el roster paga el plan completo desde el mes 1 -- se modela una curva de llenado/retencion creciente y conservadora, a validar.",
    },
    "regalias_catalogo": {
        "gross_por_anio": [3_000_000, 5_000_000, 8_000_000, 10_000_000, 12_000_000],
        "nota": "Regalias de catalogo = retorno (via Nexus, 8% comision) de las canciones/EPs/albumes en los que el sello invirtio capital propio para financiar su produccion, con % de regalia negociado caso por caso por proyecto. No es automatico ni aplica a todo el roster -- es oportunista y modesto, ligado a cuantos proyectos especiales financia el sello cada ano, no al tamano del roster. Supuesto a validar: sin cifras reales de streams ni de cuantos proyectos especiales se financiaran.",
    },
    "youtube": {
        "vistas_mensuales_por_anio": [50_000, 100_000, 200_000, 350_000, 500_000],
        "rpm_usd": 1.5,
        "nota": "Ingreso del canal propio de YouTube (AdSense/Content ID), separado de las regalias de streaming via Nexus. Supuesto a validar: el RPM de musica en YouTube varia mucho por territorio/nicho; 1.5 USD/1000 vistas es un punto de referencia conservador generico, no un dato verificado para este canal especifico. Vistas mensuales son supuesto propio de crecimiento del canal.",
    },
    "libro": {
        "ingreso_anual_por_anio": [6_000_000, 8_000_000, 10_000_000, 12_000_000, 14_000_000],
        "nota": "El libro 'Music Business Para Todos Los Humanos' SI es un producto real ya en venta en Hotmart (ES/EN/PT) -- no es hipotetico que exista o genere ingreso. El VOLUMEN de ventas proyectado aqui es un supuesto conservador de crecimiento lento y estable, a validar contra el dashboard real de Hotmart (no se tienen cifras de ventas reales a la fecha de este modelo).",
    },
    "legal_puntual_anual": 2_000_000,
    "legal_nota": "Se elimina el retainer fijo de abogado externo: el fundador cubre la funcion legal del dia a dia directamente. Se deja solo una provision puntual anual para casos de alta complejidad (ej. negociacion de contrato compleja, registro de marca, litigio puntual) -- monto estimado, no cotizado.",
    "streamer_upside_por_anio": [0, 500_000, 800_000, 1_000_000, 1_200_000],
    "streamer_upside_nota": "MEMO -- NO incluido en Ingresos Totales ni en TIR/VAN. Upside opcional: % de ingresos del streamer SOLO SI se negocia un reparto -- no es un ingreso garantizado, el retorno esperado real de esta alianza es exposicion de marca/roster (cualitativo). Cifra puramente ilustrativa, sin streamer identificado ni acuerdo real.",
    "depreciacion_anios": 5,
}

DXB = {
    "moneda": "AED",
    "fx_nota": "1 USD ~ 3.6725 AED (paridad oficial AED/USD); conversion COP->AED via USD a ~4,200 COP/USD. Cifras convertidas son MARCADORES, no cotizaciones locales.",
    "fx_usd": 3.6725,
    "tasa_descuento": 0.25,
    "tasa_impuesto_nota": "0% hasta AED 375,000 de utilidad gravable, 9% sobre el excedente (confirmado, Deloitte/FTA). En este modelo la utilidad nunca supera ese umbral, por lo que el impuesto efectivo modelado es 0% en los 5 anos.",
    "umbral_exento": 375_000,
    "tasa_impuesto": 0.09,
    "nexus_comision": 0.08,
    "capex": [
        ("Estudio (tratamiento acustico + mics + interfaz + monitores + DAW) -- CONVERTIDO de Colombia, NO es cotizacion de EAU", 45_906,
         "NO CONFIRMADO: no existe fuente de costo de estudio en EAU. Esta cifra es la conversion directa de la cifra colombiana (ya de por si sin confirmar) via FX. Cotizar localmente antes de usar."),
        ("Kit audiovisual basico -- convertido de Colombia", 16_177,
         "NO CONFIRMADO: mismo problema que la linea anterior, conversion de cifra colombiana sin cotizacion de EAU."),
        ("Equipo de oficina (2 PCs + mobiliario) -- convertido de Colombia", 9_181,
         "NO CONFIRMADO: conversion de cifra colombiana."),
        ("Arancel de importacion 5% CIF sobre equipo importado (kit audiovisual + PCs)", 1_268,
         "CONFIRMADO: arancel general EAU de 5% sobre valor CIF (u.ae). Base de calculo es un supuesto propio (que el equipo se importa), la tasa del 5% si esta sourced."),
        ("Licencia zona franca (IFZA, paquete mas economico sourced)", 12_900,
         "Estimacion de consultora (businesslinkuae.com), NO es tarifa oficial de gobierno. Elegido IFZA sobre Dubai Media City porque no exige capital minimo de AED 50,000."),
        ("Visas (1 inversionista + 1 empleado, ano 1)", 18_750,
         "NO CONFIRMADO: rangos de fuentes de baja confiabilidad (visa inversionista AED 7,000-20,000+, visa empleado AED 3,000-7,500); se usa el punto medio de cada rango."),
        ("Alianza con streamer: setup de transmision -- convertido de Colombia", 2_623,
         "SUPUESTO CONSERVADOR convertido via FX: no hay streamer identificado ni cotizacion real en EAU ni en Colombia. Retorno esperado es exposicion de marca/roster (cualitativo), NO ingreso garantizado."),
    ],
    "imprevistos_pct": 0.15,
    "capital_trabajo_meses": 6,
    "opex_mensual": [
        ("CEO / Director del Sello", 12_000, "NO CONFIRMADO: sin fuente directa de EAU para este rol; posicionado por encima del rango sourced de Marketing Executive (AED 5,500) y Social Media Manager (~AED 6,000) por mayor seniority, pero es un supuesto, no una oferta de mercado real."),
        ("Gerente Comercial (anclado en 'Marketing Executive')", 5_500, "CONFIRMADO como rango de mercado (GulfTalent) para el rol mas cercano disponible; 'Gerente Comercial de sello' especifico no tiene fuente propia."),
        ("Social Media Manager", 6_000, "CONFIRMADO: Payscale Dubai, rango AED 5,900-6,000/mes."),
        ("Contador (retainer externo)", 1_200, "NO CONFIRMADO: placeholder sin cotizacion real."),
        ("Arriendo (unidad pequena, ~150 sqft, tarifa de micro-unidad)", 3_575, "CONFIRMADO el dato de tarifa por sqft (Nikoliers 2024, rango AED 283-290/sqft/ano para unidades pequenas); el tamano de 150 sqft es un supuesto propio."),
        ("Herramientas tecnologicas", 500, "NO CONFIRMADO: estimacion propia."),
        ("Marketing y promocion", 2_000, "NO CONFIRMADO: sin datos de CAC/audiencia de musica latina en EAU."),
        ("Administrativos y generales", 800, "NO CONFIRMADO: estimacion propia."),
    ],
    "opex_crecimiento_anual": 0.06,
    "produccion": {
        "precio_unit": 3_500, "cvu": 1_750,
        "vol_mensual_por_anio": [1, 1.5, 2, 2.5, 3],
        "nota": "Precio = conversion directa del precio colombiano (decision de pricing propia, no dato de mercado). Volumen deliberadamente mas bajo que Colombia (sin base de clientes ni validacion de demanda local) -- es un supuesto de arranque conservador, no una proyeccion de mercado.",
    },
    "marca_personal": {
        "precio_unit": 9_600, "cvu": 3_050,
        "vol_mensual_por_anio": [0.5, 0.75, 1, 1.5, 2],
        "nota": "Mismo comentario que produccion: precio convertido, volumen deliberadamente conservador por falta de validacion de demanda.",
    },
    "roster_cap": 15,
    "roster_por_anio": [1, 2, 3, 5, 7],
    "roster_nota": "Mismo techo estructural de 15 artistas que Colombia (es el mismo negocio, otra sede), pero curva de crecimiento mucho mas lenta: sin escena/relaciones locales ni validacion de demanda (ver plan de negocios, Seccion 5.2), no es realista firmar al mismo ritmo que en Medellin.",
    "marca_360": {
        "precio_mensual_usd": 2999.99,
        "ocupacion_pct_por_anio": [0.15, 0.25, 0.35, 0.45, 0.55],
        "nota": "Mismo precio real confirmado de la plataforma (USD $2,999.99/mes), convertido a AED con la paridad oficial. Ocupacion deliberadamente mas baja y mas lenta que Colombia -- supuesto propio, sin ninguna validacion de demanda local, no es un dato de mercado.",
    },
    "regalias_catalogo": {
        "gross_por_anio": [500, 1_000, 1_500, 2_000, 2_500],
        "nota": "Mismo concepto que Colombia (regalias de catalogo por inversion caso por caso del sello en proyectos especiales, via Nexus), escalado muy a la baja -- sin historial ni base de catalogo local, y con EMRA (sociedad de derechos de EAU) sin tarifas comerciales activas hasta diciembre 2026.",
    },
    "youtube": {
        "vistas_mensuales_por_anio": [5_000, 10_000, 20_000, 30_000, 45_000],
        "rpm_usd": 1.5,
        "nota": "Vistas mucho menores que Colombia por falta de audiencia/canal establecido en la region; mismo RPM generico sin dato especifico de territorio EAU.",
    },
    "libro": {
        "ingreso_anual_por_anio": [0, 0, 0, 0, 0],
        "nota": "Se proyecta en CERO: no hay ninguna senal de demanda del libro en EAU (el libro ha tenido traccion en el mercado hispanohablante). Incluir una cifra simbolica sin ninguna base seria inventar un dato -- se deja en cero explicitamente.",
    },
    "legal_puntual_anual": 3_000,
    "legal_nota": "Se elimina el retainer fijo de abogado externo, igual que en Colombia. Provision puntual anual ajustada al alza vs. la conversion directa de Colombia (AED 1,749) porque los honorarios legales puntuales en EAU probablemente son mayores -- sigue siendo un supuesto sin cotizacion real.",
    "streamer_upside_por_anio": [0, 440, 700, 875, 1_050],
    "streamer_upside_nota": "MEMO -- NO incluido en Ingresos Totales ni en TIR/VAN. Mismo concepto que Colombia, convertido via FX; sin streamer identificado ni acuerdo real en EAU.",
    "depreciacion_anios": 5,
}


def compute(p):
    n = 5
    capex_subtotal = sum(x[1] for x in p["capex"])
    imprevistos = capex_subtotal * p["imprevistos_pct"]
    capex_total = capex_subtotal + imprevistos
    opex_mes1 = sum(x[1] for x in p["opex_mensual"])
    opex_anual = [opex_mes1 * 12]
    for i in range(1, n):
        val = opex_anual[-1] * (1 + p["opex_crecimiento_anual"])
        if p.get("opex_step_up_anio") == i + 1:
            val += p["opex_step_up_valor_anual"]
        opex_anual.append(val)
    opex_anual = [v + p["legal_puntual_anual"] for v in opex_anual]
    capital_trabajo = opex_mes1 * p["capital_trabajo_meses"]
    nti = capex_total + capital_trabajo

    def linea_servicio(cfg):
        ing, cog = [], []
        for vol in cfg["vol_mensual_por_anio"]:
            ing.append(vol * cfg["precio_unit"] * 12)
            cog.append(vol * cfg["cvu"] * 12)
        return ing, cog

    ing_prod, cog_prod = linea_servicio(p["produccion"])
    ing_marca, cog_marca = linea_servicio(p["marca_personal"])

    # Marca 360 (roster): precio REAL confirmado de la plataforma x ocupacion (supuesto)
    m360 = p["marca_360"]
    precio_mensual_360 = m360["precio_mensual_usd"] * p["fx_usd"]
    roster = p["roster_por_anio"]
    ocup = m360["ocupacion_pct_por_anio"]
    ing_360 = [roster[i] * ocup[i] * precio_mensual_360 * 12 for i in range(n)]

    # Regalias de catalogo: UNA sola linea (no duplicar) -- inversion propia en
    # proyectos especiales, % negociado caso por caso, distribuido via Nexus (8%).
    rc = p["regalias_catalogo"]
    reg_gross = rc["gross_por_anio"]
    reg_comision = [x * p["nexus_comision"] for x in reg_gross]

    # YouTube propio (AdSense/Content ID), separado de Nexus
    yt = p["youtube"]
    ing_youtube = [v * yt["rpm_usd"] / 1000 * p["fx_usd"] * 12 for v in yt["vistas_mensuales_por_anio"]]

    # Libro "Music Business Para Todos Los Humanos" (ya en venta real en Hotmart)
    ing_libro = p["libro"]["ingreso_anual_por_anio"]

    depre_anual = capex_total / p["depreciacion_anios"]
    tasa_imp = p["tasa_impuesto"]
    umbral = p.get("umbral_exento", 0)

    filas = []
    fc = [-nti]
    for i in range(n):
        ingresos = ing_prod[i] + ing_marca[i] + ing_360[i] + reg_gross[i] + ing_youtube[i] + ing_libro[i]
        cogs = cog_prod[i] + cog_marca[i] + reg_comision[i]
        ub = ingresos - cogs
        opex = opex_anual[i]
        ebitda = ub - opex
        uai = ebitda - depre_anual
        base_gravable = max(uai - umbral, 0) if umbral else max(uai, 0)
        impuesto = base_gravable * tasa_imp if uai > 0 else 0
        un = uai - impuesto
        filas.append(dict(
            ano=i + 1, ing_prod=ing_prod[i], cog_prod=cog_prod[i],
            ing_marca=ing_marca[i], cog_marca=cog_marca[i],
            ing_360=ing_360[i], roster_size=roster[i], ocupacion=ocup[i],
            reg_gross=reg_gross[i], reg_comision=reg_comision[i],
            ing_youtube=ing_youtube[i], ing_libro=ing_libro[i],
            streamer_upside_memo=p["streamer_upside_por_anio"][i],
            ingresos=ingresos, cogs=cogs, utilidad_bruta=ub, opex=opex,
            ebitda=ebitda, depreciacion=depre_anual, uai=uai, impuesto=impuesto,
            utilidad_neta=un,
        ))
        fc.append(un + depre_anual)

    def npv(rate):
        return sum(cf / (1 + rate) ** t for t, cf in enumerate(fc))

    van = npv(p["tasa_descuento"])
    try:
        if npv(0.001) > 0 and npv(5.0) < 0:
            tir = brentq(npv, 0.001, 5.0)
        else:
            tir = None
    except Exception:
        tir = None

    return dict(
        capex_subtotal=capex_subtotal, imprevistos=imprevistos, capex_total=capex_total,
        capital_trabajo=capital_trabajo, nti=nti, opex_anual=opex_anual, opex_mes1=opex_mes1,
        filas=filas, fc=fc, van=van, tir=tir, depre_anual=depre_anual,
    )


col = compute(COL)
dxb = compute(DXB)

# ---------------------------------------------------------------------------
# Construccion del workbook
# ---------------------------------------------------------------------------
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


def sheet_supuestos(name, p, results):
    ws = wb.create_sheet(name)
    style_title(ws, f"SUPUESTOS -- {name}", span=4)
    ws.cell(row=2, column=1, value=p["fx_nota"]).font = FONT_FLAG
    row = 4
    style_header_row(ws, row, ["Rubro", "Valor", f"Unidad ({p['moneda']})", "Fuente / Supuesto a validar"])
    row += 1
    for label, val, nota in p["capex"]:
        ws.cell(row=row, column=1, value="CAPEX: " + label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value=p["moneda"])
        c = ws.cell(row=row, column=4, value=nota)
        if "NO CONFIRMADO" in nota or "Supuesto a validar" in nota or "sin" in nota.lower():
            c.font = FONT_FLAG
        row += 1
    for label, val, nota in p["opex_mensual"]:
        ws.cell(row=row, column=1, value="OPEX mensual: " + label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value=p["moneda"] + "/mes")
        c = ws.cell(row=row, column=4, value=nota)
        if "NO CONFIRMADO" in nota or "sin" in nota.lower() or "placeholder" in nota.lower():
            c.font = FONT_FLAG
        row += 1
    for key in ["produccion", "marca_personal"]:
        cfg = p[key]
        ws.cell(row=row, column=1, value=f"Ingreso {key}: precio unitario")
        ws.cell(row=row, column=2, value=cfg["precio_unit"])
        ws.cell(row=row, column=3, value=p["moneda"])
        ws.cell(row=row, column=4, value=cfg["nota"]).font = FONT_FLAG
        row += 1
        ws.cell(row=row, column=1, value=f"Ingreso {key}: volumen mensual por ano")
        ws.cell(row=row, column=2, value=str(cfg["vol_mensual_por_anio"]))
        row += 1
    ws.cell(row=row, column=1, value="Roster: tope maximo de artistas firmados")
    ws.cell(row=row, column=2, value=p["roster_cap"])
    ws.cell(row=row, column=4, value=p["roster_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Roster: numero de artistas firmados por ano")
    ws.cell(row=row, column=2, value=str(p["roster_por_anio"]))
    row += 1
    m360 = p["marca_360"]
    ws.cell(row=row, column=1, value="Marca 360 (roster): precio mensual por artista (USD, PRECIO REAL de la plataforma)")
    ws.cell(row=row, column=2, value=m360["precio_mensual_usd"])
    row += 1
    ws.cell(row=row, column=1, value="Marca 360 (roster): % de ocupacion/retencion del roster en el plan, por ano")
    ws.cell(row=row, column=2, value=str(m360["ocupacion_pct_por_anio"]))
    ws.cell(row=row, column=4, value=m360["nota"]).font = FONT_FLAG
    row += 1
    rc = p["regalias_catalogo"]
    ws.cell(row=row, column=1, value="Regalias de catalogo (proyectos especiales con inversion propia) por ano, bruto")
    ws.cell(row=row, column=2, value=str(rc["gross_por_anio"]))
    ws.cell(row=row, column=4, value=rc["nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Provision legal puntual anual (sin retainer fijo -- fundador cubre el dia a dia)")
    ws.cell(row=row, column=2, value=p["legal_puntual_anual"])
    ws.cell(row=row, column=4, value=p["legal_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Comision Nexus sobre regalias de catalogo")
    ws.cell(row=row, column=2, value=p["nexus_comision"])
    row += 1
    yt = p["youtube"]
    ws.cell(row=row, column=1, value="YouTube propio: vistas mensuales por ano / RPM (USD/1000 vistas)")
    ws.cell(row=row, column=2, value=f"vistas={yt['vistas_mensuales_por_anio']} / rpm={yt['rpm_usd']}")
    ws.cell(row=row, column=4, value=yt["nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Libro 'Music Business Para Todos Los Humanos': ingreso anual por ano")
    ws.cell(row=row, column=2, value=str(p["libro"]["ingreso_anual_por_anio"]))
    ws.cell(row=row, column=4, value=p["libro"]["nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="MEMO (no sumado a ingresos): upside opcional ingreso compartido con streamer, por ano")
    ws.cell(row=row, column=2, value=str(p["streamer_upside_por_anio"]))
    ws.cell(row=row, column=4, value=p["streamer_upside_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Tasa de descuento (TIR/VAN)")
    ws.cell(row=row, column=2, value=p["tasa_descuento"])
    row += 1
    autosize(ws, [45, 22, 14, 70])
    ws.freeze_panes = "A5"


def sheet_capex(name, p, results):
    ws = wb.create_sheet(f"CAPEX_{name}")
    style_title(ws, f"CAPEX -- {name}", span=3)
    row = 3
    style_header_row(ws, row, ["Rubro", f"Valor ({p['moneda']})", "Nota"])
    row += 1
    for label, val, nota in p["capex"]:
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value=nota)
        row += 1
    ws.cell(row=row, column=1, value="SUBTOTAL CAPEX").font = FONT_BOLD
    ws.cell(row=row, column=2, value=results["capex_subtotal"]).font = FONT_BOLD
    row += 1
    ws.cell(row=row, column=1, value=f"Imprevistos ({p['imprevistos_pct']:.0%})")
    ws.cell(row=row, column=2, value=results["imprevistos"])
    row += 1
    ws.cell(row=row, column=1, value="TOTAL CAPEX CON IMPREVISTOS").font = FONT_BOLD
    ws.cell(row=row, column=2, value=results["capex_total"]).font = FONT_BOLD
    row += 2
    ws.cell(row=row, column=1, value=f"Capital de trabajo ({p['capital_trabajo_meses']} meses de OPEX)")
    ws.cell(row=row, column=2, value=results["capital_trabajo"])
    row += 1
    ws.cell(row=row, column=1, value="NECESIDAD TOTAL DE INVERSION (NTI)").font = FONT_BOLD
    c = ws.cell(row=row, column=2, value=results["nti"])
    c.font = FONT_BOLD
    autosize(ws, [55, 20, 75])


def sheet_opex(name, p, results):
    ws = wb.create_sheet(f"OPEX_{name}")
    style_title(ws, f"OPEX MENSUAL (ANO 1) -- {name}", span=3)
    row = 3
    style_header_row(ws, row, ["Rubro", f"Valor mensual ({p['moneda']})", "Nota"])
    row += 1
    for label, val, nota in p["opex_mensual"]:
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=2, value=val)
        ws.cell(row=row, column=3, value=nota)
        row += 1
    ws.cell(row=row, column=1, value="TOTAL OPEX MENSUAL").font = FONT_BOLD
    ws.cell(row=row, column=2, value=results["opex_mes1"]).font = FONT_BOLD
    row += 2
    style_header_row(ws, row, ["Ano", "OPEX anual"])
    row += 1
    for i, v in enumerate(results["opex_anual"], start=1):
        ws.cell(row=row, column=1, value=f"Ano {i}")
        ws.cell(row=row, column=2, value=v)
        row += 1
    autosize(ws, [55, 20, 75])


def sheet_resultados(name, p, results):
    ws = wb.create_sheet(f"EstadoResultados_{name}")
    style_title(ws, f"ESTADO DE RESULTADOS PROYECTADO 5 ANOS -- {name}", span=6)
    row = 3
    labels = [
        ("Ingresos -- Produccion musical a terceros (clientes externos)", "ing_prod"),
        ("Ingresos -- Desarrollo de marca personal (clientes externos)", "ing_marca"),
        ("Ingresos -- Marca 360 (roster, USD $2,999.99/mes x ocupacion)", "ing_360"),
        ("Ingresos -- Regalias de catalogo (proyectos especiales, bruto)", "reg_gross"),
        ("Ingresos -- YouTube propio (AdSense/Content ID)", "ing_youtube"),
        ("Ingresos -- Libro 'Music Business Para Todos Los Humanos'", "ing_libro"),
        ("INGRESOS TOTALES", "ingresos"),
        ("(-) COGS produccion", "cog_prod"),
        ("(-) COGS marca personal", "cog_marca"),
        ("(-) Comision Nexus sobre regalias de catalogo (8%)", "reg_comision"),
        ("(-) COGS TOTAL", "cogs"),
        ("UTILIDAD BRUTA", "utilidad_bruta"),
        ("(-) OPEX", "opex"),
        ("EBITDA", "ebitda"),
        ("(-) Depreciacion", "depreciacion"),
        ("UTILIDAD ANTES DE IMPUESTOS (UAI)", "uai"),
        ("(-) Impuestos", "impuesto"),
        ("UTILIDAD NETA", "utilidad_neta"),
    ]
    style_header_row(ws, row, ["Rubro"] + [f"Ano {i+1}" for i in range(5)])
    row += 1
    ws.cell(row=row, column=1, value="Memo -- artistas en roster (firmados)")
    for i, fila in enumerate(results["filas"]):
        ws.cell(row=row, column=2 + i, value=fila["roster_size"])
    row += 1
    ws.cell(row=row, column=1, value="Memo -- % ocupacion plan Marca 360")
    for i, fila in enumerate(results["filas"]):
        ws.cell(row=row, column=2 + i, value=fila["ocupacion"])
    row += 1
    c = ws.cell(row=row, column=1, value="Memo -- upside opcional streamer (NO incluido en Ingresos Totales, no garantizado)")
    c.font = FONT_FLAG
    for i, fila in enumerate(results["filas"]):
        ws.cell(row=row, column=2 + i, value=fila["streamer_upside_memo"]).font = FONT_FLAG
    row += 1
    bold_rows = {"INGRESOS TOTALES", "UTILIDAD BRUTA", "EBITDA", "UTILIDAD NETA"}
    for label, key in labels:
        ws.cell(row=row, column=1, value=label)
        if label in bold_rows:
            ws.cell(row=row, column=1).font = FONT_BOLD
        for i, fila in enumerate(results["filas"]):
            c = ws.cell(row=row, column=2 + i, value=round(fila[key]))
            if label in bold_rows:
                c.font = FONT_BOLD
        row += 1
    autosize(ws, [42, 16, 16, 16, 16, 16])


def sheet_flujo(name, p, results):
    ws = wb.create_sheet(f"FlujoCaja_TIR_VAN_{name}")
    style_title(ws, f"FLUJO DE CAJA / TIR / VAN -- {name}", span=7)
    row = 3
    style_header_row(ws, row, ["Ano 0"] + [f"Ano {i}" for i in range(1, 6)])
    row += 1
    ws.cell(row=row, column=1, value="Flujo de caja neto")
    for i, v in enumerate(results["fc"]):
        ws.cell(row=row, column=2 + i, value=round(v))
    row += 3
    ws.cell(row=row, column=1, value="NTI (inversion inicial, Ano 0)").font = FONT_BOLD
    ws.cell(row=row, column=2, value=round(results["nti"])).font = FONT_BOLD
    row += 1
    ws.cell(row=row, column=1, value=f"Tasa de descuento usada")
    ws.cell(row=row, column=2, value=p["tasa_descuento"])
    row += 1
    ws.cell(row=row, column=1, value="VAN (NPV)").font = FONT_BOLD
    ws.cell(row=row, column=2, value=round(results["van"])).font = FONT_BOLD
    row += 1
    ws.cell(row=row, column=1, value="TIR (IRR)").font = FONT_BOLD
    if results["tir"] is not None:
        ws.cell(row=row, column=2, value=round(results["tir"], 4)).font = FONT_BOLD
    else:
        c = ws.cell(row=row, column=2, value="NO CALCULABLE -- todos los flujos de caja son negativos en el horizonte de 5 anos bajo estos supuestos")
        c.font = FONT_FLAG
    autosize(ws, [45, 16, 16, 16, 16, 16, 16])


def sheet_resumen():
    ws = wb.create_sheet("RESUMEN_COMPARATIVO", 0)
    style_title(ws, "IM MUSIC -- SELLO: RESUMEN COMPARATIVO MEDELLIN vs DUBAI", span=3)
    ws.cell(row=2, column=1, value="Cifras reales, conservadoras, con cada supuesto no verificado senalado en las pestanas Supuestos_COL / Supuestos_DXB. Este NO es el modelo agresivo del plan anterior.").font = FONT_FLAG
    row = 4
    style_header_row(ws, row, ["Indicador", "Medellin (COP)", "Dubai (AED)"])
    row += 1
    datos = [
        ("Necesidad Total de Inversion (NTI)", col["nti"], dxb["nti"]),
        ("Ingresos Ano 1", col["filas"][0]["ingresos"], dxb["filas"][0]["ingresos"]),
        ("EBITDA Ano 1", col["filas"][0]["ebitda"], dxb["filas"][0]["ebitda"]),
        ("Utilidad Neta Ano 1", col["filas"][0]["utilidad_neta"], dxb["filas"][0]["utilidad_neta"]),
        ("Ingresos Ano 5", col["filas"][4]["ingresos"], dxb["filas"][4]["ingresos"]),
        ("EBITDA Ano 5", col["filas"][4]["ebitda"], dxb["filas"][4]["ebitda"]),
        ("Utilidad Neta Ano 5", col["filas"][4]["utilidad_neta"], dxb["filas"][4]["utilidad_neta"]),
        ("VAN (NPV)", col["van"], dxb["van"]),
    ]
    for label, v_col, v_dxb in datos:
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=2, value=round(v_col))
        ws.cell(row=row, column=3, value=round(v_dxb))
        row += 1
    ws.cell(row=row, column=1, value="TIR (IRR)")
    ws.cell(row=row, column=2, value=round(col["tir"], 4) if col["tir"] else "N/A")
    ws.cell(row=row, column=3, value=round(dxb["tir"], 4) if dxb["tir"] else "NO CALCULABLE (flujos siempre negativos)")
    row += 2
    ws.cell(row=row, column=1, value="Lectura honesta: el ingreso 'Marca 360' usa un PRECIO REAL confirmado de la plataforma (USD $2,999.99/mes por artista), lo que hace que ambos escenarios luzcan mucho mas fuertes que en la version anterior de este modelo -- pero todo el resultado depende de poder cobrar ese precio de forma sostenida a artistas emergentes/boutique, algo que NO esta validado comercialmente (ver nota de ocupacion en Supuestos). Medellin: TIR fuerte (ver pestana) impulsada por ese precio, con ocupacion conservadora del roster. Dubai: mejora sustancialmente vs. la version anterior (llega a Utilidad Neta positiva en Ano 5), pero el VAN acumulado a 5 anos sigue siendo negativo y la TIR sigue sin ser calculable -- no se vuelve una propuesta claramente viable dentro del horizonte evaluado.").font = FONT_FLAG
    autosize(ws, [42, 22, 30])


sheet_resumen()
sheet_supuestos("COL", COL, col)
sheet_capex("COL", COL, col)
sheet_opex("COL", COL, col)
sheet_resultados("COL", COL, col)
sheet_flujo("COL", COL, col)
sheet_supuestos("DXB", DXB, dxb)
sheet_capex("DXB", DXB, dxb)
sheet_opex("DXB", DXB, dxb)
sheet_resultados("DXB", DXB, dxb)
sheet_flujo("DXB", DXB, dxb)

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(str(OUT))

print("OK", OUT, OUT.stat().st_size, "bytes")
print()
print("=== COLOMBIA ===")
print("NTI:", round(col["nti"]))
for f in col["filas"]:
    print(f"Ano {f['ano']}: Ingresos={round(f['ingresos'])} EBITDA={round(f['ebitda'])} UtilNeta={round(f['utilidad_neta'])}")
print("VAN:", round(col["van"]), "TIR:", col["tir"])
print()
print("=== DUBAI ===")
print("NTI:", round(dxb["nti"]))
for f in dxb["filas"]:
    print(f"Ano {f['ano']}: Ingresos={round(f['ingresos'])} EBITDA={round(f['ebitda'])} UtilNeta={round(f['utilidad_neta'])}")
print("VAN:", round(dxb["van"]), "TIR:", dxb["tir"])
