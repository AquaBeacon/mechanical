import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tidy_workspace as tidy


class TidyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.scope = patch.object(tidy, "ROOT", self.root)
        self.scope.start()
        for name in ("parts", "assemblies", "print_jobs", "outputs", "spec", "tools"):
            (self.root / name).mkdir()
        self.owner = self.root / "assemblies/demo"
        self.owner.mkdir()

    def tearDown(self):
        self.scope.stop()
        self.temp.cleanup()

    def test_move_relinks_documents_and_preserves_model(self):
        (self.owner / "preview.png").write_bytes(b"image")
        (self.owner / "build.log").write_text("log")
        (self.owner / "demo.stl").write_bytes(b"model")
        (self.owner / "README.md").write_text("![Preview](preview.png)\n[Model](demo.stl)\n")
        tidy.apply(tidy.plan())
        self.assertEqual(tidy.plan(), [])
        self.assertEqual((self.owner / "demo.stl").read_bytes(), b"model")
        self.assertIn("_work/images/preview.png", (self.owner / "README.md").read_text())
        self.assertTrue((self.owner / "_work/logs/build.log").is_file())

    def test_legacy_rebuild_preserves_previous_image_and_is_idempotent(self):
        (self.owner / "preview.png").write_bytes(b"first")
        tidy.apply(tidy.plan())
        (self.owner / "preview.png").write_bytes(b"second")
        tidy.apply(tidy.plan())
        self.assertEqual((self.owner / "_work/images/preview.png").read_bytes(), b"second")
        self.assertEqual(len(list((self.owner / "_work/images/history").glob("*.png"))), 1)
        journal = self.root / "tools/_work/tidy_journal.json"
        previous = journal.read_bytes()
        tidy.apply(tidy.plan())
        self.assertEqual(journal.read_bytes(), previous)

    def test_missing_optional_output_roots_still_checks_assembly(self):
        (self.root / "outputs").rmdir()
        (self.root / "print_jobs").rmdir()
        (self.owner / "preview.png").write_bytes(b"image")
        moves = tidy.plan()
        self.assertEqual(moves, [(self.owner / "preview.png", self.owner / "_work/images/preview.png")])


if __name__ == "__main__":
    unittest.main()
