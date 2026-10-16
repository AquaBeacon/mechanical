"""Collect native results and a comparison-only FEA file; no solver or new verdict rules."""
from pathlib import Path
import hashlib
import json
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=analysis_case(PART)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    study=read(CASE/'study_final.json')
    grouped=read(CASE/'grouped_convergence.json')
    paths=sorted((CASE/'fea_grouped').glob('group_*/finished_cage_fea.json'))
    cases=[c for p in paths for c in read(p)['cases']]
    complete=len(cases)==len(study['required_cases']) and {c['case'] for c in cases}==set(study['required_cases'])
    if complete:
        comparison=read(paths[0])
        comparison['cases']=cases
        comparison['pass']=bool(grouped.get('pass',False))
        comparison['_comparison_only']='Unmodified native fine-mesh fields concatenated for native CCX comparison. Pass remains false if native mesh convergence fails.'
        comparison['_sources']=[dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]
        save(CASE/'voxel_comparison.json',comparison)
    geometry=read(CASE/'geometry_checks.json')
    sliced=read(CASE/'slice_checks.json')
    hardware=read(CASE/'hardware_checks.json') if (CASE/'hardware_checks.json').exists() else {}
    step=read(CASE/'step_checks.json') if (CASE/'step_checks.json').exists() else {}
    ccx_path=CASE/'ccx/ccx_summary.json'
    ccx=read(ccx_path) if ccx_path.exists() else None
    ccx_execution=read(CASE/'ccx_execution.json') if (CASE/'ccx_execution.json').exists() else None
    # Native ccx_summary has per-run and convergence verdicts, no top-level pass.
    # Preserve the native CLI exit verdict and separately expose solver agreement.
    ccx_runs=(ccx or {}).get('runs',[])
    ccx_native_pass=bool(ccx_execution and ccx_execution['exit_code']==0
                        and len(ccx_runs)==3 and all(r.get('pass') for r in ccx_runs)
                        and ccx['mesh_convergence'].get('pass'))
    ccx_cases=ccx_runs[-1].get('cases',[]) if ccx_runs else []
    ccx_complete=bool(len(ccx_cases)==len(study['required_cases']) and
                      {c['case'] for c in ccx_cases}==set(study['required_cases']))
    # Native CCX judges strength/equilibrium/mesh quality; explicitly check the
    # study's displacement limit as well, without changing any native verdict.
    ccx_stiffness=bool(ccx_complete and all(c.get('max_disp_mm') is not None and
        c['max_disp_mm']<=study['max_deflection_mm'] for c in ccx_cases))
    comparison=(ccx or {}).get('vs_voxel_fea_cases',{})
    if complete and ccx_runs:
        # Use the identical native comparison routine after the fine voxel jobs
        # finish. CCX may have started against the earlier screening output;
        # preserve its original summary and CLI verdict without rewriting them.
        from topopt.cli.ccx import _compare_voxel_fea
        comparison=_compare_voxel_fea(str(CASE/'voxel_comparison.json'),ccx_runs[-1])
        save(CASE/'ccx_fine_voxel_comparison.json',dict(
            native_function='topopt.cli.ccx._compare_voxel_fea',
            input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                [CASE/'voxel_comparison.json',ccx_path]},comparison=comparison))
    ccx_comparison_pass=bool(comparison.get('total')==len(study['required_cases'])
                             and comparison.get('within')==comparison.get('total'))
    log_path=CASE/'ccx_run.log'
    log=log_path.read_text(encoding='utf-8') if log_path.exists() else ''
    diagnostics=[]
    for marker in ['below the absolute minimum 1.5',
                   'the load/reaction balance did not close',
                   'nonpositive jacobian']:
        if marker in log:
            diagnostics.append(marker)
    result=dict(case=CASE.name,source_stl_sha256=geometry['sha256'],
        digital_geometry_pass=bool(geometry['pass'] and sliced['pass_check'] and hardware.get('pass_check') and step.get('pass_check')),
        required_case_count=len(study['required_cases']),
        all_original_native_fine_cases_present=complete,
        native_fine_case_checks_pass=bool(complete and all(c['pass'] for c in cases)),
        worst_element_floor_1p5_pass=bool(complete and all(c['min_safety_factor']>=1.5 for c in cases)),
        native_mesh_convergence_pass=bool(grouped.get('pass',False)),
        fine_voxel_mm=sorted({c['voxel_mm'] for c in cases}),
        native_fine_max_displacement_mm=max((c['max_displacement_mm'] for c in cases),default=None),
        native_fine_min_safety_factor=min((c['min_safety_factor'] for c in cases),default=None),
        native_fine_min_p99_5_safety_factor=min((c['safety_factor_p99_5'] for c in cases),default=None),
        ccx_summary_present=ccx is not None,ccx_native_pass=ccx_native_pass,
        ccx_all_required_cases_present=ccx_complete,
        ccx_all_cases_stiffness_pass=ccx_stiffness,
        ccx_finest_max_displacement_mm=max((c['max_disp_mm'] for c in ccx_cases if c.get('max_disp_mm') is not None),default=None),
        ccx_finest_min_worst_safety_factor=min((c['worst_element_safety_factor'] for c in ccx_cases if c.get('worst_element_safety_factor') is not None),default=None),
        ccx_finest_min_p99_5_safety_factor=min((c['safety_factor_p99_5'] for c in ccx_cases if c.get('safety_factor_p99_5') is not None),default=None),
        ccx_voxel_case_comparison_pass=ccx_comparison_pass,
        ccx_native_log_failures=diagnostics,
        ccx_execution=ccx_execution,
        two_halves_cad_mass_g=geometry['PETG_mass_g_two_halves'],
        two_halves_sliced_filament_g=2*sliced['filament_g'],
        slice_reduction_percent=100*(1-2*sliced['filament_g']/1516.08),
        physical_qualification='Not performed: unknown EPDM hardness/friction, wet slip, PETG creep and actual print variability.',
        status='exploration_only')
    result['numerical_strength_qualification_pass']=bool(result['all_original_native_fine_cases_present'] and result['native_fine_case_checks_pass'] and result['worst_element_floor_1p5_pass'] and result['native_mesh_convergence_pass'] and result['ccx_native_pass'] and result['ccx_all_cases_stiffness_pass'] and result['ccx_voxel_case_comparison_pass'])
    save(CASE/'validation_summary.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
