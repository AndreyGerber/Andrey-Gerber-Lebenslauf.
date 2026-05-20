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
st.markdown("<h2 style='text-align: center;'>Добро пожаловать на сайт</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #4B0082;'>Резюме Андрея Гербер</h1>", unsafe_allow_html=True)
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
                📍 <i>Адрес проживания: просто позвоните или напишите на @</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- ABSCHNITT SPRACHKENNTNISSE ---
    st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)
    #st.markdown("<p style='font-size: 28px; font-weight: bold; margin-bottom: 15px;'>Sprachkenntnisse</p>", unsafe_allow_html=True)
    
    # Darstellung in zwei kleinen Unterspalten für kompakte Optik
    lang_1, lang_2 = st.columns(2)
    
    st.markdown("""
        <p style='font-size: 22px;'>
            🇩🇪 <span style='color: gray; font-size: 18px;'>(C2)</span> 
            <span style='margin-right: 40px;'></span> 
            🇷🇺 <span style='color: gray; font-size: 18px;'>(C2)</span> 
            <span style='margin-right: 40px;'></span> 
            🇺🇸 <span style='color: gray; font-size: 18px;'>(B2)</span>
        </p>
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
    1988: "Родился в СССР ☭",
    1991: "Переехал в Российскую Федерацию,<br>не выходя из дома 🇷🇺",
    1996: "Школа (так себе удовольствие)",
    2006: "Эмиграция в Германию 🇩🇪",
    2010: "Учёба на авиаконструктора<br>(B.Eng. & M.Sc.)",
    2017: "TÜV Rheinland<br>(Эксперт в лаборатории &                    ",
    2019: "                  Эксперт по качеству)",
    2022: "Ferchau (в Siemens)<br>(Quality Systems Engineering)",
    2026: "Liora<br>(Data Science & ML)"
}

# Design-Einstellungen
LINIEN_DICKE = 3
STARTSTRICH_LAENGE = 0.18
JAHR_SCHRIFTGROESSE = 16

# Titel linksbündig
st.markdown("<h2 style='text-align: left;'>Мой путь</h2>", unsafe_allow_html=True)

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






# --- BLOCK MIT DEN DETAILS zum Werdegang ---
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
        st.markdown(f"<h3 style='text-align: left;'>📍 {jahr_aktiv}: Здесь начался мой путь</h3>", unsafe_allow_html=True)

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
        MASSSTAB = 1.2  # 0.7 = 70% der Originalgröße, ändere diesen Wert zum Skalieren
        OBEN_ABSTAND = "10px"

        col_text, col_foto = st.columns([1, 2.5])

        with col_text:
            st.markdown(f"<div style='margin-top: {OBEN_ABSTAND};'></div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: left;'>🎒 {jahr_aktiv}: Школьные годы</h3>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: {INFO_FONT_SIZE}; color: #0055A5;'>Как быстро пролетают 10 лет...</p>", unsafe_allow_html=True)

        with col_foto:
            img_schule = lade_formatiertes_bild("schule2.png")
            if img_schule:
                st.markdown(f"<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                
                # MASSSTAB wird hier angewendet
                original_breite = img_schule.size[0]
                neue_breite = int(original_breite * MASSSTAB)
                st.image(img_schule, width=neue_breite)
            else:
                st.error("Bild 'schule2.png' nicht gefunden.")

    elif jahr_aktiv == 2006:
        st.markdown(f"<h3 style='text-align: left;'>✈️ {jahr_aktiv}: начинается новая глава моей жизни</h3>", unsafe_allow_html=True)
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
        OBEN_ABSTAND = "10px"

        col_text, col_foto = st.columns([1, 2.5])

        with col_text:
            st.markdown(f"<h3 style='text-align: left;'>🎓 {jahr_aktiv}: Высшее образование</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top: {OBEN_ABSTAND};'></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)            
            st.markdown(f"""
                <p style='font-size: {INFO_FONT_SIZE}; color: #0055A5; line-height: 1.4;'>
                <strong>Bachelor of Engineering</strong><br>
                & <strong>Master of Science</strong>.<br><br><br><br>
                <i>"Держись, наука — я иду!"</i>
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
            st.markdown(f"<h3 style='text-align: left;'>🛠️ {jahr_aktiv}– 2022: TÜV Rheinland</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top: {OBEN_ABSTAND_TEXT};'></div>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-bottom: 5px;'><strong>Test & Measurement Engineer</strong></p>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Стандартизированные <b>акустические измерения</b> (бытовая техника, электроприборы, игрушки)</li>
                    <li>Проектирование и строительство <b>новой испытательной камеры</b> для умных колонок (Smart Speaker)</li>
                    <li><b>Измерение вибраций и специальные измерения</b> по техническим требованиям заказчика</li>
                    <li>Член <b>комитета по стандартизации DIN</b> в области звукоизоляции</li>
                </ul>
            """, unsafe_allow_html=True)


            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-top: 20px; margin-bottom: 5px;'><strong>с 2019 <br>Менеджер по качеству / Quality Expert</strong></p>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Проведение <b>внутренних аудитов</b> (ISO 9001 и ISO 17025)</li>
                    <li>Ответственность за <b>процессы CAPA</b> и <b>управление рекламациями</b></li>
                    <li><b>Внешние аудиты</b> и <b>Годовая отчётность</b></li>
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


    elif jahr_aktiv == 2022:
        MASSSTAB_FERCHAU = 1.15  # 1.15 = 115% der Originalgröße, ändere diesen Wert zum Skalieren
        OBEN_ABSTAND_TEXT = "10px" 

        col_text, col_foto = st.columns([1, 1.8])

        with col_text:
            st.markdown(f"<h3 style='text-align: left;'>⚙️ {jahr_aktiv} – 2025: Ferchau GmbH</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top: {OBEN_ABSTAND_TEXT};'></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)   

            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-bottom: 5px;'><strong>Инженер-технолог в Siemens Healthineers</strong></p><br>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Техническое обслуживание и ремонт существующего оборудования для <b>акустических и вибрационных измерений</b></li>
                    <li>Курирование монтажа нескольких <b>испытательных камер для акустических и вибрационных измерений</b> на новой производственной площадке</li>
                    <li><b>Разработка новых методов испытаний</b></li>
                    <li><b>Валидация и ввод в эксплуатацию</b> оборудования для серийного производства</li>
                </ul>
            """, unsafe_allow_html=True)




        with col_foto:
            img_fer = lade_formatiertes_bild("ferchau.png")
            if img_fer:
                st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                
                # MASSSTAB_TUV wird hier angewendet
                original_breite = img_fer.size[0]
                neue_breite = int(original_breite * MASSSTAB_FERCHAU)
                st.image(img_fer, width=neue_breite)
            else:
                st.error("Datei 'images/ferchau.png' nicht gefunden.")

st.markdown('<div style="margin-top: 150px;"></div>', unsafe_allow_html=True)

st.write("")









#ab hier beginnt dre Abschnitt mit Zeugnissen
st.markdown("<h2 style='text-align: left;'>Мои дипломы и сертификаты</h2>", unsafe_allow_html=True)
st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)


