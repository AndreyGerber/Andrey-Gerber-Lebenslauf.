import streamlit as st
import plotly.express as px
import pandas as pd
import os
from PIL import Image

# Seiteneinstellungen
st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# 1. Titel (Anpassung: Dunkellila Farbe)
st.markdown("<h1 style='text-align: center;'>Willkommen auf der Seite</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #4B0082;'>Lebenslauf von Andrey Gerber</h1>", unsafe_allow_html=True)

st.divider()

# --- FUNKTION FÜR BILDER ---
def lade_formatiertes_bild(name, target_size=(600, 400)):
    base_path = os.path.dirname(__file__)
    pfad = os.path.join(base_path, "images", name)
    if os.path.exists(pfad):
        img = Image.open(pfad)
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
        new_img.paste(img, ((target_size[0] - img.size[0]) // 2, (target_size[1] - img.size[1]) // 2))
        return new_img
    return None

if 'bild_index' not in st.session_state:
    st.session_state.bild_index = 0

slideshow_bilder = ["ich1.JPG", "ich_pass.png"]
zeichnung_name = "itsme2.png"

# --- LAYOUT ---
col_bild, col_mitte, col_daten = st.columns([1.5, 1.0, 1.5])

with col_bild:
    aktuelles_foto = lade_formatiertes_bild(slideshow_bilder[st.session_state.bild_index])
    if aktuelles_foto:
        st.image(aktuelles_foto, use_container_width=True)
    
    p_links, _, p_rechts = st.columns([1, 4, 1]) 
    if p_links.button("⬅️"):
        st.session_state.bild_index = (st.session_state.bild_index - 1) % len(slideshow_bilder)
        st.rerun()
    if p_rechts.button("➡️"):
        st.session_state.bild_index = (st.session_state.bild_index + 1) % len(slideshow_bilder)
        st.rerun()

with col_mitte:
    zeichnung = lade_formatiertes_bild(zeichnung_name, target_size=(300, 300))
    if zeichnung: st.image(zeichnung, use_container_width=True)

with col_daten:
    # Anpassung: Schriftgröße deutlich vergrößert
    st.markdown("<h3 style='font-size: 26px;'>Meine Kontaktdaten</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'><strong>Name:</strong> Andrey Gerber</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'>📞 <strong>0176 43 733 099</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'>📧 <a href='mailto:andrey.gerber.88@gmail.com'>andrey.gerber.88@gmail.com</a></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'><strong>Wohnadresse:</strong> Brauchst du nicht, ruf an oder @</p>", unsafe_allow_html=True)

st.divider()

# --- HOBBYS ---
st.subheader("Hobbys & Aktivitäten")
data = [
    dict(Hobby="Schach", Start='1996-01-01', Ende='2026-01-01', Typ="Kontinuierlich"),
    dict(Hobby="Eishockey", Start='1998-01-01', Ende='2006-01-01', Typ="Kontinuierlich"),
    dict(Hobby="Yoga", Start='2018-01-01', Ende='2026-01-01', Typ="Kontinuierlich"),
    dict(Hobby="Fussball", Start='1997-01-01', Ende='2008-01-01', Typ="Aktiv"),
    dict(Hobby="Fussball", Start='2008-01-01', Ende='2020-01-01', Typ="Pause (Striche)"),
    dict(Hobby="Fussball", Start='2020-01-01', Ende='2026-01-01', Typ="Wieder aktiv")
]
df = pd.DataFrame(data)
colors = {"Kontinuierlich": "#31333F", "Aktiv": "#0068C9", "Pause (Striche)": "#D3D3D3", "Wieder aktiv": "#0068C9"}
fig = px.timeline(df, x_start="Start", x_end="Ende", y="Hobby", color="Typ", color_discrete_map=colors, template="plotly_white")
fig.update_yaxes(autorange="reversed")
fig.update_layout(showlegend=False, height=300)
st.plotly_chart(fig, use_container_width=True)
st.info("💡 Fussball: play (not drink in stadium)")
