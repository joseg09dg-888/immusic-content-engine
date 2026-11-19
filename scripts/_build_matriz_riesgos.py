"""Matriz de riesgos exhaustiva - IM Music (Sello + Plataforma SaaS).
Formato ajustado a la referencia del usuario (matriz_riesgos_referencia.xlsx):
ID | Descripcion | Area de Impacto | Probabilidad | Impacto | Nivel de Riesgo | Estrategia de Mitigacion |
Plan de Contingencia | Responsable | Fecha de Implementacion | Fecha de Revision | Efectividad | Notas.
Secciones en mayusculas dentro de la hoja. Hoja de leyenda + hoja resumen top 15."""
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "sello_plan" / "matriz_riesgos_im_music.xlsx"

VIOLETA = "5E17EB"
BLANCO = "FFFFFF"
NEGRO_TXT = "241A36"
SECCION_FILL = "E4D9FA"
BAJO = "C6EFCE"
MEDIO = "FFEB9C"
ALTO = "FFC7A0"
CRITICO = "FFC7CE"

def banda(score):
    if score >= 16:
        return "Crítico"
    if score >= 11:
        return "Alto"
    if score >= 6:
        return "Medio"
    return "Bajo"

def color(score):
    return {"Crítico": CRITICO, "Alto": ALTO, "Medio": MEDIO, "Bajo": BAJO}[banda(score)]

CEO = "CEO/Director del Sello"
GC = "Gerente Comercial"
PM = "Project Manager (Élite 360)"
PROD = "Productor Musical / Ingeniero de Sonido"
CONT = "Contador (externo)"
DEV = "Desarrollador full-stack (plataforma)"
LEGAL = "Asesor Legal Externo (casos puntuales)"

# cada seccion: (titulo_mayuscula, prefijo_id, [filas])
# fila = (desc, area_impacto, prob, impacto, estrategia(lista str), contingencia, responsable, fecha_impl, fecha_rev, efectividad, notas)

