"""
app.py

Orchestriert nur noch: Sprache laden -> Sektionen der Reihe nach rendern.
Der eigentliche Inhalt/Layout jeder Sektion lebt in sections/*.py.

Alle Original-Sektionen sind jetzt modularisiert:
Header -> Werdegang -> Zeugnis-Galerie -> Zertifikatswände (DS + MLOps)
-> Fertigkeiten -> Hobbies -> Zitate -> Bonus.

Neue Sektion hinzufügen? Drei Schritte:
1. sections/neue_sektion.py mit render_neue_sektion(t) anlegen
2. Import oben ergänzen
3. Aufruf an der gewünschten Stelle unten einfügen
"""

import streamlit as st
import importlib

from sections.header import render_header
from sections.timeline import render_timeline_graph, render_timeline_details
from sections.certificates import render_certificate_gallery
from sections.skills import render_skills
from sections.hobbies import render_hobbies
from sections.quotes import render_quotes
from sections.bonus import render_bonus
from sections.cert_config import CERT_DEFS_DATA_SCIENCE, CERT_DEFS_MLOPS
from sections.cert_wall import render_cert_wall
from sections.cert_carousel import render_cert_carousel

# --- PAGE CONFIG (nur EINMAL, ganz am Anfang!) ---
st.set_page_config(page_title="Andrey Gerber - Resume", layout="wide")

# --- SPRACHAUSWAHL ---
if "language" not in st.session_state:
    st.session_state.language = "de"

cols = st.columns([7.5, 1.5, 1.5, 1.5])
with cols[1]:
    if st.button("🇩🇪 DE", key="lang_de", use_container_width=True):
        st.session_state.language = "de"
        st.rerun()
with cols[2]:
    if st.button("🇬🇧 EN", key="lang_en", use_container_width=True):
        st.session_state.language = "en"
        st.rerun()
with cols[3]:
    if st.button("🇷🇺 RU", key="lang_ru", use_container_width=True):
        st.session_state.language = "ru"
        st.rerun()

st.markdown("<hr style='margin-top: 5px; margin-bottom: 10px;'>", unsafe_allow_html=True)

# Lädt translations/de.py, translations/en.py oder translations/ru.py
lang_module = importlib.import_module(f"translations.{st.session_state.language}")
t = lang_module.TRANSLATIONS

# --- SEKTIONEN LADEN (Prinzip: "lade das, das und das") ---
render_header(t)
render_timeline_graph(t)
render_timeline_details(t)
render_certificate_gallery(t)

# TODO, sobald modularisiert (Reihenfolge = Original-Seitenaufbau):
# from sections.skills import render_skills
# from sections.hobbies import render_hobbies
# from sections.quotes import render_quotes
# from sections.bonus import render_bonus

render_cert_wall(
    cert_defs=CERT_DEFS_DATA_SCIENCE,
    folder="images/Data_Scientist",
    title=t["cert_wall_ds_title"],
    subtitle=t["cert_wall_ds_subtitle"],
    widget_key="ds",
)

render_cert_carousel(
    cert_defs=CERT_DEFS_MLOPS,
    folder="images/MLOps",
    title=t["cert_wall_mlops_title"],
    subtitle=t["cert_wall_mlops_subtitle"],
    widget_key="mlops",
)

render_skills(t)
render_hobbies(t)
render_quotes(t)
render_bonus(t)