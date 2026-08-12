"""
sections/header.py

Oberster Bereich: Willkommens-Titel, Foto-Slideshow, Zeichnung, Kontaktdaten,
Sprachniveaus.

Performance-Hinweis:
Die Slideshow-Pfeile (⬅️ ➡️) stecken in einem @st.fragment. Ein Klick löst
dadurch NUR einen Rerun dieses kleinen Blocks aus - nicht mehr, wie vorher,
einen kompletten Rerun der ganzen ~1100-Zeilen-Seite.
"""

import os
import streamlit as st

from utils.loaders import load_pil_image_cached

IMAGES_FOLDER = "images"
SLIDESHOW_IMAGES = ["ich1.JPG", "ich_pass.png", "aufenthaltstitel.png"]
DRAWING_IMAGE = "itsme2.png"

# Diese Daten ändern sich nicht mit der Sprache -> bewusst hier als Konstanten,
# nicht in den translations/*.py Dateien.
PHONE = "0176 43 733 099"
EMAIL = "andrey.gerber.88@gmail.com"


def _load_formatted(name: str, target_size=(900, 600), max_width=None):
    path = os.path.join(IMAGES_FOLDER, name)
    return load_pil_image_cached(path, target_size=target_size, max_width=max_width)


@st.fragment
def _render_photo_slideshow():
    if "bild_index" not in st.session_state:
        st.session_state.bild_index = 0

    current_name = SLIDESHOW_IMAGES[st.session_state.bild_index]
    current_img = _load_formatted(current_name)

    if current_img:
        st.image(current_img, use_container_width=True)
    else:
        st.error(f"Datei fehlt: {current_name}")

    p_links, p_mitte, p_rechts = st.columns([1, 4, 1])
    with p_links:
        if st.button("⬅️", key="header_slideshow_prev"):
            st.session_state.bild_index = (st.session_state.bild_index - 1) % len(SLIDESHOW_IMAGES)
            st.rerun(scope="fragment")
    with p_rechts:
        if st.button("➡️", key="header_slideshow_next"):
            st.session_state.bild_index = (st.session_state.bild_index + 1) % len(SLIDESHOW_IMAGES)
            st.rerun(scope="fragment")


def render_header(t: dict):
    st.markdown(f"<h2 style='text-align: center;'>{t['header_welcome']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: #4B0082;'>{t['header_title']}</h1>", unsafe_allow_html=True)
    st.divider()

    st.markdown("""
        <style>
        [data-testid="stHorizontalBlock"] { align-items: center; }
        .contact-link { text-decoration: none; color: #007BFF; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    col_bild, col_mitte, col_daten = st.columns([1.5, 1.0, 1.5])

    with col_bild:
        _render_photo_slideshow()

    with col_mitte:
        zeichnung = _load_formatted(DRAWING_IMAGE, target_size=(300, 300))
        if zeichnung:
            st.image(zeichnung, use_container_width=True)
        else:
            st.info(t["header_drawing_placeholder"])

    with col_daten:
        st.markdown(
            f"<p style='font-size: 30px; color: gray; margin-bottom: -10px;'>{t['header_contact_label']}</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 style='font-size: 42px; font-weight: bold; margin-top: 0px;'>Andrey Gerber</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(f"""
            <div style='line-height: 1.8;'>
                <p style='font-size: 24px;'>
                    <span style='margin-right: 15px;'>📞</span>
                    <strong>{PHONE}</strong>
                </p>
                <p style='font-size: 24px;'>
                    <span style='margin-right: 15px;'>📧</span>
                    <a href='mailto:{EMAIL}' class='contact-link'>{EMAIL}</a>
                </p>
                <p style='font-size: 24px; color: #666; margin-top: 20px;'>
                    📍 <i>{t['header_address_note']}</i>
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

        st.markdown("""
            <p style='font-size: 22px;'>
                🇩🇪 <span style='color: gray; font-size: 18px;'>(C2)</span>
                <span style='margin-right: 40px;'></span>
                🇷🇺 <span style='color: gray; font-size: 18px;'>(C2)</span>
                <span style='margin-right: 40px;'></span>
                🇺🇸 <span style='color: gray; font-size: 18px;'>(B2)</span>
            </p>
        """, unsafe_allow_html=True)

    st.divider()