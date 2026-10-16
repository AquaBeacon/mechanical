"""Write a topology-candidate report using native solver verdicts/mesh judge."""
from pathlib import Path
import hashlib
import json
import trimesh
from topopt.ccx import mesh_convergence

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE = PART / '_work/analysis/topology_petg'


def main():
    geometry = json.loads((CASE / 'geometry_checks.json').read_text(encoding='utf-8'))
    native = json.loads((CASE / 'candidate_ccx_convergence/ccx_summary.json').read_text(encoding='utf-8'))
    runs = native['runs']
    latest = runs[-1]
    convergence = {}
    for case in latest['cases']:
        series = []
        for run in runs:
            row = next(c for c in run['cases'] if c['case'] == case['case'])
            series.append(dict(target_mm=run['mesh_target_mm'], nodes=run['nodes'],
                               max_disp_mm=row.get('max_disp_mm'),
                               p99_5_stress_MPa=row.get('von_mises_p99_5_MPa'),
                               max_stress_MPa=row.get('von_mises_max_MPa'),
                               hotspot_xyz_mm=(row.get('hotspot') or {}).get('xyz_mm')))
        convergence[case['case']] = mesh_convergence(series)
    passed = geometry['pass'] and all(r.get('pass') for r in runs) and all(c['pass'] for c in convergence.values())
    baseline = trimesh.load(PART / 'child_wte4_suspension_clamp_half.stl', force='mesh')
    reduction = 100*(1-geometry['volume_mm3']/baseline.volume)
    result = dict(pass_check=bool(passed), exploration_only=not passed,
                  candidate_sha256=hashlib.sha256((CASE/'candidate.stl').read_bytes()).hexdigest(),
                  baseline_volume_mm3=float(baseline.volume), reduction_percent=float(reduction),
                  geometry=geometry, native_solver=str(CASE/'candidate_ccx_convergence/ccx_summary.json'),
                  case_convergence=convergence)
    (CASE/'verification_summary.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    lines = ['# BlueRobotics参考・PETGクランプのトポロジー最適化', '',
             '**判定: '+('解析合格・実機保持試験待ち' if passed else '探索候補。吊り下げ用印刷部品として未合格')+'。**', '',
             '## 対象と荷重', '',
             '既存のWTE4用設計元SCADの `model="topology_candidate"`。半体6個で3組。締付けM3は4本/組、フレーム固定M3は後半体の4穴（2本×2列）を全て使用。穴ピッチ36×16 mmは既存の仮寸法を維持。', '',
             '機体総質量4 kg（クランプ・フレームも含む）、3組、最大1組へ50%の偏りを仮定。静荷重19.6133 N/組、取扱い2g相当39.2266 N/組。下からの支えによる軽減は0。締付けは仮の150 N/本、推定トルク0.09 N·m（K=0.2）。実ゴムの圧縮量から予張力を確定した値ではない。締付け＋静荷重、締付け＋軸/横2g、前半体から締付けねじへの経路を含む8ケースを再解析。通常安全率3、異常1.5、変位上限1 mm。', '',
             'PETG100%ソリッド、8外周、積層Z/ラスタX、既存の暫定異方性材料カード。濡れ・クリープ・フィラメント個別の強度は材料カードに含まれない。', '',
             '## ゴムの余裕', '',
             'ユーザー確認: シート未定、1.5 mmで検討。公式BR-102678-004 RevC STEPの主内面は解析的な半径58.74 mm、内径117.48 mm。公称114.3 mm容器に対して片側1.59 mm、直径差3.18 mmの空間を確認した。公式品はゴム付きアルミクランプであり、その材料強度をPETGへ転用していない。', '',
             '[公式製品・CAD](https://bluerobotics.com/store/watertight-enclosures/enclosure-clamp/)。測定記録: `_work/analysis/topology_petg/reference_cylinders.json`。', '',
             f'PETG候補内径116.7 mm、測定した片側空間{geometry["tube_plastic_radial_clearance_mm"]:.4f} mm。厚さ1.5 mmから圧縮後1.2 mmを仮定した取合い。割り面隙間1.6 mmを残す。ゴム厚・硬度と実容器外径の公差で圧縮が変わるため、最終の締付け状態は実物で確認する。片側数mmの空間ではなく片側1.2 mmであり、2–3 mm厚シートへ変更する場合は内径を再設計する。', '',
             '## 最適化とCADへの再構成', '',
             '4荷重ケースを同時にSIMP最適化、異方性PETG、80反復、実ボクセル2.048744 mm、フィルタ6 mm。M3座面/周囲とゴム接触面をpreserveに設定。設計領域の71%が自由、体積率0.35と0.55を比較。preserveが期待最終体積の54%を占めるため、形状全体を自由生成した結果ではない。M3穴は粗い格子で解像できず、最適化では有限幅の支持パッドを使い、独立解析では元の穴内壁拘束へ戻した。', '',
             '両最適化のtermination_reasonはmax_iterations。最適化の完全収束とは呼ばない。0.35案は剛性不足、0.55案も最終FEAで解像度/横荷重変位が未合格。生STLは荷重経路の参考であり印刷一式に含めない。', '',
             'CAD候補は内外6 mmの円弧を4つのリブで結び、22度幅の貫通ポケットを4箇所に設ける。閉じた空洞の案は水/空気・サポートが閉じ込められるため採用しない。同じグリッドで0.55案と比較し、コンプライアンス差は通常/軸/横荷重で+7〜10%、前半体で-6%。この比較は荷重経路の保持の確認であり強度合格ではない。', '',
             f'候補は閉メッシュ1ボディ、体積{geometry["volume_mm3"]/1000:.2f} cm³/半体、PETG約{geometry["PETG_solid_mass_g_per_half"]:.1f} g/半体、3組約{geometry["PETG_solid_mass_g_six_halves"]/1000:.3f} kg。初期案に対して**{reduction:.1f}%軽量化**（金属・ゴム・サポート別）。外形190.7×84.55×32 mmとM3穴は維持。M3軸、外径9ワッシャ、外径8工具の全通路と屋根残肉3.28 mmを確認済み。', '',
             '![候補と初期案の比較](_work/images/topology_candidate_comparison.png)', '',
             '## 独立解析', '',
             'Gmsh二次四面体＋CalculiX。直接STLの5 mm試行はsliver要素が107個生じてFAIL。FreeCAD removeSplitter＋Gmshで表面を作り直し、元形状との最大差0.000004 mm未満、体積差0.000004%未満を確認した。形状・荷重を変えず10/5/2.5 mmで再解析。固定節点近傍を含め応力は除外なし。', '',
             '| ケース | SF p99.5 | 最悪SF | 最大変位 mm | ケース判定 | メッシュ収束 |',
             '|---|---:|---:|---:|---|---|']
    for c in latest['cases']:
        lines.append(f'| {c["case"]} | {c["safety_factor_p99_5"]:.2f} | {c["worst_element_safety_factor"]:.3f} | {c["max_disp_mm"]:.4f} | {"PASS" if c["pass"] else "FAIL"} | {"PASS" if convergence[c["case"]]["pass"] else "FAIL"} |')
    lines += ['', '| メッシュ mm | 節点 | 要素 | メッシュ品質 |', '|---:|---:|---:|---|']
    for run in runs:
        lines.append(f'| {run["mesh_target_mm"]:g} | {run["nodes"]} | {run["elements"]} | {"PASS" if run["mesh_quality"]["pass"] else "FAIL"} |')
    supplement = CASE/'candidate_ccx_netgen/ccx_summary.json'
    if supplement.exists():
        extra = json.loads(supplement.read_text(encoding='utf-8'))
        lines += ['', '### 最細メッシュの追加確認', '',
                  '形状・材料・荷重・固定条件は維持し、Gmsh標準のNetgen要素改善と閾値0.3を明示して2.5 mmを再実行した。元のCLIもNetgenと同じ既定閾値を使っていたため、メッシュ・数値は変わらず、局所応力/収束の問題は解消しなかった。追加アダプタ設定は撤去し、標準設定へ戻した。上表の3段階の系列は元の結果を保持する。単独の追加解析は収束系列の代用ではない。', '',
                  '| ケース | SF p99.5 | 最悪SF | 最大変位 mm | 判定 |', '|---|---:|---:|---:|---|']
        for row in extra['runs'][-1].get('cases', []):
            if row.get('max_disp_mm') is None:
                lines.append(f'| {row["case"]} | 未完了 | 未完了 | 未完了 | FAIL |')
            else:
                lines.append(f'| {row["case"]} | {row["safety_factor_p99_5"]:.2f} | {row["worst_element_safety_factor"]:.3f} | {row["max_disp_mm"]:.4f} | {"PASS" if row["pass"] else "FAIL"} |')
        lines += ['', '追加結果: `_work/analysis/topology_petg/candidate_ccx_netgen/ccx_summary.json`。局所応力が跳ねる箇所は、内側工具穴の入口近傍（X≈22.36、Y≈-60.32、Z≈10.58 mm）。この角部と荷重の写像を改善し、再度収束を確認する必要がある。p99.5だけで安全とは判定しない。']
    lines += ['', '最悪局所SFと各ケースの収束を含めた判定をverification_summary.jsonへ保存。未合格の場合は現行assembly/印刷STLへ昇格しない。', '',
              '## 造形・実機確認', '',
              '設計した積層Zで平置き。既存の内側ワッシャ/工具穴には除去可能な局所サポートが必要。貫通ポケットに閉じ込められるサポートは不要。自動printコマンドが提案するY上向きは材料軸を変えるので今回の解析を適用しない。造形枠・最小肉厚はPASS、サポート不要の判定はFAIL。', '',
              '仮のμ=0.15、予張力残存50%、柔らかいリングのN=πΣF近似では滑り容量141 N/組、今回39.23 Nに対し3.60倍。ただし硬いPETGの接触分布・濡れ・真円度で下がるため実測値ではない。試作の濡れた軸方向引抜き、4 kg保持、時間経過後の保持を確認する。ボルト頭/ナットは工具アクセスの都合でゴムと容器を入れる前に設置する。フレーム、下側支え、ケーブル、実重心は未設計なので全体干渉確認は未完了。', '',
              '## 再生成', '', '```powershell',
              'python tools/prepare_child_clamp_topopt.py',
              'python -m topopt setup <case>/study_topology.json --out <case>/setup --iters 80',
              'python -m topopt opt <case>/study_topology.json --out <case>/opt_v055 --volfrac 0.55 --iters 80 --quick',
              'python -m topopt compare <case>/opt_v055 <case>/candidate.stl --study <case>/study_topology.json --out <case>/compare_rails6',
              'python tools/remesh_child_clamp_surface.py --stl <case>/candidate.stl --out <case>/surface_remesh',
              '$env:TOPOPT_GMSH = (Join-Path (Get-Location).Path "tools/gmsh_clamp_delaunay.cmd")',
              '$env:OMP_NUM_THREADS="4"; $env:CCX_NPROC_EQUATION_SOLVER="4"',
              'python -m topopt ccx <case>/surface_remesh/candidate.stl --study <case>/study_candidate.json --out <case>/candidate_ccx_convergence --mesh-mm 5 --map surface --converge',
              'python tools/verify_child_clamp.py --stl <case>/candidate.stl --out <case>/geometry_checks.json',
              'python tools/report_child_clamp_topopt.py', '```', '',
              '`<case>` = `parts/child/exterior/printed/child_wte4_suspension_clamp/_work/analysis/topology_petg`。`PYTHONIOENCODING=utf-8`を設定して実行。raw/quick出力は探索記録。採用には今回の判定と実機保持試験を満たすこと。']
    (PART/'TOPOLOGY.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps(dict(pass_check=bool(passed), reduction_percent=float(reduction), report=str(PART/'TOPOLOGY.md'))))


if __name__ == '__main__':
    main()
