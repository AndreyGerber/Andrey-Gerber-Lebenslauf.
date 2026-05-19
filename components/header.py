import streamlit as st
from utils.text_loader import get_text

def show_header(lang):
    st.markdown(
        f"<h2 style='text-align: center;'>{get_text('welcome', lang)}</h2>",
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"<h1 style='text-align: center; color: #4B0082;'>{get_text('title', lang)}</h1>",
        unsafe_allow_html=True
    )
    
    st.divider()