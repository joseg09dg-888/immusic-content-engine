"""Genera docs/saas_plan/modelo_financiero_saas.xlsx — modelo financiero
realista (pre-lanzamiento, sin datos reales de usuarios) para la plataforma
SaaS 'IM MUSIC - Elite Artist Platform'. Todas las cifras no verificadas
quedan marcadas explicitamente en la columna Fuente/Supuesto."""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "saas_plan" / "modelo_financiero_saas.xlsx"
OUT.parent.mkdir(parents=True, exist_ok=True)

VIOLETA = "FF5E17EB"
BLANCO = "FFFFFFFF"
GRIS = "FFF2EDE5"
ROJO = "FFB00020"

wb = Workbook()
wb.remove(wb.active)


def style_header(ws, row, n_cols, text_rows=1):
    for r in range(row, row + text_rows):
        for c in range(1, n_cols + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor=VIOLETA)


def write_table(ws, start_row, headers, rows, col_widths=None):
    ws.append([] * 0)
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


def flag_note(ws, row, col, text):
    cell = ws.cell(row=row, column=col, value=text)
    cell.font = Font(italic=True, color="FFB00020")
    cell.alignment = Alignment(wrap_text=True)


# ---------------------------------------------------------------
# 1. SUPUESTOS
# ---------------------------------------------------------------
ws = wb.create_sheet("Supuestos")
ws.cell(row=1, column=1, value="MODELO FINANCIERO — IM MUSIC ELITE ARTIST PLATFORM (SaaS)").font = Font(bold=True, size=14, color=VIOLETA)
ws.cell(row=2, column=1, value="Plataforma pre-lanzamiento (backend/frontend funcional, sin usuarios reales de pago). Todo supuesto de crecimiento/conversión/churn es una estimación de modelado, NO un dato de mercado.").font = Font(italic=True)

