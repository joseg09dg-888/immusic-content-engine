"""Modelo financiero IM Music - Sello (standalone, sin agencia).
Dos escenarios paralelos: Medellin/Colombia (COP) y Dubai/EAU (AED), mas
dos bloques adicionales (Medellin reducido, referencia a Dubai Lean) para
comparar Escenario A (base Medellin) vs Escenario B (base Dubai).
Construido 100% desde supuestos explicitos -- cada cifra sin fuente
verificada queda marcada y consolidada en las pestanas Supuestos_COL/DXB.
"""
import copy
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
FILL_SUBTOTAL = PatternFill("solid", fgColor="E8E0FB")
FONT_HEAD = Font(color="FFFFFF", bold=True)
FONT_TITLE = Font(color=VIOLETA, bold=True, size=14)
FONT_SECTION = Font(color=VIOLETA, bold=True, size=11)
FONT_BOLD = Font(bold=True)
FONT_FLAG = Font(color="B00000", italic=True)
MONEY_FMT = "#,##0"
PCT_FMT = "0.0%"

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
         "Reduccion deliberada vs. el kit de cine del plan anterior ($27M-$45M): el Content Engine propio ya cubre grafica/video editado/voz a costo marginal casi nulo; solo se necesita equipo para filmar en vivo (camara/luces/tripode/mic)."),
        ("Estacion de edicion (Filmmaker) + estacion de diseno (Disenadora): equipo de computo + perifericos", 14_500_000,
         "CAMBIO DE ESTRUCTURA: el Filmmaker y la Disenadora dejan de ser freelance y pasan a PLANTA FIJA (ver Supuestos, bloque EQUIPO/NOMINA) -- ya no traen su propio equipo. PC potente edicion video ~$9.0M + PC/tableta diseno ~$5.5M. Las LICENCIAS (CapCut Pro, Canva Pro) siguen en OPEX, no se duplican aqui."),
        ("Equipo de oficina (2 PCs)", 5_500_000,
         "Anclado en precio unitario del plan anterior ($2.75M c/u); se excluye estacion de edicion dedicada porque esa ya se presupuesta aparte arriba."),
        ("Adecuacion basica de oficina (mobiliario)", 5_000_000,
         "Supuesto a validar: estimacion propia, sin cotizacion."),
        ("Alianza con streamer: setup de transmision (camara + capturadora + microfono + kit de luces)", 3_000_000,
         "SUPUESTO CONSERVADOR: no hay streamer identificado ni cotizacion real. Retorno esperado es exposicion de marca/roster (cualitativo), NO ingreso garantizado -- ver memo de upside opcional en EstadoResultados."),
    ],
    "imprevistos_pct": 0.15,
    "capital_trabajo_meses": 6,
    "opex_categorias": {
        "EQUIPO / NOMINA": [
            ("CEO / Director del Sello", 3_000_000, 1.5,
             "Heredado del plan anterior (rol 'Dir. Sello', salario base + factor prestaciones), sin verificacion independiente 2025/2026."),
            ("Gerente Comercial", 1_800_000, 1.5,
             "Heredado del rol mas cercano del plan anterior (Asistente de Ventas); no hay cifra propia para 'gerente comercial' de sello."),
            ("Social Media Manager (curaduria, part-time)", 2_000_000, 1.0,
             "Cifra ya representa costo mensual total (no se desagrega base/prestaciones). Dentro del rango VERIFICADO 2025 ($1.8M-$3.5M COP/mes, Computrabajo/El Empleo), extremo bajo por ser rol part-time de curaduria."),
            ("Comunicadora / Estrategia de Contenido", 2_000_000, 1.0,
             "Cifra ya es costo total. Supuesto a validar: ajustada por analogia al Social Media Manager, sin cotizacion propia independiente."),
            ("Filmmaker / Editor con IA (planta fija)", 2_200_000, 1.0,
             "Cifra ya es costo total. CAMBIO DE ESTRUCTURA confirmado por el usuario: ya no es freelance por proyecto, pasa a planta fija por acceso a la metodologia de marca formalizada (ver plan_negocios_sello.md Secciones 3.2, 6.1 y 7). Supuesto a validar: referencia salarial propia junior-mid, sin cotizacion dura."),
            ("Disenadora Grafica (planta fija)", 2_000_000, 1.0,
             "Cifra ya es costo total. Mismo cambio de estructura y misma razon que el Filmmaker. Supuesto a validar: referencia salarial propia junior-mid, sin cotizacion dura."),
        ],
        "ADECUACIONES Y ARRIENDO": [
            ("Arriendo (espacio que cubre oficina + estudio de grabacion + area de foto/contenido + area de streaming/transmision en vivo)", 5_000_000,
             "CORREGIDO: el gap real es que el espacio necesita caber las 4 funciones (oficina administrativa, estudio de grabacion -- CAPEX de audio ya presupuestado, area de fotografia/contenido visual, y area de streaming/transmision en vivo para el streamer aliado y conciertos virtuales). Supuesto a validar, RANGO REAL DE MERCADO $4M-$9M COP/mes en Medellin segun el usuario, dependiendo de ubicacion y tamano -- se usa $5,000,000 como punto medio razonable, no el piso de $2M que subestimaba el espacio necesario."),
        ],
        "HERRAMIENTAS Y TECNOLOGIA": [
            ("Notion (gestion de proyectos y documentacion)", 67_200, "Supuesto: plan Team, ~2 puestos, sin cotizacion exacta."),
            ("WhatsApp Business (comunicacion interna/artistas)", 0, "Uso basico, sin costo de API en este volumen."),
            ("Make (automatizacion Maquina de Captacion)", 37_800, "Supuesto: plan de entrada, sin cotizacion exacta."),
            ("CapCut Pro (edicion IA del Filmmaker)", 126_000, "USD $30/mes, convertido a la tasa de referencia de este modelo."),
            ("Canva Pro (diseno de la Disenadora)", 54_600, "USD $13/mes, convertido a la tasa de referencia de este modelo."),
            ("Google Drive (repositorio de audio/video/diseno)", 42_000, "Supuesto: plan de almacenamiento ampliado, sin cotizacion exacta."),
            ("Buffer / software misceláneo", 72_400, "Remanente del presupuesto de herramientas, sin asignar a una linea especifica."),
        ],
        "PAUTA Y PUBLICIDAD / MARKETING": [
            ("Pauta publicitaria (Meta Ads / TikTok Ads)", 1_200_000,
             "Supuesto a validar: presupuesto de pauta modesto para el catalogo propio, no el presupuesto masivo de agencia ($31.2M/mes del plan anterior)."),
            ("Marketing y contenido pago adicional", 300_000,
             "Supuesto a validar: colaboraciones puntuales, impulsos de publicaciones puntuales."),
        ],
        "OTROS / ADMINISTRATIVOS": [
            ("Contador (retainer externo)", 800_000, "Supuesto a validar: sin cotizacion real."),
            ("Administrativos y generales", 1_000_000, "Heredado/ajustado del plan anterior."),
        ],
    },
    "opex_crecimiento_anual": 0.08,
    "opex_step_up_anio": 3,
    "opex_step_up_valor_anual": 2_700_000 * 12,
    "opex_step_up_nota": "Nuevo Gerente Comercial de tiempo completo desde Año 3, segun el gatillo de escalamiento definido en el plan de negocios (>4-5 proyectos/mes sostenidos).",
    "produccion": {
        "precio_unit": 4_000_000, "cvu": 3_600_000,
        "vol_mensual_por_anio": [0, 0, 0, 0, 0],
        "nota": "SUPERADA por el modelo de Campamento de Creacion (ver 'campamento' abajo), validado con investigacion real en docs/sello_plan/investigacion_campamentos_musicales.md. La produccion para terceros ya no se vende como proyecto suelto mes a mes (ese formato no deja margen real) -- se empaqueta en camps de 12 artistas. Se deja la linea en cero (no se elimina el codigo) para trazabilidad del historial de correcciones.",
    },
    "marca_personal": {
        "precio_unit": 11_000_000, "cvu": 3_500_000,
        "vol_mensual_por_anio": [1.5, 2, 2.5, 3, 3],
        "nota": "Precio anclado en 'ARTISTA TRADICIONAL PERSONALIZADO' del plan anterior. CVU reducido fuertemente (31.8% vs 69% del plan anterior) porque el Content Engine propio sustituye al equipo creativo humano que encarecia este servicio en el modelo de agencia.",
    },
    "representacion_mercado": {
        "precio_mensual_usd_completo": 2000, "precio_mensual_usd_direccion": 1000,
        "precio_mensual_usd_blend": 1500,
        "clientes_por_anio": [1.5, 2, 3, 4, 5],
        "margen_cogs_pct": 0.05,
        "nota": "PRECIO REAL YA COTIZADO (no supuesto) -- coincide exactamente con plan_negocios_sello.md Secciones 4 y 10: 'Representacion / Entrada a Mercado', servicio de booking/representacion para artistas EXTERNOS al roster (sin inversion de catalogo ni produccion de video, a diferencia de Elite 360). Dos modalidades: Servicio completo USD $2.000/mes, Solo direccion USD $1.000/mes -- aqui se usa un blend 50/50 (USD $1.500/mes promedio) como supuesto de mezcla, no de precio. Volumen: 1-2 artistas externos simultaneos al inicio, creciendo modestamente -- supuesto a validar. Costo: el tiempo principal ya es del Gerente Comercial, YA PAGADO en OPEX -- no se duplica, solo 5% de costo incidental.",
    },
    "campamento": {
        "ingreso_por_camp": 60_000_000,
        "costo_por_camp": 18_900_000,
        "camps_por_anio": [2, 3, 3, 4, 4],
        "nota": "VALIDADO con investigacion real (docs/sello_plan/investigacion_campamentos_musicales.md): camp de 12 artistas x 3 noches, ingreso 12x$5.000.000 = $60.000.000 COP. Costos: finca 3 noches $3.500.000 (cotizacion real, Copacabana) + alimentacion ~20 personas x3 dias $5.400.000 (SUPUESTO sin fuente Medellin) + 3-6 productores/ingenieros freelance x3 dias, punto medio $5.400.000 (SUPUESTO sin fuente) + Filmmaker+Disenadora+Comunicadora 3 dias $3.600.000 (ADICIONAL al salario fijo, carga extra sobre la operacion normal) + transporte $1.000.000. Margen ~68.5%, dentro del rango validado 65-71%. Volumen: 2-4 camps/ano, NO mensual -- supuesto a validar.",
    },
    "roster_cap": 15,
    "roster_por_anio": [2, 4, 7, 11, 15],
    "roster_nota": "Tope duro de roster: maximo 15 artistas firmados en total (techo de largo plazo). Curva de crecimiento desde 1 artista actual hasta el techo a lo largo de 5 anos -- NO se asume crecimiento ilimitado. Volumen mas alla de este techo pertenece al modelo financiero separado de la plataforma SaaS.",
    "marca_360": {
        "precio_mensual_usd": 2999.99,
        "ocupacion_pct_por_anio": [0.30, 0.45, 0.55, 0.65, 0.70],
        "nota": "PRECIO REAL Y CONFIRMADO: plan 'ELITE 360 / ARTIST DEVELOPMENT 360' ya definido en el codigo de la plataforma IM Music -- USD $2,999.99/mes por artista activo del roster. Lo que SI es supuesto propio es la OCUPACION: no se asume que todo el roster paga el plan completo desde el mes 1 -- curva de llenado/retencion creciente y conservadora, a validar.",
    },
    "regalias_catalogo": {
        "gross_por_anio": [3_000_000, 5_000_000, 8_000_000, 10_000_000, 12_000_000],
        "nota": "Regalias de catalogo = retorno (via Nexus, 8% comision) de canciones/EPs/albumes en los que el sello invirtio capital propio, con % de regalia negociado caso por caso por proyecto. No automatico ni aplica a todo el roster -- oportunista, ligado a cuantos proyectos especiales se financien cada ano. Supuesto a validar.",
    },
    "youtube": {
        "vistas_mensuales_por_anio": [50_000, 100_000, 200_000, 350_000, 500_000],
        "rpm_usd": 1.5,
        "nota": "Ingreso del canal propio de YouTube (AdSense/Content ID), separado de Nexus. Supuesto a validar: RPM generico (1.5 USD/1000 vistas), vistas mensuales supuesto propio.",
    },
    "libro": {
        "ingreso_anual_por_anio": [6_000_000, 8_000_000, 10_000_000, 12_000_000, 14_000_000],
        "nota": "El libro 'Music Business Para Todos Los Humanos' SI es un producto real ya en venta en Hotmart (ES/EN/PT). El VOLUMEN de ventas proyectado es un supuesto conservador, a validar contra el dashboard real de Hotmart.",
    },
    "legal_puntual_anual": 2_000_000,
    "legal_nota": "Se elimina el retainer fijo de abogado externo: el fundador cubre la funcion legal del dia a dia. Provision puntual anual para casos de alta complejidad -- monto estimado, no cotizado.",
    "streamer_upside_por_anio": [0, 500_000, 800_000, 1_000_000, 1_200_000],
    "streamer_upside_nota": "MEMO -- NO incluido en Ingresos Totales ni en TIR/VAN. Upside opcional solo si se negocia % de ingresos del streamer -- no garantizado, cifra ilustrativa.",
    "depreciacion_anios": 5,
}

