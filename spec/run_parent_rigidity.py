"""Snapshot inputs, run existing topopt CLI, retain real exit status and logs."""
import json,shutil,subprocess,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service/rigidity'
name=sys.argv[1] if len(sys.argv)>1 else 'iteration_02'
assert name.startswith('iteration_') and '/' not in name and '\\' not in name
D=O/name;D.mkdir(exist_ok=False)
P=R/'parts/parent/interior/printed/parent_hand_service'
for ext in ['step','stl']:shutil.copy2(P/('lift_carrier.'+ext),D/('carrier.'+ext))
d=json.loads((O/'revised_study.json').read_text());d['part']='carrier.stl'
(D/'study.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
adapter='run_ccx_native_step.py' if '--native-step' in sys.argv else 'run_ccx_delaunay.py' if '--delaunay' in sys.argv else None
if adapter:shutil.copy2(R/'spec'/adapter,D/'mesher_adapter.py')
hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in D.iterdir() if f.is_file()}
entry=[sys.executable,'-u',str(D/'mesher_adapter.py')] if adapter else [sys.executable,'-u','-m','topopt','ccx']
screen='--screen' in sys.argv
cmd=entry+[str(D/'carrier.stl'),'--study',str(D/'study.json'),'--out',str(D/'ccx'),'--mesh-mm','8' if screen else '4']+([] if screen else ['--converge'])
(D/'inputs.json').write_text(json.dumps(dict(sha256=hashes,command=cmd,scope=('COARSE SCREEN WITHOUT MESH CONVERGENCE. ' if screen else '')+'Carrier-only, ideally clamped service-cap faces. Not PCB/assembly/physical certification.'),indent=2))
with (D/'run.log').open('w',encoding='utf-8') as log:
 result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
(D/'execution.json').write_text(json.dumps(dict(exit_code=result.returncode,completed=True,successful=result.returncode==0),indent=2))
print(name,'exit',result.returncode)
sys.exit(result.returncode)
