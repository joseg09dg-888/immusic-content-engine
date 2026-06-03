"""
RUTINA SEMANAL — IM Music Content Engine
Genera TODO el contenido de la semana (Lunes, Miércoles, Viernes) en una sola corrida.

Para cada día genera:
  01_carrusel_instagram/  -> 9 slides 1080x1080
  02_story_instagram.png  -> 1080x1920
  03_tiktok_carousel/     -> 6 slides 1080x1080
  04_tiktok_cover.png     -> 1080x1920
  05_thumbnail_youtube.png-> 1280x720
  06_youtube_short.png    -> 1080x1920
  07_pinterest.png        -> 1000x1500
  08_reel_instagram.mp4   -> VIDEO 720x1280
  09_copy_y_seo.txt       -> Todos los scripts, captions y SEO

Uso:
  python scripts/crear_contenido_semana.py             # semana actual
  python scripts/crear_contenido_semana.py --mes       # mes completo (12 packs)
  python scripts/crear_contenido_semana.py --dias 1    # solo hoy
"""
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import json

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv
load_dotenv()

from src.content_engine.research import ResearchEngine
from src.content_engine.designer import Designer
from src.content_engine.seo_engine import SEOEngine


DIAS_PUBLICACION = [0, 2, 4]  # Lunes=0, Miércoles=2, Viernes=4


def get_dias_semana(desde: datetime, n_dias: int = 3) -> list:
    """Retorna las próximas n_dias fechas de publicación (L/M/V) desde 'desde'."""
    fechas = []
    dia = desde
    while len(fechas) < n_dias:
        if dia.weekday() in DIAS_PUBLICACION:
            fechas.append(dia)
        dia += timedelta(days=1)
    return fechas


import re as _re

# Plantillas REBEL LUXURY por categoria — never generic
_HEADLINE_TEMPLATES = {
    "TikTok y viralidad":       [("EL ALGORITMO", "no es aleatorio."), ("VIRAL NO ES", "suerte. es ciencia."), ("TIKTOK PAGA", "en familiaridad."), ("EL SECRETO", "que TikTok no explica.")],
    "Distribucion y streaming": [("TUS REGALIAS", "estan desapareciendo."), ("SPOTIFY PAGA", "lo que no ves."), ("LA TRAMPA", "de la distribucion."), ("DISTRIBUIR", "no es suficiente.")],
    "Marketing musical":        [("TU MARKETING", "esta fallando."), ("LA ESTRATEGIA", "que nadie usa."), ("MARCA PERSONAL", "es supervivencia."), ("CONECTAR NO ES", "venderse.")],
    "Neurociencia y psicologia":[("EL CEREBRO", "decide antes que tu."), ("PSICOLOGIA", "aplicada al exito."), ("DOPAMINA", "y los streams."), ("LO QUE SIENTES", "cuando escuchas esto.")],
    "Desarrollo de artistas":   [("ARTISTA NO ES", "hobby. es empresa."), ("TU CARRERA", "necesita diagnostico."), ("MARCA UNICA", "o eres reemplazable."), ("EL SISTEMA", "que los grandes usan.")],
    "Industria musical":        [("LA INDUSTRIA", "no quiere que sepas esto."), ("EL NEGOCIO", "detras de la musica."), ("MAJORS", "versus independientes."), ("EL SELLO", "que nadie te explica.")],
    "YouTube y monetizacion":   [("YOUTUBE PAGA", "si sabes como."), ("MONETIZACION", "no es un mito."), ("EL ALGORITMO", "de YouTube revelado."), ("VIEWS", "no son dinero.")],
    "default":                  [("LA VERDAD", "que cambia todo."), ("REBEL LUXURY", "lo entendio primero."), ("EL SISTEMA", "esta roto."), ("MEDELLIN", "al mundo.")],
}

def _extract_number(text: str) -> str:
    """Extrae el numero mas impactante del texto (150m, 6.4M, etc.)."""
    patterns = [r"\d+\.?\d*\s*(?:m|M|millones|millions|billion|B)\b", r"\d+\.?\d*\s*(?:streams|videos|views)\b", r"\d+%", r"\$\s*\d+\.?\d*\s*(?:M|K|B)?\b"]
    for p in patterns:
        m = _re.search(p, text, _re.IGNORECASE)
        if m:
            return m.group(0).strip().upper()
    return ""