DXB = {
    "moneda": "AED",
    "fx_nota": "1 USD ~ 3.6725 AED (paridad oficial AED/USD); conversion COP->AED via USD a ~4,200 COP/USD. Cifras convertidas son MARCADORES, no cotizaciones locales.",
    "fx_usd": 3.6725,
    "tasa_descuento": 0.25,
    "tasa_impuesto_nota": "0% hasta AED 375,000 de utilidad gravable, 9% sobre el excedente (confirmado, Deloitte/FTA). En este modelo la utilidad nunca supera ese umbral.",
    "umbral_exento": 375_000,
    "tasa_impuesto": 0.09,
    "nexus_comision": 0.08,
    "capex": [
        ("Estudio (tratamiento acustico + mics + interfaz + monitores + DAW) -- convertido de Colombia", 45_906,
         "NO CONFIRMADO: no existe fuente de costo de estudio en EAU. Conversion directa de la cifra colombiana via FX."),
        ("Kit audiovisual basico -- convertido de Colombia", 16_177,
         "NO CONFIRMADO: conversion de cifra colombiana sin cotizacion de EAU."),
        ("Estacion de edicion (Filmmaker) + estacion de diseno (Disenadora) -- convertido de Colombia", 12_677,
         "CAMBIO DE ESTRUCTURA, mismo criterio que Colombia: ya no son freelance. NO CONFIRMADO: conversion via FX, sin cotizacion de EAU."),
        ("Arancel de importacion 5% CIF sobre estaciones de edicion/diseno", 634,
         "CONFIRMADO: mismo arancel general EAU de 5% CIF ya usado para el resto del equipo importado."),
        ("Equipo de oficina (2 PCs + mobiliario) -- convertido de Colombia", 9_181,
         "NO CONFIRMADO: conversion de cifra colombiana."),
        ("Arancel de importacion 5% CIF sobre equipo importado (kit audiovisual + PCs)", 1_268,
         "CONFIRMADO: arancel general EAU de 5% sobre valor CIF (u.ae)."),
        ("Licencia zona franca (IFZA, paquete mas economico sourced)", 12_900,
         "Estimacion de consultora (businesslinkuae.com), NO es tarifa oficial de gobierno."),
        ("Visas (1 inversionista + 1 empleado, ano 1)", 18_750,
         "NO CONFIRMADO: rangos de fuentes de baja confiabilidad, punto medio de cada rango."),
        ("Alianza con streamer: setup de transmision -- convertido de Colombia", 2_623,
         "SUPUESTO CONSERVADOR: no hay streamer identificado ni cotizacion real."),
        ("Comision de agencia inmobiliaria (one-time, ~10% de la renta anual de Al Quoz)", 21_000,
         "CONFIRMADO como practica comun del mercado de Dubai (comision de agencia ~10% de la renta anual, pagada una sola vez al firmar) -- calculada sobre AED 17.500/mes x12 = AED 210.000/ano x10%. Ver nota de arriendo en Supuestos_DXB para la fuente de Al Quoz."),
    ],
    "imprevistos_pct": 0.15,
    "capital_trabajo_meses": 6,
    "opex_categorias": {
        "EQUIPO / NOMINA": [
            ("CEO / Director del Sello", 12_000, 1.0,
             "Cifra ya es costo total (EAU no usa 'factor prestaciones' como Colombia). NO CONFIRMADO: sin fuente directa para este rol, posicionado por encima del rango sourced de Marketing Executive/Social Media Manager por mayor seniority."),
            ("Gerente Comercial (anclado en 'Marketing Executive')", 5_500, 1.0,
             "CONFIRMADO como rango de mercado (GulfTalent) para el rol mas cercano disponible."),
            ("Social Media Manager", 6_000, 1.0,
             "CONFIRMADO: Payscale Dubai, rango AED 5,900-6,000/mes."),
            ("Comunicadora / Estrategia de Contenido", 6_000, 1.0,
             "NO CONFIRMADO: mismo rango que el Social Media Manager (sourced), aplicado por analogia."),
            ("Filmmaker / Editor con IA (planta fija)", 6_500, 1.0,
             "CAMBIO DE ESTRUCTURA, mismo criterio que Colombia: ya no es freelance. NO CONFIRMADO: posicionado por analogia al rango sourced de Social Media Manager."),
            ("Disenadora Grafica (planta fija)", 6_000, 1.0,
             "Mismo cambio de estructura que el Filmmaker. NO CONFIRMADO: posicionado por analogia."),
        ],
        "ADECUACIONES Y ARRIENDO": [
            ("Arriendo (Al Quoz: oficina + estudio + area de foto/contenido + area de streaming)", 17_500,
             "CORREGIDO con referencia real reciente: Al Quoz, el distrito de bodegas/estudios creativos de Dubai (galerias, estudios fotograficos, showrooms), tiene unidades de 2.100-2.700 pies2 por AED 15.800-19.200/mes, antes de IVA 5% y comision de agencia ~10% unica al firmar. Fuentes: listados Dubizzle y PropertyFinder, pisos de 2026. Se usa AED 17.500/mes como punto medio del rango real. Reemplaza el supuesto anterior de micro-unidad de 150 sqft, que no cabia oficina+estudio+foto+streaming."),
        ],
        "HERRAMIENTAS Y TECNOLOGIA": [
            ("Notion", 59, "NO CONFIRMADO: conversion directa, sin cotizacion de EAU."),
            ("WhatsApp Business", 0, "Uso basico, sin costo de API en este volumen."),
            ("Make", 33, "NO CONFIRMADO: conversion directa."),
            ("CapCut Pro (Filmmaker)", 110, "USD $30/mes convertido a AED."),
            ("Canva Pro (Disenadora)", 48, "USD $13/mes convertido a AED."),
            ("Google Drive", 37, "NO CONFIRMADO: conversion directa."),
            ("Buffer / software misceláneo", 213, "Remanente del presupuesto de herramientas."),
        ],
        "PAUTA Y PUBLICIDAD / MARKETING": [
            ("Pauta publicitaria (Meta Ads / TikTok Ads)", 1_600, "NO CONFIRMADO: sin datos de CAC/audiencia de musica latina en EAU."),
            ("Marketing y contenido pago adicional", 400, "NO CONFIRMADO: estimacion propia."),
        ],
        "OTROS / ADMINISTRATIVOS": [
            ("Contador (retainer externo)", 1_200, "NO CONFIRMADO: placeholder sin cotizacion real."),
            ("Administrativos y generales", 800, "NO CONFIRMADO: estimacion propia."),
        ],
    },
    "opex_crecimiento_anual": 0.06,
    "produccion": {
        "precio_unit": 3_500, "cvu": 3_150,
        "vol_mensual_por_anio": [1, 1.5, 2, 2.5, 3],
        "nota": "CORREGIDO, mismo criterio que Colombia: margen real bajo (10%), casi punto de equilibrio y puerta de entrada de relacion/A&R. Precio convertido de Colombia. Volumen deliberadamente mas bajo que Colombia -- supuesto de arranque conservador.",
    },
    "marca_personal": {
        "precio_unit": 9_600, "cvu": 3_050,
        "vol_mensual_por_anio": [0.5, 0.75, 1, 1.5, 2],
        "nota": "Mismo comentario que produccion: precio convertido, volumen deliberadamente conservador por falta de validacion de demanda.",
    },
    "representacion_mercado": {
        "precio_mensual_usd_completo": 2000, "precio_mensual_usd_direccion": 1000,
        "precio_mensual_usd_blend": 1500,
        "clientes_por_anio": [1.5, 2, 3, 4, 5],
        "margen_cogs_pct": 0.05,
        "nota": "MISMO precio real en USD que Colombia (no se convierte a una cifra distinta: el servicio se cotiza en USD en el caso real) -- solo se convierte a AED para el libro contable. 'Entrada a Mercado' es parte central de la tesis estrategica de Dubai (Seccion 5.2 del plan de negocios).",
    },
    "campamento": {
        "ingreso_por_camp": 48_280,
        "costo_por_camp": 50_500,
        "camps_por_anio": [0, 0, 0, 0, 0],
        "nota": "NO VIABLE al precio actual -- VALIDADO con investigacion real: convirtiendo el mismo precio colombiano a AED (~48.280), solo villa+catering para ~20 personas x3 dias ya consumen AED 49.000-52.000 (91-96% del ingreso). Se deja en CERO camps/ano explicitamente, no se inventa un precio mayor.",
    },
    "roster_cap": 15,
    "roster_por_anio": [1, 2, 3, 5, 7],
    "roster_nota": "Mismo techo estructural de 15 artistas que Colombia, pero curva de crecimiento mucho mas lenta: sin escena/relaciones locales ni validacion de demanda.",
    "marca_360": {
        "precio_mensual_usd": 2999.99,
        "ocupacion_pct_por_anio": [0.15, 0.25, 0.35, 0.45, 0.55],
        "nota": "Mismo precio real confirmado de la plataforma, convertido a AED. Ocupacion deliberadamente mas baja y mas lenta que Colombia -- supuesto propio, sin validacion de demanda local.",
    },
    "regalias_catalogo": {
        "gross_por_anio": [500, 1_000, 1_500, 2_000, 2_500],
        "nota": "Mismo concepto que Colombia, escalado muy a la baja -- sin historial ni base de catalogo local, y con EMRA sin tarifas comerciales activas hasta diciembre 2026.",
    },
    "youtube": {
        "vistas_mensuales_por_anio": [5_000, 10_000, 20_000, 30_000, 45_000],
        "rpm_usd": 1.5,
        "nota": "Vistas mucho menores que Colombia por falta de audiencia/canal establecido en la region.",
    },
    "libro": {
        "ingreso_anual_por_anio": [0, 0, 0, 0, 0],
        "nota": "Se proyecta en CERO: no hay ninguna senal de demanda del libro en EAU.",
    },
    "legal_puntual_anual": 3_000,
    "legal_nota": "Se elimina el retainer fijo de abogado externo, igual que en Colombia. Provision puntual anual ajustada al alza vs. la conversion directa de Colombia.",
    "streamer_upside_por_anio": [0, 440, 700, 875, 1_050],
    "streamer_upside_nota": "MEMO -- NO incluido en Ingresos Totales ni en TIR/VAN. Mismo concepto que Colombia, convertido via FX.",
    "depreciacion_anios": 5,
}


