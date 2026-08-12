"""
sections/certificates.py

Zeugnis-/Zertifikat-Galerie: Buttons links, PDF-Download + Bildvorschau rechts.

Performance-Hinweis:
Die komplette Galerie steckt in einem @st.fragment. Ein Klick auf einen
der ~16 Dokument-Buttons rerennt NUR diesen Block - nicht Header, Timeline
etc. darüber.
"""

import os
import streamlit as st

from sections.certificate_config import DOCUMENTS_FOLDER, TOP_DOCUMENT, OTHER_DOCUMENTS
from utils.loaders import load_pdf_base64_cached

_BUTTON_CSS = """
<style>
    /* Nur Buttons INNERHALB von st.container(key="cert_gallery_buttons")
       bekommen diesen Look - alle anderen Buttons (Sprachwahl, Slideshow-
       Pfeile, Timeline-Navigation) bleiben im Standard-Streamlit-Stil. */
    .st-key-cert_gallery_buttons .stButton > button {
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
    .st-key-cert_gallery_buttons .stButton > button p {
        margin: 0 !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #475569 !important;
        line-height: 1.3 !important;
        text-align: center !important;
        width: 100% !important;
    }
    .st-key-cert_gallery_buttons .stButton > button p::first-line {
        font-size: 25px !important;
        line-height: 1.5 !important;
    }
    .st-key-cert_gallery_buttons .stButton > button:hover {
        transform: translateY(-5px) !important;
        border-color: #94a3b8 !important;
        background-color: #f1f5f9 !important;
    }
</style>
"""


@st.fragment
def render_certificate_gallery(t: dict):
    st.markdown(f"<h2 style='text-align: left;'>{t['cert_gallery_title']}</h2>", unsafe_allow_html=True)
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background-color: #e1f5fe; padding: 20px; border-radius: 15px; border-left: 5px solid #01579b; margin-bottom: 20px;">
            <p style="color: #333; font-size: 1.1em;">
                🗃️ {t['cert_gallery_intro']}
            </p>
            <div style="background-color: #fff9c4; padding: 10px; border-radius: 8px; border: 1px solid #fbc02d;">
                <strong>⚠️ {t['cert_gallery_name_change_title']}</strong><br>
                {t['cert_gallery_name_change_text']}
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "active_doc" not in st.session_state:
        st.session_state.active_doc = TOP_DOCUMENT["pdf"]

    st.markdown(_BUTTON_CSS, unsafe_allow_html=True)

    col_gallery, col_viewer = st.columns([1, 1.4])

    with col_gallery:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

        with st.container(key="cert_gallery_buttons"):
            # Top-Dokument (Namensänderung) zentriert
            t_c1, t_c2, t_c3 = st.columns(3)
            with t_c2:
                label = f"{TOP_DOCUMENT['icon']}\n{t[TOP_DOCUMENT['label_key']]}"
                if st.button(label, key=f"btn_{TOP_DOCUMENT['pdf']}", use_container_width=True):
                    st.session_state.active_doc = TOP_DOCUMENT["pdf"]

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

            # Restliche Dokumente im 3er-Grid.
            # WICHTIG: Für JEDE Zeile einen neuen st.columns(3)-Aufruf, statt
            # dieselben 3 Spalten über die ganze Schleife wiederzuverwenden.
            # Sonst stapelt sich jede Spalte unabhängig, und kleine Höhen-
            # unterschiede zwischen Buttons lassen die Zeilen auseinanderdriften.
            for row_start in range(0, len(OTHER_DOCUMENTS), 3):
                row_docs = OTHER_DOCUMENTS[row_start:row_start + 3]
                row_cols = st.columns(3)
                for col, doc in zip(row_cols, row_docs):
                    with col:
                        label = f"{doc['icon']}\n{t[doc['label_key']]}"
                        if st.button(label, key=f"btn_{doc['pdf']}", use_container_width=True):
                            st.session_state.active_doc = doc["pdf"]

        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    with col_viewer:
        active_pdf = st.session_state.active_doc
        all_docs = [TOP_DOCUMENT] + OTHER_DOCUMENTS
        active_entry = next((d for d in all_docs if d["pdf"] == active_pdf), TOP_DOCUMENT)

        pdf_path = os.path.join(DOCUMENTS_FOLDER, active_pdf)

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=f"📥 {t['cert_gallery_download_label']}: {active_pdf}",
                    data=f,
                    file_name=active_pdf,
                    mime="application/pdf",
                    use_container_width=True,
                )
        else:
            st.warning(f"{t['cert_gallery_missing_file']} ({pdf_path})")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        image_path = active_entry["image"]
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True, caption=f"{t['cert_gallery_preview_label']}: {active_pdf}")
        else:
            pdf_b64 = load_pdf_base64_cached(pdf_path)
            if pdf_b64:
                st.warning(t["cert_gallery_no_preview_warning"])
                st.markdown(f'''
                    <iframe src="data:application/pdf;base64,{pdf_b64}#toolbar=0"
                            width="100%" height="800px" style="border-radius:15px; border:1px solid #e2e8f0;">
                    </iframe>
                ''', unsafe_allow_html=True)
            else:
                st.error(t["cert_gallery_missing_file"])