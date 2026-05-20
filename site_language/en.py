import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pydeck as pdk
import base64
import os
from PIL import Image, ImageOps



# Page settings
st.set_page_config(page_title="Andrey Gerber - Resume", layout="wide")

# 1. Title (centered, two lines)
st.markdown("<h2 style='text-align: center;'>Welcome to the page of</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #4B0082;'>Andrey Gerber's Resume</h1>", unsafe_allow_html=True)
st.divider()

# --- 1. FUNCTION FOR STABLE IMAGE SIZE (scalable) ---
def load_formatted_image(name, target_size=(900, 600), max_width=None):
    path = os.path.join("images", name)
    
    if not os.path.exists(path):
        return None
        
    if path.lower().endswith(".pdf"):
        return None

    try:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
            
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
        print(f"Error with file {name}: {e}")
        return None

# --- 2. DATA & LOGIC ---
if 'bild_index' not in st.session_state:
    st.session_state.bild_index = 0

slideshow_images = ["ich1.JPG", "ich_pass.png", "aufenthaltstitel.png"]
drawing_name = "itsme2.png"

# --- 3. GLOBAL STYLE FOR CENTERING ---
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    .contact-link {
        text-decoration: none;
        color: #007BFF;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LAYOUT: 3 COLUMNS ---
col_image, col_center, col_data = st.columns([1.5, 1.0, 1.5])

with col_image:
    current_photo = load_formatted_image(slideshow_images[st.session_state.bild_index])
    if current_photo:
        st.image(current_photo, use_container_width=True)
    else:
        st.error(f"File missing: {slideshow_images[st.session_state.bild_index]}")

    # Navigation below the image
    p_left, p_center, p_right = st.columns([1, 4, 1]) 
    with p_left:
        if st.button("⬅️"):
            st.session_state.bild_index = (st.session_state.bild_index - 1) % len(slideshow_images)
            st.rerun()
    with p_right:
        if st.button("➡️"):
            st.session_state.bild_index = (st.session_state.bild_index + 1) % len(slideshow_images)
            st.rerun()

with col_center:
    drawing = load_formatted_image(drawing_name, target_size=(300, 300))
    if drawing:
        st.image(drawing, use_container_width=True)
    else:
        st.info("Your drawing will appear here...")

with col_data:
    st.markdown("<p style='font-size: 30px; color: gray; margin-bottom: -10px;'>My Contact Details</p>", unsafe_allow_html=True)
    
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
                📍 <i>Address: Just call or email me</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- LANGUAGE SKILLS SECTION ---
    st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)
    
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

# --- MY CAREER PATH ---
# All years for labeling
all_years = [1988, 1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]
# Years that get a diamond on the line (all except 1988)
years_with_diamond = [1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]

SIZE_YEARS = 19       # Font size for years (bold)
SIZE_TEXTS = 17       # Font size for descriptions

# Texts for the blocks (English version)
texts = {
    1988: "Born in USSR ☭",
    1991: "Moved to Russian Federation<br>without moving 🇷🇺",
    1996: "School (not cool)",
    2006: "Emigration to GE 🇩🇪",
    2010: "Studying aircraft design<br>(B.Eng. & Ms.Sc.)",
    2017: "TÜV Rheinland<br>(Expert in the lab  &                    ",
    2019: "                  Quality Expert)",
    2022: "Ferchau (at Siemens)<br>(Quality Systems Engineering)",
    2026: "Liora<br>(Data Science & ML)"
}

# Design settings
LINE_THICKNESS = 3
START_DASH_LENGTH = 0.18
YEAR_FONT_SIZE = 16

# Title left-aligned
st.markdown("<h2 style='text-align: left;'>My Career Path</h2>", unsafe_allow_html=True)

# --- 2. CREATE GRAPH ---
fig = go.Figure()

# Life line: Continuous from 1988 to just before the arrowhead (2034)
fig.add_trace(go.Scatter(
    x=[1988, 2029], 
    y=[0, 0],
    mode='lines',
    line=dict(color='black', width=LINE_THICKNESS),
    showlegend=False, 
    hoverinfo='none'
))

# Vertical start dash at 1988
fig.add_shape(
    type="line", 
    x0=1988, y0=-START_DASH_LENGTH, 
    x1=1988, y1=START_DASH_LENGTH,
    line=dict(color="black", width=LINE_THICKNESS + 1)
)

