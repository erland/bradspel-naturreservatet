#!/usr/bin/env python3
"""Resolve Naturreservatet build version.

Source fallback:
- data/game.yaml -> game.version

CI/release override:
- NATURRESERVATET_VERSION, often from a git tag such as vX.Y.Z

The returned version is normalized without a leading "v".
"""
from __future__ import annotations

from pathlib import Path
import os
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")

def normalize_version(value: str) -> str:
    version = str(value).strip()
    if version.startswith("refs/tags/"):
        version = version.removeprefix("refs/tags/")
    if version.startswith("v"):
        version = version[1:]
    if not VERSION_RE.match(version):
        raise ValueError(f"Invalid build version: {value!r}")
    return version

def get_build_version(root: Path = ROOT) -> str:
    override = os.environ.get("NATURRESERVATET_VERSION") or os.environ.get("GITHUB_REF_NAME")
    if override:
        return normalize_version(override)

    game = yaml.safe_load((root / "data/game.yaml").read_text(encoding="utf-8"))["game"]
    return normalize_version(str(game["version"]))

def get_game_title(root: Path = ROOT) -> str:
    game = yaml.safe_load((root / "data/game.yaml").read_text(encoding="utf-8"))["game"]
    return str(game.get("title", "Naturreservatet"))

if __name__ == "__main__":
    print(get_build_version())
