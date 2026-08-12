"""
utils/loaders.py

Gecachte Lade-Funktionen für Bilder und PDFs. Zentral an einer Stelle,
damit jede Sektion (header, timeline, certificates, hobbies, skills, ...)
dieselben Funktionen wiederverwendet statt eigene Kopien zu pflegen.

@st.cache_data sorgt dafür, dass eine Datei nur EINMAL von der Platte
gelesen/verarbeitet wird - bei jedem weiteren Rerun (Klick, Sprachwechsel)
kommt das Ergebnis direkt aus dem Cache. Das ist der zweite große
Performance-Hebel neben @st.fragment.
"""

import os
import base64
import streamlit as st
from PIL import Image


@st.cache_data(ttl=3600, show_spinner=False)
def load_pil_image_cached(path: str, target_size=(900, 600), max_width=None):
    """
    Lädt ein Bild als PIL.Image, skaliert es und cached das Ergebnis.

    target_size: feste Leinwandgröße, Bild wird zentriert eingepasst
                 (transparenter Rand). Wird ignoriert, wenn max_width gesetzt ist.
    max_width:   Bild wird proportional auf diese Breite skaliert, ohne
                 zusätzlichen Rand.
    """
    if not os.path.exists(path):
        return None
    try:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")

        if max_width:
            ratio = max_width / img.size[0]
            new_size = (max_width, int(img.size[1] * ratio))
            img.thumbnail(new_size, Image.Resampling.LANCZOS)
            return img
        elif target_size:
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
            new_img.paste(img, ((target_size[0] - img.size[0]) // 2,
                                 (target_size[1] - img.size[1]) // 2))
            return new_img
        return img
    except Exception as e:
        print(f"Fehler beim Laden von {path}: {e}")
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def load_image_base64_cached(path: str):
    """Lädt eine Bilddatei als Base64-String (für <img src='data:...'> in HTML)."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def load_pdf_base64_cached(path: str):
    """Lädt eine PDF-Datei als Base64-String (für Download-Button / iFrame-Fallback)."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def load_scaled_image_cached(path: str, degrees: int = 0, scale_percent: int = 40):
    """
    Lädt ein Bild, dreht es optional (in Grad) und skaliert es prozentual.
    Anders als load_pil_image_cached: hier wird um einen PROZENTSATZ skaliert,
    nicht auf eine feste Zielgröße - passend für die Kerzen-/Projekt-Galerien.
    """
    if not os.path.exists(path):
        return None
    try:
        img = Image.open(path)
        if degrees != 0:
            img = img.rotate(degrees, expand=True)
        scale_factor = scale_percent / 100
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        return img.resize(new_size, Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Fehler beim Laden von {path}: {e}")
        return None


@st.cache_resource(show_spinner=False)
def collect_cert_images_cached(cert_defs: tuple, folder: str) -> list:
    """
    Sammelt Base64-Bilddaten für eine Liste von Zertifikaten.

    cert_defs: Tuple aus (dateiname_ohne_endung, anzeige_name) Tupeln.
    folder:    Ordner, in dem die Bilder liegen (z.B. 'images/Data_Scientist').

    Wird von sections/cert_wall.py (3D-Wand) UND sections/cert_carousel.py
    (CSS-3D-Karussell) gemeinsam genutzt, damit die Sammel-Logik nur an
    einer Stelle gepflegt werden muss.
    """
    cert_data = []
    if not os.path.exists(folder):
        return cert_data

    for filename, display_name in cert_defs:
        for ext in (".png", ".jpg", ".jpeg"):
            img_path = os.path.join(folder, filename + ext)
            if os.path.exists(img_path):
                img_b64 = load_image_base64_cached(img_path)
                if img_b64:
                    cert_data.append({
                        "name": display_name,
                        "b64": img_b64,
                        "ext": ext[1:],
                    })
                break
    return cert_data