SECCIONES = [
("RIESGOS DE INDUSTRIA", "IND", [
("IA generativa musical (Suno, Udio, etc.) devalúa la percepción de valor de la producción humana y reduce la disposición a pagar por desarrollo de artista real.",
 "Ingresos, Posicionamiento de marca", 4, 4,
 "*Posicionar la autenticidad/historia del artista humano como diferencial frente a la IA. *No competir en volumen de producción, competir en narrativa y metodología. *Monitorear adopción de IA generativa en la industria cada trimestre.",
 "Reposicionar el discurso de marca hacia 'desarrollo de artista real, no generado' en todo el material público; acelerar casos de éxito propios como evidencia.",
 CEO, "Continuo", "Trimestral", "Planificada",
 "Tendencia de industria observada 2024-2026; sin cifra de impacto específica verificada para este negocio."),
("Saturación de lanzamientos diarios en plataformas de streaming dificulta que un artista nuevo del roster sea descubierto orgánicamente.",
 "Ingresos, Catálogo", 5, 3,
 "*Pitching activo de playlists desde el primer lanzamiento. *Inversión en campañas pagadas dirigidas, no depender solo de descubrimiento orgánico. *Calendarizar lanzamientos evitando saturación de temporadas altas.",
 "Si un lanzamiento no genera tracción en las primeras 2 semanas, relanzar con una campaña de pauta dirigida y ajustar la estrategia de contenido del Content Engine.",
 GC, "Continuo", "Mensual", "Planificada",
 "Hecho de industria ampliamente documentado (miles de lanzamientos/día en DSPs)."),
("Cambio en el algoritmo de TikTok/Instagram Reels reduce drásticamente el alcance orgánico del Content Engine para el sello y la plataforma.",
 "Marketing, Captación de clientes", 4, 3,
 "*Diversificar canales (YouTube, email, WhatsApp) para no depender de un solo algoritmo. *Monitorear métricas de alcance semanalmente para detectar caídas tempranas.",
 "Reasignar presupuesto de pauta hacia el canal que sí esté funcionando (ej. YouTube o email) mientras se ajusta la estrategia de contenido al nuevo algoritmo.",
 CEO, "Continuo", "Mensual", "Planificada",
 "Riesgo estructural de cualquier negocio dependiente de redes sociales — sin mitigación histórica propia todavía."),
("Spotify/YouTube cambian términos de API o reparto de regalías, reduciendo el margen de distribuidores pequeños como la plataforma.",
 "Ingresos, Operaciones (Plataforma)", 3, 4,
 "*Monitoreo activo de changelogs de API de Spotify/YouTube. *Cláusulas de salida con proveedores de distribución. *Evaluar un segundo agregador de distribución como respaldo.",
 "Migrar la integración afectada a un agregador alternativo en un plazo máximo de 30 días; comunicar proactivamente a los usuarios afectados.",
 DEV, "Continuo", "Trimestral", "Pendiente",
 "Riesgo de plataforma ya documentado en el plan de negocios del SaaS."),
("Consolidación de competidores DIY (ej. adquisición de un distribuidor por un player más grande) que baje precios agresivamente.",
 "Participación de mercado, Precios", 3, 3,
 "*Diferenciación en Élite 360 (no replicable por software) como ancla de defensa. *No competir en precio puro en Básico/Pro.",
 "Reforzar comunicación del diferencial Élite 360 y evaluar un ajuste táctico temporal de precio en Básico si la presión de mercado es sostenida.",
 CEO, "Continuo", "Semestral", "Planificada",
 "Supuesto — dinámica normal de mercados SaaS maduros."),
("Caída del formato álbum/EP en favor de singles sueltos reduce el valor de catálogo acumulado proyectado para el sello.",
 "Ingresos, Catálogo", 3, 2,
 "*Adoptar estrategia de lanzamiento continuo de singles en vez de álbumes desde el primer artista firmado.",
 "Replanificar el roadmap de lanzamientos del artista afectado hacia singles mensuales en vez de un álbum completo.",
 PROD, "Al firmar artista", "Anual", "Planificada",
 "Tendencia de industria documentada (IFPI, varios años)."),
("Nuevas plataformas de streaming regionales fragmentan la distribución y exigen integraciones adicionales no presupuestadas en la plataforma.",
 "Operaciones, Costos de desarrollo (Plataforma)", 2, 2,
 "*Monitorear crecimiento de nuevas plataformas antes de invertir en integración.",
 "Evaluar demanda real de usuarios antes de comprometer tiempo de desarrollo en una integración nueva.",
 DEV, "Según demanda", "Anual", "Pendiente",
 "Supuesto — bajo impacto a corto plazo, baja prioridad."),
("Dependencia de las políticas de la plataforma de streaming en vivo (Twitch/Kick/YouTube) del creador aliado — ban, cambio de monetización, o caída de audiencia fuera del control del sello.",
 "Ingresos, Exposición de marca (Alianza de streamer)", 3, 4,
 "*Diversificar el acuerdo para que la exposición de marca no dependa de una sola plataforma de streaming. *Monitorear el estado de la cuenta y las políticas de la plataforma del creador antes y durante la alianza.",
 "Si el streamer es banneado o pierde audiencia significativa, evaluar la migración del acuerdo a otra plataforma o renegociar los términos de exposición pactados.",
 GC, "Al negociar la alianza", "Mensual", "Pendiente",
 "Nueva línea de negocio: el sello financia el setup de transmisión de un creador a cambio de exposición de marca/roster."),
]),

("RIESGOS ESTRATÉGICOS Y DE MERCADO", "MER", [
("La ocupación del roster Élite 360 no alcanza el supuesto modelado (30%→70% Colombia, 15%→55% Dubái) por falta de artistas dispuestos/calificados.",
 "Ingresos, Viabilidad del modelo financiero", 4, 5,
 "*Pipeline de captación activo desde el mes 1, no depender de leads entrantes (inbound). *Revisar el supuesto de ocupación cada trimestre contra resultados reales.",
 "Si la ocupación cae por debajo del 50% del supuesto durante 2 trimestres seguidos, recortar el equipo de Élite 360 proporcionalmente y recalcular el punto de equilibrio.",
 GC, "Inmediato", "Trimestral", "Pendiente",
 "Supuesto crítico señalado explícitamente en el Modelo Financiero del Sello — no validado con datos reales."),
("Artistas emergentes no pueden sostener el ticket de USD $2.999,99/mes (~$36.000/año) del servicio Élite 360.",
 "Ingresos, Modelo de negocio", 4, 5,
 "*Explorar estructuras de pago alternativas (parte en regalías futuras o equity del artista) para talento de alto potencial y bajo flujo de caja. *Validar capacidad de pago en la etapa de scouting, antes de ofertar el contrato.",
 "Si un candidato de alto potencial no puede pagar el ticket completo, ofrecer un esquema híbrido (fee reducido + mayor % de regalías) en vez de perder al artista.",
 CEO, "Al firmar artista", "Por contrato", "Pendiente",
 "Precio real del producto; capacidad de pago de artistas emergentes es un supuesto no validado con datos reales."),
("Adopción de los planes Básico/Pro de la plataforma más lenta de lo modelado porque cobran mensualmente lo que la competencia (DistroKid/TuneCore) cobra anualmente.",
 "Ingresos, Crecimiento de suscriptores (Plataforma)", 4, 4,
 "*Evaluar planes anuales con descuento para igualar la percepción de precio de la competencia. *Comunicar el valor agregado frente al precio desde el primer contacto.",
 "Si la conversión está 50% por debajo de lo modelado tras el primer semestre de lanzamiento, introducir un plan anual con descuento como oferta de entrada.",
 CEO, "Al lanzar", "Trimestral", "Pendiente",
 "Riesgo de adopción ya flagueado en el plan de negocios del SaaS."),
("La demanda real de música latina/urbana en EAU resulta mucho menor que las señales cualitativas (J Balvin en UNTOLD, Dubai Latin Fest) sugieren.",
 "Ingresos, Viabilidad del escenario Dubái", 4, 4,
 "*Investigación de mercado local pagada antes de comprometer capital completo. *Ejecutar únicamente el escenario lean/por fases hasta validar demanda real.",
 "Si tras 12 meses en el escenario lean la demanda sigue sin materializarse, pausar la expansión a Dubái y reconcentrar el capital en Medellín.",
 CEO, "Antes de relocalizar", "Semestral", "Pendiente",
 "No existe cifra país-específica de EAU verificable — limitación de datos ya explícita en el plan del sello."),
("Los supuestos de TAM/SAM/SOM de Colombia (15%-25% del TAM como segmento urbano/independiente) no se confirman con fuentes oficiales.",
 "Proyecciones de mercado", 3, 3,
 "*Validar con Procolombia o Mincultura antes de comprometer capital a escala con base en estas cifras.",
 "Si la validación oficial da una cifra distinta, recalcular el SOM y ajustar las proyecciones del modelo financiero antes de la siguiente ronda.",
 CEO, "Antes de ronda Seed", "Única vez", "Pendiente",
 "Supuesto a validar, ya señalado explícitamente en el plan de negocios del sello."),
("El mercado de producción musical boutique en Medellín ya está más competido de lo estimado por estudios locales establecidos.",
 "Ingresos, Captación de clientes de producción", 3, 3,
 "*Diferenciación por marca y metodología propia, no por precio. *Mapear activamente a los competidores locales (ej. 574, The Icon) antes del lanzamiento comercial.",
 "Si la captación de proyectos de producción externa está por debajo de la meta, ofrecer un paquete introductorio combinando producción + desarrollo de marca como diferencial.",
 GC, "Al lanzar", "Trimestral", "Pendiente",
 "Supuesto — no se investigó a fondo la competencia real de estudios locales en este plan."),
("Cambio en preferencias de consumo hacia géneros no cubiertos inicialmente por el roster.",
 "Catálogo, Posicionamiento", 2, 2,
 "*Roster deliberadamente multigénero por diseño (urbano, R&B, jazz, trap, regional, etc.), ya mitigado en el plan de negocios.",
 "Evaluar la incorporación de un artista del género en tendencia dentro del ciclo normal de scouting, sin necesidad de un plan de choque.",
 CEO, "Continuo", "Anual", "En Proceso",
 "Mitigación de diseño ya documentada explícitamente en el plan de negocios del sello."),
]),

("RIESGOS POLÍTICOS Y REGULATORIOS", "POL", [
("Reforma tributaria colombiana en curso en el Congreso cambia la tarifa de renta societaria (hoy 35% para SAS).",
 "Costos fiscales (Colombia)", 3, 3,
 "*Monitoreo activo del trámite de la reforma (PL 477) en el Congreso. *Modelar sensibilidad de +/-5 puntos porcentuales en el financiero.",
 "Si la reforma se aprueba, recalcular inmediatamente la utilidad neta proyectada y comunicar el impacto al inversionista en el siguiente reporte.",
 CONT, "Continuo", "Semestral", "Pendiente",
 "Proyecto de ley ya mencionado en el plan — bajaría la tarifa a 33%/31% en 2027-2028 si se aprueba."),
("Regulación de criptoactivos/valores (securities) se endurece justo cuando se quiera avanzar en financiamiento tokenizado de artistas.",
 "Legal, Roadmap de producto (Plataforma)", 3, 5,
 "*No lanzar esa funcionalidad sin opinión legal de valores en cada jurisdicción relevante. *Mantenerla como roadmap de largo plazo, nunca como funcionalidad comprometida ante inversionistas.",
 "Si la regulación se endurece antes del lanzamiento de esa función, retirarla del roadmap público hasta tener claridad jurídica completa.",
 LEGAL, "Antes de evaluar la función", "Anual", "Pendiente",
 "Ya flagueado explícitamente como no evaluado en el plan de negocios del SaaS."),
("Cambios en las reglas de zona franca o impuesto corporativo en EAU (el test de Qualifying Free Zone Person se endurece).",
 "Costos fiscales (Dubái)", 2, 4,
 "*Estructurar la operación para cumplir holgadamente el test de Qualifying Free Zone Person, no al límite del umbral de 5%/AED 5M.",
 "Si se pierde el estatus de 0% calificado, recalcular inmediatamente el impuesto al 9% y ajustar el flujo de caja de Dubái por los siguientes 5 años (periodo de pérdida del beneficio).",
 CONT, "Al constituir la entidad", "Anual", "Pendiente",
 "Regla real de la ley de impuesto corporativo de EAU, 2023."),
("La visa de inversionista/trabajo del fundador en Dubái se retrasa o se rechaza, afectando el cronograma de relocalización.",
 "Operaciones, Cronograma (Dubái)", 2, 4,
 "*Iniciar el trámite de visa con holgura de al menos 3 meses antes de la fecha de relocalización comprometida.",
 "Si la visa se retrasa, operar remotamente desde Colombia el tiempo necesario sin anunciar la relocalización como completada hasta tenerla en mano.",
 CEO, "3 meses antes de relocalizar", "Única vez", "Pendiente",
 "Costos/tiempos de visa estimados por consultoras, no oficiales — ya señalado en el plan."),
("Cambios en la implementación de EMRA (sociedad de gestión de derechos de EAU; tarifas comerciales desde dic. 2026) afectan los supuestos de regalías locales.",
 "Ingresos, Regalías (Dubái)", 3, 3,
 "*No proyectar ningún ingreso de EMRA hasta que exista un historial comercial real posterior a diciembre de 2026.",
 "Si EMRA retrasa aún más la entrada en vigencia de sus tarifas, extender el supuesto de 'ingreso especulativo' en el modelo financiero sin fecha límite nueva hasta tener confirmación oficial.",
 CONT, "Post diciembre 2026", "Anual", "Pendiente",
 "EMRA licenciada en abril de 2025 bajo la Ley Federal 38/2021 — sin historial operativo todavía."),
("Restricciones cambiarias o de repatriación de capital entre Colombia y los Emiratos Árabes Unidos.",
 "Flujo de caja, Repatriación de utilidades", 2, 3,
 "*Estructurar los flujos de caja considerando los controles de cambio vigentes del Banco de la República antes de mover capital entre ambas entidades.",
 "Si surge una restricción nueva, consultar inmediatamente con el contador la vía legal de repatriación disponible (ej. inversión extranjera registrada) antes de mover fondos.",
 CONT, "Antes de operar en 2 países", "Anual", "Pendiente",
 "Supuesto — no investigado a fondo en este plan."),
("Cambios arancelarios del Consejo de Cooperación del Golfo (CCG) sobre importación de equipo de estudio hacia Dubái.",
 "Costos de CAPEX (Dubái)", 2, 2,
 "*Cotizar el código arancelario exacto antes de importar. *Considerar comprar equipo localmente en EAU en vez de importarlo si el arancel sube.",
 "Si el arancel aumenta de forma significativa, comprar el equipo de reemplazo localmente en Dubái en vez de importar.",
 CEO, "Antes de importar equipo", "Única vez", "Pendiente",
 "Arancel general del 5% CIF ya referenciado — código específico sin verificar."),
]),

("RIESGOS FINANCIEROS", "FIN", [
("Dependencia de una sola persona (el fundador) para ventas, legal, dirección y relación con artistas simultáneamente, sin respaldo operativo.",
 "Continuidad del negocio, Operaciones", 5, 5,
 "*Documentar los procesos clave (ventas, contratos tipo, relación con artistas) desde el día 1. *Contratar un segundo rol de respaldo tan pronto el flujo de caja lo permita.",
 "Si el fundador queda incapacitado temporalmente, activar los poderes delegados al contador para mantener la operación básica (pagos, nómina, obligaciones fiscales) mientras se resuelve.",
 CEO, "Inmediato", "Trimestral", "Pendiente",
 "Riesgo estructural de la operación lean definida en ambos planes de negocio — máximo impacto posible (score 25)."),
("El desarrollador único de la plataforma es un punto único de falla (key-person risk) tanto técnico como financiero.",
 "Continuidad de la plataforma, Costos de reemplazo", 4, 5,
 "*Documentación técnica exhaustiva del código desde ahora. *Evaluar un segundo desarrollador contratista de respaldo apenas haya ingreso suficiente para cubrirlo.",
 "Si el desarrollador deja el proyecto, usar la documentación técnica para contratar un reemplazo urgente vía freelance mientras se evalúa una contratación permanente.",
 CEO, "Inmediato", "Trimestral", "Pendiente",
 "Ya identificado explícitamente en el plan de negocios del SaaS."),
("Concentración de ingreso en muy pocos clientes Élite 360 (perder 1 de 12-15 representa un golpe significativo al ingreso mensual).",
 "Ingresos, Estabilidad de caja", 3, 4,
 "*Contratos con cláusula de permanencia mínima. *Mantener un pipeline de artistas candidatos de reemplazo activo en todo momento.",
 "Si se pierde un cliente Élite 360, activar inmediatamente al siguiente candidato del pipeline y renegociar el presupuesto de marketing del mes para compensar el hueco de ingreso.",
 GC, "Al firmar cada contrato", "Mensual", "Pendiente",
 "Estructura de negocio de capacidad limitada ya definida por diseño."),
("Necesidad de una segunda ronda de capital antes de llegar a flujo de caja positivo si la adopción es más lenta de lo modelado en cualquiera de los 2 negocios.",
 "Runway, Continuidad de operación", 3, 4,
 "*Negociar con el primer inversionista la posibilidad de un puente de capital adicional desde el cierre de la ronda inicial, no esperar a quedarse sin caja.",
 "Si el runway cae por debajo de 3 meses, activar la conversación de puente de inmediato y, en paralelo, recortar gasto no esencial (pauta, viajes) para extender la caja disponible.",
 CEO, "Continuo", "Mensual", "Pendiente",
 "El financiero del SaaS muestra Año 1 en pérdida; el sello en Dubái (escenario completo) nunca es positivo en 5 años."),
("Tarifas de afiliación a SAYCO/ACINPRO no confirmadas afectan la estructura real de costos del sello.",
 "Costos operativos (Sello)", 3, 3,
 "*Confirmar las tarifas vigentes llamando directamente a ambas entidades antes de presentar el financiero a un inversionista como cifra cerrada.",
 "Si la tarifa real resulta mayor a la estimada, absorberla en el primer trimestre operativo y ajustar el OPEX del resto del año.",
 CONT, "Antes de afiliarse", "Única vez", "Pendiente",
 "Ninguna entidad publica tarifa vigente para 2025 — ya señalado en el plan."),
("Costos de constitución/licencia de zona franca en Dubái son estimaciones de consultoras, no tarifas oficiales.",
 "CAPEX, Costos de constitución (Dubái)", 3, 3,
 "*Cotizar directamente con la zona franca elegida (Dubai Media City, IFZA, etc.) antes de comprometer el presupuesto final.",
 "Si el costo real excede lo presupuestado en más de 20%, reevaluar la zona franca elegida por una más económica antes de constituir la entidad.",
 CEO, "Antes de constituir entidad", "Única vez", "Pendiente",
 "Rango AED 12.900-45.000/año de fuentes de consultoría, sin verificar oficialmente."),
("Riesgo de tipo de cambio COP/USD/AED sobre las proyecciones multi-moneda de ambos modelos financieros.",
 "Rentabilidad proyectada", 4, 3,
 "*Sensibilizar el modelo a variaciones de +/-15% en la TRM y en el tipo de cambio AED/USD, no fijar una tasa única.",
 "Si una devaluación brusca afecta materialmente el margen, renegociar temporalmente los precios de servicios cotizados en moneda local (COP) para proteger el margen en USD.",
 CONT, "Continuo", "Mensual", "Pendiente",
 "Los modelos usan tasas de referencia aproximadas, no cubiertas (hedged) con instrumentos financieros."),
("Costo real de la auditoría de seguridad/legal de la plataforma no presupuestado con precisión (~USD $20.000 estimado).",
 "CAPEX de productización (Plataforma)", 3, 3,
 "*Cotizar con al menos 2 firmas de auditoría de seguridad/legal antes de comprometer el presupuesto final de la ronda pre-seed.",
 "Si el costo real excede el presupuesto, priorizar primero la auditoría de seguridad (manejo de dinero de terceros) y posponer alcances legales menores a una segunda fase.",
 CEO, "Antes de producción", "Única vez", "Pendiente",
 "Estimación propia del financiero del SaaS, no cotizada con una firma real todavía."),
]),

("RIESGOS DE MARCA Y REPUTACIÓN", "MAR", [
("Ejecución inconsistente de la identidad REBEL LUXURY (piezas genéricas, fuera de estándar) diluye el valor del intangible más importante del negocio.",
 "Valor de marca, Percepción de inversionistas", 3, 4,
 "*Revisión de marca obligatoria antes de publicar cualquier pieza, sin excepción, aplicado tanto al Content Engine como al equipo humano.",
 "Si se detecta una pieza fuera de estándar ya publicada, retirarla o corregirla dentro de las 24 horas siguientes y reforzar el checklist de revisión.",
 CEO, "Inmediato", "Continuo", "En Proceso",
 "Señalado explícitamente por el fundador como el activo más importante del negocio."),
("El Content Engine automatizado produce contenido que se percibe como genérico o de baja calidad tipo IA, dañando la percepción premium de la marca.",
 "Percepción de marca, Engagement", 3, 4,
 "*Curaduría humana obligatoria antes de publicar cualquier pieza generada por el Content Engine, nunca publicar sin revisión.",
 "Si una pieza de baja calidad ya se publicó, retirarla y reemplazarla, y ajustar los prompts/parámetros del Content Engine que la generaron.",
 CEO, "Inmediato", "Continuo", "En Proceso",
 "Riesgo estructural de cualquier content engine automatizado — mitigación de diseño ya aplicada."),
("Un escándalo o mala conducta pública de un artista firmado daña la reputación de todo el sello.",
 "Reputación, Valor de marca", 2, 5,
 "*Incluir cláusulas de conducta en todos los contratos de artista. *Debida diligencia básica de reputación antes de firmar a cualquier artista.",
 "Ante un escándalo, emitir una declaración pública clara y oportuna, evaluar la suspensión o terminación del contrato según la gravedad, y proteger activamente al resto del roster de la asociación mediática.",
 CEO, "Al firmar artista", "Por contrato", "Pendiente",
 "Riesgo estándar de la industria discográfica — aún no hay ningún contrato firmado."),
("Confusión de marca entre 'el sello', 'la plataforma' y 'el libro' si no se comunican consistentemente como un ecosistema coherente.",
 "Percepción de marca, Claridad comercial", 3, 3,
 "*Replicar la arquitectura de marca ya definida en los planes de negocio de forma consistente en todo material público y de inversionista.",
 "Si se detecta confusión en el mercado o con un inversionista, aclarar explícitamente la relación entre las 3 unidades en la siguiente comunicación oficial.",
 CEO, "Continuo", "Continuo", "En Proceso",
 "Jerarquía de marca ya documentada en el plan del sello."),
("Percepción de exageración ('vaporware') si se comunica el módulo blockchain simulado como si fuera funcional ante un inversionista o el público.",
 "Credibilidad ante inversionistas", 2, 4,
 "*Comunicación siempre honesta sobre el estado real del módulo blockchain (roadmap, no funcional) en todo pitch o material público — ya mitigado por diseño.",
 "Si alguien presenta el módulo como funcional por error, corregir públicamente de inmediato y reforzar la política interna de comunicación honesta del estado del producto.",
 CEO, "Continuo", "Continuo", "Efectiva",
 "Mitigación de diseño ya aplicada explícitamente en el plan de negocios del SaaS."),
("Comparación pública desfavorable con sellos/plataformas establecidas por falta de trayectoria o de casos de éxito propios.",
 "Percepción de marca, Credibilidad comercial", 3, 2,
 "*Liderar la comunicación con la metodología y el producto, no con comparaciones de tamaño o antigüedad frente a la competencia.",
 "Si surge una comparación desfavorable en redes o medios, responder con casos de uso concretos en vez de defender la trayectoria.",
 GC, "Continuo", "Continuo", "Pendiente",
 "Supuesto — riesgo normal de cualquier entrante nuevo en un mercado con jugadores establecidos."),
("El creador de contenido en vivo (streamer) financiado por el sello genera contenido controversial o dañino para la marca REBEL LUXURY (riesgo reputacional por asociación).",
 "Reputación, Valor de marca (Alianza de streamer)", 3, 4,
 "*Debida diligencia de contenido e historial del streamer antes de financiar su setup. *Incluir cláusula de conducta y de desasociación inmediata en caso de controversia.",
 "Ante contenido dañino del streamer, desasociar la marca públicamente de inmediato y evaluar la terminación del acuerdo según la cláusula de conducta pactada.",
 CEO, "Al firmar la alianza", "Por acuerdo", "Pendiente",
 "Nueva línea de negocio: el sello financia el setup de transmisión de un creador a cambio de exposición de marca/roster."),
]),

("RIESGOS DE MARKETING", "MKT", [
("Los bots de WhatsApp y el DM automático en redes sociales de la 'Máquina de Captación' violan las políticas anti-spam de Meta/WhatsApp, generando restricción o baneo de cuenta.",
 "Captación de clientes, Continuidad operativa", 4, 4,
 "*Usar exclusivamente la WhatsApp Business API oficial. *Cumplir estrictamente los límites de mensajería de Meta. *Nunca enviar mensajes masivos no solicitados.",
 "Si una cuenta es restringida, activar inmediatamente el canal de respaldo (email marketing) mientras se resuelve el caso con soporte de Meta/WhatsApp.",
 CEO, "Al implementar la Máquina de Captación", "Mensual", "Pendiente",
 "Riesgo técnico real de la 'Máquina de Captación' descrita en el organigrama funcional del sello."),
("Contenido generado por IA del Content Engine contiene un error de marca o un error factual visible públicamente.",
 "Reputación, Percepción de marca", 3, 4,
 "*Revisión humana obligatoria pre-publicación, sin excepción — ya establecido como regla del negocio.",
 "Si un error ya se publicó, retirarlo o corregirlo en menos de 24 horas y comunicar la corrección si ya tuvo alcance significativo.",
 CEO, "Inmediato", "Continuo", "En Proceso",
 "Riesgo estructural de automatización de contenido, mitigado por la misma regla de revisión de marca."),
("Dependencia de algoritmos de redes sociales fuera de control de la empresa para el alcance orgánico de ambos negocios.",
 "Captación de clientes, Alcance orgánico", 4, 3,
 "*Diversificar hacia email marketing y el canal YouTube propio para no depender de un solo algoritmo.",
 "Si un canal cae en alcance de forma sostenida, redistribuir el presupuesto y el calendario de contenido hacia el canal que sí esté funcionando.",
 CEO, "Continuo", "Mensual", "Pendiente",
 "Riesgo estructural de cualquier estrategia de marketing digital."),
("El email marketing automatizado es marcado como spam, dañando la entregabilidad de todas las campañas futuras.",
 "Captación de clientes, Reputación de dominio", 3, 3,
 "*Prácticas de deliverability: opt-in claro, listas limpias, monitoreo de tasa de rebote y de quejas de spam.",
 "Si la entregabilidad cae, pausar envíos masivos, limpiar la lista de contactos inactivos, y recalentar el dominio gradualmente antes de retomar el volumen normal.",
 DEV, "Al implementar email marketing", "Mensual", "Pendiente",
 "Riesgo técnico estándar de email marketing automatizado."),
("Presupuesto de marketing pagado insuficiente para competir por atención contra sellos/plataformas con más capital.",
 "Captación de clientes, Crecimiento", 3, 3,
 "*Priorizar canales orgánicos/de bajo costo (Content Engine propio) sobre pauta pagada en la etapa inicial.",
 "Si la pauta pagada no rinde el ROAS esperado, reasignar el presupuesto completo a los canales orgánicos ya validados.",
 GC, "Continuo", "Mensual", "Pendiente",
 "Supuesto — operación lean con presupuesto de pauta limitado por diseño."),
("Dependencia de un solo canal de captación (ej. solo Instagram) sin diversificación real entre WhatsApp, redes y email.",
 "Captación de clientes, Resiliencia comercial", 2, 3,
 "*La Máquina de Captación está diseñada multicanal desde el inicio (WhatsApp + redes + email), mitigado por diseño.",
 "Si un canal falla, los otros dos ya están activos por diseño — reforzar temporalmente el presupuesto de los canales restantes.",
 GC, "Continuo", "Mensual", "En Proceso",
 "Mitigación de diseño ya documentada en el organigrama funcional."),
]),

("RIESGOS ADMINISTRATIVOS Y COMERCIALES", "ADM", [
("Dependencia total del fundador para ventas, legal, dirección y relación con artistas simultáneamente, sin respaldo operativo diario.",
 "Operaciones diarias, Continuidad", 5, 5,
 "*Documentar procesos clave desde el día 1 (plantillas de venta, contrato, onboarding). *Contratar respaldo tan pronto el flujo de caja lo permita.",
 "Ante una sobrecarga crítica, priorizar explícitamente: cierre de ventas > relación con artistas firmados > tareas administrativas postergables.",
 CEO, "Inmediato", "Trimestral", "Pendiente",
 "Riesgo estructural ya identificado en Financiero — se repite aquí por su impacto directo en la operación diaria."),
("El desarrollador único de la plataforma es un punto único de falla operativo, no solo financiero (nadie más puede dar soporte técnico diario).",
 "Operaciones de la plataforma, Soporte", 4, 5,
 "*Documentación técnica exhaustiva del código y de los procesos de despliegue. *Plan de contingencia escrito si el desarrollador no puede continuar.",
 "Activar inmediatamente la documentación técnica para onboarding de emergencia de un desarrollador freelance de respaldo.",
 CEO, "Inmediato", "Trimestral", "Pendiente",
 "Ya identificado en el plan de negocios del SaaS — aparece también en Financiero por su doble naturaleza."),
("Falta de procesos documentados de onboarding de artistas del roster o de clientes de la plataforma.",
 "Experiencia del cliente, Eficiencia operativa", 4, 3,
 "*Documentar el proceso de onboarding desde el primer cliente/artista real, no esperar a tener volumen para formalizarlo.",
 "Si el primer onboarding revela vacíos de proceso, documentarlos inmediatamente después de ese primer caso, antes del segundo.",
 GC, "Al primer cliente/artista real", "Trimestral", "Pendiente",
 "La operación aún no tiene ningún cliente/artista real sobre el cual probar el proceso."),
("Dificultad para contratar al Project Manager/equipo de Élite 360 con el perfil correcto (experiencia real en management musical).",
 "Capacidad de entrega del servicio, Calidad", 3, 4,
 "*Iniciar la búsqueda de candidatos con antelación al primer contrato Élite 360 firmado, no después.",
 "Si no hay candidato listo al momento de firmar el primer cliente Élite 360, el CEO/Director cubre temporalmente el rol de PM hasta cerrar la contratación.",
 CEO, "Antes del primer contrato Élite 360", "Única vez", "Pendiente",
 "Perfil especializado y escaso en el mercado laboral de Medellín — supuesto no validado."),
("Falta de un plan de sucesión o continuidad operativa si el fundador no puede operar temporalmente (enfermedad, viaje, fuerza mayor).",
 "Continuidad del negocio", 2, 5,
 "*Delegar poderes legales y de firma a una segunda persona de confianza (ej. el contador) para continuidad operativa básica.",
 "Activar los poderes delegados de inmediato para sostener pagos, nómina y obligaciones fiscales mientras el fundador no puede operar.",
 CEO, "Inmediato", "Anual", "Pendiente",
 "No existe plan de sucesión documentado hoy."),
("Crecimiento desordenado del roster más allá de la capacidad real del equipo humano de Élite 360.",
 "Calidad del servicio, Reputación", 3, 4,
 "*Respetar estrictamente el tope de 12-15 artistas por diseño, no sobrevender el servicio por presión de ingresos.",
 "Si la demanda supera el tope, crear lista de espera formal en vez de aceptar más clientes de los que el equipo puede atender con calidad.",
 GC, "Continuo", "Mensual", "En Proceso",
 "Tope de capacidad ya definido por diseño en el plan de negocios del sello."),
]),

("RIESGOS LEGALES", "LEG", [
("La plataforma maneja dinero de terceros (regalías) sin revisión legal ni de seguridad todavía — riesgo de responsabilidad fiduciaria.",
 "Legal, Cumplimiento, Reputación (Plataforma)", 4, 5,
 "*No lanzar a producción con dinero real sin una auditoría de seguridad y una revisión legal completa de los términos de servicio.",
 "Si se detecta una brecha antes de corregirla, suspender inmediatamente el manejo de fondos reales y notificar a los usuarios afectados de forma transparente.",
 LEGAL, "Antes de producción", "Única vez", "Pendiente",
 "Ya identificado como brecha crítica en el plan de negocios del SaaS."),
("Contratos de artista mal estructurados generan disputas de derechos de autor o de regalías con el primer roster.",
 "Legal, Relación con artistas", 3, 4,
 "*Plantilla de contrato revisada por un abogado especializado en entretenimiento antes de firmar al primer artista real.",
 "Ante una disputa, intentar conciliación directa primero; escalar a asesoría legal externa puntual solo si la conciliación falla.",
 CEO, "Antes del primer contrato", "Por contrato", "Pendiente",
 "Riesgo estándar de la industria — aún no hay ningún contrato de artista firmado."),
("Derechos de autor de contenido subido por usuarios de la plataforma sin verificación de que tienen derecho legal a distribuirlo.",
 "Legal, Cumplimiento de copyright (Plataforma)", 3, 4,
 "*Proceso de verificación de derechos (declaración firmada + chequeo de Content ID) antes de distribuir cualquier obra a las plataformas de streaming.",
 "Si se detecta contenido distribuido sin derechos, retirarlo de inmediato de todas las plataformas y suspender la cuenta del usuario responsable.",
 DEV, "Antes de producción", "Continuo", "Pendiente",
 "Riesgo ya identificado en el plan de negocios del SaaS."),
("Implicaciones de valores/securities si se avanza con financiamiento tokenizado de artistas sin evaluación legal previa.",
 "Legal, Roadmap de producto (Plataforma)", 2, 5,
 "*No lanzar esta función sin opinión legal de valores en cada jurisdicción relevante — mantenerla como roadmap, nunca como funcionalidad comprometida.",
 "Si se recibe un requerimiento regulatorio antes del lanzamiento, retirar la función del roadmap público de inmediato hasta resolver la situación legal.",
 LEGAL, "Antes de evaluar la función", "Anual", "Pendiente",
 "Ya flagueado explícitamente como no evaluado en el plan de negocios del SaaS."),
("Registro de marca 'IM Music' no completado ante la Superintendencia de Industria y Comercio (SIC).",
 "Legal, Propiedad intelectual", 3, 3,
 "*Iniciar el registro de marca ante la SIC lo antes posible, antes de que un tercero pueda registrarla primero.",
 "Si un tercero ya registró una marca similar, evaluar con un abogado de PI la vía de oposición o el cambio de nombre comercial como última opción.",
 CEO, "Inmediato", "Única vez", "Pendiente",
 "No se confirmó en este proyecto si el registro de marca ya se inició."),
("Incumplimiento de la Ley 1581 de 2012 de protección de datos personales en Colombia por parte de la plataforma.",
 "Legal, Cumplimiento de datos (Plataforma)", 2, 4,
 "*Política de tratamiento de datos y aviso de privacidad revisados por un abogado antes de lanzar a producción.",
 "Si se recibe un reclamo o requerimiento de la SIC, responder dentro de los plazos legales y corregir la política/proceso señalado de inmediato.",
 LEGAL, "Antes de producción", "Anual", "Pendiente",
 "Ya identificado en el plan de negocios del SaaS."),
("Cumplimiento PCI-DSS delegado a Stripe/Wompi, pero sin auditoría de que la integración no filtre datos sensibles en logs o base de datos.",
 "Legal, Seguridad de pagos (Plataforma)", 2, 4,
 "*Auditoría de logs y almacenamiento antes de producción. *Nunca almacenar datos de tarjetas propios bajo ninguna circunstancia.",
 "Si se detecta una filtración de datos sensibles en logs, purgarlos de inmediato, notificar a los usuarios afectados y a Stripe/Wompi, y corregir el código responsable.",
 DEV, "Antes de producción", "Única vez", "Pendiente",
 "Ya identificado en el plan de negocios del SaaS."),
("El acuerdo con el streamer no está bien contractualizado (exclusividad, duración, qué pasa si se va a otra marca después de recibir el setup financiado) — riesgo de perder la inversión en equipo sin retorno.",
 "Legal, CAPEX (Alianza de streamer)", 3, 4,
 "*Contrato que ate el financiamiento del setup a un periodo de exclusividad y permanencia mínimos. *Cláusula de devolución/compensación si el streamer rompe el acuerdo antes de tiempo.",
 "Si el streamer se va antes de cumplir el periodo pactado, activar la cláusula de devolución/compensación y recuperar el equipo financiado si es físicamente posible.",
 LEGAL, "Antes de financiar el setup", "Por acuerdo", "Pendiente",
 "Nueva línea de negocio: el sello financia el setup de transmisión de un creador a cambio de exposición de marca/roster — sin contrato firmado todavía."),
]),
]

