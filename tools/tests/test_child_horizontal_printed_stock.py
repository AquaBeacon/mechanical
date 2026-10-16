"""Printed-stock recertification must reject a geometric change before dating it."""
import sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import trimesh

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import prepare_child_horizontal_plate_frame as frame


class PrintedStockTests(unittest.TestCase):
    def test_equivalent_render_preserves_original_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);original=root/'original.stl';candidate=root/'candidate.stl'
            mesh=trimesh.creation.box([10,20,30]);mesh.export(original)
            # Vertex ordering is not part of the functional geometry.
            mesh.faces=mesh.faces[::-1];mesh.export(candidate)
            before=original.read_bytes()
            with patch.object(frame,'ROOT',root),patch.object(frame,'weld'),patch.object(frame,'clean'):
                report=frame.verify_printed_render(original,candidate)
            self.assertEqual(before,original.read_bytes())
            self.assertEqual(report['bidirectional_vertex_error_mm'],0)
            self.assertTrue(candidate.with_suffix('.equivalence.json').exists())

    def test_changed_shape_rejected_without_refreshing_original(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);original=root/'original.stl';candidate=root/'candidate.stl'
            trimesh.creation.box([10,20,30]).export(original)
            trimesh.creation.box([10,20,31]).export(candidate)
            before=original.read_bytes();timestamp=original.stat().st_mtime_ns
            with patch.object(frame,'ROOT',root),patch.object(frame,'weld'),patch.object(frame,'clean'):
                with self.assertRaisesRegex(RuntimeError,'changed printed stock'):
                    frame.verify_printed_render(original,candidate)
            self.assertEqual(before,original.read_bytes())
            self.assertEqual(timestamp,original.stat().st_mtime_ns)
            self.assertFalse(candidate.with_suffix('.equivalence.json').exists())


if __name__=='__main__':unittest.main()
