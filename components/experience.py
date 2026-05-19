import streamlit as st
from utils.text_loader import get_text


def show_experience():
    t = get_text(st.session_state.lang)

    st.markdown(
        f"<h2 style='text-align: center; margin-top:50px;'>{t['experience_title']}</h2>",
        unsafe_allow_html=True
    )

    for job in t["experience"]:
        st.markdown(f"""
        <div style="
            border:1px solid #ddd;
            border-radius:10px;
            padding:20px;
            margin:20px auto;
            max-width:800px;
            background-color:#f9f9f9;
        ">
            <h3>{job['title']}</h3>
            <p><strong>{job['company']}</strong> | {job['period']}</p>
            <p>{job['description']}</p>
        </div>
        """, unsafe_allow_html=True)