import streamlit as st
from components.header import show_header

st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# Header laden
t = show_header()

# Beispiel Nutzung
st.write("Hier geht der Rest deiner App weiter...")


