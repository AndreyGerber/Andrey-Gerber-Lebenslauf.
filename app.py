import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pydeck as pdk
import base64
import os
from PIL import Image, ImageOps

# ==================== KONFIGURATION ====================
IMAGES_DIR = "images"
DOCS_DIR = "documents"

# Seiteneinstellungen
st.set_page_config(
    page_title="Lebenslauf Andrey Gerber", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== HILFSFUNKTIONEN ====================
def lade_formatiertes_bild(name, target_size=(900, 600)):
    """Lädt und formatiert Bilder mit Fehlerbehandlung"""
    pfad = os.path.join(IMAGES_DIR, name)
    
    if not os.path.exists(pfad):
        return None
        
    if pfad.lower().endswith(".pdf"):
        return None

    try:
        img = Image.open(pfad)
        if img.mode != "RGB":
            img = img.convert("RGB")
            
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
        new_img.paste(img, ((target_size[0] - img.size[0]) // 2, 
                            (target_size[1] - img.size[1]) // 2))
        return new_img
        
    except Exception as e:
        st.warning(f"Bild konnte nicht geladen werden: {name}")
        return None

def get_pdf_base64(file_name):
    """Konvertiert PDF in Base64 für Embedding"""
    path = os.path.join(DOCS_DIR, file_name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

def check_required_files():
    """Prüft ob wichtige Dateien existieren"""
    required_images = ["ich1.JPG", "ich_pass.png", "aufenthaltstitel.png"]
    missing_images = [f for f in required_images if not os.path.exists(os.path.join(IMAGES_DIR, f))]
    
    if missing_images:
        st.warning(f"⚠️ Fehlende Bilder: {', '.join(missing_images)}")
        st.info("Die App funktioniert trotzdem, aber einige Bilder werden nicht angezeigt.")

# ==================== STYLING ====================
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
    
    /* PDF-Galerie Styling */
    .custom-spacer-t { height: 30px !important; display: block; }
    .custom-spacer-b { height: 80px !important; display: block; }

    .pdf-section-wrapper div.stButton > button {
        height: 120px !important;
        width: 100% !important;
        border-radius: 16px !important;
        background-color: white !important;
        transition: all 0.3s ease !important;
    }

    .pdf-section-wrapper div.stButton > button div[data-testid="stMarkdownContainer"] p,
    .pdf-section-wrapper div.stButton > button div[data-testid="stMarkdownContainer"] p span {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: pre-wrap !important;
    }

    .pdf-section-wrapper div.stButton > button p::first-line {
        font-size: 38px !important; 
        line-height: 1.5 !important;
    }

    .pdf-section-wrapper div.stButton > button p {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #475569 !important;
        line-height: 1.1 !important;
    }

    .pdf-section-wrapper div.stButton > button:hover {
        transform: translateY(-5px) !important;
        border-color: #3b82f6 !important;
    }

    .pdf-section-wrapper .active-btn div.stButton > button {
        background: #1e293b !important;
        border-color: #1e293b !important;
    }
    
    .pdf-section-wrapper .active-btn div.stButton > button p {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("<h2 style='text-align: center;'>Willkommen auf der Seite</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #4B0082;'>Lebenslauf von Andrey Gerber</h1>", unsafe_allow_html=True)
st.divider()

# ==================== BILDERSLIDESHOW & KONTAKT ====================
if 'bild_index' not in st.session_state:
    st.session_state.bild_index = 0

slideshow_bilder = ["ich1.JPG", "ich_pass.png", "aufenthaltstitel.png"]
zeichnung_name = "itsme2.png"

col_bild, col_mitte, col_daten = st.columns([1.5, 1.0, 1.5])

with col_bild:
    aktuelles_foto = lade_formatiertes_bild(slideshow_bilder[st.session_state.bild_index])
    if aktuelles_foto:
        st.image(aktuelles_foto, use_container_width=True)
    else:
        st.info("📸 Foto wird geladen...")

    p_links, p_mitte, p_rechts = st.columns([1, 4, 1]) 
    with p_links:
        if st.button("⬅️", key="prev_img"):
            st.session_state.bild_index = (st.session_state.bild_index - 1) % len(slideshow_bilder)
            st.rerun()
    with p_rechts:
        if st.button("➡️", key="next_img"):
            st.session_state.bild_index = (st.session_state.bild_index + 1) % len(slideshow_bilder)
            st.rerun()

with col_mitte:
    zeichnung = lade_formatiertes_bild(zeichnung_name, target_size=(300, 300))
    if zeichnung:
        st.image(zeichnung, use_container_width=True)
    else:
        st.info("🎨 Hier erscheint deine Zeichnung...")

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

# ==================== WERDEGANG TIMELINE ====================
st.markdown("<h2 style='text-align: left;'>Mein Werdegang</h2>", unsafe_allow_html=True)

# Daten für Timeline
jahre_alle = [1988, 1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]
jahre_mit_raute = [1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]

texte = {
    1988: "Born in UdSSR ☭",
    1991: "Moved to Russian Federation<br>without moving 🇷🇺",
    1996: "School (not cool)",
    2006: "Emigration to GE 🇩🇪",
    2010: "Studying aircraft design<br>(B.Eng. & Ms.Sc.)",
    2017: "TÜV Rheinland<br>(Expert in the lab)",
    2019: "Quality Expert",
    2022: "Ferchau (at Siemens)<br>(Quality Systems Engineering)",
    2026: "Liora<br>(Data Science & ML)"
}

fig = go.Figure()

# Lebenslinie
fig.add_trace(go.Scatter(
    x=[1988, 2029], 
    y=[0, 0],
    mode='lines',
    line=dict(color='black', width=3),
    showlegend=False, 
    hoverinfo='none'
))

# Startstrich
fig.add_shape(
    type="line", 
    x0=1988, y0=-0.18, 
    x1=1988, y1=0.18,
    line=dict(color="black", width=4)
)

# Marker (Rauten)
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

# Jahreszahlen und Texte
for jahr in jahre_alle:
    if jahr in [1991, 2017, 2019, 2022]:
        y_offset = -0.05
    else:
        y_offset = -0.20
    
    fig.add_annotation(
        x=jahr, y=-0.1, 
        text=f"<b>{jahr}</b>",
        showarrow=False, 
        textangle=-30,
        font=dict(size=19, color="black"),
        xanchor="center", 
        yanchor="top"
    )
    
    fig.add_annotation(
        x=jahr, y=y_offset, 
        text=texte.get(jahr, ""),
        showarrow=False, 
        textangle=-30,
        font=dict(size=17, color="#4B0082"),
        xanchor="center", 
        yanchor="top"
    )

# Pfeilspitze
fig.add_annotation(
    x=2030, y=0,
    ax=2028, ay=0,
    xref="x", yref="y", 
    axref="x", ayref="y",
    showarrow=True, 
    arrowhead=2, 
    arrowsize=1.5, 
    arrowwidth=3, 
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

# ==================== INTERAKTIVE BIOGRAFIE ====================
highlights = [1988, 1996, 2006, 2010, 2017, 2022]
if 'info_idx' not in st.session_state:
    st.session_state.info_idx = 0

# Navigation
c_nav1, c_nav2, c_nav3 = st.columns([1, 4, 1])
with c_nav1:
    if st.button("⬅️ Vorheriges", key="nav_prev", disabled=(st.session_state.info_idx == 0)):
        st.session_state.info_idx -= 1
        st.rerun()
with c_nav3:
    if st.button("Nächstes ➡️", key="nav_next", disabled=(st.session_state.info_idx == len(highlights) - 1)):
        st.session_state.info_idx += 1
        st.rerun()

# Detailansicht
with st.container(height=750, border=True):
    jahr_aktiv = highlights[st.session_state.info_idx]

    if jahr_aktiv == 1988:
        st.subheader(f"📍 {jahr_aktiv}: Hier begann meine Reise")
        st.markdown("""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
                <p style="font-size: 18px;">Geboren in Tscherlak, Oblast Omsk, Sowjetunion.</p>
                <p style="font-size: 16px; color: #666;">Eine kleine Stadt an der Grenze zu Kasachstan, 
                wo meine ersten Lebensjahre geprägt waren von den politischen Umbrüchen der späten 80er Jahre.</p>
            </div>
        """, unsafe_allow_html=True)

    elif jahr_aktiv == 1996:
        col_text, col_foto = st.columns([1, 2.5])
        with col_text:
            st.subheader(f"🎒 {jahr_aktiv}: Schulzeit")
            st.markdown("""
                <p style='font-size: 20px; color: #4B0082;'>
                Die Schulzeit in Russland war herausfordernd, aber prägend. 
                10 Jahre, die mich in vielen Bereichen geformt haben.
                </p>
                <ul style='font-size: 16px;'>
                    <li>Fokus auf Mathematik und Naturwissenschaften</li>
                    <li>Erste Berührung mit Technik</li>
                    <li>Grundstein für das spätere Ingenieursstudium</li>
                </ul>
            """, unsafe_allow_html=True)
        with col_foto:
            img_schule = lade_formatiertes_bild("schule2.png", target_size=(600, 400))
            if img_schule:
                st.image(img_schule, use_container_width=True)
            else:
                st.info("📷 Schulzeit-Foto folgt...")

    elif jahr_aktiv == 2006:
        st.subheader("✈️ 2006: Der neue Lebensabschnitt beginnt")
        st.markdown("Die Auswanderung nach Deutschland - ein Neuanfang in einem neuen Land.")
        
        fig_flight = go.Figure()
        
        fig_flight.add_trace(go.Scattergeo(
            lon=[73.32, 13.40],
            lat=[54.98, 52.52],
            mode='markers+text',
            text=["Omsk", "Berlin"],
            textposition="bottom center",
            textfont=dict(size=16, color="black", family="Arial Black"),
            marker=dict(size=14, color='#FF4B4B', line=dict(width=2, color='white')),
            hoverinfo='none'
        ))
        
        fig_flight.add_trace(go.Scattergeo(
            lon=[73.32, 13.40],
            lat=[54.98, 52.52],
            mode='lines',
            line=dict(width=3, color='#FF4B4B'),
            hoverinfo='none'
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
            geo=dict(
                projection_type='equirectangular',
                showland=True, landcolor="#F0F2F6",
                showocean=True, oceancolor="#E8F4F9",
                showcountries=True, countrycolor="white",
                lataxis=dict(range=[45, 65], showgrid=False),
                lonaxis=dict(range=[5, 85], showgrid=False),
                resolution=50
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig_flight, use_container_width=True)

    elif jahr_aktiv == 2010:
        col_text, col_foto = st.columns([1, 2.5])
        with col_text:
            st.subheader(f"🎓 {jahr_aktiv}: Studium")
            st.markdown("""
                <p style='font-size: 20px; color: #1E90FF; line-height: 1.4;'>
                <strong>Bachelor of Engineering</strong><br>
                & <strong>Master of Science</strong><br><br>
                <i>"Pass auf, Wissenschaft – ich komme!"</i>
                </p>
                <p style='font-size: 16px; margin-top: 20px;'>
                Studiengang: Luftfahrtsystemtechnik an der HAW Hamburg.<br>
                Spezialisierung auf Akustik und Schwingungsmessungen.
                </p>
            """, unsafe_allow_html=True)
        with col_foto:
            img_haw = lade_formatiertes_bild("haw.png", target_size=(600, 400))
            if img_haw:
                st.image(img_haw, use_container_width=True)
            else:
                st.info("🏫 Hochschul-Foto folgt...")

    elif jahr_aktiv == 2017:
        col_text, col_foto = st.columns([1, 1.8])
        with col_text:
            st.subheader(f"🛠️ {jahr_aktiv} – 2022: TÜV Rheinland")
            
            st.markdown("""
                <p style='font-size: 22px; color: #0055A5; margin-bottom: 5px;'><strong>Test & Measurement Engineer</strong></p>
                <ul style='font-size: 16px; color: #333; line-height: 1.6;'>
                    <li>Normgerechte <b>akustische Messungen</b> (Haushaltsgeräte, Tools, Spielzeug)</li>
                    <li>Planung & Aufbau einer <b>neuen Prüfkammer</b> für Smart Speaker</li>
                    <li><b>Schwingungsmessungen & kundenspezifische Sondermessungen</b></li>
                    <li>Mitglied im <b>DIN-Normenausschuss</b> für Schalldämmung</li>
                </ul>
                
                <p style='font-size: 22px; color: #0055A5; margin-top: 20px; margin-bottom: 5px;'><strong>Qualitätsmanager / Quality Expert</strong></p>
                <ul style='font-size: 16px; color: #333; line-height: 1.6;'>
                    <li>Durchführung <b>interner Audits</b> (ISO 9001 & ISO 17025)</li>
                    <li>Verantwortung für <b>CAPA-Prozesse</b> und <b>Beschwerdemanagement</b></li>
                    <li><b>Externe Audits</b> und <b>Management Reviews</b></li>
                </ul>
            """, unsafe_allow_html=True)
        with col_foto:
            img_tuv = lade_formatiertes_bild("tuev.png", target_size=(500, 500))
            if img_tuv:
                st.image(img_tuv, use_container_width=True)
            else:
                st.info("🏢 TÜV Logo folgt...")

st.markdown('<div style="margin-top: 150px;"></div>', unsafe_allow_html=True)

# ==================== CREDENTIALS INFOBOX ====================
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

# ==================== PDF GALERIE ====================
if "active_doc" not in st.session_state:
    st.session_state.active_doc = "Namensaenderung.pdf"

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

def render_pdf_btn(doc):
    """Render einen PDF-Button in der Galerie"""
    active = st.session_state.active_doc == doc['file']
    if active: 
        st.markdown('<div class="active-btn">', unsafe_allow_html=True)
    
    if st.button(f"{doc['icon']}\n{doc['label']}", key=f"btn_{doc['file']}", use_container_width=True):
        st.session_state.active_doc = doc['file']
        st.rerun()
        
    if active: 
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="pdf-section-wrapper">', unsafe_allow_html=True)
col_gallery, col_viewer = st.columns([1, 1.4])

with col_gallery:
    st.markdown('<div class="custom-spacer-t"></div>', unsafe_allow_html=True)
    
    # Top-Dokument (zentriert)
    t_c1, t_c2, t_c3 = st.columns(3)
    with t_c2: 
        render_pdf_btn(top_doc)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Andere Dokumente im Grid
    grid_cols = st.columns(3)
    for i, doc in enumerate(other_docs):
        with grid_cols[i % 3]: 
            render_pdf_btn(doc)
    
    st.markdown('<div class="custom-spacer-b"></div>', unsafe_allow_html=True)

with col_viewer:
    pdf_b64 = get_pdf_base64(st.session_state.active_doc)
    if pdf_b64:
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{pdf_b64}#toolbar=0" '
            f'width="100%" height="850px" style="border-radius:15px; border:2px solid #1e293b;"></iframe>', 
            unsafe_allow_html=True
        )
    else:
        st.warning(f"PDF nicht gefunden: {st.session_state.active_doc}")

st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.divider()
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>"
    "© 2026 Andrey Gerber - Lebenslauf erstellt mit Streamlit"
    "</p>", 
    unsafe_allow_html=True
)

# Optional: Prüfe auf fehlende Dateien beim Start
check_required_files()