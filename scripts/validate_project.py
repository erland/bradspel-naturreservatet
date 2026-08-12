#!/usr/bin/env python3
"""Validate Naturreservatet project consistency."""
from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys

import yaml
from pypdf import PdfReader

from build_version import get_build_version

VERSION_PATTERN = re.compile(r"\bv\d+\.\d+\.\d+\b|(?<![\d.])\d+\.\d+\.\d+(?![\d.])")
VERSION_ALLOWLIST = {
    "data/game.yaml",
    "CHANGELOG.md",
    "scripts/validate_project.py",
    "scripts/build_version.py",
}

SOURCE_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".json"}

def error(errors: list[str], message: str) -> None:
    errors.append(message)
    print(f"ERROR: {message}", file=sys.stderr)

def pdf_pages(path: Path, errors: list[str]) -> int:
    try:
        reader = PdfReader(str(path))
        pages = len(reader.pages)
        if pages < 1:
            error(errors, f"Tom PDF: {path}")
        return pages
    except Exception as exc:
        error(errors, f"Ogiltig PDF {path}: {exc}")
        return 0

def relpath(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()

def check_hardcoded_versions(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = relpath(root, path)
        if rel.startswith(("output/", "release/", ".git/")):
            continue
        if path.suffix not in SOURCE_SUFFIXES:
            continue
        if rel in VERSION_ALLOWLIST:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        matches = sorted(set(VERSION_PATTERN.findall(text)))
        if matches:
            error(errors, f"Hårdkodade versionsnummer i {rel}: {matches}")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []

    required_paths = [
        "README.md",
        "PROJECT_STATUS.md",
        "CHANGELOG.md",
        ".gitignore",
        "docs/rulebook.md",
        "docs/production-guide.md",
        "docs/reference-card-v2.md",
        "docs/repository-policy.md",
        "docs/github-actions-and-release.md",
        "data/game.yaml",
        "data/tiles.yaml",
        "data/animals.yaml",
        "data/style.yaml",
        "data/reference-card-v2.yaml",
        "assets/icons/forest.svg",
        "assets/icons/lake.svg",
        "assets/icons/meadow.svg",
        "assets/icons/mountain.svg",
        "assets/icons/wetland.svg",
        "assets/icons/any-terrain.svg",
        "scripts/build_version.py",
        "scripts/build_landscape_tiles.py",
        "scripts/build_reference_card_v2.py",
        "scripts/build_score_sheets.py",
        "scripts/build_rulebook_pdf.py",
        "scripts/build_print.py",
        "scripts/package_release.py",
        "scripts/validate_project.py",
        ".github/workflows/01-validate.yml",
        ".github/workflows/02-build-preview.yml",
        ".github/workflows/03-release.yml",
    ]

    for rel in required_paths:
        if not (root / rel).exists():
            error(errors, f"Obligatorisk sökväg saknas: {rel}")

    if errors:
        return 1

    game = yaml.safe_load((root / "data/game.yaml").read_text(encoding="utf-8"))["game"]
    tiles_data = yaml.safe_load((root / "data/tiles.yaml").read_text(encoding="utf-8"))
    animals = yaml.safe_load((root / "data/animals.yaml").read_text(encoding="utf-8"))["animals"]
    style = yaml.safe_load((root / "data/style.yaml").read_text(encoding="utf-8"))
    ref = yaml.safe_load((root / "data/reference-card-v2.yaml").read_text(encoding="utf-8"))

    version = get_build_version(root)

    if "version" in style:
        error(errors, "data/style.yaml ska inte innehålla versionsnummer.")
    if "version" in ref:
        error(errors, "data/reference-card-v2.yaml ska inte innehålla versionsnummer.")
    if str(game.get("version", "")) != version and "NATURRESERVATET_VERSION" not in __import__("os").environ:
        error(errors, "Fallback-versionen i data/game.yaml matchar inte build-versionen.")

    tiles = tiles_data["tiles"]
    ids = [t["id"] for t in tiles]
    if len(ids) != 32:
        error(errors, f"Förväntade 32 brickor, fann {len(ids)}.")
    if len(ids) != len(set(ids)):
        error(errors, "Brick-ID:n är inte unika.")

    if len(animals) != 6:
        error(errors, f"Förväntade 6 djur, fann {len(animals)}.")
    if len(ref["animals"]) != 6:
        error(errors, "Referenskortet innehåller inte 6 djur.")

    valid_ids = set(ids)
    for key, expected in [("2_players", 16), ("3_players", 24), ("4_players", 32)]:
        vals = tiles_data["player_count_sets"][key]["tile_ids"]
        if len(vals) != expected:
            error(errors, f"{key}: förväntade {expected}, fann {len(vals)}.")
        unknown = sorted(set(vals) - valid_ids)
        if unknown:
            error(errors, f"{key}: okända brick-ID:n: {unknown}.")

    rulebook = (root / "docs/rulebook.md").read_text(encoding="utf-8")
    if rulebook.lstrip().startswith("# Naturreservatet v"):
        error(errors, "Regelbokens huvudrubrik ska inte innehålla versionsnummer.")
    if "startbricka" in rulebook.lower() or "startfält" in rulebook.lower():
        error(errors, "Regelboken innehåller kvarvarande hänvisning till startbricka/startfält.")

    expected_pdfs = [
        root / "output/print" / f"landskapsbrickor-70x35mm-v{version}.pdf",
        root / "output/print" / f"reference-card-a6-v2-v{version}.pdf",
        root / "output/print" / f"reference-card-a6-v2-a4-4up-v{version}.pdf",
        root / "output/print/score-sheet-a6.pdf",
        root / "output/print/score-sheets-a4.pdf",
        root / "output/print" / f"regelbok-v{version}.pdf",
    ]
    for p in expected_pdfs:
        if not p.exists():
            error(errors, f"Saknad print-PDF: {p.relative_to(root)}")
        else:
            pdf_pages(p, errors)

    check_hardcoded_versions(root, errors)

    if errors:
        print("VALIDERING MISSLYCKADES")
        return 1

    print("VALIDERING OK")
    print(f"Build-version: {version}")
    print(f"Brickor: {len(ids)}")
    print(f"Djur: {len(animals)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
