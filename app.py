import streamlit as st
import plotly.express as px
import pandas as pd

# Seiteneinstellungen
st.set_page_config(page_title="Lebenslauf Andrey Gerber", layout="wide")

# 1. Header & Kontakt
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://placeholder.com", caption="Slideshow: it's me") # Hier später dein Bild-Pfad

with col2:
    st.title("Willkommen auf der Seite")
    st.header("Lebenslauf von Andrey Gerber")
    st.write("**Name:** Andrey Gerber")
    st.write("**Wohnadresse:** Brauchst du nicht, ruf an oder @")
    st.write("📞 0176 43 733 099")
    st.write("📧 andrey.gerber.88@gmail.com")

st.divider()

# 2. Wohnort-Fahnen (UdSSR -> Russland -> Deutschland)
st.subheader("Mein Weg")
f1, p1, f2, p2, f3 = st.columns([1, 0.5, 1, 0.5, 1])
with f1: st.metric("1988", "UdSSR ☭")
with p1: st.markdown("## ➔")
with f2: st.metric("1991", "Russland 🇷🇺")
with p2: st.markdown("## ➔")
with f3: st.metric("2006", "Deutschland 🇩🇪")

st.divider()

# 3. Hobby-Timeline mit Plotly
st.subheader("Hobbys & Aktivitäten")

# Daten für die Zeitachse aufbereiten
data = [
    dict(Hobby="Schach", Start='1996-01-01', Ende='2026-01-01', Typ="Kontinuierlich"),
    dict(Hobby="Eishockey", Start='1998-01-01', Ende='2006-01-01', Typ="Kontinuierlich"),
    dict(Hobby="Yoga", Start='2018-01-01', Ende='2026-01-01', Typ="Kontinuierlich"),
    # Fußball mit Pause
    dict(Hobby="Fussball", Start='1997-01-01', Ende='2008-01-01', Typ="Aktiv"),
    dict(Hobby="Fussball", Start='2008-01-01', Ende='2020-01-01', Typ="Pause (Striche)"),
    dict(Hobby="Fussball", Start='2020-01-01', Ende='2026-01-01', Typ="Wieder aktiv")
]

df = pd.DataFrame(data)

# Farben definieren
colors = {"Kontinuierlich": "#31333F", "Aktiv": "#0068C9", "Pause (Striche)": "#D3D3D3", "Wieder aktiv": "#0068C9"}

fig = px.timeline(df, x_start="Start", x_end="Ende", y="Hobby", color="Typ", 
                  color_discrete_map=colors, template="plotly_white")

fig.update_yaxes(autorange="reversed") # Damit Schach oben steht
fig.update_layout(showlegend=False, height=300)

st.plotly_chart(fig, use_container_width=True)

st.info("💡 Fussball: play (not drink in stadium)")