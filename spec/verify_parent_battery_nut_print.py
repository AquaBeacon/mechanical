"""Check actual Bambu PETG G-code for support inside the lid nut/socket passage."""
from pathlib import Path
import hashlib,json,re,zipfile,math,sys
import trimesh
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
W=O/'_work/analysis/battery_tool_nut_access_20261013'
side_grooves='--battery-side-grooves' in sys.argv
if side_grooves:W=O/'_work/analysis/battery_side_grooves_20261013'
source=R/'parts/parent/interior/printed/parent_hand_service/battery_base.stl'
records=json.loads((W/'slicing/after_slicing.json').read_text())
assert records['battery_base']['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
project=W/'slicing/after/battery_base/battery_base.3mf'
with zipfile.ZipFile(project) as z:
    code=z.read(next(n for n in z.namelist() if n.startswith('Metadata/plate_') and n.endswith('.gcode'))).decode()
mesh=trimesh.load(source,force='mesh')
shift=[128-mesh.bounds[:,0].mean(),128-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]]
regions={'nut_and_entry':[(8.4,15.6),(.2,7.8),(21.3,28.3)],'screw_bore':[(10.5,13.5),(3.5,6.5),(.2,29)]}
if side_grooves:regions.update(rail_left=[(-3.5,104.5),(6.3,7.5),(25.7,28.1)],rail_right=[(-3.5,104.5),(47.5,48.7),(25.7,28.1)])
hits={n:[] for n in regions};xyz=[0.,0.,0.];e=0.;relative=False;feature='';count=0
for line in code.splitlines():
    if line.startswith('; FEATURE: '):feature=line[11:].strip()
    if line.startswith(';TYPE:'):feature=line[6:].strip()
    if line.startswith('M83'):relative=True
    if line.startswith('M82'):relative=False
    vals={k:float(v) for k,v in re.findall(r'\b([XYZERIJ])(-?[\d.]+)',line)}
    if line.startswith('G92'):e=vals.get('E',e);continue
    if not line.startswith(('G0 ','G1 ','G2 ','G3 ')):continue
    prev=xyz[:];xyz=[vals.get(k,xyz[i]) for i,k in enumerate('XYZ')]
    de=vals.get('E',0) if relative else vals.get('E',e)-e
    if 'E' in vals:e=vals['E']
    if de<=0 or prev[:2]==xyz[:2] or not feature.lower().startswith('support'):continue
    count+=1
    lo=[min(prev[i],xyz[i])-shift[i]-.25 for i in range(3)]
    hi=[max(prev[i],xyz[i])-shift[i]+.25 for i in range(3)]
    if line.startswith(('G2 ','G3 ')):
        assert 'R' not in vals and ('I' in vals or 'J' in vals)
        radius=math.hypot(vals.get('I',0),vals.get('J',0))
        centre=[prev[i]+vals.get(k,0) for i,k in enumerate('IJ')]
        start=math.atan2(prev[1]-centre[1],prev[0]-centre[0]);end=math.atan2(xyz[1]-centre[1],xyz[0]-centre[0])
        sign=-1 if line.startswith('G2 ') else 1
        span=(sign*(end-start))%(2*math.pi)
        if math.dist(prev[:2],xyz[:2])<1e-6:span=2*math.pi
        points=[prev[:2],xyz[:2]]
        for angle in [0,math.pi/2,math.pi,3*math.pi/2]:
            if (sign*(angle-start))%(2*math.pi)<=span+1e-9:
                points.append([centre[0]+radius*math.cos(angle),centre[1]+radius*math.sin(angle)])
        for i in range(2):lo[i]=min(p[i] for p in points)-shift[i]-.25;hi[i]=max(p[i] for p in points)-shift[i]+.25
    for name,region in regions.items():
        if all(hi[i]>=a and lo[i]<=b for i,(a,b) in enumerate(region)):
            hits[name].append(dict(feature=feature,start=[prev[i]-shift[i] for i in range(3)],end=[xyz[i]-shift[i] for i in range(3)]))
report=dict(status='PASS' if not any(hits.values()) else 'FAIL',support_segments=count,regions_model_mm=regions,bead_envelope_half_width_mm=.25,hit_counts={n:len(v) for n,v in hits.items()},hits=hits,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),project_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),limits='Bambu X1C PETG0.2/wall4/infill100/support45/bridge exclusion; other slicer profiles and physical printing require checking.')
(O/'battery_nut_print_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report['status'],report['hit_counts']);assert report['status']=='PASS'
