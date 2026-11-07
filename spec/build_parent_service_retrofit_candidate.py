"""Isolated native build of candidate parts; does not update production files."""
from pathlib import Path
import json,sys

def build(doc,parameters):
    root=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(root/'scad/lib'))
    import parent_gnss as G
    from parent_service_retrofit import collect_shapes,retrofit_fasteners,variant_folder
    data=json.loads((root/'assemblies/parent_hand_service/_work/analysis/retrofit_20261024/interfaces.json').read_text(encoding='utf-8'))
    print('INTERFACES='+json.dumps(data),flush=True)
    main=[[18+x,112-y] for x,y in data['PARENT_MAIN']['holes'].values()]
    pwr=[[25.8+y,115+x] for x,y in data['PARENT_PWR']['holes'].values()]
    out=[]
    shapes=collect_shapes(G,main,pwr,parameters['pcb_holes']['TX_improved'])
    print('RETROFIT_METADATA='+json.dumps(dict(folders={n:variant_folder(n) for n in shapes},fasteners=retrofit_fasteners(G,main,pwr),keeper_instances=[[x,y+(-3.9 if y<60 else 3.9),21.8] for x,y in G.RACK_FOOT_XY])),flush=True)
    for name,shape in shapes.items():
        obj=doc.addObject('PartDesign::Feature',name)
        obj.Label=name+' [EXPERIMENTAL - NOT RELEASED]';obj.Shape=shape
        out.append(obj)
        print('CANDIDATE='+json.dumps({'name':name,'valid':shape.isValid(),'solids':len(shape.Solids),'volume_mm3':shape.Volume}),flush=True)
    return out
