#!/usr/bin/env python3
"""Build Naturreservatet landscape tile SVG sheets and PDF."""
from pathlib import Path
import re
import cairosvg
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.1"
SVG_OUT = ROOT / "output/print/svg"
PDF_OUT = ROOT / "output/print"
SVG_OUT.mkdir(parents=True, exist_ok=True)

STYLE = {
    "Skog": {"color": "#C8E3A0", "icon": "forest.svg", "scale": 0.406},
    "Sjö": {"color": "#B9DDF3", "icon": "lake.svg", "scale": 0.406},
    "Äng": {"color": "#F7E28A", "icon": "meadow.svg", "scale": 0.3654},
    "Berg": {"color": "#D9D9D9", "icon": "mountain.svg", "scale": 0.406},
    "Våtmark": {"color": "#A9D9DF", "icon": "wetland.svg", "scale": 0.406},
}

TILES = [
("NR-01","Skog","Sjö"),
("NR-02","Skog","Sjö"),
("NR-03","Skog","Sjö"),
("NR-04","Skog","Äng"),
("NR-05","Skog","Äng"),
("NR-06","Skog","Äng"),
("NR-07","Skog","Berg"),
("NR-08","Skog","Berg"),
("NR-09","Skog","Berg"),
("NR-10","Skog","Våtmark"),
("NR-11","Skog","Våtmark"),
("NR-12","Sjö","Äng"),
("NR-13","Sjö","Äng"),
("NR-14","Sjö","Berg"),
("NR-15","Sjö","Våtmark"),
("NR-16","Sjö","Våtmark"),
("NR-17","Sjö","Våtmark"),
("NR-18","Äng","Berg"),
("NR-19","Äng","Våtmark"),
("NR-20","Äng","Våtmark"),
("NR-21","Berg","Våtmark"),
("NR-22","Skog","Skog"),
("NR-23","Sjö","Sjö"),
("NR-24","Äng","Äng"),
("NR-25","Skog","Sjö"),
("NR-26","Skog","Äng"),
("NR-27","Skog","Berg"),
("NR-28","Skog","Våtmark"),
("NR-29","Sjö","Äng"),
("NR-30","Sjö","Våtmark"),
("NR-31","Äng","Våtmark"),
("NR-32","Berg","Våtmark"),
]

def icon_inner(name):
    text=(ROOT/"assets/icons"/STYLE[name]["icon"]).read_text(encoding="utf-8")
    return re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", text, flags=re.S).strip()

def icon_group(name, cx, cy):
    scale=STYLE[name]["scale"]
    return f'<g transform="translate({cx},{cy}) scale({scale})">{icon_inner(name)}</g>'

def tile(tid,a,b,x,y):
    w,h,half=70,35,35
    return f"""<g>
<rect x="{x}" y="{y}" width="{half}" height="{h}" rx="2" fill="{STYLE[a]['color']}" stroke="#222" stroke-width="0.45"/>
<rect x="{x+half}" y="{y}" width="{half}" height="{h}" rx="2" fill="{STYLE[b]['color']}" stroke="#222" stroke-width="0.45"/>
<line x1="{x+half}" y1="{y}" x2="{x+half}" y2="{y+h}" stroke="#555" stroke-width="0.35"/>
<rect x="{x+1.8}" y="{y+1.8}" width="11" height="5" rx="1.3" fill="#fff" fill-opacity="0.9"/>
<text x="{x+7.3}" y="{y+5.4}" text-anchor="middle" font-family="Arial,sans-serif" font-size="3.2" font-weight="700">{tid}</text>
{icon_group(a,x+17.5,y+15)}
{icon_group(b,x+52.5,y+15)}
<text x="{x+17.5}" y="{y+31}" text-anchor="middle" font-family="Arial,sans-serif" font-size="4.4" font-weight="700">{a}</text>
<text x="{x+52.5}" y="{y+31}" text-anchor="middle" font-family="Arial,sans-serif" font-size="4.4" font-weight="700">{b}</text>
</g>"""

def page(items,page_no):
    groups=[]
    for i,(tid,a,b) in enumerate(items):
        row,col=divmod(i,3)
        groups.append(tile(tid,a,b,35.5+col*78,27+row*43))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="210mm" viewBox="0 0 297 210">
<rect width="297" height="210" fill="#fff"/>
<text x="12" y="10" font-family="Arial,sans-serif" font-size="6" font-weight="700">NATURRESERVATET - LANDSKAPSBRICKOR v{VERSION}</text>
<text x="12" y="16" font-family="Arial,sans-serif" font-size="3.8">Sida {page_no}/3 - 70 x 35 mm - skriv ut i faktisk storlek (100 %)</text>
{''.join(groups)}
</svg>"""

svgs=[]
pages = [TILES[:12], TILES[12:24], TILES[24:]]
for n,items in enumerate(pages,1):
    path=SVG_OUT/f"landskapsbrickor-v{VERSION}-sida-{n}.svg"
    path.write_text(page(items,n),encoding="utf-8")
    svgs.append(path)

temps=[]
for n,svg in enumerate(svgs,1):
    tmp=PDF_OUT/f"_tiles-{n}.pdf"
    cairosvg.svg2pdf(url=str(svg),write_to=str(tmp),
                    output_width=297*72/25.4,output_height=210*72/25.4)
    temps.append(tmp)

writer=PdfWriter()
for tmp in temps:
    for p in PdfReader(str(tmp)).pages:
        writer.add_page(p)
pdf=PDF_OUT/f"landskapsbrickor-70x35mm-v{VERSION}.pdf"
with pdf.open("wb") as fh:
    writer.write(fh)
for tmp in temps:
    tmp.unlink()
print(pdf)
