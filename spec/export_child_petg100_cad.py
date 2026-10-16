"""Produce portable parametric CAD with analytic exclusion geometry and STEP.
No imported STL booleans in final sources: that route failed FreeCAD conversion.
"""
from pathlib import Path
import os,subprocess,shutil,json
import trimesh
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assemblies/child_petg100_design';CAD=OUT/'cad';CAD.mkdir(exist_ok=True)
shutil.copy2(ROOT/'scad/lib/hardpoint.scad',CAD/'hardpoint.scad')
voids='''
// Explicit analytic keep-outs. D40x100 light and D26.4 TD04A remain provisional.
module cable_segment(a,b,r){
 v=b-a;len=norm(v);
 translate(a)rotate([0,acos(v[2]/len),atan2(v[1],v[0])])cylinder(r=r,h=len,$fn=24);
 translate(a)sphere(r=r,$fn=24);translate(b)sphere(r=r,$fn=24);
}
module cable_route(points,r=4){for(i=[0:len(points)-2])cable_segment(points[i],points[i+1],r);}
module scene_voids(){
 box3([-47.35,83.1,82.95],[47.35,129,167.05]);
 box3([44,-100,75],[80,-50,125]);translate([80,-75,50])cylinder(d=42,h=100);
 translate([0,-85,224.5])cylinder(d=26.4,h=55);
 box3([-25,-110,218.5],[25,-60,256.5]);
 box3([-26,-150,115],[26,-64,145]);box3([-26,-88,115],[26,-64,182]);
 for(s=[-1,1])cable_route([[s*18,-97,-40],[s*18,-97,75],[s*34,-79,105],[s*34,-79,187],[s*18,-92,202],[s*18,-92,228]]);
 cable_route([[-18,-92,202],[-18,-85,214],[0,-85,224]]);
 cable_route([[80,-75,50],[80,-75,28],[42,-79,28],[34,-79,75],[18,-97,75]]);
 for(a=[-90,-18,54,126,198])translate([28*cos(a),28*sin(a),-33.8])cylinder(d=14,h=20);
 box3([-38,-45,-48],[38,38,-34]);
}
'''
def replace_module(s,name,new):
 i=s.index('module '+name+'(');j=s.index('{',i);depth=1;k=j+1
 while depth:depth+=(s[k]=='{')-(s[k]=='}');k+=1
 return s[:i]+new+s[k:]
items=[]
for n in ['child_jaw_gate','child_core_frame','child_cam_bridge']:
 s=(OUT/n/(n+'.scad')).read_text(encoding='utf-8')
 s=s.replace('use <C:/Users/ryupc/WorkSpace/Mitou26/AquaBeacon-OSS/mechanical/scad/lib/hardpoint.scad>','use <hardpoint.scad>')
 s=replace_module(s,'scene_voids',voids)
 (CAD/(n+'.scad')).write_text(s,encoding='utf-8');items.append((n,n,None))
for n in ['vertical_light_mount','td04a_socket']:
 shutil.copy2(OUT/(n+'.scad'),CAD/(n+'.scad'))
items += [('vertical_light_saddle','vertical_light_mount','saddle'),('vertical_light_cap','vertical_light_mount','cap'),('td04a_socket','td04a_socket',None)]
manifest=[]
for name,source,part in items:
 for ext in ['stl','csg']:
  args=['C:/Program Files/OpenSCAD/openscad.exe','-o',str(CAD/(name+'.'+ext))]
  if part:args+=['-D',f'part="{part}"']
  with (CAD/(name+'_'+ext+'.log')).open('w',encoding='utf-8') as log:
   subprocess.run(args+[str(CAD/(source+'.scad'))],stdout=log,stderr=log,check=True)
 env=os.environ.copy();env.update(CSG_IN=str(CAD/(name+'.csg')),STEP_OUT=str(CAD/(name+'.step')),STL_REF=str(CAD/(name+'.stl')),OPENSCAD='C:/Program Files/OpenSCAD/openscad.exe',PYTHONIOENCODING='utf-8')
 with (CAD/(name+'_step.log')).open('w',encoding='utf-8') as log:
  subprocess.run(['C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/freecadcmd.exe',str(ROOT/'scad/lib/csg_to_step.py')],env=env,stdout=log,stderr=log)
 m=trimesh.load(CAD/(name+'.stl'),force='mesh')
 rec={'name':name,'source':source+'.scad','part_parameter':part,'watertight':bool(m.is_watertight),'volume_cm3':float(m.volume/1000),'mass_kg':float(m.volume*1.27e-6),'bounds_mm':m.bounds.tolist(),'step_exists':(CAD/(name+'.step')).exists()}
 manifest.append(rec);(CAD/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
 print(rec,flush=True)
