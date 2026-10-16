"""FreeCAD integration checks for STL cavity and disconnected-solid semantics."""
from pathlib import Path
import json
import os
import subprocess
import tempfile
import unittest
import trimesh

ROOT=Path(__file__).resolve().parents[2]
FREECAD=Path(r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe')


@unittest.skipUnless(FREECAD.exists(), 'Configured FreeCAD CLI is unavailable')
class FacetedStepTests(unittest.TestCase):
    converter='scad/lib/stl_to_step.py'
    def convert(self, mesh):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            source=folder/'source.stl'
            destination=folder/'result.step'
            report=folder/'result.json'
            mesh.export(source)
            env=os.environ.copy()
            env.update(STL_IN=str(source),STEP_OUT=str(destination),PYTHONIOENCODING='utf-8')
            if self.converter.endswith('asm_to_step.py'):
                layout=folder/'placement.json'
                layout.write_text(json.dumps({'items':[{'part':'.','file':'source','label':'reference',
                    'group':'reference','ops':[{'translate':[3,4,5]}]}]}),encoding='utf-8')
                env.update(ASM_ROOT=str(folder),ASM_JSON=str(layout),ASM_GROUP='')
            run=subprocess.run([str(FREECAD),str(ROOT/self.converter)],env=env,
                               capture_output=True,encoding='utf-8',errors='replace',timeout=60)
            self.assertTrue(destination.exists(),run.stdout+run.stderr)
            probe=folder/'readback.py'
            probe.write_text('import os,json,Part\nfrom pathlib import Path\n'
                             's=Part.read(os.environ["STEP_OUT"])\n'
                             'Path(os.environ["STEP_REPORT"]).write_text(json.dumps(dict(valid=s.isValid(),volume=s.Volume,solids=len(s.Solids),shells=len(s.Shells))))\n',encoding='utf-8')
            env['STEP_REPORT']=str(report)
            run=subprocess.run([str(FREECAD),str(probe)],env=env,capture_output=True,
                               encoding='utf-8',errors='replace',timeout=60)
            self.assertTrue(report.exists(),run.stdout+run.stderr)
            return json.loads(report.read_text(encoding='utf-8'))

    def test_internal_void_remains_a_void_in_one_solid(self):
        outside=trimesh.creation.box([10,10,10])
        cavity=trimesh.creation.box([6,6,6])
        cavity.invert()
        result=self.convert(trimesh.util.concatenate([outside,cavity]))
        self.assertTrue(result['valid'])
        self.assertEqual(result['solids'],1)
        self.assertEqual(result['shells'],2)
        self.assertAlmostEqual(result['volume'],784,places=6)

    def test_disconnected_material_remains_two_solids(self):
        first=trimesh.creation.box([2,2,2])
        second=first.copy()
        second.apply_translation([10,0,0])
        result=self.convert(trimesh.util.concatenate([first,second]))
        self.assertTrue(result['valid'])
        self.assertEqual(result['solids'],2)
        self.assertAlmostEqual(result['volume'],16,places=6)


class AssemblyReferenceStepTests(FacetedStepTests):
    """The assembly STL fallback must preserve closed reference solids too."""
    converter='scad/lib/asm_to_step.py'


if __name__=='__main__':
    unittest.main()
