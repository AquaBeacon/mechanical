"""Canonical related parts for the north penetrator/floor access revision."""
from pathlib import Path
import json
import sys
import FreeCAD as A
import Part


def battery_from_source(root):
    source=(root/'spec/build_parent_hand_service.py').read_text(encoding='utf-8')
    (root/'assemblies/parent_hand_service').mkdir(parents=True,exist_ok=True)
    (root/'parts/parent/interior/printed/parent_hand_service').mkdir(parents=True,exist_ok=True)
    scope=dict(__file__=str(root/'spec/build_parent_hand_service.py'))
    exec(compile(source.split('def holes(board):')[0],'battery_existing_prelude','exec'),scope)
    scope['P']=root.parent/'battery_debug';scope['P'].mkdir(parents=True,exist_ok=True)
    captured={};scope['save']=lambda name,c:captured.update({name:c.s.removeSplitter()})
    function='def build_battery_base():'+source.split('def build_battery_base():',1)[1].split("if '--battery-only'",1)[0]
    exec(compile(function,'existing_battery_generator','exec'),scope)
    scope['build_battery_base']()
    from parent_battery_slide import rail_support_blocker
    captured['battery_slide_rail_support_blocker']=rail_support_blocker()
    return captured


def gnss_frame_from_source(root,parameters):
    source=(root/'spec/build_parent_gnss.py').read_text(encoding='utf-8')
    scope=dict(__file__=str(root/'spec/build_parent_gnss.py'))
    exec(compile(source.split('if not FIXTURES_ONLY and not CASE_ACCESS_ONLY:')[0],'gnss_existing_prelude','exec'),scope)
    scope['P']=root.parent/'gnss_debug';scope['P'].mkdir(parents=True,exist_ok=True)
    scope['G'].power_switch_centres=lambda:parameters['switch_centres']
    captured={};scope['save']=lambda folder,name,s,*args:captured.update({name:s})
    marker="F=R/'parts/parent/interior/printed/gnss_universal_carrier'"
    body=marker+source.split(marker,1)[1].split('if FIXTURES_ONLY:',1)[0]
    exec(compile(body,'existing_gnss_frame','exec'),scope)
    return captured['gnss_universal_carrier']


def build(doc,parameters):
    root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scad/lib'))
    import parent_gnss as G
    from parent_service_retrofit import fixed_sensor_columns,ring_service,main_antenna_cradle,power_adapter,cable_routes
    from parent_corner_mounts import sony_shapes,sony_holes
    from parent_case_access import finish_cut,BATTERY_TOOL_D
    from parent_penetrator_access import vendor_shapes
    mh=[[18+x,112-y] for x,y in parameters['pcb_holes']['PARENT_MAIN']]
    ph=[[25.8+y,115+x] for x,y in parameters['pcb_holes']['PARENT_PWR']]
    shapes=main_antenna_cradle(mh,G,True)
    if parameters.get('only_underside_nuts'):
        shapes={'main_service_frame':shapes['main_service_frame']}
        shapes.update(fixed_sensor_columns(G,parameters['pcb_holes']['TX_improved']))
        result=[]
        for name,shape in shapes.items():
            assert shape.isValid() and len(shape.Solids)==1,name
            obj=doc.addObject('Part::Feature',name);obj.Shape=shape;result.append(obj)
        return result
    shapes['power_adapter']=power_adapter(ph)
    shapes.update(fixed_sensor_columns(G,parameters['pcb_holes']['TX_improved']))
    shapes.update(sony_shapes(sony_holes(G),G))
    shapes.update(battery_from_source(root))
    # The legacy generator tessellates while composing its generated SCAD.
    # Drop that display triangulation before the foundation compares analytic
    # bounds across FCStd/STEP reopening; the B-Rep surfaces are unchanged.
    shapes['battery_base']=shapes['battery_base'].cleaned()
    shapes['gnss_universal_carrier']=gnss_frame_from_source(root,parameters)
    ring=Part.read(str(root/'parts/parent/interior/printed/ann_mb1_internal_rack/ann_mb1_coax_ring.step'))
    shapes['ann_mb1_coax_ring_service']=ring_service(ring)
    shapes.update(vendor_shapes(root))
    shapes.update(cable_routes(G))
    # Conservative screw reference only: actual head height and length still
    # need measurement. Seat and nominal12mm engagement follow the old model.
    head=Part.makeCylinder(5,5,A.Vector())
    stem=Part.makeCylinder(2,12,A.Vector(0,0,-12))
    shapes['screw_m4x12_head10_h5_envelope']=head.fuse(stem)
    shapes['screw_m4x18_socket']=Part.makeCylinder(3.5,4,A.Vector()).fuse(Part.makeCylinder(2,18,A.Vector(0,0,-18)))
    shapes['nylon_screw_m2x10_envelope']=Part.makeCylinder(2,1.6,A.Vector()).fuse(Part.makeCylinder(1,G.MAG_BOLT_LENGTH,A.Vector(0,0,-G.MAG_BOLT_LENGTH)))
    shapes['nylon_washer_m2_05_envelope']=Part.makeCylinder(2.5,.5,A.Vector()).cut(Part.makeCylinder(1.1,1,A.Vector(0,0,-.1)))
    from parent_service_datums import SENSOR_BASE_Z
    for name,points in [('gnss_support_frame',G.UNIVERSAL_FRAME_FOOT_XY),('sony_support_frame',G.SONY_CARRIER_FOOT_XY)]:
        shapes[name+'_support_blocker']=Part.makeCompound([
            Part.makeBox(3.4,3.4,11.5,A.Vector(x-1.7,y-1.7,SENSOR_BASE_Z-.2))
            for i,(x,y) in enumerate(points) if name.startswith('gnss') or i!=2])
    result=[]
    for name,shape in shapes.items():
        assert shape.isValid() and len(shape.Solids)>0,name
        if not name.startswith('wetlink_') and not name.endswith('_support_blocker'):assert len(shape.Solids)==1,name
        obj=doc.addObject('Part::Feature',name);obj.Shape=shape;result.append(obj)
    return result
