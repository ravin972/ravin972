import html

INFO = {
    "user": "ravin",
    "host": "github",
    "Role": "Backend Developer & AI Integrator",
    "Stack": "Python, FastAPI, Node.js, PostgreSQL, React",
    "Cloud/Ops": "Docker, Redis, Supabase, Linux",
    "Building": "Voxly (OSS Webhook & Messaging Engine)",
    "Focus": "High-performance APIs & AI Agent Orchestration",
    "Location": "India",
}


def make_info_card(output_path: str = "info-card.svg"):
    width = 490
    height = 360

    rows_data = [
        ("Role", INFO["Role"], "#58a6ff"),
        ("Stack", INFO["Stack"], "#7ee787"),
        ("Cloud/Ops", INFO["Cloud/Ops"], "#ffa657"),
        ("Building", INFO["Building"], "#d2a8ff"),
        ("Focus", INFO["Focus"], "#79c0ff"),
        ("Location", INFO["Location"], "#ff7b72"),
    ]

    lines_svg = []
    y_pos = 80
    delay = 0.15

    for label, val, color in rows_data:
        escaped_val = html.escape(val)
        lines_svg.append(f"""
    <g class="fade-row" style="animation-delay: {delay:.2f}s;">
      <text x="25" y="{y_pos}" class="label" fill="{color}">{label}</text>
      <text x="110" y="{y_pos}" class="separator">~</text>
      <text x="130" y="{y_pos}" class="value">{escaped_val}</text>
    </g>""")
        y_pos += 30
        delay += 0.08

    palette_blocks = []
    palette_colors = [
        "#484f58",
        "#ff7b72",
        "#7ee787",
        "#d29922",
        "#58a6ff",
        "#bc8cff",
        "#39c5cf",
        "#f0f6fc",
    ]
    for idx, c in enumerate(palette_colors):
        palette_blocks.append(
            f'<rect x="{25 + idx * 24}" y="{y_pos + 18}" width="18" height="12" rx="2" fill="{c}" />'
        )

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <style>
    @keyframes slideIn {{
      0% {{ opacity: 0; transform: translateX(-10px); }}
      100% {{ opacity: 1; transform: translateX(0); }}
    }}
    .fade-row {{
      opacity: 0;
      animation: slideIn 0.35s ease-out forwards;
    }}
    text {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 13px;
    }}
    .title {{ font-weight: bold; fill: #58a6ff; }}
    .separator {{ fill: #8b949e; }}
    .label {{ font-weight: 600; }}
    .value {{ fill: #c9d1d9; }}
  </style>

  <rect width="100%" height="100%" fill="#0d1117" rx="8" stroke="#30363d" stroke-width="1" />

  <!-- Window controls -->
  <circle cx="25" cy="22" r="5" fill="#ff5f56" />
  <circle cx="42" cy="22" r="5" fill="#ffbd2e" />
  <circle cx="59" cy="22" r="5" fill="#27c93f" />

  <!-- Title bar -->
  <text x="80" y="26" class="title">{INFO['user']}@{INFO['host']}</text>
  <line x1="20" y1="42" x2="{width - 20}" y2="42" stroke="#21262d" stroke-width="1" />

  <!-- Info lines -->
  {"".join(lines_svg)}

  <!-- Terminal Color Blocks -->
  <g class="fade-row" style="animation-delay: {delay + 0.1:.2f}s;">
    {"".join(palette_blocks)}
  </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✓ Successfully generated clean '{output_path}'")


if __name__ == "__main__":
    make_info_card()