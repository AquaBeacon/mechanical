"""Report direct density smoothing and native independent verification results."""
from pathlib import Path
import json
import trimesh
import hashlib
from topopt.ccx import mesh_convergence

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE = PART/'_work/analysis/stress_smooth_r85_v065'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    opt = read(CASE/'opt/study_stress_smooth.json')
    study = read(CASE/'study_final.json')
    provenance = read(CASE/'final_provenance.json')
    geometry = read(CASE/'geometry_checks.json')
    step=read(CASE/'step_checks.json')
    printing=read(CASE/'print_checks.json')
    cleanup=read(CASE/'exact_interface_degeneracy_cleanup.json')
    ccx_path=CASE/'ccx/ccx_summary.json'
    ccx = read(ccx_path) if ccx_path.exists() else dict(runs=[],pass_check=False,error='Independent mesh generation did not complete; see ccx/run.err')
    manifest_path=CASE/'ccx/manifest.json'
    ccx_manifest=read(manifest_path) if manifest_path.exists() else {}
    final_part=PART/'child_wte4_suspension_clamp_smooth.stl'
    current_inputs={str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in [final_part,CASE/'study_final.json']}
    ccx_inputs={str(Path(i['path']).resolve()):i['sha256'] for i in ccx_manifest.get('inputs',[])}
    input_hashes_match=all(ccx_inputs.get(p)==h for p,h in current_inputs.items())
    topology_study=read(CASE/'study_stress_smooth.json')
    shared_conditions_match=all(study[k]==topology_study[k] for k in provenance['same_condition_keys'])
    final_hash_matches=study['_part_sha256']==current_inputs[str(final_part.resolve())]==provenance['final_part_sha256']
    runs = ccx.get('runs', [])
    latest = runs[-1] if runs else {}
    convergence = {}
    requirements = {c['name']: (1.5 if c.get('load_class') == 'abnormal' else study['safety_factor'])
                    for c in study['cases']}
    for case in latest.get('cases', []):
        series = []
        for run in runs:
            row = next(c for c in run['cases'] if c['case'] == case['case'])
            series.append(dict(target_mm=run['mesh_target_mm'], nodes=run['nodes'],
                               max_disp_mm=row.get('max_disp_mm'),
                               p99_5_stress_MPa=row.get('von_mises_p99_5_MPa'),
                               max_stress_MPa=row.get('von_mises_max_MPa'),
                               hotspot_xyz_mm=(row.get('hotspot') or {}).get('xyz_mm')))
        convergence[case['case']] = mesh_convergence(series)
    strict_local = {c['case']: c.get('worst_element_safety_factor', 0) >= requirements[c['case']]
                    for c in latest.get('cases', [])}
    mesh_volume_checks=[]
    for run in runs:
        volume=(run.get('mass_properties') or {}).get('volume_mm3')
        error=abs(volume/geometry['volume_mm3']-1) if volume is not None else None
        mesh_volume_checks.append(dict(mesh_mm=run['mesh_target_mm'],volume_mm3=volume,
                                       relative_error=error,pass_check=error is not None and error<0.005))
    complete = len(latest.get('cases', [])) == len(study['cases'])
    stress=opt.get('stress_constraint') or {}
    optimisation_stress_ok=bool(stress.get('enabled') and stress.get('satisfied') and
                                stress.get('samples')=='all' and stress.get('optimizer')=='mma')
    passed = bool(complete and geometry['pass'] and step['pass_check'] and provenance['all_equal'] and
                  shared_conditions_match and final_hash_matches and input_hashes_match and
                  optimisation_stress_ok and
                  all(r.get('pass') for r in runs) and
                  all(c['pass'] for c in convergence.values()) and all(strict_local.values()) and
                  all(v['pass_check'] for v in mesh_volume_checks))
    baseline = trimesh.load(PART/'child_wte4_suspension_clamp_half.stl', force='mesh')
    reduction = 100*(1-geometry['volume_mm3']/baseline.volume)
    verdict = dict(pass_check=passed, exploration_only=not passed, final_provenance=provenance,
                   topology_termination=opt['termination_reason'],native_optimisation_stress=stress,
                   native_ccx=ccx,
                   case_convergence=convergence, strict_local_safety_factor_pass=strict_local,
                   geometry=geometry,step=step,printing=printing,degeneracy_cleanup=cleanup,mesh_volume_checks=mesh_volume_checks,
                   current_shared_conditions_match=shared_conditions_match,
                   final_hash_matches=final_hash_matches,ccx_input_hashes_match=input_hashes_match,
                   baseline_volume_mm3=float(baseline.volume),
                   reduction_percent=float(reduction))
    (CASE/'verification_summary.json').write_text(json.dumps(verdict,indent=2)+'\n',encoding='utf-8')
    lines = ['# 密度分布を直接平滑化したPETGクランプ', '',
             '**状態: '+('解析合格・実機保持試験待ち' if passed else 'exploration_only: 平滑化部品の形状・造形試作。吊り下げ用途は未合格')+'。**', '',
             '設計元の `model="smooth"` は最適化した密度場の等値面を直接取り込み、M3穴・座面・ゴム内面だけを元のCAD寸法で仕上げる。単純な円弧リブへの置換は行わない。前回の `topology_candidate` と TOPOLOGY.md は不採用の探索履歴。', '',
             '## 荷重と応力の一致', '',
             '4 kgの完成機、クランプ3組、最大1組に50%が掛かる仮定。静荷重19.6133 N/組、取扱い2gで39.2266 N/組。下側支持による軽減は計算へ入れない。締付けM3は4本/組、予張力150 N/本の仮定（推定トルク0.09 N·m、K=0.2）。フレーム固定は4穴（2本×2列、36×16 mm仮ピッチ）。', '',
             '最適化と独立解析で全8ケース、荷重領域・力・固定自由度・PETGカード・材料軸・安全率・変位上限を同じJSON条件から生成し、一致を検査した。局所応力は外力として追加せず、最適化の応力制約に全要素の角点と中心の応力評価を使用する。最適化はMMA、p-norm=8、密度緩和q=0.5。独立解析は完成した平滑化STLの二次四面体によるCalculiX。応力の除外は行わない。', '',
             '通常安全率3、異常安全率1.5、最大変位1 mm。native CLIのp99.5と最悪要素SF下限1.5の判定に加え、ここでは通常ケースの最悪局所SFも3以上を確認する。密度緩和したp-normと完成形状の局所ピークは同じ数値指標ではないため、最適化制約内だけで完成品を合格としない。ボクセルの節点荷重と独立解析の表面荷重には離散化の違いが残る。', '',
             'PETGは暫定異方性材料カード、100%インフィル、8外周、積層Z・ラスタX。フィラメント個別の強度、濡れ、ゴム接触非線形、ねじ弾性、長期クリープは未同定。', '',
             '## 最適化側の全局所応力評価', '',
             '| ケース | 最悪局所SF | 最大変位 mm | 判定 |',
             '|---|---:|---:|---|']
    for row in opt['final_fea']:
        lines.append(f'| {row["case"]} | {row["min_safety_factor"]:.3f} | {row["max_displacement_mm"]:.4f} | {"PASS" if row["pass"] else "FAIL"} |')
    lines += ['', '上表は最適化格子の結果で、完成STLの独立検証結果ではない。', '',
             '## 最適化と平滑化', '',
             f'1 mm格子、自由領域体積率0.65、フィルタ4 mm、100反復上限。終了理由は `{opt["termination_reason"]}`。最大反復到達を完全収束とは呼ばない。穴周り・内面はpreserve領域。上下16 mmピッチで接する座は半径8.5 mmとして厚さゼロの接続を防ぎ、この変更も最適化側へ含めた。抽出しきい値0.4/0.5/0.6を比較し、native判定で{provenance["chosen_level"]:g}を選択した（`{provenance["chosen_reason"]}`）。密度場を0.75 mm平滑化し、1 mm間隔で面を出力してCAD側で正確な取合いを復元する。', '',
             f'平滑化半体の体積{geometry["volume_mm3"]/1000:.2f} cm³、PETG約{geometry["PETG_solid_mass_g_per_half"]:.1f} g/半体、6個で約{geometry["PETG_solid_mass_g_six_halves"]/1000:.3f} kg。厚肉設計との体積差は{reduction:.1f}%軽量化。金属・ゴム・サポート別。', '',
             f'完成形状は閉じた境界面{geometry["closed_boundary_shells"]}個を持つ1つの立体として検査した。内部空洞の合計体積は{geometry["internal_cavity_volume_mm3"]/1000:.2f} cm³。境界面数を部品数と混同しない。', '',
             '![実STLの中央断面と厚肉設計の比較](_work/images/smooth_topology_comparison.png)', '',
             f'CAD出力の面積ゼロ三角形{cleanup["zero_area_before"]}枚をMeshLabのEdge Flipで張り直した。三角形数{cleanup["triangles_after"]}枚は維持し、頂点の削減・穴埋め・リブ置換は行わない。体積差{cleanup["volume_delta_mm3"]:.9f} mm³、外形差{cleanup["bounds_delta_mm"]:.9f} mm、双方向の頂点/面中心による表面差{cleanup["bidirectional_sampled_surface_delta_mm"]:.7f} mm。STEPを読み戻して1立体・5境界面・内部空洞の維持とSTL体積/外形の一致を確認した。', '',
             '## ゴムと取合い', '',
             f'ユーザー指定の1.5 mmシートを圧縮後1.2 mmと仮定。容器外径114.3 mm、PETG内径116.7 mm、実メッシュの片側余裕{geometry["tube_plastic_radial_clearance_mm"]:.4f} mm、割り面1.6 mm。片側数mmの余裕ではない。ゴムの材質・硬度と実外径を確認し、厚いシートへ変更する場合は内径を変える。', '',
             'BlueRobotics公式BR-102678-004 RevCの主内径117.48 mm（半径58.74 mm）、容器との片側余裕1.59 mmを参考測定した。[メーカーのクランプ・CAD](https://bluerobotics.com/store/watertight-enclosures/enclosure-clamp/)。アルミ製品の強度はPETGへ転用しない。', '',
             '## 完成形状の独立解析', '',
             '| ケース | 要求SF | SF p99.5 | 最悪局所SF | 変位 mm | CLI判定 | 局所SF | 収束 |',
             '|---|---:|---:|---:|---:|---|---|---|']
    for c in latest.get('cases', []):
        if c.get('max_disp_mm') is None:
            lines.append(f'| {c["case"]} | {requirements[c["case"]]:g} | 未完了 | 未完了 | 未完了 | FAIL | FAIL | FAIL |')
            continue
        lines.append(f'| {c["case"]} | {requirements[c["case"]]:g} | {c["safety_factor_p99_5"]:.2f} | {c["worst_element_safety_factor"]:.3f} | {c["max_disp_mm"]:.4f} | {"PASS" if c["pass"] else "FAIL"} | {"PASS" if strict_local[c["case"]] else "FAIL"} | {"PASS" if convergence[c["case"]]["pass"] else "FAIL"} |')
    if not latest.get('cases'):
        lines += ['', '独立解析は四面体メッシュ生成で停止しているため、完成形状の局所応力・安全率・変位は未評価。最適化側の合格を完成品の強度保証へ代用しない。']
    lines += ['', '| メッシュ mm | 要素数 | STLとの体積差 | メッシュ品質 |',
              '|---:|---:|---:|---|']
    for run,check in zip(runs,mesh_volume_checks):
        error=f'{check["relative_error"]*100:.6f}%' if check['relative_error'] is not None else '未評価'
        lines.append(f'| {run["mesh_target_mm"]:g} | {run.get("elements","未評価")} | {error} | {"PASS" if (run.get("mesh_quality") or {}).get("pass") else "FAIL"} |')
    lines += ['', '各ケースのメッシュ収束は既存 `topopt.ccx.mesh_convergence` で判定。未収束の応力値を最終強度値として扱わない。全ケースが揃っていなければ合格にしない。メッシュ品質FAILの場合、表の局所ピークは数値的に信頼できず、実物の破断安全率とは解釈しない。応力を除外せず、解析が未合格であると記録する。', '',
              '初回の単一STL境界面によるGmsh入力は内部空洞を材料で埋め、四面体体積154939.56 mm³（完成STL135355.70 mm³）になったため全結果を不採用とした。記録は `ccx/cavity_import_failure/` に保持する。現在のアダプタは原メッシュの閉境界面を分け、GmshのSurface Loopを外側1面＋内部空洞4面として1つのVolumeへ渡す。解析アルゴリズム・材料・荷重を自作せず、native Gmsh/CalculiXを使用する。STLと各四面体メッシュの体積差0.5%以内も合格の必須条件。', '',
              '出所と同一条件の検査: `_work/analysis/stress_smooth_r85_v065/final_provenance.json`。局所評価と収束: `verification_summary.json`。最適化生密度・各閾値・平滑化前後のSTLは同じ解析フォルダに保持する。半径8 mm・体積率0.55の先行試行は `stress_smooth` に保持する。座の零厚接続と横方向変位1.058 mmのため不採用。', '',
              '## 造形と再生成', '',
              '積層Zで平置き。native造形検査は造形枠・最小肉厚PASS、支持なし造形FAIL（過張出し17.1%、最小断面p1=2.74 mm）。最適化時のオーバーハング制約は無効。内側工具穴の除去できるサポートと、密閉空洞に除去不能なサポートを生成しない設定を実際のスライスで確認し、空洞上のブリッジを試験する。ゴム・ねじは印刷しない。STEPは平滑化STLのファセット表現で、解析的な滑らかな曲面CADではない。', '',
              '```powershell', '$env:PYTHONIOENCODING="utf-8"',
              'python tools/prepare_child_clamp_smooth.py',
              'python -m topopt setup <case>/study_stress_smooth.json --out <case>/setup --voxel 1 --iters 100',
              'python -m topopt opt <case>/study_stress_smooth.json --out <case>/opt --voxel 1 --iters 100',
              'python tools/finish_child_clamp_smooth.py',
              'python tools/verify_child_clamp.py --stl <part>/child_wte4_suspension_clamp_smooth.stl --out <case>/geometry_checks.json',
              '$env:TOPOPT_GMSH=(Join-Path (Get-Location).Path "tools/gmsh_clamp_delaunay.cmd")',
              '$env:OMP_NUM_THREADS="4"; $env:CCX_NPROC_EQUATION_SOLVER="4"',
              'python -m topopt ccx <part>/child_wte4_suspension_clamp_smooth.stl --study <case>/study_final.json --out <case>/ccx --mesh-mm 5 --map surface --converge',
              'python tools/report_child_clamp_smooth.py', '```', '',
              '`<part>` はこの部品の設計元フォルダ、`<case>` はその `_work/analysis/stress_smooth_r85_v065`。計算による断面強度と、ゴムの滑り・長期保持は別途評価が必要。']
    (PART/'SMOOTH_TOPOLOGY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(dict(pass_check=passed, reduction_percent=reduction, report=str(PART/'SMOOTH_TOPOLOGY.md'))))


if __name__ == '__main__':
    main()
