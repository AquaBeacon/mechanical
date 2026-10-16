"""A fresh study: immutable existing clamp bands, density-optimized connections.

Preserving original functional bands is an input choice before optimization,
not a reconstruction of optimized material. The connecting envelope stays broad.
"""
from pathlib import Path
import hashlib,json
import trimesh

PART=Path(__file__).resolve().parents[1]
BASE=PART/'_work/analysis/topology_print'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out=BASE/'connection_only/inputs';out.mkdir(parents=True,exist_ok=False)
    request=json.loads((PART/'spec/print_topology_request.json').read_text())
    pitch=request['interfaces']['station_pitch_mm']
    rows=[]
    for half in ['upper','lower']:
        original=PART/f'child_wte4_petg_clamp_{half}.stl'
        band=trimesh.load(original,force='mesh');second=band.copy();second.apply_translation([0,0,pitch])
        preserve=trimesh.util.concatenate([band,second])
        path=out/f'{half}_complete_band_preserve.stl'
        path.write_text(trimesh.exchange.stl.export_stl_ascii(preserve),encoding='ascii')
        baseline=PART/f'child_wte4_petg_clamp_{half}_linked.stl'
        design=trimesh.load(BASE/f'{half}_design_space.stl',force='mesh')
        old=trimesh.load(baseline,force='mesh')
        budget=float(old.volume)*.99
        free=float(design.volume-preserve.volume)
        fraction=(budget-preserve.volume)/free
        if not 0<fraction<.2:raise RuntimeError('Connection budget inconsistent')
        study=json.loads((PART/f'spec/{half}_print_topology_study.json').read_text())
        study['_what']=f'{half}: preserve original full functional bands; optimize connecting material only'
        study['_why']='Clean vertical printing and no greater sliced material/time than the original linked part. Preserve smooth rubber/seat/nut interfaces before optimization.'
        study['_scope']='Connection optimization only. The complete original 40 mm bands are immutable CAD inputs, not claimed to be topology optimized.'
        study['_preload']='Six actual bolt-seat patches, each 150 N, total 900 N. Separated from contact constraints. Provisional sensitivity bound, not a torque recommendation.'
        study['geometry']['preserve']['interfaces']['stl']=str(path.resolve())
        study['design']['volfrac']=fraction
        study['finish']['add']['interfaces']=str(path.resolve())
        study['_volume_budget']=dict(baseline_mm3=float(old.volume),preserve_mm3=float(preserve.volume),
            free_envelope_mm3=free,total_target_mm3=budget,free_fraction=fraction,
            target_basis='1 percent below original CAD volume; actual slice must also be no worse')
        target=PART/f'spec/{half}_connection_topology_study.json'
        target.write_text(json.dumps(study,indent=2)+'\n',encoding='utf-8')
        rows.append(dict(half=half,study=str(target),preserve_components=len(preserve.split()),
            volume_budget=study['_volume_budget'],inputs_sha256={str(p):sha(p) for p in [original,baseline,path,BASE/f'{half}_design_space.stl',BASE/f'{half}_cuts.stl']}))
    (out/'input_manifest.json').write_text(json.dumps(dict(status='exploration_only',inputs=rows),indent=2)+'\n')
    print(json.dumps(rows,indent=2),flush=True)

if __name__=='__main__':main()
