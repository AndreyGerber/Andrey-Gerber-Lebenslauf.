import streamlit as st

def show_about(t):
    
    with st.expander(t["about_title"], expanded=False):

        st.markdown(
            f"""
            <p style="
                font-size:20px;
                line-height:1.6;
                text-align:justify;
            ">
                {t['about_text']}
            </p>
            """,
            unsafe_allow_html=True
        )