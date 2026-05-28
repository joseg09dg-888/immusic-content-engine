# IM MUSIC — SISTEMA AUTOMATIZADO COMPLETO
**Fecha:** 2026-05-28  
**Versión:** 1.0  
**Concepto de marca:** REBEL LUXURY  
**Sello:** IM Music (@immusicsello)

---

## VISIÓN

Sistema automatizado que opera desde Claude Code con dos pilares paralelos:

- **PILAR A — CONTENT ENGINE**: Noticias virales de marketing/neurociencia → video YouTube + carrusel Instagram + TikTok, 3x semana, bilingüe ES+EN
- **PILAR B — MUSIC ENGINE**: Generación de beats chill hop / afro house → masterización profesional → visualizer animado REBEL LUXURY + galaxia → YouTube + release pack para Nexus

Todo 100% gratuito en stack técnico. Sin Canva pago. Sin Suno pago. Sin plataforma de distribución propia (usa Nexus con 8%).

---

## PILAR A — CONTENT ENGINE

### A1. Research Engine

**Fuentes monitoreadas (web scraping + RSS):**
- Marketing Week, Ad Age, Music Business Worldwide, Billboard
- Neuromarketing Science & Business, Nielsen Music, Variety
- Reddit: r/marketing, r/musicbusiness, r/psychology

**Referentes analizados (estudia su formato, no copia):**
1. Gary Vee — storytelling crudo, controversia real
2. Marketing Brew — noticias cortas, alto valor informativo
3. Seth Godin — profundidad conceptual, ángulos únicos
4. Music Business Worldwide — autoridad en industria musical
5. Hubspot Marketing — educación + datos

**Algoritmo de selección:**
- Score viralidad (shares + comentarios últimas 24h)
- Nivel controversial: MEDIO (no extremo, no tibio)
- Ángulo neurociencia/psicología: OBLIGATORIO en cada pieza
- Relevancia: marketing + industria musical + comportamiento del consumidor

**Output:** Brief estructurado con:
```json
{
  "titulo_principal": "",
  "angulo_neurociencia": "",
  "hook_apertura": "",
  "datos_clave": [],
  "controversia": "",
  "fuentes": []
}
```

### A2. Content Writer (Claude API)

**Por cada publicación genera:**
1. Guión completo YouTube (5-8 min) en español
2. Subtítulos EN (Whisper, automático)
3. Caption Instagram (hasta 2200 caracteres, hashtags optimizados)
4. Caption TikTok (150 caracteres + hashtags virales)
5. 3 variantes de título YouTube con SEO
6. Descripción YouTube con timestamps + keywords

**Framework obligatorio en cada pieza:**
- Apertura con hook neurológico (primeros 5 segundos)
- Dato sorprendente o estadística
- Ángulo de psicología/neurociencia como hilo conductor
- Controversia media: cuestiona algo establecido, no ataca personas
- CTA final con identidad IM Music

**Tono:** Autoridad + rebeldía intelectual + lujo de conocimiento

### A3. Design Engine (100% GRATUITO)

**Stack:** Python + Pillow + SVG programático + Remotion

**Identidad visual hardcodeada:**
```
Colores primarios: #000000 (negro) | #6200FF (violeta) | #FFFFFF (blanco)
Concepto:         REBEL LUXURY
Motivos:          Constelaciones, galaxia, líneas de luz, polvo estelar
Logo:             IM Music (versión actualizada 2026)
Tipografía:       La del branding actual (archivo local)
```

**Piezas generadas por publicación:**
- Thumbnail YouTube: 1280×720px, alta resolución, no genérico
- Carrusel Instagram: 8 slides, 1080×1080px, PNG calidad máxima
- Cover TikTok: 1080×1920px
- Story Instagram: 1080×1920px

### A4. Video Producer

**Stack:** FFmpeg + Whisper + ElevenLabs (free tier) o voz pregrabada

### A5. Publisher

**APIs (todas gratuitas):** YouTube Data API v3, Meta Graph API, TikTok Content Posting API

**Scheduler — 3x semana:**
```
Lunes:     YouTube 18:00 | Instagram 19:00 | TikTok 20:00
Miércoles: YouTube 18:00 | Instagram 19:00 | TikTok 20:00
Viernes:   YouTube 18:00 | Instagram 19:00 | TikTok 20:00
```

---

## PILAR B — MUSIC ENGINE

### B1. Beat Generator
**Stack:** AudioCraft (Meta, open source) + MusicGen
**Géneros:** Chill Hop (85-95 BPM) | Afro House (120-128 BPM)

