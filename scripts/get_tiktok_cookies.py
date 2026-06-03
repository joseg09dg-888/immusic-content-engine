"""
Script para obtener cookies de sesion de TikTok.
Abre un browser Chromium, inicia sesion en TikTok manualmente,
luego guarda las cookies en .tiktok_cookies.json

Uso:
    python scripts/get_tiktok_cookies.py
"""
import json
import time
from pathlib import Path

OUTPUT_FILE = Path(__file__).resolve().parent.parent / ".tiktok_cookies.json"


def main():
    from playwright.sync_api import sync_playwright

    print("Abriendo browser para login en TikTok...")
    print("Inicia sesion manualmente con tu cuenta @immusicsello")
    print("Cuando veas el feed principal, presiona ENTER aqui.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.tiktok.com/login")

        input("\nPresiona ENTER cuando hayas iniciado sesion en TikTok...")

        cookies = context.cookies()
        browser.close()

    with open(OUTPUT_FILE, "w") as f:
        json.dump(cookies, f, indent=2)

    print(f"Cookies guardadas en {OUTPUT_FILE}")
    print(f"Total cookies: {len(cookies)}")

    tiktok_cookies = [c for c in cookies if "tiktok.com" in c.get("domain", "")]
    print(f"Cookies de TikTok: {len(tiktok_cookies)}")

    if len(tiktok_cookies) < 5:
        print("ADVERTENCIA: Pocas cookies - puede que no hayas iniciado sesion correctamente")
    else:
        print("OK - Cookies de TikTok guardadas correctamente")


if __name__ == "__main__":
    main()
