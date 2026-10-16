"""Report measured native-density candidates; publish only the adopted identity."""
from pathlib import Path
from datetime import date
import argparse
import hashlib
import json
import math
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
ASM=ROOT/'assemblies/child_clamp_suspension'
CASE=analysis_case(PART)

def read(path): return json.loads(path.read_text(encoding='utf-8'))
def save(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish',action='store_true')
    args=parser.parse_args()
    g=read(CASE/'geometry_checks.json'); s=read(CASE/'slice_checks.json')
    p=read(CASE/'final_provenance.json'); study=read(CASE/'study_cage.json')
    opt=read(Path(p.get('native_optimisation_dir',str(CASE/'opt')))/'study_cage.json'); interface=read(CASE/'interface.json')
    v=read(CASE/'validation_summary.json')
    grouped=read(CASE/'grouped_convergence.json')
    d=interface['clamp']; c=interface['cage']
    if 'no replacement ribs' not in p['source']: raise RuntimeError('Direct density provenance required')
    if p['final_sha256']!=g['sha256'] or s['part_sha256']!=g['print_orientation_stl_sha256']:
        raise RuntimeError('Mixed candidate identities')
    mass=2*s['filament_g']
    bolt=10*math.ceil((2*d['ear_t']+d.get('split_gap',1.6)+2+2.4+3)/10)
    fine=grouped['native_fine_cases']
    screening=read(CASE/'fea/finished_cage_fea.json')
    screening_rows=screening['cases']
    screening_note=(f"予備解析は{len(screening_rows)}条件、格子"
        f"{sorted({row['voxel_mm'] for row in screening_rows})} mm、最大変位"
        f"{max(row['max_displacement_mm'] for row in screening_rows):.4f} mm。"
        "未達のネイティブ検査項目："
        +', '.join(sorted({q['name'] for row in screening_rows for q in row['checks'] if not q['pass']}))
        +"。単一格子の予備結果は収束済みの最終値として扱いません。")
    complete=v['all_original_native_fine_cases_present']
    stiffness=complete and all(q['pass'] for row in fine for q in row['checks'] if q['name']=='stiffness')
    numerical=v['numerical_strength_qualification_pass']
    displacement=max(row['max_displacement_mm'] for row in fine)
    status=('数値解析の強度・剛性・収束・独立解析を通過。実機の滑り・長期クリープ・造形ばらつきは未確認。'
            if numerical else '数値解析の総合認定は未完了。下記の収束・独立解析の未達を残しており、4 kg吊り下げ使用不可。')
    intro=f'''最適化密度を直接平滑化した3段連結クランプです。単純図形による梁・柱への置換は行っていません。

本体2個 **{g['PETG_mass_g_two_halves']:.2f} g**、実スライスのサポート等込み **{mass:.2f} g**。当初1516.08 gから{100*(1-mass/1516.08):.1f}%削減。同じ半割り2個、1個/プレート、1個{s['filament_g']:.2f} g・{s['print_time_text']}。

完成形状の細格子解析：最大変位 **{displacement:.3f} mm**、基準1 mmの判定 **{'PASS' if stiffness else '未達または全条件未完了'}**（{len(fine)}/{len(study['cases'])}条件）。**{status}**
'''
    table='\n'.join(f"| {row['case']} | {row['voxel_mm']:g} | {row['max_displacement_mm']:.4f} | {row['min_safety_factor']:.3f} | {row['safety_factor_p99_5']:.3f} |" for row in fine)
    cleanup=p.get('enclosed_density_void_cleanup')
    adopted=bool(p.get('native_compiled_csg_identical_after_default_adoption'))
    source_note=('正本はSCADと `spec/cage_density_surface.stl`。試案の `design_parameters.json` から既定値を採用する際、ネイティブOpenSCADのCSGが同一であることを検査。'
        if adopted else '未採用の候補です。形状はこのcaseの `finished_cage.stl`、入力パラメータは `design_parameters.json`。設計元の既定値とassemblyの印刷一式はまだ置換していません。')
    history_note=('採用前の部品と印刷一式はこのcaseの `before_native_stiffness/` に保持。' if adopted else
        '未採用のため、このcaseには採用前バックアップをまだ作っていません。現行の印刷一式はそのまま残っています。')
    cleanup_note=('密閉空洞の追加処理はありません。' if not cleanup else
        f"直接平滑化した密度メッシュの内側にある閉じた境界面を{cleanup['inward_shells_removed']}個除去しました。"
        f"内部に戻る材料は片側{cleanup['filled_volume_mm3']:.2f} mm³（元の体積の{100*cleanup['relative_volume_added']:.3f}%）です。"
        "外側の全三角形はSTL精度で完全一致を確認し、新しい梁・柱・CAD栓は作っていません。"
        "貫通穴は外側境界の一部なので対象外です。処理前のメッシュと検査はdensity_void_cleanup.jsonに記録し、完成形状を改めて解析しています。")
    detail=f'''# 直接平滑化・剛性改善設計（{date.today().isoformat()}）

{intro}

## 設計と条件

解析case：`{CASE.name}`。元の11荷重条件を維持し、全体の曲げ剛性を最適化へ反映する荷重増分7条件を追加。完成機4 kgを片側の吊り穴1個で負担、2g鉛直・1g横、3段50/25/25%の荷重分担、締付け150 N/本。増分条件は無締付けで摩擦保持できるという意味ではありません。

通常p99.5安全率3、異常1.5、最悪要素の絶対下限1.5、変位1 mm以下。材料はBambu PETG Basic暫定直交異方性カード、造形Y・ラスタZ。EPDMの硬度・接触圧力・摩擦係数は未同定で、線形構造解析が滑り試験を代替することはありません。

ねじ中心X=±{d['bolt_x']:g} mm、耳厚{d['ear_t']:g} mm。ゴム接触の固定領域幅{d['contact_width']:g} mm・肉厚{d['contact_preserve_t']:g} mm。その他の材料はネイティブ最適化で配分。取付ねじパターン36×16 mm、3段中心40/100/160 mm、容器Ø114.3 mm、EPDM自由厚1 mm・暫定圧縮後0.8 mmを保持。ドーム側上端かつ外部固定面側のØ{c['rope_hole_d']:g} mm吊り穴は半割りごとに1個。ロープ径は未指定です。

金具はM3×{bolt}全ねじ12本、ナット12個、OD12×1 mmワッシャ24枚。公称分割隙間{d.get('split_gap',1.6):g} mmを締め切らず、容器を支持した状態で3段左右を交互に調整。150 N/本は解析入力であり、推奨締付けトルクへの換算はしていません。

## 最適化と後処理

自由領域体積率{study['design']['volfrac']:g}、フィルタ{study['design']['filter_mm']:g} mm、MMA応力制約、X対称。終了理由は `{opt.get('termination_reason','not reported')}`。最大反復終了を収束とは呼びません。

抽出閾値{p['chosen_level']:g}、finish格子{study['finish']['voxel_mm']:g} mm、平滑化{study['finish']['smooth_mm']:g} mm。密度場の枝分かれを直接保持し、SCADで穴・座面・接触面のみ復元。穴入口0.3 mm、外縁0.6 mm、吊り穴入口1.2 mmの局所仕上げ。ねじを内側へ移す際にワッシャ通路を除外領域へ追加しています。

{cleanup_note}

{source_note} 出所は `{CASE.relative_to(PART).as_posix()}/final_provenance.json`。印刷一式には完成メッシュのみを含めます。

## 完成形状の解析

{screening_note}

| 条件 | 格子 mm | 最大変位 mm | 最悪安全率 | p99.5安全率 |
|---|---:|---:|---:|---:|
{table}

- 細格子の全条件検査：{v['native_fine_case_checks_pass']}
- 最悪要素安全率1.5以上：{v['worst_element_floor_1p5_pass']}
- ネイティブのメッシュ収束総合判定：{v['native_mesh_convergence_pass']}
- 独立CalculiXの3段階解析・収束：{v['ccx_native_pass']}
- 独立CalculiXの全条件で変位1 mm以下：{v.get('ccx_all_cases_stiffness_pass',False)}
- 独立解析とボクセル解析の全条件比較：{v['ccx_voxel_case_comparison_pass']}

収束の詳細は `grouped_convergence.json`、独立解析は `ccx_execution.json` / `ccx/ccx_summary.json`、集計は `validation_summary.json`。未実施・失敗・未収束を合格へ読み替えません。旧形状の解析値は転用していません。

## 印刷とCAD検査

Bambu PETG Basic、X1 Carbon、0.4 mmノズル、0.20 mm、100%インフィル、外周8・上下8層、255/70°C、外ブリム5 mm、ベッドからのツリーサポート。印刷STLはX90°回転済み。外形 {' × '.join(f'{n:.2f}' for n in g['print_extents_mm'])} mm。購入品とゴムは印刷しません。

閉メッシュ・1ボディ・密閉空洞0、ねじ・工具・ワッシャ通路、筒・フランジ・ドーム等との干渉、半割り間隙、造形枠を検査。`geometry_checks.json`、`hardware_checks.json`、`step_checks.json`、`slice_checks.json` を参照。未生成の検査ファイルは未実施です。配置金具・STEPを含む全CAD検査の集計：{v['digital_geometry_pass']}。

STEPは構造を単純図形へ再構成せず、有機面の三角形分割だけを削減した近似。双方向サンプル偏差0.10 mm以下、体積差0.5%以下、外形差0.10 mm以下を検査し、同じSCADで機能寸法を復元します。実値は `step_representation.json`。印刷STLと解析入力はこのSTEP近似に置換しません。

## 再現と履歴

`CHILD_CLAMP_CASE={CASE.name}`。準備は `tools/prepare_child_clamp_cage.py`、最適化と平滑化は `tools/run_child_clamp_cage.py`、完成形状検査は `tools/validate_child_clamp_candidate.py`。各コマンド・入力・native出力・終了コードをcaseに保持しています。

STEPは `tools/build_child_clamp_cage_step.py`。組立STEPは `tools/read_child_clamp_step_direct.py` の `assembly-export` と `assembly-check-heal-cots`、STLと画像は `build.ps1 -Assemblies assemblies/child_clamp_suspension -NoStep`。直接STEP読込みではクランプの形状を書き換えず、未確定境界の購入品だけをFreeCAD標準機能で修復して同じ配置検査へ通します。

{history_note} 過去の単純図形案は履歴であり現行へ昇格させません。
'''
    (CASE/'DESIGN_REPORT.md').write_text(detail,encoding='utf-8')
    if args.publish:
        if hashlib.sha256((PART/'child_wte4_suspension_clamp_cage.stl').read_bytes()).hexdigest()!=g['sha256']:
            raise RuntimeError('Publish only adopted STL identity')
        if not p.get('native_compiled_csg_identical_after_default_adoption'):
            raise RuntimeError('Missing native CSG identity proof')
        (PART/'LIGHTWEIGHT_REVIEW.md').write_text(detail,encoding='utf-8')
        (PART/'README.md').write_text('# WTE4子機・直接平滑化トポロジークランプ\n\n'+intro+'\n[設計と検証](LIGHTWEIGHT_REVIEW.md) / [EPDM調整](EPDM_ADJUSTMENT.md)\n',encoding='utf-8')
        (ASM/'README.md').write_text('# 子機外装・直接平滑化トポロジークランプ\n\n'+intro+'\n印刷入口：[parts/PRINT.md](parts/PRINT.md)。[設計と全検証](../../parts/child/exterior/printed/child_wte4_suspension_clamp/LIGHTWEIGHT_REVIEW.md)。配置はplacement.jsonが正本です。\n',encoding='utf-8')
        epdm=f'''# EPDM 1 mmと締付け調整

耳厚{d['ear_t']:g} mm、M3×{bolt}全ねじ12本・ナット12個・OD12×1 mmワッシャ24枚。自由厚1 mm・硬度不明、圧縮後0.8 mmと150 N/本の軸力は解析上の仮定であり、必要トルクや保証保持力を意味しません。

容器を支持して3段左右を少しずつ交互に調整し、ゴムのはみ出し・耳や容器の変形を確認。公称隙間{d.get('split_gap',1.6):g} mmを締め切らず、ねじ回転数を軸力へ換算しません。強く締めるほど安全になるとは限りません。

{status} [現在の検証](LIGHTWEIGHT_REVIEW.md)。旧形状の75/300 N感度解析は現行の許容範囲へ転用しません。
'''
        (PART/'EPDM_ADJUSTMENT.md').write_text(epdm,encoding='utf-8')
        config=read(ASM/'print_config.json')
        config['note']=intro+f'\nM3×{bolt}全ねじ12本・ナット12・OD12×1 mmワッシャ24。Bambu PETG Basic/X1C/0.4ノズル/0.20 mm/100%インフィル/外周8/上下8層/255-70°C/5 mm外ブリム/ツリーサポート。X90°回転済みSTLをそのまま配置。'
        config['notes']=[(PART/n).relative_to(ROOT).as_posix() for n in ['LIGHTWEIGHT_REVIEW.md','EPDM_ADJUSTMENT.md','BAMBU_PETG_BASIC.md']]
        save(ASM/'print_config.json',config)
        metadata=read(PART/'manufacturing.json')
        metadata['source_dependencies']=list(dict.fromkeys(metadata['source_dependencies']+['spec/topology_postprocess_policy.json']))
        save(PART/'manufacturing.json',metadata)
    print(intro)

if __name__=='__main__': main()