rows = [
    ["Horizonte del modelo", "5 años", "Decisión de modelado"],
    ["Moneda base", "USD", "La plataforma cobra en USD (Stripe) y COP vía Wompi; se consolida todo a USD para comparabilidad"],
    ["Tasa de descuento (VAN/TIR)", "38%", "SUPUESTO — mayor que el 30% usado en el modelo del sello, porque un SaaS pre-ingresos es más riesgoso. No es un dato de mercado, es una decisión de modelado conservadora, a validar con el inversionista"],
    ["Comisión procesamiento de pagos (Stripe)", "2.9% + $0.30 USD por transacción", "Dato público de Stripe (stripe.com/pricing), vigente en EE. UU./internacional estándar — verificar tarifa exacta para Colombia/LatAm al momento de implementar"],
    ["Comisión procesamiento de pagos (Wompi)", "Estimado ~2.65%-3.99% + IVA según método (tarjeta/PSE/Nequi)", "NO reverificado en esta sesión con la tarifa vigente de Wompi — CONFIRMAR directamente con Wompi antes de usar en un documento para inversionistas"],
    ["Comisión de procesamiento blended usada en el modelo", "4% sobre ingresos procesados", "SUPUESTO conservador que combina Stripe+Wompi+fricción de tarjetas pequeñas — a validar"],
    ["Costo de hosting/infraestructura (Neon Postgres, Cloudinary, Gemini API)", "Escalonado: ~$100/mes año 1 hasta ~$2.000/mes año 5", "ESTIMADO con base en conocimiento general de los planes publicados de estos proveedores — NO se verificaron tablas de precios vigentes en esta sesión (sin acceso a web en este fork). Confirmar precios actuales antes de usar como dato duro"],
    ["Salario mensual desarrollador fullstack remoto (Colombia)", "~$3.000-3.300 USD/mes", "ESTIMADO de conocimiento general de mercado remoto LatAm — NO verificado con fuente actual en esta sesión. Confirmar con Computrabajo/LinkedIn Salary/comparables reales"],
    ["Salario soporte/QA part-time", "~$600-1.500 USD/mes (escalando)", "ESTIMADO, mismo nivel de confianza que el anterior — no verificado"],
    ["Revisión legal/seguridad pre-lanzamiento (una vez)", "~$20.000 USD (rango $15.000-$30.000)", "ESTIMADO — necesario por el módulo de elegibilidad de financiamiento y manejo de regalías/splits, que tocan temas financieros regulados. NO es una cotización real, pedir cotización a firma especializada en fintech/entretenimiento antes de usar"],
    ["Mezcla de planes de suscriptores (Básico/Plus/Premium/Label)", "65% / 22% / 10% / 3%", "SUPUESTO de modelado — sin datos reales de conversión aún, no hay usuarios de pago"],
    ["Comisión de marketplace de beats", "15% sobre GMV", "SUPUESTO — benchmark cualitativo tipo BeatStars (10-20% típico en la industria), no verificado con fuente específica en esta sesión"],
    ["Ingresos por financiamiento (adelantos a artistas)", "$0 modelado en los 5 años", "Se excluye deliberadamente del modelo de ingresos por ser una actividad financiera regulada/sensible y sin datos de pérdida esperada — se trata como opcionalidad futura, no como ingreso proyectado, para no inflar el modelo con una cifra inventada"],
    ["Verificación 'blockchain' (publishingController.ts, verifyBlockchain)", "$0 — PLACEHOLDER, no es una función real", "Auditado en el código: guarda un tx_hash simulado, no hay ethers.js/web3.js/solidity ni ninguna librería blockchain real en el proyecto. NO se modela ningún costo de gas ni transacción on-chain real porque esa función no existe todavía. Ver hoja CAPEX_Unico para una línea de costo FUTURO no comprometido si se decide implementarla de verdad en una fase posterior"],
    ["Etapa de la ronda de inversión modelada", "PRE-SEED", "Esto es un prototipo pre-producción con $0 de usuarios/ingresos reales. El monto y el uso de fondos de este modelo corresponden a una ronda PRE-SEED (productización + equipo mínimo + revisión legal/seguridad + go-to-market inicial) — NO a una ronda seed ni Serie A. Cualquier ronda posterior debe condicionarse a tracción real de suscriptores"],
]
r = write_table(ws, 4, ["Supuesto", "Valor", "Fuente/Supuesto"], rows, col_widths=[42, 38, 90])
for i in range(len(rows)):
    ws.cell(row=5 + i, column=3).alignment = Alignment(wrap_text=True)
    ws.row_dimensions[5 + i].height = 45