with st.container():
    st.markdown("""
        <div style="background-color: #e1f5fe; padding: 20px; border-radius: 15px; border-left: 5px solid #01579b; margin-bottom: 20px;">
            <!--<h3 style="color: #01579b; margin-top: 0;">🗃️ Дипломы и сертификаты</h3>--> 
            <p style="color: #333; font-size: 1.1em;">
                🗃️ Здесь вы найдете обзор моих академических и профессиональных документов. 
            </p>
            <div style="background-color: #fff9c4; padding: 10px; border-radius: 8px; border: 1px solid #fbc02d;">
                <strong>⚠️ Важное примечание о перемене имени:</strong><br>
                Пожалуйста, обратите внимание, что в течение жизни я сменил имя. 
                В связи с этим некоторые из представленных ниже документов (например, школьный аттестат, диплом бакалавра) 
                выданы на мое прежнее имя. <br>Соответствующее официальное свидетельство о смене имени 
                загружено в галерею в качестве первого документа.
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
top_doc = {"file": "Namensaenderung.pdf", "icon": "📝", "label": "Свидетельство о смене имени"}

other_docs = [
    {"file": "Berufsschule.pdf", "icon": "⚒️", "label": "Профтехучилище"},
    {"file": "allgemeineHochschulreife.pdf", "icon": "📜", "label": "Аттестат"},
    {"file": "Praktikum_V&F.pdf", "icon": "🔧", "label": "Практика в V&F"},
    {"file": "Bachelor.pdf", "icon": "✈️", "label": "Диплом бакалавра"},
    {"file": "Schweisskurs.pdf", "icon": "👨‍🏭", "label": "Сварщик"},
    {"file": "Wertanalytiker.pdf", "icon": "💎", "label": "ФСА"},
    {"file": "Master.pdf", "icon": "🎓", "label": "Диплом магистра"},
    {"file": "b_k_pulse.pdf", "icon": "📟", "label": "B&K Pulse"},
    {"file": "M_BBM.pdf", "icon": "🔊", "label": "M-BBM"},
    {"file": "Interner_Auditor.pdf", "icon": "🕵️", "label": "ISO 9000 ff."},
    {"file": "Qualitätsbeauftragter.pdf", "icon": "🛡️", "label": "Аудитор ISO 9001"},
    {"file": "QMB_ISO_17025.pdf", "icon": "🛡️", "label": "Аудитор ISO 17025"},
    {"file": "Data_Science.pdf", "icon": "🐍", "label": "Data Science"}
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
    active_pdf = st.session_state.active_doc
    
    # Pfad zum PDF (für den Download)
    pdf_path = os.path.join("documents", active_pdf)
    
    # Pfad zum JPG (für die sichere Anzeige in Edge)
    # Wir erstellen ein Dictionary für Ausnahmen, falls Dateinamen nicht exakt matchen
    mapping_exceptions = {
        # PDFs aus deiner Liste -> JPGs aus deinem Screenshot
        "Namensaenderung.pdf": "NamensaenderungAG.jpg",
        "Berufsschule.pdf": "Berufsschule.jpg",
        "allgemeineHochschulreife.pdf": "Abitur.jpg",
        "Praktikum_V&F.pdf": "Praktikum_V_F.jpg",
        "Bachelor.pdf": "Bachelor.jpg",
        "Schweisskurs.pdf": "schweißkurs.jpg",
        "Wertanalytiker.pdf": "Wertanalytiker.jpg",
        "Master.pdf": "Master.jpg",
        "b_k_pulse.pdf": "B_K_pulse.jpg",
        "M_BBM.pdf": "M_BBM.jpg",
        "Interner_Auditor.pdf": "Auditor9001.jpg",
        "Qualitätsbeauftragter.pdf": "QMB9001.jpg",
        "QMB_ISO_17025.pdf": "QMB17025.jpg",
        "Data_Science.pdf": "Data_Science.jpg"
    }
    
    # Bildpfad ermitteln: Entweder aus Ausnahme-Liste oder einfach Endung tauschen
    if active_pdf in mapping_exceptions:
        img_file = mapping_exceptions[active_pdf]
    else:
        img_file = active_pdf.replace(".pdf", ".jpg")
        
    image_path = os.path.join("images", "Zertifikate", img_file)

    # 1. DOWNLOAD BUTTON (Native Streamlit Funktion - sehr sicher)
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(
                label=f"📥 PDF öffnen: {active_pdf}",
                data=f,
                file_name=active_pdf,
                mime="application/pdf",
                use_container_width=True
            )
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 2. BILD ANZEIGE (Wird nicht von Edge blockiert)
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True, caption=f"Vorschau: {active_pdf}")
    else:
        # Falls das Bild nicht gefunden wurde, versuchen wir den alten IFrame als Fallback
        pdf_b64 = get_pdf_base64(active_pdf)
        if pdf_b64:
            st.warning("Bild-Vorschau nicht gefunden, lade PDF-Betrachter...")
            st.markdown(f'''
                <iframe src="data:application/pdf;base64,{pdf_b64}#toolbar=0" 
                        width="100%" height="800px" style="border-radius:15px; border:1px solid #e2e8f0;">
                </iframe>
            ''', unsafe_allow_html=True)

st.write("")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)











# ==================== FLIEßENDE 3D-WAND MIT THREE.JS ====================
import streamlit as st
import streamlit.components.v1 as components
import base64
import json
import math
import os

# Seite auf Wide-Mode stellen
#st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align: left; margin-top: 50px;'>💻 Data Science & Machine Learning</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; margin-top: 10px;'>3D-стена с возможностью масштабирования и вращения.</h5>", unsafe_allow_html=True)

# Deine 17 Zertifikatsnamen mit Nummerierung
cert_names = [
    "1_Python_for_Data_Science", "2_Exploratory_Statistics_with_Python", "3_Data_Quality",
    "4_Data_Visualization_Matplotlib", "5_Data_Visualization_with_Seaborn", "6_Matplotlib_Complements",
    "7_DataViz_with_Plotly", "8_MCQ_Linux_and_Bash", "9_Git_and_Github", "10_Unit_Testing",
    "11_Classification_with_scikit-learn", "12_Regressionn_with_scikit_learn", "13_Methodology_in_Data_Science",
    "14_Feature_Engineering_and_Optimisation", "15_Time_Series_Analysis_with_Python",
    "16_Advanced_Classification_with-scikit-learn", "17_Text_Mining", "18_Computer_Vision_with_OpenCV",
    "19_Dense_Neural_Networks_with_Keras", "20_Convolutional_Neural_Networks_with_Keras", "21_PyTorch",
    "22_Streamlit", "23_DATA_API_Fundamentals", "24_Docker_DS"
]

cert_folder = "images"
cert_data = []

# Sammle existierende Bilder mit Base64
if os.path.exists(cert_folder):
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
    positions = []
    for i in range(num_certs):
        angle = i * 0.65
        radius = 3.5
        x = math.cos(angle) * radius
        z = math.sin(angle) * radius
        y = (i - num_certs/2) * 0.35
        positions.append({"x": x, "y": y, "z": z})
    
    certs_json = json.dumps([{
        "name": cert_data[i]["name"],
        "b64": cert_data[i]["b64"],
        "ext": cert_data[i]["ext"],
        "x": positions[i]["x"],
        "y": positions[i]["y"],
        "z": positions[i]["z"]
    } for i in range(num_certs)])
    
    threejs_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; font-family: 'Segoe UI', sans-serif; background-color: #f8fafc; }}
            #modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); justify-content: center; align-items: center; cursor: pointer; }}
            #modal img {{ max-width: 90%; max-height: 90%; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div id="modal" onclick="this.style.display='none'"><img id="modalImage" src=""></div>
        <script type="importmap">
            {{ "imports": {{ "three": "https://unpkg.com/three@0.128.0/build/three.module.js", "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/" }} }}
        </script>
        <script type="module">
            import * as THREE from 'three';
            import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
            
            const certsData = {certs_json};
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xf8fafc);
            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(5, 3, 8);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);
            
            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            
            scene.add(new THREE.AmbientLight(0xffffff, 0.7));
            const sun = new THREE.DirectionalLight(0xffffff, 0.8);
            sun.position.set(5, 10, 7);
            scene.add(sun);

            const planes = [];
            certsData.forEach(cert => {{
                const loader = new THREE.TextureLoader();
                const texture = loader.load('data:image/' + cert.ext + ';base64,' + cert.b64);
                const material = new THREE.MeshStandardMaterial({{ map: texture, side: THREE.DoubleSide }});
                const plane = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.1), material);
                plane.position.set(cert.x, cert.y, cert.z);
                plane.userData = {{ src: 'data:image/' + cert.ext + ';base64,' + cert.b64 }};
                scene.add(plane);
                planes.push(plane);
            }});

            window.addEventListener('click', (e) => {{
                const mouse = new THREE.Vector2((e.clientX / window.innerWidth) * 2 - 1, -(e.clientY / window.innerHeight) * 2 + 1);
                const raycaster = new THREE.Raycaster();
                raycaster.setFromCamera(mouse, camera);
                const intersects = raycaster.intersectObjects(planes);
                if (intersects.length > 0) {{
                    document.getElementById('modalImage').src = intersects.object.userData.src;
                    document.getElementById('modal').style.display = 'flex';
                }}
            }});

            function animate() {{
                requestAnimationFrame(animate);
                planes.forEach(p => p.lookAt(camera.position));
                controls.update();
                renderer.render(scene, camera);
            }}
            animate();
        </script>
    </body>
    </html>
    """

    # Aufteilung in 3 Spalten (20% : 60% : 20%)
    col1, col2, col3 = st.columns([0.7, 3, 0.7])
    with col2:
        components.html(threejs_html, height=700, scrolling=False)
    
  





st.markdown("<br>" * 3, unsafe_allow_html=True)  # Drei Umbrüche









#Abschnitt mit Fertigkeiten

import streamlit as st
import os
from PIL import Image

# --- FUNKTION ZUM SKALIEREN ---
def load_scaled_img(path, degrees=0, scale_percent=40):
    if os.path.exists(path):
        img = Image.open(path)
        if degrees != 0:
            img = img.rotate(degrees, expand=True)
        scale_factor = scale_percent / 100
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        return img.resize(new_size, Image.Resampling.LANCZOS)
    return None

# --- EINSTELLUNGEN ---
BILD_SKALIERUNG = 38 

# CSS für Hintergrundfarbe in den Containern und Abstände
st.markdown("""
    <style>
        /* Erzwingt Hintergrundfarbe für die Border-Container */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #f8f9fa !important;
            padding: 10px !important;
        }
        /* Gleiche Höhe für die Überschriften erzwingen */
        .equal-height-header {
            min-height: 80px;
            display: flex;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ Мои навыки")
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

# Hauptspalten
col1, col2 = st.columns(2)

with col1:
    # Container mit Rahmen und Hintergrund (durch CSS oben gefärbt)
    with st.container(border=True):
        st.markdown('<div class="equal-height-header"><h3>От эскиза до готового продукта</h3></div>', unsafe_allow_html=True)
        
        kerze_files = [
            "images/kerze0.png", "images/kerze1.png", "images/kerze2.png", 
            "images/kerze3.png", "images/kerze4.jpg", "images/kerze5.jpg", "images/kerze6.jpg"
        ]
        k_cols = st.columns(3) 
        for idx, img_path in enumerate(kerze_files):
            img = load_scaled_img(img_path, scale_percent=BILD_SKALIERUNG)
            if img:
                k_cols[idx % 3].image(img, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown('<div class="equal-height-header"><h3>От идеи до передачи в производство</h3></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        project_configs = [
            ("images/project1.jpg", 0), ("images/project2.jpeg", 0),
            ("images/project3.jpeg", 90), ("images/project5.jpg", 0),   
            ("images/project4.jpeg", 90), ("images/project6.jpeg", -90)
        ]
        p_cols = st.columns(3)
        for idx, (img_path, angle) in enumerate(project_configs):
            img = load_scaled_img(img_path, angle, scale_percent=BILD_SKALIERUNG)
            if img:
                p_cols[idx % 3].image(img, use_container_width=True)
        
        st.markdown("<div style='margin-top: 58px;'></div>", unsafe_allow_html=True)


st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True) 

# --- Hard & Soft-Skills ---
st.markdown("""
    <style>
        .exp-box {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 25px;
            border-radius: 16px;
            border-left: 4px solid #4a90e2;
            height: 100%;
        }
        .exp-box h4 { color: #01579b; margin-top: 0; margin-bottom: 15px; }
        .exp-box ul { line-height: 1.8; padding-left: 1.2rem; }
        .no-bullet { list-style-type: none; padding-left: 1.2rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

exp_col1, exp_col2 = st.columns(2)

# Zentrales Styling für die Boxen (erhöht die Schriftgröße um ca. 4pt)
st.html("""
    <style>
        .exp-box {
            font-size: 1.2rem !important; /* Erhöht den Fließtext & Listen */
        }
        .exp-box h4 {
            font-size: 1.45rem !important; /* Erhöht die h4-Überschriften proportional */
        }
    </style>
""")

with exp_col1:
    st.markdown("""
        <div class="exp-box">
            <h4>💻 Аппаратное и программное обеспечение</h4>
            <ul>
                <li><strong>📐 Создание 3D-моделей в CATIA V5 или AutoCAD.</strong></li>
                <li><strong>🎙️🎧 Подключение, настройка датчиков и измерение объектов с использованием оборудования B&K или Head Acoustics.</strong></li>
                <li><strong>🔢 Анализ данных в Minitab или с помощью собственных статистических методов.</strong></li>
                <li><strong>🗄️ В SAP вроде как умеют работать все, но на самом деле — никто.</strong></li>
                <li><strong>📑 О продуктах MS Office в наше время уже никто и не говорит. Или как?</strong></li>
        </div>
        """, unsafe_allow_html=True)

with exp_col2:
    st.markdown("""
        <div class="exp-box">
            <h4>📋 Профессиональные и гибкие навыки</h4>
            <ul>
                <li>🛠️ <strong>Управление проектами (планирование, контроль реализации, валидация и ввод в эксплуатацию)</strong></li>
                <li><strong>🧩 Управление качеством | Бережливое производство и Шесть Сигм | Аудиты | Управление рисками</strong></li>
                <li><strong>🔍 ISO 9001 или IATF 16949 | CAPA или 8D | DMAIC или PDCA</strong></li>
            </ul>
            <div class="no-bullet" style="margin-top: 20px;">
                Здесь нам сначала нужно определиться с терминами, чтобы не говорить на разных языках.
            </div>
            <div style="margin-top: 13px;"></div> 
        </div>
        """, unsafe_allow_html=True)
    
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True) 

# Programmier-Abschnitt mit erhöhter Schriftart
st.markdown(f"""
    <div style="background-color: #d1e7dd; padding: 25px; border-radius: 15px; border-left: 6px solid #0f5132; color: #0f5132; font-size: 1.35rem; line-height: 1.6; margin-top: 20px;">
        <span style="font-size: 1.75rem;">🐍</span> <strong>Умею ли я программировать:</strong><br><br>
        Кстати, это делало не агентство — этот сайт я запрограммировал сам.<br>
        С помощью Python, Streamlit и пары-тройки чашек кофе.<br><br>
        <i>К слову, этот проект отлично помог мне обновить запас ругательств и их комбинаций на нескольких языках.</i>
    </div>
    """, unsafe_allow_html=True)




st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)





# --- HILFSFUNKTION FÜR BILDER (Muss vor dem Aufruf definiert sein) ---
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

st.divider()
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left;'>Увлечения</h2>", unsafe_allow_html=True)

# --- CSS FÜR LAYOUT, ZOOM UND PARAMETRIERBARE SCHRIFTGRÖSSEN ---
st.markdown("""
<style>
    :root, [data-testid="stHorizontalBlock"] {
        /* ========================================================= */
        /* PARAMETER FÜR DIE SCHRIFTGRÖSSEN (Hier einfach anpassen!) */
        /* ========================================================= */
        --size-icon: 34px;        /* Vorher: 30px */
        --size-title: 24px;       /* Vorher: 1.2rem (~19px) */
        --size-text: 19px;        /* Vorher: 0.95rem (~15px) */
        --size-placeholder: 18px; /* Vorher: 14px */
        --size-label: 14px;       /* Vorher: 10px */
    }

    [data-testid="stHorizontalBlock"] {
        display: flex;
        align-items: stretch;
    }
    .hobby-card {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 15px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        height: 100%;
        min-height: 460px; /* Leicht erhöht, da der Text nun mehr Platz braucht */
    }
    
    /* Zuweisung der Parameter über var() */
    .hobby-icon { font-size: var(--size-icon); margin-bottom: 10px; }
    .hobby-title { font-weight: bold; font-size: var(--size-title); color: #1e293b; margin-bottom: 10px; }
    .hobby-text { font-size: var(--size-text); color: #475569; line-height: 1.6; flex-grow: 1; }
    .img-label { font-size: var(--size-label); color: #94a3b8; text-align: center; margin-top: 4px; display: block; }
    
    .hobby-img-area { 
        display: flex; gap: 8px; margin-top: 15px; height: 110px; 
    }
    .hobby-img-wrapper { width: 31%; position: relative; }
    .hobby-img-wrapper img { 
        width: 100%; height: 100px; object-fit: cover; border-radius: 8px; 
        border: 1px solid #eee; transition: transform 0.3s ease;
        cursor: zoom-in;
    }
    .hobby-img-wrapper img:hover {
        transform: scale(1.8);
        z-index: 999;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="hobby-card">
        <div class="hobby-icon">♟️</div>
        <div class="hobby-title">Шахматы</div>
        <div class="hobby-text">
            Один мужчина купил своим детям шахматы. Через год он уже не мог за нами угнаться.
            Я просчитываю не только свои ходы, но и ходы коллег. 
        </div>
        <!-- Platzhalter-Text greift hier dynamisch auf die CSS-Variable zu -->
        <div style="height: 110px; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0.2; font-size: var(--size-placeholder); text-align: center; margin-top: auto;">
            Когда я только начинал играть в шахматы, в нашем посёлке камеры были у нескольких человек. Так что фотографий с тех времён, увы, нет.<br>
            <span style="font-size: 44px;">♔ ♕ ♖</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    img_f2 = get_base64_img("images/Hobbies/fussball1.png")
    img_h1 = get_base64_img("images/Hobbies/hockey1.png")
    img_h3 = get_base64_img("images/Hobbies/hockey3.png")
    
    st.markdown(f"""
    <div class="hobby-card">
        <div class="hobby-icon">🏒 & ⚽</div>
        <div class="hobby-title">Хоккей и футбол</div>
        <div class="hobby-text">Нет ничего лучше чувства, когда ты внёс вклад в успех товарища по команде.</div>
        <div class="hobby-img-area">
            <div class="hobby-img-wrapper">
                <img src="data:image/png;base64,{img_f2}" title="Золото наше">
                <span class="img-label">Футбол</span>
            </div>
            <div class="hobby-img-wrapper">
                <img src="data:image/png;base64,{img_h1}" title="И здесь на пьедестале">
                <span class="img-label">Хоккей</span>
            </div>
            <div class="hobby-img-wrapper">
                <img src="data:image/png;base64,{img_h3}" title="Взгляд за кулисы">
                <span class="img-label">Кузница</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    img_y1 = get_base64_img("images/Hobbies/box.png")
    img_y2 = get_base64_img("images/Hobbies/yoga2.jpg")
    img_y3 = get_base64_img("images/Hobbies/yoga3.png")

    st.markdown(f"""
    <div class="hobby-card">
        <div class="hobby-icon">🧘 & 🥊</div>
        <div class="hobby-title">Йога и бокс</div>
        <div class="hobby-text">Быстро реагировать и при этом оставаться невозмутимым.</div>
        <div class="hobby-img-area">
            <div class="hobby-img-wrapper">
                <img src="data:image/jpeg;base64,{img_y1}" title="Это расслабляет, говорили они">
                <span class="img-label">гибкость</span>
            </div>
            <div class="hobby-img-wrapper">
                <img src="data:image/jpeg;base64,{img_y2}" title="Это просто, говорили они">
                <span class="img-label">баланс</span>
            </div>
            <div class="hobby-img-wrapper">
                <img src="data:image/png;base64,{img_y3}" title="В жизни пригодится, говорили они">
                <span class="img-label">сила</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)




#Bonus-Abschnitt mit Video

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

st.divider()

st.markdown("<div style='margin-top: 150px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left;'>⚠️ 3 самые большие ошибки в расчётах в моей жизни</h2>", unsafe_allow_html=True)

st.markdown("""
<style>
    :root, [data-testid="stHorizontalBlock"] {
        /* PARAMETER FÜR DIE SCHRIFTGRÖSSEN */
        --size-quote: 21px;  
        --size-year: 18px;   
    }

    [data-testid="stHorizontalBlock"] {
        display: flex;
        align-items: stretch;
    }
    .quote-card {
        background: #ffffff;
        border-top: 5px solid #8e44ad;
        border-radius: 12px;
        padding: 25px;
        
        /* DIESE ZWEI ZEILEN ERZWINGEN DIE GLEICHE HÖHE */
        height: 100%;
        min-height: 180px; /* Garantiert eine einheitliche Höhe auf Desktop-Monitoren */
        
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between; /* Drückt die Jahreszahl automatisch ganz nach unten */
        transition: transform 0.2s ease;
    }
    .quote-card:hover {
        transform: translateY(-5px);
    }
    
    .quote-content {
        font-style: italic;
        color: #1e293b;
        font-size: var(--size-quote);
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .quote-year {
        text-align: right;
        font-weight: bold;
        color: #8e44ad;
        font-size: var(--size-year);
    }
    
    .quote-year::before {
        content: "— ";
    }
</style>
""", unsafe_allow_html=True)

q_col1, q_col2, q_col3 = st.columns(3)

with q_col1:
    st.markdown("""
    <div class="quote-card">
        <div class="quote-content">«Я проведу всю свою жизнь в этом месте».</div>
        <div class="quote-year">2002</div>
    </div>
    """, unsafe_allow_html=True)

with q_col2:
    st.markdown("""
    <div class="quote-card">
        <div class="quote-content">«Я уже слишком стар для программирования».</div>
        <div class="quote-year">2013</div>
    </div>
    """, unsafe_allow_html=True)

with q_col3:
    st.markdown("""
    <div class="quote-card">
        <div class="quote-content">«Цифровое резюме я набросаю быстренько. Делов-то на пару часов».</div>
        <div class="quote-year">Сейчас</div>
    </div>
    """, unsafe_allow_html=True)







st.markdown("<div style='margin-top: 200px;'></div>", unsafe_allow_html=True)



import streamlit as st
import os

# Seite auf Breitbild einstellen
st.set_page_config(layout="wide")

# Pfade definieren
video_path = os.path.join("videos", "VID_20240910_195820976.mp4")
image_path = os.path.join("images", "Frequenzen.png")

# --- CSS für Layout-Optimierung ---
st.markdown(
    """
    <style>
    /* Zentriert Video und Bild innerhalb ihrer Spalten */
    [data-testid="stColumn"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
    }

    /* Sorgt dafür, dass beide Medien eine harmonische Höhe haben */
    [data-testid="stHorizontalBlock"] video, 
    [data-testid="stHorizontalBlock"] img {
        max-height: 550px !important;
        width: auto !important;
        object-fit: contain;
    }
    
    /* Titel mittig ausrichten */
    h3 {
        text-align: left;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Bonus")

# Spalten im Verhältnis 1:2 erstellen (Video schmaler, Bild breiter)
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### Video")
    if os.path.exists(video_path):
        # Das Video füllt die schmalere Spalte optimal aus
        st.video(video_path)
    else:
        st.error("Video nicht gefunden")

with col2:
    st.write("### Frequenzbereich")
    if os.path.exists(image_path):
        # use_container_width sorgt dafür, dass das Bild die 2/3 Breite nutzt
        st.image(image_path, caption="Frequenzspektrum der Klangschale", use_container_width=True)
    else:
        st.error("Bild nicht gefunden")








st.markdown("<div style='margin-top: 350px;'></div>", unsafe_allow_html=True)







# --- DAS BUCH-SYMBOL (Am Ende deiner App) ---

st.write("") 
st.write("") 

# Spalten für die Positionierung rechts
spacer1, spacer2, book_col = st.columns([2, 1, 1])

with book_col:
    st.markdown("""
        <style>
            @keyframes float {
                0% { transform: translateY(0px) rotate(15deg); }
                50% { transform: translateY(-10px) rotate(10deg); }
                100% { transform: translateY(0px) rotate(15deg); }
            }
            .book-wrapper {
                display: flex;
                flex-direction: column;
                align-items: center;
                cursor: help;
                animation: float 4s ease-in-out infinite;
                position: relative;
                width: 120px;
            }
            .book-icon {
                font-size: 50px;
                filter: drop-shadow(5px 10px 15px rgba(0,0,0,0.2));
                transition: all 0.4s ease-in-out;
            }
            
            /* Text AUF dem Buch - Initial unsichtbar */
            .book-text {
                position: absolute;
                top: 48px;
                left: 55%;
                transform: translate(-50%, -50%) scale(0.5);
                color: #1a1a1a;
                font-family: 'Brush Script MT', cursive;
                font-size: 15px;
                font-weight: bold;
                line-height: 1.1;
                text-align: center;
                pointer-events: none;
                width: 70px;
                opacity: 0; /* Versteckt */
                transition: all 0.4s ease-in-out;
            }

            /* Hover-Effekte */
            .book-wrapper:hover .book-icon {
                transform: scale(1.2) rotate(0deg);
                filter: drop-shadow(2px 5px 5px rgba(0,0,0,0.1));
            }
            
            /* Text erscheint beim Hover */
            .book-wrapper:hover .book-text {
                opacity: 1; /* Sichtbar machen */
                transform: translate(-50%, -50%) scale(1.1); /* Leicht mit-vergrößern */
            }

            .book-tag {
                background: #f1f5f9;
                color: #64748b;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: bold;
                margin-top: -5px;
                border: 1px solid #e2e8f0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
        </style>
        
        <div class="book-wrapper" title="📖 Моя книга: Этот проект сейчас находится в разработке &ndash; история пишется день за днем.">
            <div class="book-icon">📖</div>
            <div class="book-tag">в процессе</div>
        </div>
    """, unsafe_allow_html=True)