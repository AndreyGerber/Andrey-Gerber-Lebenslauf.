
import streamlit as st
import plotly.express as px
import pandas as pd

# Seiteneinstellungen
st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# 1. Titel ganz oben (in zwei Zeilen)
st.markdown("<h1 style='text-align: center;'>Willkommen auf der Seite</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Lebenslauf von Andrey Gerber</h2>", unsafe_allow_html=True)


st.divider() # Eine Trennlinie für die Optik

# 2. Bereich darunter: Links Slideshow, Rechts Daten
col1, col2 = st.columns([1, 1]) # Erstellt zwei gleich breite Spalten

col1, col2 = st.columns([1, 1.2]) 

with col1:
    st.subheader("it's me")
    
    # 1. Definieren der Pfade (Probiere es mal mit ./ am Anfang)
    meine_bilder = ["./images/ich1.JPG", "./images/ich_pass.png"]
    
    wahl = st.radio("Foto auswählen:", range(1, len(meine_bilder) + 1), horizontal=True, label_visibility="collapsed")
    
    # 2. Das Bild anzeigen mit Fehler-Check
    bild_pfad = meine_bilder[wahl - 1]
    
    import os
    if os.path.exists(bild_pfad):
        st.image(bild_pfad, width=280)
    else:
        st.error(f"Datei nicht gefunden: {bild_pfad}")
        # Zeigt dir an, welche Dateien Streamlit ÜBERHAUPT im Ordner sieht:
        st.write("Vorhandene Dateien im Ordner 'images':", os.listdir("./images") if os.path.exists("./images") else "Ordner nicht gefunden")


with col2:
    st.subheader("Meine Kontaktdaten")
    st.write(f"**Name:** Andrey Gerber")
    st.write(f"**Wohnadresse:** Brauchst du nicht, ruf an oder @")
    st.write("📞 0176 43 733 099")
    st.write("📧 andrey.gerber.88@gmail.com")

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