"""
scripts/keep_streamlit_awake.py

Besucht die Streamlit-Cloud-App mit einem echten (headless) Browser und
klickt den "Yes, get this app back up!"-Button, falls die App gerade
schläft. Ein simpler HTTP-Request (curl/requests) reicht dafür NICHT aus,
da eine schlafende App nur eine statische HTML-Hülle zurückgibt (Status
200, ohne die eigentliche App zu starten) - es braucht echtes
Browser-Rendering + einen echten Klick.

Wird von .github/workflows/keep-streamlit-awake.yml alle paar Stunden
automatisch ausgeführt.
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright

APP_URL = os.environ.get(
    "STREAMLIT_APP_URL",
    "https://andrey-gerber-lebenslauf.streamlit.app/",
)

# Mögliche Texte des Wach-Buttons (auf Streamlit Cloud aktuell Englisch,
# aber zur Sicherheit mehrere Varianten abgedeckt)
WAKE_BUTTON_TEXTS = [
    "Yes, get this app back up!",
    "get this app back up",
]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Besuche {APP_URL} ...")
        page.goto(APP_URL, wait_until="networkidle", timeout=60_000)

        # Kurz warten, damit eine eventuelle "App is sleeping"-Seite
        # vollständig rendert (das ist eine kleine Web-App für sich).
        time.sleep(3)

        woke_up = False
        for text in WAKE_BUTTON_TEXTS:
            try:
                button = page.get_by_text(text, exact=False)
                if button.count() > 0:
                    print(f"App schläft - klicke Button: '{text}'")
                    button.first.click()
                    woke_up = True
                    # Nach dem Klick etwas warten, bis die App hochfährt
                    time.sleep(15)
                    break
            except Exception as e:
                print(f"Hinweis beim Suchen nach '{text}': {e}")

        if not woke_up:
            print("Kein Wach-Button gefunden - App war vermutlich schon wach.")

        browser.close()
        print("Fertig.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fehler: {e}")
        sys.exit(1)