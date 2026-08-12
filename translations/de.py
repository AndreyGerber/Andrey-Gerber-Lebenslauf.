"""
translations/de.py

Zentrales Text-Dictionary für die deutsche Version.
Prinzip: JEDER sichtbare Text bekommt einen Key. Layout-Code (in sections/)
verwendet nur noch t["key"] und bleibt für alle Sprachen identisch.

Aktuell befüllt: Zertifikatswand-Texte (als Startpunkt).
TODO: restliche Sektionen (Header, Werdegang, Zeugnisse, Fertigkeiten,
Hobbies, Zitate, Bonus) folgen, sobald wir sie modularisieren.
"""

TRANSLATIONS = {
    # --- Header ---
    "header_welcome": "Willkommen auf der Seite",
    "header_title": "Lebenslauf von Andrey Gerber",
    "header_contact_label": "Meine Kontaktdaten",
    "header_address_note": "Wohnadresse: Brauchst du nicht, ruf an oder schreib",
    "header_drawing_placeholder": "Hier erscheint deine Zeichnung...",

    # --- Werdegang: Zeitstrahl-Grafik ---
    "tl_section_title": "Mein Werdegang",
    "tl_year_1988": "Geboren in der UdSSR ☭",
    "tl_year_1991": "In die Russische Föderation<br>umgezogen – ohne umzuziehen 🇷🇺",
    "tl_year_1996": "School (not cool)",
    "tl_year_2006": "Emigration nach Deutschland 🇩🇪",
    "tl_year_2010": "Studium Flugzeugbau<br>(B.Eng. & M.Sc.)",
    "tl_year_2017": "TÜV Rheinland<br>Sachverständiger für Technische Akustik", 
    "tl_year_2019": "TÜV Rheinland<br> Quality Expert)",
    "tl_year_2022": "Ferchau (bei Siemens)<br>Prozesstechnologe",
    "tl_year_2026": "Liora<br>Data Science & MLOps",

    # --- Werdegang: Detailblöcke ---
    "tl_nav_back": "⬅️ Zurück",
    "tl_nav_next": "Weiter ➡️",

    "tl_1988_heading": "📍 1988: Hier begann meine Reise",

    "tl_1996_heading": "🎒 1996: Schulzeit",
    "tl_1996_text": "So schnell vergehen 10 Jahre.",

    "tl_2006_heading": "✈️ 2006: Der neue Lebensabschnitt beginnt",

    "tl_2010_heading": "🎓 2010: Studium",
    "tl_2010_text": "<strong>Bachelor of Engineering</strong><br>& <strong>Master of Science</strong>.<br><br><br><br><i>\"Pass auf, Wissenschaft – ich komme!\"</i>",

    "tl_2017_heading": "🛠️ 2017 – 2022: TÜV Rheinland",
    "tl_2017_role1_title": "Test & Measurement Engineer",
    "tl_2017_role1_bullets": "<li>Normgerechte <b>akustische Messungen</b> (Haushaltsgeräte, Tools, Spielzeug)</li><li>Planung & Aufbau einer <b>neuen Prüfkammer</b> für Smart Speaker</li><li><b>Schwingungsmessungen & kundenspezifische Sondermessungen</b></li><li>Mitglied im <b>DIN-Normenausschuss</b> für Schalldämmung</li>",
    "tl_2017_role2_title": "ab 2019 <br>Qualitätsmanager / Quality Expert",
    "tl_2017_role2_bullets": "<li>Durchführung <b>interner Audits</b> (ISO 9001 & ISO 17025)</li><li>Verantwortung für <b>CAPA-Prozesse</b> und <b>Beschwerdemanagement</b></li><li><b>Externe Audits</b> und <b>Management Reviews</b></li>",

    "tl_2022_heading": "⚙️ 2022 – 2025: Ferchau GmbH",
    "tl_2022_role_title": "Prozesstechnologe bei Siemens Healthineers",
    "tl_2022_role_bullets": "<li>Wartung und Reparatur bestehender Anlagen für <b>akustische und Vibrationsmessungen</b></li><li>Betreuung vom Aufbau von mehreren <b>Prüfkammern für akustische und Vibrationsmessungen</b> an dem neuen Produktionsstandort</li><li><b>Entwicklung neuer Prüfmethoden</b></li><li><b>Validierung und Inbetriebnahme</b> für die Serienfertigung</li>",

    "tl_2026_heading": "🤖 2026: Liora",
    "tl_2026_role_title": "Weiterbildung: Data Science & MLOps Engineer",
    "tl_2026_bullets": "<li>Ausbildung zum <b>Data Scientist</b> (Python, ML, Deep Learning)</li><li>Weiterbildung zum <b>MLOps Engineer</b> (Docker, CI/CD, Model Deployment)</li><li>Diesen digitalen Lebenslauf selbst mit <b>Python & Streamlit</b> entwickelt</li>",

    # --- Zeugnis-Galerie ---
    "cert_gallery_title": "Meine Zeugnisse und Zertifikate",
    "cert_gallery_intro": "Hier finden Sie eine Übersicht meiner akademischen und beruflichen Nachweise.",
    "cert_gallery_name_change_title": "Wichtiger Hinweis zur Namensänderung:",
    "cert_gallery_name_change_text": "Bitte beachten Sie, dass ich im Laufe meines Lebens meinen Namen geändert habe. Einige der unten aufgeführten Dokumente (z. B. Abitur, Bachelor) sind daher auf meinen früheren Namen ausgestellt. Ein entsprechender Nachweis über die Namensänderung ist als erstes Dokument in der Galerie hinterlegt.",
    "cert_gallery_download_label": "PDF öffnen",
    "cert_gallery_preview_label": "Vorschau",
    "cert_gallery_no_preview_warning": "Bild-Vorschau nicht gefunden, lade PDF-Betrachter...",
    "cert_gallery_missing_file": "Datei nicht gefunden.",

    "cert_gallery_label_namensaenderung": "Namensänderung",
    "cert_gallery_label_berufsschule": "Berufsschule",
    "cert_gallery_label_abitur": "Abitur",
    "cert_gallery_label_praktikum": "Praktikum V&F",
    "cert_gallery_label_bachelor": "Bachelor Zeugnis",
    "cert_gallery_label_schweisskurs": "Schweißkurs",
    "cert_gallery_label_wertanalytiker": "Wertanalytiker",
    "cert_gallery_label_master": "Master Zeugnis",
    "cert_gallery_label_bk_pulse": "B&K Pulse",
    "cert_gallery_label_mbbm": "M-BBM",
    "cert_gallery_label_auditor": "Auditor 9000 ff.",
    "cert_gallery_label_qmb9001": "QMB ISO 9001",
    "cert_gallery_label_qmb17025": "QMB ISO 17025",
    "cert_gallery_label_datascience": "Data_Science",
    "cert_gallery_label_diploma_ds": "Diplom: Data Science",
    "cert_gallery_label_diploma_mlops": "Diplom: MLOps Engineer",

    # --- Fertigkeiten ---
    "skills_title": "🛠️ Meine Fertigkeiten",
    "skills_kerze_title": "Von der Skizze bis zum fertigen Produkt",
    "skills_project_title": "Von der Idee bis zur Übergabe an die Fertigung",

    "skills_hw_sw_title": "Hardware & Software",
    "skills_hw_sw_items": "<li><strong>📐 3D-Modelle mit CATIA V5 oder AutoCAD erstellen.</strong></li><li><strong>🎙️🎧 Sensorik anschließen, einstellen und Objekte vermessen mit Technik von B&K oder Head Acoustics.</strong></li><li><strong>🔢 Daten mit Minitab oder selbst erstellten statistischen Methoden analysieren.</strong></li><li><strong>🗄️ SAP kann jeder irgendwie und niemand gleichzeitig.</strong></li><li><strong>📑 Von MS-Produkten spricht heutzutage doch niemand mehr. Oder?</strong></li>",

    "skills_hard_soft_title": "Hardskills & Softskills",
    "skills_hard_soft_items": "<li>🛠️ <strong>Projektmanagement (Planung, Steuerung der Umsetzung, Validierung & Inbetriebnahme)</strong></li><li><strong>🧩 Qualitätsmanagement | Lean Management & Six Sigma | Audits | Risikomanagement</strong></li><li><strong>🔍 ISO 9001 oder IATF 16949 | CAPA oder 8D | DMAIC oder PDCA</strong></li>",
    "skills_hard_soft_note": "Hier müssen wir zunächst die Begriffe definieren, bevor aneinander vorbeigesprochen wird.",

    "skills_coding_title": "Ob ich programmieren kann:",
    "skills_coding_text": "Das hier ist übrigens keine Agentur – diese Seite habe ich selbst programmiert.<br>Mit Python, Streamlit und der ein oder anderen Tasse Kaffee.<br><br><i>Übrigens half mir dieses Projekt dabei, meinen Wortschatz an Schimpfwörtern und deren Kombinationen in mehreren Sprachen zu aktualisieren.</i>",

    # --- Hobbies ---
    "hobbies_title": "Leidenschaften & Ausgleich",

    "hobbies_chess_title": "Schach",
    "hobbies_chess_text": "Ein Mann hat seinen Kindern ein Schachspiel gekauft. Nach einem Jahr konnte er mit uns nicht mehr mithalten. Ich sehe nicht nur meine Züge voraus, sondern auch die Züge des Mitspielers.",
    "hobbies_chess_placeholder": "Wo es bei mir mit Schach losging, gab's bei uns im Ort wahrscheinlich drei Personen mit Kameras. Von daher leider keine Bilder von damals.",

    "hobbies_sport_title": "Eishockey & Fußball",
    "hobbies_sport_text": "Nichts ist besser als das Gefühl, zum Erfolg des anderen beigetragen zu haben.",
    "hobbies_sport_img1_title": "Einmal Gold",
    "hobbies_sport_img1_label": "Fußball",
    "hobbies_sport_img2_title": "Auch hier auf dem Podest",
    "hobbies_sport_img2_label": "Eishockey",
    "hobbies_sport_img3_title": "Blick hinter die Kulissen",
    "hobbies_sport_img3_label": "Schmiede",

    "hobbies_yoga_title": "Yoga & Boxen",
    "hobbies_yoga_text": "Schnell reagieren und trotzdem gelassen bleiben.",
    "hobbies_yoga_img1_title": "Es ist entspannt, haben sie gesagt",
    "hobbies_yoga_img1_label": "agil",
    "hobbies_yoga_img2_title": "Ist einfach, haben sie gesagt",
    "hobbies_yoga_img2_label": "ausbalanciert",
    "hobbies_yoga_img3_title": "Du wirst es im Leben brauchen, haben sie gesagt",
    "hobbies_yoga_img3_label": "stark",

    # --- Zitate ---
    "quotes_title": "⚠️ Die 3 größten Fehlschätzungen meines Lebens",
    "quotes_1_text": "Ich werde mein ganzes Leben an diesem Ort verbringen.",
    "quotes_1_year": "2002",
    "quotes_2_text": "Ich bin schon zu alt fürs Programmieren.",
    "quotes_2_year": "2013",
    "quotes_3_text": "Den digitalen Lebenslauf baue ich schnell. Dauert eh nur ein paar Stunden.",
    "quotes_3_year": "2026",

    # --- Bonus ---
    "bonus_title": "Bonus",
    "bonus_video_label": "Video",
    "bonus_image_label": "Frequenzbereich",
    "bonus_image_caption": "Frequenzspektrum der Klangschale",
    "footer_book_tooltip": "📖 Mein Buch: Dieses Projekt befindet sich gerade in Arbeit – die Geschichte schreibt sich von Tag zu Tag weiter.",
    "footer_book_tag": "noch in Arbeit",

    # --- Zertifikatswände ---
    "cert_wall_ds_title": "💻 Data Science",
    "cert_wall_ds_subtitle": "eine 3D-Wand, die man zoomen und drehen kann.",

    "cert_wall_mlops_title": "⚙️ MLOps Engineer",
    "cert_wall_mlops_subtitle": "eine 3D-Wand, die man zoomen und drehen kann.",
}