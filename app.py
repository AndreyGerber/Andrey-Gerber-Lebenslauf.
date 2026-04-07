
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
    # Nutze relativen Pfad oder absoluten Pfad falls nötig
    pfad = os.path.join("images", name)
    if os.path.exists(pfad):
        img = Image.open(pfad)
        # Erstellt ein Bild mit festem Format, ohne es zu verzerren
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

slideshow_bilder = ["ich1.JPG", "ich_pass.png", "aufenthaltstitel.png"]
zeichnung_name = "itsme2.png"

# --- 3. GLOBALER STYLE FÜR ZENTRIERUNG ---
st.markdown("""
    <style>
    /* Zentriert den Inhalt aller Spalten vertikal */
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    /* Link-Styling */
    .contact-link {
        text-decoration: none;
        color: #007BFF;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LAYOUT: 3 SPALTEN ---
col_bild, col_mitte, col_daten = st.columns([1.5, 1.0, 1.5])

with col_bild:
    # Foto laden
    aktuelles_foto = lade_formatiertes_bild(slideshow_bilder[st.session_state.bild_index])
    if aktuelles_foto:
        st.image(aktuelles_foto, use_container_width=True)
    else:
        st.error(f"Datei fehlt: {slideshow_bilder[st.session_state.bild_index]}")

    # Navigation unter dem Bild
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
    # Zeichnung/Pfeil laden
    zeichnung = lade_formatiertes_bild(zeichnung_name, target_size=(300, 300))
    if zeichnung:
        st.image(zeichnung, use_container_width=True)
    else:
        st.info("Hier erscheint deine Zeichnung...")

with col_daten:
    # Header
    st.markdown("<p style='font-size: 30px; color: gray; margin-bottom: -10px;'>Meine Kontaktdaten</p>", unsafe_allow_html=True)
    
    # Name: Groß und Fett
    st.markdown("<h1 style='font-size: 42px; font-weight: bold; margin-top: 0px;'>Andrey Gerber</h1>", unsafe_allow_html=True)
    
    # Kontaktdaten mit Icons
    st.markdown(f"""
        <div style='line-height: 1.8;'>
            <p style='font-size: 24px;'>
                <span style='margin-right: 15px;'>📞</span> 
                <strong>0176 43 733 099</strong>
            </p>
            <p style='font-size: 24px;'>
                <span style='margin-right: 15px;'>📧</span> 
                <a href='mailto:andrey.gerber.88@gmail.com' class='contact-link'>
                    andrey.gerber.88@gmail.com
                </a>
            </p>
            <p style='font-size: 24px; color: #666; margin-top: 20px;'>
                📍 <i>Wohnadresse: Brauchst du nicht, ruf an oder @</i>
            </p>
            </p></p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ... hier geht es weiter mit deinem "Mein Weg" (Flaggen) und der Timeline







import streamlit as st
import plotly.graph_objects as go

# --- 1. DATENKONFIGURATION ---
# Alle Jahre für die Beschriftung
jahre_alle = [1988, 1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]
# Jahre, die eine Raute auf der Linie erhalten (alle außer 1988)
jahre_mit_raute = [1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]

GROESSE_JAHRE = 19       # Schriftgröße der Jahreszahlen (fett)
GROESSE_TEXTE = 17       # Schriftgröße der Beschreibungen

# Hier kannst du deine Texte für die Blöcke definieren
texte = {
    1988: "Born in UdSSR ☭",
    1991: "Moved to Russian Federation<br>without moving 🇷🇺",
    1996: "School (not cool)",
    2006: "Emigration to GE 🇩🇪",
    2010: "Studying aircraft design<br>(B.Eng. & Ms.Sc.)",
    2017: "TÜV Rheinland<br>(Expert in the lab  &                    ",
    2019: "                  Quality Expert)",
    2022: "Ferchau (at Siemens)<br>(Quality Systems Engineering)",
    2026: "Liora<br>(Data Science & ML)"
}

# Design-Einstellungen
LINIEN_DICKE = 3
STARTSTRICH_LAENGE = 0.18
JAHR_SCHRIFTGROESSE = 16

# Titel linksbündig
st.markdown("<h2 style='text-align: left;'>Mein Werdegang</h2>", unsafe_allow_html=True)

# --- 2. GRAFIK ERSTELLEN ---
fig = go.Figure()

# Lebenslinie: Durchgehend von 1988 bis kurz vor die Pfeilspitze (2034)
fig.add_trace(go.Scatter(
    x=[1988, 2029], 
    y=[0, 0],
    mode='lines',
    line=dict(color='black', width=LINIEN_DICKE),
    showlegend=False, 
    hoverinfo='none'
))

# Senkrechter Startstrich bei 1988
fig.add_shape(
    type="line", 
    x0=1988, y0=-STARTSTRICH_LAENGE, 
    x1=1988, y1=STARTSTRICH_LAENGE,
    line=dict(color="black", width=LINIEN_DICKE + 1)
)

# Weiße Rauten (NUR ab 1996), mittig auf der Linie
fig.add_trace(go.Scatter(
    x=jahre_mit_raute, 
    y=[0] * len(jahre_mit_raute),
    mode='markers',
    marker=dict(
        symbol='diamond', 
        size=16, 
        color='white', 
        line=dict(color='black', width=2)
    ),
    showlegend=False, 
    hoverinfo='none'
))

# Jahreszahlen und Textblöcke (45° gedreht)
for i, jahr in enumerate(jahre_alle):
    # Logik: Nur die Jahre 1991, 2010, 2019 und 2026 werden tiefer gesetzt
    # Das schafft Platz für die langen Texte der Nachbarn.
    if jahr in [1991, 2017, 2019, 2022]:
        y_offset = -0.05  # Deutlich tiefer für maximale Freiheit
    else:
        y_offset = -0.20  # Standardhöhe
    
    # 1. Das Jahr
    fig.add_annotation(
        x=jahr, y=-0.1, 
        text=f"<b>{jahr}</b>",
        showarrow=False, 
        textangle=-30,
        font=dict(size=GROESSE_JAHRE, color="black"),
        xanchor="center", 
        yanchor="top"
    )
    
    # 2. Der Textblock (mit gezieltem Versatz)
    fig.add_annotation(
        x=jahr, y=y_offset, 
        text=texte.get(jahr, ""),
        showarrow=False, 
        textangle=-30,
        font=dict(size=GROESSE_TEXTE, color="#4B0082"),
        xanchor="center", 
        yanchor="top"
    )

# WICHTIG: Das Layout braucht mehr Platz nach unten für den tiefen Text (-0.75)
fig.update_layout(
    height=500,
    margin=dict(l=50, r=50, t=20, b=250), 
    yaxis=dict(range=[-1.8, 0.5]) 
)


# Pfeilspitze am rechten Ende
fig.add_annotation(
    x=2030, y=0,           # Spitze
    ax=2028, ay=0,         # Ende der Linie
    xref="x", yref="y", 
    axref="x", ayref="y",
    showarrow=True, 
    arrowhead=2, 
    arrowsize=1.5, 
    arrowwidth=LINIEN_DICKE, 
    arrowcolor="black"
)

# Layout-Anpassung für die schrägen Texte
fig.update_layout(
    height=450, 
    margin=dict(l=0, r=0, t=10, b=150),
    xaxis=dict(
        showgrid=False, 
        zeroline=False, 
        showticklabels=False, 
        range=[1985, 2035] # Genug Platz links und rechts
    ),
    yaxis=dict(
        showgrid=False, 
        zeroline=False, 
        showticklabels=False, 
        range=[-1.8, 0.6] # Platz für die schrägen Texte nach unten
    ),
    plot_bgcolor="rgba(0,0,0,0)", 
    paper_bgcolor="rgba(0,0,0,0)"
)

# Anzeige in Streamlit
st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True, 'displayModeBar': False})










