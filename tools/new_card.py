"""Génère une carte de projet SVG pour le README.

Exemple :
  python tools/new_card.py --id mon-projet --title "Mon projet" \
      --desc "Une courte description de ce que fait le projet." \
      --logo assets/logos/mon-projet.png --tags HTML,JS,Cloudflare \
      --url https://github.com/lp-alyx/mon-projet

Crée assets/cards/<id>.svg (le logo y est intégré) et affiche la ligne à coller dans le README.
"""
import argparse, base64, mimetypes, textwrap
from pathlib import Path
from xml.sax.saxutils import escape

p = argparse.ArgumentParser()
p.add_argument("--id", required=True)
p.add_argument("--title", required=True)
p.add_argument("--desc", required=True)
p.add_argument("--logo", required=True, help="chemin du logo dans le repo (png, jpg, svg, webp)")
p.add_argument("--tags", default="")
p.add_argument("--url", default="")
p.add_argument("--c1", default="#7c3aed", help="couleur d'accent 1")
p.add_argument("--c2", default="#06b6d4", help="couleur d'accent 2")
a = p.parse_args()

W, H = 480, 200
logo = Path(a.logo)
mime = mimetypes.guess_type(logo.name)[0] or "image/png"
if logo.suffix.lower() == ".svg":
    mime = "image/svg+xml"
data = base64.b64encode(logo.read_bytes()).decode()

lines = textwrap.wrap(a.desc, 44)[:3]
desc = "".join(
    f'<text x="120" y="{88 + i * 20}" font-size="14" fill="#9ba7b4">{escape(l)}</text>'
    for i, l in enumerate(lines)
)

pills, x = "", 24
for t in [t.strip() for t in a.tags.split(",") if t.strip()]:
    w = len(t) * 7.6 + 22
    pills += (
        f'<rect x="{x}" y="156" width="{w:.0f}" height="26" rx="13" fill="url(#ac)" fill-opacity="0.18" stroke="url(#ac)" stroke-opacity="0.7"/>'
        f'<text x="{x + w / 2:.0f}" y="173" font-size="12" font-weight="600" fill="#e6edf3" text-anchor="middle">{escape(t)}</text>'
    )
    x += w + 8

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI,Helvetica,Arial,sans-serif">
<defs>
<linearGradient id="ac" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a.c1}"/><stop offset="1" stop-color="{a.c2}"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#161b22"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
</defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20" fill="url(#bg)" stroke="url(#ac)" stroke-width="2"/>
<rect x="24" y="30" width="76" height="76" rx="20" fill="url(#ac)" fill-opacity="0.22" stroke="url(#ac)" stroke-opacity="0.8"/>
<image x="40" y="46" width="44" height="44" preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{data}"/>
<text x="120" y="58" font-size="22" font-weight="700" fill="#ffffff">{escape(a.title)}</text>
{desc}
{pills}
<text x="{W-24}" y="173" font-size="13" font-weight="600" fill="url(#ac)" text-anchor="end">Voir le projet →</text>
</svg>'''

out = Path("assets/cards") / f"{a.id}.svg"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg, encoding="utf-8")
print(f"Carte créée : {out}\n\nColle ceci dans le README :\n")
img = f'<img src="./assets/cards/{a.id}.svg" width="400" alt="{escape(a.title)}" />'
print(f'<a href="{a.url}">{img}</a>' if a.url else img)
