import streamlit as st
from components.header import show_header

st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

lang = st.selectbox("🌍 Sprache / Language", ["de", "en", "ru"])

show_header(lang)