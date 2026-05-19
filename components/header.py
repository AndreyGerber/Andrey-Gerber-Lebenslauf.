# components/header.py

import streamlit as st
from utils.text_loader import get_text
from utils.image_loader import load_formatted_image
import os

def show_header():
    # Sprache initialisieren
    if "lang" not in st.session_state:
        st.session_state.lang = "de"

    # Sprachbuttons
    def lang_button(label, code):
        if st.button(label, key=f"lang_{code}"):
            st.session_state.lang = code
            st.rerun()

    spacer1, col1, col2, col3, spacer2 = st.columns([4, 1, 1, 1, 4])
    with col1:
        lang_button("🇩🇪 Deutsch", "de")
    with col2:
        lang_button("🇬🇧 English", "en")
    with col3:
        lang_button("🇷🇺 Русский", "ru")

    # Texte laden
    t = get_text(st.session_state.lang)

    # Titel anzeigen
    st.markdown(f"<h2 style='text-align: center;'>{t['welcome']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: #4B0082;'>{t['title']}</h1>", unsafe_allow_html=True)
    
    st.divider()

    # --- DREISPALTIGES LAYOUT FÜR BILDER UND KONTAKTDATEN ---
    col_bild, col_mitte, col_daten = st.columns([1.5, 1.0, 1.5])

    # === SPALTE 1: SLIDESHOW BILDER ===
    with col_bild:
        # Slideshow-Bilder
        slideshow_bilder = ["ich1.JPG", "ich_pass.png", "aufenthaltstitel.png"]
        
        if 'bild_index' not in st.session_state:
            st.session_state.bild_index = 0
        
        aktuelles_foto = load_formatted_image(slideshow_bilder[st.session_state.bild_index])
        if aktuelles_foto:
            st.image(aktuelles_foto, use_container_width=True)
        else:
            st.error(f"Datei fehlt: {slideshow_bilder[st.session_state.bild_index]}")
        
        # Navigation unter dem Bild
        p_links, p_mitte, p_rechts = st.columns([1, 4, 1])
        with p_links:
            if st.button("⬅️", key="prev_img"):
                st.session_state.bild_index = (st.session_state.bild_index - 1) % len(slideshow_bilder)
                st.rerun()
        with p_rechts:
            if st.button("➡️", key="next_img"):
                st.session_state.bild_index = (st.session_state.bild_index + 1) % len(slideshow_bilder)
                st.rerun()

    # === SPALTE 2: "ITS ME" ZEICHNUNG ===
    with col_mitte:
        zeichnung = load_formatted_image("itsme2.png", target_size=(300, 300))
        if zeichnung:
            st.image(zeichnung, use_container_width=True)
        else:
            st.info("Hier erscheint deine Zeichnung...")

    # === SPALTE 3: KONTAKTDATEN ===
    with col_daten:
        st.markdown("<p style='font-size: 30px; color: gray; margin-bottom: -10px;'>Meine Kontaktdaten</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 42px; font-weight: bold; margin-top: 0px;'>{t['contact_name']}</h1>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='line-height: 1.8;'>
                <p style='font-size: 24px;'>
                    <span style='margin-right: 15px;'>📞</span> 
                    <strong>{t['contact_phone']}</strong>
                </p>
                <p style='font-size: 24px;'>
                    <span style='margin-right: 15px;'>📧</span> 
                    <a href='mailto:{t['contact_email']}' style='text-decoration: none; color: #007BFF; font-weight: bold;'>
                        {t['contact_email']}
                    </a>
                </p>
                <p style='font-size: 24px; color: #666; margin-top: 20px;'>
                    📍 <i>{t['contact_address']}</i>
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Sprachkenntnisse
        st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)
        
        languages_html = "<p style='font-size: 22px;'>"
        for lang in t['languages']:
            languages_html += f"{lang['flag']} {lang['name']} <span style='color: gray; font-size: 18px;'>({lang['level']})</span> &nbsp;&nbsp;&nbsp;"
        languages_html += "</p>"
        
        st.markdown(languages_html, unsafe_allow_html=True)

    return t