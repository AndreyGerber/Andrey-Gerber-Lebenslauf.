"""
sections/cert_wall.py

Wiederverwendbare 3D-Zertifikatswand (Three.js).
Wird für BEIDE Tracks (Data Science & MLOps Engineer) mit unterschiedlichen
Daten aufgerufen -> kein Code-Duplikat mehr.

Performance:
- @st.cache_resource sammelt die Bilddaten (inkl. Base64) nur EINMAL pro
  Track und Prozess, nicht bei jedem Rerun.
- @st.fragment sorgt dafür, dass ein Rerun innerhalb dieses Blocks
  (z. B. durch einen Widget-Klick INNERHALB des Fragments) nicht die
  komplette restliche Seite neu ausführt. Falls du hier später noch
  Streamlit-Widgets ergänzt (z. B. einen Umschalter "nur Diplome zeigen"),
  bleibt es trotzdem schnell.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import math

from utils.loaders import collect_cert_images_cached


def _build_threejs_html(cert_data: list) -> str:
    num_certs = len(cert_data)
    positions = []
    for i in range(num_certs):
        angle = i * 0.65
        radius = 3.5
        x = math.cos(angle) * radius
        z = math.sin(angle) * radius
        y = (i - num_certs / 2) * 0.35
        positions.append({"x": x, "y": y, "z": z})

    certs_json = json.dumps([{
        "name": cert_data[i]["name"],
        "b64": cert_data[i]["b64"],
        "ext": cert_data[i]["ext"],
        "x": positions[i]["x"],
        "y": positions[i]["y"],
        "z": positions[i]["z"],
    } for i in range(num_certs)])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; font-family: 'Segoe UI', sans-serif; background-color: #f8fafc; }}
            #modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); justify-content: center; align-items: center; cursor: pointer; }}
            #modal img {{ max-width: 90%; max-height: 90%; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div id="modal" onclick="this.style.display='none'"><img id="modalImage" src=""></div>
        <script type="importmap">
            {{ "imports": {{ "three": "https://unpkg.com/three@0.128.0/build/three.module.js", "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/" }} }}
        </script>
        <script type="module">
            import * as THREE from 'three';
            import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';

            const certsData = {certs_json};
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xf8fafc);
            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(5, 3, 8);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;

            scene.add(new THREE.AmbientLight(0xffffff, 0.7));
            const sun = new THREE.DirectionalLight(0xffffff, 0.8);
            sun.position.set(5, 10, 7);
            scene.add(sun);

            const planes = [];
            certsData.forEach(cert => {{
                const loader = new THREE.TextureLoader();
                const texture = loader.load('data:image/' + cert.ext + ';base64,' + cert.b64);
                const material = new THREE.MeshStandardMaterial({{ map: texture, side: THREE.DoubleSide }});
                const plane = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.1), material);
                plane.position.set(cert.x, cert.y, cert.z);
                plane.userData = {{ src: 'data:image/' + cert.ext + ';base64,' + cert.b64 }};
                scene.add(plane);
                planes.push(plane);
            }});

            window.addEventListener('click', (e) => {{
                const mouse = new THREE.Vector2((e.clientX / window.innerWidth) * 2 - 1, -(e.clientY / window.innerHeight) * 2 + 1);
                const raycaster = new THREE.Raycaster();
                raycaster.setFromCamera(mouse, camera);
                const intersects = raycaster.intersectObjects(planes);
                if (intersects.length > 0) {{
                    document.getElementById('modalImage').src = intersects.object.userData.src;
                    document.getElementById('modal').style.display = 'flex';
                }}
            }});

            function animate() {{
                requestAnimationFrame(animate);
                planes.forEach(p => p.lookAt(camera.position));
                controls.update();
                renderer.render(scene, camera);
            }}
            animate();
        </script>
    </body>
    </html>
    """


@st.fragment
def render_cert_wall(cert_defs: tuple, folder: str, title: str, subtitle: str, widget_key: str):
    """
    Rendert eine 3D-Zertifikatswand.

    cert_defs:  Tuple[(dateiname_ohne_endung, anzeige_name), ...]
    folder:     Bildordner, z. B. "images" oder "images/MLOps"
    title:      Überschrift (aus den Übersetzungen, z. B. t["cert_wall_ds_title"])
    subtitle:   Unterzeile
    widget_key: eindeutiger Key, falls mehrere Wände auf derselben Seite sind
    """
    st.markdown(f"<h2 style='text-align: left; margin-top: 50px;'>{title}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left; margin-top: 10px;'>{subtitle}</h5>", unsafe_allow_html=True)

    cert_data = collect_cert_images_cached(cert_defs, folder)

    if not cert_data:
        st.info("Noch keine Zertifikatsbilder in diesem Ordner gefunden.")
        return

    html = _build_threejs_html(cert_data)
    col1, col2, col3 = st.columns([0.7, 3, 0.7])
    with col2:
        components.html(html, height=700, scrolling=False)