# ---------------------------------------------------------------
# 2. PRICING PROPUESTO
# ---------------------------------------------------------------
ws = wb.create_sheet("Pricing_Propuesto")
ws.cell(row=1, column=1, value="PROPUESTA DE PRECIOS — PENDIENTE DE VALIDAR CON EL DOCUMENTO DE NEGOCIO").font = Font(bold=True, size=13, color=ROJO)
ws.cell(row=2, column=1, value="El pricing actual en el código (Básico $15, Plus $3.75, Premium $7.50, Enterprise10 $19.99) es un borrador con error: Plus cuesta menos que Básico. Esta tabla corrige la estructura con una escalera monotónica, referenciando (sin verificar en esta sesión) los rangos públicos conocidos de DistroKid (~$19.99-$89.99/año) y TuneCore (~$9.99-$49.99/año).")
ws.cell(row=2, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[2].height = 45

rows = [
    ["Básico", 19.99, 1, "Distribución ilimitada, splits, stats diarias, 1 marca de sello"],
    ["Plus", 34.99, 2, "+ fecha de lanzamiento personalizable, precios iTunes, analytics avanzado"],
    ["Premium", 59.99, 5, "+ multi-artista, soporte prioritario, herramientas promocionales"],
    ["Label (Enterprise)", 149.99, 10, "+ reportes consolidados, acceso API, marca blanca parcial"],
]
write_table(ws, 5, ["Plan", "Precio anual (USD) — PROPUESTA", "Máx. artistas", "Incluye"], rows, col_widths=[22, 28, 16, 60])
ws.cell(row=10, column=1, value="ARPU blended (ponderado por mezcla de Supuestos): $31.19 USD/año por suscriptor — ver hoja Supuestos.").font = Font(italic=True)

# ---------------------------------------------------------------
# 3. PROYECCION DE SUSCRIPTORES
# ---------------------------------------------------------------
ws = wb.create_sheet("Proyeccion_Suscriptores")
ws.cell(row=1, column=1, value="PROYECCIÓN DE SUSCRIPTORES — ESCENARIO CONSERVADOR DE MODELADO (NO hay datos reales de conversión; no confundir con un SOM de mercado)").font = Font(bold=True, color=ROJO)
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[1].height = 30

years = ["Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]
subs = [50, 300, 1200, 3500, 8000]
arpu = 31.19
gmv_beats = [2000, 12000, 48000, 140000, 320000]

rows = [["Suscriptores de pago (fin de año)"] + subs]
rows.append(["ARPU blended (USD/año)"] + [arpu] * 5)
rows.append(["GMV marketplace de beats (USD)"] + gmv_beats)
write_table(ws, 3, ["Métrica"] + years, rows, col_widths=[36, 12, 12, 12, 12, 12])
ws.cell(row=8, column=1, value="Supuesto de arranque: catálogo propio del sello (artistas firmados) + crecimiento orgánico boutique en Medellín, sin pauta pagada agresiva los primeros 2 años.").font = Font(italic=True)

# ---------------------------------------------------------------
# 4. INGRESOS
# ---------------------------------------------------------------
sub_rev = [round(s * arpu, 2) for s in subs]
beat_comm = [round(g * 0.15, 2) for g in gmv_beats]
total_rev = [round(a + b, 2) for a, b in zip(sub_rev, beat_comm)]

ws = wb.create_sheet("Ingresos")
rows = [
    ["Ingresos por suscripción"] + sub_rev,
    ["Comisión marketplace de beats (15% GMV)"] + beat_comm,
    ["Ingresos por financiamiento"] + [0, 0, 0, 0, 0],
    ["INGRESOS TOTALES"] + total_rev,
]
write_table(ws, 1, ["Rubro"] + years, rows, col_widths=[38, 13, 13, 13, 13, 13])
ws.cell(row=7, column=1, value="Ingresos por financiamiento modelados en $0: ver Supuestos — se excluye deliberadamente por ser actividad financiera sensible sin datos de pérdida esperada.").font = Font(italic=True, color=ROJO)

# ---------------------------------------------------------------
# 5. COSTOS VARIABLES (COGS)
# ---------------------------------------------------------------
processed_volume = [round(sr + g, 2) for sr, g in zip(sub_rev, gmv_beats)]
cogs = [round(v * 0.04, 2) for v in processed_volume]

ws = wb.create_sheet("COGS_Variable")
ws.cell(row=1, column=1, value="Costo variable = 4% sobre volumen procesado (ingresos por suscripción + GMV completo del marketplace, ya que la plataforma procesa el pago completo antes de pagarle al productor). Supuesto blended Stripe+Wompi — ver Supuestos, no verificado con tarifa exacta vigente.").font = Font(italic=True)
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[1].height = 45
rows = [
    ["Volumen procesado (USD)"] + processed_volume,
    ["Comisión de procesamiento (4%)"] + cogs,
]
write_table(ws, 3, ["Rubro"] + years, rows, col_widths=[38, 13, 13, 13, 13, 13])

# ---------------------------------------------------------------
# 6. OPEX
# ---------------------------------------------------------------
tecnologia = [1200, 2400, 6000, 12000, 24000]
equipo = [43200, 48000, 88800, 93600, 118800]
marketing = [6000, 15000, 35000, 70000, 130000]
legal_admin = [2000, 2500, 3000, 4000, 5000]
opex_total = [round(a + b + c + d, 2) for a, b, c, d in zip(tecnologia, equipo, marketing, legal_admin)]

ws = wb.create_sheet("OPEX")
ws.cell(row=1, column=1, value="Equipo mínimo viable para llevar el prototipo a producción y mantenerlo — TODOS los salarios son estimados no verificados (ver Supuestos). El CEO/gerente del sello puede compartir tiempo con esta plataforma; aquí NO se duplica ese costo, se asume que el rol de producto lo cubre el mismo CEO del sello salvo que el inversionista prefiera separarlo.").font = Font(italic=True)
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[1].height = 45
rows = [
    ["Tecnología (hosting + Cloudinary + Gemini API)"] + tecnologia,
    ["Equipo (dev + QA/soporte)"] + equipo,
    ["Marketing / adquisición de usuarios"] + marketing,
    ["Legal y administrativo (recurrente)"] + legal_admin,
    ["TOTAL OPEX"] + opex_total,
]
write_table(ws, 3, ["Rubro"] + years, rows, col_widths=[42, 13, 13, 13, 13, 13])

# ---------------------------------------------------------------
# 7. CAPEX / COSTOS ÚNICOS
# ---------------------------------------------------------------
ws = wb.create_sheet("CAPEX_Unico")
ws.cell(row=1, column=1, value="CAPEX es prácticamente $0 — es software ya construido (backend Node/TypeScript + Express + PostgreSQL, frontend React/Vite), el desarrollo ya está hundido (sunk cost) y no se re-factura al inversionista.")
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
rows = [
    ["Revisión legal y de seguridad pre-lanzamiento (una vez, Año 1)", 20000, "ESTIMADO, rango $15.000-$30.000 — necesario por el módulo de elegibilidad de financiamiento y el manejo de splits/regalías. Pedir cotización real antes de usar como cifra dura."],
    ["[FUTURO, NO COMPROMETIDO] Implementación real de verificación blockchain on-chain", "No cuantificado", "La función 'verifyBlockchain' actual en publishingController.ts es un PLACEHOLDER que guarda un tx_hash simulado — no hay ethers.js/web3.js/solidity en el proyecto. Si en una fase posterior (no Año 1) se decide construir una verificación on-chain real, ahí sí habría costo de desarrollo + gas de transacción. NO se incluye en el NTI de esta ronda pre-seed; es una línea de roadmap futuro, no un gasto actual."],
]
write_table(ws, 3, ["Concepto", "Valor (USD)", "Nota"], rows, col_widths=[55, 15, 80])
ws.row_dimensions[4].height = 45
ws.row_dimensions[5].height = 70
ws.cell(row=4, column=3).alignment = Alignment(wrap_text=True)
ws.cell(row=5, column=3).alignment = Alignment(wrap_text=True)
ws.cell(row=5, column=1).font = Font(italic=True, color=ROJO)

# ---------------------------------------------------------------
# 8. ESTADO DE RESULTADOS
# ---------------------------------------------------------------
capex_by_year = [20000, 0, 0, 0, 0]
ebitda = [round(tr - c - o, 2) for tr, c, o in zip(total_rev, cogs, opex_total)]
ebit = [round(e - cx, 2) for e, cx in zip(ebitda, capex_by_year)]

ws = wb.create_sheet("Estado_Resultados")
rows = [
    ["INGRESOS TOTALES"] + total_rev,
    ["(-) Costos Variables (COGS)"] + cogs,
    ["(-) OPEX"] + opex_total,
    ["EBITDA"] + ebitda,
    ["(-) Costo único (legal/seguridad)"] + capex_by_year,
    ["RESULTADO OPERATIVO (antes de impuestos)"] + ebit,
]
write_table(ws, 1, ["Rubro"] + years, rows, col_widths=[42, 13, 13, 13, 13, 13])
ws.cell(row=9, column=1, value="El modelo NO aplica impuesto de renta porque el resultado operativo es negativo en los 5 años bajo estos supuestos — no hay utilidad gravable.").font = Font(italic=True, color=ROJO)

# ---------------------------------------------------------------
# 9. NECESIDAD DE INVERSIÓN (NTI)
# ---------------------------------------------------------------
cum_burn = sum(e for e in ebit)  # negative
buffer_6m = round((opex_total[0] + opex_total[1]) / 2 * 0.5, 2)
nti = round(abs(cum_burn) + buffer_6m, 2)

ws = wb.create_sheet("Necesidad_Inversion")
rows = [
    ["Déficit de caja acumulado proyectado (5 años, suma de resultado operativo negativo)", round(abs(cum_burn), 2)],
    ["Colchón de seguridad (~6 meses de OPEX promedio Año 1-2)", buffer_6m],
    ["NECESIDAD TOTAL DE INVERSIÓN (NTI) — PROPUESTA, RONDA PRE-SEED", nti],
]
write_table(ws, 1, ["Concepto", "Valor (USD)"], rows, col_widths=[70, 18])
ws.cell(row=5, column=1, value="Etapa de la ronda: PRE-SEED. El producto es un prototipo pre-producción con $0 de usuarios/ingresos reales — este capital financia productización (QA/estabilización), equipo mínimo, revisión legal/seguridad y go-to-market inicial, NO una expansión de una base de usuarios ya validada. No corresponde a una ronda seed ni Serie A.").font = Font(bold=True, color=ROJO)
ws.cell(row=5, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[5].height = 45
ws.cell(row=6, column=1, value="Esta cifra es un resultado del modelo, NO una validación de mercado. Dado que el flujo de caja es negativo en los 5 años bajo supuestos conservadores, se recomienda levantar este capital en etapas (pre-seed ahora, para llegar con tracción real de suscriptores a una futura ronda seed), no de una sola vez.").font = Font(italic=True, color=ROJO)
ws.cell(row=6, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[6].height = 45

# ---------------------------------------------------------------
# 10. FLUJO DE CAJA / TIR / VAN
# ---------------------------------------------------------------
ws = wb.create_sheet("Flujo_Caja_TIR_VAN")
flujo = [-nti] + ebit  # year 0 outlay, then years 1-5 operating result as proxy for cash flow (no D&A/CAPEX recurring)
ws.cell(row=1, column=1, value="ADVERTENCIA: bajo estos supuestos conservadores, el flujo de caja operativo es NEGATIVO todos los años del horizonte de 5 años. Esto significa que NO existe una TIR convencional calculable (no hay un punto de retorno positivo dentro del horizonte) y el VAN a 5 años es necesariamente negativo. Esto no es un error del modelo: es la realidad de una plataforma SaaS pre-ingresos compitiendo contra DistroKid/TuneCore con una base de adopción conservadora. Forzar una TIR/VAN positiva aquí implicaría inflar los supuestos de crecimiento de forma no defendible.").font = Font(bold=True, color=ROJO)
ws.cell(row=1, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[1].height = 90

rows = [["Flujo de caja neto (Año 0 = -NTI; Años 1-5 = resultado operativo)"] + flujo]
write_table(ws, 3, ["Periodo"] + ["Año 0"] + years, rows, col_widths=[55, 13, 13, 13, 13, 13, 13])

tasa = 0.38
van = flujo[0] + sum(cf / ((1 + tasa) ** (i + 1)) for i, cf in enumerate(flujo[1:]))
ws.cell(row=6, column=1, value=f"VAN a 5 años, tasa de descuento 38%: USD {round(van, 2):,.2f} (negativo bajo estos supuestos)")
ws.cell(row=7, column=1, value="TIR: no computable dentro del horizonte de 5 años (no hay cambio de signo hacia flujo positivo). Alternativas honestas para presentar al inversionista: (a) extender el horizonte de análisis a 7-8 años hasta breakeven proyectado, (b) estructurar esta ronda explícitamente como PRE-SEED (productización + equipo mínimo + legal/seguridad + go-to-market inicial) con hitos de tracción real de suscriptores antes de levantar una futura ronda seed, (c) revisar si el ritmo de contratación de equipo puede ser aún más lento sin comprometer la plataforma.")
ws.cell(row=7, column=1).alignment = Alignment(wrap_text=True)
ws.row_dimensions[7].height = 60

for sheet in wb.worksheets:
    sheet.sheet_view.showGridLines = False

wb.save(str(OUT))
print(f"OK: {OUT} ({OUT.stat().st_size // 1024}KB)")
print("EBITDA por año:", ebitda)
print("NTI:", nti, "VAN:", round(van, 2))
