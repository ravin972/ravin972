import os
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # Space (bright/bg) -> Dense symbols (dark areas)


def make_ascii_svg(
    input_path: str = "data/source-prepped.png",
    output_path: str = "ascii-portrait.svg",
    grid_width: int = 92,
):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run prep_photo.py first.")
        return

    img = Image.open(input_path).convert("L")
    w_orig, h_orig = img.size

    char_aspect = 0.55
    grid_height = int((h_orig / w_orig) * grid_width * char_aspect)
    resized = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)

    ascii_rows = []
    ramp_len = len(RAMP)
    for y in range(grid_height):
        row_chars = []
        for x in range(grid_width):
            pixel = resized.getpixel((x, y))
            idx = int((255 - pixel) / 255.0 * (ramp_len - 1))
            row_chars.append(RAMP[idx])
        ascii_rows.append("".join(row_chars))

    char_w = 6.0
    line_h = 10.5
    svg_w = int(grid_width * char_w) + 20
    svg_h = int(grid_height * line_h) + 20

    clip_defs = []
    text_elements = []

    row_dur = 0.28
    stagger = 0.035

    for y, line in enumerate(ascii_rows):
        start_time = round(y * stagger, 3)
        row_y = y * line_h + 10
        escaped_line = (
            line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

        clip_defs.append(f"""
    <clipPath id="wipe-{y}">
      <rect x="10" y="{row_y}" width="0" height="{line_h + 2}">
        <animate attributeName="width" from="0" to="{svg_w}" dur="{row_dur}s" begin="{start_time}s" fill="freeze" />
      </rect>
    </clipPath>""")

        text_elements.append(
            f'    <text x="10" y="{row_y + line_h - 2}" clip-path="url(#wipe-{y})">{escaped_line}</text>'
        )

    svg_content = f"""<svg viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <style>
    text {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: 8.5px;
      fill: #8b949e;
      white-space: pre;
    }}
  </style>
  <defs>{"".join(clip_defs)}
  </defs>
  <rect width="100%" height="100%" fill="#0d1117" rx="8" />
  <g>
{"".join(text_elements)}
  </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"✓ Generated animated ASCII art at '{output_path}'")


if __name__ == "__main__":
    make_ascii_svg()