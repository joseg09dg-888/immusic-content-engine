# Matriz de Riesgos IM Music — Notas

62 riesgos específicos en 8 categorías (Industria, Mercado, Político/Regulatorio, Financiero, Marca, Marketing, Administrativo/Comercial, Legal), cubriendo tanto el Sello como la Plataforma SaaS, con el formato de la matriz de referencia del usuario (ID, Probabilidad×Impacto, Estrategia de Mitigación, Plan de Contingencia, Responsable, fechas, Efectividad, Notas).

## Top 5 riesgos críticos (score más alto)

1. **R-FIN-001 / R-ADM-001 (25 — el máximo posible)**: Dependencia total del fundador para ventas, legal, dirección y relación con artistas, sin respaldo. Responsable: CEO/Director.
2. **R-MER-001 (20)**: La ocupación del roster Élite 360 no alcanza el supuesto modelado. Responsable: Gerente Comercial.
3. **R-MER-002 (20)**: Artistas emergentes no pueden sostener el ticket de $2.999,99 USD/mes. Responsable: CEO/Director.
4. **R-FIN-002 (20)**: El desarrollador único de la plataforma es un punto único de falla. Responsable: CEO/Director.
5. **R-LEG-001 (20)**: La plataforma maneja dinero de terceros sin revisión legal/seguridad todavía. Responsable: Asesor Legal Externo.

## Por qué casi todo está en "Pendiente" o "Planificada"

El sello no tiene artistas firmados y la plataforma es un prototipo pre-producción — no hay nada que mitigar "activamente" todavía porque la operación real no ha comenzado. Esto es honesto, no un error de la matriz.

**Importante:** esto NO significa que los riesgos sean poco probables por ser "del futuro". Varias probabilidades se ajustaron AL ALZA con evidencia de 14 casos reales documentados en la industria (ver sección siguiente) — la matriz predice lo que ya le pasó a otros, no se excusa en que "hoy no hay nada que mitigar".

## Casos reales usados como evidencia (14 citados con fuente)

1. **d4vd** — soltado por su sello y banneado de Twitch en 24h tras cargos de asesinato (2026) — hallels.com
2. **Jimmie Allen** — soltado por BBR Music Group tras demandas de abuso sexual (2023) — Variety
3. **Marilyn Manson** — soltado por Loma Vista tras acusaciones de abuso (2021)
4. **FN Meka** — soltado por Capitol Music Group en <2 semanas por contenido racista (2022) — PopSci
5. **Dr Disrespect** — Turtle Beach, NBA 2K24, Midnight Society y 49ers cortaron patrocinio en días tras ban de Twitch — tech4gamers.com, kotaku.com
6. **G FUEL** — perdió 75+ streamers patrocinados tras escándalo de 2022 — mein-mmo.de
7. **JPMorgan/AT&T** — retiraron pauta de Twitch tras denuncias de antisemitismo en la plataforma (2024) — Bloomberg
8. **Lucki vs. Empire Distribution** — demanda por romper exclusividad tras recibir +$600K USD de inversión — Complex
9. **Kyedae (Kick)** — denunció oferta de contrato más baja tras diagnóstico de cáncer — win.gg
10. **Megan Thee Stallion vs. 1501 Certified** — disputa por caracterización de álbum como mixtape (2022) — CBS News
11. **H.E.R. vs. MBK Entertainment** — demanda para anular contrato de servicios personales — Rolling Stone
12. **DistroKid / Sony vs. Trefuego** — DistroKid retuvo $14.000 USD de un artista por disputa de terceros — musicbusinessworldwide.com
13. **Amazon Music/DistroKid** — demanda activa (mar. 2025) por regalías no pagadas y shadowbanning — aapnews.aap.com.au
14. **UMG vs. DistroKid (2026)** y **UMG/Believe vs. TuneCore ($500M, acuerdo)** — distribución no autorizada de remixes y reclamos de copyright vía Content ID — musicbusinessworldwide.com, lawyer-monthly.com
15. **RBX vs. Spotify** — demanda colectiva por streams fraudulentos con bots que benefician a Drake y distorsionan el pool pro-rata (2025-2026) — rollingstone.com, thefader.com
16. **Michael Smith (EE.UU.)** — imputado criminalmente por esquema de streams falsos con IA/bots — digitalmusicnews.com
17. **PledgeMusic / Allegro Media Group / Music Dealers** — colapsos de plataformas que dejaron artistas/sellos sin cobrar o con catálogo bloqueado — hypebot.com, opb.org, slippedisc.com
18. **Meta/WhatsApp Business Policy Enforcement** (fuente oficial) — enforcement real contra cuentas que violan la política de mensajería — developers.facebook.com

## Roles usados (solo los reales del proyecto)

CEO/Director del Sello (el fundador, cubre legal rutinario), Gerente Comercial, Project Manager (Élite 360), Productor Musical/Ingeniero de Sonido, Contador (externo), Desarrollador full-stack (plataforma), Asesor Legal Externo (casos puntuales). No se usaron roles del archivo de referencia viejo que ya no existen (Traficker, Gerente Administrativo/RRHH, Director Artístico, etc.).

## Riesgo agregado en auditoría de consistencia: R-LEG-011

Se detectó que la matriz no tenía ningún riesgo sobre fuga de la metodología propietaria a través de Filmmaker, Diseñadora Gráfica y Comunicadora — los 3 roles que pasaron de freelance a planta fija precisamente por tener acceso a esa metodología (ver `plan_negocios_sello.md`). R-LEG-005 solo cubre el registro de marca ante la SIC, no esto. Se agregó **R-LEG-011** (Probabilidad 2 × Impacto 5 = Nivel 10), con mitigación anclada en el Acuerdo de Confidencialidad y la protección de secreto empresarial (Decisión 486) ya existentes en el Data Room.

## Estructura del archivo

- **Leyenda_Metodologia**: explica cada columna y la fórmula de Nivel de Riesgo.
- **Resumen_Top15_Criticos**: los 15 riesgos de mayor score en todo el documento, ordenados descendente.
- **Matriz_Completa**: las 8 secciones en mayúsculas, cada una ordenada por Nivel de Riesgo descendente.
