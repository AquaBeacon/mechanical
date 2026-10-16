"""FreeCAD CLI: compare actual STEP/STL dimensions and refresh structural alias."""
from pathlib import Path
import json, os, math
import FreeCAD as App, Part

ROOT = Path(__file__).resolve().parents[1]
ASSEMBLY = ROOT / 'assemblies/parent_oneplate'
WORK = ASSEMBLY / '_work/analysis/repeatable_mount'
layout = json.loads((ASSEMBLY / 'placement.json').read_text(encoding='utf-8'))
geometry = json.loads((WORK / 'geometry_checks.json').read_text(encoding='utf-8'))
records = []
seen = set()
for entry in geometry['printed_meshes']:
    source = ROOT / entry['file']
    if source in seen:
        continue
    seen.add(source)
    shape = Part.read(str(source.with_suffix('.step')))
    bb = shape.BoundBox
    actual = [[bb.XMin, bb.YMin, bb.ZMin], [bb.XMax, bb.YMax, bb.ZMax]]
    delta = max(abs(actual[j][i] - entry['bounds_mm'][j][i]) for j in range(2) for i in range(3))
    relative_volume = abs(shape.Volume - entry['volume_mm3']) / entry['volume_mm3']
    rec = dict(file=str(source.with_suffix('.step').relative_to(ROOT)), valid=shape.isValid(),
               solids=len(shape.Solids), bounds_mm=actual, bbox_delta_mm=delta,
               volume_mm3=shape.Volume, relative_volume_error=relative_volume)
    rec['passed'] = rec['valid'] and rec['solids'] == 1 and delta < .01 and relative_volume < .0001
    if source.stem == 'parent_light_jaw':
        # The retained jaw's native STEP has circular arcs, whereas its SCAD
        # STL uses 32-gons. Compare both to their respective analytic volumes.
        radius = 2.25 / math.cos(math.pi / 32)
        circle_area = math.pi * radius ** 2
        polygon_area = 16 * math.sin(math.pi / 16) * radius ** 2
        native = (700 - (4 - math.pi) * 4) * 8 - 2 * circle_area * 8
        tessellated = (700 - 16 + 64 * math.sin(math.pi / 16)) * 8 - 2 * polygon_area * 8
        rec['native_analytic_volume_error_mm3'] = abs(shape.Volume - native)
        rec['polygon_analytic_volume_error_mm3'] = abs(entry['volume_mm3'] - tessellated)
        rec['passed'] = (rec['valid'] and rec['solids'] == 1 and delta < .01 and
                         rec['native_analytic_volume_error_mm3'] < .001 and
                         rec['polygon_analytic_volume_error_mm3'] < .001)
    records.append(rec)
    print(rec, flush=True)
assert all(r['passed'] for r in records), 'STEP/STL mismatch'
filtered = dict(layout, items=[i for i in layout['items'] if i['group'] != 'hardware'])
filtered_path = ASSEMBLY / '_work/intermediate/repeatable_structure_placement.json'
filtered_path.parent.mkdir(parents=True, exist_ok=True)
filtered_path.write_text(json.dumps(filtered, ensure_ascii=False, indent=2), encoding='utf-8')
os.environ['ASM_JSON'] = str(filtered_path)
os.environ['ASM_ROOT'] = str(ROOT)
os.environ['STEP_OUT'] = str(ASSEMBLY / 'parent_oneplate_structure.step')
os.environ.pop('ASM_GROUP', None)
exec(compile((ROOT / 'scad/lib/asm_to_step.py').read_text(encoding='utf-8-sig'), 'asm_to_step.py', 'exec'))
(WORK / 'step_checks.json').write_text(json.dumps(dict(passed=True, parts=records,
    structural_alias='parent_oneplate_structure.step', structural_items=len(filtered['items']),
    collision_evidence='geometry_checks.json'), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('STEP dimensions, volumes and valid solids: PASS', flush=True)
