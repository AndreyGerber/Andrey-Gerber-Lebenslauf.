"""
sections/skills.py

Fertigkeiten-Bereich: zwei Bildergalerien (Kerzen-Projekt, CAD-Projekte)
in Containern nebeneinander, darunter Hardware/Software- und Hard-/Softskill-
Boxen, abgeschlossen mit dem "kann ich programmieren"-Hinweis.

Keine Interaktivität (keine Buttons) -> kein @st.fragment nötig.
"""

import streamlit as st
from utils.loaders import load_scaled_image_cached

IMAGE_SCALE = 38

KERZE_FILES = [
    "images/kerze0.png", "images/kerze1.png", "images/kerze2.png",
    "images/kerze3.png", "images/kerze4.jpg", "images/kerze5.jpg", "images/kerze6.jpg",
]

# (Pfad, Rotation in Grad)
PROJECT_CONFIGS = [
    ("images/project1.jpg", 0), ("images/project2.jpeg", 0),
    ("images/project3.jpeg", 90), ("images/project5.jpg", 0),
    ("images/project4.jpeg", 90), ("images/project6.jpeg", -90),
]


def render_skills(t: dict):
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

    st.title(t["skills_title"])
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown(f'<div class="equal-height-header"><h3>{t["skills_kerze_title"]}</h3></div>', unsafe_allow_html=True)
            k_cols = st.columns(3)
            for idx, img_path in enumerate(KERZE_FILES):
                img = load_scaled_image_cached(img_path, scale_percent=IMAGE_SCALE)
                if img:
                    k_cols[idx % 3].image(img, use_container_width=True)

    with col2:
        with st.container(border=True):
            st.markdown(f'<div class="equal-height-header"><h3>{t["skills_project_title"]}</h3></div>', unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
            p_cols = st.columns(3)
            for idx, (img_path, angle) in enumerate(PROJECT_CONFIGS):
                img = load_scaled_image_cached(img_path, angle, scale_percent=IMAGE_SCALE)
                if img:
                    p_cols[idx % 3].image(img, use_container_width=True)
            st.markdown("<div style='margin-top: 58px;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # --- Hard- & Softskill-Boxen ---
    st.markdown("""
        <style>
            .exp-box {
                background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
                padding: 25px;
                border-radius: 16px;
                border-left: 4px solid #4a90e2;
                height: 100%;
                font-size: 1.2rem !important;
            }
            .exp-box h4 { color: #01579b; margin-top: 0; margin-bottom: 15px; font-size: 1.45rem !important; }
            .exp-box ul { line-height: 1.8; padding-left: 1.2rem; }
            .no-bullet { list-style-type: none; padding-left: 1.2rem; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.markdown(f"""
            <div class="exp-box">
                <h4>💻 {t['skills_hw_sw_title']}</h4>
                <ul>{t['skills_hw_sw_items']}</ul>
            </div>
        """, unsafe_allow_html=True)

    with exp_col2:
        st.markdown(f"""
            <div class="exp-box">
                <h4>📋 {t['skills_hard_soft_title']}</h4>
                <ul>{t['skills_hard_soft_items']}</ul>
                <div class="no-bullet" style="margin-top: 20px;">{t['skills_hard_soft_note']}</div>
                <div style="margin-top: 13px;"></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background-color: #d1e7dd; padding: 25px; border-radius: 15px; border-left: 6px solid #0f5132; color: #0f5132; font-size: 1.35rem; line-height: 1.6; margin-top: 20px;">
            <span style="font-size: 1.75rem;">🐍</span> <strong>{t['skills_coding_title']}</strong><br><br>
            {t['skills_coding_text']}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)