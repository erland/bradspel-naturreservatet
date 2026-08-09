#!/usr/bin/env python3
from pathlib import Path
import sys, yaml
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
errors=[]

game=yaml.safe_load((ROOT/"data/game.yaml").read_text(encoding="utf-8"))["game"]
tiles_data=yaml.safe_load((ROOT/"data/tiles.yaml").read_text(encoding="utf-8"))
animals=yaml.safe_load((ROOT/"data/animals.yaml").read_text(encoding="utf-8"))["animals"]
ref=yaml.safe_load((ROOT/"data/reference-card-v2.yaml").read_text(encoding="utf-8"))

tiles=tiles_data["tiles"]
ids=[t["id"] for t in tiles]
if len(ids)!=32: errors.append(f"Förväntade 32 brickor, fann {len(ids)}")
if len(ids)!=len(set(ids)): errors.append("Brick-ID:n är inte unika")
if len(animals)!=6: errors.append(f"Förväntade 6 djur, fann {len(animals)}")
if len(ref["animals"])!=6: errors.append("Referenskortet innehåller inte 6 djur")
if str(game["version"])!=str(ref["version"]): errors.append("Versionsskillnad mellan game.yaml och reference-card-v2.yaml")

for key, expected in [("2_players",16),("3_players",24),("4_players",32)]:
    vals=tiles_data["player_count_sets"][key]["tile_ids"]
    if len(vals)!=expected: errors.append(f"{key}: förväntade {expected}, fann {len(vals)}")
    missing=set(vals)-set(ids)
    if missing: errors.append(f"{key}: okända ID:n {sorted(missing)}")

required=[
    ROOT/"docs/rulebook.md",
    ROOT/"output/print"/f"landskapsbrickor-70x35mm-v{game['version']}.pdf",
    ROOT/"output/print"/f"reference-card-a6-v2-v{game['version']}.pdf",
    ROOT/"output/print/score-sheet-a6.pdf",
]
for p in required:
    if not p.exists(): errors.append(f"Saknad fil: {p.relative_to(ROOT)}")

for p in required:
    if p.suffix==".pdf" and p.exists():
        try:
            if len(PdfReader(str(p)).pages)<1:
                errors.append(f"Tom PDF: {p.relative_to(ROOT)}")
        except Exception as e:
            errors.append(f"Ogiltig PDF {p.relative_to(ROOT)}: {e}")

if errors:
    print("VALIDERING MISSLYCKADES")
    for e in errors: print("-",e)
    sys.exit(1)
print("VALIDERING OK")
print(f"Version: {game['version']}")
print(f"Brickor: {len(ids)}")
print(f"Djur: {len(animals)}")
