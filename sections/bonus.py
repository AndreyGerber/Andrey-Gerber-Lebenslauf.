"""
sections/bonus.py

Bonus-Bereich: Video links, Frequenzbild rechts.
Abgeschlossen mit dem kleinen schwebenden Buch-Icon ("noch in Arbeit")
ganz am Ende der Seite.

Statisch, keine Interaktivität -> kein @st.fragment nötig.
"""

import os
import streamlit as st

VIDEO_PATH = os.path.join("videos", "VID_20240910_195820976.mp4")
IMAGE_PATH = os.path.join("images", "Frequenzen.png")

_LAYOUT_CSS = """
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
</style>
"""

_BOOK_CSS_AND_HTML = """
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
    .book-wrapper:hover .book-icon {
        transform: scale(1.2) rotate(0deg);
        filter: drop-shadow(2px 5px 5px rgba(0,0,0,0.1));
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
<div class="book-wrapper" title="{tooltip}">
    <div class="book-icon">📖</div>
    <div class="book-tag">{tag}</div>
</div>
"""


def render_bonus(t: dict):
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div style='margin-top: 200px;'></div>", unsafe_allow_html=True)

    st.markdown(_LAYOUT_CSS, unsafe_allow_html=True)
    st.title(t["bonus_title"])

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write(f"### {t['bonus_video_label']}")
        if os.path.exists(VIDEO_PATH):
            st.video(VIDEO_PATH)
        else:
            st.error(f"Video nicht gefunden: {VIDEO_PATH}")

    with col2:
        st.write(f"### {t['bonus_image_label']}")
        if os.path.exists(IMAGE_PATH):
            st.image(IMAGE_PATH, caption=t["bonus_image_caption"], use_container_width=True)
        else:
            st.error(f"Bild nicht gefunden: {IMAGE_PATH}")

    st.markdown("<div style='margin-top: 350px;'></div>", unsafe_allow_html=True)
    st.write("")
    st.write("")

    spacer1, spacer2, book_col = st.columns([2, 1, 1])
    with book_col:
        st.markdown(
            _BOOK_CSS_AND_HTML.format(tooltip=t["footer_book_tooltip"], tag=t["footer_book_tag"]),
            unsafe_allow_html=True,
        )