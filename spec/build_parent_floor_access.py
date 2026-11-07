"""Isolated candidate from the existing floor source; no production publishing."""
from pathlib import Path
import json


def build(doc, parameters):
    root = Path(__file__).resolve().parents[1]
    (root/'assemblies/parent_hand_service').mkdir(parents=True, exist_ok=True)
    (root/'parts/parent/interior/printed/parent_hand_service').mkdir(parents=True, exist_ok=True)
    source = (root/'spec/build_parent_hand_service.py').read_text(encoding='utf-8')
    scope = dict(__file__=str(root/'spec/build_parent_hand_service.py'))
    exec(compile(source.split('def holes(board):')[0], 'existing_floor_prelude', 'exec'), scope)
    # OCC STEP writer on Windows rejects long (>260 character) debug paths.
    scope['P'] = root.parent/'floor_debug'
    scope['P'].mkdir(parents=True, exist_ok=True)
    scope['holes'] = lambda board: parameters['pcb_holes'][board]
    output = {}
    scope['save'] = lambda name, c: output.update({name:c.s.removeSplitter()})
    body = (root/'spec/parent_switch_tx_body.py').read_text(encoding='utf-8').split('# Battery source')[0]
    before,after=body.split('from parent_floor_access import add_floor_access',1)
    if parameters.get('base_cache'):
        import Part
        exec(compile(before.split('grid_x=')[0],'floor_datums','exec'),scope)
        shape=Part.Shape();shape.read(str(root/parameters['base_cache']))
        assert shape.isValid() and len(shape.Solids)==1
        scope['floor']=scope['CSG'](shape,'')
    else:
        exec(compile(before,'existing_floor_base','exec'),scope)
        assert scope['floor'].s.isValid() and len(scope['floor'].s.Solids)==1
        scope['floor'].s.exportBrep(str(root.parent/'floor_base.brep'))
        print('FLOOR_BASE_CACHED',flush=True)
    exec(compile('from parent_floor_access import add_floor_access'+after,'floor_access_features','exec'),scope)
    floor = output['floor_plate']
    assert floor.isValid() and len(floor.Solids) == 1
    obj = doc.addObject('Part::Feature', 'floor_plate')
    obj.Shape = floor
    obj.addProperty('App::PropertyString', 'AccessReport')
    obj.AccessReport = json.dumps(scope['floor_access_report'])
    print('FLOOR_ACCESS_REPORT='+obj.AccessReport, flush=True)
    return [obj]