# White diamonds (starting 1996), centered on the line
fig.add_trace(go.Scatter(
    x=years_with_diamond, 
    y=[0] * len(years_with_diamond),
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

# Year numbers and text blocks (rotated 45°)
for i, year in enumerate(all_years):
    if year in [1991, 2017, 2019, 2022]:
        y_offset = -0.05
    else:
        y_offset = -0.20
    
    fig.add_annotation(
        x=year, y=-0.1, 
        text=f"<b>{year}</b>",
        showarrow=False, 
        textangle=-30,
        font=dict(size=SIZE_YEARS, color="black"),
        xanchor="center", 
        yanchor="top"
    )
    
    fig.add_annotation(
        x=year, y=y_offset, 
        text=texts.get(year, ""),
        showarrow=False, 
        textangle=-30,
        font=dict(size=SIZE_TEXTS, color="#4B0082"),
        xanchor="center", 
        yanchor="top"
    )

fig.update_layout(
    height=500,
    margin=dict(l=50, r=50, t=20, b=250), 
    yaxis=dict(range=[-1.8, 0.5]) 
)

# Arrowhead at the right end
fig.add_annotation(
    x=2030, y=0,
    ax=2028, ay=0,
    xref="x", yref="y", 
    axref="x", ayref="y",
    showarrow=True, 
    arrowhead=2, 
    arrowsize=1.5, 
    arrowwidth=LINE_THICKNESS, 
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

# --- DETAILS BLOCK FOR CAREER PATH ---
BLOCK_HEIGHT = 750
IMAGE_WIDTH = 350
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

with st.container(height=BLOCK_HEIGHT, border=True):
    active_year = highlights[st.session_state.info_idx]

    if active_year == 1988:
        st.markdown(f"<h3 style='text-align: left;'>📍 {active_year}: Here my journey began</h3>", unsafe_allow_html=True)

        MAP_SCALE = 0.8
        
        def get_base64(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()

        try:
            img_b64 = get_base64("images/tscherlak_map.png")
            
            st.markdown(f"""
                <div style="width: {int(MAP_SCALE * 100)}%; margin: auto;">
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
            st.error(f"Error: {e}")

    elif active_year == 1996:
        SCALE = 1.2
        TOP_MARGIN = "10px"

        col_text, col_photo = st.columns([1, 2.5])

        with col_text:
            st.markdown(f"<div style='margin-top: {TOP_MARGIN};'></div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: left;'>🎒 {active_year}: School Years</h3>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: {INFO_FONT_SIZE}; color: #0055A5;'>How quickly 10 years pass.</p>", unsafe_allow_html=True)

        with col_photo:
            img_school = load_formatted_image("schule2.png")
            if img_school:
                st.markdown(f"<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                original_width = img_school.size[0]
                new_width = int(original_width * SCALE)
                st.image(img_school, width=new_width)
            else:
                st.error("Image 'schule2.png' not found.")

    elif active_year == 2006:
        st.markdown(f"<h3 style='text-align: left;'>✈️ {active_year}: A new chapter begins</h3>", unsafe_allow_html=True)
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

    elif active_year == 2010:
        STUDY_SCALE = 1.0
        TOP_MARGIN = "10px"

        col_text, col_photo = st.columns([1, 2.5])

        with col_text:
            st.markdown(f"<h3 style='text-align: left;'>🎓 {active_year}: Studies</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top: {TOP_MARGIN};'></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)            
            st.markdown(f"""
                <p style='font-size: {INFO_FONT_SIZE}; color: #0055A5; line-height: 1.4;'>
                <strong>Bachelor of Engineering</strong><br>
                & <strong>Master of Science</strong>.<br><br><br><br>
                <i>"Watch out, science – I'm coming!"</i>
                </p>
                """, unsafe_allow_html=True)

        with col_photo:
            img_haw = load_formatted_image("haw.png")
            if img_haw:
                st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
                original_width = img_haw.size[0]
                new_width = int(original_width * STUDY_SCALE)
                st.image(img_haw, width=new_width)
            else:
                st.error("Image 'haw.png' could not be loaded.")

    elif active_year == 2017:
        TUV_SCALE = 1.15
        TOP_MARGIN_TEXT = "10px" 

        col_text, col_photo = st.columns([1, 1.8])

        with col_text:
            st.markdown(f"<h3 style='text-align: left;'>🛠️ {active_year}– 2022: TÜV Rheinland</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top: {TOP_MARGIN_TEXT};'></div>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-bottom: 5px;'><strong>Test & Measurement Engineer</strong></p>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Standard-compliant <b>acoustic measurements</b> (household appliances, tools, toys)</li>
                    <li>Planning & setup of a <b>new test chamber</b> for smart speakers</li>
                    <li><b>Vibration measurements & custom special measurements</b></li>
                    <li>Member of the <b>DIN standards committee</b> for sound insulation</li>
                </ul>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-top: 20px; margin-bottom: 5px;'><strong>from 2019 <br>Quality Manager / Quality Expert</strong></p>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Conducting <b>internal audits</b> (ISO 9001 & ISO 17025)</li>
                    <li>Responsibility for <b>CAPA processes</b> and <b>complaint management</b></li>
                    <li><b>External audits</b> and <b>management reviews</b></li>
                </ul>
            """, unsafe_allow_html=True)

        with col_photo:
            img_tuv = load_formatted_image("tuev.png")
            if img_tuv:
                st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                original_width = img_tuv.size[0]
                new_width = int(original_width * TUV_SCALE)
                st.image(img_tuv, width=new_width)
            else:
                st.error("File 'images/tuev.png' not found.")

    elif active_year == 2022:
        FERCHAU_SCALE = 1.15
        TOP_MARGIN_TEXT = "10px" 

        col_text, col_photo = st.columns([1, 1.8])

        with col_text:
            st.markdown(f"<h3 style='text-align: left;'>⚙️ {active_year} – 2025: Ferchau GmbH</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top: {TOP_MARGIN_TEXT};'></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)   

            st.markdown(f"""
                <p style='font-size: 24px; color: #0055A5; margin-bottom: 5px;'><strong>Process Technologist at Siemens Healthineers</strong></p><br>
                <ul style='font-size: 20px; color: #333; line-height: 1.6;'>
                    <li>Maintenance and repair of existing equipment for <b>acoustic and vibration measurements</b></li>
                    <li>Supporting the setup of several <b>test chambers for acoustic and vibration measurements</b> at the new production site</li>
                    <li><b>Development of new test methods</b></li>
                    <li><b>Validation and commissioning</b> for series production</li>
                </ul>
            """, unsafe_allow_html=True)

        with col_photo:
            img_fer = load_formatted_image("ferchau.png")
            if img_fer:
                st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                original_width = img_fer.size[0]
                new_width = int(original_width * FERCHAU_SCALE)
                st.image(img_fer, width=new_width)
            else:
                st.error("File 'images/ferchau.png' not found.")

st.markdown('<div style="margin-top: 150px;"></div>', unsafe_allow_html=True)

st.write("")

# --- CERTIFICATES SECTION ---
st.markdown("<h2 style='text-align: left;'>My Certificates & Credentials</h2>", unsafe_allow_html=True)
st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <div style="background-color: #e1f5fe; padding: 20px; border-radius: 15px; border-left: 5px solid #01579b; margin-bottom: 20px;">
            <p style="color: #333; font-size: 1.1em;">
                🗃️ Here you will find an overview of my academic and professional credentials.
            </p>
            <div style="background-color: #fff9c4; padding: 10px; border-radius: 8px; border: 1px solid #fbc02d;">
                <strong>⚠️ Important note regarding name change:</strong><br>
                Please note that I have changed my name during my life. Some of the documents listed below 
                (e.g., high school diploma, Bachelor's degree) are therefore issued under my previous name. 
                <br>Corresponding proof of the name change is provided as the first document in the gallery.
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- PDF GALLERY with st.button ---
if "active_doc" not in st.session_state:
    st.session_state.active_doc = "Namensaenderung.pdf"

def get_pdf_base64(file_name):
    path = os.path.join("documents", file_name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

top_doc = {"file": "Namensaenderung.pdf", "icon": "📝", "label": "Name Change"}
other_docs = [
    {"file": "Berufsschule.pdf", "icon": "⚒️", "label": "Vocational School"},
    {"file": "allgemeineHochschulreife.pdf", "icon": "📜", "label": "High School Diploma"},
    {"file": "Praktikum_V&F.pdf", "icon": "🔧", "label": "Internship V&F"},
    {"file": "Bachelor.pdf", "icon": "✈️", "label": "Bachelor's Degree"},
    {"file": "Schweisskurs.pdf", "icon": "👨‍🏭", "label": "Welding Course"},
    {"file": "Wertanalytiker.pdf", "icon": "💎", "label": "Value Analyst"},
    {"file": "Master.pdf", "icon": "🎓", "label": "Master's Degree"},
    {"file": "b_k_pulse.pdf", "icon": "📟", "label": "B&K Pulse"},
    {"file": "M_BBM.pdf", "icon": "🔊", "label": "M-BBM"},
    {"file": "Interner_Auditor.pdf", "icon": "🕵️", "label": "Auditor 9001 ff."},
    {"file": "Qualitätsbeauftragter.pdf", "icon": "🛡️", "label": "QMB ISO 9001"},
    {"file": "QMB_ISO_17025.pdf", "icon": "🛡️", "label": "QMB ISO 17025"},
    {"file": "Data_Science.pdf", "icon": "🐍", "label": "Data Science"}
]

# Global CSS for ALL buttons
st.markdown("""
<style>
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
    
    .stButton > button p {
        margin: 0 !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #475569 !important;
        line-height: 1.3 !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    .stButton > button p::first-line {
        font-size: 25px !important;
        line-height: 1.5 !important;
    }
    
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
    
    # Top document centered
    t_c1, t_c2, t_c3 = st.columns(3)
    with t_c2:
        doc = top_doc
        is_active = st.session_state.active_doc == doc['file']
        
        if st.button(f"{doc['icon']}\n{doc['label']}", key=f"btn_{doc['file']}", use_container_width=True):
            st.session_state.active_doc = doc['file']
            st.rerun()
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Other documents in a 3-column grid
    grid_cols = st.columns(3)
    for i, doc in enumerate(other_docs):
        with grid_cols[i % 3]:
            if st.button(f"{doc['icon']}\n{doc['label']}", key=f"btn_{doc['file']}", use_container_width=True):
                st.session_state.active_doc = doc['file']
                st.rerun()
    
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

with col_viewer:
    active_pdf = st.session_state.active_doc
    
    pdf_path = os.path.join("documents", active_pdf)
    
    # Exception mapping for image previews
    mapping_exceptions = {
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
    
    if active_pdf in mapping_exceptions:
        img_file = mapping_exceptions[active_pdf]
    else:
        img_file = active_pdf.replace(".pdf", ".jpg")
        
    image_path = os.path.join("images", "Zertifikate", img_file)

    # 1. DOWNLOAD BUTTON
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(
                label=f"📥 Open PDF: {active_pdf}",
                data=f,
                file_name=active_pdf,
                mime="application/pdf",
                use_container_width=True
            )
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 2. IMAGE PREVIEW
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True, caption=f"Preview: {active_pdf}")
    else:
        pdf_b64 = get_pdf_base64(active_pdf)
        if pdf_b64:
            st.warning("Image preview not found, loading PDF viewer...")
            st.markdown(f'''
                <iframe src="data:application/pdf;base64,{pdf_b64}#toolbar=0" 
                        width="100%" height="800px" style="border-radius:15px; border:1px solid #e2e8f0;">
                </iframe>
            ''', unsafe_allow_html=True)

st.write("")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==================== FLOWING 3D WALL WITH THREE.JS ====================
st.markdown("<h2 style='text-align: left; margin-top: 50px;'>💻 Data Science & Machine Learning</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; margin-top: 10px;'>a 3D wall that you can zoom and rotate.</h5>", unsafe_allow_html=True)

# Your 24 certificate names with numbering
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

# Collect existing images with Base64
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
    import math
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

    # Layout: 3 columns (20% : 60% : 20%)
    col1, col2, col3 = st.columns([0.7, 3, 0.7])
    with col2:
        components.html(threejs_html, height=700, scrolling=False)
    
st.markdown("<br>" * 3, unsafe_allow_html=True)

# --- SKILLS SECTION ---
# Function for scaling images
def load_scaled_img(path, degrees=0, scale_percent=40):
    if os.path.exists(path):
        img = Image.open(path)
        if degrees != 0:
            img = img.rotate(degrees, expand=True)
        scale_factor = scale_percent / 100
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        return img.resize(new_size, Image.Resampling.LANCZOS)
    return None

# Settings
IMAGE_SCALING = 38 

# CSS for background color and spacing
st.markdown("""
    <style>
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #f8f9fa !important;
            padding: 10px !important;
        }
        .equal-height-header {
            min-height: 80px;
            display: flex;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ My Skills")
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

# Main columns
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown('<div class="equal-height-header"><h3>From sketch to finished product</h3></div>', unsafe_allow_html=True)
        
        candle_files = [
            "images/kerze0.png", "images/kerze1.png", "images/kerze2.png", 
            "images/kerze3.png", "images/kerze4.jpg", "images/kerze5.jpg", "images/kerze6.jpg"
        ]
        k_cols = st.columns(3) 
        for idx, img_path in enumerate(candle_files):
            img = load_scaled_img(img_path, scale_percent=IMAGE_SCALING)
            if img:
                k_cols[idx % 3].image(img, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown('<div class="equal-height-header"><h3>From idea to handover to production</h3></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        project_configs = [
            ("images/project1.jpg", 0), ("images/project2.jpeg", 0),
            ("images/project3.jpeg", 90), ("images/project5.jpg", 0),   
            ("images/project4.jpeg", 90), ("images/project6.jpeg", -90)
        ]
        p_cols = st.columns(3)
        for idx, (img_path, angle) in enumerate(project_configs):
            img = load_scaled_img(img_path, angle, scale_percent=IMAGE_SCALING)
            if img:
                p_cols[idx % 3].image(img, use_container_width=True)
        
        st.markdown("<div style='margin-top: 58px;'></div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True) 

# --- Hard & Soft Skills ---
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

# Central styling for the boxes (larger font)
st.html("""
    <style>
        .exp-box {
            font-size: 1.2rem !important;
        }
        .exp-box h4 {
            font-size: 1.45rem !important;
        }
    </style>
""")

with exp_col1:
    st.markdown("""
        <div class="exp-box">
            <h4>💻 Hardware & Software</h4>
            <ul>
                <li><strong>📐 Create 3D models with CATIA V5 or AutoCAD.</strong></li>
                <li><strong>🎙️🎧 Connect and configure sensors, measure objects with technology from B&K or Head Acoustics.</strong></li>
                <li><strong>🔢 Analyze data with Minitab or self-created statistical methods.</strong></li>
                <li><strong>🗄️ Everyone knows SAP somehow, but no one knows it the same way.</strong></li>
                <li><strong>📑 Nobody talks about MS products nowadays. Right?</strong></li>
        </div>
        """, unsafe_allow_html=True)

with exp_col2:
    st.markdown("""
        <div class="exp-box">
            <h4>📋 Hard Skills & Soft Skills</h4>
            <ul>
                <li>🛠️ <strong>Project management (planning, execution control, validation & commissioning)</strong></li>
                <li><strong>🧩 Quality management | Lean Management & Six Sigma | Audits | Risk management</strong></li>
                <li><strong>🔍 ISO 9001 or IATF 16949 | CAPA or 8D | DMAIC or PDCA</strong></li>
            </ul>
            <div class="no-bullet" style="margin-top: 20px;">
                First we need to define the terms before we talk past each other.
            </div>
            <div style="margin-top: 13px;"></div> 
        </div>
        """, unsafe_allow_html=True)
    
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True) 

# Programming section
st.markdown(f"""
    <div style="background-color: #d1e7dd; padding: 25px; border-radius: 15px; border-left: 6px solid #0f5132; color: #0f5132; font-size: 1.35rem; line-height: 1.6; margin-top: 20px;">
        <span style="font-size: 1.75rem;">🐍</span> <strong>Can I code?</strong><br><br>
        By the way, this isn't an agency – I programmed this page myself.<br>
        With Python, Streamlit, and one or two cups of coffee.<br><br>
        <i>This project also helped me update my vocabulary of swear words and their combinations in several languages.</i>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

# --- HOBBIES & PASSIONS SECTION ---
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

st.divider()
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left;'>Passions & Balance</h2>", unsafe_allow_html=True)

# CSS for layout, zoom, and scalable fonts
st.markdown("""
<style>
    :root, [data-testid="stHorizontalBlock"] {
        --size-icon: 34px;
        --size-title: 24px;
        --size-text: 19px;
        --size-placeholder: 18px;
        --size-label: 14px;
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
        min-height: 460px;
    }
    
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
        <div class="hobby-title">Chess</div>
        <div class="hobby-text">
            A man bought a chess set for his children. After a year, he couldn't keep up with us anymore.
            I don't just see my moves ahead, but also my opponent's moves.
        </div>
        <div style="height: 110px; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0.2; font-size: var(--size-placeholder); text-align: center; margin-top: auto;">
            When I started playing chess, there were probably only three people in our town with cameras. So unfortunately no pictures from back then.<br>
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
        <div class="hobby-title">Ice Hockey & Soccer</div>
        <div class="hobby-text">Nothing beats the feeling of contributing to someone else's success.</div>
        <div class="hobby-img-area">
            <div class="hobby-img-wrapper">
                <img src="data:image/png;base64,{img_f2}" title="Gold medal">
                <span class="img-label">Soccer</span>
            </div>
            <div class="hobby-img-wrapper">
                <img src="data:image/png;base64,{img_h1}" title="On the podium again">
                <span class="img-label">Ice Hockey</span>
            </div>
            <div class="hobby-img-wrapper">
                <img src="data:image/png;base64,{img_h3}" title="Behind the scenes">
                <span class="img-label">Training</span>
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
        <div class="hobby-title">Yoga & Boxing</div>
        <div class="hobby-text">React quickly and still stay calm.</div>
        <div class="hobby-img-area">
            <div class="hobby-img-wrapper">
                <img src="data:image/jpeg;base64,{img_y1}" title="It's relaxing, they said">
                <span class="img-label">agile</span>
            </div>
            <div class="hobby-img-wrapper">
                <img src="data:image/jpeg;base64,{img_y2}" title="It's easy, they said">
                <span class="img-label">balanced</span>
            </div>
            <div class="hobby-img-wrapper">
                <img src="data:image/png;base64,{img_y3}" title="You'll need it in life, they said">
                <span class="img-label">strong</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- BONUS SECTION: MISJUDGMENTS ---
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
st.divider()
st.markdown("<div style='margin-top: 150px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left;'>⚠️ The 3 biggest misjudgments of my life</h2>", unsafe_allow_html=True)

st.markdown("""
<style>
    :root, [data-testid="stHorizontalBlock"] {
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
        height: 100%;
        min-height: 180px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
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
        <div class="quote-content">"I will spend my entire life in this place."</div>
        <div class="quote-year">2002</div>
    </div>
    """, unsafe_allow_html=True)

with q_col2:
    st.markdown("""
    <div class="quote-card">
        <div class="quote-content">"I'm already too old for programming."</div>
        <div class="quote-year">2013</div>
    </div>
    """, unsafe_allow_html=True)

with q_col3:
    st.markdown("""
    <div class="quote-card">
        <div class="quote-content">"I'll build the digital resume quickly. It'll only take a few hours."</div>
        <div class="quote-year">Today</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 200px;'></div>", unsafe_allow_html=True)

# --- BONUS SECTION: VIDEO & FREQUENCY IMAGE ---
video_path = os.path.join("videos", "VID_20240910_195820976.mp4")
image_path = os.path.join("images", "Frequenzen.png")

# CSS for layout optimization
st.markdown(
    """
    <style>
    [data-testid="stColumn"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
    }

    [data-testid="stHorizontalBlock"] video, 
    [data-testid="stHorizontalBlock"] img {
        max-height: 550px !important;
        width: auto !important;
        object-fit: contain;
    }
    
    h3 {
        text-align: left;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Bonus")

# Columns in ratio 1:2 (video narrower, image wider)
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### Video")
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.error("Video not found")

with col2:
    st.write("### Frequency Range")
    if os.path.exists(image_path):
        st.image(image_path, caption="Frequency spectrum of the singing bowl", use_container_width=True)
    else:
        st.error("Image not found")

st.markdown("<div style='margin-top: 350px;'></div>", unsafe_allow_html=True)

# --- THE BOOK SYMBOL (At the end of your app) ---
st.write("") 
st.write("") 

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
                opacity: 0;
                transition: all 0.4s ease-in-out;
            }

            .book-wrapper:hover .book-icon {
                transform: scale(1.2) rotate(0deg);
                filter: drop-shadow(2px 5px 5px rgba(0,0,0,0.1));
            }
            
            .book-wrapper:hover .book-text {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1.1);
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
        
        <div class="book-wrapper" title="📖 My book: This project is currently a work in progress – the story writes itself day by day.">
            <div class="book-icon">📖</div>
            <div class="book-tag">still in progress</div>
        </div>
    """, unsafe_allow_html=True)