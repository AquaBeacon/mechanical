"""Simplify final CSG booleans without imported meshes or empty intermediate solids."""
from pathlib import Path
import json,os,subprocess
import trimesh
from sanitize_csg import clean
ROOT=Path(__file__).resolve().parents[1];CAD=ROOT/'assemblies/child_petg100_design/cad'
def replace_module(s,name,new):
 i=s.index('module '+name+'(');j=s.index('{',i);depth=1;k=j+1
 while depth:depth+=(s[k]=='{')-(s[k]=='}');k+=1
 return s[:i]+new+s[k:]
for name in ['child_jaw_gate','child_core_frame']:
 p=CAD/(name+'.scad');s=p.read_text(encoding='utf-8')
 if name=='child_jaw_gate':
  cuts='bore_void();core_knuckles();hinge_swing();finger_room();bridge_zone();hp_envelope();small_holes();scene_voids();'
 else:
  cuts='bore_void();gate_half();gate_knuckles();grooves();tie_slots();tie_backspace();hand_room();cable_cavity();hp1_holes();hp23_holes();hp23_envelope();guard_tabs();small_holes();scene_voids();'
 s=replace_module(s,'manufactured','module manufactured(){difference(){union(){preserve_bodies();intersection(){structure();design_space();}}'+cuts+'}}')
 s=s.replace('module cable_route(points,r=4)','module cable_route(points,r=4.15)')
 p.write_text(s,encoding='utf-8')
 for ext in ['stl','csg']:
  with (CAD/(name+'_'+ext+'.log')).open('w',encoding='utf-8') as log:
   subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(CAD/(name+'.'+ext)),str(p)],stdout=log,stderr=log,check=True)
 csg=CAD/(name+'_clean.csg');csg.write_text(clean((CAD/(name+'.csg')).read_text()),encoding='utf-8')
 env=os.environ.copy();env.update(CSG_IN=str(csg),STEP_OUT=str(CAD/(name+'.step')),STL_REF=str(CAD/(name+'.stl')),OPENSCAD='C:/Program Files/OpenSCAD/openscad.exe',PYTHONIOENCODING='utf-8')
 with (CAD/(name+'_step_clean.log')).open('w',encoding='utf-8') as log:
  subprocess.run(['C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/freecadcmd.exe',str(ROOT/'scad/lib/csg_to_step.py')],env=env,stdout=log,stderr=log)
 m=trimesh.load(CAD/(name+'.stl'),force='mesh')
 print(name, 'watertight',m.is_watertight,'cm3',m.volume/1000,'step',(CAD/(name+'.step')).exists(),flush=True)
