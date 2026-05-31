# IM Music Content Engine — Claude Code Instructions

## Proyecto
Sistema automatizado REBEL LUXURY para IM Music sello discográfico.
Spec maestro: `docs/superpowers/specs/2026-05-28-immusic-system-design.md`

## Stack
- Python 3.12 | anthropic | pillow | librosa | pydub | pyloudnorm
- AudioCraft/MusicGen | Manim | FFmpeg | Whisper
- Claude API: claude-sonnet-4-6

## Marca (INMUTABLE)
```
Negro:   #000000
Violeta: #5E17EB
Crema:   #F2EDE5
Concepto: REBEL LUXURY
Motivos:  Galaxia, constelaciones, polvo estelar
Fuentes:  Anton (títulos/subtítulos)
```
brand.py es la única fuente de verdad. Todo cambio visual pasa por ahí.

## Reglas absolutas
1. NUNCA declarar algo "listo" sin verificación real
2. brand.py para toda identidad visual — no hardcodear colores en otro lado
3. Aprobación de beats siempre manual (usuario es el A&R)
4. LUFS targets: Spotify -14 | YouTube -13 | Apple -16
5. Publicación: L/M/V 18:00-20:00 hora Colombia

## Estructura
```
src/core/         → brand.py, config.py, scheduler.py
src/content_engine/ → research.py, writer.py, designer.py, video_producer.py, publisher.py
src/music_engine/ → beat_generator.py, mastering.py, visualizer.py, release_pack.py
assets/           → logo, fonts, templates, characters
releases/         → output de cada track
```

## Personajes
- Chill Hop (85-95 BPM): El Viajero Nocturno — ciudad nocturna, neón violeta
- Afro House (120-128 BPM): El Ser Galáctico — galaxia, nebulosas, polvo estelar

## Distribución
- Nexus (8% regalías) — NO plataforma propia
- Plataformas: YouTube + Instagram + TikTok
