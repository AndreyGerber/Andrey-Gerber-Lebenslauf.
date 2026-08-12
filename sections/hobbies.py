"""
sections/hobbies.py

"Leidenschaften & Ausgleich": drei Hobby-Karten nebeneinander.
Statisch, keine Interaktivität -> kein @st.fragment nötig.
"""

import streamlit as st
from utils.loaders import load_image_base64_cached

IMAGES_FOLDER = "images/Hobbies"

_CSS = """
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
    .hobby-img-area { display: flex; gap: 8px; margin-top: 15px; height: 110px; }
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
"""


def render_hobbies(t: dict):
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: left;'>{t['hobbies_title']}</h2>", unsafe_allow_html=True)
    st.markdown(_CSS, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="hobby-card">
            <div class="hobby-icon">♟️</div>
            <div class="hobby-title">{t['hobbies_chess_title']}</div>
            <div class="hobby-text">{t['hobbies_chess_text']}</div>
            <div style="height: 110px; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0.2; font-size: var(--size-placeholder); text-align: center; margin-top: auto;">
                {t['hobbies_chess_placeholder']}<br>
                <span style="font-size: 44px;">♔ ♕ ♖</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        img_f2 = load_image_base64_cached(f"{IMAGES_FOLDER}/fussball1.png")
        img_h1 = load_image_base64_cached(f"{IMAGES_FOLDER}/hockey1.png")
        img_h3 = load_image_base64_cached(f"{IMAGES_FOLDER}/hockey3.png")
        st.markdown(f"""
        <div class="hobby-card">
            <div class="hobby-icon">🏒 &amp; ⚽</div>
            <div class="hobby-title">{t['hobbies_sport_title']}</div>
            <div class="hobby-text">{t['hobbies_sport_text']}</div>
            <div class="hobby-img-area">
                <div class="hobby-img-wrapper">
                    <img src="data:image/png;base64,{img_f2}" title="{t['hobbies_sport_img1_title']}">
                    <span class="img-label">{t['hobbies_sport_img1_label']}</span>
                </div>
                <div class="hobby-img-wrapper">
                    <img src="data:image/png;base64,{img_h1}" title="{t['hobbies_sport_img2_title']}">
                    <span class="img-label">{t['hobbies_sport_img2_label']}</span>
                </div>
                <div class="hobby-img-wrapper">
                    <img src="data:image/png;base64,{img_h3}" title="{t['hobbies_sport_img3_title']}">
                    <span class="img-label">{t['hobbies_sport_img3_label']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        img_y1 = load_image_base64_cached(f"{IMAGES_FOLDER}/box.png")
        img_y2 = load_image_base64_cached(f"{IMAGES_FOLDER}/yoga2.jpg")
        img_y3 = load_image_base64_cached(f"{IMAGES_FOLDER}/yoga3.png")
        st.markdown(f"""
        <div class="hobby-card">
            <div class="hobby-icon">🧘 &amp; 🥊</div>
            <div class="hobby-title">{t['hobbies_yoga_title']}</div>
            <div class="hobby-text">{t['hobbies_yoga_text']}</div>
            <div class="hobby-img-area">
                <div class="hobby-img-wrapper">
                    <img src="data:image/png;base64,{img_y1}" title="{t['hobbies_yoga_img1_title']}">
                    <span class="img-label">{t['hobbies_yoga_img1_label']}</span>
                </div>
                <div class="hobby-img-wrapper">
                    <img src="data:image/jpeg;base64,{img_y2}" title="{t['hobbies_yoga_img2_title']}">
                    <span class="img-label">{t['hobbies_yoga_img2_label']}</span>
                </div>
                <div class="hobby-img-wrapper">
                    <img src="data:image/png;base64,{img_y3}" title="{t['hobbies_yoga_img3_title']}">
                    <span class="img-label">{t['hobbies_yoga_img3_label']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.divider()