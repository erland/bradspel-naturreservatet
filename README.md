# Naturreservatet

Ett lätt tile-placement-spel för 2–4 spelare där varje spelare bygger ett eget naturreservat och skapar livsmiljöer för djur.

## Spelram

- 2–4 spelare
- cirka 15–30 minuter
- 8 turer per spelare
- 16/24/32 landskapsbrickor vid 2/3/4 spelare

## Viktiga källfiler

- `docs/rulebook.md` – aktuella regler
- `data/game.yaml` – spelmetadata och fallback-version
- `data/tiles.yaml` – brickor och spelaruppsättningar
- `data/animals.yaml` – djurkrav och poäng
- `data/style.yaml` – färger, ikoner och komponentmått
- `data/reference-card-v2.yaml` – visuella exempel på djurkraven
- `assets/icons/` – återanvändbara SVG-ikoner

## Bygga printmaterial

```bash
python scripts/build_print.py
```

Releasebyggen kan styra versionsnamn via miljövariabel:

```bash
NATURRESERVATET_VERSION=vX.Y.Z python scripts/build_print.py
```

Om ingen miljövariabel finns används fallback-versionen i `data/game.yaml`.

## Testa projektet

```bash
python scripts/build_print.py
python scripts/validate_project.py
python -m unittest discover -s tests -v
```

## Källa och genererad output

`output/` och `release/` är genererade kataloger och behöver normalt inte checkas in.
Se `docs/repository-policy.md`.