def build_slides_from_brief(brief: dict) -> list:
    """
    Slides REBEL LUXURY con Rebel Brain Method.
    Headlines de marca — NUNCA palabras del titulo RSS.
    """
    titulo  = brief.get("titulo_principal", "")
    datos   = brief.get("datos_clave", [""])
    angulo  = brief.get("angulo_neurociencia", "")
    fuente  = brief.get("fuentes", [{}])[0].get("source", "fuente verificada")
    tema    = brief.get("tema_categoria", "default")

    dato_texto = datos[0] if datos else titulo
    numero     = _extract_number(dato_texto + " " + titulo)
    dato_short = dato_texto[:55]

    templates = _HEADLINE_TEMPLATES.get(tema, _HEADLINE_TEMPLATES["default"])
    h1, h1sub = templates[hash(titulo) % len(templates)]

    credibility_h = numero if numero else "EL DATO"
    credibility_s = f"verificado. {fuente}."

    return [
        {"context": "Lo que la industria no dice.",        "title": h1,               "subtitle": h1sub,                          "cta": "SIGUE LEYENDO"},
        {"context": "La industria lleva anos sabiendolo.", "title": "Y SIGUIO",        "subtitle": "vendiendo como si no.",        "cta": "SIGUE LEYENDO"},
        {"context": dato_short,                            "title": "POR QUE",         "subtitle": "nadie te lo dijo antes?",      "cta": "SIGUE LEYENDO"},
        {"context": f"Fuente: {fuente}",                   "title": credibility_h,     "subtitle": credibility_s,                  "cta": "SIGUE LEYENDO"},
        {"context": "El cerebro no lo procesa como crees.","title": "LA CIENCIA",      "subtitle": "lo explica todo.",             "cta": "SIGUE LEYENDO"},
        {"context": "Esto no es opinion.",                 "title": "ES BIOLOGIA",     "subtitle": "y ahora es tu ventaja.",       "cta": "SIGUE LEYENDO"},
        {"context": "La pregunta correcta no es como.",   "title": "ES POR QUE",      "subtitle": "nadie mas lo esta haciendo.",  "cta": "SIGUENOS AHORA"},
        {"context": "IM Music. Medellin al mundo.",        "title": "REBEL LUXURY",    "subtitle": "no es estetica. es estrategia.","cta": "SIGUENOS AHORA"},
    ]


