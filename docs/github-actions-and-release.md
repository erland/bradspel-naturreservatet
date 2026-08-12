# GitHub Actions och release

## 01 Validate

Körs på pull request och push till `main`.

Den bygger först all print-output och kör sedan:

```bash
python scripts/validate_project.py
python -m unittest discover -s tests -v
```

## 02 Build Print Preview

Körs manuellt via `workflow_dispatch`.

Bygger och laddar upp artifactet `naturreservatet-print-preview` med:

- landskapsbrickor
- A6-referenskort
- A4 med fyra referenskort
- A6-poängblad
- A4 med fyra poängblad
- regelbok som PDF via Pandoc
- `PRINT_MANIFEST.json`

## 03 Release Print Package

Körs när en tagg som `vX.Y.Z` pushas.

GitHub-taggen skickas till byggscriptet som `NATURRESERVATET_VERSION`.

Skapar:

- release-zip i `release/`
- separata PDF-assets från `output/print/`
- `PRINT_MANIFEST.json`

## Lokal körning

```bash
python scripts/build_print.py
python scripts/validate_project.py
python -m unittest discover -s tests -v
python scripts/package_release.py
```

## Output-policy

`output/` och `release/` är genererade kataloger och ska normalt inte checkas in.
