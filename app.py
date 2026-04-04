
import streamlit as st
import plotly.express as px
import pandas as pd

import streamlit as st
import os

# Seiteneinstellungen
st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# 1. Titel (zentriert und zwei Zeilen)
st.markdown("<h1 style='text-align: center;'>Willkommen auf der Seite</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Lebenslauf von Andrey Gerber</h2>", unsafe_allow_html=True)

st.divider()

# 2. Slideshow-Logik (Session State)
if 'bild_index' not in st.session_state:
    st.session_state.bild_index = 0

meine_bilder = ["images/ich1.JPG", "images/ich_pass.png"]

# 3. Layout: 3 Spalten (Bilder | Deine Zeichnung | Daten)
col_bild, col_mitte, col_daten = st.columns([1.5, 1.0, 1.5])

with col_bild:
    # Aktuelles Foto anzeigen
    st.image(meine_bilder[st.session_state.bild_index], width=280)
    
    # Pfeile direkt unter das Foto
    p1, p2 = st.columns(2)
    with p1:
        if st.button("⬅️"):
            st.session_state.bild_index = (st.session_state.bild_index - 1) % len(meine_bilder)
            st.rerun()
    with p2:
        if st.button("➡️"):
            st.session_state.bild_index = (st.session_state.bild_index + 1) % len(meine_bilder)
            st.rerun()

with col_mitte:
    # Hier laden wir deine Zeichnung statt nur Text
    st.markdown("<p style='text-align: center; font-weight: bold;'>it's me</p>", unsafe_allow_html=True)
    
    # Pfad zu deiner selbstgemalten Datei (anpassen, wenn der Name anders ist!)
    pfad_zeichnung = "images/itsme.png" 
    
    if os.path.exists(pfad_zeichnung):
        st.image(pfad_zeichnung, use_container_width=True)
    else:
        st.info("Hier erscheint bald meine Zeichnung...")
    
    st.markdown("<h2 style='text-align: center;'>←</h2>", unsafe_allow_html=True)

with col_daten:
    st.subheader("Meine Kontaktdaten")
    st.write(f"**Name:** Andrey Gerber")
    st.write("📞 0176 43 733 099")
    st.write("📧 andrey.gerber.88@gmail.com")
    st.write("**Wohnadresse:** Brauchst du nicht, ruf an oder @")

st.divider()

# ... hier geht es weiter mit deinem "Mein Weg" (Flaggen) und der Timeline




# 3. Hobby-Timeline mit Plotly
st.subheader("Hobbys & Aktivitäten")

# Daten für die Zeitachse aufbereiten
data = [
    dict(Hobby="Schach", Start='1996-01-01', Ende='2026-01-01', Typ="Kontinuierlich"),
    dict(Hobby="Eishockey", Start='1998-01-01', Ende='2006-01-01', Typ="Kontinuierlich"),
    dict(Hobby="Yoga", Start='2018-01-01', Ende='2026-01-01', Typ="Kontinuierlich"),
    # Fußball mit Pause
    dict(Hobby="Fussball", Start='1997-01-01', Ende='2008-01-01', Typ="Aktiv"),
    dict(Hobby="Fussball", Start='2008-01-01', Ende='2020-01-01', Typ="Pause (Striche)"),
    dict(Hobby="Fussball", Start='2020-01-01', Ende='2026-01-01', Typ="Wieder aktiv")
]

df = pd.DataFrame(data)

# Farben definieren
colors = {"Kontinuierlich": "#31333F", "Aktiv": "#0068C9", "Pause (Striche)": "#D3D3D3", "Wieder aktiv": "#0068C9"}

fig = px.timeline(df, x_start="Start", x_end="Ende", y="Hobby", color="Typ", 
                  color_discrete_map=colors, template="plotly_white")

fig.update_yaxes(autorange="reversed") # Damit Schach oben steht
fig.update_layout(showlegend=False, height=300)

st.plotly_chart(fig, use_container_width=True)

st.info("💡 Fussball: play (not drink in stadium)")