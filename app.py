
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






# --- 1. DATEN DEFINIEREN ---
stationen = [
    {"jahr": 1988, "event": "Geburt", "land": "UdSSR", "farbe": "#d32f2f"}, # Rot
    {"jahr": 1991, "event": "Russland", "land": "Russland", "farbe": "#1976d2"}, # Blau
    {"jahr": 1996, "event": "Schule", "land": "Russland", "farbe": "#1976d2"},
    {"jahr": 2006, "event": "Emigration", "land": "Deutschland", "farbe": "#fbc02d"}, # Gold
    {"jahr": 2022, "event": "Hausbau", "land": "Deutschland", "farbe": "#fbc02d"},
    {"jahr": 2024, "event": "Heute", "land": "Deutschland", "farbe": "#fbc02d"}
]

if 'selected_year' not in st.session_state:
    st.session_state.selected_year = 1988

# --- 2. DEN PFEIL BAUEN (Layout) ---
st.write("### 🌍 Klicke auf ein Ereignis:")

# Wir erstellen 6 Spalten für die 6 Ereignisse
cols = st.columns(len(stationen))

for i, s in enumerate(stationen):
    with cols[i]:
        # Der farbige Balken über dem Button (verbindet die Stationen)
        st.markdown(f"""
            <div style="
                background-color: {s['farbe']}; 
                height: 10px; 
                margin-bottom: 5px;
                border-radius: 2px;
                width: 100%;
            "></div>
        """, unsafe_allow_html=True)
        
        # Der Button als "Raute" (Highlight wenn ausgewählt)
        label = f"◆ {s['jahr']}" if s['jahr'] == st.session_state.selected_year else f"◇ {s['jahr']}"
        if st.button(label, key=f"btn_{s['jahr']}", use_container_width=True):
            st.session_state.selected_year = s['jahr']
            st.rerun()

# --- 3. INHALTE ANZEIGEN ---
st.divider()
aktuelle_wahl = next(item for item in stationen if item["jahr"] == st.session_state.selected_year)

col_text, col_visual = st.columns([1, 2])

with col_text:
    st.header(f"Station: {aktuelle_wahl['jahr']}")
    st.subheader(aktuelle_wahl['event'])
    st.write(f"Land: {aktuelle_wahl['land']}")
    
    # Hier kannst du deine Bilder/Logik einfügen
    if aktuelle_wahl['jahr'] == 1996:
        st.info("📸 Hier öffnen wir jetzt dein Schulbild...")
    elif aktuelle_wahl['jahr'] == 2006:
        st.success("✈️ Animation: Flug von Omsk nach Neustrelitz startet!")

with col_visual:
    # Platzhalter für Karte oder Animation
    st.write("*(Hier erscheint deine Karte oder Animation)*")



