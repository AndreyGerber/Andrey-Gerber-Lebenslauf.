
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
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = 1988

# Hier definierst du deine Stationen und Koordinaten
STATIONEN = {
    1988: {"titel": "Geburt in der UdSSR", "ort": "Tscherlak", "lat": 54.15, "lon": 74.80, "text": "In Tscherlak geboren, kurz vor dem Zerfall der Sowjetunion."},
    1996: {"titel": "Schulzeit", "ort": "Omsk", "lat": 54.98, "lon": 73.37, "text": "Einschulung und Kindheit in Sibirien."},
    2006: {"titel": "Emigration", "ort": "Neustrelitz", "lat": 53.36, "lon": 13.06, "text": "Neustart in Deutschland. Ein großer Flug in ein neues Leben."},
    2022: {"titel": "Hausbau", "ort": "Deutschland", "lat": 52.52, "lon": 13.40, "text": "Ein wichtiger Meilenstein in der neuen Heimat."}
}

# --- 5. VISUELLER ZEITSTRAHL (HORIZONTALE NAVIGATION) ---
st.markdown("<h3 style='text-align: center;'>Meine Reise</h3>", unsafe_allow_html=True)

# Spalten für die Jahre (proportional oder gleichmäßig)
zeit_cols = st.columns(len(STATIONEN))
jahre = sorted(STATIONEN.keys())

for i, jahr in enumerate(jahre):
    with zeit_cols[i]:
        # Button-Farbe hervorheben, wenn ausgewählt
        label = f"📍 {jahr}" if jahr == st.session_state.selected_year else str(jahr)
        if st.button(label, use_container_width=True, key=f"btn_{jahr}"):
            st.session_state.selected_year = jahr
            st.rerun()

# --- 6. INTERAKTIVE KARTE & DETAILS ---
st.divider()
c1, c2 = st.columns([1, 2])

aktuelle_station = STATIONEN[st.session_state.selected_year]

with c1:
    st.markdown(f"### {aktuelle_station['titel']}")
    st.markdown(f"**Ort:** {aktuelle_station['ort']}")
    st.write(aktuelle_station)
    
    # Dynamischer Bild-Platzhalter für die jeweilige Station
    bild_name = f"station_{st.session_state.selected_year}.jpg"
    station_bild = lade_formatiertes_bild(bild_name, target_size=(400, 300))
    if station_bild:
        st.image(station_bild, caption=f"Eindruck aus {st.session_state.selected_year}")
    else:
        st.info(f"📸 Hier kannst du später ein Foto von '{aktuelle_station['ort']}' einfügen.")

with c2:
    # Einfache Karte mit Plotly (da du es oben schon importiert hast)
    map_data = pd.DataFrame([aktuelle_station])
    fig = px.scatter_mapbox(
        map_data, 
        lat="lat", lon="lon", 
        zoom=4, 
        height=400,
        text="ort"
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)




