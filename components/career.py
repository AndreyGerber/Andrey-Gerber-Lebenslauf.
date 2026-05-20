import streamlit as st
import plotly.graph_objects as go
from utils.text_loader import get_text


def show_career():
    t = get_text(st.session_state.lang)

    st.markdown(f"<h2 style='text-align: left;'>{t['career_title']}</h2>", unsafe_allow_html=True)

    jahre_alle = [1988, 1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]
    jahre_mit_raute = [1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]

    GROESSE_JAHRE = 19
    GROESSE_TEXTE = 17

    texte = t["career_timeline"]

    fig = go.Figure()

    # Linie
    fig.add_trace(go.Scatter(
        x=[1988, 2029],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=3),
        showlegend=False
    ))

    # Rauten
    fig.add_trace(go.Scatter(
        x=jahre_mit_raute,
        y=[0] * len(jahre_mit_raute),
        mode='markers',
        marker=dict(symbol='diamond', size=16, color='white',
                    line=dict(color='black', width=2)),
        showlegend=False
    ))

    # Texte
    for jahr in jahre_alle:
        fig.add_annotation(
            x=jahr,
            y=-0.1,
            text=f"<b>{jahr}</b>",
            showarrow=False,
            textangle=-30,
            font=dict(size=GROESSE_JAHRE)
        )

        fig.add_annotation(
            x=jahr,
            y=-0.25,
            text=texte.get(jahr, ""),
            showarrow=False,
            textangle=-30,
            font=dict(size=GROESSE_TEXTE, color="#4B0082")
        )

    # 🔥 Pfeil (WICHTIG!)
    fig.add_annotation(
        x=2030, y=0,
        ax=2028, ay=0,
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor="black"
    )

    # 🔥 Layout FIX (verschieben korrigiert)
    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=10, b=150),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[1985, 2035]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-1.8, 0.6]
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Navigation
    highlights = [1988, 1996, 2006, 2010, 2017, 2022]

    if 'info_idx' not in st.session_state:
        st.session_state.info_idx = 0

    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button("⬅️", key="prev"):
            st.session_state.info_idx = max(0, st.session_state.info_idx - 1)
            st.rerun()

    with col3:
        if st.button("➡️", key="next"):
            st.session_state.info_idx = min(len(highlights)-1, st.session_state.info_idx + 1)
            st.rerun()

    jahr = highlights[st.session_state.info_idx]

    # Details
    st.markdown(f"<h3>{t['career_details'][jahr]['title']}</h3>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='font-size:20px; line-height:1.6;'>{t['career_details'][jahr]['text']}</p>",
        unsafe_allow_html=True
    )