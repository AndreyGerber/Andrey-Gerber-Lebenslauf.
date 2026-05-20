# utils/image_loader.py

import os
from PIL import Image

def load_formatted_image(name, target_size=(900, 600), max_width=None):
    pfad = os.path.join("assets", "images", name)

    if not os.path.exists(pfad):
        pfad = os.path.join("images", name)

    if not os.path.exists(pfad):
        return None

    if pfad.lower().endswith(".pdf"):
        return None

    try:
        img = Image.open(pfad)

        if img.mode != "RGB":
            img = img.convert("RGB")

        if max_width:
            ratio = max_width / img.size[0]
            new_size = (max_width, int(img.size[1] * ratio))
            img.thumbnail(new_size, Image.Resampling.LANCZOS)
            return img
        else:
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
            new_img.paste(
                img,
                (
                    (target_size[0] - img.size[0]) // 2,
                    (target_size[1] - img.size[1]) // 2,
                ),
            )
            return new_img

    except Exception as e:
        print(f"Fehler bei Datei {name}: {e}")
        return None