def opex_mes1_total(p):
    total = 0.0
    for row in p["opex_categorias"]["EQUIPO / NOMINA"]:
        total += row[1] * row[2]
    for cat in ("ADECUACIONES Y ARRIENDO", "HERRAMIENTAS Y TECNOLOGIA", "PAUTA Y PUBLICIDAD / MARKETING", "OTROS / ADMINISTRATIVOS"):
        for row in p["opex_categorias"][cat]:
            total += row[1]
    return total


def compute(p):
    n = 5
    capex_subtotal = sum(x[1] for x in p["capex"])
    imprevistos = capex_subtotal * p["imprevistos_pct"]
    capex_total = capex_subtotal + imprevistos
    opex_mes1 = opex_mes1_total(p)
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

    camp = p["campamento"]
    ing_camp = [c * camp["ingreso_por_camp"] for c in camp["camps_por_anio"]]
    cog_camp = [c * camp["costo_por_camp"] for c in camp["camps_por_anio"]]

    rm = p["representacion_mercado"]
    precio_anual_rm = rm["precio_mensual_usd_blend"] * p["fx_usd"] * 12
    ing_rm = [c * precio_anual_rm for c in rm["clientes_por_anio"]]
    cog_rm = [x * rm["margen_cogs_pct"] for x in ing_rm]

    m360 = p["marca_360"]
    precio_mensual_360 = m360["precio_mensual_usd"] * p["fx_usd"]
    roster = p["roster_por_anio"]
    ocup = m360["ocupacion_pct_por_anio"]
    ing_360 = [roster[i] * ocup[i] * precio_mensual_360 * 12 for i in range(n)]

    rc = p["regalias_catalogo"]
    reg_gross = rc["gross_por_anio"]
    reg_comision = [x * p["nexus_comision"] for x in reg_gross]

    yt = p["youtube"]
    ing_youtube = [v * yt["rpm_usd"] / 1000 * p["fx_usd"] * 12 for v in yt["vistas_mensuales_por_anio"]]

    ing_libro = p["libro"]["ingreso_anual_por_anio"]

    depre_anual = capex_total / p["depreciacion_anios"]
    tasa_imp = p["tasa_impuesto"]
    umbral = p.get("umbral_exento", 0)

    filas = []
    fc = [-nti]
    for i in range(n):
        ingresos = ing_prod[i] + ing_marca[i] + ing_camp[i] + ing_rm[i] + ing_360[i] + reg_gross[i] + ing_youtube[i] + ing_libro[i]
        cogs = cog_prod[i] + cog_marca[i] + cog_camp[i] + cog_rm[i] + reg_comision[i]
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
            ing_camp=ing_camp[i], cog_camp=cog_camp[i], camps=camp["camps_por_anio"][i],
            ing_rm=ing_rm[i], cog_rm=cog_rm[i], clientes_rm=rm["clientes_por_anio"][i],
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
# Escenario B: Medellin REDUCIDO (el fundador se radica en Dubai; Filmmaker,
# Disenadora y Comunicadora se comparten de forma remota desde la operacion
# de Dubai y dejan de ser costo fijo de Medellin; se agrega un Project
# Manager - Elite 360 para cubrir el roster ya existente).
# ---------------------------------------------------------------------------
COL_REDUCIDO = copy.deepcopy(COL)
_nomina_reducida = [
    row for row in COL_REDUCIDO["opex_categorias"]["EQUIPO / NOMINA"]
    if row[0] not in (
        "Comunicadora / Estrategia de Contenido",
        "Filmmaker / Editor con IA (planta fija)",
        "Disenadora Grafica (planta fija)",
    )
]
_nomina_reducida.append((
    "Project Manager - Elite 360 (NUEVO en este escenario)", 3_000_000, 1.0,
    "Rol citado en plan_negocios_sello.md Seccion 3.2 pero NO incluido antes en el modelo financiero base -- se agrega aqui porque el escenario reducido necesita a alguien cubriendo la entrega del roster sin el equipo creativo fijo local. Estimado nuevo, sin cotizacion."
))
COL_REDUCIDO["opex_categorias"]["EQUIPO / NOMINA"] = _nomina_reducida
COL_REDUCIDO["capex"] = [
    item for item in COL_REDUCIDO["capex"] if "Estacion de edicion" not in item[0]
]
col_reducido = compute(COL_REDUCIDO)

