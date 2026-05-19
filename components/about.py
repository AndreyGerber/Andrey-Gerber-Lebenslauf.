import streamlit as st

def show_about(t):
    st.markdown("---")
    st.markdown(f"## {t['about_title']}")
    st.write(t["about_text"])