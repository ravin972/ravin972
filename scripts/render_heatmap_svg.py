import json
import os

PALETTE = [
    "#161b22",  # None
    "#0e4429",  # Level 1
    "#006d32",  # Level 2
    "#26a641",  # Level 3
    "#39d353",  # Level 4
    "#69f0a0",  # Peak
]


def render_heatmap_svg(
    json_path: str = "data/contributions.json",
    output_path: str = "contrib-heatmap.svg",
):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} missing. Run fetch_contributions.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_year = data.get("total_year", 0)
    streak = data.get("current_streak", 0)

    box_size = 11
    gap = 3
    pad_left = 32
    pad_top = 40
    width = 860
    height = 185

    svg_rects = []
    # Take the last 53 weeks (53 * 7 = 371 days)
    for i, day in enumerate(days[-371:]):
        col = i // 7
        row = i % 7
        x = pad_left + col * (box_size + gap)
        y = pad_top + row * (box_size + gap)
        level = min(day.get("level", 0), len(PALETTE) - 1)
        color = PALETTE[level]

        delay = (col * 0.015) + (row * 0.008)

        svg_rects.append(
            f'<rect class="heat-box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
            f'rx="2" fill="{color}" style="animation-delay: {delay:.3f}s;" />'
        )

    legend_x = width - 180
    legend_y = height - 20
    legend_svg = []
    for idx, c in enumerate(PALETTE):
        legend_svg.append(
            f'<rect x="{legend_x + 36 + idx * 14}" y="{legend_y - 9}" width="10" height="10" rx="2" fill="{c}" />'
        )

    svg = f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <style>
    @keyframes dropIn {{
      0% {{ opacity: 0; transform: scale(0.6) translateY(-4px); }}
      100% {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}
    .heat-box {{
      opacity: 0;
      transform-box: fill-box;
      transform-origin: center;
      animation: dropIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    text {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 11px;
      fill: #8b949e;
    }}
  </style>

  <rect width="100%" height="100%" fill="#0d1117" rx="8" stroke="#30363d" stroke-width="1" />

  <!-- Header -->
  <text x="{pad_left}" y="25" fill="#58a6ff" font-weight="bold">./contributions.sh</text>
  <text x="180" y="25" fill="#8b949e">{total_year:,} contributions in the last year · {streak}-day active streak</text>

  <!-- Heatmap matrix -->
  <g>
    {"".join(svg_rects)}
  </g>

  <!-- Legend -->
  <text x="{legend_x}" y="{legend_y}">Less</text>
  {"".join(legend_svg)}
  <text x="{legend_x + 36 + len(PALETTE) * 14 + 6}" y="{legend_y}">More</text>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✓ Generated contribution heatmap at '{output_path}'")


if __name__ == "__main__":
    render_heatmap_svg()