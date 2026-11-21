# Manual de Funciones y Procesos — IM Music (notas)

Workbook: `docs/sello_plan/manual_funciones_im_music.xlsx` — 1 hoja índice + 11 hojas de rol, mismo formato que el ejemplo de referencia del usuario (`docs/sello_plan/proceso_csv/proceso_desarrollador.csv`): columnas Tarea/Proceso, Subpasos/Detalles, Responsable, Herramientas, Métricas de Éxito, Posibles Automatizaciones, Frecuencia — más una fila final de "Interconexión con otros roles" en cada hoja.

## Los 11 roles

1. **CEO / Director del Sello** — scouting, firma de artistas, A&R, inversionistas, función legal rutinaria.
2. **Gerente Comercial** — cierra leads de la Máquina de Captación, negocia y transfiere al responsable de ejecución.
3. **Project Manager — Élite 360** — ejecuta el servicio 360 para el roster (máx. 12-15 artistas).
4. **Productor Musical** (freelance) — dirección creativa y producción.
5. **Ingeniero de Sonido** (freelance) — mezcla y masterización a estándar de cada plataforma.
6. **Contador** (externo) — finanzas, impuestos, nómina, distribución de regalías.
7. **Desarrollador Full-Stack** — única persona de desarrollo de la plataforma SaaS (key-person risk ya en la matriz de riesgos).
8. **Asesor Legal Externo** — solo casos de alta complejidad.
9. **Comunicadora / Estrategia de Contenido** — define la parrilla editorial y dirige al Content Engine, al Filmmaker y a la Diseñadora.
10. **Filmmaker / Editor con IA** (planta fija) — edita material humano real de los artistas, contraparte del video sintético del Content Engine.
11. **Diseñadora Gráfica** (planta fija) — diseño bespoke que excede el sistema de plantillas automatizado.

> Corregido en auditoría de consistencia: estos dos roles estaban etiquetados "(freelance)" en el índice y en el encabezado de sus propias hojas, desactualizado frente a la decisión de pasarlos a planta fija (ver `plan_negocios_sello.md` Secciones 3.2, 6.1, 7 y `modelo_financiero_sello_notas.md`). Ya corregido en `manual_funciones_im_music.xlsx` (hoja `00_Indice` filas 13-14, encabezados A1 de ambas hojas de rol, y nombres de las pestañas).

## El circuito interconectado (ejemplos clave)

- CEO firma artista → dispara Gerente Comercial (facturación) + Project Manager Élite 360 (onboarding).
- Gerente Comercial cierra producción externa → dispara Productor Musical.
- Productor Musical entrega → dispara Ingeniero de Sonido → masterización aprobada dispara Desarrollador (publicación) + Contador (tracking de regalías).
- Comunicadora define parrilla → dispara briefing simultáneo a Content Engine (automatizado), Filmmaker (material humano real) y Diseñadora (piezas bespoke) → recibe métricas de vuelta para ajustar el siguiente periodo.
- Un bug/caída de la plataforma (Desarrollador) puede bloquear el cobro de suscripciones que recibe el Contador — debe notificarse al CEO si afecta Élite 360.

## Automatizaciones ya cubiertas vs. deliberadamente humanas

La mayoría de los pasos repetitivos (generación de contenido masivo, reportes financieros, alertas de errores, conciliación bancaria, calificación inicial de leads) ya están marcadas como automatizables o ya automatizadas en el stack del proyecto (Content Engine, Máquina de Captación con IA, dashboards). Las decisiones creativas, de negociación, de criterio editorial y de representación legal quedan explícitamente marcadas como "deliberadamente humanas" — no se fuerza una automatización donde no aporta.
