# Naturreservatet

Ett lätt tile-placement-spel för 2–4 spelare där varje spelare bygger ett eget naturreservat och skapar livsmiljöer för djur.

## Aktuell version

v0.3.3 – speltestbas med spelmotor för 2–4 spelare

## Spelram

- 2–4 spelare
- cirka 15–30 minuter
- 8 turer per spelare
- 16/24/32 landskapsbrickor vid 2/3/4 spelare

## Viktiga källfiler

- `docs/rulebook.md` – aktuella regler
- `data/game.yaml` – spelmetadata
- `data/tiles.yaml` – brickor och spelaruppsättningar
- `data/animals.yaml` – djurkrav och poäng
- `data/style.yaml` – färger, ikoner och komponentmått
- `data/reference-card-v2.yaml` – visuella exempel på djurkraven
- `assets/icons/` – återanvändbara SVG-ikoner

## Bygga output

```bash
python scripts/build_landscape_tiles.py
python scripts/build_reference_card_v2.py
python scripts/validate_project.py
```

## Aktuell utskriftsoutput

- `output/print/landskapsbrickor-70x35mm-v0.3.0.pdf`
- `output/print/reference-card-a6-v2-v0.3.0.pdf`
- `output/print/reference-card-a6-v2-a4-4up-v0.3.0.pdf`
- `output/print/score-sheet-a6.pdf`
- `output/print/score-sheets-a4.pdf`

Filer i `output/` är genererade. Ändra källorna i `data/`, `docs/`, `assets/`, `templates/` eller `scripts/`.

## Spelmotor

Se `docs/SPELMOTORPLAN.md` och `scripts/simulator/README.md`.

Snabbtest:

```bash
python -m unittest discover -s tests -v
python -m scripts.simulator.simulate --games 250
```

## Fler­spelar­simulering v0.3.3

- `scripts/simulator/simulate_multiplayer.py`
- `output/simulation-v0.3.3/multiplayer-summary.json`
- `output/simulation-v0.3.3/multiplayer-report.md`
- `output/simulation-v0.3.3/analysis.md`
