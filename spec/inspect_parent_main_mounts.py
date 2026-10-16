"""Read-only mounting review; cylinders are clearance probes, not print parts.

Use the existing FreeCAD native runner. No canonical CAD/configuration is written.
"""
from pathlib import Path
import json,sys

def build(doc, parameters):
    import FreeCAD as A,Part
    root=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(root/'spec'))
    from parent_access_common import common
    placement=json.loads((root/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
    holes=json.loads((root/'assemblies/parent_hand_service/hole_sources.json').read_text(encoding='utf-8'))['MAIN']
    targets=['box_bcas212310g','p_main','antenna_rack','coax_ring','coax_coil_keepout','p_pwr','gnss_coax_route']
    scene={}
    for it in placement['items']:
        if it['label'] not in targets+['main_lower_carrier']:continue
        shape=Part.read(str(root/it['part']/(it.get('file',Path(it['part']).name)+'.step')))
        for op in reversed(it['ops']):
            if 'rotate' in op:
                for axis,angle in zip([A.Vector(1,0,0),A.Vector(0,1,0),A.Vector(0,0,1)],op['rotate']):shape.rotate(A.Vector(0,0,0),axis,angle)
            if 'translate' in op:shape.translate(A.Vector(*op['translate']))
        scene[it['label']]=shape
    objects=[]
    for i,(x,y) in enumerate(holes):
        shape=Part.makeCylinder(3.5,41.95-18.8,A.Vector(x,y,18.8)).cut(Part.makeCylinder(1.725,41.95-18.8+.2,A.Vector(x,y,18.7)))
        row={n:common(shape,scene[n]) for n in targets}
        obj=doc.addObject('PartDesign::Feature','MainMountProbe'+str(i));obj.Label='Exploration only: direct MAIN corner '+str(i)
        obj.Shape=shape
        obj.addProperty('App::PropertyBool','ExplorationOnly','Review');obj.ExplorationOnly=True
        obj.addProperty('App::PropertyString','CornerXY','Review');obj.CornerXY=json.dumps([x,y])
        obj.addProperty('App::PropertyString','IntersectionsMm3','Review');obj.IntersectionsMm3=json.dumps(row)
        obj.addProperty('App::PropertyString','CurrentCarrierVolumeMm3','Review');obj.CurrentCarrierVolumeMm3=str(scene['main_lower_carrier'].Volume)
        print('MAIN_MOUNT_REVIEW',json.dumps(dict(corner=i,xy_mm=[x,y],overlap_mm3=row,current_carrier_mm3=scene['main_lower_carrier'].Volume)),flush=True)
        objects.append(obj)
    return objects
