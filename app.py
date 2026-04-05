
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






# --- 4. DATEN FÜR DIE STORY-NAVIGATION ---
import plotly.graph_objects as go

# --- 1. DATEN FÜR DEN PFEIL ---
df_timeline = pd.DataFrame([
    {"jahr": 1988, "event": "Geburt", "farbe": "red", "symbol": "diamond"},
    {"jahr": 1991, "event": "Russland", "farbe": "blue", "symbol": "diamond"},
    {"jahr": 1996, "event": "Schule", "farbe": "blue", "symbol": "diamond"},
    {"jahr": 2006, "event": "Emigration", "farbe": "gold", "symbol": "diamond"},
    {"jahr": 2022, "event": "Hausbau", "farbe": "gold", "symbol": "diamond"},
    {"jahr": 2024, "event": "Heute", "farbe": "gold", "symbol": "arrow-right"}
])

# --- 2. DEN PFEIL ZEICHNEN ---
fig_arrow = go.Figure()

# Die Linie (dein Pfeil)
fig_arrow.add_trace(go.Scatter(
    x=[1988, 1991, 2006, 2024], 
    y=[0, 0, 0, 0],
    mode='lines',
    line=dict(color='black', width=3),
    hoverinfo='none'
))

# Die farbigen Segmente (UdSSR, Russland, Deutschland)
segments = [
    (1988, 1991, 'red'), (1991, 2006, 'blue'), (2006, 2024, 'gold')
]
for start, end, color in segments:
    fig_arrow.add_trace(go.Scatter(
        x=[start, end], y=[0, 0],
        mode='lines',
        line=dict(color=color, width=8),
        hoverinfo='none'
    ))

# Die klickbaren Ereignisse (Rauten)
fig_arrow.add_trace(go.Scatter(
    x=df_timeline['jahr'],
    y=[0] * len(df_timeline),
    mode='markers+text',
    marker=dict(symbol='diamond', size=15, color='white', line=dict(width=2, color='black')),
    text=df_timeline['jahr'],
    textposition="bottom center",
    customdata=df_timeline['event'],
    hovertemplate="<b>%{text}</b>: %{customdata}<extra></extra>"
))

# Layout-Anpassungen für "sauberen" Look
fig_arrow.update_layout(
    height=150, margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[1987, 2025]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 0.5]),
    showlegend=False,
    clickmode='event+select'
)

# --- 3. INTERAKTION AUSWERTEN ---
# Hier nutzen wir st_plotly_events (muss evtl. mit 'pip install streamlit-plotly-events' installiert werden)
# ODER wir nutzen einfache Radio-Buttons als Fallback, die wie der Zeitstrahl gestylt sind.

st.markdown("### Klicke auf ein Ereignis auf dem Zeitstrahl:")
selected_event = st.selectbox("Wähle ein Jahr:", df_timeline['jahr'], label_visibility="collapsed")

# --- 4. ANZEIGE DER INHALTE (Wie vorher) ---
st.session_state.selected_year = selected_event
# Hier folgt dein Code für Karte, Bilder oder Animationen...



