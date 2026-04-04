
import streamlit as st
import plotly.express as px
import pandas as pd

import os

# Seiteneinstellungen
st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# 1. Titel (zentriert und zwei Zeilen)
st.markdown("<h1 style='text-align: center;'>Willkommen auf der Seite</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Lebenslauf von Andrey Gerber</h2>", unsafe_allow_html=True)

st.divider()


from PIL import Image, ImageOps

# --- 1. FUNKTION FÜR STABILE BILDGRÖSSE ---
def lade_formatiertes_bild(name, target_size=(600, 400)):
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


    # Pfeile direkt unter das Foto
    p1, p2 = st.columns(2)
    with p1:
        if st.button("⬅️"):
            st.session_state.bild_index = (st.session_state.bild_index - 1) % len(slideshow_bilder)
            st.rerun()
    with p2:
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
    st.subheader("Meine Kontaktdaten")
    st.write(f"**Name:** Andrey Gerber")
    st.markdown("📞 **0176 43 733 099**")
    st.markdown("📧 [andrey.gerber.88@gmail.com](mailto:andrey.gerber.88@gmail.com)")
    st.write("---")
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