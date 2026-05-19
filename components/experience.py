import streamlit as st
from utils.text_loader import get_text


def show_experience():
    t = get_text(st.session_state.lang)

    st.markdown(f"## {t['experience_title']}")

    for job in t["experience"]:
        html = f"""
        <div style="
            border:1px solid #ddd;
            border-radius:10px;
            padding:25px;
            margin:25px auto;
            max-width:900px;
            background-color:#f9f9f9;
        ">
            <h3 style="font-size:24px; margin-bottom:10px;">
                {job['title']}
            </h3>

            <p style="font-size:18px; margin:5px 0;">
                <strong>{job['company']}</strong> | {job['period']}
            </p>

            <p style="font-size:18px; line-height:1.6; margin-top:10px;">
                {job['description']}
            </p>
        </div>
        """

        st.markdown(html, unsafe_allow_html=True)