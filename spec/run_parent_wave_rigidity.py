"""Run the existing native STEP/CalculiX adapter; preserve solver evidence."""
from pathlib import Path
import sys,subprocess,json,hashlib,datetime,os
R=Path(__file__).resolve().parents[1]
tag,name=sys.argv[1:3]
assert tag.isidentifier() and name.isidentifier()
D=R/'assemblies/parent_hand_service/_work/analysis/wave_rigidity_20261009'/tag/name
mesh=sys.argv[sys.argv.index('--mesh-mm')+1] if '--mesh-mm' in sys.argv else ('3' if '--converge' in sys.argv else '4')
suffix='_surface5' if '--surface5' in sys.argv else ''
if '--circle16' in sys.argv:suffix+='_circle16'
if '--floor-local' in sys.argv:suffix+='_floorlocal'
if '--floor-smallfaces' in sys.argv:suffix+='_floorsmallfaces'
out=D/(((('ccx_converged_h' if '--converge' in sys.argv else 'ccx_screen_h')+mesh.replace('.','p')) if '--mesh-mm' in sys.argv else ('ccx_converged' if '--converge' in sys.argv else 'ccx_screen'))+suffix)
assert not out.exists(), 'Keep each analysis run; choose a new tag for changed input'
cmd=[sys.executable,'-u',str(R/'spec/run_ccx_native_step.py'),str(D/(name+'.stl')),'--study',str(D/'study.json'),'--out',str(out),'--mesh-mm',mesh]
if '--converge' in sys.argv:cmd.append('--converge')
record=dict(start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=cmd,
 sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in D.iterdir() if f.is_file()},
 scope='Printed fixture at ideal bolted floor interfaces, generic dense dry PETG, six-direction2g payload budget; excludes physical joints, PCB/case compliance')
(D/(out.name+'_inputs.json')).write_text(json.dumps(record,indent=2),encoding='utf-8')
with (D/(out.name+'.log')).open('w',encoding='utf-8') as f:
 env=dict(os.environ)
 if '--surface5' in sys.argv:env['PARENT_GMSH_SURFACE_ALGORITHM']='5'
 if '--circle16' in sys.argv:env['PARENT_GMSH_CIRCLE_POINTS']='16'
 if '--floor-local' in sys.argv:env['PARENT_GMSH_FLOOR_LOCAL']='1'
 if '--floor-smallfaces' in sys.argv:env['PARENT_GMSH_FLOOR_LOCAL']='smallfaces'
 result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env)
(D/(out.name+'_execution.json')).write_text(json.dumps(dict(exit_code=result.returncode,completed=True,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2),encoding='utf-8')
print(tag,name,'native CCX exit',result.returncode,flush=True)
sys.exit(result.returncode)
