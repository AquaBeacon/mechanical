"""Extract existing purchased ballast B dimensions; run with FreeCAD CLI."""
from pathlib import Path
import hashlib,json
import Part
root=Path(__file__).resolve().parents[1]
source=root/'parts/common/exterior/cots/ballast_plate/ballast_plate_b.step'
shape=Part.read(str(source));box=shape.BoundBox
holes=sorted({(round(f.Surface.Center.x,6),round(f.Surface.Center.y,6),round(f.Surface.Radius*2,6))
    for f in shape.Faces if isinstance(f.Surface,Part.Cylinder) and abs(f.Surface.Axis.z)>.999})
assert shape.isValid() and len(shape.Solids)==1 and len(holes)==4
assert all(abs(y)<1e-6 for x,y,d in holes)
sha=hashlib.sha256(source.read_bytes()).hexdigest()
target=root/'scad/lib/ballast_plate_b_interface.scad'
target.write_text('// Generated from existing ballast_plate_b.step; do not hand edit.\n'
    '// Source SHA-256: '+sha+'\n'
    f'ballast_b_size={json.dumps([box.XLength,box.YLength,box.ZLength])};\n'
    f'ballast_b_hole_x={json.dumps([x for x,y,d in holes])};\n'
    f'ballast_b_hole_d_provisional={holes[0][2]}; // Actual hole diameter remains unmeasured.\n',encoding='utf-8')
out=root/'assemblies/child_horizontal_plate_frame/_work/analysis/ballast_mount'
out.mkdir(parents=True,exist_ok=True)
(out/'reference.json').write_text(json.dumps(dict(source=source.relative_to(root).as_posix(),sha256=sha,
    size_mm=[box.XLength,box.YLength,box.ZLength],holes_xyd_mm=holes,hole_d_status='provisional; actual unmeasured'),indent=2),encoding='utf-8')
print('BALLAST_B_INTERFACE_PASS',flush=True)
