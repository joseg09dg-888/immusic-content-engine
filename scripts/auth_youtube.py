"""
Script para autorizar YouTube OAuth una sola vez.
Abre el browser, pide permiso para la cuenta @immusicsello,
guarda el token en .youtube_token.json para uso automatico futuro.

Uso:
    python scripts/auth_youtube.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


def main():
    from core.config import Config
    from content_engine.publisher import _build_yt_client, _YT_TOKEN_FILE

    print("Iniciando flujo OAuth de YouTube...")
    print(f"Client ID: {Config.GOOGLE_CLIENT_ID[:40]}...")
    print()
    print("Se abrira el browser — inicia sesion con immusicsello@gmail.com")
    print("y otorga permisos de subida de videos.")
    print()

    try:
        yt = _build_yt_client()
        result = yt.channels().list(part="snippet", mine=True).execute()
        channels = result.get("items", [])
        if channels:
            ch = channels[0]["snippet"]
            print(f"Autenticado como: {ch['title']}")
            print(f"Canal ID: {channels[0]['id']}")
            print(f"Token guardado en: {_YT_TOKEN_FILE}")
            print()
            print("YouTube OAuth conectado correctamente.")
            print(f"Agrega YOUTUBE_CHANNEL_ID={channels[0]['id']} a tu .env")
        else:
            print("Autenticado pero no se encontro canal. Verifica la cuenta.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
