import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_version import get_build_version, normalize_version

class BuildVersionTests(unittest.TestCase):
    def tearDown(self):
        os.environ.pop("NATURRESERVATET_VERSION", None)
        os.environ.pop("GITHUB_REF_NAME", None)

    def test_ignores_github_ref_name_merge_ref(self):
        os.environ.pop("NATURRESERVATET_VERSION", None)
        os.environ["GITHUB_REF_NAME"] = "2/merge"
        self.assertRegex(get_build_version(ROOT), r"^\d+\.\d+\.\d+")

    def test_explicit_tag_override(self):
        os.environ["NATURRESERVATET_VERSION"] = "v9.9.9"
        os.environ["GITHUB_REF_NAME"] = "2/merge"
        self.assertEqual(get_build_version(ROOT), "9.9.9")

    def test_invalid_explicit_override_fails(self):
        os.environ["NATURRESERVATET_VERSION"] = "2/merge"
        with self.assertRaises(ValueError):
            get_build_version(ROOT)

    def test_normalize_refs_tags(self):
        self.assertEqual(normalize_version("refs/tags/v1.2.3"), "1.2.3")

if __name__ == "__main__":
    unittest.main()
