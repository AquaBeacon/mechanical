"""Foundation recipe for the canonical parent battery base and top-lift lid.

The legacy generator is executed with all exports redirected to a temporary
folder. Only the returned document objects are exported by the foundation.
"""
from pathlib import Path
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[1]


def build(doc, parameters):
    if parameters:
        raise ValueError('This recipe has no editable parameters')
    source = (ROOT / 'spec/build_parent_hand_service.py').read_text(encoding='utf-8')
    (ROOT / 'assemblies/parent_hand_service').mkdir(parents=True, exist_ok=True)
    scope = {'__file__': str(ROOT / 'spec/build_parent_hand_service.py')}
    exec(compile(source.split('def holes(board):')[0], 'battery_prelude', 'exec'), scope)
    captured = {}
    with tempfile.TemporaryDirectory(prefix='parent_battery_') as temp:
        scope['P'] = Path(temp)
        scope['save'] = lambda name, c: captured.update({name: c.s.removeSplitter()})
        function = 'def build_battery_base():' + source.split('def build_battery_base():', 1)[1].split("if '--battery-only'", 1)[0]
        exec(compile(function, 'battery_generator', 'exec'), scope)
        scope['build_battery_base']()
    captured['battery_base'] = captured['battery_base'].cleaned()
    sys.path.insert(0, str(ROOT / 'scad/lib'))
    from parent_battery_slide import lid
    captured['parent_lipo_retainer_lid_slide'] = lid(scope['bc']['bolt_xy'])
    result = []
    for name, shape in captured.items():
        obj = doc.addObject('Part::Feature', name)
        obj.Shape = shape
        result.append(obj)
    doc.recompute()
    return result
