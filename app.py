
import streamlit as st
import plotly.express as px
import pandas as pd

import os

# Seiteneinstellungen
st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# 1. Titel (zentriert und zwei Zeilen)
st.markdown("<h2 style='text-align: center;'>Willkommen auf der Seite</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #4B0082;'>Lebenslauf von Andrey Gerber</h1>", unsafe_allow_html=True)
st.divider()


from PIL import Image, ImageOps

# --- 1. FUNKTION FÜR STABILE BILDGRÖSSE ---
def lade_formatiertes_bild(name, target_size=(900, 600)):
    base_path = os.path.dirname(__file__)
    pfad = os.path.join(base_path, "images", name)
    if os.path.exists(pfad):
        img = Image.open(pfad)
        # Erstellt ein Bild mit festem Format, ohne es zu verzerren (Padding)
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        # Erzeugt einen transparenten Hintergrund in der Zielgröße
        new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
        # Zentriert das Bild auf dem Hintergrund
        new_img.paste(img, ((target_size[0] - img.size[0]) // 2, 
                            (target_size[1] - img.size[1]) // 2))
        return new_img
    return None

# --- 2. DATEN & LOGIK ---
if 'bild_index' not in st.session_state:
    st.session_state.bild_index = 0

slideshow_bilder = ["ich1.JPG", "ich_pass.png"]
zeichnung_name = "itsme2.png"

# --- 3. LAYOUT: 3 SPALTEN ---
col_bild, col_mitte, col_daten = st.columns([1.5, 1.0, 1.5])

with col_bild:
    # Stabiles Bild laden
    aktuelles_foto = lade_formatiertes_bild(slideshow_bilder[st.session_state.bild_index])
    if aktuelles_foto:
        st.image(aktuelles_foto, use_container_width=True)
    else:
        st.error(f"Datei fehlt: {slideshow_bilder[st.session_state.bild_index]}")


    p_links, p_mitte, p_rechts = st.columns([1, 4, 1]) 
    
    with p_links:
        if st.button("⬅️"):
            st.session_state.bild_index = (st.session_state.bild_index - 1) % len(slideshow_bilder)
            st.rerun()
            
    with p_rechts:
        if st.button("➡️"):
            st.session_state.bild_index = (st.session_state.bild_index + 1) % len(slideshow_bilder)
            st.rerun()

with col_mitte:
    # Deine Zeichnung laden (ebenfalls formatiert für Stabilität)
    zeichnung = lade_formatiertes_bild(zeichnung_name, target_size=(300, 300))
    if zeichnung:
        st.image(zeichnung, use_container_width=True)
    else:
        st.info("Hier erscheint bald deine Zeichnung...")

with col_daten:
    # Anpassung: Schriftgröße deutlich vergrößert
    st.markdown("<h3 style='font-size: 26px;'>Meine Kontaktdaten</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'><strong>Name:</strong> Andrey Gerber</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'>📞 <strong>0176 43 733 099</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'>📧 <a href='mailto:andrey.gerber.88@gmail.com'>andrey.gerber.88@gmail.com</a></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 22px;'><strong>Wohnadresse:</strong> Brauchst du nicht, ruf an oder @</p>", unsafe_allow_html=True)


st.divider()

# ... hier geht es weiter mit deinem "Mein Weg" (Flaggen) und der Timeline







import streamlit as st
import plotly.graph_objects as go

# --- 1. DATENKONFIGURATION ---
# Alle Jahre für die Beschriftung
jahre_alle = [1988, 1996, 2006, 2010, 2017, 2019, 2022, 2026]
# Jahre, die eine Raute auf der Linie erhalten (alle außer 1988)
jahre_mit_raute = [1996, 2006, 2010, 2017, 2019, 2022, 2026]

# Hier kannst du deine Texte für die Blöcke definieren
texte = {
    1988: "Geburt in UdSSR",
    1996: "Schulzeit Russland",
    2006: "Emigration DE",
    2010: "mein Text",
    2017: "mein Text",
    2019: "mein Text",
    2022: "Hausbau",
    2026: "Zukunft"
}

# Design-Einstellungen
LINIEN_DICKE = 3
STARTSTRICH_LAENGE = 0.25
JAHR_SCHRIFTGROESSE = 16

# Titel linksbündig
st.markdown("<h2 style='text-align: left;'>Mein Werdegang</h2>", unsafe_allow_html=True)

# --- 2. GRAFIK ERSTELLEN ---
fig = go.Figure()

# Lebenslinie: Durchgehend von 1988 bis kurz vor die Pfeilspitze (2034)
fig.add_trace(go.Scatter(
    x=[1988, 2028], 
    y=[0, 0],
    mode='lines',
    line=dict(color='black', width=LINIEN_DICKE),
    showlegend=False, 
    hoverinfo='none'
))

# Senkrechter Startstrich bei 1988
fig.add_shape(
    type="line", 
    x0=1988, y0=-STARTSTRICH_LAENGE, 
    x1=1988, y1=STARTSTRICH_LAENGE,
    line=dict(color="black", width=LINIEN_DICKE + 1)
)

# Weiße Rauten (NUR ab 1996), mittig auf der Linie
fig.add_trace(go.Scatter(
    x=jahre_mit_raute, 
    y=[0] * len(jahre_mit_raute),
    mode='markers',
    marker=dict(
        symbol='diamond', 
        size=22, 
        color='white', 
        line=dict(color='black', width=2)
    ),
    showlegend=False, 
    hoverinfo='none'
))

# Jahreszahlen und Textblöcke (45° gedreht)
for jahr in jahre_alle:
    # Das Jahr (fett)
    fig.add_annotation(
        x=jahr, y=-0.1, 
        text=f"<b>{jahr}</b>",
        showarrow=False, 
        textangle=-25,
        font=dict(size=JAHR_SCHRIFTGROESSE, color="black"),
        xanchor="right", 
        yanchor="top"
    )
    # Der individuelle Textblock darunter
    fig.add_annotation(
        x=jahr, y=-0.2, 
        text=texte.get(jahr, "mein Text"),
        showarrow=False, 
        textangle=-25,
        font=dict(size=12, color="gray"),
        xanchor="right", 
        yanchor="top"
    )

# Pfeilspitze am rechten Ende
fig.add_annotation(
    x=2030, y=0,           # Spitze
    ax=2028, ay=0,         # Ende der Linie
    xref="x", yref="y", 
    axref="x", ayref="y",
    showarrow=True, 
    arrowhead=2, 
    arrowsize=1.5, 
    arrowwidth=LINIEN_DICKE, 
    arrowcolor="black"
)

# Layout-Anpassung für die schrägen Texte
fig.update_layout(
    height=450, 
    margin=dict(l=0, r=0, t=10, b=150),
    xaxis=dict(
        showgrid=False, 
        zeroline=False, 
        showticklabels=False, 
        range=[1985, 2035] # Genug Platz links und rechts
    ),
    yaxis=dict(
        showgrid=False, 
        zeroline=False, 
        showticklabels=False, 
        range=[-1.8, 0.6] # Platz für die schrägen Texte nach unten
    ),
    plot_bgcolor="rgba(0,0,0,0)", 
    paper_bgcolor="rgba(0,0,0,0)"
)

# Anzeige in Streamlit
st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True, 'displayModeBar': False})











