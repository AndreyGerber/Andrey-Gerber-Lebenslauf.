import streamlit as st
from utils.text_loader import get_text


def show_experience():
    t = get_text(st.session_state.lang)

    with st.expander(t["experience_title"], expanded=False):

        for job in t["experience"]:

            st.markdown(
                f"""
                <div style="
                    border:1px solid #ddd;
                    border-radius:12px;
                    padding:25px;
                    margin:25px auto;
                    max-width:900px;
                    background-color:#f9f9f9;
                ">

                    <h3 style="
                        font-size:26px;
                        margin-bottom:10px;
                        color:#222;
                    ">
                        {job['title']}
                    </h3>

                    <div style="
                        font-size:18px;
                        margin:5px 0 10px 0;
                        color:#444;
                    ">
                        <strong>{job['company']}</strong> | {job['period']}
                    </div>

                    <div style="
                        font-size:18px;
                        line-height:1.7;
                        color:#333;
                    ">
                        {job['description']}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )