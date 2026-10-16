"""Check STEP-readback surfaces against authoritative rendered STL geometry."""
from pathlib import Path
import hashlib,json
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_horizontal_plate_frame'
report=json.loads((OUT/'_work/analysis/layout/step_validation.json').read_text(encoding='utf-8'))
assert len(report['parts'])==8,'Need all eight closed, valid STEP source variants first'
rows=[]
for entry in report['parts']:
    stem=entry['variant']
    base='child_wte4_petg_clamp' if stem.startswith('child_wte4_petg_clamp') else 'child_horizontal_plate_frame'
    folder=ROOT/'parts/child/exterior/printed'/base
    source=folder/(stem+'.stl');readback=folder/'_work/intermediate'/(stem+'_step_readback.stl')
    meshes=[trimesh.load(source,force='mesh'),trimesh.load(readback,force='mesh')]
    a,b=meshes
    box=float(np.abs(a.bounds-b.bounds).max())
    maximum=0
    for start,target in [(a,b),(b,a)]:
        points=np.vstack([start.vertices[::max(1,len(start.vertices)//2000)],
                          start.triangles_center[::max(1,len(start.faces)//2000)]])
        for i in range(0,len(points),500):
            maximum=max(maximum,float(trimesh.proximity.closest_point(target,points[i:i+500])[1].max()))
    row=dict(part=stem,bounds_delta_mm=box,sampled_bidirectional_surface_delta_mm=maximum,
             source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             method='Up to 2000 vertices + 2000 triangle centres in each direction; STEP solid validity is checked in FreeCAD')
    rows.append(row);print(stem,box,maximum,flush=True)
    if box>.001 or maximum>.001: raise RuntimeError(f'STEP/STL fidelity failed: {stem}')
(OUT/'_work/analysis/layout/step_surface_validation.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
print('STEP_SURFACE_VALIDATION_PASS')
