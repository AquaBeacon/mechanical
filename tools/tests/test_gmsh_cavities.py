"""Regression: a hollow STL must not become solid material during tet meshing."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(all(importlib.util.find_spec(p) for p in ('gmsh','topopt','trimesh')),
                     'native Gmsh/topopt and trimesh required')
class CavityImportTests(unittest.TestCase):
    def test_one_material_volume_keeps_inner_void(self):
        import trimesh
        from topopt import ccx
        root=Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory(prefix='body-models-gmsh-cavity-') as folder:
            directory=Path(folder)
            outer=trimesh.creation.box(extents=[10,10,10])
            cavity=trimesh.creation.box(extents=[6,6,6]); cavity.invert()
            source=directory/'hollow.stl'
            trimesh.util.concatenate([outer,cavity]).export(source)
            refined=directory/'refined.stl'
            ccx.refine_stl(str(source),str(refined),2.0)
            geo=directory/'hollow.geo'; mesh_path=directory/'hollow.inp'
            ccx.write_geo(str(geo),str(refined),2.0)
            result=subprocess.run([sys.executable,str(root/'tools/gmsh_clamp_delaunay.py'),
                                   str(geo),'-3','-format','inp','-o',str(mesh_path)],
                                  capture_output=True,text=True,timeout=60)
            self.assertEqual(result.returncode,0,result.stdout[-3000:]+result.stderr[-3000:])
            mesh=ccx.read_mesh(str(mesh_path))
            mass=ccx.mass_properties(mesh['xyz'],mesh['elements'],1270,ids=mesh['ids'])
            self.assertAlmostEqual(mass['volume_mm3'],784.0,places=3)
            self.assertLess(mass['volume_mm3'],1000.0)


if __name__=='__main__':
    unittest.main()
