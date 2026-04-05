
import streamlit as st
import plotly.express as px
import pandas as pd

import os

# Seiteneinstellungen
st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# 1. Titel (zentriert und zwei Zeilen)
st.markdown("<h2 style='text-align: center;'>Willkommen auf der Seite</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #4B0082;'>Lebenslauf von Andrey Gerber</h1>", unsafe_allow_html=True)
st.divider()


from PIL import Image, ImageOps

# --- 1. FUNKTION FÜR STABILE BILDGRÖSSE ---
def lade_formatiertes_bild(name, target_size=(900, 600)):
    base_path = os.path.dirname(__file__)
    pfad = os.path.join(base_path, "images", name)
    if os.path.exists(pfad):
        img = Image.open(pfad)
        # Erstellt ein Bild mit festem Format, ohne es zu verzerren (Padding)
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        # Erzeugt einen transparenten Hintergrund in der Zielgröße
        new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
        # Zentriert das Bild auf dem Hintergrund
        new_img.paste(img, ((target_size[0] - img.size[0]) // 2, 
                            (target_size[1] - img.size[1]) // 2))
        return new_img
    return None

# --- 2. DATEN & LOGIK ---
if 'bild_index' not in st.session_state:
    st.session_state.bild_index = 0

slideshow_bilder = ["ich1.JPG", "ich_pass.png"]
zeichnung_name = "itsme2.png"

# --- 3. LAYOUT: 3 SPALTEN ---
col_bild, col_mitte, col_daten = st.columns([1.5, 1.0, 1.5])

with col_bild:
    # Stabiles Bild laden
    aktuelles_foto = lade_formatiertes_bild(slideshow_bilder[st.session_state.bild_index])
    if aktuelles_foto:
        st.image(aktuelles_foto, use_container_width=True)
    else:
        st.error(f"Datei fehlt: {slideshow_bilder[st.session_state.bild_index]}")


    p_links, p_mitte, p_rechts = st.columns([1, 4, 1]) 
    
    with p_links:
        if st.button("⬅️"):
            st.session_state.bild_index = (st.session_state.bild_index - 1) % len(slideshow_bilder)
            st.rerun()
            
    with p_rechts:
        if st.button("➡️"):
            st.session_state.bild_index = (st.session_state.bild_index + 1) % len(slideshow_bilder)
            st.rerun()

with col_mitte:
    # Deine Zeichnung laden (ebenfalls formatiert für Stabilität)
    zeichnung = lade_formatiertes_bild(zeichnung_name, target_size=(300, 300))
    if zeichnung:
        st.image(zeichnung, use_container_width=True)
    else:
        st.info("Hier erscheint bald deine Zeichnung...")

with col_daten:
    # Anpassung: Schriftgröße deutlich vergrößert
    st.markdown("<h3 style='font-size: 26px;'>Meine Kontaktdaten</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'><strong>Name:</strong> Andrey Gerber</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'>📞 <strong>0176 43 733 099</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'>📧 <a href='mailto:andrey.gerber.88@gmail.com'>andrey.gerber.88@gmail.com</a></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'><strong>Wohnadresse:</strong> Brauchst du nicht, ruf an oder @</p>", unsafe_allow_html=True)


st.divider()

# ... hier geht es weiter mit deinem "Mein Weg" (Flaggen) und der Timeline







import streamlit as st
import plotly.graph_objects as go

# --- 1. DATEN ---
jahre = [1988, 1996, 2006, 2010, 2017, 2019, 2022, 2026]

# --- 2. GRAFIK ERSTELLEN ---
fig = go.Figure()

# Hauptlinie: Startet exakt bei 1988 und geht bis nach 2026
fig.add_trace(go.Scatter(
    x=[1988, 2030], y=[0, 0],
    mode='lines',
    line=dict(color='black', width=2),
    hoverinfo='none',
    showlegend=False
))

# Senkrechter Startstrich bei 1988
fig.add_shape(
    type="line",
    x0=1988, y0=-0.15, x1=1988, y1=0.15,
    line=dict(color="black", width=3)
)

# Weiße Rauten und Jahre
fig.add_trace(go.Scatter(
    x=jahre, y=[0] * len(jahre),
    mode='markers+text',
    marker=dict(
        symbol='diamond', 
        size=18, 
        color='white', 
        line=dict(color='black', width=1.5)
    ),
    text=jahre,
    textposition="bottom center",
    textfont=dict(size=12, color="black"),
    hoverinfo='none',
    showlegend=False
))

# Pfeilspitze am Ende (nach rechts)
fig.add_annotation(
    x=2032, y=0,           # Spitze des Pfeils
    ax=2030, ay=0,         # Schaft-Ende
    xref="x", yref="y",
    axref="x", ayref="y",
    showarrow=True,
    arrowhead=2, 
    arrowsize=1.2, 
    arrowwidth=2, 
    arrowcolor="black"
)

# Layout-Anpassung
fig.update_layout(
    height=200,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(
        showgrid=False, 
        zeroline=False, 
        showticklabels=False, 
        # Range startet kurz vor 1988, damit der Strich gut sichtbar ist
        range=[1985, 2035] 
    ),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 0.5]),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

# Anzeige in Streamlit
st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True, 'displayModeBar': False})



