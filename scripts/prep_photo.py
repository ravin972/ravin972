import os
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prep_photo(
    input_path: str = "data/source-photo.jpg",
    output_path: str = "data/source-prepped.png",
):
    if not os.path.exists(input_path):
        print(f"Error: '{input_path}' not found.")
        sys.exit(1)

    print(f"1. Loading image from {input_path}...")
    pil_raw = Image.open(input_path).convert("RGBA")

    # Tight crop around the head/shoulders area (removes empty bottom torso)
    w, h = pil_raw.size
    crop_box = (int(w * 0.05), int(h * 0.05), int(w * 0.95), int(h * 0.88))
    cropped = pil_raw.crop(crop_box)

    import io

    buf = io.BytesIO()
    cropped.save(buf, format="PNG")
    cropped_bytes = buf.getvalue()

    print("2. Removing background using rembg...")
    no_bg_bytes = remove(cropped_bytes)
    pil_no_bg = Image.open(io.BytesIO(no_bg_bytes)).convert("RGBA")
    np_img = np.array(pil_no_bg)

    rgb = np_img[:, :, :3]
    alpha = np_img[:, :, 3]

    print("3. Enhancing facial edge contrast via CLAHE...")
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    # CLAHE with clipLimit 3.5 gives sharp edge definition to sunglasses, hair, and beard
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    print("4. Compositing subject onto pure white background...")
    alpha_norm = (alpha / 255.0)[:, :, np.newaxis]
    white_bg = np.ones_like(rgb, dtype=np.float32) * 255.0
    fg = np.repeat(enhanced_gray[:, :, np.newaxis], 3, axis=2).astype(
        np.float32
    )

    composited = (fg * alpha_norm + white_bg * (1.0 - alpha_norm)).astype(
        np.uint8
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    Image.fromarray(composited).save(output_path)
    print(f"✓ Saved prepped image to '{output_path}'")


if __name__ == "__main__":
    prep_photo()