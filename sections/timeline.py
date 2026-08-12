"""
sections/timeline.py

Werdegang-Bereich: die Plotly-Zeitstrahl-Grafik (render_timeline_graph)
und die sechs interaktiven Jahres-Detailblöcke (render_timeline_details).

Performance-Hinweis:
Die Back/Next-Buttons stecken in einem @st.fragment - ein Klick rerennt
nur diesen Block, nicht die komplette Seite.
"""

import os
import streamlit as st
import plotly.graph_objects as go

from utils.loaders import load_pil_image_cached, load_image_base64_cached

IMAGES_FOLDER = "images"

YEARS_ALL = [1988, 1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]
YEARS_WITH_DIAMOND = [1991, 1996, 2006, 2010, 2017, 2019, 2022, 2026]
YEAR_TEXT_KEYS = {
    1988: "tl_year_1988", 1991: "tl_year_1991", 1996: "tl_year_1996",
    2006: "tl_year_2006", 2010: "tl_year_2010", 2017: "tl_year_2017",
    2019: "tl_year_2019", 2022: "tl_year_2022", 2026: "tl_year_2026",
}

SIZE_YEARS = 19
SIZE_TEXTS = 17
LINE_WIDTH = 3
START_TICK_LENGTH = 0.18

HIGHLIGHT_YEARS = [1988, 1996, 2006, 2010, 2017, 2022, 2026]
BLOCK_HEIGHT = 750


# ---------------------------------------------------------------- GRAFIK ---
def render_timeline_graph(t: dict):
    st.markdown(f"<h2 style='text-align: left;'>{t['tl_section_title']}</h2>", unsafe_allow_html=True)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[1988, 2029], y=[0, 0], mode='lines',
        line=dict(color='black', width=LINE_WIDTH),
        showlegend=False, hoverinfo='none'
    ))

    fig.add_shape(
        type="line", x0=1988, y0=-START_TICK_LENGTH, x1=1988, y1=START_TICK_LENGTH,
        line=dict(color="black", width=LINE_WIDTH + 1)
    )

    fig.add_trace(go.Scatter(
        x=YEARS_WITH_DIAMOND, y=[0] * len(YEARS_WITH_DIAMOND), mode='markers',
        marker=dict(symbol='diamond', size=16, color='white', line=dict(color='black', width=2)),
        showlegend=False, hoverinfo='none'
    ))

    for jahr in YEARS_ALL:
        fig.add_annotation(
            x=jahr, y=-0.1, text=f"<b>{jahr}</b>", showarrow=False, textangle=-30,
            font=dict(size=SIZE_YEARS, color="black"), xanchor="center", yanchor="top"
        )
        fig.add_annotation(
            x=jahr, y=-0.22, text=t.get(YEAR_TEXT_KEYS[jahr], ""), showarrow=False, textangle=-30,
            font=dict(size=SIZE_TEXTS, color="#4B0082"), xanchor="right", yanchor="top"
        )

    fig.add_annotation(
        x=2030, y=0, ax=2028, ay=0, xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=LINE_WIDTH, arrowcolor="black"
    )

    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=10, b=150),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[1985, 2035]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.8, 0.6]),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True, 'displayModeBar': False})


