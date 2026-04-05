
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

#events = [{"x": 2022, "text": "Hausbau"}]  # hier Zeitperioden angeben






import plotly.graph_objects as go
import streamlit as st

st.subheader("Mein Lebensweg")

# 1. Deine Meilensteine
events = [{"x": 2022, "text": "Hausbau"}]  # hier Zeitperioden angeben

fig = go.Figure()

# --- 2. FUNKTION FÜR ECHTE FLAGGEN-BILDER ---
def add_flag_image(fig, x_start, x_end, img_url):
    fig.add_layout_image(
        dict(
            source=img_url,
            xref="x", yref="y",
            x=x_start, y=0.6, # Obere linke Ecke des Bildes
            sizex=x_end - x_start, sizey=0.6, # Breite und Höhe des Bildes
            sizing="stretch", # Bild wird genau in den Bereich eingepasst
            opacity=1.0,
            layer="below"
        )
    )

# --- 3. DIE FLAGGEN PLATZIEREN ---
# Hier Pfade zu deinen Bildern im 'images' Ordner oder URLs einfügen
add_flag_image(fig, 1988, 1991, "https://wikimedia.org")
add_flag_image(fig, 1991, 2004, "https://wikimedia.org")
add_flag_image(fig, 2004, 2026, "https://wikimedia.org")

# --- 4. RAUTEN & TEXTE (Auf mittlerer Höhe 0.3) ---
fig.add_trace(go.Scatter(
    x=[e["x"] for e in events],
    y=[0.3] * len(events),
    mode="markers+text",
    marker=dict(symbol="diamond", size=18, color="white", line=dict(width=2, color="black")),
    text=[f"<b>{e['x']}</b><br>{e}" for e in events],
    textposition="bottom center",
    showlegend=False
))

# --- 5. PFEILSPITZE & STARTSTRICH ---
# Die Pfeilspitze bekommt die Farbe der letzten Flagge (Gold)
fig.add_annotation(
    x=2028, y=0.3, ax=2026, ay=0.3,
    xref="x", yref="y", axref="x", ayref="y",
    showarrow=True, arrowhead=3, arrowsize=4, arrowwidth=2, arrowcolor="#FFCC00"
)

fig.add_shape(type="line", x0=1988, x1=1988, y0=0, y1=0.6, line=dict(color="black", width=4))
fig.add_annotation(x=1988, y=-0.2, text="<b>1988</b>", showarrow=False, font=dict(size=16))

# --- 6. LAYOUT ---
fig.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[1985, 2030]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 1.2]),
    height=400,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10)
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


