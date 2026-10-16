"""Derived fit views; canonical placement and purchased CAD remain unchanged."""
from pathlib import Path
import json,subprocess,runpy
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
C=O/'_work/intermediate';I=O/'_work/images'
ops=runpy.run_path(str(R/'scad/lib/asm_gen.py'))['ops_to_scad']
d=json.loads((O/'placement.json').read_text(encoding='utf-8'))
osc='C:/Program Files/OpenSCAD/openscad.exe'
for pose,file in [('closed','placement.json'),('service','service_placement.json')]:
 subprocess.run(['C:/Python313/python.exe',str(R/'scad/lib/asm_gen.py'),str(O/file),str(O/(pose+'_view.scad'))],check=True)
for name,selected,camera,size in [
 ('case_floor_fit',['plate','box_bcas212310g'],'320,-180,330,105,115,12','1400,1100'),
 ('case_floor_top',['plate','box_bcas212310g'],'105,115,600,105,115,0','1200,1300'),
 ('case_interior_open',None,'360,-290,300,105,115,35','1400,1100'),
 ('main_fixed_plate',['main_column_0','main_column_1','main_column_2','main_column_3','main_mount_plate','p_main'],'235,-155,155,70,65,30','1300,950'),
 ('sony_fixed_plate',['sony_column_0','sony_column_1','sony_column_2','sony_column_3','sony_mount_plate','spresense'],'310,20,190,173,174,48','1300,950')]:
 lines=['// Derived inspection only; placement.json is authoritative.']
 for it in d['items']:
  n=it['label']
  if n=='lid_keepout' or (selected and n not in selected):continue
  if n in ['tx_top_keepout','gnss_xh_keepout','coax_coil_keepout']:continue
  f=R/it['part']/(it.get('file',Path(it['part']).name)+'.stl')
  geometry=ops(it['ops'])+f'import("{f.as_posix()}",convexity=20);'
  if name in ['main_fixed_plate','sony_fixed_plate'] and n in ['p_main','spresense']:geometry='translate([0,0,12]) '+geometry
  if n=='box_bcas212310g' and selected:
   geometry='intersection(){'+geometry+'translate([-1,-1,-2]) cube([212,232,20]);}'
  color='#8c9cb0' if n=='box_bcas212310g' else it.get('color','#32a58d')
  lines.append(f'color("{color}",{it.get("alpha",1)}) '+geometry)
 view=C/(name+'.scad');view.write_text('\n'.join(lines),encoding='utf-8')
 p=subprocess.run([osc,'-o',str(I/(name+'.png')),'--imgsize='+size,'--projection=o','--viewall','--camera='+camera,str(view)],capture_output=True,text=True,creationflags=0x08000000)
 (O/'_work/logs'/(name+'_render.log')).write_text(p.stdout+p.stderr,encoding='utf-8');assert p.returncode==0,p.stderr
print('Rendered corrected case/floor and installed interior')
