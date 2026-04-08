import streamlit as st
import plotly.graph_objects as go
import os, base64
from PIL import Image

# =========================================
# CONFIG
# =========================================
st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# =========================================
# STATE MANAGEMENT
# =========================================
if "timeline_selected" not in st.session_state:
    st.session_state.timeline_selected = 1988

if "bild_index" not in st.session_state:
    st.session_state.bild_index = 0

# =========================================
# UTILS
# =========================================
@st.cache_data
def lade_formatiertes_bild(name, target_size=(900, 600)):
    pfad = os.path.join("images", name)
    if not os.path.exists(pfad) or pfad.lower().endswith(".pdf"):
        return None
    try:
        img = Image.open(pfad)
        if img.mode != "RGB":
            img = img.convert("RGB")

        img.thumbnail(target_size)
        new_img = Image.new("RGBA", target_size, (255,255,255,0))
        new_img.paste(img, ((target_size[0]-img.size[0])//2,
                            (target_size[1]-img.size[1])//2))
        return new_img
    except:
        return None


def get_pdf_base64(file):
    path = os.path.join("documents", file)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# =========================================
# HEADER
# =========================================
def render_header():
    st.markdown("<h2 style='text-align:center;'>Willkommen auf der Seite</h2>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;color:#4B0082;'>Lebenslauf von Andrey Gerber</h1>", unsafe_allow_html=True)
    st.divider()

# =========================================
# PROFIL
# =========================================
def render_profil():
    bilder = ["ich1.JPG", "ich_pass.png", "aufenthaltstitel.png"]

    col1, col2, col3 = st.columns([1.5,1,1.5])

    with col1:
        img = lade_formatiertes_bild(bilder[st.session_state.bild_index])
        if img:
            st.image(img, use_container_width=True)

        c1,_,c2 = st.columns([1,3,1])

        with c1:
            if st.button("⬅️"):
                st.session_state.bild_index = (st.session_state.bild_index-1) % len(bilder)
                st.rerun()

        with c2:
            if st.button("➡️"):
                st.session_state.bild_index = (st.session_state.bild_index+1) % len(bilder)
                st.rerun()

    with col2:
        img = lade_formatiertes_bild("itsme2.png",(300,300))
        if img:
            st.image(img)

    with col3:
        st.markdown("## Andrey Gerber")
        st.markdown("📞 0176 43 733 099")
        st.markdown("📧 andrey.gerber.88@gmail.com")

# =========================================
# TIMELINE (KLICKBAR!)
# =========================================
def render_timeline():

    jahre = [1988, 1991, 1996, 2006, 2010, 2017, 2019, 2022]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=jahre,
        y=[0]*len(jahre),
        mode='markers+lines',
        marker=dict(size=12)
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=0,r=0,t=0,b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(visible=False)
    )

    # 👉 Klick-Logik
    selected = st.plotly_chart(fig, use_container_width=True, key="timeline", on_select="rerun")

    # Workaround: Buttons unter Timeline (zuverlässiger als Plotly click)
    cols = st.columns(len(jahre))

    for i, jahr in enumerate(jahre):
        with cols[i]:
            if st.button(str(jahr)):
                # 👉 deine Sonderlogik
                if jahr == 1991:
                    return
                if jahr in [2017, 2019, 2022]:
                    st.session_state.timeline_selected = 2017
                else:
                    st.session_state.timeline_selected = jahr
                st.rerun()

# =========================================
# DETAIL SECTIONS
# =========================================
def render_details():

    jahr = st.session_state.timeline_selected

    st.divider()

    # ======================
    if jahr == 1988:
        st.subheader("📍 1988: Hier begann meine Reise")

    # ======================
    elif jahr == 1996:
        st.subheader("🎒 1996: Schulzeit")
        st.markdown("So schnell vergehen 10 Jahre.")

    # ======================
    elif jahr == 2006:
        st.subheader("✈️ 2006: Der neue Lebensabschnitt beginnt")

    # ======================
    elif jahr == 2010:
        st.subheader("🎓 2010: Studium")

    # ======================
    elif jahr == 2017:
        st.subheader("🛠️ 2017 – 2022: TÜV Rheinland")

# =========================================
# PDF SECTION
# =========================================
def render_pdf():

    docs = [
        "Namensaenderung.pdf",
        "Bachelor.pdf",
        "Master.pdf"
    ]

    if "doc" not in st.session_state:
        st.session_state.doc = docs[0]

    col1, col2 = st.columns([1,2])

    with col1:
        for d in docs:
            if st.button(d):
                st.session_state.doc = d

    with col2:
        pdf = get_pdf_base64(st.session_state.doc)
        if pdf:
            st.markdown(
                f'<iframe src="data:application/pdf;base64,{pdf}" width="100%" height="800px"></iframe>',
                unsafe_allow_html=True
            )

# =========================================
# MAIN
# =========================================
render_header()
render_profil()
render_timeline()
render_details()
render_pdf()