def build():
    wb = openpyxl.Workbook()
    header_font = Font(color=BLANCO, bold=True, size=11)
    header_fill = PatternFill("solid", fgColor=VIOLETA)
    seccion_font = Font(bold=True, size=11, color=NEGRO_TXT)
    seccion_fill = PatternFill("solid", fgColor=SECCION_FILL)
    wrap = Alignment(wrap_text=True, vertical="top")

    cols = ["ID", "Descripción del Riesgo", "Área de Impacto", "Probabilidad (1-5)", "Impacto (1-5)",
            "Nivel de Riesgo (D×E)", "Estrategia de Mitigación", "Plan de Contingencia",
            "Responsable de la Mitigación", "Fecha de Implementación", "Fecha de Revisión",
            "Efectividad de la Mitigación", "Notas/Comentarios"]
    widths = [12, 46, 26, 12, 10, 12, 42, 38, 28, 20, 14, 16, 36]

    # ---- Hoja 1: Leyenda / Metodología ----
    wsL = wb.active
    wsL.title = "Leyenda_Metodologia"
    wsL.column_dimensions["A"].width = 30
    wsL.column_dimensions["B"].width = 95
    leyenda = [
        ("MATRIZ DE RIESGOS — IM MUSIC (Sello + Plataforma SaaS)", ""),
        ("", ""),
        ("Columna A (ID)", "Identificador único del riesgo. Prefijo de 3 letras por categoría + número secuencial (ej. R-MER-001)."),
        ("Columna B (Descripción del Riesgo)", "Descripción específica y concreta del riesgo — no genérica."),
        ("Columna C (Área de Impacto)", "Área del negocio afectada si el riesgo se materializa (ingresos, legal, reputación, operaciones, etc.)."),
        ("Columna D (Probabilidad)", "Escala 1 (muy baja) a 5 (muy alta) de que el riesgo ocurra."),
        ("Columna E (Impacto)", "Escala 1 (muy bajo) a 5 (muy alto) del efecto si el riesgo ocurre."),
        ("Columna F (Nivel de Riesgo)", "Probabilidad × Impacto (máximo 25). Bandas: 1-5 Bajo, 6-10 Medio, 11-15 Alto, 16-25 Crítico."),
        ("Columna G (Estrategia de Mitigación)", "Acciones PREVENTIVAS concretas para reducir probabilidad y/o impacto antes de que el riesgo ocurra."),
        ("Columna H (Plan de Contingencia)", "Acciones REACTIVAS — qué hacer específicamente SI el riesgo ya se materializó, distinto de la mitigación preventiva."),
        ("Columna I (Responsable de la Mitigación)", "Rol real del proyecto responsable — solo roles que existen hoy: CEO/Director del Sello, Gerente Comercial, Project Manager (Élite 360), Productor Musical/Ingeniero de Sonido, Contador (externo), Desarrollador full-stack (plataforma), Asesor Legal Externo (casos puntuales)."),
        ("Columna J (Fecha de Implementación)", "Cuándo se implementa la mitigación (Inmediato, Continuo, Al firmar artista, Antes de producción, etc.) — no fechas fijas, ya que el negocio aún no opera."),
        ("Columna K (Fecha de Revisión)", "Periodicidad de revisión de la efectividad de la mitigación (Mensual, Trimestral, Semestral, Anual, Única vez, Por contrato)."),
        ("Columna L (Efectividad de la Mitigación)", "Estado actual: Planificada (definida, no ejecutada) / En Proceso (parcialmente aplicada) / Efectiva (aplicada y funcionando) / Crítica (requiere atención urgente) / Pendiente (no iniciada)."),
        ("Columna M (Notas/Comentarios)", "Fuente del dato o supuesto detrás del riesgo, y contexto adicional relevante."),
        ("", ""),
        ("Nota sobre el estado real del negocio", "El sello no tiene artistas firmados todavía y la plataforma SaaS es un prototipo pre-producción — por eso casi todas las mitigaciones están en estado 'Planificada' o 'Pendiente', no 'Efectiva'. Esto es honesto, no un error: no hay nada que mitigar activamente todavía porque la operación real no ha comenzado."),
    ]
    for r in leyenda:
        wsL.append(r)
    wsL["A1"].font = Font(bold=True, size=14, color=VIOLETA)
    for row in wsL.iter_rows(min_row=3, max_row=wsL.max_row):
        for c in row:
            c.alignment = wrap

    # ---- construir filas con scoring ----
    all_rows = []  # (id, *fila, seccion)
    for titulo, prefijo, filas in SECCIONES:
        for i, f in enumerate(filas, start=1):
            desc, area, prob, impacto, estrat, contin, resp, fimpl, frev, efect, notas = f
            score = prob * impacto
            rid = f"R-{prefijo}-{i:03d}"
            all_rows.append((rid, desc, area, prob, impacto, score, estrat, contin, resp, fimpl, frev, efect, notas, titulo))

    # ---- Hoja 2: Resumen Top 15 ----
    ws1 = wb.create_sheet("Resumen_Top15_Criticos")
    ws1.append(cols)
    for j, w in enumerate(widths, start=1):
        ws1.column_dimensions[get_column_letter(j)].width = w
    for c in ws1[1]:
        c.font = header_font
        c.fill = header_fill
    top15 = sorted(all_rows, key=lambda r: r[5], reverse=True)[:15]
    for row in top15:
        ws1.append(list(row[:13]))
    for r in range(2, ws1.max_row + 1):
        ws1.cell(r, 6).fill = PatternFill("solid", fgColor=color(ws1.cell(r, 6).value))
        for c in range(1, 14):
            ws1.cell(r, c).alignment = wrap
    ws1.freeze_panes = "A2"

    # ---- Hoja 3: Matriz completa con secciones ----
    ws2 = wb.create_sheet("Matriz_Completa")
    ws2.append(cols)
    for j, w in enumerate(widths, start=1):
        ws2.column_dimensions[get_column_letter(j)].width = w
    for c in ws2[1]:
        c.font = header_font
        c.fill = header_fill

    for titulo, prefijo, filas in SECCIONES:
        sec_row = ws2.max_row + 1
        ws2.append([titulo] + [""] * 12)
        for col in range(1, 14):
            ws2.cell(sec_row, col).fill = seccion_fill
            ws2.cell(sec_row, col).font = seccion_font
        seccion_rows = sorted([r for r in all_rows if r[13] == titulo], key=lambda r: r[5], reverse=True)
        for row in seccion_rows:
            ws2.append(list(row[:13]))
    for r in range(2, ws2.max_row + 1):
        val = ws2.cell(r, 6).value
        if isinstance(val, (int, float)):
            ws2.cell(r, 6).fill = PatternFill("solid", fgColor=color(val))
        for c in range(1, 14):
            ws2.cell(r, c).alignment = wrap
    ws2.freeze_panes = "A2"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(OUT))
    print(f"OK: {OUT} ({OUT.stat().st_size // 1024}KB) — {len(all_rows)} riesgos totales")
    for titulo, prefijo, filas in SECCIONES:
        print(f"  {titulo}: {len(filas)}")
    print("TOP 5 GLOBAL:")
    for row in top15[:5]:
        print(f"  [{row[5]}] {row[0]} {row[1][:60]}... -> {row[8]}")

if __name__ == "__main__":
    build()
