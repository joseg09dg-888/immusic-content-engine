# Modelo Financiero — IM MUSIC Elite Artist Platform (SaaS)
## Notas en lenguaje simple

Este documento resume en palabras simples lo que hay en `modelo_financiero_saas.xlsx`. Está pensado como un prototipo pre-producción: hay backend y frontend funcionando (Node/TypeScript + Express + PostgreSQL, integración real con Spotify, Stripe y Wompi), pero **$0 en usuarios de pago reales**. Todo lo que aquí es "proyección" es una estimación de modelado, no un dato de mercado comprobado.

## Lo más importante primero

- **Etapa de la ronda: PRE-SEED.** Este dinero no financia una expansión de usuarios ya validados — financia llevar el prototipo a producción (QA/estabilización), armar el equipo mínimo, hacer la revisión legal/seguridad que el producto necesita, y el primer empuje de mercado.
- **Pedido de inversión (NTI) propuesto: ~USD $312.000.** Cubre el déficit de caja proyectado a 5 años bajo supuestos conservadores + un colchón de seguridad de ~6 meses de gastos.
- **El modelo da pérdidas los 5 años**, mejorando cada año, casi llegando a punto de equilibrio en el año 5 (-$3.060 USD). No se infló el modelo para mostrar una TIR bonita — se reporta la realidad.
- **No hay TIR calculable a 5 años** porque el flujo de caja nunca se vuelve positivo en ese horizonte. El VAN a 5 años (tasa de descuento 38%) es de **-$445.711 USD** — negativo, como corresponde a una historia de pérdidas sostenidas.
- Esto **no es un defecto del modelo**: es lo que de verdad pasa si se proyecta de forma conservadora un SaaS pre-ingresos compitiendo contra DistroKid/TuneCore, sin inflar la adopción de usuarios para que se vea bien.

## Qué hacer con esto, en términos honestos

1. **Extender el horizonte a 7-8 años** en una versión futura del modelo — con la trayectoria actual (pérdida decreciente, casi breakeven en año 5), es razonable que sí llegue a ser rentable un par de años después del corte de este modelo.
2. **Levantar el capital en etapas**: pre-seed ahora (este monto), y una ronda seed posterior condicionada a tracción real de suscriptores — no pedir todo de una vez como si ya hubiera usuarios pagando.
3. Considerar si el ritmo de contratación del equipo (2 desarrolladores para el año 3) puede ser aún más lento/lean sin poner en riesgo la plataforma — eso mejoraría el punto de equilibrio.

## La corrección importante sobre "blockchain"

En el código existe una función llamada `verifyBlockchain` (en `publishingController.ts`). **Es un placeholder/simulación** — genera un `tx_hash` falso. No hay ninguna librería real de blockchain instalada en el proyecto (nada de ethers.js, web3.js o Solidity). Por eso:

- **No se modeló ningún costo de gas ni transacción on-chain real** — porque esa función no existe todavía de verdad.
- Si en el futuro (no en el año 1, ni en esta ronda pre-seed) se decide construir una verificación blockchain real, eso tendría un costo de desarrollo + costo de gas que habría que cotizar en ese momento. Quedó anotado en la hoja `CAPEX_Unico` del Excel como una línea de **roadmap futuro no comprometido**, para que nadie lo confunda con un gasto actual.

## Supuestos que TIENES que validar antes de mostrarle esto a un inversionista real

Estas cifras están en el modelo pero **no están verificadas con una fuente actual confirmada en esta sesión** — son estimaciones razonables, no hechos:

- **Comisión real de Wompi** en Colombia (se usó un rango público aproximado de 2.65%-3.99% + IVA, sin confirmar la tarifa vigente exacta — llamar a Wompi directamente).
- **Precio actual de hosting** (Neon Postgres, Cloudinary, Gemini API) — se usaron estimaciones escalonadas de conocimiento general, no tablas de precios verificadas en esta sesión.
- **Salario real de un desarrollador fullstack remoto en Colombia** (~$3.000-3.300 USD/mes usado en el modelo) — no se verificó con una fuente salarial actual en esta sesión.
- **Conversión y churn de suscriptores** — no existen datos reales porque la plataforma no tiene usuarios de pago aún. Toda la curva de crecimiento (50 → 300 → 1.200 → 3.500 → 8.000 suscriptores en 5 años) es un supuesto de modelado conservador, no una medición.
- **Costo real de la revisión legal/seguridad pre-lanzamiento** (~$20.000 USD estimado) — pedir cotización real a una firma especializada en fintech/entretenimiento antes de usar esta cifra en un documento formal.
- **El pricing de planes** (Básico $19.99, Plus $34.99, Premium $59.99, Label $149.99 USD/año) es una propuesta de corrección al pricing roto que tenía el código (donde "Plus" costaba menos que "Básico"), basada en el rango general conocido de DistroKid/TuneCore — no es un pricing validado con el mercado todavía.

## Resumen numérico (ver detalle completo en el Excel)

| Año | Ingresos | EBITDA |
|---|---|---|
| 1 | $1.860 | -$50.683 |
| 2 | $11.157 | -$57.597 |
| 3 | $44.628 | -$91.589 |
| 4 | $130.165 | -$59.402 |
| 5 | $297.520 | -$3.061 |

NTI propuesto (ronda pre-seed): **~$312.407 USD**. VAN a 5 años (38% descuento): **-$445.711 USD** (negativo). TIR: no computable en este horizonte.