# Bloque Dubai Lean: tomado de un archivo YA EXISTENTE y separado
# (modelo_financiero_sello_dubai_lean.xlsx / _notas.md), no reconstruido aqui.
# Solo Anos 1, 3 y 5 estan documentados en ese resumen.
DUBAI_LEAN = {
    "nti": 168_787,
    "ebitda": {1: -123_561, 3: 158_515, 5: 374_674},
    "utilidad_neta": {5: 359_997},
    "van": 35_292,
    "tir": 0.291,
    "nota": "Tomado de modelo_financiero_sello_dubai_lean_notas.md (archivo separado ya existente, NO reconstruido en este script). Solo Anos 1, 3 y 5 estan documentados en ese resumen -- Anos 2 y 4 no se citan ahi. Ver modelo_financiero_sello_dubai_lean.xlsx para el detalle linea por linea. Ese modelo asume que el fundador SI se radica en Dubai, con escalamiento por fases -- aqui se usa solo como el bloque de costos/ingresos de la operacion de Dubai dentro del Escenario A, para comparar.",
}

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


def mset(ws, row, col_, value, bold=False, flag=False, fmt=MONEY_FMT):
    c = ws.cell(row=row, column=col_, value=round(value) if isinstance(value, float) else value)
    if fmt:
        c.number_format = fmt
    if bold:
        c.font = FONT_BOLD
    if flag:
        c.font = FONT_FLAG
    return c


