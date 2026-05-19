import streamlit as st
from utils.text_loader import get_text


def show_experience():
    t = get_text(st.session_state.lang)

    # Titel
    st.markdown(f"## {t['experience_title']}")

    for job in t["experience"]:
        with st.container():

            # Jobtitel größer
            st.markdown(
                f"<div style='font-size:26px; font-weight:600;'>{job['title']}</div>",
                unsafe_allow_html=True
            )

            # Firma + Zeitraum
            st.markdown(
                f"<div style='font-size:18px; margin-top:5px;'><strong>{job['company']} | {job['period']}</strong></div>",
                unsafe_allow_html=True
            )

            # Beschreibung
            st.markdown(
                f"<div style='font-size:18px; line-height:1.6; margin-top:10px;'>{job['description']}</div>",
                unsafe_allow_html=True
            )

            st.markdown("---")