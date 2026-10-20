from __future__ import annotations

import hashlib
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "package_skill.py"
SPEC = importlib.util.spec_from_file_location("review_atlas_packager", SCRIPT_PATH)
PACKAGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGER)


class PackageTests(unittest.TestCase):
    def test_archive_contains_only_runtime_skill_files(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "review-atlas.skill"
            PACKAGER.write_archive(ROOT, destination)

            with zipfile.ZipFile(destination) as archive:
                names = archive.namelist()

            self.assertEqual(destination.stat().st_mode & 0o777, 0o644)
            self.assertIn("review-atlas/SKILL.md", names)
            self.assertIn("review-atlas/LICENSE", names)
            self.assertIn("review-atlas/assets/pr-review-template.md", names)
            self.assertIn("review-atlas/references/review-process.md", names)
            self.assertFalse(any("README.md" in name for name in names))
            self.assertFalse(any("/tests/" in name for name in names))
            self.assertFalse(any("/bin/" in name for name in names))
            self.assertFalse(any("/.git" in name for name in names))

    def test_archive_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = PACKAGER.write_archive(ROOT, root / "first.skill")
            second = PACKAGER.write_archive(ROOT, root / "second.skill")

            first_hash = hashlib.sha256(first.read_bytes()).hexdigest()
            second_hash = hashlib.sha256(second.read_bytes()).hexdigest()

            self.assertEqual(first_hash, second_hash)

    def test_validation_rejects_incomplete_source(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, "Missing required"):
                PACKAGER.write_archive(
                    Path(directory), Path(directory) / "review-atlas.skill"
                )


if __name__ == "__main__":
    unittest.main()
