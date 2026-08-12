"""
sections/cert_carousel.py

CSS-3D-Karussell: leichtgewichtige Alternative zu cert_wall.py.
Kein WebGL/Three.js - nur CSS 3D-Transforms + etwas Vanilla-JS zum Drehen
per Maus-Drag / Touch-Swipe. Dreht außerdem sanft von alleine, wenn man
nicht mit der Maus drüber ist.

Nutzt dieselbe collect_cert_images_cached()-Funktion wie cert_wall.py,
damit die Bild-Sammel-Logik nur einmal gepflegt werden muss.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import math

from utils.loaders import collect_cert_images_cached

CARD_WIDTH = 260
CARD_HEIGHT = 200


def _build_carousel_html(cert_data: list) -> str:
    num_certs = len(cert_data)
    angle_step = 360 / num_certs

    # Radius so berechnen, dass sich die Karten im Ring gerade nicht überlappen
    # (Standardformel für ein regelmäßiges Vieleck aus n Karten der Breite CARD_WIDTH)
    radius = int((CARD_WIDTH / 2) / math.tan(math.pi / num_certs)) + 40

    cards_html = ""
    for i, cert in enumerate(cert_data):
        angle = i * angle_step
        cards_html += f"""
        <div class="cert-card" style="transform: rotateY({angle}deg) translateZ({radius}px);"
             data-src="data:image/{cert['ext']};base64,{cert['b64']}" data-name="{cert['name']}">
            <img src="data:image/{cert['ext']};base64,{cert['b64']}" alt="{cert['name']}">
            <div class="cert-label">{cert['name']}</div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0; overflow: hidden; font-family: 'Segoe UI', sans-serif;
                background-color: #f8fafc; height: 100%;
                display: flex; align-items: center; justify-content: center;
            }}
            .scene {{
                width: 100%; height: 520px;
                perspective: 1400px;
                display: flex; align-items: center; justify-content: center;
                cursor: grab;
                user-select: none;
            }}
            .scene:active {{ cursor: grabbing; }}
            .carousel {{
                position: relative;
                width: {CARD_WIDTH}px; height: {CARD_HEIGHT}px;
                transform-style: preserve-3d;
                transition: transform 0.15s ease-out;
            }}
            .cert-card {{
                position: absolute;
                width: {CARD_WIDTH}px; height: {CARD_HEIGHT}px;
                left: 0; top: 0;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                border: 2px solid #e2e8f0;
                background: white;
                cursor: pointer;
            }}
            .cert-card img {{
                width: 100%; height: 100%; object-fit: cover; display: block;
                pointer-events: none;
            }}
            .cert-label {{
                position: absolute; bottom: 0; left: 0; right: 0;
                background: rgba(0,0,0,0.55);
                color: white; font-size: 12px; text-align: center;
                padding: 4px 6px;
                pointer-events: none;
                white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            }}
            #modal {{
                display: none; position: fixed; z-index: 1000; left: 0; top: 0;
                width: 100%; height: 100%; background: rgba(0,0,0,0.9);
                justify-content: center; align-items: center; cursor: pointer;
            }}
            #modal img {{ max-width: 90%; max-height: 90%; border-radius: 10px; }}
            .hint {{
                position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%);
                color: #94a3b8; font-size: 13px; pointer-events: none;
            }}
        </style>
    </head>
    <body>
        <div id="modal" onclick="this.style.display='none'"><img id="modalImage" src=""></div>
        <div class="scene" id="scene">
            <div class="carousel" id="carousel">
                {cards_html}
            </div>
            <div class="hint">↔️ Ziehen zum Drehen</div>
        </div>
        <script>
            const scene = document.getElementById('scene');
            const carousel = document.getElementById('carousel');
            let rotationY = 0;
            let isDragging = false;
            let startX = 0;
            let startRotation = 0;
            let autoRotate = true;

            function applyRotation() {{
                carousel.style.transform = `rotateY(${{rotationY}}deg)`;
            }}

            scene.addEventListener('pointerdown', (e) => {{
                isDragging = true;
                autoRotate = false;
                startX = e.clientX;
                startRotation = rotationY;
                carousel.style.transition = 'none';
                scene.setPointerCapture(e.pointerId);
            }});

            scene.addEventListener('pointermove', (e) => {{
                if (!isDragging) return;
                const delta = e.clientX - startX;
                rotationY = startRotation + delta * 0.4;
                applyRotation();
            }});

            scene.addEventListener('pointerup', () => {{
                isDragging = false;
                carousel.style.transition = 'transform 0.15s ease-out';
            }});

            scene.addEventListener('pointerleave', () => {{
                isDragging = false;
            }});

            // Klick (ohne Ziehen) auf eine Karte -> Großansicht
            let dragDistance = 0;
            scene.addEventListener('pointerdown', (e) => {{ dragDistance = 0; }});
            scene.addEventListener('pointermove', (e) => {{
                if (isDragging) dragDistance += Math.abs(e.movementX);
            }});
            document.querySelectorAll('.cert-card').forEach(card => {{
                card.addEventListener('click', () => {{
                    if (dragDistance > 5) return;  // war ein Drag, kein Klick
                    document.getElementById('modalImage').src = card.dataset.src;
                    document.getElementById('modal').style.display = 'flex';
                }});
            }});

            // Sanfte Auto-Rotation, solange nicht gezogen wird
            function tick() {{
                if (autoRotate) {{
                    rotationY += 0.08;
                    applyRotation();
                }}
                requestAnimationFrame(tick);
            }}
            tick();

            // Nach 3 Sekunden Inaktivität wieder auto-rotieren
            let resumeTimer;
            scene.addEventListener('pointerup', () => {{
                clearTimeout(resumeTimer);
                resumeTimer = setTimeout(() => {{ autoRotate = true; }}, 3000);
            }});
        </script>
    </body>
    </html>
    """


def render_cert_carousel(cert_defs: tuple, folder: str, title: str, subtitle: str, widget_key: str):
    """
    Rendert ein CSS-3D-Karussell (Alternative zu render_cert_wall).

    Gleiche Signatur wie render_cert_wall(), damit du in app.py einfach
    zwischen beiden hin- und herschalten kannst.
    """
    st.markdown(f"<h2 style='text-align: left; margin-top: 50px;'>{title}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left; margin-top: 10px;'>{subtitle}</h5>", unsafe_allow_html=True)

    cert_data = collect_cert_images_cached(cert_defs, folder)

    if not cert_data:
        st.info("Noch keine Zertifikatsbilder in diesem Ordner gefunden.")
        return

    html = _build_carousel_html(cert_data)
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        components.html(html, height=540, scrolling=False)