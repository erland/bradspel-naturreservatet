#!/usr/bin/env python3
"""Build all printable PDFs and copy them to a preview/dist directory."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def version() -> str:
    return str(yaml.safe_load((ROOT / "data/game.yaml").read_text(encoding="utf-8"))["game"]["version"])


def inspect_pdf(path: Path) -> dict:
    reader = PdfReader(str(path))
    return {
        "file": path.name,
        "pages": len(reader.pages),
        "bytes": path.stat().st_size,
    }


def expected_pdfs(ver: str) -> list[tuple[Path, str]]:
    return [
        (ROOT / "output/print" / f"landskapsbrickor-70x35mm-v{ver}.pdf", f"naturreservatet-landskapsbrickor-v{ver}.pdf"),
        (ROOT / "output/print" / f"reference-card-a6-v2-v{ver}.pdf", f"naturreservatet-referenskort-a6-v{ver}.pdf"),
        (ROOT / "output/print" / f"reference-card-a6-v2-a4-4up-v{ver}.pdf", f"naturreservatet-referenskort-a4-4up-v{ver}.pdf"),
        (ROOT / "output/print/score-sheet-a6.pdf", f"naturreservatet-poangblad-a6-v{ver}.pdf"),
        (ROOT / "output/print/score-sheets-a4.pdf", f"naturreservatet-poangblad-a4-4up-v{ver}.pdf"),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    out = Path(args.output_dir).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    run([sys.executable, "scripts/build_landscape_tiles.py"])
    run([sys.executable, "scripts/build_reference_card_v2.py"])
    run([sys.executable, "scripts/build_score_sheets.py"])

    ver = version()
    manifest = {
        "project": "Naturreservatet",
        "version": ver,
        "type": "print-preview",
        "pdfs": [],
    }

    for src, dest_name in expected_pdfs(ver):
        if not src.exists():
            raise FileNotFoundError(src)
        info = inspect_pdf(src)
        dest = out / dest_name
        shutil.copy2(src, dest)
        info["artifact_name"] = dest.name
        manifest["pdfs"].append(info)

    (out / "PRINT_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