import pydeck as pdk
#Oben ist der Abschnitt mit "meinem Werdegang" und dem Pfeil. Unten die "Erklärung dazu"


BLOCK_HOEHE = 750
BILD_BREITE = 350
INFO_FONT_SIZE = "24px" # Etwas größer, da der Block jetzt massiver ist

# 1. Navigation (absolut unabhängig)
highlights = [1988, 1996, 2006, 2010, 2017, 2022]
if 'info_idx' not in st.session_state:
    st.session_state.info_idx = 0

# Buttons oben
c_nav1, c_nav2, c_nav3 = st.columns([1, 4, 1])
with c_nav1:
    if st.button("⬅️", key="nav_prev", disabled=(st.session_state.info_idx == 0)):
        st.session_state.info_idx -= 1
        st.rerun()
with c_nav3:
    if st.button("➡️", key="nav_next", disabled=(st.session_state.info_idx == len(highlights) - 1)):
        st.session_state.info_idx += 1
        st.rerun()

# 2. Der 750px Block
with st.container(height=BLOCK_HOEHE, border=True):
    jahr_aktiv = highlights[st.session_state.info_idx]

    if jahr_aktiv == 1988:
            st.subheader(f"📍 {jahr_aktiv}: Hier begann meine Reise")

            # --- DEIN PARAMETER ---
            MASSSTAB_MAP = 0.8  # Ändere NUR diesen Wert (z.B. 0.5 für 50%)
            # ----------------------------

            import base64
            def get_base64(path):
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()

            try:
                img_b64 = get_base64("images/tscherlak_map.png")
                
                # WICHTIG: Die Prozentwerte für top/left müssen die ORIGINAL-Werte bleiben, 
                # die bei 100% Größe funktioniert haben.
                st.markdown(f"""
                    <div style="width: {int(MASSSTAB_MAP * 100)}%; margin: auto;">
                        <div style="position: relative; display: inline-block; width: 100%;">
                            <img src="data:image/png;base64,{img_b64}" style="width: 100%; display: block; border-radius: 10px;">
                            <div style="
                                position: absolute;
                                top: 45.3%;
                                left: 89.8%;
                                transform: translate(-50%, -100%);
                                font-size: 40px;
                                filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.5));
                                z-index: 999;
                            ">📍</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Fehler: {e}")

  



    # --- INNERHALB DEINES 750px CONTAINERS ---
    elif jahr_aktiv == 1996:
        # --- DEINE PARAMETER ---
        MASSSTAB = 1.0  # 1.0 = 100%. Verringere dies, falls der Scrollbalken erscheint.
        OBEN_ABSTAND = "200px" # Schiebt den Inhalt in die Mitte der 750px Höhe

        # Zwei Spalten (Text links, Bild rechts)
        col_text, col_foto = st.columns([1, 2.5])

        with col_text:
            # Vertikaler Abstand für den Text
            st.markdown(f"<div style='margin-top: {OBEN_ABSTAND};'></div>", unsafe_allow_html=True)
            st.subheader(f"🎒 {jahr_aktiv}: Schulzeit")
            st.markdown(f"<p style='font-size: {INFO_FONT_SIZE}; color: #4B0082;'>So schnell vergehen 10 Jahre.</p>", unsafe_allow_html=True)

        with col_foto:
            img_schule = lade_formatiertes_bild("schule2.png")
            if img_schule:
                # FIX: Wir nehmen nur den ersten Wert (Index 0) des Tupels
                original_breite = img_schule.size[0] 
                neue_breite = int(original_breite * MASSSTAB)
                
                # Vertikaler Abstand für das Bild (etwas weniger als beim Text für optische Mitte)
                st.markdown(f"<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
                st.image(img_schule, width=neue_breite)
            else:
                st.error("Bild 'schule2.png' nicht gefunden.")

    elif jahr_aktiv == 2006:
        st.subheader("✈️ 2006: Der neue Lebensabschnitt beginnt")
        st.divider()

        fig_flight = go.Figure()

        # 1. ORTE (Omsk & Berlin) - Texte UNTER den Punkten
        fig_flight.add_trace(go.Scattergeo(
            lon = [73.32, 13.40],
            lat = [54.98, 52.52],
            mode = 'markers+text',
            text = ["Omsk", "Berlin"],
            textposition = "bottom center",
            textfont = dict(size=16, color="black", family="Arial Black"),
            marker = dict(size=14, color='#FF4B4B', line=dict(width=2, color='white')),
            hoverinfo = 'none'
        ))

        # 2. FLUGROUTE (Die rote Linie)
        fig_flight.add_trace(go.Scattergeo(
            lon = [73.32, 13.40],
            lat = [54.98, 52.52],
            mode = 'lines',
            line = dict(width=3, color='#FF4B4B'),
            hoverinfo = 'none'
        ))

        # 3. DAS LANDENDE FLUGZEUG (An das Ende der Linie geschoben)
        # x=14.5 setzt es fast direkt auf den Punkt Berlin (13.4)
        fig_flight.add_annotation(
            x=14.8, y=52.7, 
            text="✈️",
            showarrow=False,
            font=dict(size=50), # Etwas größer für bessere Sichtbarkeit
            textangle=-140,     # Nase zeigt steil nach links unten auf Berlin
            xref="x", yref="y"
        )

        # 4. LAYOUT
        fig_flight.update_layout(
            height=550,
            margin=dict(l=0, r=0, t=10, b=0),
            geo = dict(
                projection_type = 'equirectangular',
                showland = True, landcolor = "#F0F2F6",
                showocean = True, oceancolor = "#E8F4F9",
                showcountries = True, countrycolor = "white",
                # Fokus-Bereich angepasst, damit Berlin links genug Platz hat
                lataxis = dict(range=[45, 65], showgrid=False),
                lonaxis = dict(range=[5, 85], showgrid=False),
                resolution = 50
            ),
            showlegend = False
        )

        st.plotly_chart(fig_flight, use_container_width=True, key="flight_landing_final_fix")


    elif jahr_aktiv == 2010:
            # --- DEINE PARAMETER FÜR DIESEN ABSCHNITT ---
            MASSSTAB_STUDIUM = 1.0 # 1.0 = 100%, 0.8 = 80% der Originalgröße
            OBEN_ABSTAND = "50px"  # Vertikale Zentrierung für den Text

            col_text, col_foto = st.columns([1, 2.5])

            with col_text:
                st.markdown(f"<div style='margin-top: {OBEN_ABSTAND};'></div>", unsafe_allow_html=True)
                st.subheader(f"🎓 {jahr_aktiv}: Studium")
                
                # Hier ist dein Text, schick formatiert
                st.markdown(f"""
                    <p style='font-size: {INFO_FONT_SIZE}; color: #1E90FF; line-height: 1.4;'>
                    <strong>Bachelor of Engineering</strong><br>
                    & <strong>Master of Science</strong>.<br><br>
                    <i>"Pass auf, Wissenschaft – ich komme!"</i>
                    </p>
                    """, unsafe_allow_html=True)

            with col_foto:
                img_haw = lade_formatiertes_bild("haw.png")
                if img_haw:
                    # Berechne die neue Breite basierend auf dem Maßstab
                    original_breite = img_haw.size[0]
                    neue_breite = int(original_breite * MASSSTAB_STUDIUM)
                    
                    # Zentriert das Bild etwas im hohen Block
                    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
                    st.image(img_haw, width=neue_breite)
                else:
                    st.error("Bild 'haw.png' konnte nicht geladen werden.")

    elif jahr_aktiv == 2017:
        # --- PARAMETER ---
        MASSSTAB_TUV = 1.15
        OBEN_ABSTAND_TEXT = "10px" 

        col_text, col_foto = st.columns([1, 1.8])

        with col_text:
            st.markdown(f"<div style='margin-top: {OBEN_ABSTAND_TEXT};'></div>", unsafe_allow_html=True)
            st.subheader(f"🛠️ {jahr_aktiv} – 2022: TÜV Rheinland")
            
            # Fokus 1: Test & Measurement (2017-2019)
            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-bottom: 5px;'><strong>Test & Measurement Engineer</strong></p>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Normgerechte <b>akustische Messungen</b> (Haushaltsgeräte, Tools, Spielzeug)</li>
                    <li>Planung & Aufbau einer <b>neuen Prüfkammer</b> für Smart Speaker</li>
                    <li><b>Schwingungsmessungen & kundenspezifische Sondermessungen</b></li>
                    <li>Mitglied im <b>DIN-Normenausschuss</b> für Schalldämmung</li>
                </ul>
            """, unsafe_allow_html=True)

            # Fokus 2: Qualitätsmanagement (2019-2022)
            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-top: 20px; margin-bottom: 5px;'><strong>ab 2019 <br>Qualitätsmanager / Quality Expert</strong></p>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Durchführung <b>interner Audits</b>  (ISO 9001 & ISO 17025)</li>
                    <li>Verantwortung für <b>CAPA-Prozesse</b> und <b>Beschwerdemanagement</li>
                    <li><b>Externe Audits</b>  und <b>Management Reviews</b></li>
                    
                </ul>
            """, unsafe_allow_html=True)

        with col_foto:
            # Bild aus dem Unterordner "images" laden
            img_tuv = lade_formatiertes_bild("tuev.png") 
            if img_tuv:
                # Vertikaler Abstand, damit das Logo mittig zum Text steht
                st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                st.image(img_tuv, width=int(img_tuv.size[0] * MASSSTAB_TUV))
            else:
                st.error("Datei 'images/tuev.png' nicht gefunden.")






st.markdown('<div style="margin-top: 150px;"></div>', unsafe_allow_html=True)

# Block mit dem Hinweis auf die Namensänderung
st.write("") # Trennlinie zum vorherigen Abschnitt

# Erstellt eine dekorative Infobox
with st.container():
    st.markdown("""
        <div style="background-color: #e1f5fe; padding: 20px; border-radius: 15px; border-left: 5px solid #01579b; margin-bottom: 20px;">
            <h3 style="color: #01579b; margin-top: 0;">🗃️ Credentials & Zertifikate</h3>
            <p style="color: #333; font-size: 1.1em;">
                Hier finden Sie eine Übersicht meiner akademischen und beruflichen Nachweise. 
            </p>
            <div style="background-color: #fff9c4; padding: 10px; border-radius: 8px; border: 1px solid #fbc02d;">
                <strong>⚠️ Wichtiger Hinweis zur Namensänderung:</strong><br>
                Bitte beachten Sie, dass ich im Laufe meines Lebens meinen Namen geändert habe. 
                Einige der unten aufgeführten Dokumente (z. B. Abitur, Bachelor) sind daher auf meinen 
                früheren Namen ausgestellt. <br>Ein entsprechender Nachweis über die Namensänderung ist als 
                erstes Dokument in der Galerie hinterlegt.
            </div>
        </div>
    """, unsafe_allow_html=True)








import streamlit as st
import base64
import os

# --- 1. SETUP ---
PDF_FOLDER = "documents"

def get_pdf_base64(file_name):
    path = os.path.join(PDF_FOLDER, file_name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

if "active_doc" not in st.session_state:
    st.session_state.active_doc = "Namensaenderung.pdf"

# --- 2. DATEN ---
top_doc = {"file": "Namensaenderung.pdf", "icon": "📝", "label": "Namensänderung"}
other_docs = [
    {"file": "Berufsschule.pdf", "icon": "⚒️", "label": "Berufsschule"},
    {"file": "allgemeineHochschulreife.pdf", "icon": "📜", "label": "Abitur"},
    {"file": "Praktikum_V&F.pdf", "icon": "🔧", "label": "Praktikum V&F"},
    {"file": "Bachelor.pdf", "icon": "✈️", "label": "Bachelor Zeugnis"},
    {"file": "Schweisskurs.pdf", "icon": "👨‍🏭", "label": "Schweißkurs"},
    {"file": "Wertanalytiker.pdf", "icon": "💎", "label": "Wertanalytiker"},
    {"file": "Master.pdf", "icon": "🎓", "label": "Master Zeugnis"},
    {"file": "b_k_pulse.pdf", "icon": "📟", "label": "B&K Pulse"},
    {"file": "M_BBM.pdf", "icon": "🔊", "label": "M-BBM"},
    {"file": "InternerQualitätsauditor.pdf", "icon": "🕵️", "label": "Auditor 9000 ff."},
    {"file": "Qualitätsbeauftragter.pdf", "icon": "🛡️", "label": "QMB ISO 9001"},
    {"file": "QMB_ISO_17025.pdf", "icon": "🛡️", "label": "QMB ISO 17025"}
]

# --- 3. STYLING (ISOLIERT & REPARIERT) ---
st.markdown("""
<style>
    /* Button als Karte mit Schatten statt Rahmen */
    .pdf-section-wrapper div.stButton > button {
        height: 120px !important; /* Etwas höher für mehr Platz */
        border: 1px solid #f1f5f9 !important;
        border-radius: 16px !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Die Emojis (Icons) gezielt ansprechen */
    /* Hinweis: Wir nutzen hier eine größere Font-Size für den ersten Teil des Button-Texts */
    .pdf-section-wrapper div.stButton > button p {
        font-size: 14px !important; /* Textgröße */
        font-weight: 500 !important;
        line-height: 1.4 !important;
    }

    /* Hover-Effekt: Karte hebt sich leicht ab */
    .pdf-section-wrapper div.stButton > button:hover {
        border-color: #3b82f6 !important;
        background-color: #f8fafc !important;
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1) !important;
    }

    /* Aktiver Status (Dunkelblau) */
    .pdf-section-wrapper div.active-btn button {
        background: #1e293b !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. LAYOUT & LOGIK ---
st.markdown('<div class="pdf-section-wrapper">', unsafe_allow_html=True)

col_gallery, col_viewer = st.columns([1, 1.4])

with col_gallery:
    def render_btn(doc):
        active = st.session_state.active_doc == doc['file']
        if active: st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        
        # WICHTIG: Reines Markdown, kein HTML-Span. \n für den Umbruch.
        if st.button(f"{doc['icon']}\n\n{doc['label']}", key=f"doc_btn_{doc['file']}", use_container_width=True):
            st.session_state.active_doc = doc['file']
            st.rerun()
            
        if active: st.markdown('</div>', unsafe_allow_html=True)

    # Top Dokument (zentriert)
    t_c1, t_c2, t_c3 = st.columns(3)
    with t_c2: render_btn(top_doc)

    # Grid für Rest
    grid_cols = st.columns(3)
    for i, d in enumerate(other_docs):
        with grid_cols[i % 3]: 
            render_btn(d)

with col_viewer:
    pdf_b64 = get_pdf_base64(st.session_state.active_doc)
    if pdf_b64:
        display = f'<iframe src="data:application/pdf;base64,{pdf_b64}#toolbar=0" width="100%" height="900px" style="border:2px solid #334155; border-radius:15px;"></iframe>'
        st.markdown(display, unsafe_allow_html=True)
    else:
        st.warning(f"Dokument {st.session_state.active_doc} nicht gefunden.")

st.markdown('</div>', unsafe_allow_html=True)














# --- 2. DAS GALERIE-STYLING (Schwarze Rahmen & Passepartout) ---







# --- 1. DATEN-LISTE (Deine 17 Bilder) ---


st.write("") # Abstandshalter nach unten






st.markdown("<br>", unsafe_allow_html=True) # HTML-Umbruch für präzise Kontrolle
st.markdown("<br>", unsafe_allow_html=True) # HTML-Umbruch für präzise Kontrolle








