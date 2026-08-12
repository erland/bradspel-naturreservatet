#!/usr/bin/env python3
"""Package a clean printable release for Naturreservatet."""
from __future__ import annotations

from pathlib import Path
import json
import shutil
import subprocess
import sys
import zipfile

from build_version import get_build_version

ROOT = Path(__file__).resolve().parents[1]
VERSION = get_build_version(ROOT)
RELEASE_ROOT = ROOT / "release" / f"v{VERSION}"
PRINT_OUT = ROOT / "output" / "print"

def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_print.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_project.py")], check=True)

    if RELEASE_ROOT.exists():
        shutil.rmtree(RELEASE_ROOT)
    RELEASE_ROOT.mkdir(parents=True, exist_ok=True)

    print_dir = RELEASE_ROOT / "print"
    print_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads((PRINT_OUT / "PRINT_MANIFEST.json").read_text(encoding="utf-8"))
    for item in manifest["print_files"]:
        src = ROOT / item["path"]
        shutil.copy2(src, print_dir / src.name)

    (RELEASE_ROOT / "PRINT_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        f"# Naturreservatet v{VERSION} print release",
        "",
        "Skriv ut PDF-filer i `print/` i faktisk storlek, 100 %.",
        "",
        "## Innehåll",
        "",
    ]
    for item in manifest["print_files"]:
        lines.append(f"- `{Path(item['path']).name}` ({item['pages']} sidor)")
    (RELEASE_ROOT / "README_RELEASE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    zip_path = ROOT / "release" / f"naturreservatet-v{VERSION}-print-release.zip"
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for file in RELEASE_ROOT.rglob("*"):
            if file.is_file():
                z.write(file, file.relative_to(RELEASE_ROOT.parent))

    print(zip_path)

if __name__ == "__main__":
    main()
