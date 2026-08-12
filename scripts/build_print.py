#!/usr/bin/env python3
"""Build all printable PDFs for Naturreservatet."""
from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys
import yaml
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/print"

def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / script)], check=True)

def pdf_pages(path: Path) -> int:
    return len(PdfReader(str(path)).pages)

def main() -> None:
    game = yaml.safe_load((ROOT / "data/game.yaml").read_text(encoding="utf-8"))["game"]
    version = str(game["version"])
    title = game.get("title", "Naturreservatet")
    OUT.mkdir(parents=True, exist_ok=True)

    run("build_landscape_tiles.py")
    run("build_reference_card_v2.py")
    run("build_score_sheets.py")
    run("build_rulebook_pdf.py")

    files = [
        OUT / f"landskapsbrickor-70x35mm-v{version}.pdf",
        OUT / f"reference-card-a6-v2-v{version}.pdf",
        OUT / f"reference-card-a6-v2-a4-4up-v{version}.pdf",
        OUT / "score-sheet-a6.pdf",
        OUT / "score-sheets-a4.pdf",
        OUT / f"regelbok-v{version}.pdf",
    ]

    missing = [str(path) for path in files if not path.exists()]
    if missing:
        raise SystemExit("Missing print files: " + ", ".join(missing))

    manifest = {
        "game": title,
        "version": version,
        "print_files": [
            {
                "path": str(path.relative_to(ROOT)),
                "pages": pdf_pages(path),
            }
            for path in files
        ],
    }
    (OUT / "PRINT_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
