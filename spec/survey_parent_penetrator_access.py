"""Inspect current geometry against the newly confirmed north-wall ports."""
from pathlib import Path
import json
import FreeCAD as A
import Part


def build(doc, parameters):
    root=Path(__file__).resolve().parents[1]
    report=dict(status='survey', rows=[], vendor_surfaces={})
    folder=root/'parts/common/exterior/cots/wetlink_penetrator_m10/ref'
    for name, file in [('nut','WL-M10-NUT-R1/WL-M10-NUT-PUBLIC.STEP'),
                       ('body','WLP-M10-6.5MM-R1/WLP-M10-6.5MM-R1-PUBLIC.STEP'),
                       ('tool','WL-M10-BULKHEAD-WRENCH-R1/WL-M10-BULKHEAD-WRENCH-R1-PUBLIC.STEP')]:
        s=Part.read(str(folder/file))
        circles=[]
        for f in s.Faces:
            surf=f.Surface
            if isinstance(surf,Part.Cylinder):
                rec=dict(radius=surf.Radius, center=list(surf.Center), axis=list(surf.Axis))
                if rec not in circles:circles.append(rec)
        report['vendor_surfaces'][name]=dict(bounds=str(s.BoundBox), cylinders=circles)
    rows=json.loads((root/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))['items']
    for row in rows:
        if row['label'] not in ['plate','tx_improved','sony_mount_plate','gnss_sony_shared_column','gnss_universal_carrier']:continue
        p=root/row['part']/(row.get('file',Path(row['part']).name)+'.step')
        target=Part.read(str(p))
        for op in reversed(row.get('ops',[])):
            if 'translate' in op:target.translate(A.Vector(*op['translate']))
            elif 'rotate' in op:
                for axis,angle in zip([(1,0,0),(0,1,0),(0,0,1)],op['rotate']):
                    target.rotate(A.Vector(),A.Vector(*axis),angle)
        for x in [150,175]:
            for z in [30,32.5,35]:
                shaft=Part.makeCylinder(5,20,A.Vector(x,210,z),A.Vector(0,1,0))
                nut=Part.makeCylinder(9,8,A.Vector(x,218.9,z),A.Vector(0,1,0))
                hardware=shaft.fuse(nut)
                v=hardware.common(target).Volume if hardware.BoundBox.intersect(target.BoundBox) else 0.
                report['rows'].append(dict(target=row['label'], port_x=x, height=z, overlap_mm3=v,
                                           envelope='M10 thread and conservative OD18/H8 nut'))
    print('PENETRATOR_SURVEY='+json.dumps(report),flush=True)
    obj=doc.addObject('Part::Feature','SurveyMarker');obj.Shape=Part.makeBox(1,1,1)
    obj.addProperty('App::PropertyString','Inspection');obj.Inspection=json.dumps(report)
    return [obj]
