
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
from streamlit_plotly_events import plotly_events
import pandas as pd

# 1. DATEN DER STATIONEN (Deine Jahre aus der Zeichnung)
stations_data = [
    {"jahr": 1988, "event": "Geburt", "info": "Start in der UdSSR"},
    {"jahr": 1996, "event": "Schule", "info": "Kindheit in Russland"},
    {"jahr": 2006, "event": "Emigration", "info": "Flug Omsk -> Neustrelitz"},
    {"jahr": 2010, "event": "Studium/Arbeit", "info": "Erste Schritte in DE"},
    {"jahr": 2017, "event": "Meilenstein", "info": "Weitere Entwicklung"},
    {"jahr": 2019, "event": "Karriere", "info": "Beruflicher Weg"},
    {"jahr": 2022, "event": "Hausbau", "info": "Wurzeln schlagen"},
    {"jahr": 2026, "event": "Zukunft", "info": "Ausblick"}
]
df = pd.DataFrame(stations_data)

if 'selected_year' not in st.session_state:
    st.session_state.selected_year = 1988

# 2. DEN SCHWARZEN PFEIL ZEICHNEN
fig = go.Figure()

# Die Hauptlinie (Pfeilschaft)
fig.add_trace(go.Scatter(
    x=[1985, 2027], y=[0, 0],
    mode='lines',
    line=dict(color='black', width=3),
    hoverinfo='none'
))

# Die Rauten (Events)
fig.add_trace(go.Scatter(
    x=df['jahr'],
    y=[0] * len(df),
    mode='markers+text',
    marker=dict(
        symbol='diamond',
        size=18,
        color='white',
        line=dict(color='black', width=2)
    ),
    text=df['jahr'],
    textposition="top center",
    textfont=dict(size=16, color="black"),
    hovertext=df['event'],
    hoverinfo="text"
))

# Die Pfeilspitze
fig.add_annotation(
    x=2028, y=0, ax=2027, ay=0,
    xref="x", yref="y", showarrow=True,
    arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="black"
)

# Layout-Einstellungen für maximale Sauberkeit
fig.update_layout(
    height=200,
    margin=dict(l=10, r=10, t=50, b=10),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[1985, 2030]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 0.5]),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    clickmode='event+select'
)

# 3. INTERAKTION (Klick auf Raute)
st.write("### 📍 Wähle eine Station auf meinem Lebensweg:")
selected_point = plotly_events(fig, click_event=True, hover_event=False)

if selected_point:
    st.session_state.selected_year = selected_point[0]['x']

# 4. ANZEIGE DES INHALTS UNTER DEM PFEIL
st.divider()
wahl = df[df['jahr'] == st.session_state.selected_year].iloc[0]

c1, c2 = st.columns([1, 2])
with c1:
    st.markdown(f"## {wahl['jahr']}")
    st.subheader(wahl['event'])
    st.info(wahl['info'])

with c2:
    # Hier kommt deine Visualisierung rein (Karte/Bild)
    if wahl['jahr'] == 2006:
        st.success("✈️ Hier startet jetzt die Flug-Animation von Omsk nach Neustrelitz!")
    else:
        st.write(f"*(Platzhalter für Visualisierung von {wahl['jahr']})*")