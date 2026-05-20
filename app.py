import streamlit as st
import base64
import os
from PIL import Image
import hashlib
from functools import lru_cache
import time

# --- PAGE CONFIG MUSS ALS ERSTES KOMMEN ---
st.set_page_config(page_title="Andrey Gerber - Resume", layout="wide")

# --- CACHE-FUNKTIONEN FÜR BILDER (damit sie nicht jedes Mal neu geladen werden) ---
@st.cache_data(ttl=3600, max_entries=200)
def load_image_cached(image_path):
    """Lädt ein Bild und cached es dauerhaft"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

@st.cache_data(ttl=3600, max_entries=200)
def load_pil_image_cached(image_path, target_size=None, max_width=None):
    """Lädt ein PIL-Bild und cached es"""
    if not os.path.exists(image_path):
        return None
    try:
        from PIL import Image, ImageOps
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

@st.cache_data(ttl=3600, max_entries=100)
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

# --- SPRACHAUSWAHL MIT SESSION STATE ---
if 'language' not in st.session_state:
    st.session_state.language = 'de'  # Standard: Deutsch

# Funktion zum Laden des Sprachmoduls
def load_language_module(lang_code):
    """Dynamisches Laden des Sprachmoduls"""
    if lang_code == 'de':
        from site_language import de as lang_module
    elif lang_code == 'en':
        from site_language import en as lang_module
    elif lang_code == 'ru':
        from site_language import ru as lang_module
    else:
        from site_language import de as lang_module
    return lang_module

# --- CUSTOM CSS FÜR DIE SPRACHBUTTONS (oben zentriert) ---
st.markdown("""
<style>
    /* Container für die Sprachbuttons */
    .language-switcher {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 20px;
        padding: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Sprachbutton Styling */
    .lang-btn {
        background: rgba(255,255,255,0.2);
        border: none;
        color: white;
        padding: 10px 25px;
        border-radius: 40px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .lang-btn:hover {
        background: rgba(255,255,255,0.4);
        transform: translateY(-2px);
    }
    
    .lang-btn-active {
        background: white;
        color: #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* Streamlit Button Override */
    div[data-testid="column"]:has(button) {
        display: flex;
        justify-content: center;
    }
    
    /* Ladeanimation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 400px;
        font-size: 24px;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# --- SPRACHAUSWAHL MIT 3 BUTTONS (oben zentriert) ---
st.markdown('<div class="language-switcher">', unsafe_allow_html=True)

# 3 Spalten für die Buttons (zentriert)
col_lang1, col_lang2, col_lang3, col_lang_spacer = st.columns([1, 1, 1, 3])

with col_lang1:
    if st.button("🇩🇪 Deutsch", key="lang_de", use_container_width=True):
        if st.session_state.language != 'de':
            st.session_state.language = 'de'
            st.rerun()

with col_lang2:
    if st.button("🇬🇧 English", key="lang_en", use_container_width=True):
        if st.session_state.language != 'en':
            st.session_state.language = 'en'
            st.rerun()

with col_lang3:
    if st.button("🇷🇺 Русский", key="lang_ru", use_container_width=True):
        if st.session_state.language != 'ru':
            st.session_state.language = 'ru'
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Aktive Sprache hervorheben (visuelles Feedback)
if st.session_state.language == 'de':
    st.markdown("""
    <style>
        button[key="lang_de"] {
            background: white !important;
            color: #667eea !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)
elif st.session_state.language == 'en':
    st.markdown("""
    <style>
        button[key="lang_en"] {
            background: white !important;
            color: #667eea !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)
elif st.session_state.language == 'ru':
    st.markdown("""
    <style>
        button[key="lang_ru"] {
            background: white !important;
            color: #667eea !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Kleiner Abstand nach den Buttons
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# --- LADE DAS AUSGEWÄHLTE SPRACHMODUL ---
try:
    lang_module = load_language_module(st.session_state.language)
    
    # Wenn das Modul eine main() Funktion hat, rufe sie auf
    if hasattr(lang_module, 'main'):
        # Übergebe die gecachten Funktionen an das Sprachmodul
        lang_module.main(
            load_image_cached=load_image_cached,
            load_pil_image_cached=load_pil_image_cached,
            load_pdf_cached=load_pdf_cached,
            get_certificate_list=get_certificate_list
        )
    else:
        # Fallback: Führe das Modul direkt aus (wie ein normales Skript)
        # Aber mit injizierten gecachten Funktionen
        # Wir setzen die Funktionen im globalen Namespace des Moduls
        import sys
        if st.session_state.language == 'de':
            from site_language import de
            de.load_image_cached = load_image_cached
            de.load_pil_image_cached = load_pil_image_cached
            de.load_pdf_cached = load_pdf_cached
            de.get_certificate_list = get_certificate_list
            # Führe den Code aus (das Modul hat bereits seinen eigenen Code)
        elif st.session_state.language == 'en':
            from site_language import en
            en.load_image_cached = load_image_cached
            en.load_pil_image_cached = load_pil_image_cached
            en.load_pdf_cached = load_pdf_cached
            en.get_certificate_list = get_certificate_list
        elif st.session_state.language == 'ru':
            from site_language import ru
            ru.load_image_cached = load_image_cached
            ru.load_pil_image_cached = load_pil_image_cached
            ru.load_pdf_cached = load_pdf_cached
            ru.get_certificate_list = get_certificate_list
            
except Exception as e:
    st.error(f"Fehler beim Laden der Sprachdatei: {e}")
    st.info("Bitte stelle sicher, dass der Ordner 'site_language' existiert und die Dateien de.py, en.py und ru.py enthält.")