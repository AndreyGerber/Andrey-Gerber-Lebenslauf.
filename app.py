
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
import streamlit as st

st.subheader("Mein Lebensweg in Farben")



# 1. Daten definieren (Beispiel)
events = [{"x": 2022, "text": "Hausbau"}]  # hier Zeitperioden angeben



fig = go.Figure()

# --- 2. DER FARBIGE PFEIL (3 SEGMENTE) ---
# UdSSR (Rot)
fig.add_trace(go.Scatter(
    x=[1988, 1991], y=[0, 0], mode="lines",
    line=dict(color="#CC0000", width=6), showlegend=False, hoverinfo="skip"
))
# Russland (Blau - stellvertretend für die Trikolore)
fig.add_trace(go.Scatter(
    x=[1991, 2006], y=[0, 0], mode="lines",
    line=dict(color="#003399", width=6), showlegend=False, hoverinfo="skip"
))
# Deutschland (Gold/Gelb)
fig.add_trace(go.Scatter(
    x=[2006, 2026], y=[0, 0], mode="lines",
    line=dict(color="#FFCC00", width=6), showlegend=False, hoverinfo="skip"
))

# --- 3. DIE PFEILSPITZE AM ENDE ---
fig.add_annotation(
    x=2027, y=0, ax=2026, ay=0,
    xref="x", yref="y", axref="x", ayref="y",
    showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=6, arrowcolor="#FFCC00"
)

# --- 4. RAUTEN & TEXTE ---
fig.add_trace(go.Scatter(
    x=[e["x"] for e in events],
    y=[0] * len(events),
    mode="markers+text",
    marker=dict(symbol="diamond", size=15, color="white", line=dict(width=2, color="black")),
    text=[f"<b>{e['x']}</b><br>{e}" for e in events],
    textposition="bottom center",
    hoverinfo="none",
    showlegend=False
))

# --- 5. BESCHRIFTUNG UNTER DEM START (1988) ---
fig.add_annotation(
    x=1988, y=-0.2, text="<b>1988</b>",
    showarrow=False, font=dict(size=14, color="black")
)

# --- 6. LÄNDER-ÜBERSCHRIFTEN ---
laender = [
    {"x": 1989.5, "label": "Sowjetunion"},
    {"x": 1998.5, "label": "Russland"},
    {"x": 2016, "label": "Deutschland"}
]
for l in laender:
    fig.add_annotation(x=l["x"], y=0.3, text=f"<b>{l['label']}</b>", showarrow=False)

# Layout-Feinschliff
fig.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[1987, 2028]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.8, 0.8]),
    height=300,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

