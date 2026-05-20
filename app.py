import streamlit as st
from components.header import show_header
from components.about import show_about
from components.experience import show_experience
from components.career import show_career

st.set_page_config(layout="wide")

t = show_header()

show_about(t)
show_experience()
show_career()