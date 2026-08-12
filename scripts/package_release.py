#!/usr/bin/env python3
"""Create a clean print release package for Naturreservatet."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def project_version() -> str:
    return str(yaml.safe_load((ROOT / "data/game.yaml").read_text(encoding="utf-8"))["game"]["version"])


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def pdf_info(path: Path) -> dict:
    reader = PdfReader(str(path))
    return {"file": path.name, "pages": len(reader.pages), "bytes": path.stat().st_size}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="", help="Release id, usually the Git tag, e.g. v0.3.4.")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    project_ver = project_version()
    release_id = args.version or f"v{project_ver}"

    dist = Path(args.output_dir).resolve()
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir(parents=True, exist_ok=True)

    run([sys.executable, "scripts/validate_project.py", "."])
    run([sys.executable, "scripts/build_print.py", "--output-dir", str(dist / "print/pdf")])

    release_root = dist / f"naturreservatet-{release_id}"
    release_root.mkdir(parents=True, exist_ok=True)
    (release_root / "print/pdf").mkdir(parents=True, exist_ok=True)
    (release_root / "docs").mkdir(parents=True, exist_ok=True)

    # Move/copy preview PDFs into release folder.
    for pdf in sorted((dist / "print/pdf").glob("*.pdf")):
        shutil.copy2(pdf, release_root / "print/pdf" / pdf.name)

    for rel in [
        "README.md",
        "PROJECT_STATUS.md",
        "CHANGELOG.md",
        "docs/rulebook.md",
        "docs/production-guide.md",
        "docs/reference-card-v2.md",
        "docs/score-sheet.md",
    ]:
        src = ROOT / rel
        if src.exists():
            dest = release_root / "docs" / Path(rel).name if rel.startswith("docs/") else release_root / Path(rel).name
            shutil.copy2(src, dest)

    pdfs = [pdf_info(p) for p in sorted((release_root / "print/pdf").glob("*.pdf"))]
    manifest = {
        "project": "Naturreservatet",
        "project_version": project_ver,
        "release_id": release_id,
        "recommended_print_format": "PDF",
        "pdfs": pdfs,
        "source_note": "PDF-filerna är genererad output. Källor finns i projektets data/docs/assets/scripts.",
    }
    (release_root / "RELEASE_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (release_root / "README.md").write_text(
        f"""# Naturreservatet {release_id}

Detta är ett rent print-and-play-releasepaket.

## Skriv ut

Använd PDF-filerna i `print/pdf/`.

Skriv ut i faktisk storlek, 100 %, utan “anpassa till sida”.

## Innehåll

- landskapsbrickor
- visuellt A6-referenskort
- A4 med fyra referenskort
- A6-poängblad
- A4 med fyra poängblad
- regel- och produktionsdokumentation

Se `RELEASE_MANIFEST.json` för exakt fillista.
""",
        encoding="utf-8",
    )

    zip_path = dist / f"naturreservatet-{release_id}-print-release.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in release_root.rglob("*"):
            if p.is_file():
                z.write(p, p.relative_to(release_root.parent))

    print(json.dumps({"release_zip": str(zip_path), "manifest": manifest}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
