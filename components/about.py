import streamlit as st

def show_about(t):
    st.markdown("---")
    st.markdown(f"## {t['about_title']}")

    st.markdown(
        f"""
        <p style="
            font-size:18px;
            line-height:1.6;
            text-align:justify;
        ">
            {t['about_text']}
        </p>
        """,
        unsafe_allow_html=True
    )