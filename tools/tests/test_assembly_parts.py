"""Behavior checks for standalone packaging, quantity, mirrors and source drift."""
import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import trimesh

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import assembly_parts as ap


class PrintBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.scope = patch.object(ap, "ROOT", self.root)
        self.scope.start()
        self.part = "parts/child/interior/printed/bracket"
        self.folder = self.root / self.part
        self.folder.mkdir(parents=True)
        self.mesh = trimesh.creation.box(extents=[3, 5, 7])
        self.mesh.apply_translation([12, 23, 34])
        self.mesh.export(self.folder / "bracket.stl")
        (self.folder / "bracket.scad").write_text("cube([3,5,7]);\n")
        self.assembly = self.root / "assemblies" / "fixture"
        self.assembly.mkdir(parents=True)

    def tearDown(self):
        self.scope.stop()
        self.temp.cleanup()

    def placement(self, items, key="items"):
        ap.write_json(self.assembly / "placement.json", {"name": "fixture", key: items})

    def item(self, **extra):
        return {"part": self.part, **extra}

    def test_quantities_and_reflections_are_separate(self):
        self.placement([self.item(label="a"), self.item(label="b"), self.item(label="left", ops=[{"mirror": [1, 0, 0]}])])
        entries, _ = ap.definitions(self.assembly)
        self.assertEqual([e["quantity"] for e in entries], [2, 1])
        self.assertEqual(entries[1]["file"], "bracket_mirrored.stl")

    def test_cots_and_documented_non_print_models_are_excluded(self):
        ap.write_json(self.folder / "manufacturing.json", {"non_print_files": ["foam"]})
        self.placement([self.item(), self.item(file="foam"), {"part": "parts/common/interior/cots/screw"}])
        entries, _ = ap.definitions(self.assembly)
        self.assertEqual(len(entries), 1)

    def test_legacy_parts_schema_and_standalone_copy(self):
        self.placement([self.item()], key="parts")
        ap.build(self.assembly)
        manifest = ap.read(self.assembly / "parts/manifest.json")
        self.assertEqual(manifest["parts"][0]["quantity"], 1)
        portable = self.root / "portable"
        shutil.copytree(self.assembly / "parts", portable)
        shutil.rmtree(self.folder)
        mesh = trimesh.load(portable / "bracket.stl", force="mesh")
        self.assertTrue(mesh.is_watertight)
        np.testing.assert_allclose(mesh.bounds[0], [0, 0, 0])
        self.assertFalse(any(p.suffix == ".scad" for p in portable.rglob("*")))

    def test_print_rotation_and_modifier_keep_relative_position(self):
        self.placement([self.item()])
        ap.write_json(self.folder / "manufacturing.json", {"print_rotations_deg": {"bracket": [90, 0, 0]}})
        modifier = self.mesh.copy()
        modifier.export(self.root / "modifier.stl")
        ap.write_json(self.assembly / "print_config.json", {"modifiers": [{"host": "bracket", "source": "modifier.stl"}]})
        ap.build(self.assembly)
        host = trimesh.load(self.assembly / "parts/bracket.stl", force="mesh")
        mod = trimesh.load(self.assembly / "parts/modifiers/modifier.stl", force="mesh")
        np.testing.assert_allclose(host.bounds, mod.bounds)
        np.testing.assert_allclose(host.extents, [3, 7, 5])
        self.assertEqual(ap.check(self.assembly), [])

    def test_copy_source_quantity_and_cad_drift_are_detected(self):
        self.placement([self.item()])
        ap.build(self.assembly)
        self.assertEqual(ap.check(self.assembly), [])
        target = self.assembly / "parts/bracket.stl"
        target.write_bytes(target.read_bytes() + b"changed")
        self.assertTrue(any("copy changed" in e for e in ap.check(self.assembly)))
        ap.build(self.assembly)
        self.placement([self.item(), self.item()])
        self.assertTrue(any("placement/config" in e for e in ap.check(self.assembly)))
        ap.build(self.assembly)
        cad = self.folder / "bracket.scad"
        cad.write_text("cube([3,5,8]);\n")
        os.utime(cad, (time.time() + 2, time.time() + 2))
        self.assertTrue(any("sources changed" in e for e in ap.check(self.assembly)))
        with self.assertRaisesRegex(ValueError, "rebuild STL"):
            ap.build(self.assembly)

    def test_scaled_reflection_preserves_metric_and_handedness(self):
        shape = ap.linear_matrix([{"rotate": [30, 40, 50]}, {"scale": [2, 3, 4]}, {"rotate": [10, 20, 30]}, {"mirror": [0, 1, 0]}])
        self.assertLess(np.linalg.det(shape), 0)
        np.testing.assert_allclose(sorted(np.linalg.svd(shape)[1]), [2, 3, 4], atol=1e-8)
        np.testing.assert_allclose(ap.linear_matrix([{"rotate": [45, 60, 30]}]), np.eye(3), atol=1e-8)

    def test_export_precision_preserves_a_closed_mesh_after_bed_translation(self):
        # The short edge is distinct near zero, but float32 collapses it at X100.
        mesh = trimesh.Trimesh([[-100, -1, -1], [0, 0, 0], [1e-6, 0, 0], [0, 0, 1]],
                              [[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3]])
        mesh.fix_normals()
        mesh.export(self.folder / "bracket.stl")
        self.placement([self.item()])
        with self.assertRaisesRegex(ValueError, "invalid exported print mesh"):
            ap.build(self.assembly)
        ap.write_json(self.folder / "manufacturing.json", {"portable_stl_export_format": "stl_ascii"})
        ap.build(self.assembly)
        packed = trimesh.load(self.assembly / "parts/bracket.stl", force="mesh")
        self.assertTrue(packed.is_volume)
        self.assertEqual(packed.euler_number, mesh.euler_number)
        self.assertAlmostEqual(packed.volume, mesh.volume, places=12)
        self.assertEqual(ap.check(self.assembly), [])

    def test_imported_topology_mesh_requires_regeneration_before_sync(self):
        source = self.folder / "spec/surface.stl"
        source.parent.mkdir()
        self.mesh.export(source)
        ap.write_json(self.folder / "manufacturing.json", {"source_dependencies": ["spec/surface.stl"]})
        self.placement([self.item()])
        ap.build(self.assembly)
        changed = self.mesh.copy()
        changed.apply_translation([1, 0, 0])
        changed.export(source)
        os.utime(source, (time.time() + 2, time.time() + 2))
        self.assertTrue(any("sources changed" in e for e in ap.check(self.assembly)))
        with self.assertRaisesRegex(ValueError, "rebuild STL"):
            ap.build(self.assembly)

    def test_path_escape_and_unmanaged_files_are_rejected(self):
        with self.assertRaises(ValueError):
            ap.source_path("../outside", "bracket")
        self.placement([self.item()])
        ap.build(self.assembly)
        (self.assembly / "parts/untracked.stl").write_bytes(b"unknown")
        self.assertTrue(any("unmanaged" in e for e in ap.check(self.assembly)))


if __name__ == "__main__":
    unittest.main()
