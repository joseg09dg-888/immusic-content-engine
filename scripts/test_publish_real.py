"""
Test de publicacion real en todas las plataformas.
Usa imagenes ya generadas en logs/rebel_luxury_v1/

Uso:
    python scripts/test_publish_real.py [--instagram] [--youtube] [--tiktok] [--all]
"""
import sys
import io
import argparse
from pathlib import Path

# Fix Unicode output on Windows cp1252 terminals
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.config import Config
from src.content_engine.writer import PublicationPackage

# Paquete de prueba real
TEST_PKG = PublicationPackage(
    brief={
        "titulo_principal": "REBEL LUXURY",
        "angulo_neurociencia": "La neurociencia del éxito musical",
        "hook_apertura": "¿Por qué algunos artistas dominan y otros desaparecen?",
        "datos_clave": ["El 1% de artistas genera el 77% de streams"],
        "controversia": "La industria no quiere que sepas esto",
        "fuentes": ["IM Music Research 2026"],
    },
    script_es="IM Music — REBEL LUXURY. El sello que rompe las reglas.",
    captions_instagram=(
        "El arte de dominar la industria musical.\n\n"
        "No es suerte. Es estrategia REBEL LUXURY.\n\n"
        "#IMMusic #RebelLuxury #MúsicaColombiana #IndustriaMusical"
    ),
    caption_tiktok="El secreto que los sellos no quieren que sepas 🎵 #IMMusic #RebelLuxury",
    youtube_titles=[
        "REBEL LUXURY: El Sistema que Domina la Industria Musical | IM Music",
        "Cómo IM Music Construye Artistas Millonarios | REBEL LUXURY",
        "La Estrategia Musical que Nadie Explica | IM Music Sello",
    ],
    youtube_description=(
        "IM Music — el sello discográfico REBEL LUXURY que está cambiando "
        "la industria musical colombiana.\n\n"
        "En este video revelamos el sistema que usamos para posicionar artistas "
        "en las plataformas globales.\n\n"
        "🎵 Síguenos: @immusicsello\n"
        "📧 Contacto: immusicsello@gmail.com\n\n"
        "#IMMusic #RebelLuxury #IndustriaMusical #Colombia"
    ),
)

# Assets de prueba (usa los ya generados)
POST_IMG   = ROOT / "logs" / "rebel_luxury_v1" / "post.png"
STORY_IMG  = ROOT / "logs" / "rebel_luxury_v1" / "story.png"
THUMB_IMG  = ROOT / "logs" / "rebel_luxury_v1" / "thumbnail.png"


def test_instagram():
    print("\n" + "="*50)
    print("INSTAGRAM — instagrapi")
    print("="*50)

    if not POST_IMG.exists():
        print(f"❌ Imagen no encontrada: {POST_IMG}")
        print("   Ejecuta primero: python scripts/gen_design.py")
        return False

    username = Config.INSTAGRAM_USERNAME
    password = Config.INSTAGRAM_PASSWORD

    if not username or not password:
        print("❌ INSTAGRAM_USERNAME o INSTAGRAM_PASSWORD no configurados en .env")
        return False

    print(f"Usuario: {username}")
    print(f"Imagen:  {POST_IMG}")

    try:
        from instagrapi import Client
        cl = Client()

        session_file = ROOT / ".instagram_session.json"
        if session_file.exists():
            print("Cargando sesión cacheada...")
            cl.load_settings(session_file)
            try:
                cl.login(username, password)
                print("✅ Sesión cargada correctamente")
            except Exception as e:
                print(f"  Sesión expirada, re-login... ({e})")
                cl = Client()
                cl.login(username, password)
                cl.dump_settings(session_file)
        else:
            print("Login fresco...")
            cl.login(username, password)
            cl.dump_settings(session_file)
            print("✅ Sesión guardada")

        print(f"\nSubiendo foto a Instagram...")
        caption = TEST_PKG.captions_instagram
        media = cl.photo_upload(str(POST_IMG), caption[:2200])
        media_id = str(media.pk)
        print(f"✅ PUBLICADO en Instagram: https://www.instagram.com/p/{media.code}/")
        print(f"   Media ID: {media_id}")
        return True

    except Exception as e:
        print(f"❌ Error Instagram: {e}")
        return False


