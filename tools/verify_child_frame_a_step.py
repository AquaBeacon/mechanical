"""FreeCAD CLI readback of delivered frame A variants. No CAD edits."""
from pathlib import Path
import json
import FreeCAD
import Mesh
import Part

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
rows={}
for name in ['lower_minus','lower_plus','upper_minus','upper_plus','splice']:
    stem=PART/f'child_exterior_structural_frame_{name}'
    shape=Part.read(str(stem.with_suffix('.step')))
    mesh=Mesh.Mesh(str(stem.with_suffix('.stl')))
    b=shape.BoundBox; m=mesh.BoundBox
    edges=['XMin','XMax','YMin','YMax','ZMin','ZMax']
    error=max(abs(getattr(b,k)-getattr(m,k)) for k in edges)
    volume_error=abs(shape.Volume-mesh.Volume)/abs(mesh.Volume)
    row=dict(valid=bool(shape.isValid()),solids=len(shape.Solids),closed=bool(shape.isClosed()),
             step_volume_mm3=shape.Volume,stl_volume_mm3=mesh.Volume,
             relative_volume_error=volume_error,max_bounds_error_mm=error)
    row['pass']=row['valid'] and row['closed'] and row['solids']==1 and volume_error<=.0025 and error<.01
    rows[name]=row
report=dict(pass_readback=all(r['pass'] for r in rows.values()),parts=rows)
(CASE/'step_readback.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Frame A STEP readback',report['pass_readback'],flush=True)
if not report['pass_readback']: raise RuntimeError('Frame A STEP/STL mismatch; see step_readback.json')
