"""Derived CAD views; canonical parts/placement are never modified here."""
from pathlib import Path
import json,math,subprocess
import trimesh
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
W=O/'_work/analysis/print_economy_20261009';C=O/'_work/intermediate';I=O/'_work/images'
C.mkdir(exist_ok=True);I.mkdir(exist_ok=True)
OSC='C:/Program Files/OpenSCAD/openscad.exe'
old=W/'history/parts/parent/interior/printed/parent_hand_service/floor_plate.stl'
new=R/'parts/parent/interior/printed/parent_hand_service/floor_plate.stl'
scene='// Comparison view only, mm.\n'
for x,source,label,color in [(0,old,'BEFORE','#929aa6'),(225,new,'AFTER','#32a58d')]:
 scene+=f'color("{color}") translate([{x},0,0]) import("{source.as_posix()}",convexity=20);\n'
 scene+=f'color("#263a46") translate([{x+50},-7,8.84]) linear_extrude(1) text("{label}",size=10);\n'
source=C/'print_floor_comparison.scad';source.write_text(scene,encoding='utf-8')
subprocess.run([OSC,'-o',str(I/'print_floor_comparison.png'),'--imgsize=1600,1000','--projection=o','--viewall','--camera=620,-550,900,220,110,15',str(source)],check=True,capture_output=True,creationflags=0x08000000)
placement=json.loads((O/'placement.json').read_text(encoding='utf-8'))
poses={'floor_plate':[112,112],'ann_mb1_internal_rack':[325,68],'ann_mb1_coax_ring':[325,202],'gnss_universal_carrier':[500,62],'sony_upper_carrier':[500,200],'main_lower_carrier':[125,335],'battery_base':[315,335],'parent_lipo_retainer_lid_narrow':[480,335],'gnss_column_front':[610,245],'gnss_column_rear':[635,245],'gnss_edge_cap_front':[600,285],'gnss_edge_cap':[600,310]}
scene='// Derived print orientations; quantities in PRINT.md.\n';done=set()
for it in placement['items']:
 if '/printed/' not in it['part']:continue
 name=it.get('file',Path(it['part']).name)
 if name not in poses or name in done:continue
 done.add(name);folder=R/it['part'];source=folder/(name+'.stl')
 rotation=json.loads((folder/'manufacturing.json').read_text()).get('print_rotations_deg',{}).get(name,[0,0,0])
 mesh=trimesh.load(source,force='mesh')
 for axis,ang in zip([[1,0,0],[0,1,0],[0,0,1]],rotation):mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(ang),axis))
 bounds=mesh.bounds;x,y=poses[name];offset=[float(x-bounds[:,0].mean()),float(y-bounds[:,1].mean()),float(-bounds[0,2])]
 scene+=f'color("#32a58d") translate({offset}) rotate({rotation}) import("{source.as_posix()}",convexity=20);\n'
 label=name.replace('gnss_','').replace('parent_lipo_retainer_','').replace('ann_mb1_','')
 scene+=f'color("#263a46") translate([{x-bounds[1,0]/2+bounds[0,0]/2},{y-(bounds[1,1]-bounds[0,1])/2-11},0]) linear_extrude(.4) text("{label}",size=5);\n'
source=C/'print_parts_orientations.scad';source.write_text(scene,encoding='utf-8')
subprocess.run([OSC,'-o',str(I/'print_parts_orientations.png'),'--imgsize=1800,1200','--projection=o','--viewall','--camera=850,-750,1250,345,210,18',str(source)],check=True,capture_output=True,creationflags=0x08000000)
print('Rendered floor comparison and current print orientations')
