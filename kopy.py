if jahr == 1988:
        st.subheader(f"📍 {jahr}: Geburtsort Tscherlak")
        col_text, col_map = st.columns([1, 1.5])
        
        with col_text:
            # Der "nachgebaute" Info-Kasten mit anpassbarer Schriftgröße
            st.markdown(f"""
                <div style="background-color: #e8f4f9; padding: 15px; border-radius: 5px; 
                            border-left: 6px solid #0072b2; margin-bottom: 20px;">
                    <p style="color: #004466; font-size: {SCHRIFT_GROESSE_INFO}; margin: 0; line-height: 1.4;">
                        Hier begann meine Reise in der UdSSR.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            img = lade_formatiertes_bild("tscherlak.png", target_size=(BILD_BREITE_1988, BILD_BREITE_1988))
            if img: st.image(img, width=BILD_BREITE_1988)

        with col_map:
            # Farbige Karte von Tscherlak
            st.map(pd.DataFrame({'lat': [54.12], 'lon': [74.80]}), zoom=7)