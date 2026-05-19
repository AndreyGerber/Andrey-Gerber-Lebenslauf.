import streamlit as st
from utils.text_loader import get_text


def show_experience():
    t = get_text(st.session_state.lang)

    # Titel
    st.markdown(f"## {t['experience_title']}")

    # Jobs durchlaufen
    for job in t["experience"]:
        with st.container():
            st.markdown(f"### {job['title']}")
            
            st.markdown(
                f"**{job['company']} | {job['period']}**"
            )
            
            st.write(job['description'])

            st.markdown("---")