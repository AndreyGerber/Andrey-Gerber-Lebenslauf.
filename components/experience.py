import streamlit as st

def show_experience(t):
    st.markdown("---")
    st.markdown(f"## {t['experience_title']}")

    for job in t["experience"]:
        st.markdown(
            f"""
            <div style="
                margin-bottom:25px;
                padding:15px;
                border-left:4px solid #4B0082;
                background-color:#f9f9f9;
                border-radius:8px;
            ">
                <h4 style="margin-bottom:5px;">{job['title']}</h4>
                <p style="margin:0; font-weight:600;">
                    {job['company']} | {job['period']}
                </p>
                <p style="margin-top:10px; line-height:1.5;">
                    {job['description']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )