"""Associate actual final STL hashes with native solver and convergence results."""
from pathlib import Path
import json,hashlib,trimesh,math
from geometry import layout

ROOT=Path(__file__).resolve().parents[2];P=ROOT/'parts/common/jigs/over_center_latch'
cases={n:'dji_groove40N_20261010_ribs55_plate6_h05_serial' for n in ['base','lever','bail']}
cases['keeper']='dji_groove40N_20261010_ribs55_plate6'
report={}
for name,case in cases.items():
    run=P/'_work/analysis'/case;study_path=run/'studies'/(name+'_study.json')
    study=json.loads(study_path.read_text(encoding='utf-8'))
    canonical=P/('over_center_latch_'+name+'.stl')
    current_sha=hashlib.sha256(canonical.read_bytes()).hexdigest()
    exact_surface_equivalence=False
    if study['_canonical_source_sha256']!=current_sha:
        # OpenSCAD may reorder identical facets between builds. Verify exact
        # vertices and triangle surfaces, not just bounds or sampled distances.
        recorded=json.loads((run/'studies/parameters.json').read_text(encoding='utf-8'))
        label='link_left' if name=='bail' else name
        item=next(i for i in layout(recorded) if i['label']==label)
        a,b=trimesh.load(canonical),trimesh.load(study['part'])
        a.apply_transform(trimesh.transformations.rotation_matrix(math.radians(item['ops'][1]['rotate'][1]),[0,1,0]))
        a.apply_translation(item['ops'][0]['translate'])
        assert a.is_volume and b.is_volume and a.is_watertight and b.is_watertight,name
        def surfaces(m):return sorted(tuple(sorted(tuple(v) for v in t)) for t in m.triangles)
        assert surfaces(a)==surfaces(b),(name,'final geometry differs from analysed shape')
        exact_surface_equivalence=True
    assert study['_source_sha256']==hashlib.sha256(Path(study['part']).read_bytes()).hexdigest(),name
    result_path=run/(name+'_convergence')/(name+'_closed_fea.json')
    conv_path=run/(name+'_convergence')/(name+'_closed_fea_convergence.json')
    result=json.loads(result_path.read_text(encoding='utf-8'));conv=json.loads(conv_path.read_text(encoding='utf-8'))
    report[name]=dict(study=str(study_path.relative_to(ROOT)),result=str(result_path.relative_to(ROOT)),
        convergence=str(conv_path.relative_to(ROOT)),canonical_stl_sha256=current_sha,
        analysed_canonical_stl_sha256=study['_canonical_source_sha256'],
        exact_surface_equivalence_despite_serialisation_order=exact_surface_equivalence,
        native_case_checks_pass=result['pass'],mesh_convergence_pass=conv['pass'],cases=result['cases'],
        convergence_cases=conv['cases'])
summary=dict(status='prototype_strength_verification_incomplete',parts=report,
    limitations=['All analysis input hashes verified; final source SHA equality or exact triangle-surface equivalence verified.',
        'Native percentile-based case checks do not certify worst-element stresses.',
        'Mesh convergence is required; the remaining FAIL verdicts are retained.',
        'Base 100 N direct-press case has a worst-element safety factor below one at the fixture boundary.',
        'CalculiX comparison could not mesh the refined STL shell; no CCX strength result.',
        '40 N is a nominal rubber-model target, not a measured or certified force.'])
out=ROOT/'assemblies/over_center_latch/_work/analysis/verification/strength_report.json'
out.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
for name,r in report.items():
    print(name,'worst SF',round(min(c['min_safety_factor'] for c in r['cases']),2),
        'p99.5 SF',round(min(c['safety_factor_p99_5'] for c in r['cases']),2),
        'max displacement',round(max(c['max_displacement_mm'] for c in r['cases']),4),
        'mesh convergence',r['mesh_convergence_pass'])
