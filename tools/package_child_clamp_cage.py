"""Publish verified cage geometry as the existing assembly's prototype package.

Geometry/slice validation is mandatory. Native independent strength remains a
separate verdict, never inferred from successful packaging or printer fit.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
ASSEMBLY = ROOT/'assemblies/child_clamp_suspension'
from child_clamp_case import analysis_case
CASE = analysis_case(PART)


def save(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--geometry-only', action='store_true', help='stage CAD/source/placement while slice is pending; does not qualify printing')
    parser.add_argument('--parametric', action='store_true', help='publish the canonical parametric topology reconstruction, without replacing the historic density source')
    args = parser.parse_args()
    policy=PART/'spec/topology_postprocess_policy.json'
    if args.parametric and policy.exists() and json.loads(policy.read_text(encoding='utf-8')).get('mode')=='direct_smoothed_density':
        raise RuntimeError('User requires directly smoothed topology, not a parametric lattice replacement.')
    geometry = json.loads((CASE/'geometry_checks.json').read_text(encoding='utf-8'))
    if not geometry['pass']:
        raise RuntimeError('Final geometry did not pass')
    source = CASE/'finished_cage.stl'
    if hashlib.sha256(source.read_bytes()).hexdigest()!=geometry['sha256']:
        raise RuntimeError('Geometry checks belong to another STL')
    proof={}
    if policy.exists() and json.loads(policy.read_text(encoding='utf-8')).get('mode')=='direct_smoothed_density':
        proof=json.loads((CASE/'final_provenance.json').read_text(encoding='utf-8'))
        if ('no replacement ribs' not in proof.get('source','') or
            proof.get('final_sha256')!=geometry['sha256'] or
            proof.get('finishing_scad_sha256')!=hashlib.sha256((PART/'child_wte4_suspension_clamp.scad').read_bytes()).hexdigest()):
            raise RuntimeError('Direct-density provenance does not match the current CAD and checked STL')
        if proof.get('design_parameters') and not proof.get('native_compiled_csg_identical_after_default_adoption'):
            raise RuntimeError('Adopt checked direct-density parameters with native CSG identity proof before packaging')
    if not args.geometry_only:
        sliced = json.loads((CASE/'slice_checks.json').read_text(encoding='utf-8'))
        if not sliced['pass_check'] or sliced['part_sha256']!=geometry['print_orientation_stl_sha256']:
            raise RuntimeError('Actual analysed print orientation did not pass Bambu Studio slice')
    if not args.parametric:
        shutil.copy2(CASE/'cage_density_surface.stl', PART/'spec/cage_density_surface.stl')
    if args.parametric:
        adoption=json.loads((CASE/'canonical_adoption.json').read_text(encoding='utf-8'))
        actual_source=hashlib.sha256((PART/'child_wte4_suspension_clamp.scad').read_bytes()).hexdigest()
        if (not adoption['native_compiled_csg_identical'] or
            adoption['source_after_sha256']!=actual_source or
            adoption['candidate_stl_sha256']!=geometry['sha256']):
            raise RuntimeError('Canonical CAD does not match the compiled and rendered candidate')
        # Publish the checked build after default-only source adoption. Preserve
        # content exactly, but timestamp this export now rather than before the
        # source change whose compiled CSG was proved byte-identical.
        shutil.copyfile(source, PART/'child_wte4_suspension_clamp_cage.stl')
    else:
        if proof.get('native_compiled_csg_identical_after_default_adoption'):
            # Publish the already rendered candidate after proving the default
            # adoption compiles identically; retain its original hash in proof.
            shutil.copyfile(source, PART/'child_wte4_suspension_clamp_cage.stl')
        else:
            shutil.copy2(source, PART/'child_wte4_suspension_clamp_cage.stl')
    (PART/'variants.txt').write_text('half model="half"\nliner model="liner"\ncage model="cage"\n',encoding='utf-8')
    metadata = json.loads((PART/'manufacturing.json').read_text(encoding='utf-8'))
    metadata['non_print_files'] = ['child_wte4_suspension_clamp_liner','child_wte4_suspension_clamp_smooth']
    metadata['print_rotations_deg'] = {'child_wte4_suspension_clamp_half':[0,0,0], 'child_wte4_suspension_clamp_cage':[90,0,0]}
    metadata['source_dependencies'] = ['spec/cage_density_surface.stl','spec/bambu_petg_basic_material.json']
    if args.parametric:
        metadata['source_dependencies'] = ['spec/bambu_petg_basic_material.json']
    metadata['degenerate_edge_flip_files'] = ['child_wte4_suspension_clamp_cage']
    metadata['note'] = 'Three connected M3 clamp bands and one 10.5mm eye per half, two identical cage halves. User confirmed 1mm rubber; provisional 20% compression. Bambu PETG Basic V3.0, 100% infill, 8 walls/shells, 0.20mm, 0.4 nozzle. Source Y build, rotate X90. Exploration only until independent strength, wet slip/creep and physical print trials qualify. Old smooth single-half files are historical and non-print.'
    if args.parametric:
        metadata['note'] += ' Parametric reconstruction informed by native topology load paths; not an unmodified density mesh. All three mounting patterns retained.'
    metadata['closed_void_policy'] = 'No enclosed cavities in material; keep vessel space, bolt/tool bores and rope hole open'
    void_free = (CASE/'void_free_revision.json').exists()
    if void_free:
        metadata['closed_void_policy'] = 'No enclosed cavities in material; keep vessel space, bolt/tool bores and rope hole open'
        metadata['note'] += ' 2026-10-02: enclosed cavity filled by CAD postprocessing only; no optimisation or structural reanalysis started.'
    save(PART/'manufacturing.json',metadata)
    placement = json.loads((ASSEMBLY/'placement.json').read_text(encoding='utf-8'))
    interface = json.loads((CASE/'interface.json').read_text(encoding='utf-8'))
    from child_clamp_placement import candidate_placement
    placement, bolt_length = candidate_placement(placement, interface, geometry)
    placement['note'] = 'Three connected M3 clamp bands, two identical optimised cage halves, two 10.5mm rope eyes on the four-hole mounting-face side at the upper axial end. 1mm rubber, provisional compressed 0.8mm. Existing WTE4 114.3mm OD x200mm, band centres40/100/160. Four-hole pads retained but are not supports in lifting analysis. X90 print rotation, Y build axis. Independent strength and physical wet/creep/print trials required.'
    save(ASSEMBLY/'placement.json',placement)
    config = dict(status='exploration_only',
        note='**形状・造形検討用。吊り上げ使用の強度認定は未完了。** 3段を連結した同じ半割りケージ2個。Bambu PETG Basic V3.0、100%インフィル、外周8、上下8層、0.20mm、0.4mmノズル。印刷STLはX90°回転済みで、そのまま読み込む。5mm外ブリム、ベッド面からのサポートのみ。穴の局所サポートは除去可能なことを確認。ゴムは購入した1mmシート6枚、圧縮0.8mmは仮定。M3x60ボルト12本、ナット12、OD12ワッシャ24。4穴面側の上端にØ10.5ロープ穴2個。湿潤滑り・クリープ・実物造形試験は未認定。',
        notes=['parts/child/exterior/printed/child_wte4_suspension_clamp/CAGE_TOPOLOGY.md',
            'parts/child/exterior/printed/child_wte4_suspension_clamp/BAMBU_PETG_BASIC.md'])
    config['note']=config['note'].replace('M3x60',f'M3x{bolt_length}')
    final_fea_file = CASE/'fea/finished_cage_fea.json'
    if void_free and not final_fea_file.exists():
        config['note'] += ' 2026-10-02: 材料内部の密閉空洞は0個。再最適化せず中実化。変更後の構造再解析は未実施。前回形状の偏荷重変位1.079mm超過・独立メッシュ停止は履歴で、新形状へ数値を転用しない。'
        config['notes'].append('parts/child/exterior/printed/child_wte4_suspension_clamp/OPTIMIZATION_INPUTS.md')
    if final_fea_file.exists():
        final_fea = json.loads(final_fea_file.read_text(encoding='utf-8'))
        failures = [r for r in final_fea['cases'] if any(check['name']=='stiffness' and not check['pass'] for check in r['checks'])]
        if failures:
            config['note'] += (' 完成STL再解析の剛性未達: '+', '.join(
                f'{r["case"]} 変位{r["max_displacement_mm"]:.3f}mm（基準1mm）' for r in failures)+
                '。吊り上げ使用前にこの未達を解消する。独立解析と収束の判定は設計元の最新検証記録を参照。')
    for note in ['EPDM_ADJUSTMENT.md','LIGHTWEIGHT_REVIEW.md']:
        config['notes'].append((PART/ note).relative_to(ROOT).as_posix())
    save(ASSEMBLY/'print_config.json',config)
    if not args.geometry_only:
        job_dir = ASSEMBLY/'print_jobs'
        job_dir.mkdir(exist_ok=True)
        job_file = job_dir/'cage_x1c_petg100.3mf'
        shutil.copy2(Path(sliced['project_3mf']),job_file)
        save(job_dir/'cage_x1c_petg100.json',dict(
            status='exploration_only', project=job_file.name,
            project_sha256=hashlib.sha256(job_file.read_bytes()).hexdigest(),
            source_stl='parts/child_wte4_suspension_clamp_cage.stl',
            source_design_stl_sha256=geometry['sha256'],
            sliced_print_stl_sha256=sliced['part_sha256'],
            printer=sliced['printer_name'], material=sliced['filament_preset'],
            layer_mm=sliced['layer_mm'], supports=sliced['support_type'],
            process_overrides=sliced['process_overrides'],
            nozzle_celsius=255,bed_celsius=70,
            quantity_per_plate=1, required_plates=2,
            validation_case=CASE.relative_to(ROOT).as_posix(),
            note='Actual Bambu Studio sliced project, one identical half per plate. Geometry/printing checks do not qualify lifting strength. Keep X90 source orientation; inspect removable supports and internal bridges in a physical print.'))
        (job_dir/'README.md').write_text('''# X1 Carbon用のスライス確認済みプロジェクト

印刷条件と数量の入口は [../parts/PRINT.md](../parts/PRINT.md)。`cage_x1c_petg100.3mf` は実STLをBambu Studio CLIでスライスした1個/プレートのプロジェクトです。同一半割りを合計2個造形します。STLのハッシュ・材料・設定・解析元は同名JSONへ記録しています。

**exploration_only: 吊り上げ使用の強度認定は未完了。** 100%インフィル、外周8、上下8層、0.20 mm、Bambu PETG Basic、255°C/70°C、5 mm外ブリム、ベッド面からのサポートです。印刷姿勢を保ち、内部ブリッジ・吊り穴のサポート除去を実物で確認します。スライス成功は実機での印刷成功を意味しません。
''',encoding='utf-8')
    print('Staged canonical cage surface, generated STL and existing assembly placement; strength status remains exploration_only.')


if __name__ == '__main__':
    main()