CATEGORIAS_OPEX = ["ADECUACIONES Y ARRIENDO", "HERRAMIENTAS Y TECNOLOGIA", "PAUTA Y PUBLICIDAD / MARKETING", "OTROS / ADMINISTRATIVOS"]


def sheet_supuestos(name, p, results):
    ws = wb.create_sheet(f"Supuestos_{name}")
    style_title(ws, f"SUPUESTOS -- {name}", span=4)
    ws.cell(row=2, column=1, value=p["fx_nota"]).font = FONT_FLAG
    row = 4
    style_header_row(ws, row, ["Rubro", "Valor", f"Unidad ({p['moneda']})", "Fuente / Supuesto a validar"])
    row += 1
    ws.cell(row=row, column=1, value="-- CAPEX --").font = FONT_SECTION
    row += 1
    for label, val, nota in p["capex"]:
        ws.cell(row=row, column=1, value="CAPEX: " + label)
        mset(ws, row, 2, val)
        ws.cell(row=row, column=3, value=p["moneda"])
        c = ws.cell(row=row, column=4, value=nota)
        if "NO CONFIRMADO" in nota or "Supuesto a validar" in nota or "SUPUESTO" in nota:
            c.font = FONT_FLAG
        row += 1
    row += 1
    ws.cell(row=row, column=1, value="-- OPEX: EQUIPO / NOMINA (Puesto, Salario Base, Factor Prestaciones, Costo Empresa) --").font = FONT_SECTION
    row += 1
    style_header_row(ws, row, ["Puesto", "Salario Base", "Factor Prest.", "Costo Empresa Mensual"])
    row += 1
    for puesto, base, factor, nota in p["opex_categorias"]["EQUIPO / NOMINA"]:
        ws.cell(row=row, column=1, value=puesto)
        mset(ws, row, 2, base)
        ws.cell(row=row, column=3, value=factor)
        mset(ws, row, 4, base * factor)
        row += 1
    row += 1
    for cat in CATEGORIAS_OPEX:
        ws.cell(row=row, column=1, value=f"-- OPEX: {cat} --").font = FONT_SECTION
        row += 1
        for label, val, nota in p["opex_categorias"][cat]:
            ws.cell(row=row, column=1, value=label)
            mset(ws, row, 2, val)
            ws.cell(row=row, column=3, value=p["moneda"] + "/mes")
            c = ws.cell(row=row, column=4, value=nota)
            if "NO CONFIRMADO" in nota or "Supuesto" in nota:
                c.font = FONT_FLAG
            row += 1
        row += 1
    for key in ["produccion", "marca_personal"]:
        cfg = p[key]
        ws.cell(row=row, column=1, value=f"Ingreso {key}: precio unitario")
        mset(ws, row, 2, cfg["precio_unit"])
        ws.cell(row=row, column=3, value=p["moneda"])
        ws.cell(row=row, column=4, value=cfg["nota"]).font = FONT_FLAG
        row += 1
        ws.cell(row=row, column=1, value=f"Ingreso {key}: volumen mensual por ano")
        ws.cell(row=row, column=2, value=str(cfg["vol_mensual_por_anio"]))
        row += 1
    camp = p["campamento"]
    ws.cell(row=row, column=1, value="Campamento de Creacion: ingreso y costo por camp, # camps/ano")
    ws.cell(row=row, column=2, value=f"ingreso={camp['ingreso_por_camp']} / costo={camp['costo_por_camp']} / camps={camp['camps_por_anio']}")
    ws.cell(row=row, column=4, value=camp["nota"]).font = FONT_FLAG
    row += 1
    rm = p["representacion_mercado"]
    ws.cell(row=row, column=1, value="Representacion/Entrada a Mercado: precios USD (completo/direccion/blend), clientes/ano")
    ws.cell(row=row, column=2, value=f"completo=${rm['precio_mensual_usd_completo']} / direccion=${rm['precio_mensual_usd_direccion']} / blend=${rm['precio_mensual_usd_blend']} / clientes={rm['clientes_por_anio']}")
    ws.cell(row=row, column=4, value=rm["nota"]).font = FONT_FLAG
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
    mset(ws, row, 2, p["legal_puntual_anual"])
    ws.cell(row=row, column=4, value=p["legal_nota"]).font = FONT_FLAG
    row += 1
    ws.cell(row=row, column=1, value="Comision Nexus sobre regalias de catalogo")
    ws.cell(row=row, column=2, value=p["nexus_comision"]).number_format = PCT_FMT
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
    ws.cell(row=row, column=2, value=p["tasa_descuento"]).number_format = PCT_FMT
    row += 1
    autosize(ws, [48, 20, 16, 80])
    ws.freeze_panes = "A5"


def sheet_capex(name, p, results):
    ws = wb.create_sheet(f"CAPEX_{name}")
    style_title(ws, f"CAPEX -- {name}", span=3)
    row = 3
    style_header_row(ws, row, ["Rubro", f"Valor ({p['moneda']})", "Nota"])
    row += 1
    for label, val, nota in p["capex"]:
        ws.cell(row=row, column=1, value=label)
        mset(ws, row, 2, val)
        ws.cell(row=row, column=3, value=f"Ver Supuestos_{name}")
        row += 1
    mset(ws, row, 1, "SUBTOTAL CAPEX", fmt=None, bold=True)
    mset(ws, row, 2, results["capex_subtotal"], bold=True)
    row += 1
    ws.cell(row=row, column=1, value=f"Imprevistos ({p['imprevistos_pct']:.0%})")
    mset(ws, row, 2, results["imprevistos"])
    row += 1
    mset(ws, row, 1, "TOTAL CAPEX CON IMPREVISTOS", fmt=None, bold=True)
    mset(ws, row, 2, results["capex_total"], bold=True)
    row += 2
    ws.cell(row=row, column=1, value=f"Capital de trabajo ({p['capital_trabajo_meses']} meses de OPEX)")
    mset(ws, row, 2, results["capital_trabajo"])
    row += 1
    mset(ws, row, 1, "NECESIDAD TOTAL DE INVERSION (NTI)", fmt=None, bold=True)
    mset(ws, row, 2, results["nti"], bold=True)
    autosize(ws, [58, 20, 24])


