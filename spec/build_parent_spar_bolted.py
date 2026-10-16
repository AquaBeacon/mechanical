"""Build only the parent screw-fastened exterior. Sources are in scad/lib.
No edits to the existing parent or child assemblies. Run from any directory.
"""
from pathlib import Path
import json, subprocess, os, math, sys
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_spar_bolted'
PRINT=ROOT/'print_jobs/parent_spar_bolted'
OSC=r'C:\Program Files\OpenSCAD\openscad.exe'
FC=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'
SPECS={
 'disk':('disk();','disk();',1),
 'fin':('fin();','translate([0,125,0]) rotate([90,0,0]) fin();',4),
 'hub':('hub();','hub();',2),
 'beam_lower':('beam(true);','translate([0,0,16]) rotate([0,90,0]) beam(true);',1),
 'beam_upper':('beam(false);','translate([0,0,16]) rotate([0,90,0]) beam(false);',1),
 'coupler_half':('coupler();','translate([0,0,27]) rotate([-90,0,0]) coupler();',2),
 'float_body':('float_body();','float_body();',2),
 'float_lid':('float_lid();','translate([0,0,6]) rotate([180,0,0]) float_lid();',2),
 'float_top':('float_end(true);','float_end(true);',1),
 'float_bottom':('float_end(false);','translate([0,0,8]) rotate([180,0,0]) float_end(false);',1),
 'ballast_body':('ballast_body();','ballast_body();',1),
 'ballast_lid':('ballast_lid();','ballast_lid();',1),
 'camera_bridge':('camera_bridge();','translate([0,0,225]) rotate([-90,0,0]) camera_bridge();',1),
 'gps_bridge':('gps_bridge();','translate([0,0,10]) rotate([0,90,0]) gps_bridge();',1),
}
OUT.mkdir(parents=True,exist_ok=True); PRINT.mkdir(parents=True,exist_ok=True)
def run(args,log,env=None):
 r=subprocess.run([str(x) for x in args],capture_output=True,text=True,env=env)
 Path(log).write_text(r.stdout+r.stderr,encoding='utf-8')
 if r.returncode: raise RuntimeError(f'{args[0]} failed: {log}\n{r.stderr[-1000:]}')
 return r

def build_part(key,body,orientation,qty):
 name='parent_spar_'+key; folder=ROOT/'parts/parent/exterior/printed'/name
 folder.mkdir(parents=True,exist_ok=True)
 scad=folder/(name+'.scad')
 scad.write_text('// mm. part=print is the intended X1C orientation.\npart="assembly"; // [assembly,print]\nuse <../../../../../scad/lib/parent_spar_bolted.scad>\nif(part=="print") { '+orientation+' } else { '+body+' }\n',encoding='utf-8')
 stl=folder/(name+'.stl'); pstl=PRINT/(name+'.stl')
 run([OSC,'-o',stl,scad],folder/'render.log')
 run([OSC,'-D','part="print"','-o',pstl,scad],folder/'print_render.log')
 m=trimesh.load(pstl,force='mesh')
 assert m.is_watertight and len(m.split())==1,(key,'invalid mesh')
 assert max(m.extents)<=250,(key,m.extents)
 assert abs(m.bounds[0,2])<.05,(key,'not on bed',m.bounds)
 # Conservative rectangle containing the part + 5 mm brim, entirely right
 # of the cutter exclusion strip. No disabling the printer exclusion area.
 assert m.extents[0]+10<=236 and m.extents[1]+10<=250,(key,'brim/exclusion fit')
 result={'quantity':qty,'size_mm':m.extents.tolist(),'watertight':True,'bodies':1,
         'bed_center_xy':[138,128], 'brim_mm':5,
         'volume_cm3':float(m.volume/1000),'print_stl':str(pstl.relative_to(ROOT))}
 if '--no-step' not in sys.argv:
  csg=folder/(name+'.csg'); step=folder/(name+'.step')
  run([OSC,'-o',csg,scad],folder/'csg.log')
  env=os.environ.copy();env.update(OPENSCAD=OSC,CSG_IN=str(csg),STEP_OUT=str(step),STL_REF=str(stl))
  r=run([FC,ROOT/'scad/lib/csg_to_step.py'],folder/'step.log',env)
  assert step.exists() and 'check vs STL:' in r.stdout and '[csg2step] wrote' in r.stdout,key
 folder.joinpath(name+'.md').write_text(f'# {name}\n\n親機ねじ固定外装。数量 {qty}。寸法 {m.extents.round(2).tolist()} mm（印刷姿勢）。\n\n設計ソースは `scad/lib/parent_spar_bolted.scad` の `{key}`。\n印刷用STLは `print_jobs/parent_spar_bolted/{name}.stl`。部品フォルダのSTL/STEPは組立座標。\n\n締結表・材料・組立順・未検証条件は `assemblies/parent_spar_bolted/README.md` を参照。\n閉じた単一メッシュ・250 mm枠・5 mmブリムを含む保守的なベッド配置を機械確認。\n実荷重の安全率・疲労・水密性は未評価。\n',encoding='utf-8')
 print(key, m.extents.round(2).tolist(),flush=True)
 return result

if __name__=='__main__':
 report={}
 for key,(body,orientation,qty) in SPECS.items():
  report[key]=build_part(key,body,orientation,qty)
 OUT.joinpath('print_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
