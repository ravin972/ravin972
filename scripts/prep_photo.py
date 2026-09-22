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
        print(f"Error: '{input_path}' not found. Please provide an image.")
        sys.exit(1)

    print(f"1. Removing background from {input_path}...")
    with open(input_path, "rb") as f:
        img_bytes = f.read()
    no_bg = remove(img_bytes)

    import io

    pil_img = Image.open(io.BytesIO(no_bg)).convert("RGBA")
    np_img = np.array(pil_img)

    rgb = np_img[:, :, :3]
    alpha = np_img[:, :, 3]

    print("2. Enhancing contrast with CLAHE...")
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    print("3. Compositing onto white background...")
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