def sheet_opex(name, p, results):
    ws = wb.create_sheet(f"OPEX_{name}")
    style_title(ws, f"OPEX MENSUAL (ANO 1), POR BLOQUE -- {name}", span=3)
    row = 3
    style_header_row(ws, row, ["Puesto", f"Costo Empresa Mensual ({p['moneda']})", "Nota"])
    row += 1
    ws.cell(row=row, column=1, value="EQUIPO / NOMINA").font = FONT_SECTION
    row += 1
    style_header_row(ws, row, ["Puesto", "Salario Base", "Factor Prest.", "Costo Empresa"])
    row += 1
    subtotal_nomina = 0
    for puesto, base, factor, nota in p["opex_categorias"]["EQUIPO / NOMINA"]:
        ws.cell(row=row, column=1, value=puesto)
        mset(ws, row, 2, base)
        ws.cell(row=row, column=3, value=factor)
        costo = base * factor
        mset(ws, row, 4, costo)
        subtotal_nomina += costo
        row += 1
    ws.cell(row=row, column=1, value=f"Subtotal EQUIPO / NOMINA").font = FONT_BOLD
    ws.cell(row=row, column=1).fill = FILL_SUBTOTAL
    mset(ws, row, 4, subtotal_nomina, bold=True)
    ws.cell(row=row, column=4).fill = FILL_SUBTOTAL
    row += 2

    subtotales = {"EQUIPO / NOMINA": subtotal_nomina}
    for cat in CATEGORIAS_OPEX:
        ws.cell(row=row, column=1, value=cat).font = FONT_SECTION
        row += 1
        style_header_row(ws, row, ["Rubro", f"Costo Mensual ({p['moneda']})", "Nota"])
        row += 1
        subtotal = 0
        for label, val, nota in p["opex_categorias"][cat]:
            ws.cell(row=row, column=1, value=label)
            mset(ws, row, 2, val)
            ws.cell(row=row, column=3, value=f"Ver Supuestos_{name}")
            subtotal += val
            row += 1
        ws.cell(row=row, column=1, value=f"Subtotal {cat}").font = FONT_BOLD
        ws.cell(row=row, column=1).fill = FILL_SUBTOTAL
        mset(ws, row, 2, subtotal, bold=True)
        ws.cell(row=row, column=2).fill = FILL_SUBTOTAL
        subtotales[cat] = subtotal
        row += 2

    mset(ws, row, 1, "TOTAL OPEX MENSUAL (suma de subtotales)", fmt=None, bold=True)
    mset(ws, row, 2, results["opex_mes1"], bold=True)
    row += 1
    ws.cell(row=row, column=1, value="  (= " + " + ".join(f"{k}: {round(v):,}" for k, v in subtotales.items()) + ")").font = Font(italic=True, size=8)
    row += 2
    style_header_row(ws, row, ["Ano", "OPEX anual (con crecimiento + provision legal puntual)"])
    row += 1
    for i, v in enumerate(results["opex_anual"], start=1):
        ws.cell(row=row, column=1, value=f"Ano {i}")
        mset(ws, row, 2, v)
        row += 1
    autosize(ws, [48, 20, 20, 24])


