"""
TikTok login with Selenium — uses Chrome + credentials from .env.
Logs in automatically, captures session cookies, saves to .tiktok_cookies.json.

Run:
    python scripts/get_tiktok_cookies.py
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

COOKIES_FILE = Path(__file__).resolve().parent.parent / ".tiktok_cookies.json"
USERNAME = os.environ["TIKTOK_USERNAME"]
PASSWORD = os.environ["TIKTOK_PASSWORD"]


def build_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    # Use system Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def do_login(driver: webdriver.Chrome) -> bool:
    print(f"Opening TikTok login... (username: {USERNAME})")
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(4)

    wait = WebDriverWait(driver, 20)

    # Enter username/email
    try:
        user_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='username'], input[placeholder*='mail'], input[placeholder*='sername']")
        ))
        user_input.clear()
        user_input.send_keys(USERNAME)
        time.sleep(1)

        pass_input = driver.find_element(
            By.CSS_SELECTOR, "input[type='password'], input[placeholder*='assword']"
        )
        pass_input.clear()
        pass_input.send_keys(PASSWORD)
        time.sleep(1)

        # Click login button
        login_btn = driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], button[data-e2e='login-button']"
        )
        login_btn.click()
        print("Credentials submitted. Waiting for login to complete...")
        time.sleep(8)
        return True
    except Exception as e:
        print(f"  Auto-fill failed: {e}")
        print("  Please log in manually in the browser window. Press Enter when done.")
        input("  >>> ")
        return True


def save_cookies(driver: webdriver.Chrome) -> dict:
    cookies = driver.get_cookies()
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f, indent=2)
    return cookies


def verify_login(driver: webdriver.Chrome) -> bool:
    """Check that we're logged in by looking for sessionid cookie."""
    cookies = driver.get_cookies()
    names = [c["name"] for c in cookies]
    return "sessionid" in names or "sid_guard" in names


def main():
    driver = build_driver()
    try:
        do_login(driver)

        # Wait up to 30s for successful login (sessionid cookie appears)
        print("Waiting for session cookies...")
        for i in range(30):
            if verify_login(driver):
                break
            time.sleep(1)
            if i % 5 == 0:
                print(f"  Waiting... {i}s")

        if not verify_login(driver):
            print("[!] sessionid not found. TikTok may have shown a captcha.")
            print("    Solve the captcha in the browser, then press Enter.")
            input("    >>> ")

        cookies = save_cookies(driver)
        session_names = [c["name"] for c in cookies if c["name"] in ("sessionid", "sid_guard", "tt_csrf_token")]
        print()
        if verify_login(driver):
            print(f"[OK] Login successful.")
            print(f"     Session cookies: {[c['name'] for c in cookies]}")
            print(f"     Saved -> {COOKIES_FILE} ({len(cookies)} cookies)")
        else:
            print(f"[!] Login may have failed. Saved {len(cookies)} cookies anyway.")
            print(f"    File: {COOKIES_FILE}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