### B2. Mastering Engine
**Stack:** Python + Librosa + PyDub + SoX + pyloudnorm
**Targets:** Spotify -14 LUFS | YouTube -13 LUFS | Apple Music -16 LUFS
**Exports:** WAV 24bit 44.1kHz | MP3 320kbps | FLAC | M4A 256kbps

### B3. Visualizer Engine (REBEL LUXURY + GALAXIA)
**Stack:** Manim + FFmpeg + Python + Librosa (análisis de audio reactivo)

**CHILL HOP — "El Viajero Nocturno"**
- Ciudad nocturna futurista, lluvia suave, neón violeta
- Constelaciones que forman el logo IM Music

**AFRO HOUSE — "El Ser Galáctico"**
- Galaxia abierta, nebulosas, polvo estelar que vibra con el beat
- Partículas reaccionan a kicks y bajos en tiempo real

### B4. Release Pack Generator
Genera estructura `/releases/YYYY-MM-DD_[nombre-track]/` con audio, video, artwork, metadata, nexus_delivery.

### B5. YouTube Music Publisher
Sube visualizer 4K + gestiona playlists automáticas.

---

## ARQUITECTURA TÉCNICA

```
Claude Code (orquestador maestro)
│
├── PILAR A: CONTENT ENGINE
│   ├── research.py       → web_search + RSS scraping
│   ├── writer.py         → Claude API (claude-sonnet-4-6)
│   ├── designer.py       → Pillow + SVG + Remotion
│   ├── video_producer.py → FFmpeg + Whisper + ElevenLabs
│   └── publisher.py      → YouTube + Meta + TikTok APIs
│
├── PILAR B: MUSIC ENGINE
│   ├── beat_generator.py → AudioCraft/MusicGen
│   ├── mastering.py      → Librosa + PyDub + SoX + pyloudnorm
│   ├── visualizer.py     → Manim + FFmpeg + audio-reactive
│   ├── release_pack.py   → genera estructura + ZIP Nexus
│   └── music_publisher.py → YouTube API + playlist manager
│
├── core/
│   ├── brand.py          → identidad visual centralizada
│   ├── scheduler.py      → orquesta timing de publicaciones
│   ├── config.py         → API keys, rutas, configuración
│   └── approval_cli.py   → aprobación de beats en terminal
│
└── assets/
    ├── logo/             → logo IM Music SVG + PNG
    ├── fonts/            → tipografías de marca
    ├── templates/        → base templates visuales
    └── characters/       → assets de los 2 personajes
```

---

## MARCA IM MUSIC

| Campo | Valor |
|-------|-------|
| Negro | #000000 |
| Violeta | #6200FF |
| Blanco | #FFFFFF |
| Concepto | REBEL LUXURY |
| Motivos | Galaxia, constelaciones, polvo estelar |
| Personaje Chill Hop | El Viajero Nocturno |
| Personaje Afro House | El Ser Galáctico |
| Distribución | Nexus (8%) |
| Publicación | L/M/V 18:00-20:00 |
| LUFS Spotify | -14 |
| LUFS YouTube | -13 |
| LUFS Apple | -16 |

---

## FASES DE IMPLEMENTACIÓN

**FASE 1 (Semanas 1-2): Fundación**
- Setup Claude Code + dependencias
- brand.py con identidad completa
- research.py + writer.py funcionando
- Primera publicación manual de prueba

**FASE 2 (Semanas 3-4): Design + Video**
- designer.py con templates IM Music
- video_producer.py con FFmpeg + Whisper
- publisher.py YouTube + Instagram

**FASE 3 (Semanas 5-6): Music Engine**
- beat_generator.py + approval_cli.py
- mastering.py cadena completa
- release_pack.py + integración Nexus

**FASE 4 (Semanas 7-8): Visualizer**
- visualizer.py con Manim + audio-reactive
- Personajes + escenarios galaxia/constelaciones

**FASE 5 (Semana 9+): Full automation**
- scheduler.py orquesta todo
- TikTok publisher + analytics

---

## NOTAS IMPORTANTES

1. **Canva MCP**: disponible para uso manual. El sistema principal usa Pillow+SVG.
2. **Aprobación de beats**: siempre manual. El usuario es el A&R del sello.
3. **brand.py**: fuente única de verdad para identidad visual.
4. **ISRC**: formato colombiano CO-[registro]-[año]-[secuencia].
5. **Copyright YouTube**: activar Content ID a través de Nexus.
