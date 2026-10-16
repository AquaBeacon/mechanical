"""Small synthetic FreeCAD integration: no production files or GUI touched."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
FREECAD = Path(os.environ.get("FREECADCMD", str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/FreeCAD 1.0/bin/freecadcmd.exe")))

PROBE = r'''
import os, sys, json
from pathlib import Path
import FreeCAD as App, Part, Mesh
root = Path(os.environ['PROBE_ROOT'])
scratch = Path(os.environ['PROBE_SCRATCH'])
sys.path.insert(0, str(root / 'tools/cad_foundation'))
from freecad_worker import matrix_for, run
from cli import digest

def close_enough(a, b):
    assert max(abs(x-y) for x,y in zip(a,b)) < 1e-5, (a,b)

ops = [{'translate':[10,20,30]}, {'rotate':[0,0,90]}, {'scale':[2,3,1]}]
v = matrix_for(ops).multVec(App.Vector(1,2,3))
close_enough([v.x,v.y,v.z], [4,22,33])
v = matrix_for([{'mirror':[1,0,0]}]).multVec(App.Vector(1,2,3))
close_enough([v.x,v.y,v.z], [-1,2,3])
box = Part.makeBox(1,2,3)
box.exportStep(str(scratch/'box.step'))
box.exportStl(str(scratch/'box.stl'))
snapshots = {name: {'path':str(scratch/name), 'sha256':digest(scratch/name)} for name in ('box.step','box.stl')}
entries=[]
for i, (source, transforms) in enumerate([
    ('box.step', ops), ('box.step',[{'translate':[5,0,0]},{'mirror':[1,0,0]}]),
    ('box.step',[{'translate':[5,0,0]},{'rotate':[0,0,90]}]),
    ('box.stl', ops)]):
    entries.append(dict(index=i,label='instance '+str(i),source=source,stl_reference='box.stl',ops=transforms,
        group='demo',editability='mesh_reference' if source.endswith('stl') else 'imported_brep'))
out=scratch/'result';out.mkdir()
job=dict(name='Synthetic',run_id='test',run_dir=str(out),kind='assembly',entries=entries,snapshots=snapshots)
result=run(job)
assert result['component_count']==4
for name, expected, volume in [
    ('Component0000',[4,20,30,10,22,33],36),
    ('Component0001',[4,0,0,5,2,3],6),
    ('Component0002',[3,0,0,5,1,3],6),
    ('Component0003',[4,20,30,10,22,33],36)]:
    m=result['components'][name]
    close_enough(m['bbox_mm'],expected)
    assert abs(m['volume_mm3']-volume)<1e-5, m
before=digest(out/'model.FCStd')
try: run(job)
except ValueError as error: assert 'overwrite' in str(error)
else: raise AssertionError('existing document was overwritten')
assert before==digest(out/'model.FCStd')
# A shifted vendor STEP must fail consistency checks instead of silently moving the assembly.
bad=Part.makeBox(1,2,3,App.Vector(100,0,0))
bad.exportStep(str(scratch/'bad.step'))
snapshots['box.step']={'path':str(scratch/'bad.step'),'sha256':digest(scratch/'bad.step')}
badout=scratch/'badresult';badout.mkdir();job['run_dir']=str(badout)
try: run(job)
except ValueError as error: assert 'STEP/STL mismatch' in str(error)
else: raise AssertionError('mismatched STEP was accepted')
assert not (badout/'model.FCStd').exists()
(scratch/'passed.json').write_text(json.dumps({'passed': True,'cases': ['transform_order','reflection','rigid_placement','mesh_reference','readback','no_overwrite','step_stl_mismatch']}))
'''


@unittest.skipUnless(FREECAD.is_file(), "FreeCADCmd is unavailable")
class CadFoundationFreeCADTests(unittest.TestCase):
    def test_transforms_readback_and_rejections(self):
        with tempfile.TemporaryDirectory() as folder:
            scratch = Path(folder)
            script = scratch / "probe.py"
            script.write_text(PROBE, encoding="utf-8")
            env = os.environ.copy()
            env.pop("CAD_FOUNDATION_JOB", None)
            env.update(PROBE_ROOT=str(ROOT), PROBE_SCRATCH=str(scratch))
            result = subprocess.run([str(FREECAD), "-u", str(scratch/"user.cfg"), "-s", str(scratch/"system.cfg"), str(script)],
                                    env=env, capture_output=True, encoding="utf-8", errors="replace", timeout=45,
                                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            receipt = scratch / "passed.json"
            self.assertTrue(receipt.exists(), result.stdout + result.stderr)
            self.assertTrue(json.loads(receipt.read_text())["passed"])


if __name__ == "__main__":
    unittest.main()