# --------------------------------------------------------- DETAIL-BLÖCKE ---
def _render_1988(t: dict):
    st.markdown(f"<h3 style='text-align: left;'>{t['tl_1988_heading']}</h3>", unsafe_allow_html=True)
    scale = 0.8
    img_b64 = load_image_base64_cached(os.path.join(IMAGES_FOLDER, "tscherlak_map.png"))
    if img_b64:
        st.markdown(f"""
            <div style="width: {int(scale * 100)}%; margin: auto;">
                <div style="position: relative; display: inline-block; width: 100%;">
                    <img src="data:image/png;base64,{img_b64}" style="width: 100%; display: block; border-radius: 10px;">
                    <div style="position: absolute; top: 45.3%; left: 89.8%; transform: translate(-50%, -100%);
                                font-size: 40px; filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.5)); z-index: 999;">📍</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Datei fehlt: images/tscherlak_map.png")


def _render_1996(t: dict):
    scale = 1.2
    col_text, col_foto = st.columns([1, 2.5])
    with col_text:
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: left;'>{t['tl_1996_heading']}</h3>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 24px; color: #0055A5;'>{t['tl_1996_text']}</p>", unsafe_allow_html=True)
    with col_foto:
        img = load_pil_image_cached(os.path.join(IMAGES_FOLDER, "schule2.png"))
        if img:
            st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
            st.image(img, width=int(img.size[0] * scale))
        else:
            st.error("Bild 'schule2.png' nicht gefunden.")


def _render_2006(t: dict):
    st.markdown(f"<h3 style='text-align: left;'>{t['tl_2006_heading']}</h3>", unsafe_allow_html=True)
    st.divider()

    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=[73.32, 13.40], lat=[54.98, 52.52], mode='markers+text',
        text=["Omsk", "Berlin"], textposition="bottom center",
        textfont=dict(size=16, color="black", family="Arial Black"),
        marker=dict(size=14, color='#FF4B4B', line=dict(width=2, color='white')),
        hoverinfo='none'
    ))
    fig.add_trace(go.Scattergeo(
        lon=[73.32, 13.40], lat=[54.98, 52.52], mode='lines',
        line=dict(width=3, color='#FF4B4B'), hoverinfo='none'
    ))
    fig.add_annotation(x=14.8, y=52.7, text="✈️", showarrow=False, font=dict(size=50), textangle=-140, xref="x", yref="y")
    fig.update_layout(
        height=550, margin=dict(l=0, r=0, t=10, b=0),
        geo=dict(
            projection_type='equirectangular',
            showland=True, landcolor="#F0F2F6",
            showocean=True, oceancolor="#E8F4F9",
            showcountries=True, countrycolor="white",
            lataxis=dict(range=[45, 65], showgrid=False),
            lonaxis=dict(range=[5, 85], showgrid=False),
            resolution=50,
        ),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, key="flight_landing")


def _render_2010(t: dict):
    scale = 1.0
    col_text, col_foto = st.columns([1, 2.5])
    with col_text:
        st.markdown(f"<h3 style='text-align: left;'>{t['tl_2010_heading']}</h3>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 24px; color: #0055A5; line-height: 1.4;'>{t['tl_2010_text']}</p>", unsafe_allow_html=True)
    with col_foto:
        img = load_pil_image_cached(os.path.join(IMAGES_FOLDER, "haw.png"))
        if img:
            st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
            st.image(img, width=int(img.size[0] * scale))
        else:
            st.error("Bild 'haw.png' konnte nicht geladen werden.")


def _render_2017(t: dict):
    scale = 1.15
    col_text, col_foto = st.columns([1, 1.8])
    with col_text:
        st.markdown(f"<h3 style='text-align: left;'>{t['tl_2017_heading']}</h3>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
            <p style='font-size: 24px; color: #0055A5; margin-bottom: 5px;'><strong>{t['tl_2017_role1_title']}</strong></p>
            <ul style='font-size: 20px; color: #333; line-height: 1.6;'>{t['tl_2017_role1_bullets']}</ul>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <p style='font-size: 24px; color: #0055A5; margin-top: 20px; margin-bottom: 5px;'><strong>{t['tl_2017_role2_title']}</strong></p>
            <ul style='font-size: 20px; color: #333; line-height: 1.6;'>{t['tl_2017_role2_bullets']}</ul>
        """, unsafe_allow_html=True)
    with col_foto:
        img = load_pil_image_cached(os.path.join(IMAGES_FOLDER, "tuev.png"))
        if img:
            st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
            st.image(img, width=int(img.size[0] * scale))
        else:
            st.error("Datei 'images/tuev.png' nicht gefunden.")


def _render_2022(t: dict):
    scale = 1.15
    col_text, col_foto = st.columns([1, 1.8])
    with col_text:
        st.markdown(f"<h3 style='text-align: left;'>{t['tl_2022_heading']}</h3>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
            <p style='font-size: 24px; color: #0055A5; margin-bottom: 5px;'><strong>{t['tl_2022_role_title']}</strong></p><br>
            <ul style='font-size: 20px; color: #333; line-height: 1.6;'>{t['tl_2022_role_bullets']}</ul>
        """, unsafe_allow_html=True)
    with col_foto:
        img = load_pil_image_cached(os.path.join(IMAGES_FOLDER, "ferchau.png"))
        if img:
            st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
            st.image(img, width=int(img.size[0] * scale))
        else:
            st.error("Datei 'images/ferchau.png' nicht gefunden.")


def _render_2026(t: dict):
    scale = 1.15
    col_text, col_foto = st.columns([1, 1.8])
    with col_text:
        st.markdown(f"<h3 style='text-align: left;'>{t['tl_2026_heading']}</h3>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
            <p style='font-size: 24px; color: #0055A5; margin-bottom: 5px;'><strong>{t['tl_2026_role_title']}</strong></p><br>
            <ul style='font-size: 20px; color: #333; line-height: 1.6;'>{t['tl_2026_bullets']}</ul>
        """, unsafe_allow_html=True)
    with col_foto:
        img = load_pil_image_cached(os.path.join(IMAGES_FOLDER, "liora.png"))
        if img:
            st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
            st.image(img, width=int(img.size[0] * scale))
        else:
            st.error("Datei 'images/liora.png' nicht gefunden.")


_RENDERERS = {
    1988: _render_1988, 1996: _render_1996, 2006: _render_2006,
    2010: _render_2010, 2017: _render_2017, 2022: _render_2022,
    2026: _render_2026,
}


@st.fragment
def render_timeline_details(t: dict):
    if "tl_info_idx" not in st.session_state:
        st.session_state.tl_info_idx = 0

    c_nav1, c_nav2, c_nav3 = st.columns([1, 4, 1])
    with c_nav1:
        if st.button(t["tl_nav_back"], key="tl_nav_prev", disabled=(st.session_state.tl_info_idx == 0)):
            st.session_state.tl_info_idx -= 1
            st.rerun(scope="fragment")
    with c_nav3:
        if st.button(t["tl_nav_next"], key="tl_nav_next", disabled=(st.session_state.tl_info_idx == len(HIGHLIGHT_YEARS) - 1)):
            st.session_state.tl_info_idx += 1
            st.rerun(scope="fragment")

    with st.container(height=BLOCK_HEIGHT, border=True):
        jahr_aktiv = HIGHLIGHT_YEARS[st.session_state.tl_info_idx]
        _RENDERERS[jahr_aktiv](t)