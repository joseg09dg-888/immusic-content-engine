"""Genera docs/saas_plan/modelo_financiero_saas.xlsx — modelo financiero
realista (pre-lanzamiento, sin usuarios reales) para 'IM MUSIC - Elite
Artist Platform', con los 3 planes REALES definidos en el producto:
Basico Distribucion ($19.99/mes), Pro Crecimiento ($149.99/mes) y
Elite 360 Artist Development ($2,999.99/mes, tope duro 12-15 clientes)."""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "saas_plan" / "modelo_financiero_saas.xlsx"
OUT.parent.mkdir(parents=True, exist_ok=True)

VIOLETA = "FF5E17EB"
ROJO = "FFB00020"

wb = Workbook()
wb.remove(wb.active)


def style_header(ws, row, n_cols):
    for c in range(1, n_cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=VIOLETA)


def write_table(ws, start_row, headers, rows, col_widths=None):
    for j, h in enumerate(headers, start=1):
        ws.cell(row=start_row, column=j, value=h)
    style_header(ws, start_row, len(headers))
    r = start_row + 1
    for row in rows:
        for j, val in enumerate(row, start=1):
            ws.cell(row=r, column=j, value=val)
        r += 1
    if col_widths:
        for j, w in enumerate(col_widths, start=1):
            ws.column_dimensions[get_column_letter(j)].width = w
    return r


