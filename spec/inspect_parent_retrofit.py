"""Read-only retrofit survey; run through the existing FreeCAD foundation.

Outputs review objects only. Does not modify production parts or placement.
"""
from pathlib import Path
import json
import FreeCAD as A
import Part


def build(doc, parameters):
    root = Path(__file__).resolve().parents[1]
    placement = json.loads((root / 'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
    labels = ['plate', 'p_main', 'p_pwr', 'antenna_rack', 'antenna_ground_plate',
              'gnss_universal_carrier', 'coax_ring']
    if parameters.get('connector_only', 0):
        labels = ['p_pwr']
    scene = {}
    objects = []
    for row in placement['items']:
        if row['label'] not in labels:
            continue
        folder = root / row['part']
        shape = Part.read(str(folder / (row.get('file', folder.name) + '.step')))
        for op in reversed(row.get('ops', [])):
            if 'rotate' in op:
                for axis, angle in zip([A.Vector(1,0,0), A.Vector(0,1,0), A.Vector(0,0,1)], op['rotate']):
                    shape.rotate(A.Vector(), axis, angle)
            if 'translate' in op:
                shape.translate(A.Vector(*op['translate']))
        scene[row['label']] = shape
        print('Loaded ' + row['label'], flush=True)
        obj = doc.addObject('Part::Feature', row['label'])
        b = shape.BoundBox
        # Review envelopes only: exporting the PCB's thousands of tiny solids
        # is unnecessary for this numeric survey and expensive on the user's PC.
        obj.Shape = Part.makeBox(b.XLength, b.YLength, b.ZLength, A.Vector(b.XMin,b.YMin,b.ZMin))
        obj.Label = row['label'] + ' [BOUNDING ENVELOPE ONLY]'
        objects.append(obj)
    def bounds(s):
        b = s.BoundBox
        return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
    pairs = []
    for board, support in ([] if parameters.get('bounds_only', 0) else [('p_main','antenna_rack'), ('p_main','antenna_ground_plate'), ('p_pwr','gnss_universal_carrier')]):
        for lift in [0, 2, 4, 6, 8]:
            shifted = scene[support].copy()
            shifted.translate(A.Vector(0,0,lift))
            candidates = [s for s in scene[board].Solids if s.BoundBox.intersect(shifted.BoundBox)]
            overlap = Part.makeCompound(candidates).common(shifted) if candidates else Part.Shape()
            volume = 0.0 if overlap.isNull() else overlap.Volume
            pairs.append(dict(board=board, support=support, lift_mm=lift,
                              intersection_mm3=volume,
                              intersection_bounds=bounds(overlap) if volume > .001 else None))
            print('Survey pair ' + json.dumps(pairs[-1]), flush=True)
    report = dict(status='SURVEY_ONLY', bounds={k:bounds(s) for k,s in scene.items()},
                  high_solids={k:[bounds(s) for s in scene[k].Solids if s.BoundBox.ZMax > z and s.Volume > 1] for k,z in [('p_main',55),('p_pwr',30 if parameters.get('connector_only', 0) else 44)] if k in scene},
                  pairs=pairs, limitations=['CAD geometry only; actual component and plugged cable differences remain unresolved.',
                                            'Lift trials are not approved layouts or fastening validation.'])
    objects[0].addProperty('App::PropertyString', 'RetrofitSurvey')
    objects[0].RetrofitSurvey = json.dumps(report)
    print('RETROFIT_SURVEY=' + json.dumps(report), flush=True)
    return objects
