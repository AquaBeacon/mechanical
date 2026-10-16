"""Check final changed structures against every neighbour; record mesh integrity."""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, str(Path('scad/lib').resolve()))
from check_asm_contacts import load, surface_samples, inset_samples

np.random.seed(20260926)
items=json.loads(Path('assemblies/child_interior/placement.json').read_text(encoding='utf-8'))['items']
items=[it for it in items if it.get('group')=='interior']
meshes={it['label']:load(Path('.'),it) for it in items}
fast={it['label'] for it in items if '/cots/screw' in it['part'] or '/cots/hex_spacer' in it['part']}
changed=('vtray_deck','flange_brace')
bad=[]
for name in changed:
    m=meshes[name]
    print(name,'watertight',m.is_watertight,'components',len(m.split()),flush=True)
    assert m.is_watertight and len(m.split())==1
    sm=surface_samples(m)
    tm=cKDTree(sm)
    im=inset_samples(m)
    for other,n in meshes.items():
        if other==name or other in fast:
            continue
        if np.any(m.bounds[0]>n.bounds[1]+0.3) or np.any(n.bounds[0]>m.bounds[1]+0.3):
            continue
        sn=surface_samples(n)
        tn=cKDTree(sn)
        gap=min(tn.query(sm)[0].min(),tm.query(sn)[0].min())
        if gap>=0.3:
            continue
        pen=0
        for pts,dst,tree in ((im,n,tn),(inset_samples(n),m,tm)):
            if not dst.is_watertight:
                continue
            inside=dst.contains(pts)
            if inside.sum()>=3:
                pen=max(pen,float(tree.query(pts[inside])[0].max()))
        print(name,other,'gap',round(gap,3),'penetration',round(pen,3),flush=True)
        if pen>0.05:
            bad.append((name,other,pen))
print('INTERFERENCES',bad,flush=True)
sys.exit(bool(bad))
