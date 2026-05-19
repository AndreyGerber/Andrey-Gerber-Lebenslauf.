import streamlit as st
from components.header import show_header
from components.about import show_about

# Header + Sprache
t = show_header()

# About Section
show_about(t)