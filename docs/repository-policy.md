# Repository policy

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

## Versioner

Fallback-versionen finns i:

```text
data/game.yaml
```

Vid GitHub-release kan git-taggen ersätta fallback-versionen genom miljövariabeln `NATURRESERVATET_VERSION`.

## Regelbok

Regelbokens källa är:

```text
docs/rulebook.md
```

PDF-versionen byggs med Pandoc till `output/print/`.
