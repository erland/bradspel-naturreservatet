#!/usr/bin/env python3
"""Build the Naturreservatet rulebook PDF from docs/rulebook.md using Pandoc."""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
GAME = yaml.safe_load((ROOT / "data/game.yaml").read_text(encoding="utf-8"))["game"]
VERSION = str(GAME["version"])
SOURCE = ROOT / "docs/rulebook.md"
OUT_DIR = ROOT / "output/print"
OUT = OUT_DIR / f"regelbok-v{VERSION}.pdf"

def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source: {SOURCE}")

    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("Pandoc is required to build the rulebook PDF.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        pandoc,
        str(SOURCE),
        "-o", str(OUT),
        "--pdf-engine=xelatex",
        "-V", "documentclass=article",
        "-V", "geometry:margin=18mm",
        "-V", "fontsize=10pt",
        "-V", "mainfont=DejaVu Serif",
        "-V", "sansfont=DejaVu Sans",
        "-V", "monofont=DejaVu Sans Mono",
        "-V", "colorlinks=true",
        "-V", "linkcolor=black",
        "-V", "urlcolor=black",
        "--metadata", f"title=Naturreservatet regelbok v{VERSION}",
    ]
    subprocess.run(cmd, check=True)
    print(OUT)

if __name__ == "__main__":
    main()
