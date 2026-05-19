import streamlit as st
from components.header import show_header
from components.about import show_about
from components.experience import show_experience

# Header + Sprache
t = show_header()

# About Section
show_about(t)
show_experience(t)