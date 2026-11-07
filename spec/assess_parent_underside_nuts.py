"""Survey existing floor seats and underside nut/washer space; not a keeper design."""
from pathlib import Path
import json,math
import FreeCAD as A
import Part

def build(doc,parameters):
    root=Path(__file__).resolve().parents[1]
    floor=Part.read(str(root/'parts/parent/interior/printed/parent_hand_service/floor_plate.step'))
    case=Part.read(str(root/'parts/parent/exterior/cots/bcas212310g/bcas212310g.step'))
    d=json.loads((root/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
    prefixes=('main_carrier_nut_','sony_carrier_nut_','gnss_frame_nut_','antenna_rack_nut_')
    rows=[];out=[]
    def common(s,t):
        if not s.BoundBox.intersect(t.BoundBox):return 0.0
        c=s.common(t)
        return 0.0 if c.isNull() else c.Volume
    for row in d['items']:
        if not row['label'].startswith(prefixes):continue
        x,y,_=next(op['translate'] for op in row['ops'] if 'translate' in op)
        z=8.84;washer_h=.5;nut_h=2.4;af=5.5
        washer=Part.makeCylinder(3.5,washer_h,A.Vector(x,y,z-washer_h)).cut(Part.makeCylinder(1.6,washer_h+.2,A.Vector(x,y,z-washer_h-.1)))
        pts=[A.Vector(x+af/math.sqrt(3)*math.cos(math.pi/6+i*math.pi/3),y+af/math.sqrt(3)*math.sin(math.pi/6+i*math.pi/3),z-washer_h-nut_h) for i in range(6)]
        nut=Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(A.Vector(0,0,nut_h)).cut(Part.makeCylinder(1.5,nut_h+.2,A.Vector(x,y,z-washer_h-nut_h-.1)))
        moved=washer.copy();moved.translate(A.Vector(0,0,.05))
        contact=common(moved,floor)/.05
        nut_moved=nut.copy();nut_moved.translate(A.Vector(0,0,.05))
        record={'label':row['label'],'xy_mm':[x,y],'nut_bottom_mm':5.94,
                'washer_floor_area_estimate_mm2':contact,
                'nut_washer_area_estimate_mm2':common(nut_moved,washer)/.05,
                'nut_case_overlap_mm3':common(nut,case),'washer_case_overlap_mm3':common(washer,case),
                'floor_overlap_mm3':common(nut.fuse(washer),floor),
                'load_direction':'+Z: nut -> washer -> underside of existing floor',
                'limitations':'Small axial contact probe only. No nut keeper, lateral escape, preload or strength qualification.'}
        rows.append(record);print('NUT_CHECK='+json.dumps(record),flush=True)
        obj=doc.addObject('Part::Feature',row['label']+'_survey')
        obj.Shape=Part.makeBox(7,7,nut_h+washer_h,A.Vector(x-3.5,y-3.5,z-nut_h-washer_h))
        obj.Label=row['label']+' [BOUNDING ENVELOPE, NOT PRINTABLE]';out.append(obj)
    report={'status':'SURVEY_ONLY','nut_af_mm':5.5,'nut_h_mm':2.4,'washer_od_mm':7,'washer_id_mm':3.2,
            'washer_h_mm':.5,'rows':rows,'limitations':['Hardware dimensions are design envelopes; user inventory not measured.',
            'Geometry clearance and bearing-area probes do not validate fastening or strength.',
            'Keeper design and full retention/removal paths remain unverified.']}
    print('NUT_SURVEY='+json.dumps(report),flush=True)
    out[0].addProperty('App::PropertyString','NutSurvey');out[0].NutSurvey=json.dumps(report)
    return out
