#!/usr/bin/env python3
"""Build Naturreservatet landscape tile SVG sheets and PDF.

Källor:
- data/game.yaml
- data/tiles.yaml
- data/style.yaml
- assets/icons/*.svg

Output:
- output/print/svg/landskapsbrickor-vX.Y.Z-sida-N.svg
- output/print/landskapsbrickor-70x35mm-vX.Y.Z.pdf
"""

from __future__ import annotations

from pathlib import Path
import re
import yaml
import cairosvg
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
SVG_OUT = ROOT / "output/print/svg"
PDF_OUT = ROOT / "output/print"
SVG_OUT.mkdir(parents=True, exist_ok=True)
PDF_OUT.mkdir(parents=True, exist_ok=True)


def icon_inner(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", text, flags=re.S).strip()


def icon_group(root: Path, terrain_name: str, meta: dict, cx: float, cy: float) -> str:
    scale = float(meta.get("icon_scale", meta.get("scale", 0.406)))
    icon_path = root / meta["icon"]
    return f'<g transform="translate({cx},{cy}) scale({scale})">{icon_inner(icon_path)}</g>'


def tile_group(root: Path, style: dict, tile: dict, x: float, y: float) -> str:
    w, h, half = 70, 35, 35
    tid, a, b = tile["id"], tile["a"], tile["b"]
    ta, tb = style["terrain"][a], style["terrain"][b]
    return f"""<g>
<rect x="{x}" y="{y}" width="{half}" height="{h}" rx="2" fill="{ta['color']}" stroke="#222" stroke-width="0.45"/>
<rect x="{x+half}" y="{y}" width="{half}" height="{h}" rx="2" fill="{tb['color']}" stroke="#222" stroke-width="0.45"/>
<line x1="{x+half}" y1="{y}" x2="{x+half}" y2="{y+h}" stroke="#555" stroke-width="0.35"/>
<rect x="{x+1.8}" y="{y+1.8}" width="11" height="5" rx="1.3" fill="#fff" fill-opacity="0.9"/>
<text x="{x+7.3}" y="{y+5.4}" text-anchor="middle" font-family="Arial,sans-serif" font-size="3.2" font-weight="700">{tid}</text>
{icon_group(root,a,ta,x+17.5,y+15)}
{icon_group(root,b,tb,x+52.5,y+15)}
<text x="{x+17.5}" y="{y+31}" text-anchor="middle" font-family="Arial,sans-serif" font-size="4.4" font-weight="700">{a}</text>
<text x="{x+52.5}" y="{y+31}" text-anchor="middle" font-family="Arial,sans-serif" font-size="4.4" font-weight="700">{b}</text>
</g>"""


def page(root: Path, version: str, style: dict, tiles: list[dict], page_no: int, page_count: int) -> str:
    groups = []
    for i, tile in enumerate(tiles):
        row, col = divmod(i, 3)
        groups.append(tile_group(root, style, tile, 35.5 + col * 78, 27 + row * 43))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="210mm" viewBox="0 0 297 210">
<rect width="297" height="210" fill="#fff"/>
<text x="12" y="10" font-family="Arial,sans-serif" font-size="6" font-weight="700">NATURRESERVATET - LANDSKAPSBRICKOR v{version}</text>
<text x="12" y="16" font-family="Arial,sans-serif" font-size="3.8">Sida {page_no}/{page_count} - 70 x 35 mm - skriv ut i faktisk storlek (100 %)</text>
{''.join(groups)}
</svg>"""


def main() -> int:
    game = yaml.safe_load((ROOT / "data/game.yaml").read_text(encoding="utf-8"))["game"]
    style = yaml.safe_load((ROOT / "data/style.yaml").read_text(encoding="utf-8"))
    tiles_data = yaml.safe_load((ROOT / "data/tiles.yaml").read_text(encoding="utf-8"))

    version = str(game["version"])
    tiles = tiles_data["tiles"]
    pages = [tiles[i:i+12] for i in range(0, len(tiles), 12)]

    svgs = []
    for n, items in enumerate(pages, 1):
        path = SVG_OUT / f"landskapsbrickor-v{version}-sida-{n}.svg"
        path.write_text(page(ROOT, version, style, items, n, len(pages)), encoding="utf-8")
        svgs.append(path)

    temps = []
    for n, svg in enumerate(svgs, 1):
        tmp = PDF_OUT / f"_landscape-tiles-{n}.pdf"
        cairosvg.svg2pdf(
            url=str(svg),
            write_to=str(tmp),
            output_width=297 * 72 / 25.4,
            output_height=210 * 72 / 25.4,
        )
        temps.append(tmp)

    writer = PdfWriter()
    for tmp in temps:
        for p in PdfReader(str(tmp)).pages:
            writer.add_page(p)

    pdf = PDF_OUT / f"landskapsbrickor-70x35mm-v{version}.pdf"
    with pdf.open("wb") as fh:
        writer.write(fh)

    for tmp in temps:
        tmp.unlink()

    print(pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
