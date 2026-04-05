
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








# 3. Hobby-Timeline mit Plotly
import plotly.graph_objects as go

st.subheader("Mein Weg")

# 1. Daten für deine Meilensteine festlegen
meilensteine = [
    {"jahr": 1988, "event": "Geburt", "ort": "UdSSR"},
    {"jahr": 1995, "event": "Einschulung", "ort": "Russland"},
    {"jahr": 2004, "event": "Umzug", "ort": "Deutschland"},
    {"jahr": 2024, "event": "Heute", "ort": "Portfolio"}
]

jahre = [m["jahr"] for m in meilensteine]
texte = [f"<b>{m['jahr']}</b><br>{m['event']}<br>{m['ort']}" for m in meilensteine]

# 2. Den Zeitstrahl-Pfeil erstellen
fig_weg = go.Figure()

# Die Hauptlinie (der Schaft des Pfeils)
fig_weg.add_trace(go.Scatter(
    x=[1987, 2026], 
    y=[0, 0],
    mode="lines",
    line=dict(color="#4B0082", width=6),
    hoverinfo="skip"
))

# Die Meilensteine als Punkte auf der Linie
fig_weg.add_trace(go.Scatter(
    x=jahre,
    y=[0] * len(jahre),
    mode="markers+text",
    marker=dict(size=12, color="#4B0082", symbol="diamond"),
    text=texte,
    textposition="top center",
    hoverinfo="none"
))

# 3. Die Pfeilspitze hinzufügen
fig_weg.add_annotation(
    x=2026, y=0,
    ax=2025, ay=0,
    xref="x", yref="y",
    axref="x", ayref="y",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=6,
    arrowcolor="#4B0082"
)

# Layout-Einstellungen (Achsen verstecken)
fig_weg.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[1985, 2028]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 1]),
    margin=dict(l=20, r=20, t=50, b=20),
    height=250,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_weg, use_container_width=True)
