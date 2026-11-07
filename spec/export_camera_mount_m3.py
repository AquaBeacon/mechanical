from pathlib import Path
from datetime import datetime, timezone
import os,subprocess,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
OSC=r'C:\Program Files\OpenSCAD\openscad.exe'
FC=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'
RUN=OUT/'_work/analysis'/('step_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
RUN.mkdir(parents=True)
for name in ['camera_mount']:
 subprocess.run([OSC,'-o',str(RUN/(name+'.csg')),str(OUT/(name+'.scad'))],cwd=ROOT,check=True,capture_output=True)
 env=os.environ.copy();env.update(CSG_IN=str(RUN/(name+'.csg')),STEP_OUT=str(RUN/(name+'.step')),STL_REF=str(OUT/(name+'.stl')),OPENSCAD=OSC,PYTHONIOENCODING='utf-8')
 r=subprocess.run([FC,str(ROOT/'scad/lib/csg_to_step.py')],cwd=ROOT,env=env,capture_output=True,text=True,errors='replace')
 (RUN/(name+'_step.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
 if not (RUN/(name+'.step')).exists():
  env['STL_IN']=str(OUT/(name+'.stl'))
  r=subprocess.run([FC,str(ROOT/'scad/lib/stl_to_step.py')],cwd=ROOT,env=env,capture_output=True,text=True,errors='replace')
  (RUN/(name+'_faceted_step.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
 assert (RUN/(name+'.step')).exists(),r.stdout+r.stderr
 shutil.copy2(RUN/(name+'.step'),OUT/(name+'.step'))
 print(name,'STEP exported',flush=True)
env=os.environ.copy();env['CAMERA_M3_ROOT']=str(ROOT)
(OUT/'cad_checks.json').unlink(missing_ok=True)
r=subprocess.run([FC,str(ROOT/'spec/verify_camera_mount_m3.py')],cwd=ROOT,env=env,capture_output=True,text=True,errors='replace')
(RUN/'cad_checks.log').write_text(r.stdout+r.stderr,encoding='utf-8')
print(r.stdout[-2500:]);assert (OUT/'cad_checks.json').exists()
