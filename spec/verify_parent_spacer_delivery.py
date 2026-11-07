"""FreeCAD read-only checks for complete, individually printable parent supports."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import subprocess
import FreeCAD as A
import Part
import Mesh
import MeshPart

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'spec'))
from parent_access_common import load, common, mesh_volume
from configure_parent_spacer_delivery import SPACERS

OUT = ROOT / 'assemblies/parent_hand_service'
v = A.Vector
data, scene = load()
members = [i for i in data['items'] if i.get('file') in SPACERS]
assert Counter(i['file'] for i in members) == Counter(SPACERS)
assert all(i.get('print') is True and 'print_set' not in i for i in members)
assert not any('hex_spacer' in i['part'] for i in data['items'])
config = json.loads((OUT / 'print_config.json').read_text(encoding='utf-8'))
assert not any(i['file'] == 'parent_stack_spacer_set' for i in config['extra_parts'])
checks = []
hashes = {}
# Rebuild the manufacturing meshes from the existing analytic STEP sources.
# This also resolves pre-existing stale mesh fingerprints without touching CAD
# geometry or merely advancing file timestamps. Independently render SCAD first.
sys.path.insert(0, str(ROOT/'tools'))
from assembly_parts import definitions
render_dir = OUT/'_work/intermediate/spacer_delivery'
render_dir.mkdir(parents=True, exist_ok=True)
all_mesh_checks = []
for item in definitions(OUT)[0]:
    base = ROOT/item['part']/item['stem']
    rendered_path = render_dir/(item['stem']+'.stl')
    run = subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(rendered_path),
                          str(base.with_suffix('.scad'))],capture_output=True,text=True,
                         creationflags=0x08000000)
    (OUT/'_work/logs'/('spacer_delivery_render_'+item['stem']+'.log')).write_text(run.stdout+run.stderr,encoding='utf-8')
    assert run.returncode == 0 and 'WARNING:' not in run.stderr and 'ERROR:' not in run.stderr, item['stem']
    shape = Part.read(str(base.with_suffix('.step')))
    rendered_mesh = Mesh.Mesh(str(rendered_path))
    b = shape.optimalBoundingBox(False,False)
    delta = max(abs(getattr(b,k)-getattr(rendered_mesh.BoundBox,k)) for k in ('XMin','XMax','YMin','YMax','ZMin','ZMax'))
    diff = abs(mesh_volume(rendered_mesh)-shape.Volume)/shape.Volume
    assert shape.isValid() and len(shape.Solids)==1 and rendered_mesh.isSolid() and delta<.05 and diff<.02,(item['stem'],delta,diff)
    if '--refresh-meshes' in sys.argv:
        mesh = MeshPart.meshFromShape(Shape=shape,LinearDeflection=.025,AngularDeflection=.10,Relative=False)
        assert mesh.isSolid()
        mesh.write(str(base.with_suffix('.stl')))
    all_mesh_checks.append(dict(part=item['stem'],closed_scad_stl=True,bbox_difference_mm=delta,volume_relative_difference=diff))
    print('PASS SCAD/STEP',item['stem'],flush=True)
for stem in SPACERS:
    it = next(i for i in members if i['file'] == stem)
    base = ROOT / it['part'] / stem
    step = Part.read(str(base.with_suffix('.step')))
    stl = Mesh.Mesh(str(base.with_suffix('.stl')))
    rendered = Mesh.Mesh(str(OUT / '_work/intermediate/spacer_delivery' / (stem + '.stl')))
    b = step.optimalBoundingBox(False, False)
    delta = max(abs(getattr(b, k) - getattr(rendered.BoundBox, k))
                for k in ('XMin', 'XMax', 'YMin', 'YMax', 'ZMin', 'ZMax'))
    diffs = [abs(mesh_volume(m) - step.Volume) / step.Volume for m in (stl, rendered)]
    expected_height = 14.3 if stem.startswith('main') else (42.5 if stem.startswith('sony') else 32.0)
    bore = Part.makeCylinder(1.72, b.ZLength + .2, v(0, 0, -.1))
    blocked = step.common(bore).Volume
    ok = (step.isValid() and len(step.Solids) == 1 and stl.isSolid() and rendered.isSolid()
          and delta < .05 and max(diffs) < .02 and abs(b.ZMin) < .001
          and abs(b.ZLength - expected_height) < .001 and blocked < .001)
    checks.append(dict(part=stem, quantity=SPACERS[stem], extents_mm=[b.XLength,b.YLength,b.ZLength],
                       valid_step=step.isValid(), closed_source_stl=stl.isSolid(),
                       closed_openscad_stl=rendered.isSolid(), bbox_difference_mm=delta,
                       volume_relative_differences=diffs, blocked_bore_mm3=blocked, passed=ok))
    for suffix in ('.step', '.stl', '.scad'):
        path = base.with_suffix(suffix)
        hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()

for it in members:
    name = it['label']; shape = scene[name]
    host = 'main_mount_plate' if name.startswith('main') else ('sony_mount_plate' if name.startswith('sony') else 'gnss_universal_carrier')
    lower_gap = shape.distToShape(scene['plate'])[0]
    upper_gap = shape.distToShape(scene[host])[0]
    bb=shape.optimalBoundingBox(False,False)
    plane=Part.makePlane(20,20,v(bb.Center.x-10,bb.Center.y-10,bb.ZMin))
    bearing_area=shape.common(plane).common(scene['plate'].common(plane)).Area
    intersections = []
    for label, other in scene.items():
        if label == name or label in ('lid_keepout', 'tx_top_keepout', 'coax_coil_keepout', 'gnss_xh_keepout'):
            continue
        volume = common(shape, other)
        if volume > .01:
            intersections.append(dict(label=label, overlap_mm3=volume))
    checks.append(dict(label=name, lower_seat_gap_mm=lower_gap, upper_seat_gap_mm=upper_gap,
                       floor_bearing_area_mm2=bearing_area,collisions=intersections,
                       passed=lower_gap < .02 and upper_gap < .02 and bearing_area>.1 and not intersections))

# Check continuous material under every existing integral screw seat, from
# named fastener axes and board/plate datums rather than invented hole locations.
integral_groups = [('pwr_mount_', 'plate', 18.9, 28.25, 2.0, 2.6),
                   ('tx_mount_', 'plate', 18.9, 24.75, 2.0, 2.6),
                   ('lipo_ret_mount_', 'plate', 18.9, 20.0, 2.0, 2.6),
                   ('main_mount_', 'main_mount_plate', 35.7, 41.95, 2.0, 2.6),
                   ('sony_mount_', 'sony_mount_plate', 62.3, 65.55, 1.5, 2.3)]
for prefix, host, bottom, top, inner, outer in integral_groups:
    screws = [i for i in data['items'] if i['label'].startswith(prefix)
              and i['part'].endswith('/cots/screw')]
    assert len(screws) == 4, (prefix, len(screws))
    for it in screws:
        x,y,_ = next(op['translate'] for op in it['ops'] if 'translate' in op)
        height = top - bottom - .05
        ring = Part.makeCylinder(outer,height,v(x,y,bottom)).cut(Part.makeCylinder(inner,height,v(x,y,bottom)))
        missing = ring.cut(scene[host]).Volume
        checks.append(dict(label=it['label'] + '_integral_support', host=host,
                           support_top_z_mm=top, missing_material_mm3=missing, passed=missing < .01))

service = json.loads((OUT/'service_placement.json').read_text(encoding='utf-8'))
assert Counter(i['file'] for i in service['items'] if i.get('file') in SPACERS) == Counter(SPACERS)
assert all(i.get('print') is True for i in service['items'] if i.get('file') in SPACERS)
result = dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',
              separate_spacer_types=5,separate_spacer_quantity=12,
              geometry_changed=['sony_column_right: Y-elongated bearing foot; shaft/key/joint height retained'],
              checks=checks,all_print_meshes=all_mesh_checks,source_hashes=hashes,
              limitations=['Physical fit, torque, creep and wave strength remain unverified.',
                           'Legacy circular 3.45 mm spacer bores retained with existing fits; no printed threads.'])
(OUT/'spacer_delivery_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for c in checks:
    if not c['passed']: print('FAIL',c,flush=True)
print(result['status'],len(checks),'checks; five spacer types, twelve pieces',flush=True)
assert result['status'] == 'PASS'
