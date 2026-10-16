"""Run in FreeCAD; strict faceted STEP export from merged, verified meshes."""
import os,json
from pathlib import Path
import Mesh,Part
root=Path(os.environ['BODY_ROOT'])
defaults=['parts/child/interior/printed/'+p for p in ('child_vtray_deck/child_vtray_deck_t200','child_flange_brace/child_flange_brace')]
for part in json.loads(os.environ['BODY_MESHES']) if 'BODY_MESHES' in os.environ else defaults:
    p=root/part
    mesh=Mesh.Mesh(str(p.with_suffix('.stl')))
    shape=Part.Shape()
    shape.makeShapeFromMesh(mesh.Topology,0.001)
    solids=[Part.makeSolid(s) for s in shape.Shells]
    assert len(solids)==1
    shape=solids[0]
    report={'valid':shape.isValid(),'solids':len(shape.Solids),
            'volume_mm3':shape.Volume,'stl_volume_mm3':mesh.Volume,
            'relative_volume_difference':abs(shape.Volume-mesh.Volume)/abs(mesh.Volume),
            'representation':'faceted STEP; edit original SCAD for parameter changes'}
    print(p.name,json.dumps(report),flush=True)
    assert report['valid'] and report['relative_volume_difference']<0.005
    shape.exportStep(str(p.with_suffix('.step')))
    p.with_suffix('.check.json').write_text(json.dumps(report,indent=2))
