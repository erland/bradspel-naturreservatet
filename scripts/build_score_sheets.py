#!/usr/bin/env python3
"""Build Naturreservatet score sheet PDFs."""

from __future__ import annotations

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6, A4
from reportlab.lib.units import mm
from pypdf import PdfReader, PdfWriter, Transformation

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/print"
OUT.mkdir(parents=True, exist_ok=True)

ANIMALS = [
    ("Groda", 2),
    ("Rådjur", 2),
    ("Bäver", 4),
    ("Trana", 4),
    ("Lo", 5),
    ("Fiskgjuse", 6),
]


def draw_score_sheet(c: canvas.Canvas, x0: float, y0: float, w: float, h: float) -> None:
    pad = 6 * mm
    c.setLineWidth(0.6)
    c.rect(x0, y0, w, h)
    y = y0 + h - pad

    c.setFont("Helvetica-Bold", 13)
    c.drawString(x0 + pad, y, "NATURRESERVATET - POÄNGBLAD")
    y -= 7 * mm

    c.setFont("Helvetica", 8)
    c.drawString(x0 + pad, y, "Spelare: ______________________________")
    y -= 7 * mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0 + pad, y, "Djur")
    y -= 5 * mm

    for name, pts in ANIMALS:
        c.setFont("Helvetica", 8)
        c.rect(x0 + pad, y - 2.5 * mm, 3 * mm, 3 * mm)
        c.drawString(x0 + pad + 5 * mm, y - 1.7 * mm, f"{name}  {pts} p")
        y -= 5 * mm

    y -= 1 * mm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0 + pad, y, "Bonus")
    y -= 5 * mm

    bonuses = [
        "Minst 4 djurarter  +3",
        "Alla 5 naturtyper  +2",
        "Områden med minst 4 lika fält: ____ x 1",
    ]

    for bonus in bonuses:
        c.setFont("Helvetica", 7.5)
        if not bonus.startswith("Områden"):
            c.rect(x0 + pad, y - 2.5 * mm, 3 * mm, 3 * mm)
            c.drawString(x0 + pad + 5 * mm, y - 1.7 * mm, bonus)
        else:
            c.drawString(x0 + pad, y - 1.7 * mm, bonus)
        y -= 5 * mm

    y -= 2 * mm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0 + pad, y, "Djur: ____   Bonus: ____   TOTALT: ______")


def main() -> int:
    a6 = OUT / "score-sheet-a6.pdf"
    c = canvas.Canvas(str(a6), pagesize=A6)
    draw_score_sheet(c, 0, 0, A6[0], A6[1])
    c.showPage()
    c.save()

    a4 = OUT / "score-sheets-a4.pdf"
    src = PdfReader(str(a6)).pages[0]
    writer = PdfWriter()
    page = writer.add_blank_page(width=A4[0], height=A4[1])
    positions = [
        (0, A4[1] - A6[1]),
        (A6[0], A4[1] - A6[1]),
        (0, A4[1] - 2 * A6[1]),
        (A6[0], A4[1] - 2 * A6[1]),
    ]
    for x, y in positions:
        page.merge_transformed_page(src, Transformation().translate(tx=x, ty=y))
    with a4.open("wb") as fh:
        writer.write(fh)

    print(a6)
    print(a4)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
