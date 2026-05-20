# app.py (korrigierte Version)

import streamlit as st
import os
import base64
from PIL import Image
import importlib.util
import sys

# --- PAGE CONFIG ---
st.set_page_config(page_title="Andrey Gerber - Resume", layout="wide")

# --- CACHING FUNKTIONEN (damit alles schnell lädt) ---
@st.cache_data(ttl=3600)
def load_image_cached(image_path):
    """Lädt ein Bild und cached es dauerhaft"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

@st.cache_data(ttl=3600)
def load_pil_image_cached(image_path, target_size=(900, 600), max_width=None):
    """Lädt ein PIL-Bild und cached es"""
    if not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        if max_width:
            ratio = max_width / img.size[0]
            new_size = (max_width, int(img.size[1] * ratio))
            img.thumbnail(new_size, Image.Resampling.LANCZOS)
            return img
        elif target_size:
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
            new_img.paste(img, ((target_size[0] - img.size[0]) // 2, 
                                (target_size[1] - img.size[1]) // 2))
            return new_img
        return img
    except Exception as e:
        print(f"Fehler beim Laden von {image_path}: {e}")
        return None

@st.cache_data(ttl=3600)
def load_pdf_cached(pdf_path):
    """Lädt ein PDF und cached es"""
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

@st.cache_resource
def get_certificate_list():
    """Cache für die Liste der Zertifikate"""
    cert_folder = "images"
    cert_names = [
        "1_Python_for_Data_Science", "2_Exploratory_Statistics_with_Python", "3_Data_Quality",
        "4_Data_Visualization_Matplotlib", "5_Data_Visualization_with_Seaborn", "6_Matplotlib_Complements",
        "7_DataViz_with_Plotly", "8_MCQ_Linux_and_Bash", "9_Git_and_Github", "10_Unit_Testing",
        "11_Classification_with_scikit-learn", "12_Regressionn_with_scikit_learn", "13_Methodology_in_Data_Science",
        "14_Feature_Engineering_and_Optimisation", "15_Time_Series_Analysis_with_Python",
        "16_Advanced_Classification_with-scikit-learn", "17_Text_Mining", "18_Computer_Vision_with_OpenCV",
        "19_Dense_Neural_Networks_with_Keras", "20_Convolutional_Neural_Networks_with_Keras", "21_PyTorch",
        "22_Streamlit", "23_DATA_API_Fundamentals", "24_Docker_DS"
    ]
    
    cert_data = []
    if os.path.exists(cert_folder):
        for cert_name in cert_names:
            for ext in ['.png', '.jpg', '.jpeg']:
                img_path = os.path.join(cert_folder, cert_name + ext)
                if os.path.exists(img_path):
                    img_b64 = load_image_cached(img_path)
                    if img_b64:
                        display_name = cert_name.split('_', 1)[1].replace('_', ' ')
                        cert_data.append({
                            "name": display_name,
                            "b64": img_b64,
                            "ext": ext[1:]
                        })
                    break
    return cert_data

# --- CUSTOM CSS FÜR SPRACHBUTTONS ---
st.markdown("""
<style>
.language-bar {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-bottom: 20px;
    padding: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 60px;
}
.language-bar button {
    background: rgba(255,255,255,0.2) !important;
    border: none !important;
    color: white !important;
    padding: 8px 30px !important;
    border-radius: 40px !important;
    font-size: 18px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}
.language-bar button:hover {
    background: rgba(255,255,255,0.4) !important;
    transform: translateY(-2px) !important;
}
.active-lang {
    background: white !important;
    color: #667eea !important;
}
</style>
""", unsafe_allow_html=True)

# --- SPRACHAUSWAHL ---
if 'language' not in st.session_state:
    st.session_state.language = 'de'

# Erstellt eine breite leere Spalte links und drei kleine, exakt passende Spalten rechts
cols = st.columns([7.5, 1.5, 1.5, 1.5])

with cols[1]:
    if st.button("🇩🇪 DE", key="lang_de", use_container_width=True):
        st.session_state.language = 'de'
        st.rerun()

with cols[2]:
    if st.button("🇬🇧 EN", key="lang_en", use_container_width=True):
        st.session_state.language = 'en'
        st.rerun()

with cols[3]:
    if st.button("🇷🇺 RU", key="lang_ru", use_container_width=True):
        st.session_state.language = 'ru'
        st.rerun()

st.markdown("<div style='margin-top: -10px;'></div><hr style='margin-top: 5px; margin-bottom: 10px;'>", unsafe_allow_html=True)


# --- LADE DIE AUSGEWÄHLTE SPRACHDATEI (OHNE main() AUFRUF) ---
try:
    # Pfad zur Sprachdatei
    lang_file = f"site_language/{st.session_state.language}.py"
    
    if os.path.exists(lang_file):
        # Lese die Datei
        with open(lang_file, "r", encoding="utf-8") as f:
            code = f.read()
        
        # Erstelle einen eigenen Namensraum für die Ausführung
        namespace = {
            'st': st,
            'pd': __import__('pandas'),
            'px': __import__('plotly.express'),
            'go': __import__('plotly.graph_objects'),
            'pdk': __import__('pydeck'),
            'base64': base64,
            'os': os,
            'Image': Image,
            'ImageOps': __import__('PIL.ImageOps'),
            'load_image_cached': load_image_cached,
            'load_pil_image_cached': load_pil_image_cached,
            'load_pdf_cached': load_pdf_cached,
            'get_certificate_list': get_certificate_list,
            '__name__': '__main__',
        }
        
        # Führe den Code aus (das ist dasselbe wie wenn die Datei direkt ausgeführt wird)
        exec(code, namespace)
        
    else:
        st.error(f"Sprachdatei nicht gefunden: {lang_file}")
        st.info(f"Erwarteter Pfad: {os.path.abspath(lang_file)}")
        
except Exception as e:
    st.error(f"Fehler beim Laden der Seite: {e}")
    st.info("Stelle sicher, dass die Dateien de.py, en.py und ru.py im Ordner 'site_language' existieren.")
    
    # Zeige mehr Details für debugging
    import traceback
    with st.expander("Technische Details für Debugging"):
        st.code(traceback.format_exc())