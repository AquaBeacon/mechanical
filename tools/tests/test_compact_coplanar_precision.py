"""Large CAD plates must retain doubles during the STEP input cleanup."""
import sys, tempfile, unittest
from pathlib import Path
import numpy as np
import trimesh

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from compact_coplanar_mesh import compact

class CoplanarPrecisionTests(unittest.TestCase):
    def test_large_fractional_plate_preserves_volume(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            source=root / "source.stl"
            target=root / "step_input.stl"
            original=trimesh.creation.box(extents=[232,134,11.2])
            original.apply_translation([0.13,0.37,-12.0])
            original.export(source,file_type="stl_ascii")
            data=compact(source,target,root / "report.json")
            actual=trimesh.load(target,force="mesh")
            self.assertTrue(actual.is_volume)
            self.assertLess(abs(original.volume-actual.volume),0.001)
            self.assertLess(np.max(np.abs(original.bounds-actual.bounds)),0.001)
            self.assertEqual(data["export_format"],"asciistl")
            self.assertTrue(target.read_text(encoding="ascii").startswith("solid"))

if __name__=="__main__":
    unittest.main()
