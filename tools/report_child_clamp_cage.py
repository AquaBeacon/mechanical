"""Write current cage documentation from native solver/geometry/slicer results."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
ASSEMBLY = ROOT/'assemblies/child_clamp_suspension'
CASE = PART/'_work/analysis/connected_cage_rubber1_v065'


def read(path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def assembly_step_result():
    """Keep the native FreeCAD verification verdict with its input identities."""
    log = CASE/'assembly_step_verify.log'
    if not log.exists():
        return {}
    content = log.read_text(encoding='utf-8',errors='replace')
    verdict = re.search(r'\[verify-asm\] (\d+) item\(s\), (\d+) NG',content)
    if not verdict:
        return {}
    count, failures = map(int,verdict.groups())
    placement = read(ASSEMBLY/'placement.json')
    reported = re.findall(r'\[verify-asm\].*? maxdiff=([0-9.]+)',content)
    result = dict(native_tool='FreeCAD scad/lib/verify_asm_step.py',
        item_count=count,failures=failures,
        max_reported_bound_difference_mm=max(map(float,reported),default=None),
        tolerance_mm=.5,
        pass_check=bool(failures==0 and count==len(placement['items']) and len(reported)==count),
        input_sha256={path.relative_to(ROOT).as_posix():hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [ASSEMBLY/'placement.json',ASSEMBLY/'child_clamp_suspension.step']},
        native_log='assembly_step_verify.log')
    (CASE/'assembly_step_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


def main():
    opt = read(CASE/'opt/study_cage.json')
    final_fea = read(CASE/'fea/finished_cage_fea.json')
    geometry = read(CASE/'geometry_checks.json')
    slicing = read(CASE/'slice_checks.json')
    ccx = read(CASE/'ccx/ccx_summary.json')
    independent = read(CASE/'independent_analysis_status.json')
    steps = read(CASE/'step_checks.json')
    representation = read(CASE/'step_representation.json')
    assembly_steps = assembly_step_result()
    dims = ' × '.join(f'{x:.2f}' for x in geometry.get('print_extents_mm',[])) or '解析中'
    grams = geometry.get('PETG_mass_g_two_halves',0)
    lines = ['# 3段連結クランプと吊り穴（2026-10-01）','',
        '既存の半割りM3クランプを軸方向に3段つなぎ、WTE4容器を囲むケージを2つの同一半割りで作る。中央の固定ねじ4本がある面側の上端に、各半割り1個のØ10.5 mmロープ穴を置いた。3段間の接続形状と吊り耳への荷重経路を、native topoptの応力制約付き最適化で同時に求め、密度場を直接平滑化している。単純なリブへの置換は行っていない。','',
        '**exploration_only: 形状・造形検討用。吊り上げ使用の強度認定は未完了。** 最適化、完成形状の独立解析、実物の印刷・濡れたゴムの引抜き・クリープは別の検査であり、造形枠やスライスの合格を強度へ転用しない。','',
        '## 寸法・取合い','',
        '| 項目 | 寸法・条件 |','|---|---|',
        '| WTE4 | 既存のØ114.3 × 200 mm。容器・フランジ・蓋を変更しない |',
        '| ゴム | ユーザー確認済み1 mmシート。硬度・材質は未確定。20%圧縮後0.8 mmは仮定 |',
        '| 接触面内径 | Ø115.9 mm。圧縮量は予張力を意味しない |',
        '| バンド中心 / 幅 | Z=40 / 100 / 160 mm、各32 mm |',
        '| 吊り穴 | Ø10.5 mm、ねじ山なし。後半体は(0,-73,194)、軸X。前半体は180°回転した対向位置 |',
        '| 吊り耳 | 軸方向半径16、半径方向12、幅24 mm。穴口1.2 mm面取り |',
        '| M3締結 | 4本/段、3段で12本。Ø3.5通り穴、既存のM3×60・ナット・OD12ワッシャ |',
        '| 中央の固定4穴 | 36 × 16 mmピッチを各段で保持。今回の吊り解析では支持に使わない |',
        f'| 印刷外形 / 質量 | {dims} mm、同一半割り2個で約{grams:.1f} g（PETG 1.25 g/cm³、サポート・ゴム・金属別） |','',
        '外形端部とゴム接触面の縁は0.6 mm面取り、従来の根元はR3、吊り穴口は1.2 mm面取り。完成CADでM3入口へ0.3 mm面取りを追加し、機能径を維持する。正確なワッシャ座・工具段差は機能面として保持する。工具穴と内側曲面の交差稜線は、3 mm以上の屋根残肉とOD9ワッシャ着座の取合いを保つため維持する。最適化面の平滑化は1 mm。曲面同士の結合部は実メッシュの局所確認が完了するまで全面検証済みとは扱わない。','',
        '## 解析条件と結果','',
        'Bambu PETG Basicアップグレード版TDS V3.0を反映した既存の暫定異方性カードを継承。100%インフィル、外周8、積層Y、ラスタZ。印刷回転はX=90°で、容器軸Zの吊り荷重を積層面内に置く。メーカーにないせん断・圧縮特性は暫定値のまま。材料の根拠は[BAMBU_PETG_BASIC.md](BAMBU_PETG_BASIC.md)の材料節。','',
        '完成機質量4 kgを仮定（このケージを含む。実測質量ではない）し、静荷重39.2266 N、2g 78.4532 Nを1つの半割り・1つの吊り耳だけへ負担させる保守的なモデル。各段M3予張力150 N/本の仮定。3段の分担を50/25/25%として50%の段を入れ替える。通常SF3、異常SF1.5、変位上限1 mm。締付けのみ、静荷重3ケース、2g3ケース、X±とY±の偏荷重4ケースの計11ケース。底・固定4穴・蓋ねじへ支持の効果を数えない。','',
        '吊り穴の剛なピン領域を固定した近似で、ロープ接触・ピン回転・相手半割りとの接触を解くモデルではない。実ロープの掛け方、角度、濡れた摩擦、クリープの認定は別途必要。','',
        f'最適化: 2 mm格子、自由領域体積率0.65、フィルタ6 mm、100反復、終了理由 `{opt.get("termination_reason","実行中")}`。native全体判定: `{opt.get("pass","未評価")}`。最大反復到達を完全収束とは呼ばない。','',
        '| ケース | 最適化格子の変位 mm | SF p99.5 | 最悪局所SF | native判定 |','|---|---:|---:|---:|---|']
    for row in opt.get('final_fea',[]):
        lines.append(f'| {row["case"]} | {row["max_displacement_mm"]:.4f} | {row["safety_factor_p99_5"]:.3f} | {row["min_safety_factor"]:.3f} | {row["pass"]} |')
    lines += ['', '上表は最適化格子の値。平滑化・正確な穴加工後の完成STLの強度へ代用しない。', '',
        f'完成STLのnativeボクセル再解析（1 mm格子）: `{final_fea.get("pass","未完了")}`。単一格子の結果はメッシュ収束の証明ではない。', '',
        '| ケース | 完成STL変位 mm | SF p99.5 | 最悪局所SF | native判定 |', '|---|---:|---:|---:|---|']
    for row in final_fea.get('cases', final_fea.get('results', [])):
        lines.append(f'| {row["case"]} | {row["max_displacement_mm"]:.4f} | {row["safety_factor_p99_5"]:.3f} | {row["min_safety_factor"]:.3f} | {row["pass"]} |')
    lines += ['',
        '完成STLではX負方向の2g偏荷重 `skew_x_-1_2g` の変位1.079 mmが1 mm基準を超過したため、完成形状のnative総合判定はFAIL。通常・異常荷重の強度指標と他10ケースが通っていても、吊り上げ使用の合格とは扱わない。今回の納品は寸法・造形を検証した試作用CADで、実使用前には剛性基準の達成と独立メッシュ収束が必要。', '',
        f'完成形状の独立解析: native CalculiX判定 `{ccx.get("pass","未完了")}`。詳細は `_work/analysis/connected_cage_rubber1_v065/ccx/`。表面細分化あり、同じ材料・荷重・領域・支持を使う。メッシュ品質・体積・局所ピークと収束を確認する。メッシュ生成停止や収束未合格の結果から吊り上げ可とは判定しない。','',
        f'独立解析の実行状態: `{independent.get("failed_stage","未評価")}`。{independent.get("reason","")} 原形状をHXTで四面体化する段階で制約面を回復できず、3D要素が作られなかった。CalculiXの荷重解析・3メッシュ収束は未成立。失敗記録は `independent_analysis_status.json` とnativeログ。', '',
        '## 造形・形状検証','',
        f'- 閉メッシュ・1物理ボディ、M3穴12本/半体、固定4穴×3段と工具/ワッシャ通路、ゴム接触、WTE4全購入品との干渉: `{geometry.get("pass","未評価")}`。',
        f'- STEP/STL外形・体積読み戻し: `{steps.get("pass_check","未評価")}`。STEPは密度面の面数を減らした後、同じSCADで穴・座面・ゴム面を復元したファセットソリッド。表示用近似面は{representation.get("proxy_faces","未評価")}三角形。印刷STLと解析入力は元の245084三角形を保持。',
        f'- 組立STEPの配置読み戻し: `{assembly_steps.get("pass_check","実行中")}`。native FreeCADでplacement.jsonに対する全{assembly_steps.get("item_count",61)}部品の位置を照合。詳細は `assembly_step_checks.json` と `assembly_step_verify.log`。',
        '- 配布STL・3MF・解析入力の同一性と印刷一式/整理/ツールテストの記録は `delivery_checks.json`。`shape_print_preparation_pass` と `lifting_qualification_pass` は独立した判定。',
        f'- STEP用メッシュの印刷STLとの体積差{100*representation.get("relative_volume_error",0):.6f}%、外形最大差{representation.get("max_bounds_error_mm","未評価")} mm。密度面の双方向MeshLabサンプル最大差0.0964 mm（全域の厳密誤差上限ではない）。元の245084面STEPは読み戻しが30分を超えたため、case内の `full_faceted_step.step` へ保持。',
        f'- X1 Carbonの250 mm保守的枠と5 mmブリム、手元の18 × 28 mm除外領域の回避: `{geometry.get("fits_x1c_250mm_with_5mm_brim","未評価")}` / `{geometry.get("avoids_installed_x1c_exclusion","未評価")}`。',
        f'- Bambu Studio実スライス、X90°回転済みの姿勢を維持、100%インフィル、外周8、上下8層、0.20 mm、255°C/ベッド70°C: `{slicing.get("pass_check","未評価")}`。',
        f'- Textured PEI Plate、1個/プレート。予測{(slicing.get("print_time_s") or 0)/3600:.2f}時間、PETG {(slicing.get("filament_g") or 0):.2f} g/プレート（サポート込み）。同じ半割りを2プレート造形。スライス済み3MFとハッシュ・設定はassemblyの `print_jobs/`。',
        '- 矩形充填の基準角は90°（印刷XYのY、設計座標Zに対応）、層ごとに交互方向。異方性材料カードのラスタZはこの工具経路を単一方向で近似した暫定入力。',
        '- サポートはベッド面からのみ。密閉空洞内へ除去不能なサポートを入れない。内部ブリッジと吊り穴内の除去可能性は断面・実物で確認する。支持なし造形の合格は意味しない。','',
        '印刷一式のSTLはX90°回転・ベッド原点への移動済み。スライサの自動姿勢変更を使わず、同じ半割りを2個、1個/プレートで造形する。5 mm外ブリムを指定し、反り・穴欠損のないことを確認する。ゴムは幅32 mm、半周約179 mmを6枚切って実物で端を調整。3段を少しずつ均等に締め、割り面が底付きせずゴムへ圧力が残ることを確認する。圧縮量・トルクだけで保持力を保証しない。','',
        '## 正本と再生成','',
        'SCADは従来の1か所を拡張し、`model="cage"` が `spec/cage_density_surface.stl` を読み込む。穴・座面・ゴム面は同じSCADから復元。平滑化元と材料カードをmanufacturing.jsonのsource_dependenciesに記録。配置・個数は既存assemblyのplacement.jsonが正本。','',
        '```powershell', '$env:PYTHONIOENCODING="utf-8"',
        'python tools/prepare_child_clamp_cage.py',
        'python tools/clamp_bambu_material.py setup <case>/study_cage.json --out <case>/setup --voxel 2 --iters 100',
        'python tools/run_child_clamp_cage.py',
        'python tools/clamp_bambu_material.py fea <case>/study_final.json --out <case>/fea --voxel 1 --no-png  # 終了コード1は判定未達。結果を確認する',
        'python tools/verify_child_clamp_cage.py',
        'python tools/slice_child_clamp_cage.py',
        'python tools/package_child_clamp_cage.py',
        '.\\build.ps1 parts\\child\\exterior\\printed\\child_wte4_suspension_clamp',
        'python tools/build_child_clamp_cage_step.py  # CAD用STEPの面数削減・正確な取合い復元・読み戻し',
        '.\\build.ps1 -Assemblies assemblies\\child_clamp_suspension',
        'python tools/report_child_clamp_cage.py',
        'python tools/assembly_parts.py sync child_clamp_suspension',
        'python tools/assembly_parts.py check',
        'python tools/tidy_workspace.py check', '```','',
        '`<case>` は設計元の `_work/analysis/connected_cage_rubber1_v065`。setupプレビュー確認後にrunを実行する。CCXや追加検証の生データは同caseへ保持する。初回体積率0.50案は `_work/analysis/connected_cage_rubber1` に保持し、完成STLの偏荷重変位超過で不採用。','',
        '2026-09-28以前の単体クランプ・1.5 mmゴム・積層Zの解析は履歴。旧原本・配置・STL/STEPを `_work/analysis/single_clamp_20260928_snapshot/` に保存した。旧smooth出力を今回の印刷一式へ含めない。']
    (PART/'CAGE_TOPOLOGY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (PART/'README.md').write_text(f'''# WTE4子機・3段連結M3/PETGクランプ

3つのクランプを一体につないだ半割りケージを2個でWTE4耐圧容器に取り付けます。固定ねじ4本の面側の上端に、各半割り1個、計2個のØ10.5 mmロープ穴があります。接続部も含めて応力制約付きトポロジー最適化を行い、密度場を直接平滑化しています。

ゴムはユーザー指定の1 mmへ更新。仮の20%圧縮で接触面内径Ø115.9 mmです。既存M3の穴・ワッシャ座・3段の位置（40/100/160 mm）を再利用します。完成機4 kg・取扱い2g、Bambu PETG Basic TDS V3.0を引き継ぎ、吊り荷重が積層面内になるY積層で検討しました。

印刷入口は [parts/PRINT.md](../../../../../assemblies/child_clamp_suspension/parts/PRINT.md)。同じ半割り2個、印刷姿勢の外形は{dims} mm、PETG約{grams:.1f} g/2個（サポート・ゴム・金属別）。印刷一式のSTLはX90°回転済みです。1個/プレート、5 mmブリム、100%インフィル、外周8、上下8層、0.20 mm、0.4 mmノズルで使います。

**exploration_only: 形状・造形検討用。吊り上げ使用の強度認定は未完了。** 実物の層間強度・ゴム保持・湿潤引抜き・クリープ・内部ブリッジの確認が必要です。

完成STLの再解析では偏荷重1ケースの変位1.079 mmが1 mm基準を超過しました。独立四面体解析もメッシュ生成で停止し、収束確認は未完了です。吊り上げ使用前には、この未達を解消します。

寸法・解析・実スライス・再生成は [CAGE_TOPOLOGY.md](CAGE_TOPOLOGY.md)。配置は [assembly](../../../../../assemblies/child_clamp_suspension/README.md)。ゴムとM3金属部品は印刷しません。締付けM3×60は12本、ナット12個、OD12ワッシャ24枚。中央の4穴パッドは保持していますが今回の吊り支持には使いません。

旧単体の解析は [SMOOTH_TOPOLOGY.md](SMOOTH_TOPOLOGY.md)、材料の根拠と2026-09-28の数値は [BAMBU_PETG_BASIC.md](BAMBU_PETG_BASIC.md)。旧README・SCAD・配置・STL/STEPは `_work/analysis/single_clamp_20260928_snapshot/` に保存しています。
''',encoding='utf-8')
    (ASSEMBLY/'README.md').write_text(f'''# 子機外装・WTE4の3段連結クランプ

3段のM3クランプをトポロジー最適化で一体につないだ半割りケージ2個で、既存WTE4（Ø114.3 × 200 mm）を囲みます。固定ねじ4本の面側の上端にØ10.5 mmのロープ穴を各半割り1個設けています。ゴムは1 mm、圧縮後0.8 mmは仮定です。

印刷入口は [parts/PRINT.md](parts/PRINT.md)。同じ半割り2個、X90°回転済みのSTL外形{dims} mm。1個/プレートで5 mmブリムを付けます。材料はBambu PETG Basic（アップグレード版TDS V3.0）、100%インフィル・外周8・上下8層・0.20 mm・0.4 mmノズルです。

**exploration_only: 形状・造形検討用。吊り上げ使用の強度認定は未完了。** 4 kg完成機・2gの入力を引き継いでいますが、完成形状の独立解析・実物の造形/湿潤引抜き/クリープを通してから運用します。蓋ねじ・未設計フレーム・底面支持の効果は解析へ含めていません。

完成STLの再解析では偏荷重1ケースの変位1.079 mmが1 mm基準を超過しました。独立四面体解析はメッシュ生成で停止し、収束確認は未完了です。寸法・X1 Carbonの実スライスを検証した試作用CADとして保存し、吊り上げ使用前には剛性未達と独立収束を解消します。

- [設計元と取合い](../../parts/child/exterior/printed/child_wte4_suspension_clamp/README.md)
- [最適化・形状検査・実スライス](../../parts/child/exterior/printed/child_wte4_suspension_clamp/CAGE_TOPOLOGY.md)
- [配置の正本](placement.json) / [組立STEP](child_clamp_suspension.step)

バンド中心はZ=40/100/160 mm、各幅32 mm。半割りは前後180°対向。M3×60締付け12本、ナット12、OD12ワッシャ24枚、1 mmゴム半周6枚。中央の固定4穴（36 × 16 mmピッチ）を各段で残しています。工具と内側ワッシャを使う場合はゴム・容器を置く前に取り付けます。容器とフランジの保守通路を塞ぎません。

旧単体3組の1.5 mmゴムの構成は設計元の履歴へ保存しました。[STRENGTH.md](STRENGTH.md)はさらに古い厚肉4g案で、今回の形状へ数値を転用しません。
''',encoding='utf-8')
    index = ROOT/'docs/部品一覧.md'
    text = index.read_text(encoding='utf-8')
    text = '\n'.join(f'子機の新外装用（2026-10-01）: [WTE4の3段連結M3/PETGクランプ](../parts/child/exterior/printed/child_wte4_suspension_clamp/README.md)。同じ半割りケージ2個、固定4穴の面側上端にØ10.5ロープ穴2個。ゴム1 mm、仮圧縮0.8 mm。接続部も含めた応力制約付き最適化と直接平滑化。印刷姿勢X90°、100%インフィル。[配置・印刷入口](../assemblies/child_clamp_suspension/README.md)。exploration_only、吊り上げ使用の独立強度・湿潤滑り・クリープ・実物造形は未認定。' if '子機の新外装用' in row and 'child_wte4_suspension_clamp' in row else row for row in text.splitlines())+'\n'
    index.write_text(text,encoding='utf-8')
    print('Updated cage part/assembly documentation and human parts index.')


if __name__ == '__main__':
    main()
