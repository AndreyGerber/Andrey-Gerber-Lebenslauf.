import streamlit as st
from utils.text_loader import get_text


def show_experience():
    t = get_text(st.session_state.lang)

    # Section Title (links statt mittig)
    st.markdown(
        f"<h2 style='margin-top:50px; font-size:32px;'>{t['experience_title']}</h2>",
        unsafe_allow_html=True
    )
for job in t["experience"]:
    st.markdown(
        f"""
        <div style="
            border:1px solid #ddd;
            border-radius:10px;
            padding:25px;
            margin:25px auto;
            max-width:900px;
            background-color:#f9f9f9;
        ">

            <h3 style="
                font-size:24px;
                margin-bottom:10px;
            ">
                {job['title']}
            </h3>

            <p style="
                font-size:18px;
                margin:5px 0;
            ">
                <strong>{job['company']}</strong> | {job['period']}
            </p>

            <p style="
                font-size:18px;
                line-height:1.6;
                margin-top:10px;
            ">
                {job['description']}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )