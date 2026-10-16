"""FreeCAD CLI: actual final STEP/STL dimensions, volumes and moving bodies."""
from pathlib import Path
import sys,json,math,itertools
sys.path.insert(0,str(Path(__file__).resolve().parent))
import FreeCAD as App
import Part,Mesh
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'parts/common/jigs/over_center_latch';ASM=ROOT/'assemblies/over_center_latch'
v=json.loads((P/'parameters.json').read_text(encoding='utf-8'));parts=['base','bail','lever','keeper','epdm','axis_a','axis_b']
raw={};checks={}
for name in parts:
    stem='over_center_latch_'+name;sh=Part.Shape();sh.read(str(P/(stem+'.step')));mesh=Mesh.Mesh(str(P/(stem+'.stl')))
    assert sh.isValid() and len(sh.Solids)==1,(name,'invalid/multiple solids')
    error=abs(sh.Volume-abs(mesh.Volume))/abs(mesh.Volume)
    bounds=max(abs(getattr(sh.BoundBox,k)-getattr(mesh.BoundBox,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
    assert error<.0025 and bounds<.002,(name,error,bounds)
    checks[name]=dict(valid=True,solids=len(sh.Solids),volume_mm3=sh.Volume,relative_volume_error=error,max_bound_error_mm=bounds);raw[name]=sh
collisions=[]
poses=json.loads((ASM/'_work/analysis/kinematics/step_poses.json').read_text(encoding='utf-8'))
for frame in poses:
    theta,lift=frame['angle_deg'],frame['lift_deg']
    shapes={}
    for i in frame['items']:
        if i['label']=='epdm':continue
        name=i['file'].replace('over_center_latch_','');q=raw[name].copy()
        q.rotate(App.Vector(),App.Vector(0,1,0),i['ops'][1]['rotate'][1]);q.translate(App.Vector(*i['ops'][0]['translate']));shapes[i['label']]=q
    for a,b in itertools.combinations(shapes,2):
        ba,bb=shapes[a].BoundBox,shapes[b].BoundBox
        overlap=[max(0,min(getattr(ba,k+'Max'),getattr(bb,k+'Max'))-max(getattr(ba,k+'Min'),getattr(bb,k+'Min'))) for k in ['X','Y','Z']]
        if min(overlap)<1e-6:volume=0.
        else:
            common=shapes[a].common(shapes[b]);volume=0. if common.isNull() else common.Volume
        assert volume<.005,(theta,lift,a,b,volume)
        collisions.append(dict(angle_deg=theta,lift_deg=lift,pair=[a,b],intersection_mm3=volume))
assembly=Part.Shape();assembly.read(str(ASM/'over_center_latch.step'));assert assembly.isValid()
placement=json.loads((ASM/'placement.json').read_text(encoding='utf-8'))
expected=sum(raw[i['file'].replace('over_center_latch_','')].Volume for i in placement['items'])
assert abs(assembly.Volume-expected)/expected<.0001
out=ASM/'_work/analysis/verification/step_report.json';out.write_text(json.dumps(dict(parts=checks,four_pose_intersections=collisions,assembly_valid=True,assembly_solids=len(assembly.Solids)),indent=2)+'\n',encoding='utf-8')
print('PASS: current STEP solids, final STL volume/bounds, four-pose interference and assembly placement')
