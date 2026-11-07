"""Rev.7 removable vessel locators; retain the current integral camera and skids."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
SCREWS='parts/common/interior/cots/screw'
LOCATORS='parts/parent/exterior/printed/parent_oneplate_box_locator'

def main():
    p=A/'placement.json';data=json.loads(p.read_text(encoding='utf-8'))
    data['items']=[i for i in data['items'] if not i['label'].startswith('bolt_on_')]
    def add(label,part,file,xyz=None,rot=None,group='hardware'):
        ops=[] if xyz is None else [{'translate':xyz}]
        if rot:ops.append({'rotate':rot})
        data['items'].append(dict(label='bolt_on_'+label,part=part,file=file,ops=ops,
                                 group=group,color='Silver' if group=='hardware' else 'MediumSeaGreen'))
    for variant in ('side_left','side_right','end_fixed','end_push'):
        add(variant,LOCATORS,'parent_oneplate_box_locator_'+variant,group='exterior')
    for x in (-110,110):
        for y in (-8,8):
            add(f'side_bolt_{x}_{y}',SCREWS,'screw_m4x20_socket',[x,y,1.3])
            add(f'side_nut_{x}_{y}',SCREWS,'screw_nut_m4',[x,y,-15.5])
    for s in (-1,1):
        for y in (52,62):
            add(f'end_bolt_{s}_{y}',SCREWS,'screw_m4x25_socket',[s*94,s*y,-27.3],[180,0,0])
            add(f'end_nut_{s}_{y}',SCREWS,'screw_nut_m4',[s*94,s*y,-7.3])
    data['vessel_locator_revision']='removable_r7_20261022'
    data['note']='Rev.7 flat lower plate, four removable vessel locators; retain printed upper clamp/skids and current integral camera. Side M4x20 x4, end M4x25 x4, M4 nuts x8.'
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Configured removable vessel locators; retained current sensor and printed-part placements.')

if __name__=='__main__':main()
