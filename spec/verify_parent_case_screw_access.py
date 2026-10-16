"""FreeCAD: check straight and inclined tool access to installed case anchors."""
from pathlib import Path
import sys, json, math, hashlib
import FreeCAD as A, Part
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R/'spec'))
sys.path.insert(0, str(R/'scad/lib'))
from parent_access_common import load, common, v
import parent_gnss as G
from parent_case_access import tool as envelope, TOOL_CLEAR_D, direction, GUIDE_ID, GUIDE_OD, BATTERY_TOOL_D
O = R/'assemblies/parent_hand_service'
D = O/'_work/analysis/case_screw_access_20261012'
D.mkdir(parents=True, exist_ok=True)
placement, scene = load()
rows = []
for i, (x,y) in enumerate(G.CASE_ANCHOR_XY):
    z = G.CASE_ANCHOR_SEAT_Z + G.CASE_ANCHOR_HEAD_DH[1]
    # Installed key shaft above head; socket engagement is a physical fit check.
    tool = Part.makeCylinder(TOOL_CLEAR_D/2,(110-z)/direction(i).z,v(x,y,z),direction(i))
    hits = []
    for label, shape in scene.items():
        if label.startswith('case_anchor_') or label in ['lid_keepout']: continue
        if i==1 and label in ['lipo','lipo_ret_lid','lipo_ret_pads']+['lipo_ret_bolt_'+str(k) for k in range(4)]: continue
        vol = common(tool,shape)
        if vol > 0.001:
            cut = tool.common(shape); b = cut.BoundBox
            hits.append(dict(label=label,volume_mm3=vol,z_range=[b.ZMin,b.ZMax]))
    rows.append(dict(anchor=i,xy=[x,y],tool_diameter_mm=TOOL_CLEAR_D,direction=list(direction(i)),required=i<3,pass_=not hits if i<3 else None,hits=hits))
if '--probe' in sys.argv:
    (D/'probe.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print(json.dumps(rows,indent=2),flush=True)
    raise SystemExit(0)
baseline=json.loads((D/'baseline.json').read_text(encoding='utf-8'))
floor=[]
for suffix in ['scad','step','stl']:
    path=R/f'parts/parent/interior/printed/parent_hand_service/floor_plate.{suffix}'
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    floor.append(dict(file=path.relative_to(R).as_posix(),unchanged=sha==baseline[path.relative_to(R).as_posix()],sha256=sha))
changed=['lipo_tray','main_mount_plate','coax_ring']
old_scene=dict(scene)
for label in changed+['coax_coil_keepout']:
    it=next(q for q in placement['items'] if q['label']==label)
    path=Path(it['part'])/(it.get('file',Path(it['part']).name)+'.step')
    s=Part.read(str(D/'history'/path))
    for op in reversed(it['ops']):
        if 'rotate' in op:
            for axis,ang in zip([v(1,0,0),v(0,1,0),v(0,0,1)],op['rotate']):s.rotate(v(0,0,0),axis,ang)
        if 'translate' in op:s.translate(v(*op['translate']))
    old_scene[label]=s
pairs=[]
for label in changed:
    for other in scene:
        if other==label or other=='lid_keepout':continue
        after=common(scene[label],scene[other])
        if after>.001:
            before=common(old_scene[label],old_scene[other])
            pairs.append(dict(parts=[label,other],before_mm3=before,after_mm3=after,pass_=after<=before+.05))
out=dict(status='PASS' if all(r['pass_'] for r in rows if r['required']) and all(q['unchanged'] for q in floor) and all(q['pass_'] for q in pairs) else 'FAIL',tool_checks=rows,floor_files=floor,interference_checks=pairs,tool='Long 2.5 mm ball-end hex key; SW tilt10 degrees southwest, NW tilt10 degrees west, SE vertical',guide_id_mm=GUIDE_ID,guide_od_mm=GUIDE_OD,battery_removal='Remove lid screw, slide lid south2 then lift, remove pack/top foam only; leave tray installed',excluded_anchor='NE under TX/Sony, inaccessible with electronics installed; not counted among three accessible screws',limitations=['Tool socket engagement, torque and actual key dimensions need physical check.','Three-anchor wave rigidity and creep not qualified.','Coil must remain outside new guard, within OD100/ID75/H10; actual 5 m winding capacity and R20 bends require physical check.'])
angle=math.radians(10)
guard_top=G.RACK_BASE_Z+G.COIL_BOTTOM_LOCAL+G.COIL_HEIGHT+.5
wall=GUIDE_OD/2-(guard_top-19)*math.tan(angle)-GUIDE_ID/2/math.cos(angle)-.2
column_gap=math.dist(G.CASE_ANCHOR_XY[0],G.MAIN_CARRIER_FOOT_XY[0])-GUIDE_OD/2-3.5
assert wall>=.8 and column_gap>=.1,(wall,column_gap)
out['guard_minimum_wall_mm']=wall
out['guide_to_main_column_gap_mm']=column_gap
out['battery_tray_tool_opening_mm']=BATTERY_TOOL_D
out['battery_removal']='Disconnect lead; remove four tray mount screws, lift closed module90 mm, remove one lid screw and slide south108 mm. SE case anchor is also exposed by removing the module.'
(O/'case_screw_access_checks.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2),flush=True)
assert out['status']=='PASS'
