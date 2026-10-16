"""Check the finished A against the current connected clamp cage, in mm."""
from pathlib import Path
import hashlib,json
import trimesh

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
clamp=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp/child_wte4_suspension_clamp_cage.stl'
d=json.loads((PART/'spec/design_parameters.json').read_text())
frame=PART/'child_exterior_structural_frame_full.stl'
a=trimesh.load(frame,force='mesh'); c=trimesh.load(clamp,force='mesh')
if not c.is_watertight or not c.is_winding_consistent: raise RuntimeError('Current clamp reference is not a closed mesh')
c.apply_transform([[1,0,0,0],[0,0,1,0],[0,-1,0,-d['inner_face_x']],[0,0,0,1]])
intersection=trimesh.boolean.intersection([a,c],engine='manifold')
volume=float(intersection.volume)
report=dict(pass_contact_geometry=volume<1e-6,intersection_volume_mm3=volume,
            frame_sha256=hashlib.sha256(frame.read_bytes()).hexdigest(),
            clamp_sha256=hashlib.sha256(clamp.read_bytes()).hexdigest(),
            scope='A versus current connected clamp cage; both sides use the same proper relative rotation. Does not qualify clamp strength, C, guard or cables.')
(CASE/'clamp_contact_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
if not report['pass_contact_geometry']: raise RuntimeError('Clamp/A collision; see clamp_contact_checks.json')
