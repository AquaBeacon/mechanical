from pathlib import Path
import os,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
OSC=r'C:\Program Files\OpenSCAD\openscad.exe'
FC=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'
for name in ['camera_mount']:
 (OUT/(name+'.step')).unlink(missing_ok=True)
 subprocess.run([OSC,'-o',str(OUT/(name+'.csg')),str(OUT/(name+'.scad'))],check=True,capture_output=True)
 env=os.environ.copy();env.update(CSG_IN=str(OUT/(name+'.csg')),STEP_OUT=str(OUT/(name+'.step')),STL_REF=str(OUT/(name+'.stl')),OPENSCAD=OSC,PYTHONIOENCODING='utf-8')
 r=subprocess.run([FC,str(ROOT/'scad/lib/csg_to_step.py')],env=env,capture_output=True,text=True,errors='replace')
 (OUT/(name+'_step.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
 assert (OUT/(name+'.step')).exists(),r.stdout+r.stderr
 print(name,'STEP exported',flush=True)
env=os.environ.copy();env['CAMERA_M3_ROOT']=str(ROOT)
(OUT/'cad_checks.json').unlink(missing_ok=True)
r=subprocess.run([FC,str(ROOT/'spec/verify_camera_mount_m3.py')],env=env,capture_output=True,text=True,errors='replace')
(OUT/'cad_checks.log').write_text(r.stdout+r.stderr,encoding='utf-8')
print(r.stdout[-2500:]);assert (OUT/'cad_checks.json').exists()
