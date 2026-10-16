"""Document the adopted prototype using measured files, preserving failed studies."""
from pathlib import Path
import json
import math
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
ASM=ROOT/'assemblies/child_clamp_suspension'
CASE=analysis_case(PART)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    policy=PART/'spec/topology_postprocess_policy.json'
    if policy.exists() and read(policy).get('mode')=='direct_smoothed_density':
        raise RuntimeError('Use report_child_clamp_direct_density.py for the current user-required geometry.')
    adoption=read(CASE/'canonical_adoption.json')
    geometry=read(CASE/'geometry_checks.json')
    sliced=read(CASE/'slice_checks.json')
    interface=read(CASE/'interface.json')
    d=interface['clamp']
    total=sliced['filament_g']*2
    reduction=(1-total/1516.08)*100
    length=10*math.ceil((2*d.get('ear_t',24)+1.6+2+2.4+3)/10)
    dims=' × '.join(f'{x:.2f}' for x in geometry['print_extents_mm'])
    results=[]
    paths=set(CASE.glob('fea*/finished_cage_fea.json'))|set(CASE.glob('fea_grouped/*/finished_cage_fea.json'))
    paths={p for p in paths if p.parent.name!='fea_preload_sensitivity'}
    for p in sorted(paths):
        cs=read(p)['cases']
        results.append(f'| `{p.relative_to(CASE).as_posix()}` | {len(cs)} | {cs[0]["voxel_mm"]:g} | '
                       f'{max(c["max_displacement_mm"] for c in cs):.3f} | '
                       f'{min(c["min_safety_factor"] for c in cs):.3f} | '
                       f'{min(c["safety_factor_p99_5"] for c in cs):.3f} |')
    grouped=CASE/'grouped_convergence.json'
    convergence='未完了'
    if grouped.exists():
        batch=read(grouped)
        convergence='合格' if batch.get('pass',False) else '未合格（nativeメッシュ収束判定FAIL。詳細JSONを参照）'
    validation_path=CASE/'validation_summary.json'
    validation=read(validation_path) if validation_path.exists() else {}
    fine_text='細格子の全ケース集計は未完了です。'
    if validation.get('all_original_native_fine_cases_present',validation.get('all_11_native_fine_cases_present')):
        fine_text=(f"0.5 mm細格子の11ケースは全て計算済み。最大変位 {validation['native_fine_max_displacement_mm']:.3f} mm、"
                   f"最小の最悪要素安全率 {validation['native_fine_min_safety_factor']:.3f}、"
                   f"最小p99.5安全率 {validation['native_fine_min_p99_5_safety_factor']:.3f}。"
                   '各ケースの細格子判定と最悪要素下限は通過しましたが、2/1/0.5 mm間のnative収束判定は通過していません。')
    ccx_text='CalculiX独立解析は未完了です。'
    execution_path=CASE/'ccx_execution.json'
    if execution_path.exists():
        execution=read(execution_path)
        ccx_text=(f"CalculiX独立解析の実行終了コードは {execution['exit_code']}。"
                  f"native集計出力は{'あり' if execution['native_summary_present'] else 'なし'}、"
                  f"native総合判定は{'合格' if validation.get('ccx_native_pass') else '未合格'}。"
                  '16/8/4 mmの収束確認を指定し、二次四面体C3D10・全11荷重・表面細分化を維持しました。'
                  '実行記録は `ccx_execution.json`、診断は `ccx_run.log` と `ccx/` を参照。')
        failure_messages={
            'below the absolute minimum 1.5':'最悪要素安全率が絶対下限1.5未満',
            'the load/reaction balance did not close':'荷重・反力の釣合い不成立',
            'nonpositive jacobian':'非正ヤコビアン（不適切な四面体要素）によるソルバ停止',
        }
        failures=validation.get('ccx_native_log_failures',[])
        if failures:
            ccx_text+=' ログに記録された問題：'+ '、'.join(failure_messages.get(f,f) for f in failures)+'。独立解析の強度合格を裏付ける結果ではありません。'
    preload_text='最新形状の75/300 N感度解析は未実施です。'
    sensitivity=CASE/'fea_preload_sensitivity/finished_cage_fea.json'
    if sensitivity.exists():
        sensitivity_cases=read(sensitivity)['cases']
        rows=[]
        for force in [75,300]:
            selected=[c for c in sensitivity_cases if c['case'].endswith(f'_preload{force}N')]
            if len(selected)!=11: raise RuntimeError('Incomplete preload sensitivity batch')
            rows.append(f'| {force} N/本 | {max(c["max_displacement_mm"] for c in selected):.3f} mm | {min(c["min_safety_factor"] for c in selected):.3f} | {min(c["safety_factor_p99_5"] for c in selected):.3f} |')
        preload_text='''最新形状でも75/300 Nの22ケースを2 mm格子で実行しました。

| 仮定締付け力 | 全ケース最大変位 | 最悪安全率 | p99.5安全率 |
|---|---:|---:|---:|
'''+chr(10).join(rows)+'''

300 N/本は偏荷重時に1 mm変位基準を超過しました。粗い単一格子の感度値であり、許容トルクや推奨軸力ではありません。原本は最新caseの `study_preload_sensitivity.json` と `fea_preload_sensitivity/finished_cage_fea.json`。
'''
    review=f'''# 軽量化の納品記録（2026-10-05）

現行は `{CASE.name}` のパラメトリック再構成案。トポロジー最適化の荷重経路を参考に、リング・柱・締付け耳を再設計したものです。新しいSIMP収束解そのものではありません。**exploration_only：形状・造形検討用。4 kg吊り下げ使用の合格品ではありません。**

## 材料量（半割り2個の合計）

| 比較 | 従来 | 今回 |
|---|---:|---:|
| CAD実体積×PETG 1.25 g/cm³ | 1418.24 g | {geometry['PETG_mass_g_two_halves']:.2f} g |
| Bambu Studio実スライス・サポート等込み | 1516.08 g | {total:.2f} g |

使用フィラメントを **{reduction:.1f}%削減**。100%インフィル・外周8・上下8層・0.20 mm・X90°の姿勢は維持し、サポート方式は `{sliced['support_type']}`。従来は通常サポートのため、スライス使用量の差には形状変更とサポート方式変更の両方を含みます。1個あたり {sliced['filament_g']:.2f} g、予測時間 {sliced['print_time_text']}。実機の印刷成功を確認した値ではありません。

## 形状と取合い

- 同一の3段連結半割りを2個。バンド中心Z=40/100/160 mm。
- 容器Ø114.3 mm、EPDM自由厚1 mm、圧縮後0.8 mmは仮定。接触幅 {d.get('contact_width',32):g} mm。
- 外部固定4穴×3段はX=±18、Z=各段中心±8、外面Y=-84.95 mmを維持。
- ドーム側上端・外部固定面側にØ10.5 mm吊り穴を各半割り1個。中心[0,-73,194] mm、反対半割りは180°回転。ロープ径未指定の暫定穴。
- 締付けボルト中心X=±{d['bolt_x']:g} mm、耳厚 {d.get('ear_t',24):g} mm。M3×{length}全ねじ12本、M3ナット12個、OD12×厚1 mmワッシャ24枚。頭形状は既存CADと同等の工具が入るもの。
- 公称分割隙間1.6 mmは許容締込み量ではない。締付けトルク・EPDM摩擦・硬度・クリープは未確認。
- 局所面取り0.6 mm、穴入口0.3 mm、吊り穴入口1.2 mm。薄い面板縁0.25 mm、リブ根元は局所丸み。ワッシャ座と円筒の接触面は機能寸法を優先する。

閉メッシュ、1物理ボディ、密閉空洞0、各取付穴と工具/ワッシャ通路、容器5部品との干渉、半割り間隙、X1C造形枠を検査済み。印刷外形 {dims} mm。CAD検査の正本は同caseの `geometry_checks.json`。これらは強度試験ではありません。

ワッシャ座面の多角形化による面位置の差は最大 {geometry.get('clamp_washer_seat_surface_deviation_mm',0):.4f} mm（検査許容0.02 mm）。金属部品は最も外側の実座面Y=±{abs(geometry.get('clamp_washer_seat_y',-d.get('ear_t',24)-.8)):.4f} mmに合わせています。実配置の干渉とナットからのねじ突出は `hardware_checks.json`、STEP/STL照合は `step_checks.json` を参照。

## 構造解析の実測出力

4 kg、2g、横1g偏荷重、締付け150 N/本、片側だけで全荷重を受ける11ケースを維持。材料はBambu PETG Basic TDSを基にした暫定直交異方性カード、造形Y・ラスタZ。許容変位1 mm、p99.5安全率は通常3・異常時1.5、最悪要素の絶対下限1.5。全て既存topoptソルバを使用し、独自FEAは実装していません。

| 出力 | ケース数 | 格子mm | 最大変位mm | 最悪安全率 | p99.5安全率 |
|---|---:|---:|---:|---:|---:|
{chr(10).join(results)}

{fine_text}

ボクセルのメッシュ収束判定：**{convergence}**。単一格子値や途中の細格子値を収束済み最終値とは扱いません。最悪要素安全率1.5未満をp99.5の値で隠して合格にしません。

{ccx_text}

全検証の集計は同caseの `validation_summary.json`。EPDMの摩擦接触・容器の接触圧力・湿潤滑り・長期クリープ・実造形ばらつきはこの線形解析では認定できません。

## 履歴と再現

volfrac0.20のnative最適化は100反復・最大反復終了で未収束。911 gスライス候補は最大変位4.808 mmで不採用。ボルトアクセス切欠きの拡大案は細格子で局所安全率低下、外側ボルト・幅24 mm案は本体1028 gかつ変位1.433 mmで不採用。全候補・失敗ログは `_work/analysis/lightweight_*` に保存し、旧CAD/印刷資料は `lightweight_lattice/before_revision/` に保存しています。

正本は同部品のSCADとmanufacturing.json。原始密度メッシュは印刷用に配布していません。採用時のCSG一致は `{CASE.name}/canonical_adoption.json`、ソース/STLハッシュとパラメータは同caseのJSONに記録。印刷用コピーを直接編集しません。

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:CHILD_CLAMP_CASE='{CASE.name}'
python tools/verify_child_clamp_cage.py --require-no-closed-voids
python tools/slice_child_clamp_cage.py --support tree
python tools/assembly_parts.py sync child_clamp_suspension
python tools/assembly_parts.py check child_clamp_suspension
```

SCADを変更した場合は先に再レンダリング・再解析・STEP再生成が必要です。syncだけではCADは再生成されません。
'''
    (PART/'LIGHTWEIGHT_REVIEW.md').write_text(review,encoding='utf-8')
    (PART/'EPDM_ADJUSTMENT.md').write_text(f'''# EPDM 1 mmと締付け調整（2026-10-05）

自由厚1 mm・硬度不明はユーザー確認済み。圧縮後0.8 mm、通常解析の150 N/本は仮定であり、必要トルクや保証された保持力を表す値ではありません。最新形状と判定は [LIGHTWEIGHT_REVIEW.md](LIGHTWEIGHT_REVIEW.md) を参照。

## 現行の調整機構

M3×{length}全ねじ12本、ナット12個、OD12×厚1 mmワッシャ24枚で調整します。容器を支持した状態で、3段左右を少しずつ交互に締め、隙間、ゴムのはみ出し、耳と容器の変形を確認します。公称分割隙間1.6 mmを全量締め込んでよいという意味ではありません。分割面を接触させるまで締め切らず、ねじ回転数から軸力を換算しません。強く締めるほど安全になるとは限りません。

EPDMの摩擦・圧縮特性・湿潤滑り・長期クリープ・容器接触圧力は未評価。実物で必要な保持力と許容締付け範囲を確認するまで、吊り下げ運用は未認定です。

## 保存した感度解析

旧重量版と中実設計領域について、75/300 N/本の22ケースを2 mm格子で比較しました。旧重量版の300 N締付け単独変位は1.557 mm、全ケース最大1.779 mm。中実領域は1.364/1.561 mmで、いずれも1 mmを超過しました。これらは `_work/analysis/epdm_adjustable_20261005/` の旧形状の感度値であり、現行軽量形状の結果ではありません。75/300 Nを推奨締付け力として使わないでください。

## 最新形状の感度確認

{preload_text}

単一格子の感度値は収束・強度保証の代わりにはなりません。
''',encoding='utf-8')
    common=f'''2026-10-05：半割り2個の実スライス使用量を **1516.08 g → {total:.2f} g（{reduction:.1f}%削減）** に変更しました。本体のCAD体積換算は {geometry['PETG_mass_g_two_halves']:.2f} g。3段連結・外部固定4穴×3段・ドーム側上端のØ10.5 mm吊り穴を維持しています。

**exploration_only：4 kg吊り下げ使用の強度合格は未確認。** メッシュ収束は{convergence}。形状/スライスの合格を吊り下げ強度の合格とは扱いません。

CalculiX独立解析も未合格。詳細な原因・実行記録は設計元のLIGHTWEIGHT_REVIEW.mdに保存しています。

同じSTLを2個、1個/プレート。Bambu PETG Basic、255°C/70°C、0.4 mmノズル、0.20 mm、100%インフィル、外周8・上下8層、5 mm外ブリム、ベッドからのツリーサポート。STLはX90°回転済み、外形 {dims} mm。1個 {sliced['filament_g']:.2f} g、{sliced['print_time_text']}のスライス予測。

EPDM自由厚1 mm・硬度不明。圧縮後0.8 mmは仮定。接触幅{d.get('contact_width',32):g} mm、バンド中心Z=40/100/160 mm。締付け用M3×{length}全ねじ12本、ナット12個、OD12×厚1 mmワッシャ24枚。公称隙間1.6 mmを締め切らず、支持した状態で3段左右を交互に調整します。必要トルクと滑り保持性能は未確定です。
'''
    (PART/'README.md').write_text('# WTE4子機・軽量3段連結クランプ\n\n'+common+'''
印刷入口は [PRINT.md](../../../../../assemblies/child_clamp_suspension/parts/PRINT.md)。

- [軽量化・解析・再現記録](LIGHTWEIGHT_REVIEW.md)
- [EPDM調整と旧形状の感度解析](EPDM_ADJUSTMENT.md)
- [材料定数](BAMBU_PETG_BASIC.md)
- [組立と配置](../../../../../assemblies/child_clamp_suspension/README.md)

現行の正本は `child_wte4_suspension_clamp.scad` の cage バリアント。旧密度形状は cage_density、旧単独バンドは half として保持します。旧解析値を現行形状の合格根拠には転用しません。
''',encoding='utf-8')
    (ASM/'README.md').write_text('# 子機外装・軽量3段連結クランプ\n\n'+common+'''
印刷・数量・組付けの入口は **[parts/PRINT.md](parts/PRINT.md)**。実STLと説明をparts内に同梱し、3MFはprint_jobs内に保存しています。配置の正本はplacement.json。購入品やゴムは印刷しません。

- [軽量化と全検証結果](../../parts/child/exterior/printed/child_wte4_suspension_clamp/LIGHTWEIGHT_REVIEW.md)
- [設計元](../../parts/child/exterior/printed/child_wte4_suspension_clamp/README.md)
- [組立STEP](child_clamp_suspension.step)

固定面の内側ワッシャ・工具はゴムと容器を入れる前に取り付けます。材料内部に密閉空洞はありません。ロープ径未指定のためØ10.5 mmは暫定。実機印刷・支持下での静荷重/偏荷重・湿潤滑り/長期クリープ確認を終えるまでは吊り下げ使用へ移行しません。
''',encoding='utf-8')
    config=read(ASM/'print_config.json')
    config['note']=config['note'].split(' 最新軽量版:')[0]
    config['note']+=f' 最新軽量版: 2個合計{total:.2f}g（サポート等込み予測）、従来比{reduction:.1f}%減。締付けボルトはM3×{length}全ねじ。数値収束: {convergence}。'
    config['note']+=' CalculiX独立解析も未合格（局所安全率・荷重反力釣合い・要素形状の問題）。4 kg吊り下げ使用には移行しない。'
    config['notes']=[str((PART/n).relative_to(ROOT)).replace('\\','/') for n in ['LIGHTWEIGHT_REVIEW.md','EPDM_ADJUSTMENT.md','BAMBU_PETG_BASIC.md']]
    (ASM/'print_config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Documented {CASE.name}: {total:.2f} g, saving {reduction:.1f}%')


if __name__=='__main__':main()
