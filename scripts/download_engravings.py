"""
Download public-domain vintage engravings for the REBEL LUXURY visual pipeline.
Images are B&W line-art from Wikimedia Commons (CC0 / public domain).
Output: assets/engravings/

Run once:
    python scripts/download_engravings.py
"""
import time
from pathlib import Path
from typing import Optional

import requests

SAVE_DIR = Path(__file__).resolve().parent.parent / "assets" / "engravings"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "IMMusic-ContentEngine/1.0 (immusicsello@gmail.com)"}

# Wikimedia Commons searches — each yields vintage B&W engraving suitable for REBEL LUXURY
SEARCH_TERMS = [
    "Gustave Dore engraving angel",
    "vintage engraving lion heraldic",
    "antique engraving eagle",
    "memento mori skull engraving",
    "baroque engraving hand",
    "vintage engraving crown royal",
    "botanical engraving rose flower",
    "vintage engraving snake serpent",
    "classical engraving figure",
    "antique engraving building architecture",
    "vintage engraving cupid cherub",
    "engraving money coins gold",
]


def search_wikimedia(query: str, limit: int = 3) -> list:
    """Search Wikimedia Commons for image file titles matching query."""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": 6,
        "srlimit": limit,
        "format": "json",
    }
    try:
        r = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params=params, headers=HEADERS, timeout=15,
        )
        r.raise_for_status()
        return [res["title"] for res in r.json().get("query", {}).get("search", [])]
    except Exception as e:
        print(f"  Search error: {e}")
        return []


def get_image_url(file_title: str) -> Optional[str]:
    """Get direct download URL for a Wikimedia Commons file (max 1200px wide)."""
    params = {
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "iiurlwidth": 1200,
        "format": "json",
    }
    try:
        r = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params=params, headers=HEADERS, timeout=15,
        )
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            info = (page.get("imageinfo") or [{}])[0]
            mime = info.get("mime", "")
            if mime.startswith("image/"):
                return info.get("thumburl") or info.get("url")
    except Exception:
        pass
    return None


def download_image(url: str, save_path: Path) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        size_kb = save_path.stat().st_size // 1024
        print(f"  [OK] {save_path.name}  ({size_kb} KB)")
        return True
    except Exception as e:
        print(f"  [FAIL] {url}: {e}")
        if save_path.exists():
            save_path.unlink()
        return False


def main():
    print(f"Downloading vintage engravings to: {SAVE_DIR}")
    print()

    downloaded = 0
    for i, term in enumerate(SEARCH_TERMS):
        print(f"[{i+1}/{len(SEARCH_TERMS)}] '{term}'")
        titles = search_wikimedia(term, limit=3)
        for title in titles:
            slug = title.replace("File:", "").strip()
            slug = "".join(c if c.isalnum() or c in "_-." else "_" for c in slug)[:50]
            ext = ".jpg" if slug.lower().endswith(".jpg") else ".png"
            save_path = SAVE_DIR / f"eng_{i:02d}_{slug}{'' if slug.endswith(ext) else ext}"
            if save_path.exists():
                print(f"  [SKIP] {save_path.name}")
                downloaded += 1
                break
            url = get_image_url(title)
            if url:
                if download_image(url, save_path):
                    downloaded += 1
                    break
            time.sleep(0.4)

    print()
    files = list(SAVE_DIR.glob("*.*"))
    print(f"Total engravings available: {len(files)}")
    for f in sorted(files):
        print(f"  {f.name}")
    if not files:
        print()
        print("[!] No files downloaded. Manually place B&W PNG/JPG engravings in:")
        print(f"    {SAVE_DIR}")
        print("    Good sources: commons.wikimedia.org, rawpixel.com (filter: public domain)")


if __name__ == "__main__":
    main()