def sheet_resultados(name, p, results):
    ws = wb.create_sheet(f"EstadoResultados_{name}")
    style_title(ws, f"ESTADO DE RESULTADOS PROYECTADO 5 ANOS -- {name}", span=6)
    row = 3
    labels = [
        ("Ingresos -- Produccion musical a terceros (clientes externos)", "ing_prod"),
        ("Ingresos -- Desarrollo de marca personal (clientes externos)", "ing_marca"),
        ("Ingresos -- Campamento de Creacion / turismo artistico", "ing_camp"),
        ("Ingresos -- Representacion / Entrada a Mercado (clientes externos)", "ing_rm"),
        ("Ingresos -- Marca 360 (roster, USD $2,999.99/mes x ocupacion)", "ing_360"),
        ("Ingresos -- Regalias de catalogo (proyectos especiales, bruto)", "reg_gross"),
        ("Ingresos -- YouTube propio (AdSense/Content ID)", "ing_youtube"),
        ("Ingresos -- Libro 'Music Business Para Todos Los Humanos'", "ing_libro"),
        ("INGRESOS TOTALES", "ingresos"),
        ("(-) COGS produccion", "cog_prod"),
        ("(-) COGS marca personal", "cog_marca"),
        ("(-) COGS campamento (finca, catering, produccion freelance, transporte)", "cog_camp"),
        ("(-) COGS representacion/entrada a mercado (5% incidental)", "cog_rm"),
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
    ws.cell(row=row, column=1, value="Memo -- campamentos de creacion realizados en el ano")
    for i, fila in enumerate(results["filas"]):
        ws.cell(row=row, column=2 + i, value=fila["camps"])
    row += 1
    ws.cell(row=row, column=1, value="Memo -- clientes Representacion/Entrada a Mercado")
    for i, fila in enumerate(results["filas"]):
        ws.cell(row=row, column=2 + i, value=fila["clientes_rm"])
    row += 1
    ws.cell(row=row, column=1, value="Memo -- artistas en roster (firmados)")
    for i, fila in enumerate(results["filas"]):
        ws.cell(row=row, column=2 + i, value=fila["roster_size"])
    row += 1
    ws.cell(row=row, column=1, value="Memo -- % ocupacion plan Marca 360")
    for i, fila in enumerate(results["filas"]):
        ws.cell(row=row, column=2 + i, value=fila["ocupacion"]).number_format = PCT_FMT
    row += 1
    c = ws.cell(row=row, column=1, value="Memo -- upside opcional streamer (NO incluido en Ingresos Totales, no garantizado)")
    c.font = FONT_FLAG
    for i, fila in enumerate(results["filas"]):
        mset(ws, row, 2 + i, fila["streamer_upside_memo"], flag=True)
    row += 1
    bold_rows = {"INGRESOS TOTALES", "UTILIDAD BRUTA", "EBITDA", "UTILIDAD NETA"}
    for label, key in labels:
        ws.cell(row=row, column=1, value=label)
        if label in bold_rows:
            ws.cell(row=row, column=1).font = FONT_BOLD
        for i, fila in enumerate(results["filas"]):
            mset(ws, row, 2 + i, fila[key], bold=(label in bold_rows))
        row += 1
    autosize(ws, [48, 18, 18, 18, 18, 18])


def sheet_flujo(name, p, results):
    ws = wb.create_sheet(f"FlujoCaja_TIR_VAN_{name}")
    style_title(ws, f"FLUJO DE CAJA / TIR / VAN -- {name}", span=7)
    row = 3
    style_header_row(ws, row, ["Ano 0"] + [f"Ano {i}" for i in range(1, 6)])
    row += 1
    ws.cell(row=row, column=1, value="Flujo de caja neto")
    for i, v in enumerate(results["fc"]):
        mset(ws, row, 2 + i, v)
    row += 3
    mset(ws, row, 1, "NTI (inversion inicial, Ano 0)", fmt=None, bold=True)
    mset(ws, row, 2, results["nti"], bold=True)
    row += 1
    ws.cell(row=row, column=1, value="Tasa de descuento usada")
    ws.cell(row=row, column=2, value=p["tasa_descuento"]).number_format = PCT_FMT
    row += 1
    mset(ws, row, 1, "VAN (NPV)", fmt=None, bold=True)
    mset(ws, row, 2, results["van"], bold=True)
    row += 1
    mset(ws, row, 1, "TIR (IRR)", fmt=None, bold=True)
    if results["tir"] is not None:
        c = ws.cell(row=row, column=2, value=results["tir"])
        c.number_format = PCT_FMT
        c.font = FONT_BOLD
    else:
        c = ws.cell(row=row, column=2, value="NO CALCULABLE -- todos los flujos de caja son negativos en el horizonte de 5 anos bajo estos supuestos")
        c.font = FONT_FLAG
    autosize(ws, [45, 18, 18, 18, 18, 18, 18])


def sheet_resumen():
    ws = wb.create_sheet("RESUMEN_COMPARATIVO", 0)
    style_title(ws, "IM MUSIC -- SELLO: RESUMEN COMPARATIVO MEDELLIN vs DUBAI", span=3)
    ws.cell(row=2, column=1, value="Cifras reales, conservadoras, con cada supuesto no verificado senalado en las pestanas Supuestos_COL / Supuestos_DXB. Este NO es el modelo agresivo del plan anterior. Ver tambien la pestana COMPARATIVO_ESCENARIOS para Escenario A (base Medellin) vs Escenario B (base Dubai).").font = FONT_FLAG
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
        mset(ws, row, 2, v_col)
        mset(ws, row, 3, v_dxb)
        row += 1
    ws.cell(row=row, column=1, value="TIR (IRR)")
    if col["tir"]:
        ws.cell(row=row, column=2, value=col["tir"]).number_format = PCT_FMT
    else:
        ws.cell(row=row, column=2, value="N/A")
    if dxb["tir"]:
        ws.cell(row=row, column=3, value=dxb["tir"]).number_format = PCT_FMT
    else:
        ws.cell(row=row, column=3, value="NO CALCULABLE (flujos siempre negativos)")
    row += 2
    ws.cell(row=row, column=1, value="Lectura honesta: el ingreso 'Marca 360' usa un PRECIO REAL confirmado de la plataforma (USD $2,999.99/mes por artista) -- pero todo el resultado depende de poder cobrarlo de forma sostenida a artistas emergentes/boutique, algo que NO esta validado comercialmente (ver ocupacion en Supuestos_COL/DXB). Dubai no cierra el caso de negocio en 5 anos bajo el modelo completo (equipo fijo desde el dia 1) -- ver COMPARATIVO_ESCENARIOS para alternativas.").font = FONT_FLAG
    autosize(ws, [42, 22, 30])


def sheet_comparativo_escenarios():
    ws = wb.create_sheet("COMPARATIVO_ESCENARIOS", 1)
    style_title(ws, "COMPARATIVO: ESCENARIO A (BASE MEDELLIN) vs ESCENARIO B (BASE DUBAI)", span=7)
    ws.cell(row=2, column=1, value="La decision real no es 'Medellin O Dubai' en abstracto -- es donde se radica el fundador. Esto muestra los 4 bloques por separado y como se combinan en cada escenario, sin recomendar cual elegir.").font = FONT_FLAG
    row = 4

    ws.cell(row=row, column=1, value="BLOQUE 1 -- Medellin COMPLETO (equipo fijo local, como esta hoy)").font = FONT_SECTION
    row += 1
    style_header_row(ws, row, ["Indicador", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5", "VAN / TIR"])
    row += 1
    ws.cell(row=row, column=1, value="EBITDA (COP)")
    for i, f in enumerate(col["filas"]):
        mset(ws, row, 2 + i, f["ebitda"])
    mset(ws, row, 7, col["van"], bold=True)
    row += 1
    ws.cell(row=row, column=1, value="Utilidad Neta (COP)")
    for i, f in enumerate(col["filas"]):
        mset(ws, row, 2 + i, f["utilidad_neta"])
    ws.cell(row=row, column=7, value=f"TIR: {col['tir']*100:.1f}%" if col["tir"] else "TIR: N/A")
    row += 1
    ws.cell(row=row, column=1, value=f"NTI: {round(col['nti']):,} COP").font = Font(italic=True)
    row += 2

    ws.cell(row=row, column=1, value="BLOQUE 2 -- Dubai COMPLETO (equipo fijo local, como esta hoy)").font = FONT_SECTION
    row += 1
    style_header_row(ws, row, ["Indicador", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5", "VAN / TIR"])
    row += 1
    ws.cell(row=row, column=1, value="EBITDA (AED)")
    for i, f in enumerate(dxb["filas"]):
        mset(ws, row, 2 + i, f["ebitda"])
    mset(ws, row, 7, dxb["van"], bold=True)
    row += 1
    ws.cell(row=row, column=1, value="Utilidad Neta (AED)")
    for i, f in enumerate(dxb["filas"]):
        mset(ws, row, 2 + i, f["utilidad_neta"])
    ws.cell(row=row, column=7, value="TIR: NO CALCULABLE" if not dxb["tir"] else f"TIR: {dxb['tir']*100:.1f}%")
    row += 1
    ws.cell(row=row, column=1, value=f"NTI: {round(dxb['nti']):,} AED").font = Font(italic=True)
    row += 2

    ws.cell(row=row, column=1, value="BLOQUE 3 -- Dubai LEAN / por fases (archivo separado ya existente, fundador radicado alla con escalamiento gradual)").font = FONT_SECTION
    row += 1
    style_header_row(ws, row, ["Indicador", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5", "VAN / TIR"])
    row += 1
    ws.cell(row=row, column=1, value="EBITDA (AED)")
    mset(ws, row, 2, DUBAI_LEAN["ebitda"][1])
    ws.cell(row=row, column=3, value="sin dato")
    mset(ws, row, 4, DUBAI_LEAN["ebitda"][3])
    ws.cell(row=row, column=5, value="sin dato")
    mset(ws, row, 6, DUBAI_LEAN["ebitda"][5])
    mset(ws, row, 7, DUBAI_LEAN["van"], bold=True)
    row += 1
    ws.cell(row=row, column=1, value="Utilidad Neta (AED)")
    ws.cell(row=row, column=2, value="sin dato")
    ws.cell(row=row, column=3, value="sin dato")
    ws.cell(row=row, column=4, value="sin dato")
    ws.cell(row=row, column=5, value="sin dato")
    mset(ws, row, 6, DUBAI_LEAN["utilidad_neta"][5])
    ws.cell(row=row, column=7, value=f"TIR: {DUBAI_LEAN['tir']*100:.1f}%")
    row += 1
    ws.cell(row=row, column=1, value=f"NTI: {DUBAI_LEAN['nti']:,} AED").font = Font(italic=True)
    row += 1
    ws.cell(row=row, column=1, value=DUBAI_LEAN["nota"]).font = FONT_FLAG
    row += 2

    ws.cell(row=row, column=1, value="BLOQUE 4 -- Medellin REDUCIDO (fundador radicado en Dubai; Comunicadora/Filmmaker/Disenadora se comparten remoto desde Dubai, se agrega Project Manager local)").font = FONT_SECTION
    row += 1
    style_header_row(ws, row, ["Indicador", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5", "VAN / TIR"])
    row += 1
    ws.cell(row=row, column=1, value="EBITDA (COP)")
    for i, f in enumerate(col_reducido["filas"]):
        mset(ws, row, 2 + i, f["ebitda"])
    mset(ws, row, 7, col_reducido["van"], bold=True)
    row += 1
    ws.cell(row=row, column=1, value="Utilidad Neta (COP)")
    for i, f in enumerate(col_reducido["filas"]):
        mset(ws, row, 2 + i, f["utilidad_neta"])
    ws.cell(row=row, column=7, value=f"TIR: {col_reducido['tir']*100:.1f}%" if col_reducido["tir"] else "TIR: N/A")
    row += 1
    ws.cell(row=row, column=1, value=f"NTI: {round(col_reducido['nti']):,} COP").font = Font(italic=True)
    row += 1
    ws.cell(row=row, column=1, value="El ingreso (Marca 360, campamento, representacion, YouTube, libro, regalias) se asume IGUAL al Bloque 1 -- el catalogo/roster no desaparece por mudarse el fundador, solo cambia el equipo LOCAL fijo. El rol 'Project Manager' es nuevo en este escenario, no existia en el modelo base, y su costo es un supuesto propio sin cotizacion.").font = FONT_FLAG
    row += 2

    ws.cell(row=row, column=1, value="ESCENARIO A -- Base Medellin (Bloque 1 + Bloque 3)").font = FONT_SECTION
    row += 1
    style_header_row(ws, row, ["Indicador", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5", "Nota"])
    row += 1
    ws.cell(row=row, column=1, value="EBITDA combinado (dos monedas, NO se suman directamente)")
    ws.cell(row=row, column=2, value=f"{round(col['filas'][0]['ebitda']):,} COP + {round(DUBAI_LEAN['ebitda'][1]):,} AED")
    ws.cell(row=row, column=3, value=f"{round(col['filas'][1]['ebitda']):,} COP + sin dato AED")
    ws.cell(row=row, column=4, value=f"{round(col['filas'][2]['ebitda']):,} COP + {round(DUBAI_LEAN['ebitda'][3]):,} AED")
    ws.cell(row=row, column=5, value=f"{round(col['filas'][3]['ebitda']):,} COP + sin dato AED")
    ws.cell(row=row, column=6, value=f"{round(col['filas'][4]['ebitda']):,} COP + {round(DUBAI_LEAN['ebitda'][5]):,} AED")
    row += 1
    ws.cell(row=row, column=1, value="NTI combinado (NO se suma entre monedas)")
    ws.cell(row=row, column=2, value=f"{round(col['nti']):,} COP + {DUBAI_LEAN['nti']:,} AED")
    row += 1
    ws.cell(row=row, column=1, value="VAN y TIR se muestran por bloque (tasas de descuento distintas, 30% vs 25% -- sumarlos directamente no es correcto): Medellin VAN $" + f"{round(col['van']):,} COP (TIR {col['tir']*100:.1f}%)" if col["tir"] else "" ).font = Font(italic=True)
    row += 1
    ws.cell(row=row, column=1, value=f"Dubai Lean VAN AED {DUBAI_LEAN['van']:,} (TIR {DUBAI_LEAN['tir']*100:.1f}%)").font = Font(italic=True)
    row += 2

    ws.cell(row=row, column=1, value="ESCENARIO B -- Base Dubai (Bloque 2 + Bloque 4)").font = FONT_SECTION
    row += 1
    style_header_row(ws, row, ["Indicador", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5", "Nota"])
    row += 1
    ws.cell(row=row, column=1, value="EBITDA combinado (dos monedas, NO se suman directamente)")
    for i in range(5):
        ws.cell(row=row, column=2 + i, value=f"{round(col_reducido['filas'][i]['ebitda']):,} COP + {round(dxb['filas'][i]['ebitda']):,} AED")
    row += 1
    ws.cell(row=row, column=1, value="Utilidad Neta combinada (dos monedas, NO se suman directamente)")
    for i in range(5):
        ws.cell(row=row, column=2 + i, value=f"{round(col_reducido['filas'][i]['utilidad_neta']):,} COP + {round(dxb['filas'][i]['utilidad_neta']):,} AED")
    row += 1
    ws.cell(row=row, column=1, value="NTI combinado (NO se suma entre monedas)")
    ws.cell(row=row, column=2, value=f"{round(col_reducido['nti']):,} COP + {round(dxb['nti']):,} AED")
    row += 1
    ws.cell(row=row, column=1, value=f"Medellin reducido VAN $" + f"{round(col_reducido['van']):,} COP (TIR {col_reducido['tir']*100:.1f}%)" if col_reducido["tir"] else "N/A").font = Font(italic=True)
    row += 1
    ws.cell(row=row, column=1, value=f"Dubai completo VAN AED {round(dxb['van']):,} (TIR NO CALCULABLE)" if not dxb["tir"] else "").font = Font(italic=True)
    row += 2

    ws.cell(row=row, column=1, value="Nota metodologica: no se combina VAN/TIR entre bloques en monedas o tasas de descuento distintas en una sola cifra -- eso seria una mezcla matematicamente cuestionable. Se muestran EBITDA/Utilidad Neta nominal por ano (sumas validas dentro de cada ano, en sus propias monedas) y VAN/TIR por bloque, para que la comparacion sea transparente, no una sola cifra artificialmente consolidada.").font = FONT_FLAG
    autosize(ws, [55, 24, 24, 24, 24, 24, 24])


sheet_resumen()
sheet_comparativo_escenarios()
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
print("Sheets:", wb.sheetnames)
print()
print("=== COLOMBIA (completo) ===")
print("NTI:", round(col["nti"]))
for f in col["filas"]:
    print(f"Ano {f['ano']}: Ingresos={round(f['ingresos'])} EBITDA={round(f['ebitda'])} UtilNeta={round(f['utilidad_neta'])}")
print("VAN:", round(col["van"]), "TIR:", col["tir"])
print()
print("=== COLOMBIA (reducido, Escenario B) ===")
print("NTI:", round(col_reducido["nti"]))
for f in col_reducido["filas"]:
    print(f"Ano {f['ano']}: Ingresos={round(f['ingresos'])} EBITDA={round(f['ebitda'])} UtilNeta={round(f['utilidad_neta'])}")
print("VAN:", round(col_reducido["van"]), "TIR:", col_reducido["tir"])
print()
print("=== DUBAI (completo) ===")
print("NTI:", round(dxb["nti"]))
for f in dxb["filas"]:
    print(f"Ano {f['ano']}: Ingresos={round(f['ingresos'])} EBITDA={round(f['ebitda'])} UtilNeta={round(f['utilidad_neta'])}")
print("VAN:", round(dxb["van"]), "TIR:", dxb["tir"])
