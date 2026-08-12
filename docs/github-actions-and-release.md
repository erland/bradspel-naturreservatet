# GitHub Actions och releaseflöde

Det här projektet använder tre workflows i `.github/workflows/`.

## 01-validate.yml

Körs vid pull request och push till `main` när projektfiler ändras.

Kontrollerar:

- obligatoriska filer
- YAML-konsistens
- versionsnummer
- 32 unika brickor
- 16/24/32-brickorsuppsättningar
- sex djur och sex referenskortsexempel
- att print-PDF:er finns och är läsbara
- automatiska spelmotortester

## 02-build-preview.yml

Körs manuellt via `workflow_dispatch`.

Bygger alla PDF:er som ska kunna skrivas ut och laddar upp ett gemensamt Actions-artifact:

`naturreservatet-print-preview`

Artifactet innehåller:

- landskapsbrickor
- A6-referenskort
- A4 med fyra referenskort
- A6-poängblad
- A4 med fyra poängblad
- `PRINT_MANIFEST.json`

## 03-release.yml

Körs när en tagg som börjar med `v` pushas, exempelvis:

```bash
git tag v0.3.4
git push origin v0.3.4
```

Workflowen:

1. validerar projektet
2. bygger all print-output
3. skapar ett rent releasepaket
4. skapar eller uppdaterar GitHub Release
5. laddar upp release-zip och PDF:er som separata assets

## Lokala kommandon

```bash
python -m pip install -r requirements.txt
python scripts/validate_project.py .
python -m unittest discover -s tests -v
python scripts/build_print.py --output-dir /tmp/naturreservatet-preview
python scripts/package_release.py --version v0.3.4 --output-dir /tmp/naturreservatet-release
```

## Princip

PDF-filer är rekommenderat printformat. SVG, YAML, Markdown och Python-script är källor eller källnära exportformat.
