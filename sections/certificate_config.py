"""
sections/certificate_config.py

Zentrale, sprachunabhängige Liste der Dokumente für die Zeugnis-Galerie.
Jeder Eintrag verknüpft: PDF-Dateiname (in documents/), Vorschaubild-Pfad,
Icon und einen Übersetzungs-Key für die Beschriftung.

Die zwei Diplome (Data Science & MLOps) verweisen bewusst direkt auf die
Bilder, die schon in images/Data_Scientist/ bzw. images/MLOps/ liegen -
keine Notwendigkeit, sie zusätzlich nach images/Zertifikate/ zu kopieren.
"""

DOCUMENTS_FOLDER = "documents"

TOP_DOCUMENT = {
    "pdf": "Namensaenderung.pdf",
    "image": "images/Zertifikate/NamensaenderungAG.jpg",
    "icon": "📝",
    "label_key": "cert_gallery_label_namensaenderung",
}

OTHER_DOCUMENTS = [
    {"pdf": "Berufsschule.pdf", "image": "images/Zertifikate/Berufsschule.jpg", "icon": "⚒️", "label_key": "cert_gallery_label_berufsschule"},
    {"pdf": "allgemeineHochschulreife.pdf", "image": "images/Zertifikate/Abitur.jpg", "icon": "📜", "label_key": "cert_gallery_label_abitur"},
    {"pdf": "Praktikum_V&F.pdf", "image": "images/Zertifikate/Praktikum_V_F.jpg", "icon": "🔧", "label_key": "cert_gallery_label_praktikum"},
    {"pdf": "Bachelor.pdf", "image": "images/Zertifikate/Bachelor.jpg", "icon": "✈️", "label_key": "cert_gallery_label_bachelor"},
    {"pdf": "Schweisskurs.pdf", "image": "images/Zertifikate/schweißkurs.jpg", "icon": "👨‍🏭", "label_key": "cert_gallery_label_schweisskurs"},
    {"pdf": "Wertanalytiker.pdf", "image": "images/Zertifikate/Wertanalytiker.jpg", "icon": "💎", "label_key": "cert_gallery_label_wertanalytiker"},
    {"pdf": "Master.pdf", "image": "images/Zertifikate/Master.jpg", "icon": "🎓", "label_key": "cert_gallery_label_master"},
    {"pdf": "b_k_pulse.pdf", "image": "images/Zertifikate/B_K_pulse.jpg", "icon": "📟", "label_key": "cert_gallery_label_bk_pulse"},
    {"pdf": "M_BBM.pdf", "image": "images/Zertifikate/M_BBM.jpg", "icon": "🔊", "label_key": "cert_gallery_label_mbbm"},
    {"pdf": "Interner_Auditor.pdf", "image": "images/Zertifikate/Auditor9001.jpg", "icon": "🕵️", "label_key": "cert_gallery_label_auditor"},
    {"pdf": "Qualitätsbeauftragter.pdf", "image": "images/Zertifikate/QMB9001.jpg", "icon": "🛡️", "label_key": "cert_gallery_label_qmb9001"},
    {"pdf": "QMB_ISO_17025.pdf", "image": "images/Zertifikate/QMB17025.jpg", "icon": "🛡️", "label_key": "cert_gallery_label_qmb17025"},
    {"pdf": "Data_Science.pdf", "image": "images/Zertifikate/Data_Science.jpg", "icon": "🐍", "label_key": "cert_gallery_label_datascience"},
    {"pdf": "00_MLOps Engineer_Diploma.pdf", "image": "images/MLOps/00_MLOps Engineer_Diploma.jpg", "icon": "⚙️", "label_key": "cert_gallery_label_diploma_mlops"},
]