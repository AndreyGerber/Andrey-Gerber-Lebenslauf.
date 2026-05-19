import streamlit as st
from utils.text_loader import get_text


def show_header():
    # Sprache initialisieren
    if "lang" not in st.session_state:
        st.session_state.lang = "de"

    # Buttons
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

    # Header anzeigen
    st.markdown(f"<h2 style='text-align: center;'>{t['welcome']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: #4B0082;'>{t['title']}</h1>", unsafe_allow_html=True)

    st.divider()

    return t  # 🔥 DAS IST ENTSCHEIDEND