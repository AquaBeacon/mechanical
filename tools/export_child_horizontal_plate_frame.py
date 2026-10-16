"""Export verified frame/clamp variants and assembly in FreeCAD CLI.

Environment: ASM_ROOT, ASM_JSON and STEP_OUT as used by asm_to_step.py.
"""
from pathlib import Path
import os
import runpy
import json
import hashlib
import FreeCAD as App
import Part
import Mesh

def export_part(folder,variant):
    source = folder/f'{variant}.stl'
    target = source.with_suffix('.step')
    mesh = Mesh.Mesh(str(source))
    shell = Part.Shape()
    shell.makeShapeFromMesh(mesh.Topology, 0.05)
    solid = Part.makeSolid(shell)
    method='native verified-STL conversion, tolerance0.05'
    if not solid.isValid():
        solid.fix(1e-7,1e-7,5e-5)
        method+='; OCC numerical fix max0.00005mm'
    print(variant,method,'valid=',solid.isValid(),'closed=',solid.isClosed(),flush=True)
    error = abs(solid.Volume-abs(mesh.Volume))/max(abs(mesh.Volume),1)
    if not solid.isValid() or not solid.isClosed() or len(solid.Solids)!=1 or error > 0.0025:
        raise RuntimeError(f'Invalid STEP conversion: {variant}; valid={solid.isValid()}, closed={solid.isClosed()}, solids={len(solid.Solids)}, volume_error={error}')
    doc = App.newDocument('Study_'+variant)
    obj = doc.addObject('Part::Feature','Plate')
    obj.Label = 'fit_prototype_'+variant
    obj.Shape = solid
    doc.recompute()
    Part.export([obj],str(target))
    check = Part.Shape();check.read(str(target))
    if not check.isValid() or not check.isClosed() or len(check.Solids)!=1 or abs(check.Volume-solid.Volume)/solid.Volume > 0.0025:
        raise RuntimeError(f'STEP readback failed: {variant}')
    bound=check.BoundBox
    readback=folder/'_work/intermediate'/f'{variant}_step_readback.stl'
    readback.parent.mkdir(parents=True,exist_ok=True)
    Mesh.Mesh(check.tessellate(0.001)).write(str(readback))
    entry={'variant':variant,'valid':True,'closed':True,'solid_count':1,'method':method,'volume_relative_error':error,
                    'mesh_volume_mm3':abs(mesh.Volume),'step_volume_mm3':check.Volume,
                    'step_extents_mm':[bound.XLength,bound.YLength,bound.ZLength],
                    'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                    'step_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    App.closeDocument(doc.Name)
    print('PART_STEP_READBACK_COMPLETE',variant,flush=True)
    return entry

def main():
    root=Path(os.environ['ASM_ROOT'])
    part=root/'parts/child/exterior/printed/child_horizontal_plate_frame'
    variants=[(part,f'child_horizontal_plate_frame_{v}') for v in ['side','bottom','top','ballast_cap','guard_front','guard_rear','rotation_key','clamp_support']]
    variants += [(root/'parts/child/exterior/printed/child_wte4_petg_clamp',f'child_wte4_petg_clamp_{v}') for v in ['upper_linked','lower_linked']]
    reports=[]
    for folder,variant in variants:
        reports.append(export_part(folder,variant))
    runpy.run_path(str(root/'scad/lib/asm_to_step.py'),run_name='__main__')
    output=root/'assemblies/child_horizontal_plate_frame/_work/analysis/layout/step_validation.json'
    output.write_text(json.dumps({'status':'fit_prototype','parts':reports},indent=2)+'\n',encoding='utf-8')
    print('HORIZONTAL_FRAME_STEP_COMPLETE',flush=True)

# FreeCAD command-file imports share the interactive global namespace.
# Keep conversion locals isolated and ignore reentrant command-file execution.
if not globals().get('_horizontal_frame_export_running',False):
    _horizontal_frame_export_running=True
    main()
