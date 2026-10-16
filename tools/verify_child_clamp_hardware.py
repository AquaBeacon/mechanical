"""Check the actual placed purchased hardware against both canonical cage halves."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import trimesh
from child_clamp_case import analysis_case
from verify_child_clamp_cage import native_solid

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=analysis_case(PART)


def placed(item, override=None):
    path=override or ROOT/item['part']/(item['file']+'.stl')
    mesh=trimesh.load(path,force='mesh')
    matrix=np.eye(4)
    for op in item.get('ops',[]):
        for kind,value in op.items():
            if kind=='translate':
                transform=np.eye(4)
                transform[:3,3]=value
            elif kind=='rotate':
                transform=trimesh.transformations.euler_matrix(*np.radians(value),axes='sxyz')
            else:
                raise ValueError('Unverified hardware transform: '+kind)
            matrix=matrix@transform
    mesh.apply_transform(matrix)
    return mesh,matrix,hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',action='store_true',help='Check case STL and proposed placement without publishing it')
    args=parser.parse_args()
    source=ROOT/'assemblies/child_clamp_suspension/placement.json'
    placement=json.loads(source.read_text(encoding='utf-8'))
    override=None
    if args.candidate:
        from child_clamp_placement import candidate_placement
        placement,_=candidate_placement(placement,
            json.loads((CASE/'interface.json').read_text(encoding='utf-8')),
            json.loads((CASE/'geometry_checks.json').read_text(encoding='utf-8')))
        source=CASE/'placement_candidate.json'
        source.write_text(json.dumps(placement,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        override=CASE/'finished_cage.stl'
    items=placement['items']
    clamp_meshes=[placed(i,override) for i in items if i.get('group')=='clamps']
    clamps=[native_solid(m[0]) for m in clamp_meshes]
    if len(clamps)!=2: raise ValueError('Expected two cage halves')
    hardware={i['label']:placed(i) for i in items if i.get('group')=='hardware'}
    if len(hardware)!=48: raise ValueError('Expected 12 bolts, 12 nuts, 24 washers')
    checks=[]
    for label,(mesh,matrix,sha) in hardware.items():
        solid=native_solid(mesh)
        volumes=[abs((solid^clamp).volume()) for clamp in clamps]
        row=dict(label=label,source_sha256=sha,clamp_intersection_mm3=volumes,
                 pass_check=max(volumes)<.01)
        if label.endswith('_bolt'):
            nut=hardware[label[:-5]+'_nut'][0]
            axis=matrix[:3,:3]@np.array([0,0,-1.])
            extension=float(np.max(mesh.vertices@axis)-np.max(nut.vertices@axis))
            row['tip_beyond_nut_mm']=extension
            row['pass_check'] &= extension>=1.5
        checks.append(row)
    result=dict(placement_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        placement_source=str(source),candidate_only=args.candidate,
        clamp_source_sha256=[m[2] for m in clamp_meshes],
        note='Nominal rigid geometry and at least 1.5mm tip beyond nut; not preload or thread strength qualification.',
        components=checks,pass_check=all(r['pass_check'] for r in checks))
    (CASE/'hardware_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(pass_check=result['pass_check'],hardware_count=len(checks),
        maximum_intersection_mm3=max(max(r['clamp_intersection_mm3']) for r in checks),
        minimum_tip_beyond_nut_mm=min(r['tip_beyond_nut_mm'] for r in checks if 'tip_beyond_nut_mm' in r))))
    raise SystemExit(0 if result['pass_check'] else 1)


if __name__=='__main__':main()
