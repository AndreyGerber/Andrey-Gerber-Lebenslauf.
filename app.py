import streamlit as st

if "lang" not in st.session_state:
    st.session_state.lang = "de"


col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🇩🇪 Deutsch"):
        st.session_state.lang = "de"
        st.rerun()

with col2:
    if st.button("🇬🇧 English"):
        st.session_state.lang = "en"
        st.rerun()

with col3:
    if st.button("🇷🇺 Русский"):
        st.session_state.lang = "ru"
        st.rerun()

from utils.text_loader import get_text

t = get_text(st.session_state.lang)


st.markdown(f"<h2 style='text-align: center;'>{t['welcome']}</h2>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: #4B0082;'>{t['title']}</h1>", unsafe_allow_html=True)


def lang_button(label, code):
    is_active = st.session_state.lang == code

    if st.button(label, key=f"lang_{code}"):
        st.session_state.lang = code
        st.rerun()

col1, col2, col3 = st.columns(3)

with col1:
    lang_button("🇩🇪 Deutsch", "de")

with col2:
    lang_button("🇬🇧 English", "en")

with col3:
    lang_button("🇷🇺 Русский", "ru")