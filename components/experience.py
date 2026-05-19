import streamlit as st
from utils.text_loader import get_text


def show_experience():
    t = get_text(st.session_state.lang)

    # Titel NICHT mehr zentriert
    st.markdown(
        f"<h2 style='margin-top:50px;'>{t['experience_title']}</h2>",
        unsafe_allow_html=True
    )

    for job in t["experience"]:
        st.markdown(f"""
        <div style="
            border:1px solid #ddd;
            border-radius:10px;
            padding:20px;
            margin:20px 0;
            width:100%;
            background-color:#f9f9f9;
            text-align:left;
        ">
            <h3 style="margin-bottom:5px;">{job['title']}</h3>
            <p style="margin:0;"><strong>{job['company']}</strong> | {job['period']}</p>
            <p style="margin-top:10px;">{job['description']}</p>
        </div>
        """, unsafe_allow_html=True)