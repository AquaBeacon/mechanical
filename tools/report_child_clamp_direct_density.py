"""Document measured directly smoothed density output without certifying strength."""
from pathlib import Path
import json
import re
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
ASM=ROOT/'assemblies/child_clamp_suspension'
CASE=analysis_case(PART)


def read(path): return json.loads(path.read_text(encoding='utf-8'))


def main():
    provenance=read(CASE/'final_provenance.json')
    if 'no replacement ribs' not in provenance['source']: raise RuntimeError('Not a direct density candidate')
    g=read(CASE/'geometry_checks.json')
    s=read(CASE/'slice_checks.json')
    f=read(CASE/'fea/finished_cage_fea.json')
    mass=2*s['filament_g']
    displacement=max(c['max_displacement_mm'] for c in f['cases'])
    failed_checks=sorted({q['name'] for c in f['cases'] for q in c['checks'] if not q['pass']})
    intro=f'''2026-10-05ユーザー指定に従い、**最適化密度を直接平滑化した形状**を現行に戻しました。リング・柱・梁への単純図形置換は行いません。前回の984.04 gの再構成案は履歴です。

本体2個のCAD体積換算は **{g['PETG_mass_g_two_halves']:.2f} g**、Bambu Studio実スライスのサポート等込み使用量は **{mass:.2f} g**（当初1516.08 gから{100*(1-mass/1516.08):.1f}%削減）。同一半割り2個、1個/プレート、1個{s['filament_g']:.2f} g・{s['print_time_text']}の予測です。

**exploration_only：形状確認用。4 kg吊り下げ使用不可。** 完成STLの2 mm格子・11条件再解析は最大変位{displacement:.3f} mmで基準1 mmを超過。この形状の収束解析・独立解析は未実施（粗格子で既に剛性未達）。実機の滑り/クリープも未確認です。前回の単純図形案の解析値を転用しません。
'''
    detail=f'''# 直接平滑化したトポロジー形状（2026-10-05）

{intro}

## 作り方と正本

- native最適化runは `{provenance['source_native_run']}`。volfrac0.20・100反復で最大反復終了（未収束）。荷重は完成機4 kg、2g、横1g、150 N/本の仮定締付け、全11ケースを保持。
- native extractの閾値0.4を採用し、finish格子1 mm・平滑化1 mmの保存済み出力を使用。元の有機的な部材・枝分かれを保持し、新しい梁や柱で再構成しません。
- `spec/cage_density_surface.stl` が平滑化した構造面。SCADの `cage_smooth()` はこれを読み込み、取付穴・座面・ゴム接触面・吊り穴だけを正確なCAD寸法へ復元し、設計領域外を切り取ります。穴入口0.3 mm、外縁0.6 mm、吊り穴入口1.2 mmの局所仕上げ。
- 密度場そのものは印刷用に配布しません。完成STLは元のSCADから再レンダリング・検査済み。出所とハッシュは `{CASE.relative_to(PART).as_posix()}/final_provenance.json`。
- 今後の制約はルートAGENTS.mdと `spec/topology_postprocess_policy.json` に保存。旧再構成の採用ツールはこの制約により停止します。

## 取合いと印刷

3段中心Z=40/100/160 mm、接触幅32 mm、容器Ø114.3 mm。EPDM自由厚1 mm・硬度不明、圧縮後0.8 mmは仮定。外部固定4穴×3段はX=±18 mm・Z=段中心±8 mm、外面Y=-84.95 mm。ドーム側上端・外部固定面側にØ10.5 mmの吊り穴を各半割り1個。ロープ径未指定の暫定寸法です。

この最適化runの元の耳厚24 mm・締付けボルトX=±85.95 mmを維持します。金具は **M3×60全ねじ12本、M3ナット12個、OD12×厚1 mmワッシャ24枚**。前回の再構成案のM3×70とは異なります。工具・穴・ワッシャ・容器との取合いを再確認し、placement.jsonを更新しました。

Bambu PETG Basic、X1 Carbon、0.4 mmノズル、0.20 mm、100%インフィル、外周8・上下8層、255/70°C、外ブリム5 mm、ベッドからのツリーサポート。印刷STLはX90°回転済み。造形外形は {' × '.join(f'{v:.2f}' for v in g['print_extents_mm'])} mm。スライス成功と実機造形成功は別です。

## 検査の範囲

閉メッシュ・1ボディ・材料内部の密閉空洞0、12本分の締付け経路、外部固定穴・工具経路・ワッシャ座、容器5部品との干渉、半割り間隙、造形枠を検査。`geometry_checks.json`、金具の `hardware_checks.json`、STEP照合の `step_checks.json`、`slice_checks.json` を同caseに保存。

STEPは有機面の三角形数だけを減らした近似面を使い、同じSCADで機能寸法を復元します。双方向サンプル偏差0.10 mm以下・体積差0.5%以下・外形差0.10 mm以下を検査し、実値は `step_representation.json` に記録。これは単純形状への再構成ではなく三角形分割の削減です。印刷STLと解析入力にはこの近似を使いません。

STEP読み戻しは `tools/read_child_clamp_step_direct.py` を使用。OCCTの読み込み時自動修復をこのプロセスだけ無効にし、書き出し形状を変更せずにFreeCADの妥当性・1ソリッド/1シェル・外形・体積の検査を実行します。検査条件は緩めていません。既定の自動修復を伴う読み戻しは15分以上CPU稼働が続いたため、合格した直接読み込みで置換し、記録を `default_step_read_superseded.json` と `direct_step_*.json` に残しました。ソフト本体やユーザー設定は変更していません。[OCCT公式のSTEP形状処理仕様](https://github.com/Open-Cascade-SAS/OCCT/blob/master/dox/user_guides/step/step.md)。

組立の曲面購入品は修復なしの読み込みで境界が未確定になる場合があり、初回は4点が配置検査NGでした。`assembly-check-heal-cots` モードでは、読み込んだ境界未確定の購入品だけにFreeCADの標準形状修復を行い、同じ配置検査を実行します。対象は容器筒・上下フランジ・底蓋・ドームで、実際の修復対象をJSONに記録します。クランプは修復・置換せず、期待値や元部品の形状を実測値の代わりに使いません。失敗した初回ログも保持します。

強度は不合格のままです。2 mm再解析は単一格子の診断であり収束済み最終値ではありません。今後は密度場の最適化条件や平滑化幅・閾値を調整し、その形状のまま再解析します。単純図形への置換で代用しません。

native出力で不合格の検査項目：{', '.join(failed_checks)}。薄い箇所を表現するメッシュ分解能も不足しており、粗格子での安全率を最終強度の根拠には使いません。

## 再現と履歴

元の最適化・抽出結果は上記runに保持。今回の再レンダリングは `tools/restore_child_clamp_density.py`、検証は `tools/verify_child_clamp_cage.py`、スライスは `tools/slice_child_clamp_cage.py --support tree`。case指定は `CHILD_CLAMP_CASE={CASE.name}`。再実行で履歴を上書きしません。

STEPは `tools/build_child_clamp_cage_step.py` で再生成・読み戻し検査。組立STEPには `tools/read_child_clamp_step_direct.py` の `CLAMP_DIRECT_STEP_MODE=assembly-export` と `assembly-check-heal-cots` を順に用い、`ASM_ROOT`・`CLAMP_DIRECT_CASE`・`ASM_JSON`・`STEP_OUT`/`STEP_IN` を対象の絶対パスで指定します。STLと4方向画像は `build.ps1 -Assemblies assemblies/child_clamp_suspension -NoStep` で更新します。`-NoStep` は、別経路で済ませたSTEP生成を重複させないための指定で、STEP検査を省略する意味ではありません。

前回のSCAD・STL・STEP・3MF・印刷説明は `{CASE.relative_to(PART).as_posix()}/before_direct_density/` に保存。旧独立解析の失敗記録も残しています。
'''
    (PART/'LIGHTWEIGHT_REVIEW.md').write_text(detail,encoding='utf-8')
    (PART/'README.md').write_text('# WTE4子機・直接平滑化トポロジークランプ\n\n'+intro+'\n[全検証・設計方針](LIGHTWEIGHT_REVIEW.md) / [EPDM調整](EPDM_ADJUSTMENT.md) / [印刷入口](../../../../../assemblies/child_clamp_suspension/parts/PRINT.md)\n',encoding='utf-8')
    (ASM/'README.md').write_text('# 子機外装・直接平滑化トポロジークランプ\n\n'+intro+'\n印刷入口は [parts/PRINT.md](parts/PRINT.md)。[設計と全検証](../../parts/child/exterior/printed/child_wte4_suspension_clamp/LIGHTWEIGHT_REVIEW.md)。配置の正本はplacement.json、購入品とゴムは印刷しません。\n\nM3×60全ねじ12本、ナット12、OD12×1 mmワッシャ24。EPDM自由厚1 mm・硬度不明。公称分割隙間1.6 mmを締め切らず、容器を支持して3段左右を交互に調整します。必要トルク・許容軸力は未確定です。\n',encoding='utf-8')
    (PART/'EPDM_ADJUSTMENT.md').write_text('''# EPDM 1 mmと締付け調整

現行は直接平滑化した密度形状。耳厚24 mm、M3×60全ねじ12本・M3ナット12個・OD12×1 mmワッシャ24枚。自由厚1 mm・硬度不明、圧縮後0.8 mmと解析の150 N/本は仮定です。必要トルクや保持力を意味しません。

容器を支持して3段左右を少しずつ交互に調整し、ゴムのはみ出し・耳と容器の変形を確認します。公称隙間1.6 mmを締め切らず、ねじ回転数を軸力へ換算しません。強く締めるほど安全になるとは限りません。

形状の剛性は不合格で、吊り下げ使用不可。湿潤滑り・接触圧力・PETGの長期クリープは未評価です。[現在の検証記録](LIGHTWEIGHT_REVIEW.md)を参照。旧75/300 N感度解析は旧形状の履歴として_work/analysis内に保存し、現行の推奨値には転用しません。
''',encoding='utf-8')
    config=read(ASM/'print_config.json')
    config['note']=f'**直接平滑化トポロジー・形状確認用。4 kg吊り下げ使用不可。** 2個合計{mass:.2f} g（ツリーサポート等込み予測）。M3×60全ねじ12本、ナット12、OD12×1 mmワッシャ24。EPDM自由厚1 mm・硬度不明。3段連結、指定側Ø10.5 mm吊り穴2個。Bambu PETG Basic・X1C・0.4ノズル・0.20 mm・100%インフィル・外周8・上下8層・255/70°C・5 mm外ブリム。X90°回転済みSTLをそのまま使い、1個/プレート。完成形状の粗格子解析で最大変位{displacement:.3f} mm、基準1 mm超過。収束・独立解析・実機試験は未合格。'
    config['notes']=[(PART/n).relative_to(ROOT).as_posix() for n in ['LIGHTWEIGHT_REVIEW.md','EPDM_ADJUSTMENT.md','BAMBU_PETG_BASIC.md']]
    (ASM/'print_config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    metadata=read(PART/'manufacturing.json')
    metadata['source_dependencies'].append('spec/topology_postprocess_policy.json')
    metadata['source_dependencies']=list(dict.fromkeys(metadata['source_dependencies']))
    metadata['note']=metadata['note'].split(' Direct native density smoothing with exact functional CAD interfaces.')[0]
    metadata['note']+=' Direct native density smoothing with exact functional CAD interfaces. User prohibits primitive reconstruction.'
    (PART/'manufacturing.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Documented direct density: {mass:.2f} g; native max displacement {displacement:.3f} mm (FAIL)')


if __name__=='__main__':main()
