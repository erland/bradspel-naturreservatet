#!/usr/bin/env python3
"""Build Naturreservatet visual A6 reference cards."""
from pathlib import Path
import yaml
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6, A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from pypdf import PdfReader, PdfWriter, Transformation

ROOT = Path(__file__).resolve().parents[1]
DATA = yaml.safe_load((ROOT/"data/reference-card-v2.yaml").read_text(encoding="utf-8"))
STYLE = yaml.safe_load((ROOT/"data/style.yaml").read_text(encoding="utf-8"))
ANIMALS = yaml.safe_load((ROOT/"data/animals.yaml").read_text(encoding="utf-8"))["animals"]
VERSION = str(DATA["version"])
OUT = ROOT/"output/print"
OUT.mkdir(parents=True, exist_ok=True)

terrain = STYLE["terrain"].copy()
terrain["Valfri"] = {
    "color": STYLE["rules"]["Valfri"]["color"],
    "icon": STYLE["rules"]["Valfri"]["icon"]
}
icon_cache = {
    name: svg2rlg(str(ROOT/meta["icon"]))
    for name, meta in terrain.items()
}
animal_by_id = {a["id"]: a for a in ANIMALS}

def draw_cell(c, x, y, size, name):
    is_any = name == "Valfri"
    c.setStrokeColor(colors.HexColor("#777777" if is_any else "#444444"))
    c.setLineWidth(0.55 if is_any else 0.45)
    if is_any:
        c.setDash(2.2, 1.8)
    c.setFillColor(colors.HexColor(terrain[name]["color"]))
    c.roundRect(x, y, size, size, 1.2*mm, fill=1, stroke=1)
    c.setDash()

    drawing = icon_cache[name]
    maxdim = max(drawing.width, drawing.height)
    scale = (size * (0.40 if is_any else 0.44)) / maxdim
    c.saveState()
    c.translate(x + size/2 - drawing.width*scale/2,
                y + size*0.58 - drawing.height*scale/2)
    c.scale(scale, scale)
    renderPDF.draw(drawing, c, 0, 0)
    c.restoreState()

    c.setFillColor(colors.HexColor("#555555" if is_any else "#222222"))
    c.setFont("Helvetica-Bold", 4.5 if is_any else 4.8)
    c.drawCentredString(x + size/2, y + 1.2*mm, "Valfri" if is_any else name)

def draw_pattern(c, x, y, w, h, grid, cell):
    rows = len(grid)
    cols = max(len(row) for row in grid)
    sx = x + (w-cols*cell)/2
    sy = y + (h-rows*cell)/2
    for r, row in enumerate(grid):
        for col, name in enumerate(row):
            if name:
                draw_cell(c, sx+col*cell, sy+(rows-1-r)*cell, cell, name)

def wrap(text, size, width):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words, lines, cur = text.split(), [], ""
    for word in words:
        test = (cur+" "+word).strip()
        if stringWidth(test, "Helvetica", size) <= width:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

pdf = OUT/f"reference-card-a6-v2-v{VERSION}.pdf"
c = canvas.Canvas(str(pdf), pagesize=A6)
W,H = A6
margin = 5*mm
row_heights = [v*mm for v in DATA["layout"]["row_heights_mm"]]
cell = DATA["layout"]["terrain_cell_mm"]*mm

c.setFillColor(colors.HexColor("#F8FAF4")); c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(colors.HexColor("#234B2C")); c.setFont("Helvetica-Bold",13.5)
c.drawString(margin,H-margin-1*mm,"NATURRESERVATET")
c.setFillColor(colors.HexColor("#333333")); c.setFont("Helvetica",7.2)
c.drawString(margin,H-margin-5.8*mm,"Djurkrav - visuellt referenskort")

pattern_w = 38*mm
text_x = margin+pattern_w+3*mm
text_w = W-margin-text_x
y_top = H-margin-15*mm

for i,(entry,row_h) in enumerate(zip(DATA["animals"],row_heights)):
    animal = animal_by_id[entry["id"]]
    name, pts, req = animal["name"], animal["points"], animal["requirement"]
    grid = entry["pattern"]
    y = y_top-row_h
    c.setFillColor(colors.white if i%2==0 else colors.HexColor("#F1F5EC"))
    c.roundRect(margin,y+0.6*mm,W-2*margin,row_h-1.2*mm,1.8*mm,fill=1,stroke=0)
    draw_pattern(c,margin+1.2*mm,y+1.2*mm,pattern_w-2.4*mm,row_h-2.4*mm,grid,cell)

    c.setFillColor(colors.HexColor("#1F3E25")); c.setFont("Helvetica-Bold",8.2)
    c.drawString(text_x,y+row_h-5.2*mm,name)
    c.setFillColor(colors.HexColor("#7A4E00"))
    c.drawRightString(W-margin-1.5*mm,y+row_h-5.2*mm,f"{pts} p")
    c.setFillColor(colors.HexColor("#222222")); c.setFont("Helvetica",6.1)
    ty=y+row_h-9.3*mm
    for line in wrap(req,6.1,text_w)[:4]:
        c.drawString(text_x,ty,line); ty-=3*mm
    if entry["id"]=="fiskgjuse":
        c.setFillColor(colors.HexColor("#555555")); c.setFont("Helvetica-Oblique",5.4)
        c.drawString(text_x,y+3.1*mm,"? = valfri naturtyp")
    y_top=y

c.setFillColor(colors.HexColor("#444444")); c.setFont("Helvetica-Oblique",5.4)
c.drawString(margin,2.4*mm,"Intill = sida mot sida. Diagonaler räknas inte.")
c.save()

a4 = OUT/f"reference-card-a6-v2-a4-4up-v{VERSION}.pdf"
src=PdfReader(str(pdf)).pages[0]
writer=PdfWriter()
page=writer.add_blank_page(width=A4[0],height=A4[1])
for x,y in [(0,A4[1]-A6[1]),(A6[0],A4[1]-A6[1]),(0,A4[1]-2*A6[1]),(A6[0],A4[1]-2*A6[1])]:
    page.merge_transformed_page(src,Transformation().translate(tx=x,ty=y))
with a4.open("wb") as f: writer.write(f)
print(pdf)
print(a4)
