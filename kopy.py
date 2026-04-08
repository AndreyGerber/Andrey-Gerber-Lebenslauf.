#2D-Lösung

import streamlit as st
import os
import base64

def get_base64_img(file_path):
    """Konvertiert lokale Bilder in Base64, um Pfadprobleme in Streamlit zu vermeiden."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def st_certificate_wall(image_folder="images"):
    """Erzeugt eine gekrümmte 2D-Wand mit 3D-Effekt in Reihen (20% Überlappung)."""
    if not os.path.exists(image_folder):
        st.error(f"Ordner '{image_folder}' nicht gefunden.")
        return

    # Deine spezifischen Zertifikatsdateien (17 Stück)
    cert_filenames = [
        "1_Python_for_Data_Science.jpg",
        "2_Exploratory_Statistics_with_Python.jpg",
        "3_Data_Quality.jpg",
        "4_Data_Visualization_Matplotlib.jpg",
        "5_Data_Visualization_with_Seaborn.jpg",
        "6_Matplotlib_Complements.jpg",
        "7_DataViz_with_Plotly.jpg",
        "8_MCQ_Linux_and_Bash.jpg",
        "9_Git_and_Github.jpg",
        "10_Unit_Testing.jpg",
        "11_Classification_with_scikit-learn.jpg",
        "12_Regression_with_scikit-learn.jpg",
        "13_Methodology_in_Data_Science.jpg",
        "14_Feature_Engineering_and_Optimisation.jpg",
        "15_Time_Series_Analysis_with_Python.jpg",
        "16_Advanced_Classification_with_scikit-learn.jpg",
        "17_Text_Mining.jpg"
    ]
    
    # Nur existierende Bilder filtern
    valid_certs = []
    for filename in cert_filenames:
        img_path = os.path.join(image_folder, filename)
        if os.path.exists(img_path):
            valid_certs.append(filename)
    
    if not valid_certs:
        st.error("Keine der angegebenen Bilder gefunden.")
        return

    # 2 Reihen: erste Reihe 9 Bilder, zweite Reihe 8 Bilder
    row1 = valid_certs[:9]
    row2 = valid_certs[9:]
    rows_list = [row1, row2]
    
    # CSS mit hellem Hintergrund und Überlappung
    html_content = """
    <style>
        .main-wall {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8edf5 100%);
            padding: 60px 0;
            display: flex;
            flex-direction: column;
            gap: 60px;
            align-items: center;
            overflow: visible;
            border-radius: 20px;
        }
        .row-container {
            display: flex;
            perspective: 1200px;
            justify-content: center;
            width: 100%;
        }
        .cert-card {
            width: 150px;
            height: auto;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            box-shadow: -3px 8px 15px rgba(0,0,0,0.15);
            cursor: pointer;
            z-index: 1;
            border-radius: 8px;
            background: white;
            border: 2px solid #e0e6ed;
        }
        
        /* Jedes Bild überlappt das nächste um 20% (30px bei 150px Breite) */
        .row-container .cert-card {
            margin-left: -30px;
        }
        
        /* Erstes Bild in der Reihe hat keinen negativen Margin links */
        .row-container .cert-card:first-child {
            margin-left: 0;
        }
        
        /* Hover-Effekt: 1.5x Vergrößerung + nach vorne */
        .cert-card:hover {
            transform: scale(3.5) rotateY(0deg) translateZ(80px) !important;
            z-index: 100;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            margin: 0 20px !important;
            border-color: #4a90e2;
        }
        
        /* Korrigiert die Margin beim Hover für alle Bilder */
        .row-container .cert-card:hover {
            margin-left: 20px !important;
            margin-right: 20px !important;
        }
        
        .cert-caption {
            text-align: center;
            font-size: 10px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #2c3e50;
            padding: 5px;
            background: rgba(255,255,255,0.9);
            border-radius: 0 0 8px 8px;
            margin-top: -4px;
            max-width: 150px;
            word-break: break-word;
        }
    </style>
    <div class="main-wall">
    """

    for row_idx, row in enumerate(rows_list):
        html_content += '<div class="row-container">'
        mid = (len(row) - 1) / 2
        
        for i, filename in enumerate(row):
            b64_data = get_base64_img(os.path.join(image_folder, filename))
            if b64_data:
                # Anzeigename ohne Nummer und Endung
                display_name = filename.split('_', 1)[1].replace('.jpg', '').replace('.png', '').replace('_', ' ')
                
                # Krümmung berechnen (sanfter für besseren Effekt)
                rotation = (mid - i) * 8
                
                html_content += f'''
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <img src="data:image/jpeg;base64,{b64_data}" 
                         class="cert-card" 
                         style="transform: rotateY({rotation}deg);" 
                         title="{display_name}">
                    <div class="cert-caption">{display_name}</div>
                </div>
                '''
        html_content += '</div>'

    html_content += """
    </div>
    
    <script>
    const images = document.querySelectorAll('.cert-card');
    images.forEach(img => {
        img.addEventListener('click', function() {
            const modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0,0,0,0.85)';
            modal.style.zIndex = '10000';
            modal.style.display = 'flex';
            modal.style.justifyContent = 'center';
            modal.style.alignItems = 'center';
            modal.style.cursor = 'pointer';
            
            const modalImg = document.createElement('img');
            modalImg.src = this.src;
            modalImg.style.maxWidth = '85%';
            modalImg.style.maxHeight = '85%';
            modalImg.style.borderRadius = '12px';
            modalImg.style.boxShadow = '0 0 40px rgba(0,0,0,0.5)';
            
            modal.appendChild(modalImg);
            document.body.appendChild(modal);
            
            modal.onclick = function() {
                document.body.removeChild(modal);
            };
        });
    });
    </script>
    """
    
    # Anzeige in Streamlit
    st.components.v1.html(html_content, height=900, scrolling=True)

# --- App Aufruf ---
st.set_page_config(page_title="Lebenslauf Zertifikate", layout="wide")

# Titel mit Smiley
st.header("🐍 ob ich programmieren kann... 👨‍💻")

st_certificate_wall()

st.markdown("<br>" * 3, unsafe_allow_html=True)  # Drei Umbrüche