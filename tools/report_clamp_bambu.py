"""Summarise native Bambu clamp runs without reimplementing a solver or judge."""
from pathlib import Path
import hashlib
import json
import trimesh
from topopt.ccx import mesh_convergence

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=PART/'_work/analysis/bambu_petg_basic_v3'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    opt=read(CASE/'opt/study_stress_smooth.json')
    old=read(PART/'_work/analysis/stress_smooth_r85_v065/opt/study_stress_smooth.json')
    study=read(CASE/'study_final.json')
    topology=read(CASE/'study_stress_smooth.json')
    provenance=read(CASE/'final_provenance.json')
    geometry=read(CASE/'geometry_checks.json')
    printing=read(CASE/'print_checks.json') if (CASE/'print_checks.json').exists() else {}
    step=read(CASE/'step_checks.json') if (CASE/'step_checks.json').exists() else {}
    ccx=read(CASE/'ccx/ccx_summary.json') if (CASE/'ccx/ccx_summary.json').exists() else {}
    runs=ccx.get('runs',[])
    latest=runs[-1] if runs else {}
    card=read(PART/'spec/bambu_petg_basic_material.json')
    conditions_equal=all(study[k]==topology[k] for k in provenance['same_condition_keys'])
    finished=Path(study['part'])
    input_matches=sha(finished)==study['_part_sha256']==provenance['final_part_sha256']
    ccx_manifest=read(CASE/'ccx/manifest.json') if (CASE/'ccx/manifest.json').exists() else {}
    inputs={str(Path(i['path']).resolve()):i['sha256'] for i in ccx_manifest.get('inputs',[])}
    ccx_matches=all(inputs.get(str(p.resolve()))==sha(p) for p in [finished,CASE/'study_final.json'])
    convergence={}
    for case in latest.get('cases',[]):
        series=[]
        for run in runs:
            row=next((r for r in run.get('cases',[]) if r['case']==case['case']),{})
            if row.get('max_disp_mm') is not None:
                series.append(dict(target_mm=run['mesh_target_mm'],nodes=run['nodes'],
                    max_disp_mm=row['max_disp_mm'],p99_5_stress_MPa=row['von_mises_p99_5_MPa'],
                    max_stress_MPa=row['von_mises_max_MPa'],
                    hotspot_xyz_mm=(row.get('hotspot') or {}).get('xyz_mm')))
        convergence[case['case']]=mesh_convergence(series)
    volume_checks=[dict(target_mm=r['mesh_target_mm'],relative_error=abs(r['mass_properties']['volume_mm3']/geometry['volume_mm3']-1),
        pass_check=abs(r['mass_properties']['volume_mm3']/geometry['volume_mm3']-1)<0.005) for r in runs if r.get('mass_properties')]
    baseline=trimesh.load(PART/'child_wte4_suspension_clamp_half.stl',force='mesh')
    previous_volume=read(PART/'_work/analysis/stress_smooth_r85_v065/geometry_checks.json')['volume_mm3']
    required={c['name']:1.5 if c.get('load_class')=='abnormal' else study['safety_factor'] for c in study['cases']}
    strict={c['case']:c.get('worst_element_safety_factor',0)>=required[c['case']] for c in latest.get('cases',[])}
    # A single independent mesh cannot establish convergence. Native convergence
    # remains the judge; the three-run completeness guard prevents partial release.
    passed=bool(conditions_equal and input_matches and ccx_matches and geometry['pass'] and opt['pass'] and step.get('pass_check') and
        len(runs)>=3 and len(latest.get('cases',[]))==8 and all(r.get('pass') for r in runs) and
        all(v['pass_check'] for v in volume_checks) and all(strict.values()) and
        all(c['pass'] for c in convergence.values()))
    summary=dict(pass_check=passed,exploration_only=not passed,conditions_equal=conditions_equal,
        final_input_hash_matches=input_matches,ccx_input_hash_matches=ccx_matches,
        material_card_sha256=sha(PART/'spec/bambu_petg_basic_material.json'),
        material=card,native_topology=opt,native_ccx=ccx,native_convergence=convergence,
        strict_local_safety_factor_pass=strict,mesh_volume_checks=volume_checks,geometry=geometry,printing=printing,step=step,
        prior_generic_final_volume_mm3=previous_volume,
        volume_change_from_generic_percent=100*(geometry['volume_mm3']/previous_volume-1),
        reduction_from_solid_percent=100*(1-geometry['volume_mm3']/baseline.volume))
    (CASE/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    source=card['orthotropic']['source']
    lines=['# Bambu Lab PETG Basicでの再最適化', '',
        '**exploration_only: 直接平滑化した形状試作。吊り下げ用途の強度は未合格。**', '',
        '## 材料の根拠', '',
        f'[メーカーTDS V3.0]({source})（原本: `ref/Bambu_PETG_Basic_TDS_V3.0.pdf`）。ユーザー提示の曲げ75/56 MPa、衝撃34.2 kJ/m²と一致するアップグレード品。旧配合PETG BasicやPETG HFのTDSは使わない。', '',
        '| 特性 | メーカー掲載値 | 今回の入力 | 前回の汎用PETG |',
        '|---|---|---|---|',
        '| ヤング率XY MPa | 2780 ±65 | Ex=Ey=2715 | Ex=2100, Ey=1750 |',
        '| ヤング率Z MPa | 2550 ±100 | 2450 | 1150 |',
        '| 引張強度XY MPa | 51 ±1 | Xt=50, Yt=33暫定 | Xt=42, Yt=33 |',
        '| 引張強度Z MPa | 35 ±6 | 29 | 25 |',
        '| 曲げ強度XY/Z MPa | 75 ±3 / 56 ±4 | 引張・圧縮強度へ転用しない | — |',
        '| 衝撃強度XY kJ/m² | 34.2 ±4.1 | 静荷重・2g荷重へ転用しない | — |',
        '| 密度 g/cm³ | 1.25 | 1.25 | 1.27 |', '',
        '平均から掲載±幅を引いた値は暫定的な下側入力であり、統計的な設計許容値ではない。XYヤング率を両層内軸へ適用する仮定。ラスタ直交の引張強度Yt=33、圧縮Xc/Yc/Zc=50/42/35 MPa、せん断Sxy/Syz/Szx=20/14/14 MPa、せん断弾性率700/420/420 MPa、ポアソン比0.38/0.34/0.34は従来の暫定値を維持。未掲載値を曲げ強度から推算して強化しない。メーカー試験はX1-Carbon、255°C、ベッド70°C、150 mm/s、100%インフィル。実機・湿潤・クリープ・ゴム接触は未同定。', '',
        '材料カードの正本は `spec/bambu_petg_basic_material.json`。`tools/clamp_bambu_material.py` が別名カードを実行プロセスへ登録してnative topoptを呼ぶ。汎用PETGとインストール済みソルバは変更しない。', '',
        '## 同じ荷重での比較', '',
        '4 kg完成機を3クランプで支持し、1組が50%を負担。静荷重19.6133 N、取扱い2g 39.2266 N、締付け150 N/M3×4本。底側支持の軽減なし。通常SF3、異常SF1.5、変位上限1 mm。積層Z・ラスタX、8外周・100%インフィル。前回と同じ8ケース、拘束・荷重領域・格子・体積率。', '',
        f'最適化と独立解析の条件一致: {conditions_equal}。完成形状SHA一致: {input_matches}。独立解析入力SHA一致: {ccx_matches}。局所応力はMMAの応力制約へ全要素角点・中心評価を含め、独立解析のみ追加したケースや応力除外はない。p-norm=8、密度緩和q=0.5。', '',
        '| ケース | 前回最適化変位 mm | 今回最適化変位 mm | 今回最悪局所SF | native判定 |',
        '|---|---:|---:|---:|---|']
    previous={r['case']:r for r in old['final_fea']}
    for r in opt['final_fea']:
        lines.append(f'| {r["case"]} | {previous[r["case"]]["max_displacement_mm"]:.4f} | {r["max_displacement_mm"]:.4f} | {r["min_safety_factor"]:.3f} | {"PASS" if r["pass"] else "FAIL"} |')
    lines += ['', '両列はそれぞれの最適化形状の比較。同一形状だけの材料感度解析ではない。最適化格子の応力合格は完成STLの強度保証ではない。', '',
        f'1 mm格子、原点[-97.35,-87.35,-2]、195×89×36、体積率0.65、フィルタ4 mm、100反復上限。終了理由 `{opt["termination_reason"]}`。最大反復到達を完全収束とは呼ばない。', '',
        '## 直接平滑化した部品', '',
        f'抽出しきい値{provenance["chosen_level"]:g}、native密度場を0.75 mm平滑化し1 mmで面出力。M3穴・座面・ゴム面のみ元CADで復元。単純リブへの再構成、メッシュの削減、空洞の材料埋めはしない。体積{geometry["volume_mm3"]/1000:.2f} cm³、半体{geometry["PETG_solid_mass_g_per_half"]:.1f} g、6個{geometry["PETG_solid_mass_g_six_halves"]/1000:.3f} kg。厚肉初期形状から{summary["reduction_from_solid_percent"]:.1f}%削減、前回平滑化形状との体積差{summary["volume_change_from_generic_percent"]:+.2f}%。', '',
        f'閉メッシュ・実穴・工具・ゴム取合い検査: {geometry["pass"]}。M3締付け4本と固定4本/組を維持。ゴム1.5 mmは圧縮後1.2 mmの仮定、内径116.7 mm、実半径余裕{geometry["tube_plastic_radial_clearance_mm"]:.4f} mm。圧縮量は材質・硬度未定のため実物で確認する。', '',
        '![実STLの断面](_work/images/bambu_topology_comparison.png)', '',
        '## 完成形状の独立解析', '',
        '| ケース | 最大変位 mm | SF p99.5 | 最悪局所SF | native判定 |',
        '|---|---:|---:|---:|---|']
    for r in latest.get('cases',[]):
        if r.get('max_disp_mm') is None:
            lines.append(f'| {r["case"]} | 未完了 | 未完了 | 未完了 | FAIL |')
        else:
            lines.append(f'| {r["case"]} | {r["max_disp_mm"]:.4f} | {r["safety_factor_p99_5"]:.3f} | {r["worst_element_safety_factor"]:.3f} | {"PASS" if r["pass"] else "FAIL"} |')
    if not latest.get('cases'):
        lines += ['', '**独立解析は四面体メッシュ生成で停止。完成形状の応力・変位は未評価。最適化側の合格を完成品へ代用しない。** 最終試行は `ccx_hxt_single.log` / `ccx_hxt_single.err`。入力ハッシュの一致は確認したが、四面体品質・体積・メッシュ収束を検査できたという意味ではない。']
    lines += ['', '| メッシュ mm | 要素数 | 品質 | STL体積一致 |', '|---|---:|---|---|']
    for r,v in zip(runs,volume_checks):
        lines.append(f'| {r["mesh_target_mm"]:g} | {r["elements"]} | {"PASS" if r.get("mesh_quality",{}).get("pass") else "FAIL"} | {"PASS" if v["pass_check"] else "FAIL"} |')
    lines += ['', 'native Gmsh/CalculiX、表面荷重、標準表面細分化あり。負体積の閉境界を内部空洞として渡し、四面体体積をSTLと照合。局所応力は除外しない。メッシュ品質が不合格なら局所ピークを実物の破断安全率と解釈しない。3段階収束を満たさない計算を最終強度値として採用しない。今回の数値・判定・ハッシュは `_work/analysis/bambu_petg_basic_v3/verification_summary.json` に保持する。', '',
        '最初のHXT（4スレッド）はヒープ破損で停止（終了値3221226356）。`ccx_hxt_crash` に保持する。同じSTL境界・内側空洞でDelaunay（1スレッド）を試し、300万回以上の点挿入/削除が反復したため打切り（`ccx_delaunay_stalled`）。最終HXT（1スレッド）もメッシュ生成で停止。形状の穴埋めや応力除外による回避はしない。今回は完成形状の応力・変位を取得できていない。', '',
        f'STEP/STL読み戻し一致: {step.get("pass_check",False)}。造形検査は `_work/analysis/bambu_petg_basic_v3/print_checks.json` を参照。平置きの造形枠・最小肉厚は合格、支持なし造形は不合格（過張出し約16.8%）。軸方向の吊り荷重は積層方向Zと一致するため、nativeの荷重対積層方向の造形判定も不合格。異方性FEAへこの向きを明示しているが、層間強度の実物試験と内部空洞のブリッジ確認が必要。', '',
        '## 再実行', '', '```powershell', '$env:PYTHONIOENCODING="utf-8"',
        'python tools/clamp_bambu_material.py setup <case>/study_stress_smooth.json --out <case>/setup --voxel 1 --iters 100',
        'python tools/clamp_bambu_material.py opt <case>/study_stress_smooth.json --out <case>/opt --voxel 1 --iters 100',
        'python tools/finish_child_clamp_smooth.py --case <case> --candidate-only',
        'python tools/verify_child_clamp.py --stl <case>/finished_candidate.stl --out <case>/geometry_checks.json --density-g-cm3 1.25',
        '$env:TOPOPT_GMSH=(Join-Path (Get-Location).Path "tools/gmsh_clamp_delaunay.cmd")',
        '$env:TOPOPT_GMSH_ALGORITHM="10"; $env:TOPOPT_GMSH_THREADS="1"',
        '$env:OMP_NUM_THREADS="4"; $env:CCX_NPROC_EQUATION_SOLVER="4"',
        'python tools/clamp_bambu_material.py ccx <case>/finished_candidate.stl --study <case>/study_final.json --out <case>/ccx --mesh-mm 5 --map surface',
        'python tools/report_clamp_bambu.py', '```', '',
        '`<case>` は設計元の `_work/analysis/bambu_petg_basic_v3`。支持なし造形・内部空洞ブリッジ・実物保持/滑り/長期クリープも別途確認する。前回汎用材料の解析は `stress_smooth_r85_v065` に履歴として保持する。']
    (PART/'BAMBU_PETG_BASIC.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['pass_check','reduction_from_solid_percent','volume_change_from_generic_percent']}))


if __name__=='__main__':
    main()