def test_youtube():
    print("\n" + "="*50)
    print("YOUTUBE — OAuth")
    print("="*50)

    token_file = ROOT / ".youtube_token.json"
    creds_file = ROOT / "credentials.json"

    if not creds_file.exists():
        print("❌ credentials.json no encontrado")
        print("   Descarga desde Google Console y coloca en raíz del proyecto")
        return False

    if not token_file.exists():
        print("⚠️  .youtube_token.json no existe — ejecuta: python scripts/auth_youtube.py")
        return False

    if not STORY_IMG.exists():
        print(f"❌ Video de prueba no encontrado: {STORY_IMG}")
        return False

    print(f"Credenciales: {creds_file}")
    print(f"Token:        {token_file}")

    try:
        from src.content_engine.publisher import YouTubePublisher
        yt = YouTubePublisher(channel_id=Config.YOUTUBE_CHANNEL_ID)
        print("Verificando canal...")
        client = yt._get_client()
        result = client.channels().list(part="snippet", mine=True).execute()
        channels = result.get("items", [])
        if channels:
            print(f"✅ Canal: {channels[0]['snippet']['title']}")
        else:
            print("⚠️  Autenticado pero sin canal encontrado")

        # YouTube upload requires video file, not image
        print("\n⚠️  Upload de video real requiere archivo .mp4")
        print("   (publisher.py listo — video_producer pendiente de integración)")
        return True

    except Exception as e:
        print(f"❌ Error YouTube: {e}")
        return False


def test_tiktok():
    print("\n" + "="*50)
    print("TIKTOK — tiktok-uploader")
    print("="*50)

    cookies_file = ROOT / ".tiktok_cookies.json"

    if not cookies_file.exists():
        print("❌ .tiktok_cookies.json no encontrado")
        print()
        print("Para generar las cookies ejecuta:")
        print("   python scripts/get_tiktok_cookies.py")
        print()
        print("El script abre un browser Chromium. Inicia sesión en TikTok")
        print("y presiona ENTER cuando estés en el feed principal.")
        return False

    import json
    with open(cookies_file) as f:
        cookies = json.load(f)
    tiktok_cookies = [c for c in cookies if "tiktok.com" in c.get("domain", "")]
    print(f"Cookies TikTok: {len(tiktok_cookies)} encontradas")

    if len(tiktok_cookies) < 5:
        print("❌ Muy pocas cookies — sesión posiblemente inválida")
        return False

    # Verificar que tiktok-uploader está instalado
    try:
        from tiktok_uploader.upload import upload_video
    except ImportError:
        print("❌ tiktok-uploader no instalado")
        print("   pip install tiktok-uploader")
        return False

    print("✅ Cookies OK + tiktok-uploader disponible")
    print()
    print("⚠️  TikTok upload requiere archivo .mp4 (no imagen)")
    print("   Caption preparada:", TEST_PKG.caption_tiktok)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instagram", action="store_true")
    parser.add_argument("--youtube", action="store_true")
    parser.add_argument("--tiktok", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if not any([args.instagram, args.youtube, args.tiktok, args.all]):
        print("Uso: python scripts/test_publish_real.py [--instagram] [--youtube] [--tiktok] [--all]")
        print()
        print("Ejemplos:")
        print("  python scripts/test_publish_real.py --instagram")
        print("  python scripts/test_publish_real.py --all")
        sys.exit(0)

    results = {}

    if args.instagram or args.all:
        results["instagram"] = test_instagram()
    if args.youtube or args.all:
        results["youtube"] = test_youtube()
    if args.tiktok or args.all:
        results["tiktok"] = test_tiktok()

    print("\n" + "="*50)
    print("RESUMEN")
    print("="*50)
    for platform, ok in results.items():
        print(f"  {'✅' if ok else '❌'} {platform.upper()}")


if __name__ == "__main__":
    main()