def generate_copy_seo(brief: dict, output_file: Path):
    """Genera archivo de texto con todos los scripts, captions y SEO."""
    titulo = brief.get("titulo_principal", "")
    datos = brief.get("datos_clave", [""])
    dato = datos[0][:200] if datos else ""
    angulo = brief.get("angulo_neurociencia", "")
    hook = brief.get("hook_apertura", "")

    content = f"""PACK DE CONTENIDO — {titulo}
{'='*60}
Fuente: {brief.get('fuentes', [{}])[0].get('source', '')}
Tema: {brief.get('tema_categoria', '')}
Fecha: {datetime.now().strftime('%Y-%m-%d')}

DATOS VERIFICADOS:
{dato}

ANGULO NEUROCIENCIA:
{angulo}

{'='*60}
GUION YOUTUBE SHORTS (55-58s) — Rebel Brain Method
{'='*60}
[0-3s PATTERN INTERRUPT]
{hook}

[3-15s TENSION BUILDER]
La industria lleva tiempo sabiendo esto. Y siguió vendiendo como si no.
{dato[:150]}

[15-45s INSIGHT REVELATION]
{angulo}

[45-55s REBEL REFRAME]
La pregunta no es cómo hacerlo. La pregunta es por qué nadie te lo había dicho.

[55-58s]
IM MUSIC — REBEL LUXURY.

{'='*60}
GUION INSTAGRAM REEL (7-45s)
{'='*60}
[0-3s] {hook}
[3-30s] {dato[:200]}
[30-43s] {angulo[:200]}
[43-45s] IM Music — Rebel Luxury.

{'='*60}
GUION TIKTOK (21-90s)
{'='*60}
"{hook}"
"{dato[:200]}"
"{angulo[:200]}"
"La industria te vendió que necesitas [X] para llegar a [Y]."
"Esto prueba que necesitas entender el cerebro humano."
"Eso no cuesta nada."

{'='*60}
CAPTION INSTAGRAM (Rebel Luxury)
{'='*60}
{hook}

{dato[:300]}

{angulo[:300]}

La industria te vendió que necesitas millones para llegar a millones.
Esto prueba que necesitas entender el cerebro humano.

Eso no cuesta nada.

#MusicMarketing #TikTokMusic #IndependentArtist #MusicBusiness #RebelLuxury #IMMusic #ArtistaIndependiente #MarketingMusical #NeurocienciaMusical #ViralMusic

{'='*60}
CAPTION TIKTOK
{'='*60}
{hook[:100]} 🔥 #MusicMarketing #TikTokMusic #IndependentArtist #IMMusic

{'='*60}
SEO YOUTUBE
{'='*60}
TITULO (A/B test 3 opciones):
1. "{titulo[:80]}"
2. "{hook[:80]}"
3. "Lo que la industria no quiere que sepas sobre {brief.get('tema_categoria', 'la musica')}"

TAGS (30):
music marketing, tiktok music, independent artist, spotify algorithm, music business, artista independiente, marketing musical, neurociencia musica, viral music, im music rebel luxury, medellin music, {brief.get('tema_categoria', 'musica viral').lower()}, music psychology, algorithmic promotion, independent label, sello discografico

PUBLICACION:
YouTube: 18:00 COT | Instagram: 19:00 COT | TikTok: 20:00 COT
"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding="utf-8")


def generate_day_pack(brief: dict, fecha: datetime, out_dir: Path):
    """Genera el pack completo de un día."""
    out_dir.mkdir(parents=True, exist_ok=True)
    d = Designer()

    print(f"\n{'-'*55}")
    print(f"Generando: {fecha.strftime('%A %Y-%m-%d')}")
    print(f"Tema: {brief.get('titulo_principal', '')[:60]}")
    print(f"{'-'*55}")

    slides = build_slides_from_brief(brief)

    # 1. Carrusel Instagram
    d.generate_carousel(slides, out_dir / "01_carrusel_instagram")
    print("  [OK] 01 Carrusel Instagram (9 slides)")

    # 2. Story
    d.generate_story(brief.get("hook_apertura", "")[:25], brief.get("tema_categoria", ""), out_dir / "02_story_instagram.png")
    print("  [OK] 02 Story Instagram")

    # 3. TikTok carousel
    tiktok_slides = [
        {"titulo": s["title"], "subtitulo": s["subtitle"]} for s in slides[:5]
    ]
    d.generate_tiktok_carousel_slides(tiktok_slides, out_dir / "03_tiktok_carousel")
    print("  [OK] 03 TikTok Carousel")

    # 4. TikTok cover
    d.generate_tiktok_cover(slides[0]["title"], out_dir / "04_tiktok_cover.png")
    print("  [OK] 04 TikTok Cover")

    # 5. YouTube thumbnail
    titulo = brief.get("titulo_principal", "")
    d.generate_thumbnail(titulo[:30], brief.get("tema_categoria", ""), out_dir / "05_thumbnail_youtube.png")
    print("  [OK] 05 YouTube Thumbnail")

    # 6. YouTube Short
    d.generate_youtube_short_thumbnail(slides[0]["title"], slides[0]["subtitle"][:25], out_dir / "06_youtube_short.png")
    print("  [OK] 06 YouTube Short cover")

    # 7. Pinterest
    d.generate_pinterest_pin(titulo[:35], brief.get("angulo_neurociencia", "")[:40], out_dir / "07_pinterest.png")
    print("  [OK] 07 Pinterest Pin")

    # 8. Reel video (from carousel slides)
    carousel_dir = out_dir / "01_carrusel_instagram"
    slide_files = sorted(carousel_dir.glob("slide_0[1-8].png"))
    if slide_files:
        _generate_reel_video(slide_files, out_dir / "08_reel_instagram.mp4")

    # 9. Copy y SEO
    generate_copy_seo(brief, out_dir / "09_copy_y_seo.txt")
    print("  [OK] 09 Copy y SEO")

    return out_dir


def _generate_reel_video(slide_files: list, output: Path):
    """Convierte slides en video Reel animado."""
    import shutil
    from PIL import Image as PIL_Image

    seq_dir = output.parent / "_seq"
    seq_dir.mkdir(exist_ok=True)
    fps, dur = 30, 3
    n = 0
    for slide in slide_files:
        img = PIL_Image.open(slide).convert("RGB")
        canvas = PIL_Image.new("RGB", (720, 1280), (94, 23, 235))
        sq = img.resize((720, 720))
        canvas.paste(sq, (0, 280))
        for _ in range(fps * dur):
            canvas.save(seq_dir / f"f{n:05d}.jpg", quality=82)
            n += 1

    r = subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", str(seq_dir / "f%05d.jpg"),
        "-c:v", "libx264", "-crf", "20", "-preset", "fast", "-pix_fmt", "yuv420p",
        str(output)
    ], capture_output=True, text=True)
    shutil.rmtree(seq_dir)
    if r.returncode == 0:
        print(f"  [OK] 08 Reel Instagram MP4 ({output.stat().st_size//1024}KB)")
    else:
        print(f"  [!] Reel falló: {r.stderr[-80:]}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mes", action="store_true", help="Produce el mes completo (13 packs)")
    parser.add_argument("--dias", type=int, default=3, help="Numero de dias a producir (default: 3 = una semana)")
    parser.add_argument("--desde", help="Fecha inicio YYYY-MM-DD (default: hoy)")
    args = parser.parse_args()

    desde = datetime.strptime(args.desde, "%Y-%m-%d") if args.desde else datetime.now()
    n_dias = 13 if args.mes else args.dias

    print("=" * 50)
    print("  IM MUSIC CONTENT ENGINE - RUTINA SEMANAL")
    print("=" * 50)
    print(f"Produciendo {n_dias} paquetes de contenido")
    print(f"Publicacion: L/M/V — YouTube 18:00 | IG 19:00 | TikTok 20:00 COT")
    print()

    # Research: obtener N stories distintas
    eng = ResearchEngine()
    stories = eng.fetch_all()
    top_stories = eng.top_stories(stories, n=n_dias)

    if not top_stories:
        print("[ERROR] No se encontraron stories. Verifica conexion a internet.")
        sys.exit(1)

    print(f"Stories encontradas: {len(stories)} | Seleccionadas: {len(top_stories)}")

    # Fechas de publicacion
    fechas = get_dias_semana(desde, n_dias)

    # Generar pack por dia
    base_out = Path("outputs") / f"semana_{desde.strftime('%Y-%m-%d')}"
    results = []

    for i, (story, fecha) in enumerate(zip(top_stories, fechas)):
        brief = eng.build_brief(story)
        dia_str = fecha.strftime("%Y-%m-%d_%A")
        pack_dir = base_out / f"{i+1:02d}_{dia_str}"
        try:
            generate_day_pack(brief, fecha, pack_dir)
            results.append({"fecha": str(fecha.date()), "dir": str(pack_dir), "ok": True})
        except Exception as e:
            print(f"  [ERROR] {e}")
            results.append({"fecha": str(fecha.date()), "dir": str(pack_dir), "ok": False})

    # Resumen
    print(f"\n{'='*55}")
    print(f"RESUMEN — {len([r for r in results if r['ok']])}/{len(results)} packs generados")
    print(f"{'='*55}")
    for r in results:
        status = "OK" if r["ok"] else "FAIL"
        print(f"  [{status}] {r['fecha']} -> {Path(r['dir']).name}")

    print(f"\nOutputs en: {base_out}")
    print()

    # Auto-sincronizar con Google Drive for Desktop
    try:
        from src.core.drive_sync import sync_folder_to_drive, drive_status
        print(f"Drive: {drive_status()}")
        if sync_folder_to_drive(base_out, subfolder="CONTENIDO"):
            print("[OK] Contenido disponible en Google Drive automaticamente")
        else:
            print("Cuando instales Drive para Escritorio, corre:")
            print(f"  python scripts/sync_to_drive.py --folder {base_out}")
    except Exception as e:
        print(f"[!] Auto-sync: {e}")


if __name__ == "__main__":
    main()
