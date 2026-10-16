"""Generate the simple parent layout and previews; existing designs are retained."""
import json
import subprocess
from pathlib import Path
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_simple'
OUT.mkdir(parents=True,exist_ok=True)
old=json.loads((ROOT/'assemblies/parent_bottom_sensors/placement.json').read_text(encoding='utf-8'))
items=[dict(i) for i in old['items'] if i.get('group') in ('vessel','floats')]
for i in items:
    i.pop('note',None)
items.insert(0,dict(label='simple_deck',part='parts/parent/exterior/printed/parent_simple_deck',group='exterior',color='Orange',ops=[]))
layout=dict(name='parent_simple',note='Simple deck with reserved underside mount holes. Floats are reference envelopes; ropes and accessory mounts are not modelled.',coordinate_system='Box bottom Z=0. Deck Z=-12..0.',groups=dict(exterior=True,vessel=True,floats=True),items=items)
(OUT/'placement.json').write_text(json.dumps(layout,indent=2),encoding='utf-8')
subprocess.run(['python',str(ROOT/'scad/lib/asm_gen.py'),str(OUT/'placement.json'),str(OUT/'parent_simple_view.scad')],check=True)
oscad=r'C:\Program Files\OpenSCAD\openscad.exe'
part=ROOT/'parts/parent/exterior/printed/parent_simple_deck'
for source,target,camera in [(OUT/'parent_simple_view.scad',OUT/'preview.png','0,0,0,65,0,30,0'),(part/'parent_simple_deck.scad',OUT/'underside.png','0,0,0,180,0,0,0')]:
    result=subprocess.run([oscad,'-o',str(target),'--imgsize=1100,850','--viewall','--autocenter','--projection=o','--camera='+camera,str(source)],capture_output=True,text=True)
    (OUT/(target.stem+'.log')).write_text(result.stdout+result.stderr,encoding='utf-8')
    result.check_returncode()
mesh=trimesh.load(part/'parent_simple_deck.stl',force='mesh')
checks=dict(bounds_mm=mesh.bounds.tolist(),watertight=bool(mesh.is_watertight),components=len(mesh.split()),volume_mm3=float(mesh.volume),accessory_roof_mm=4,notes='Geometry only. No load, buoyancy or slicer validation.')
assert mesh.is_watertight and checks['components']==1
assert all(abs(a-b)<0.01 for a,b in zip(mesh.extents,[236,236,12]))
(OUT/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(checks)
