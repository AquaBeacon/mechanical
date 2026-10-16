"""Compare solved snapshots to current final STEP; headers may differ on export."""
from pathlib import Path
import sys,json,hashlib
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';D=O/'_work/analysis/wave_rigidity_20261009'
jobs={'gnss_frame':('wave_switch_clearance','gnss_universal_carrier','gnss_universal_carrier'),
 'antenna_rack':('wave_release','ann_mb1_internal_rack','ann_mb1_internal_rack'),
 'main_carrier':('reinforced_02','parent_hand_service','main_lower_carrier'),
 'sony_carrier':('reinforced_02','parent_hand_service','sony_upper_carrier'),
 'floor_plate':('wave_floor_budget','parent_hand_service','floor_plate')}
if '--current' in sys.argv:
 selected=json.loads((O/'wave_analysis_jobs.json').read_text())
 jobs={n:(selected[n][0],jobs[n][1],jobs[n][2]) for n in selected}
elif len(sys.argv)>1:jobs={n:(sys.argv[1],p,f) for n,(_,p,f) in jobs.items()}
rows=[]
for n,(tag,part,file) in jobs.items():
 a=D/tag/n/(n+'.step');b=R/'parts/parent/interior/printed'/part/(file+'.step')
 sa,sb=Part.read(str(a)),Part.read(str(b));av,bv=sa.Volume,sb.Volume
 stack=a.parent/'stack_source_hashes.json'
 if stack.exists():
  sources=json.loads(stack.read_text())['sources'];shapes=[]
  placement=json.loads((O/'placement.json').read_text(encoding='utf-8'))
  for it in placement['items']:
   rel=it['part']+'/'+it.get('file',Path(it['part']).name)+'.step'
   if rel not in sources:continue
   # Re-exported STEP headers may differ; final aggregate positive CAD
   # symmetric difference below remains the required geometry comparison.
   p=R/rel
   s=Part.read(str(p))
   for op in reversed(it['ops']):
    assert 'translate' in op;s.translate(A.Vector(*op['translate']))
   shapes.append(s)
  assert len(shapes)==5
  sb=shapes[0].multiFuse(shapes[1:]).removeSplitter();bv=sb.Volume
 diff=sa.cut(sb).Volume+sb.cut(sa).Volume
 bounds=['XMin','XMax','YMin','YMax','ZMin','ZMax'];delta=max(abs(getattr(sa.BoundBox,k)-getattr(sb.BoundBox,k)) for k in bounds)
 rows.append(dict(part=n,snapshot=a.relative_to(R).as_posix(),current=b.relative_to(R).as_posix(),sha256={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [a,b]},volume_mm3=[av,bv],symmetric_difference_mm3=diff,bbox_delta_mm=delta,pass_=diff<.001 and delta<.00001))
out=dict(status='PASS' if all(r['pass_'] for r in rows) else 'FAIL',checks=rows,note='STEP export headers/timestamps may differ. Positive CAD volume/bounding-box comparison is required, never inferred from a similar filename.')
(O/'wave_analysis_geometry_checks.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(out['status']);assert out['status']=='PASS'
