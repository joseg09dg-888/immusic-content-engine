# Dubái — Modelo Lean/Por Fases v4 (resumen en lenguaje plano)

Este documento es una **alternativa** al modelo Dubái completo (`modelo_financiero_sello.xlsx`), no un reemplazo. El fundador **sí se radica en Dubái** y **sí monta estudio y oficina** desde el Año 1, pero a escala mínima, escalando por fases solo cuando los ingresos/flujo de caja lo justifiquen.

## Estructura de ingresos (v4 — corregida)

- **Servicio ELITE 360** (precio REAL de la plataforma, no estimado): **USD $2.999,99/mes por artista** — incluye Project Manager dedicado, manager musical, videos musicales, branding, gestión de Meta Ads, campamentos musicales y red de industria. El "360" es el **alcance del servicio de marketing/marca**, no un reparto de ingresos de streaming/shows/merch/patrocinios del artista.
- **Roster con tope duro de 12 artistas** en Dubái (extremo bajo del rango 12-15 instruido), con curva de ocupación gradual: 1 → 3 → 6 → 9 → 12 artistas firmados al cierre de cada año (no 12 desde el mes 1).
- **Tasa de ocupación del roster: 85% (estimada)** — no todos los cupos firmados facturan el fee completo todos los meses.
- **Producción musical** (externos + roster puntual): igual que antes, 1-3 proyectos/mes.
- **YouTube propio** (AdSense/Content ID): supuesto conservador, sin datos reales de vistas.
- **Libro "Music Business Para Todos Los Humanos"**: ingreso YA VALIDADO (el libro ya se vende en Hotmart ES/EN/PT) — solo el volumen de copias/mes es supuesto.
- **Regalías de catálogo / proyectos especiales**: UNA sola línea (no duplicada) — retorno vía Nexus (8% comisión) de canciones/EPs/álbumes que el sello financia con capital propio, con % de regalía negociado caso por caso. No es ingreso automático por artista del roster.
- **Legal casi a cero** (AED 200/mes): el fundador cubre la función legal directamente.

## Resultado — ahora SÍ es positivo

| | Modelo Completo (referencia pre-corrección) | Modelo Lean v4 |
|---|---|---|
| Inversión requerida (NTI) | AED 318.259 | **AED 168.787** |
| EBITDA Año 1 | -AED 327.892 | -AED 123.561 |
| EBITDA Año 3 | — | **+AED 158.515** (primer año positivo) |
| EBITDA Año 5 | -AED 247.663 | **+AED 374.674** |
| Utilidad Neta Año 5 | — | **+AED 359.997** |
| **VAN (25%)** | -AED 1.133.096 | **+AED 35.292** |
| **TIR** | No calculable | **29,1%** |
| Gatillo de escalamiento | N/A | Se activa en el **Año 4** (primera contratación local + upgrade de oficina) |

**Lectura honesta:** el precio real del plan ELITE 360 (USD $2.999,99/mes/artista) es sustancialmente más alto que la tarifa que se había estimado antes, y eso cambia el resultado de fondo: con una curva de ocupación conservadora y un roster que tarda 5 años en llegar a 12 artistas, el negocio **se vuelve rentable a partir del Año 3** y termina con VAN y TIR positivos. Esto no es un número forzado — así salió con los supuestos declarados.

## El riesgo real a validar — no es financiero, es operativo

El plan ELITE 360 es un servicio de **alto contacto**: Project Manager dedicado, videos musicales, campamentos musicales. Este modelo lean asume que **una sola persona (el fundador) + freelancers por proyecto** pueden entregar ese nivel de servicio a varios artistas en simultáneo (hasta ~9 pagantes en Año 5) sin contratar nadie fijo hasta el Año 4. Esa es una tensión real entre "modelo lean sin contrataciones" y "servicio premium de alto contacto" que **debe validarse operativamente antes de vender este plan a escala** — no basta con que los números cuadren en Excel; hay que confirmar que es humanamente posible entregarlo así.

También queda sin resolver si el presupuesto de pauta de Meta Ads está incluido en el fee de $2.999,99 o se factura aparte al artista — este modelo asume que está incluido (de ahí el costo de entrega del 40% del fee, también una estimación, no una cotización real).

## Supuestos marcados como no confirmados

Todo lo de CAPEX (estudio, kit audiovisual, licencia de zona franca, visa), el costo de entrega del plan ELITE 360 (40%, estimación propia), la tasa de ocupación (85%, estimación), el volumen de copias del libro, y los montos de regalías de catálogo — ver la pestaña "Supuestos" del archivo para el detalle línea por línea, cada uno con su nota de fuente o de "no confirmado". El precio del plan ELITE 360 en sí ($2.999,99/mes) es el único dato de ingreso que es real, no estimado.

## ⚠️ Pendiente de corrección (detectado en auditoría de consistencia, no resuelto aquí)

Este archivo quedó desactualizado en dos puntos frente a `modelo_financiero_sello.xlsx` (el modelo Dubái completo, ya corregido) y requiere una decisión humana antes de usarse frente a un inversionista o concurso:

1. **Arriendo — revisado y aclarado (ya NO es un pendiente, el texto de `Supuestos!D20`/`D25` estaba mal redactado, no el número).** La redacción original de `Supuestos!D20`/`D25` decía que el diferencial de AED 2.775/mes del Año 4 se calculaba contra "AED 3.575/mes del modelo completo", lo que sugería (incorrectamente) que era una cifra vieja/desactualizada del arriendo Al Quoz del modelo completo (hoy corregido a AED 17.500/mes, `OPEX_DXB!B16`). Verificado contra `Supuestos_DXB!D27` del modelo completo: el arriendo Al Quoz de AED 17.500/mes es para una unidad de **2.100-2.700 sqft** (bodega/estudio creativo de gran formato, uso mixto oficina+estudio+foto+streaming). La oficina pequeña del Año 4 de este modelo Lean es explícitamente de **~150 sqft** ("oficina/estudio dedicado pequeño"), calculada con una tarifa por sqft distinta y sí confirmada (Nikoliers 2024) para un local convencional — **no son el mismo tipo de espacio y no son comparables por sqft** (un local pequeño convencional cuesta más por sqft que una bodega de gran formato en Al Quoz). Por lo tanto, AED 3.575/mes para esa oficina pequeña **no es una versión obsoleta de AED 17.500 — es una cifra independiente y correcta para un inmueble distinto**, y no debe recalcularse contra el arriendo Al Quoz. Se corrigió el texto de `Supuestos!D20` y `D25` en el archivo para que ya no sugiera lo contrario. Los valores `B20=800` y `B25=2.775` NO cambiaron — eran correctos.

2. **Falta la línea "Representación / Entrada a Mercado".** El modelo completo (`modelo_financiero_sello.xlsx`, hoja `EstadoResultados_DXB!A12`) incluye esta línea de ingreso desde la corrección más reciente, explícitamente "igual en ambos mercados, al mismo precio en USD" (ver `modelo_financiero_sello_notas.md`). Este archivo (`EstadoResultados`, filas 4-8) no la tiene. No se agregó aquí porque el modelo completo cubre su costo con el tiempo ya pagado del Gerente Comercial (OPEX fijo) — y en este escenario Lean el Gerente Comercial no se contrata hasta que se activa el gatillo de escalamiento (Año 4 en el caso base). Antes de agregar la línea hay que decidir quién la entrega en Año 1-3: ¿el fundador solo, absorbiendo ese tiempo adicional sobre la ya ajustada carga operativa del plan ELITE 360? Eso cambiaría también el supuesto de "costo casi nulo" que tiene la línea en el modelo completo.
