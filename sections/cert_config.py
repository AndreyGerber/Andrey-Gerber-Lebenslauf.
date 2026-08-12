"""
sections/cert_config.py

Zentrale, sprachunabhängige Liste der Zertifikate pro Track.
Format je Eintrag: (dateiname_ohne_endung, anzeige_name)

Wenn du ein neues Zertifikat hinzufügst: einfach hier eine Zeile ergänzen
und die passende Bilddatei in den jeweiligen Ordner legen. Kein Code
in cert_wall.py muss angefasst werden.
"""

# --- Diplome (NICHT auf der 3D-Wand, sondern später für die Zeugnis-Galerie) ---
DIPLOMA_DATA_SCIENCE = ("0_Andrey_GERBER_diploma", "Diploma: Data Science")
DIPLOMA_MLOPS = ("00_MLOps_Engineer_Diploma", "Diploma: MLOps Engineer")

# --- Track 1: Data Science ---
# Bilder liegen in: images/Data_Scientist/
CERT_DEFS_DATA_SCIENCE = (
    ("1_Python_for_Data_Science", "Python for Data Science"),
    ("2_Exploratory_Statistics_with_Python", "Exploratory Statistics with Python"),
    ("3_Data_Quality", "Data Quality"),
    ("4_Data_Visualization_Matplotlib", "Data Visualization Matplotlib"),
    ("5_Data_Visualization_with_Seaborn", "Data Visualization with Seaborn"),
    ("6_Matplotlib_Complements", "Matplotlib Complements"),
    ("7_DataViz_with_Plotly", "DataViz with Plotly"),
    ("8_MCQ_Linux_and_Bash", "MCQ Linux and Bash"),
    ("9_Git_and_Github", "Git and Github"),
    ("10_Unit_Testing", "Unit Testing"),
    ("11_Classification_with_scikit-learn", "Classification with scikit-learn"),
    ("12_Regression_with_scikit-learn", "Regression with scikit-learn"),  # Tippfehler-Fix!
    ("13_Methodology_in_Data_Science", "Methodology in Data Science"),
    ("14_Feature_Engineering_and_Optimisation", "Feature Engineering and Optimisation"),
    ("15_Time_Series_Analysis_with_Python", "Time Series Analysis with Python"),
    ("16_Advanced_Classification_with_scikit-learn", "Advanced Classification with scikit-learn"),  # Tippfehler-Fix!
    ("17_Text_Mining", "Text Mining"),
    ("18_Computer_Vision_with_OpenCV", "Computer Vision with OpenCV"),
    ("19_Dense_Neural_Networks_with_Keras", "Dense Neural Networks with Keras"),
    ("20_Convolutional_Neural_Networks_with_Keras", "Convolutional Neural Networks with Keras"),
    ("21_PyTorch", "PyTorch"),
    ("22_Streamlit", "Streamlit"),
    ("23_DATA_API_Fundamentals", "DATA API Fundamentals"),
    ("24_Docker_DS", "Docker"),
    ("25_SQL", "SQL"),
)

# --- Track 2: MLOps Engineer ---
# Bilder liegen in: images/MLOps/
CERT_DEFS_MLOPS = (
    ("01_Linux_Bash_for_MLOps", "Linux & Bash for MLOps"),
    ("02_FastAPI", "FastAPI"),
    ("03_MLFlow", "MLFlow"),
    ("04_DVC_Dagshub", "DVC & Dagshub"),
    ("05_Docker", "Docker"),
    ("06_nginx", "nginx"),
    ("07_airflow", "Airflow"),
    ("08_bentoml", "BentoML"),
    ("09_Drift_Monitoring", "Drift Monitoring"),
    ("10_Prometheus_and_Grafana", "Prometheus & Grafana"),
)