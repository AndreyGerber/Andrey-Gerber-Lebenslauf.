
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






import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

# --- 1. DATEN FÜR DEN PFEIL ---
events_data = [
    {"jahr": 1988, "land": "Sowjetunion", "farbe": "#d32f2f", "name": "Geburt"},
    {"jahr": 1991, "land": "Russland", "farbe": "#1976d2", "name": "Russland"},
    {"jahr": 1996, "land": "Russland", "farbe": "#1976d2", "name": "Schule"},
    {"jahr": 2006, "land": "Deutschland", "farbe": "#fbc02d", "name": "Emigration"},
    {"jahr": 2022, "land": "Deutschland", "farbe": "#fbc02d", "name": "Hausbau"},
    {"jahr": 2024, "land": "Deutschland", "farbe": "#fbc02d", "name": "Heute"}
]
df_timeline = pd.DataFrame(events_data)

# --- 2. GRAFIK ERSTELLEN ---
fig = go.Figure()

# Hintergrund-Segmente (Die dicken farbigen Balken)
segments = [(1988, 1991, "#d32f2f"), (1991, 2006, "#1976d2"), (2006, 2024, "#fbc02d")]
for start, end, color in segments:
    fig.add_trace(go.Scatter(
        x=[start, end], y=[0, 0], mode='lines',
        line=dict(color=color, width=12), hoverinfo='none'
    ))

# Die Marker (Weiße Rauten wie in deiner Zeichnung)
fig.add_trace(go.Scatter(
    x=df_timeline['jahr'], y=[0]*len(df_timeline),
    mode='markers+text',
    marker=dict(symbol='diamond', size=18, color='white', line=dict(width=2, color='black')),
    text=df_timeline['jahr'], textposition="bottom center",
    hovertext=df_timeline['name'], hoverinfo="text"
))

# Pfeilspitze am Ende
fig.add_annotation(x=2024.5, y=0, ax=2023.5, ay=0, xref="x", yref="y",
                   showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor="black")

# Layout aufräumen
fig.update_layout(
    height=180, margin=dict(l=40, r=40, t=20, b=20),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[1987, 2026]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 0.5]),
    showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
)

# --- 3. INTERAKTION ---
st.markdown("### Klicke auf ein Ereignis (Raute):")
selected_point = plotly_events(fig, click_event=True, hover_event=False)

# Wenn geklickt wird, Jahr im Session State speichern
if selected_point:
    st.session_state.selected_year = selected_point[0]['x']

# --- 4. ANZEIGE DER STATION (Animation oder Bild) ---
st.divider()
jahr = st.session_state.get('selected_year', 1988)
station = df_timeline[df_timeline['jahr'] == jahr].iloc[0]

c1, c2 = st.columns([1, 1])
with c1:
    st.header(f"Station: {jahr}")
    st.subheader(station['name'])
    # Hier kannst du deine Bilder für 1996 oder 2006 laden
    st.write(f"Hier öffnen wir jetzt die Animation oder das Bild für {station['land']}.")

with c2:
    # Hier kommt deine Karte (wie im vorherigen Schritt besprochen)
    st.info("🗺️ Karte wird auf den Ort zentriert...")