years = ["Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]

# ---------------------------------------------------------------
# PLANES REALES (corregidos por el coordinador — reemplazan la
# escalera inventada $19.99/$34.99/$59.99/$149.99 anual)
# ---------------------------------------------------------------
PRICE_BASICO_MES = 19.99
PRICE_PRO_MES = 149.99
PRICE_ELITE_MES = 2999.99

price_basico_ano = round(PRICE_BASICO_MES * 12, 2)
price_pro_ano = round(PRICE_PRO_MES * 12, 2)
price_elite_ano = round(PRICE_ELITE_MES * 12, 2)

# Suscriptores self-service (Básico + Pro), curva conservadora de modelado
# (sin datos reales de conversión), mezcla 85% Básico / 15% Pro
total_selfservice = [50, 300, 1200, 3500, 8000]
basico_subs = [round(t * 0.85) for t in total_selfservice]
pro_subs = [t - b for t, b in zip(total_selfservice, basico_subs)]

# Élite 360 — TOPE DURO de 12-15 clientes simultáneos (capacidad humana,
# no un SaaS escalable). Ramp conservador hasta el tope en Año 4-5.
# Élite 360 NO se modela aquí — se vende a través de la plataforma pero su
# ingreso y el costo del equipo que lo entrega (Project Manager, management)
# se contabilizan ÚNICAMENTE en docs/sello_plan/modelo_financiero_sello.xlsx,
# para no duplicar ese ingreso en los dos financieros.

rev_basico = [round(s * price_basico_ano, 2) for s in basico_subs]
rev_pro = [round(s * price_pro_ano, 2) for s in pro_subs]
total_rev = [round(a + b, 2) for a, b in zip(rev_basico, rev_pro)]

# ---------------------------------------------------------------
# 1. SUPUESTOS
# ---------------------------------------------------------------
ws = wb.create_sheet("Supuestos")
ws.cell(row=1, column=1, value="MODELO FINANCIERO — IM MUSIC ELITE ARTIST PLATFORM (SaaS)").font = Font(bold=True, size=14, color=VIOLETA)
ws.cell(row=2, column=1, value="Plataforma pre-lanzamiento (backend/frontend funcional, $0 usuarios de pago reales). Todo supuesto de crecimiento/conversión/churn es una estimación de modelado, NO un dato de mercado.")
ws.cell(row=2, column=1).alignment = Alignment(wrap_text=True)

rows = [
    ["Plan Básico — Distribución", f"${PRICE_BASICO_MES}/mes (${price_basico_ano}/año)", "Precio REAL ya definido en el producto. Autoservicio, escala sin límite técnico."],
    ["Plan Pro — Crecimiento", f"${PRICE_PRO_MES}/mes (${price_pro_ano}/año)", "Precio REAL ya definido en el producto. Autoservicio + marketing con IA, escala sin límite técnico."],
    ["Plan Élite 360 — Artist Development", f"${PRICE_ELITE_MES}/mes (${price_elite_ano}/año) — EXCLUIDO de este modelo", "Existe y se vende A TRAVÉS de esta plataforma, pero su ingreso y el costo del equipo que lo entrega (Project Manager, management, desarrollo artístico) se contabilizan ÚNICAMENTE en docs/sello_plan/modelo_financiero_sello.xlsx — RESOLUCIÓN FINAL del riesgo de doble conteo: este financiero de la plataforma SaaS queda SOLO con Básico + Pro."],
    ["⚠ Riesgo de precio vs. competencia (Básico/Pro)", "Básico/Pro cobran POR MES lo que DistroKid (~$19.99-89.99/año) y TuneCore (~$9.99-49.99/año) cobran POR AÑO", "Esto es ~5-10x más caro que la distribución DIY estándar del mercado (comparación de conocimiento general, no verificada con tarifas vigentes en esta sesión). La curva de adopción modelada abajo es OPTIMISTA si el mercado percibe el precio como fuera de rango — ver hoja Sensibilidad."],
    ["⚠ RIESGO DE DOBLE CONTEO — COSTO", "Equipo de Élite 360 (PM dedicado + desarrollo artístico) NO está presupuestado en este modelo", "Ese costo de personal YA se modela en el Modelo Financiero IM Music — Sello (mismo equipo, mismos artistas). Aquí solo se incluye el ingreso de Élite 360 y el equipo de INGENIERÍA de la plataforma (no el equipo de servicio al artista). Si se suman ambos modelos sin ajustar, el costo de ese equipo quedaría sin contar en ningún lado — o contado dos veces si alguien lo agrega aquí también."],
    ["✅ DOBLE CONTEO DE INGRESO — RESUELTO", "Élite 360 se excluyó por completo de este modelo", "El ingreso de Élite 360 y el costo del equipo que lo entrega viven ÚNICAMENTE en docs/sello_plan/modelo_financiero_sello.xlsx. Este modelo de la plataforma SaaS queda SOLO con Básico + Pro, ambos de autoservicio puro, sin equipo humano dedicado por cliente."],
    ["Mezcla Básico/Pro en la base de autoservicio", "85% / 15%", "SUPUESTO de modelado — sin datos reales de conversión aún."],
    ["Comisión de procesamiento de pagos (Stripe+Wompi blended)", "4% sobre el ARR de suscripción cobrado", "SUPUESTO — Stripe público (~2.9%+$0.30), Wompi NO reverificado en esta sesión (rango público ~2.65%-3.99%+IVA). Confirmar con Wompi antes de usar como dato duro."],
    ["Modelo de ingresos de la plataforma", "EXCLUSIVAMENTE suscripción (Básico + Pro + Élite 360) — ARR puro", "Decisión explícita de alcance: la plataforma NO se queda con ningún % de regalías de la música distribuida, NO cobra comisión del marketplace de beats como línea de ingreso del negocio, y NO se modela fee de originación de financiamiento. Si esas funciones existen en el producto, son features del plan, no líneas de ingreso independientes en este modelo."],
    ["Verificación 'blockchain' (publishingController.ts, verifyBlockchain)", "$0 — PLACEHOLDER, no es una función real", "Auditado en el código: guarda un tx_hash simulado, no hay ethers.js/web3.js/solidity. No se modela ningún costo de gas/transacción real. Ver CAPEX_Unico para la línea de roadmap futuro NO comprometido."],
    ["Etapa de la ronda de inversión modelada", "PRE-SEED", "Prototipo pre-producción, $0 usuarios reales. El NTI aquí es un puente de arranque (equipo + legal/seguridad + ventas iniciales de Élite 360), NO una cobertura de pérdidas multianuales — ver hoja Necesidad_Inversion."],
    ["Tasa de descuento (VAN/TIR)", "38%", "SUPUESTO de modelado conservador (mayor que el 30% del modelo del sello, por ser un SaaS pre-ingresos) — no es un dato de mercado."],
    ["Impuesto de renta aplicado a utilidad positiva", "35%", "Tarifa de sociedades en Colombia 2025-2026 (misma fuente verificada usada en el plan del sello: Art. 240 E.T., Ley 2277/2022)."],
]
write_table(ws, 4, ["Supuesto", "Valor", "Fuente/Supuesto"], rows, col_widths=[40, 40, 95])
for i in range(len(rows)):
    ws.cell(row=5 + i, column=3).alignment = Alignment(wrap_text=True)
    ws.cell(row=5 + i, column=1).alignment = Alignment(wrap_text=True)
    ws.row_dimensions[5 + i].height = 48

# ---------------------------------------------------------------
# 2. PLANES Y PRECIOS (reales)
# ---------------------------------------------------------------
ws = wb.create_sheet("Planes_Reales")
ws.cell(row=1, column=1, value="LOS 3 PLANES REALES DEL PRODUCTO (ya definidos en el código — reemplazan la escalera anterior inventada).").font = Font(bold=True, color=VIOLETA)
rows = [
    ["Básico — Distribución", PRICE_BASICO_MES, price_basico_ano, "Sin límite", "Autoservicio: distribución + splits + stats"],
    ["Pro — Crecimiento", PRICE_PRO_MES, price_pro_ano, "Sin límite", "Autoservicio + marketing con IA"],
    ["Élite 360 — Artist Development (EXCLUIDO de este financiero)", PRICE_ELITE_MES, price_elite_ano, "12-15 clientes (TOPE DURO)", "PM dedicado, management, videos musicales, branding, Meta Ads gestionado, campamentos musicales — se vende en esta plataforma pero se contabiliza en el financiero del SELLO, no aquí"],
]
write_table(ws, 3, ["Plan", "Precio/mes (USD)", "Precio/año (USD)", "Capacidad", "Incluye"], rows, col_widths=[30, 16, 16, 40, 70])

# ---------------------------------------------------------------
# 3. PROYECCION DE SUSCRIPTORES
# ---------------------------------------------------------------
ws = wb.create_sheet("Proyeccion_Suscriptores")
ws.cell(row=1, column=1, value="Solo Básico/Pro — autoservicio puro, sin equipo humano dedicado por cliente. Curva conservadora de modelado, sin datos reales (ver Supuestos y Sensibilidad). Élite 360 NO aparece aquí: se contabiliza en el financiero del sello.").font = Font(italic=True, color=ROJO)
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
rows = [
    ["Suscriptores Básico"] + basico_subs,
    ["Suscriptores Pro"] + pro_subs,
]
write_table(ws, 3, ["Métrica"] + years, rows, col_widths=[34, 12, 12, 12, 12, 12])

# ---------------------------------------------------------------
# 4. INGRESOS
# ---------------------------------------------------------------
ws = wb.create_sheet("Ingresos")
ws.cell(row=1, column=1, value="Modelo de ingresos EXCLUSIVAMENTE de suscripción Básico + Pro (ARR), ambos de autoservicio puro. Élite 360 NO se incluye aquí — su ingreso y el costo del equipo que lo entrega viven en docs/sello_plan/modelo_financiero_sello.xlsx, para resolver el doble conteo de forma definitiva.")
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[1].height = 30
rows = [
    ["Ingresos Básico"] + rev_basico,
    ["Ingresos Pro"] + rev_pro,
    ["INGRESOS TOTALES (ARR)"] + total_rev,
]
write_table(ws, 3, ["Rubro"] + years, rows, col_widths=[38, 15, 15, 15, 15, 15])

# ---------------------------------------------------------------
# 5. COGS
# ---------------------------------------------------------------
processed_volume = [round(b + p, 2) for b, p in zip(rev_basico, rev_pro)]
cogs = [round(v * 0.04, 2) for v in processed_volume]

ws = wb.create_sheet("COGS_Variable")
ws.cell(row=1, column=1, value="4% sobre el ARR de suscripción cobrado (SOLO Básico+Pro) vía Stripe/Wompi.")
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
rows = [
    ["Volumen procesado (USD)"] + processed_volume,
    ["Comisión de procesamiento (4%)"] + cogs,
]
write_table(ws, 3, ["Rubro"] + years, rows, col_widths=[38, 15, 15, 15, 15, 15])

# ---------------------------------------------------------------
# 6. OPEX — SOLO equipo de INGENIERÍA de la plataforma
# ---------------------------------------------------------------
tecnologia = [2400, 6000, 18000, 45000, 90000]
equipo_ingenieria = [36000, 38400, 40800, 43200, 45600]
ia_soporte_ventas = [1200, 3600, 9600, 22000, 42000]
marketing = [6000, 15000, 35000, 70000, 130000]
legal_admin = [3000, 4000, 6000, 8000, 10000]
opex_total = [round(a + b + c + d + e, 2) for a, b, c, d, e in
              zip(tecnologia, equipo_ingenieria, ia_soporte_ventas, marketing, legal_admin)]

ws = wb.create_sheet("OPEX")
ws.cell(row=1, column=1, value="FILOSOFÍA LEAN EXPLÍCITA DEL FUNDADOR: operar con el menor número de personas posible. UN SOLO programador full-stack en nómina (no segundo dev, no QA separado — testing básico lo cubre el mismo programador). Soporte al cliente y ventas de primer nivel se cubren con HERRAMIENTAS DE IA (Claude/Gemini API), no con personas — por eso aparecen como línea de costo de herramientas, no como salario. NO incluye al Project Manager ni al equipo de desarrollo artístico de Élite 360 — ese costo YA está presupuestado en el Modelo Financiero IM Music — Sello, para evitar doble conteo.").font = Font(italic=True, color=ROJO)
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[1].height = 60
rows = [
    ["Tecnología (hosting + Cloudinary + Gemini API del producto)"] + tecnologia,
    ["Programador único full-stack (1 persona, NO Élite 360)"] + equipo_ingenieria,
    ["Herramientas IA de soporte y ventas (reemplaza personal humano)"] + ia_soporte_ventas,
    ["Marketing / adquisición de usuarios autoservicio"] + marketing,
    ["Legal y administrativo (recurrente, casi a cero)"] + legal_admin,
    ["TOTAL OPEX"] + opex_total,
]
write_table(ws, 3, ["Rubro"] + years, rows, col_widths=[50, 15, 15, 15, 15, 15])
ws.cell(row=10, column=1, value="⚠ Riesgo de key-person: con un solo programador y cero QA dedicado, cualquier ausencia, renuncia o cuello de botella técnico detiene el desarrollo/soporte de la plataforma por completo. Es una decisión deliberada de bajo costo, pero es un riesgo operativo real que hay que decirle al inversionista, no esconderlo.").font = Font(italic=True, color=ROJO)
ws.cell(row=10, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[10].height = 45

# ---------------------------------------------------------------
# 7. CAPEX / COSTOS ÚNICOS
# ---------------------------------------------------------------
ws = wb.create_sheet("CAPEX_Unico")
ws.cell(row=1, column=1, value="CAPEX ~$0 — software ya construido, desarrollo hundido (sunk cost), no se refactura al inversionista.")
rows = [
    ["Revisión legal y de seguridad pre-lanzamiento (una vez, Año 1)", 20000, "ESTIMADO, rango $15.000-$30.000 — por el módulo de financiamiento y manejo de splits/regalías. Pedir cotización real."],
    ["[FUTURO, NO COMPROMETIDO] Verificación blockchain on-chain real", "No cuantificado", "'verifyBlockchain' actual es un PLACEHOLDER (tx_hash simulado, sin ethers.js/web3.js/solidity). Si se construye de verdad en fase posterior, ahí habría costo de desarrollo + gas. NO incluido en el NTI de esta ronda pre-seed."],
]
write_table(ws, 3, ["Concepto", "Valor (USD)", "Nota"], rows, col_widths=[55, 16, 85])
ws.row_dimensions[4].height = 45
ws.row_dimensions[5].height = 70
for rr in (4, 5):
    ws.cell(row=rr, column=3).alignment = Alignment(wrap_text=True)
ws.cell(row=5, column=1).font = Font(italic=True, color=ROJO)

# ---------------------------------------------------------------
# 8. ESTADO DE RESULTADOS (con impuesto, porque ahora hay utilidad)
# ---------------------------------------------------------------
costo_unico = [20000, 0, 0, 0, 0]
ebitda = [round(tr - c - o, 2) for tr, c, o in zip(total_rev, cogs, opex_total)]
uai = [round(e - cu, 2) for e, cu in zip(ebitda, costo_unico)]
impuesto = [round(max(u, 0) * 0.35, 2) for u in uai]
utilidad_neta = [round(u - i, 2) for u, i in zip(uai, impuesto)]

ws = wb.create_sheet("Estado_Resultados")
rows = [
    ["INGRESOS TOTALES"] + total_rev,
    ["(-) Costos Variables (COGS)"] + cogs,
    ["(-) OPEX (solo ingeniería de plataforma)"] + opex_total,
    ["EBITDA"] + ebitda,
    ["(-) Costo único (legal/seguridad, Año 1)"] + costo_unico,
    ["UTILIDAD ANTES DE IMPUESTOS (UAI)"] + uai,
    ["(-) Impuesto de renta (35% sobre UAI positiva)"] + impuesto,
    ["UTILIDAD NETA"] + utilidad_neta,
]
write_table(ws, 1, ["Rubro"] + years, rows, col_widths=[42, 15, 15, 15, 15, 15])

# ---------------------------------------------------------------
# 9. NECESIDAD DE INVERSIÓN (NTI) — puente de arranque, no déficit multianual
# ---------------------------------------------------------------
puente_6m = round(opex_total[0] / 2, 2)
legal_unico = 20000
colchon_ventas = 30000
nti = round(puente_6m + legal_unico + colchon_ventas, 2)

ws = wb.create_sheet("Necesidad_Inversion")
ws.cell(row=1, column=1, value="Este modelo queda SOLO con Básico + Pro (autoservicio). Élite 360 se excluyó por completo — su ingreso y el costo de su equipo viven únicamente en el financiero del sello.").font = Font(bold=True, color=ROJO)
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[1].height = 45
rows = [
    ["Puente de caja (~6 meses de OPEX, Año 1)", puente_6m],
    ["Revisión legal y de seguridad pre-lanzamiento (única vez)", legal_unico],
    ["Colchón para adquisición inicial de usuarios de autoservicio", colchon_ventas],
    ["NECESIDAD TOTAL DE INVERSIÓN (NTI) — RONDA PRE-SEED", nti],
]
write_table(ws, 3, ["Concepto", "Valor (USD)"], rows, col_widths=[65, 18])
ws.cell(row=8, column=1, value="Etapa: PRE-SEED. Este NTI financia ÚNICAMENTE la operación de Básico+Pro (programador único + herramientas de IA + marketing de autoservicio) — ver Estado_Resultados y Sensibilidad para saber si ese negocio por sí solo es rentable en el horizonte de 5 años antes de tratar esta cifra como definitiva.").font = Font(italic=True, color=ROJO)
ws.cell(row=8, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[8].height = 45

# ---------------------------------------------------------------
# 10. FLUJO DE CAJA / TIR / VAN
# ---------------------------------------------------------------
flujo = [-nti] + utilidad_neta
tasa = 0.38


def van(cashflows, rate):
    return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cashflows))


def irr_bisection(cashflows, lo=-0.99, hi=20.0, iters=200):
    def f(r):
        return van(cashflows, r)
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None
    for _ in range(iters):
        mid = (lo + hi) / 2
        fmid = f(mid)
        if abs(fmid) < 1e-6:
            return mid
        if flo * fmid < 0:
            hi = mid
            fhi = fmid
        else:
            lo = mid
            flo = fmid
    return (lo + hi) / 2


van_38 = round(van(flujo, tasa), 2)
tir = irr_bisection(flujo)

ws = wb.create_sheet("Flujo_Caja_TIR_VAN")
ws.cell(row=1, column=1, value="SOLO Básico + Pro (autoservicio puro, sin Élite 360). Léase el resultado exacto que imprime el script al correrlo — no se asume de antemano si el flujo es positivo o negativo: se reporta el número real, sea bueno o malo.").font = Font(bold=True, color=ROJO)
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[1].height = 90

rows = [["Flujo de caja neto (Año 0 = -NTI; Años 1-5 = utilidad neta)"] + flujo]
write_table(ws, 3, ["Periodo"] + ["Año 0"] + years, rows, col_widths=[55, 15, 15, 15, 15, 15, 15])

tir_txt = f"{tir * 100:.1f}%" if tir is not None else "no computable"
ws.cell(row=6, column=1, value=f"VAN a 5 años, tasa de descuento 38%: USD {van_38:,.2f}")
ws.cell(row=7, column=1, value=f"TIR a 5 años: {tir_txt}")
ws.cell(row=8, column=1, value="Etapa de la ronda: PRE-SEED. Un TIR de esta magnitud en una ronda pre-seed sin un solo cliente firmado todavía es una señal de ALTO RIESGO del modelo, no una garantía de retorno — preséntese junto con la hoja Sensibilidad, nunca sola.").font = Font(bold=True, color=ROJO)
ws.cell(row=8, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[8].height = 30

# ---------------------------------------------------------------
# 11. SENSIBILIDAD — honestidad sobre la dependencia del caso base
# ---------------------------------------------------------------
ws = wb.create_sheet("Sensibilidad")
ws.cell(row=1, column=1, value="Qué tan dependiente es el resultado de que la adopción de Básico/Pro llegue a los niveles modelados (Élite 360 se deja igual en los 3 escenarios, porque depende de ventas de alto contacto, no de elasticidad de precio masiva).").font = Font(italic=True)
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)

def escenario_year5(factor):
    b5 = basico_subs[-1] * factor
    p5 = pro_subs[-1] * factor
    rev_b = b5 * price_basico_ano
    rev_p = p5 * price_pro_ano
    rev_t = rev_b + rev_p
    vol = rev_b + rev_p
    cogs_e = vol * 0.04
    opex_e = opex_total[-1]
    ebitda_e = rev_t - cogs_e - opex_e
    return round(rev_t, 2), round(ebitda_e, 2)

base_rev5, base_ebitda5 = escenario_year5(1.0)
cons_rev5, cons_ebitda5 = escenario_year5(0.5)
pesi_rev5, pesi_ebitda5 = escenario_year5(0.25)

rows = [
    ["Caso base (100% de la adopción modelada)", base_rev5, base_ebitda5],
    ["Conservador (50% de la adopción de Básico/Pro)", cons_rev5, cons_ebitda5],
    ["Pesimista (25% de la adopción de Básico/Pro)", pesi_rev5, pesi_ebitda5],
]
write_table(ws, 3, ["Escenario (Año 5)", "Ingresos totales (USD)", "EBITDA (USD)"], rows, col_widths=[45, 22, 22])
ws.cell(row=8, column=1, value="Con Élite 360 excluido, toda la rentabilidad de este modelo depende exclusivamente de que Básico+Pro alcancen la escala de autoservicio modelada. No hay ningún ingreso de respaldo (ya no hay un 'techo' de servicio boutique que sostenga el EBITDA si la adopción de autoservicio es baja) — léase el escenario pesimista con esa honestidad.").font = Font(italic=True, color=ROJO)
ws.cell(row=8, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[8].height = 60

for sheet in wb.worksheets:
    sheet.sheet_view.showGridLines = False

wb.save(str(OUT))
print(f"OK: {OUT} ({OUT.stat().st_size // 1024}KB)")
print("Ingresos totales:", total_rev)
print("EBITDA:", ebitda)
print("Utilidad neta:", utilidad_neta)
print("NTI:", nti, "VAN(38%):", van_38, "TIR:", tir_txt)
print("Sensibilidad Y5 -> base:", (base_rev5, base_ebitda5), "cons:", (cons_rev5, cons_ebitda5), "pesi:", (pesi_rev5, pesi_ebitda5))
