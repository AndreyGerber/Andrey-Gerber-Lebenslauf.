import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pydeck as pdk
import base64
import os
from PIL import Image, ImageOps

# Seiteneinstellungen
st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# 1. Titel (zentriert und zwei Zeilen)
st.markdown("<h2 style='text-align: center;'>Willkommen auf der Seite</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #4B0082;'>Lebenslauf von Andrey Gerber</h1>", unsafe_allow_html=True)
st.divider()

# --- 1. FUNKTION FÜR STABILE BILDGRÖSSE (angepasst: skalierbar) ---
def lade_formatiertes_bild(name, target_size=(900, 600), max_width=None):
    pfad = os.path.join("images", name)
    
    if not os.path.exists(pfad):
        return None
        
    if pfad.lower().endswith(".pdf"):
        return None

    try:
        img = Image.open(pfad)
        if img.mode != "RGB":
            img = img.convert("RGB")
            
        # Wenn max_width angegeben ist, skaliere dahin
        if max_width:
            ratio = max_width / img.size[0]
            new_size = (max_width, int(img.size[1] * ratio))
            img.thumbnail(new_size, Image.Resampling.LANCZOS)
            return img
        else:
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
            new_img.paste(img, ((target_size[0] - img.size[0]) // 2, 
                                (target_size[1] - img.size[1]) // 2))
            return new_img
        
    except Exception as e:
        print(f"Fehler bei Datei {name}: {e}")
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
    zeichnung = lade_formatiertes_bild(zeichnung_name, target_size=(300, 300))
    if zeichnung:
        st.image(zeichnung, use_container_width=True)
    else:
        st.info("Hier erscheint deine Zeichnung...")

with col_daten:
    st.markdown("<p style='font-size: 30px; color: gray; margin-bottom: -10px;'>Meine Kontaktdaten</p>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='font-size: 42px; font-weight: bold; margin-top: 0px;'>Andrey Gerber</h1>", unsafe_allow_html=True)
    
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
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- MEIN WERDEGANG (ORIGINAL, unverändert) ---
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
    if jahr in [1991, 2017, 2019, 2022]:
        y_offset = -0.05
    else:
        y_offset = -0.20
    
    fig.add_annotation(
        x=jahr, y=-0.1, 
        text=f"<b>{jahr}</b>",
        showarrow=False, 
        textangle=-30,
        font=dict(size=GROESSE_JAHRE, color="black"),
        xanchor="center", 
        yanchor="top"
    )
    
    fig.add_annotation(
        x=jahr, y=y_offset, 
        text=texte.get(jahr, ""),
        showarrow=False, 
        textangle=-30,
        font=dict(size=GROESSE_TEXTE, color="#4B0082"),
        xanchor="center", 
        yanchor="top"
    )

fig.update_layout(
    height=500,
    margin=dict(l=50, r=50, t=20, b=250), 
    yaxis=dict(range=[-1.8, 0.5]) 
)

# Pfeilspitze am rechten Ende
fig.add_annotation(
    x=2030, y=0,
    ax=2028, ay=0,
    xref="x", yref="y", 
    axref="x", ayref="y",
    showarrow=True, 
    arrowhead=2, 
    arrowsize=1.5, 
    arrowwidth=LINIEN_DICKE, 
    arrowcolor="black"
)

fig.update_layout(
    height=450, 
    margin=dict(l=0, r=0, t=10, b=150),
    xaxis=dict(
        showgrid=False, 
        zeroline=False, 
        showticklabels=False, 
        range=[1985, 2035]
    ),
    yaxis=dict(
        showgrid=False, 
        zeroline=False, 
        showticklabels=False, 
        range=[-1.8, 0.6]
    ),
    plot_bgcolor="rgba(0,0,0,0)", 
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True, 'displayModeBar': False})

# --- BLOCK MIT DEN DETAILS (Karte repariert) ---
BLOCK_HOEHE = 750
BILD_BREITE = 350
INFO_FONT_SIZE = "24px"

highlights = [1988, 1996, 2006, 2010, 2017, 2022]
if 'info_idx' not in st.session_state:
    st.session_state.info_idx = 0

c_nav1, c_nav2, c_nav3 = st.columns([1, 4, 1])
with c_nav1:
    if st.button("⬅️ Back", key="nav_prev", disabled=(st.session_state.info_idx == 0)):
        st.session_state.info_idx -= 1
        st.rerun()
with c_nav3:
    if st.button("Next ➡️", key="nav_next", disabled=(st.session_state.info_idx == len(highlights) - 1)):
        st.session_state.info_idx += 1
        st.rerun()

with st.container(height=BLOCK_HOEHE, border=True):
    jahr_aktiv = highlights[st.session_state.info_idx]

    if jahr_aktiv == 1988:
        st.subheader(f"📍 {jahr_aktiv}: Hier begann meine Reise")

        MASSSTAB_MAP = 0.8
        
        def get_base64(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()

        try:
            img_b64 = get_base64("images/tscherlak_map.png")
            
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

    elif jahr_aktiv == 1996:
        MASSSTAB = 1  # 0.7 = 70% der Originalgröße, ändere diesen Wert zum Skalieren
        OBEN_ABSTAND = "200px"

        col_text, col_foto = st.columns([1, 2.5])

        with col_text:
            st.markdown(f"<div style='margin-top: {OBEN_ABSTAND};'></div>", unsafe_allow_html=True)
            st.subheader(f"🎒 {jahr_aktiv}: Schulzeit")
            st.markdown(f"<p style='font-size: {INFO_FONT_SIZE}; color: #4B0082;'>So schnell vergehen 10 Jahre.</p>", unsafe_allow_html=True)

        with col_foto:
            img_schule = lade_formatiertes_bild("schule2.png")
            if img_schule:
                st.markdown(f"<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
                
                # MASSSTAB wird hier angewendet
                original_breite = img_schule.size[0]
                neue_breite = int(original_breite * MASSSTAB)
                st.image(img_schule, width=neue_breite)
            else:
                st.error("Bild 'schule2.png' nicht gefunden.")

    elif jahr_aktiv == 2006:
        st.subheader("✈️ 2006: Der neue Lebensabschnitt beginnt")
        st.divider()

        fig_flight = go.Figure()

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

        fig_flight.add_trace(go.Scattergeo(
            lon = [73.32, 13.40],
            lat = [54.98, 52.52],
            mode = 'lines',
            line = dict(width=3, color='#FF4B4B'),
            hoverinfo = 'none'
        ))

        fig_flight.add_annotation(
            x=14.8, y=52.7, 
            text="✈️",
            showarrow=False,
            font=dict(size=50),
            textangle=-140,
            xref="x", yref="y"
        )

        fig_flight.update_layout(
            height=550,
            margin=dict(l=0, r=0, t=10, b=0),
            geo = dict(
                projection_type = 'equirectangular',
                showland = True, landcolor = "#F0F2F6",
                showocean = True, oceancolor = "#E8F4F9",
                showcountries = True, countrycolor = "white",
                lataxis = dict(range=[45, 65], showgrid=False),
                lonaxis = dict(range=[5, 85], showgrid=False),
                resolution = 50
            ),
            showlegend = False
        )

        st.plotly_chart(fig_flight, use_container_width=True, key="flight_landing_final_fix")

    elif jahr_aktiv == 2010:
        MASSSTAB_STUDIUM = 1.0  # 0.8 = 80% der Originalgröße, ändere diesen Wert zum Skalieren
        OBEN_ABSTAND = "50px"

        col_text, col_foto = st.columns([1, 2.5])

        with col_text:
            st.markdown(f"<div style='margin-top: {OBEN_ABSTAND};'></div>", unsafe_allow_html=True)
            st.subheader(f"🎓 {jahr_aktiv}: Studium")
            
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
                st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
                
                # MASSSTAB_STUDIUM wird hier angewendet
                original_breite = img_haw.size[0]
                neue_breite = int(original_breite * MASSSTAB_STUDIUM)
                st.image(img_haw, width=neue_breite)
            else:
                st.error("Bild 'haw.png' konnte nicht geladen werden.")

    elif jahr_aktiv == 2017:
        MASSSTAB_TUV = 1.15  # 1.15 = 115% der Originalgröße, ändere diesen Wert zum Skalieren
        OBEN_ABSTAND_TEXT = "10px" 

        col_text, col_foto = st.columns([1, 1.8])

        with col_text:
            st.markdown(f"<div style='margin-top: {OBEN_ABSTAND_TEXT};'></div>", unsafe_allow_html=True)
            st.subheader(f"🛠️ {jahr_aktiv} – 2022: TÜV Rheinland")
            
            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-bottom: 5px;'><strong>Test & Measurement Engineer</strong></p>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Normgerechte <b>akustische Messungen</b> (Haushaltsgeräte, Tools, Spielzeug)</li>
                    <li>Planung & Aufbau einer <b>neuen Prüfkammer</b> für Smart Speaker</li>
                    <li><b>Schwingungsmessungen & kundenspezifische Sondermessungen</b></li>
                    <li>Mitglied im <b>DIN-Normenausschuss</b> für Schalldämmung</li>
                </ul>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-top: 20px; margin-bottom: 5px;'><strong>ab 2019 <br>Qualitätsmanager / Quality Expert</strong></p>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Durchführung <b>interner Audits</b>  (ISO 9001 & ISO 17025)</li>
                    <li>Verantwortung für <b>CAPA-Prozesse</b> und <b>Beschwerdemanagement</li>
                    <li><b>Externe Audits</b>  und <b>Management Reviews</b></li>
                    
                </ul>
            """, unsafe_allow_html=True)

        with col_foto:
            img_tuv = lade_formatiertes_bild("tuev.png")
            if img_tuv:
                st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                
                # MASSSTAB_TUV wird hier angewendet
                original_breite = img_tuv.size[0]
                neue_breite = int(original_breite * MASSSTAB_TUV)
                st.image(img_tuv, width=neue_breite)
            else:
                st.error("Datei 'images/tuev.png' nicht gefunden.")

st.markdown('<div style="margin-top: 150px;"></div>', unsafe_allow_html=True)

st.write("")









#ab hier beginnt dre Abschnitt mit Zeugnissen


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

# --- PDF GALERIE mit st.button (funktioniert garantiert) ---
if "active_doc" not in st.session_state:
    st.session_state.active_doc = "Namensaenderung.pdf"

def get_pdf_base64(file_name):
    path = os.path.join("documents", file_name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

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

# Globales CSS für ALLE Buttons (akzeptiere bitte)
st.markdown("""
<style>
    /* Alle Buttons in der App */
    .stButton > button {
        height: 70px !important;
        width: 100% !important;
        border-radius: 16px !important;
        background-color: #f1f5f9 !important;
        border: 2px solid #94a3b8 !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
        padding: 10px !important;
        gap: 8px !important;
    }
    
    /* Der Text im Button */
    .stButton > button p {
        margin: 0 !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #475569 !important;
        line-height: 1.3 !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    /* Icon (erste Zeile) */
    .stButton > button p::first-line {
        font-size: 25px !important;
        line-height: 1.5 !important;
    }
    
    /* Hover Effekt */
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        border-color: #94a3b8 !important;
        background-color: #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)

col_gallery, col_viewer = st.columns([1, 1.4])

with col_gallery:
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Top-Dokument zentriert
    t_c1, t_c2, t_c3 = st.columns(3)
    with t_c2:
        doc = top_doc
        is_active = st.session_state.active_doc == doc['file']
        
        if st.button(f"{doc['icon']}\n{doc['label']}", key=f"btn_{doc['file']}", use_container_width=True):
            st.session_state.active_doc = doc['file']
            st.rerun()
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Andere Dokumente im 3er-Grid
    grid_cols = st.columns(3)
    for i, doc in enumerate(other_docs):
        with grid_cols[i % 3]:
            if st.button(f"{doc['icon']}\n{doc['label']}", key=f"btn_{doc['file']}", use_container_width=True):
                st.session_state.active_doc = doc['file']
                st.rerun()
    
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

with col_viewer:
    pdf_b64 = get_pdf_base64(st.session_state.active_doc)
    if pdf_b64:
        st.markdown(f'''
            <iframe 
                src="data:application/pdf;base64,{pdf_b64}#toolbar=0" 
                width="100%" 
                height="850px" 
                style="border-radius:15px; border:1px solid #e2e8f0;">
            </iframe>
        ''', unsafe_allow_html=True)


st.write("")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)











# ==================== FLIEßENDE 3D-WAND MIT THREE.JS ====================
st.markdown("<h2 style='text-align: center; margin-top: 50px;'>📜 Meine Zertifikate & Nachweise</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; margin-bottom: 30px;'>✧ Fließende 3D-Wand – Maus ziehen zum Drehen, Klick auf Zertifikat zum Vergrößern ✧</p>", unsafe_allow_html=True)

# Deine 17 Zertifikatsnamen mit Nummerierung
cert_names = [
    "1_Python_for_Data_Science",
    "2_Exploratory_Statistics_with_Python",
    "3_Data_Quality",
    "4_Data_Visualization_Matplotlib",
    "5_Data_Visualization_with_Seaborn",
    "6_Matplotlib_Complements",
    "7_DataViz_with_Plotly",
    "8_MCQ_Linux_and_Bash",
    "9_Git_and_Github",
    "10_Unit_Testing",
    "11_Classification_with_scikit-learn",
    "12_Regressionn_with_scikit_learn",
    "13_Methodology_in_Data_Science",
    "14_Feature_Engineering_and_Optimisation",
    "15_Time_Series_Analysis_with_Python",
    "16_Advanced_Classification_with-scikit-learn",
    "17_Text_Mining"
]

cert_folder = "images"

# Sammle existierende Bilder mit Base64
import base64
import json
import math

cert_data = []
for cert_name in cert_names:
    for ext in ['.png', '.jpg', '.jpeg']:
        img_path = os.path.join(cert_folder, cert_name + ext)
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            display_name = cert_name.split('_', 1)[1].replace('_', ' ')
            cert_data.append({
                "name": display_name,
                "b64": img_b64,
                "ext": ext[1:]
            })
            break

num_certs = len(cert_data)

if num_certs > 0:
    # Positionen für fließende Spirale berechnen
    positions = []
    for i in range(num_certs):
        angle = i * 0.65
        radius = 3.5
        x = math.cos(angle) * radius
        z = math.sin(angle) * radius
        y = (i - num_certs/2) * 0.35
        positions.append({"x": x, "y": y, "z": z})
    
    # Konvertiere zu JSON
    certs_json = json.dumps([{
        "name": cert_data[i]["name"],
        "b64": cert_data[i]["b64"],
        "ext": cert_data[i]["ext"],
        "x": positions[i]["x"],
        "y": positions[i]["y"],
        "z": positions[i]["z"]
    } for i in range(num_certs)])
    
    # Three.js HTML/CSS/JS
    threejs_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            #info {{
                position: absolute;
                top: 20px;
                left: 20px;
                color: white;
                background: rgba(0,0,0,0.6);
                padding: 8px 15px;
                border-radius: 8px;
                pointer-events: none;
                z-index: 10;
                font-size: 14px;
            }}
            #modal {{
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.9);
                justify-content: center;
                align-items: center;
            }}
            #modal img {{
                max-width: 90%;
                max-height: 90%;
                border-radius: 10px;
                box-shadow: 0 0 30px rgba(0,0,0,0.5);
            }}
            #modal .close {{
                position: absolute;
                top: 20px;
                right: 40px;
                color: white;
                font-size: 50px;
                font-weight: bold;
                cursor: pointer;
            }}
            #modal .close:hover {{ color: #69c0ff; }}
        </style>
    </head>
    <body>
        <div id="info">
            🌀 Fließende 3D-Wand | 🖱️ Maus ziehen = drehen | Rechtsklick ziehen = schwenken | Scrollen = zoomen | Klick = vergrößern
        </div>
        <div id="modal" onclick="this.style.display='none'">
            <span class="close">&times;</span>
            <img id="modalImage" src="">
        </div>
        
        <script type="importmap">
            {{
                "imports": {{
                    "three": "https://unpkg.com/three@0.128.0/build/three.module.js",
                    "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/"
                }}
            }}
        </script>
        
        <script type="module">
            import * as THREE from 'three';
            import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
            import {{ CSS2DRenderer, CSS2DObject }} from 'three/addons/renderers/CSS2DRenderer.js';
            
            const certsData = {certs_json};
            
            // Szene, Kamera, Renderer
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xf8fafc);
            
            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(5, 3, 8);
            camera.lookAt(0, 0, 0);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            document.body.appendChild(renderer.domElement);
            
            // CSS2DRenderer für Text
            const labelRenderer = new CSS2DRenderer();
            labelRenderer.setSize(window.innerWidth, window.innerHeight);
            labelRenderer.domElement.style.position = 'absolute';
            labelRenderer.domElement.style.top = '0px';
            labelRenderer.domElement.style.left = '0px';
            labelRenderer.domElement.style.pointerEvents = 'none';
            document.body.appendChild(labelRenderer.domElement);
            
            // Orbit Controls
            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.rotateSpeed = 1.0;
            controls.zoomSpeed = 1.2;
            controls.panSpeed = 0.8;
            controls.enableZoom = true;
            controls.enablePan = true;
            
            // Licht
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(5, 10, 7);
            directionalLight.castShadow = true;
            scene.add(directionalLight);
            const backLight = new THREE.DirectionalLight(0xffffff, 0.3);
            backLight.position.set(-3, 2, -4);
            scene.add(backLight);
            
            // Hilfslinien (dezent)
            const gridHelper = new THREE.GridHelper(12, 20, 0xcccccc, 0xe0e0e0);
            gridHelper.position.y = -1.8;
            scene.add(gridHelper);
            
            // Zertifikate erstellen
            const certificates = [];
            
            certsData.forEach((cert, idx) => {{
                const img = new Image();
                img.src = `data:image/${{cert.ext}};base64,${{cert.b64}}`;
                
                img.onload = () => {{
                    const texture = new THREE.CanvasTexture(img);
                    
                    const material = new THREE.MeshStandardMaterial({{
                        map: texture,
                        side: THREE.DoubleSide,
                        roughness: 0.3,
                        metalness: 0.1
                    }});
                    
                    const aspect = img.width / img.height;
                    const width = 1.4;
                    const height = width / aspect;
                    const geometry = new THREE.PlaneGeometry(width, height);
                    const plane = new THREE.Mesh(geometry, material);
                    plane.position.set(cert.x, cert.y, cert.z);
                    plane.userData = {{ imageSrc: `data:image/${{cert.ext}};base64,${{cert.b64}}`, name: cert.name }};
                    plane.castShadow = true;
                    scene.add(plane);
                    
                    // Rahmen
                    const borderGeometry = new THREE.BoxGeometry(width + 0.06, height + 0.06, 0.03);
                    const borderMaterial = new THREE.MeshStandardMaterial({{ color: 0xffffff, metalness: 0.1, roughness: 0.3 }});
                    const border = new THREE.Mesh(borderGeometry, borderMaterial);
                    border.position.set(cert.x, cert.y, cert.z - 0.02);
                    scene.add(border);
                    
                    // Text unter dem Bild
                    const div = document.createElement('div');
                    div.textContent = cert.name;
                    div.style.color = '#475569';
                    div.style.fontSize = '11px';
                    div.style.fontWeight = '600';
                    div.style.textAlign = 'center';
                    div.style.backgroundColor = 'rgba(255,255,255,0.85)';
                    div.style.padding = '3px 8px';
                    div.style.borderRadius = '20px';
                    div.style.border = '1px solid #e2e8f0';
                    div.style.pointerEvents = 'none';
                    
                    const label = new CSS2DObject(div);
                    label.position.set(cert.x, cert.y - height/2 - 0.12, cert.z);
                    scene.add(label);
                    
                    certificates.push(plane);
                }};
            }});
            
            // Raycaster für Klick
            const raycaster = new THREE.Raycaster();
            const mouse = new THREE.Vector2();
            
            function onMouseClick(event) {{
                mouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1;
                mouse.y = -(event.clientY / renderer.domElement.clientHeight) * 2 + 1;
                
                raycaster.setFromCamera(mouse, camera);
                const intersects = raycaster.intersectObjects(certificates);
                
                if (intersects.length > 0) {{
                    const selected = intersects[0].object;
                    const modal = document.getElementById('modal');
                    const modalImg = document.getElementById('modalImage');
                    modal.style.display = 'flex';
                    modalImg.src = selected.userData.imageSrc;
                }}
            }}
            
            window.addEventListener('click', onMouseClick, false);
            
            // Animation
            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
                labelRenderer.render(scene, camera);
            }}
            animate();
            
            // Fenster-Größe anpassen
            window.addEventListener('resize', onWindowResize, false);
            function onWindowResize() {{
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
                labelRenderer.setSize(window.innerWidth, window.innerHeight);
            }}
        </script>
    </body>
    </html>
    """
    
    # HTML in Streamlit einbetten
    st.components.v1.html(threejs_html, height=700, width=None)
    
else:
    st.warning(f"⚠️ Keine Zertifikats-Bilder gefunden. Lege PNG/JPG Dateien in den Ordner 'images/' mit folgenden Namen:\n\n" + 
               "\n".join([f"• {name}.png" for name in cert_names]))
    





st.markdown("<br>" * 3, unsafe_allow_html=True)  # Drei Umbrüche














import streamlit as st
import os
from PIL import Image

def load_scaled_img(path, degrees=0, scale=0.4):
    if os.path.exists(path):
        img = Image.open(path)
        if degrees != 0:
            img = img.rotate(degrees, expand=True)
        new_size = (int(img.width * scale), int(img.height * scale))
        return img.resize(new_size, Image.Resampling.LANCZOS)
    return None

# --- CONTAINER FÜR FERTIGKEITEN (UM DAS CSS ZU ISOLIEREN) ---
with st.container():
    # Wir vergeben eine eindeutige CSS-Klasse nur für diesen Bereich
    st.markdown("""
        <style>
            /* Nur Bilder innerhalb von Containern mit dieser Struktur erhalten den Schatten */
            .skill-section img {
                border-radius: 12px !important;
                box-shadow: 3px 3px 12px rgba(0,0,0,0.2) !important;
                margin-bottom: 10px !important;
            }
        </style>
        <div class="skill-section">
    """, unsafe_allow_html=True)

    st.title("🛠️ Meine Fertigkeiten")
    st.divider()

    header_col1, header_col2 = st.columns(2)
    with header_col1:
        st.subheader("Von der Skizze bis zum fertigen Produkt")
    with header_col2:
        st.subheader("Von der Idee bis zur Übergabe...")

    content_col1, content_col2 = st.columns(2)

    with content_col1:
        kerze_files = [
            "images/kerze0.png", "images/kerze1.png", "images/kerze2.png", 
            "images/kerze3.png", "images/kerze4.jpg", "images/kerze5.jpg", "images/kerze6.jpg"
        ]
        k_cols = st.columns(3) 
        for idx, img_path in enumerate(kerze_files):
            img = load_scaled_img(img_path, scale=0.35)
            if img:
                k_cols[idx % 3].image(img)

    with content_col2:
        project_configs = [
            ("images/project1.jpg", 0), ("images/project2.jpeg", 0),
            ("images/project3.jpeg", 90), ("images/project4.jpeg", 90),
            ("images/project5.jpg", 0), ("images/project6.jpeg", -90)
        ]
        p_cols = st.columns(2)
        for idx, (img_path, angle) in enumerate(project_configs):
            img = load_scaled_img(img_path, angle, scale=0.42)
            if img:
                p_cols[idx % 2].image(img)

    st.markdown("</div>", unsafe_allow_html=True) # Ende der skill-section

st.divider()

# --- QM & METHODIK (Bleibt Standard-Streamlit ohne spezielles CSS) ---
st.subheader("📉 Expertise & Methodik")
info_col1, info_col2 = st.columns(2)
with info_col1:
    st.info("**Qualitätsmanagement & Audits**\n\nISO 9001/17025 | CAPA-Coaching")
with info_col2:
    st.info("**Lean Management & Datenanalyse**\n\nSix Sigma | Prozessoptimierung")

st.success("🐍 **Programmierkenntnisse:** Diese Seite wurde mit Python und Leidenschaft gebaut.")
