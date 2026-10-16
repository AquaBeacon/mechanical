"""Focused tests for read-only CAD planning and source snapshots."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "cad_foundation" / "cli.py"
SPEC = importlib.util.spec_from_file_location("cad_foundation_cli", MODULE_PATH)
cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cli)


class CadFoundationPlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.placement_dir = self.root / "assemblies" / "demo"
        self.placement_dir.mkdir(parents=True)
        self.parts = self.root / "parts" / "demo"
        plate = self.parts / "plate"
        variant = self.parts / "variant"
        plate.mkdir(parents=True)
        variant.mkdir(parents=True)
        (plate / "plate.step").write_bytes(b"step original")
        (plate / "plate.stl").write_bytes(b"mesh reference")
        (variant / "variant.STEP").write_bytes(b"variant step")
        self.placement_path = self.placement_dir / "placement.json"
        self.data = {
            "name": "Demo assembly", "units": "mm",
            "parts": [
                {"part": "parts/demo/plate", "label": "legacy plate", "group": "frame",
                 "ops": [{"translate": [1, 2, 3]}]},
                {"part": "parts/demo/variant", "file": "variant", "group": "preview",
                 "ops": [{"mirror": [0, 0, 1]}, {"scale": [1, 1, 1]}]},
            ],
        }
        self.write_data()

    def tearDown(self):
        self.temp.cleanup()

    def write_data(self):
        self.placement_path.write_text(json.dumps(self.data), encoding="utf-8")

    def test_legacy_parts_variants_groups_order_and_references(self):
        plan = cli.make_plan(self.root, self.placement_dir)
        self.assertEqual(plan["placement"], "assemblies/demo/placement.json")
        self.assertEqual(plan["component_count"], 2)
        self.assertEqual([row["index"] for row in plan["entries"]], [0, 1])
        self.assertEqual([row["group"] for row in plan["entries"]], ["frame", "preview"])
        first, second = plan["entries"]
        self.assertEqual(first["source"], "parts/demo/plate/plate.step")
        self.assertEqual(first["stl_reference"], "parts/demo/plate/plate.stl")
        self.assertEqual(first["editability"], "imported_brep")
        self.assertEqual(second["file"], "variant")
        self.assertEqual(second["source"], "parts/demo/variant/variant.STEP")
        self.assertEqual(second["ops"], [{"mirror": [0, 0, 1]}, {"scale": [1, 1, 1]}])

    def test_missing_component_is_reported_in_plan(self):
        self.data["parts"].append({"part": "parts/demo/plate", "file": "absent"})
        self.write_data()
        plan = cli.make_plan(self.root, self.placement_path)
        self.assertEqual([Path(p).as_posix() for p in plan["missing"]],
                         ["parts/demo/plate/absent"])
        self.assertIsNone(plan["entries"][-1]["source"])

    def test_escaped_part_path_is_rejected(self):
        self.data["parts"][0]["part"] = "../outside"
        self.write_data()
        with self.assertRaisesRegex(ValueError, "leaves repository"):
            cli.make_plan(self.root, self.placement_path)

    def test_invalid_transforms_are_rejected(self):
        bad_ops = [
            [{"translate": [1, 2]}],
            [{"translate": [1, float("nan"), 3]}],
            [{"rotate": [1, float("inf"), 0]}],
            [{"scale": [1, 0, 1]}],
            [{"scale": [1, 1e-12, 1]}],
            [{"mirror": [0, 0, 0]}],
            [{"shear": [1, 0, 0]}],
            [{"translate": [1, 2, 3], "scale": [1, 1, 1]}],
        ]
        for ops in bad_ops:
            with self.subTest(ops=ops):
                self.data["parts"][0]["ops"] = ops
                self.write_data()
                with self.assertRaises(ValueError):
                    cli.make_plan(self.root, self.placement_path)

    def test_plan_is_read_only(self):
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        plan = cli.make_plan(self.root, self.placement_path)
        after = {p.relative_to(self.root).as_posix(): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertTrue(plan["entries"])

    def test_snapshot_copies_inputs_and_preserves_sources(self):
        plan = cli.make_plan(self.root, self.placement_path)
        sources_before = {relative: (self.root / relative).read_bytes()
                          for relative in (plan["placement"], "parts/demo/plate/plate.step",
                                           "parts/demo/plate/plate.stl", "parts/demo/variant/variant.STEP")}
        run = self.root / "run"
        (run / "intermediate").mkdir(parents=True)
        snapshots = cli.snapshot_inputs(self.root, run, plan)
        self.assertEqual(set(snapshots), set(sources_before))
        for relative, original in sources_before.items():
            record = snapshots[relative]
            self.assertEqual(Path(record["path"]).read_bytes(), original)
            self.assertEqual(record["sha256"], cli.digest(self.root / relative))
            self.assertEqual((self.root / relative).read_bytes(), original)

    def test_layout_edit_after_plan_is_rejected(self):
        plan = cli.make_plan(self.root, self.placement_path)
        self.data["parts"][0]["ops"] = [{"translate": [9, 8, 7]}]
        self.write_data()
        run = self.root / "run"
        (run / "intermediate").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "placement changed"):
            cli.snapshot_inputs(self.root, run, plan)

    def test_concurrent_source_edit_during_copy_is_rejected(self):
        plan = cli.make_plan(self.root, self.placement_path)
        run = self.root / "run"
        (run / "intermediate").mkdir(parents=True)
        original_copy = cli.shutil.copyfile

        def concurrent_copy(source, target):
            original_copy(source, target)
            if Path(source).suffix == ".step":
                Path(source).write_bytes(b"concurrently edited CAD")

        with patch.object(cli.shutil, "copyfile", side_effect=concurrent_copy):
            with self.assertRaisesRegex(ValueError, "input changed during snapshot"):
                cli.snapshot_inputs(self.root, run, plan)


if __name__ == "__main__":
    unittest.main()
