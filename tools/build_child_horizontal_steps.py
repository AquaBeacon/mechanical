"""FreeCAD CLI: identical finished mesh geometry into verified faceted STEP.

Uses existing STL_IN/STEP_OUT environment conventions. Set STL_IN to the source
part directory, STEP_OUT to that same directory. No GUI or second geometry design.
"""
import hashlib
import json
import os
from pathlib import Path
import FreeCAD as App
import Mesh
import Part

ROOT=Path(__file__).resolve().parents[1]
PART=Path(os.environ['STL_IN'])
DEST=Path(os.environ['STEP_OUT'])
report={}
doc=App.newDocument('Child_horizontal_finished_parts')
paths=sorted(PART.glob('child_exterior_open_frame_*.stl'))
paths += [ROOT/'parts/child/exterior/cots'/name/'visual_proxy.stl' for name in ['action_camera','dive_light']]
for src in paths:
    if not src.exists():raise RuntimeError('Missing reference mesh '+str(src))
    target=(DEST/(src.stem+'.step')) if src.parent==PART else src.with_suffix('.step')
    mesh=Mesh.Mesh(str(src));shape=Part.Shape();shape.makeShapeFromMesh(mesh.Topology,0.000001)
    if src.parent==PART:
        result=Part.makeSolid(shape)
        if not result.isValid():raise RuntimeError('Invalid manufacturing STEP '+src.stem)
        # Merges triangle boundaries without changing the finished surface.
        merged=result.removeSplitter()
        if merged.isValid() and abs(merged.Volume-result.Volume)/result.Volume<1e-8:result=merged
    else:
        # Visual proxies are intersecting reference shells, not print parts.
        result=Part.makeCompound([Part.makeSolid(s) for s in shape.Shells])
    obj=doc.addObject('Part::Feature','Body');obj.Label=src.stem;obj.Shape=result
    doc.recompute();Part.export([obj],str(target));back=Part.Shape();back.read(str(target))
    vol=abs(mesh.Volume);error=abs(abs(back.Volume)-vol)/max(vol,1e-12)
    bb=back.BoundBox
    row=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
             step_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
             step_valid=back.isValid(),solid_count=len(back.Solids),volume_mm3=back.Volume,
             stl_volume_mm3=vol,relative_volume_error=error,
             bounds_mm=[[bb.XMin,bb.YMin,bb.ZMin],[bb.XMax,bb.YMax,bb.ZMax]],faces=len(back.Faces),
             representation='Faceted planes from the finished OpenSCAD mesh; no second CAD geometry')
    if src.parent==PART and (not row['step_valid'] or len(back.Solids)!=1 or error>.0025):
        raise RuntimeError('STEP read-back failed '+src.stem+' '+str(row))
    report[src.relative_to(ROOT).as_posix()]=row
    doc.removeObject(obj.Name);print('[horizontal-step]',src.stem,len(back.Faces),'faces',error,flush=True)
path=PART/'_work/analysis/step_checks.json'
path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
App.closeDocument(doc.Name)
