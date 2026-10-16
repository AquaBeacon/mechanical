"""Use existing assembly/access checks on candidate meshes without adoption."""
from pathlib import Path
import argparse, ast, hashlib, json, sys
import trimesh

PART=Path(__file__).resolve().parents[1]
ROOT=PART.parents[4]
sys.path.insert(0,str(ROOT/'tools'))
import prepare_child_horizontal_plate_frame as assembly

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upper',type=Path,required=True)
    parser.add_argument('--lower',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    placement=json.loads((assembly.OUT/'placement.json').read_text(encoding='utf-8'))
    world=assembly.load_world(placement)
    candidates={f'clamp_linked_{half}':trimesh.load(path,force='mesh') for half,path in [('upper',args.upper),('lower',args.lower)]}
    reports={}
    for row,mesh in world:
        if row['label'] in candidates:
            candidate=candidates[row['label']]
            if not candidate.is_volume or len(candidate.split())!=1: raise RuntimeError('Invalid candidate mesh')
            mesh.vertices=candidate.vertices.copy();mesh.faces=candidate.faces.copy()
            mesh.apply_transform(assembly.matrix(row['ops']))
            reports[row['label']]=dict(volume_mm3=float(candidate.volume),dimensions_mm=candidate.extents.tolist())
    log=(assembly.OUT/'_work/logs/layout.log').read_text(encoding='utf-8')
    interfaces=dict(ast.literal_eval(next(line[6:] for line in log.splitlines() if line.startswith('ECHO: ["INTERFACES"')))[1:])
    assembly.load_world=lambda _:world
    original_save=assembly.save
    assembly.save=lambda _,data:original_save(args.out/'assembly_validation.json',data)
    assembly.validate(placement,reports,interfaces)
    fixed=[(row,mesh) for row,mesh in world if row['print'] and row['label'] not in ['clamp_linked_upper','removable_upper_frame']]
    vessel=[(row,mesh) for row,mesh in world if row['group']=='vessel']
    failures=[];poses=[]
    for height in [0,.5,1,2,5,10,20,40,80,100]:
        blocked=[]
        for row,mesh in vessel:
            raised=mesh.copy();raised.apply_translation([0,0,height])
            for target,other in fixed:
                overlap=assembly.overlap(raised,other)
                if overlap>.1: blocked.append(dict(vessel=row['label'],part=target['label'],overlap_mm3=overlap))
        poses.append(dict(lift_mm=height,blocked=blocked));failures.extend(blocked)
    original_save(args.out/'vessel_entry.json',dict(result='FAIL' if failures else 'PASS',poses=poses,failures=failures,
        candidate_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [args.upper,args.lower]}))
    if failures: raise RuntimeError('Vessel insertion failed')
    print('CANDIDATE_ASSEMBLY_PASS: structural pairs, fasteners, drivers, nut entries, hand/cable/band reservations and 10 vessel entry poses')

if __name__=='__main__': main()
