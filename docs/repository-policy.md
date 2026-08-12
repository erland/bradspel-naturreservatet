# Repository policy v0.3.5

## Källa

Följande kataloger och filer är källmaterial och ska versionsstyras:

- `.github/`
- `assets/`
- `data/`
- `docs/`
- `scripts/`
- `templates/`
- `tests/`
- `README.md`
- `PROJECT_STATUS.md`
- `CHANGELOG.md`
- `requirements.txt`

## Genererad output

Följande kataloger är byggartefakter och behöver normalt inte versionsstyras:

- `output/`
- `release/`

De kan återskapas med:

```bash
python scripts/build_print.py
python scripts/package_release.py
```

## Regelbok

Regelbokens källa är `docs/rulebook.md`.

PDF-versionen byggs med Pandoc till:

```text
output/print/regelbok-v0.3.5.pdf
```
