"""Collect immutable candidate measurements; never turns a failed FEA into PASS."""
from pathlib import Path
import json
import hashlib
import trimesh

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'


def main():
    rows=[]
    for case in sorted((PART/'_work/analysis').glob('lightweight_*')):
        mesh_path=case/'finished_cage.stl'
        if not mesh_path.exists():
            continue
        mesh=trimesh.load(mesh_path,force='mesh')
        row=dict(case=case.name,sha256=hashlib.sha256(mesh_path.read_bytes()).hexdigest(),
                 two_halves_solid_PETG_g=float(mesh.volume*.0025),
                 watertight=bool(mesh.is_watertight),boundary_shells=len(mesh.split()),fea=[])
        for path in sorted(set(case.glob('fea*/finished_cage_fea.json')) | set(case.glob('fea_grouped/*/finished_cage_fea.json'))):
            data=json.loads(path.read_text(encoding='utf-8'))
            cases=data['cases']
            row['fea'].append(dict(path=path.relative_to(ROOT).as_posix(),
                voxel_mm=cases[0]['voxel_mm'],
                max_displacement_mm=max(c['max_displacement_mm'] for c in cases),
                minimum_safety_factor=min(c['min_safety_factor'] for c in cases),
                minimum_p99_5_safety_factor=min(c['safety_factor_p99_5'] for c in cases),
                all_case_checks_pass=all(c['pass'] for c in cases),
                mesh_convergence='See separate native convergence verdict; single-mesh values are screening only.'))
        for path in [case/'slice_checks.json']:
            if path.exists():
                row['slice']=json.loads(path.read_text(encoding='utf-8'))
        rows.append(row)
    out=PART/'_work/analysis/lightweight_candidate_comparison.json'
    out.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(out)


if __name__=='__main__':
    main()
