from pathlib import Path
import Part,json
root=Path(__file__).resolve().parents[2]
result={}
for n in ['base','lever','bail','keeper']:
 s=Part.Shape();s.read(str(root/'parts/common/jigs/over_center_latch'/('over_center_latch_'+n+'.step')))
 verts,faces=s.tessellate(.001)
 result[n]=[[[verts[i].x,verts[i].y,verts[i].z] for i in f] for f in faces]
(root/'assemblies/over_center_latch/_work/intermediate/verified_step_facets.json').write_text(json.dumps(result))
print('PASS exported existing verified STEP facets')
