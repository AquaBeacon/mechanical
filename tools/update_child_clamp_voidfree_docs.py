"""Document the void-free CAD revision without changing historical analysis."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
ASSEMBLY = ROOT/'assemblies/child_clamp_suspension'
CASE = PART/'_work/analysis/connected_cage_rubber1_solid'
ORIGINAL = PART/'_work/analysis/connected_cage_rubber1_v065'


def main():
    revision = json.loads((CASE/'void_free_revision.json').read_text(encoding='utf-8'))
    geometry = json.loads((CASE/'geometry_checks.json').read_text(encoding='utf-8'))
    sliced = json.loads((CASE/'slice_checks.json').read_text(encoding='utf-8'))
    if not geometry['no_enclosed_material_cavities'] or not geometry['pass'] or not sliced['pass_check']:
        raise RuntimeError('Void-free geometry and actual slice must pass before updating current documentation')
    dimensions = ' × '.join(f'{v:.2f}' for v in geometry['print_extents_mm'])
    part_text = f'''# WTE4子機・密閉空洞のない3段連結クランプ

2026-10-02: 既存の最適化結果にあった材料内部の密閉空洞1個を埋めました。**再最適化・FEA・CalculiXは開始していません。** 外表面と外形は維持し、同じ設計元SCADで再生成。完成STLは1物理ボディ・1境界シェルで、密閉空洞0個です。追加材料は{revision['added_volume_mm3']:.3f} mm³、PETG約{revision['added_volume_mm3']*.00125:.3f} g/半割りです。

3段を連結した同じ半割りケージ2個で既存WTE4を囲みます。ゴム自由厚1 mm、圧縮後0.8 mmは仮定。固定4穴の面側上端にØ10.5 mmの吊り穴を各半割り1個残しています。容器空間・M3穴・工具/ワッシャ通路・吊り穴は開放した機能空間で、中実化の対象ではありません。

印刷入口は [PRINT.md](../../../../../assemblies/child_clamp_suspension/parts/PRINT.md)。X90°回転済み、外形{dimensions} mm、同じSTLを2個、1個/プレート。Bambu PETG Basic、100%インフィル、外周8、上下8層、0.20 mm、0.4 mmノズル、5 mm外ブリム、ベッドからのサポートです。現在の実スライス予測は{sliced['print_time_text']}・{sliced['filament_g']:.2f} g/個。実機の印刷成功を確認したという意味ではありません。

**exploration_only: 吊り上げ使用の強度認定は未完了。** 変更前の形状は偏荷重変位1.079 mm > 基準1 mm、独立解析はメッシュ生成で停止。中実化後の形状は構造再解析していないため、旧数値を新形状の評価値として転用しません。

- [初期モデル・全材料定数・全荷重/支持条件・最適化設定](OPTIMIZATION_INPUTS.md)
- [変更前のトポロジー最適化と解析記録](CAGE_TOPOLOGY.md)
- [組立と配置](../../../../../assemblies/child_clamp_suspension/README.md)

現在の設計は同じSCADと `spec/cage_density_surface.stl`（内側境界を除去済み）が正本。変更記録は `_work/analysis/connected_cage_rubber1_solid/void_free_revision.json`。変更前の原本・STEP・配置・文書は旧caseの `before_closed_void_fill/` へ保存しました。工具座の機能段差は保持しています。

再最適化を伴わない再生成:

```powershell
$env:PYTHONIOENCODING="utf-8"
python tools/remove_child_clamp_cage_voids.py
$env:CHILD_CLAMP_CASE="connected_cage_rubber1_solid"
python tools/verify_child_clamp_cage.py --require-no-closed-voids
python tools/slice_child_clamp_cage.py
python tools/package_child_clamp_cage.py
python tools/update_child_clamp_voidfree_docs.py
python tools/assembly_parts.py sync child_clamp_suspension
python tools/assembly_parts.py check child_clamp_suspension
```

STEPは `tools/export_child_clamp_voidfree_step.py` を既存FreeCAD CLIとASM_ROOT環境変数で実行して生成します。部品/組立の読戻しは既存のverifyスクリプトで行い、新caseへログを保存します。独立強度解析の合格を意味しません。
'''
    (PART/'README.md').write_text(part_text,encoding='utf-8')
    historic = (ORIGINAL/'before_closed_void_fill/part/CAGE_TOPOLOGY.md').read_text(encoding='utf-8')
    (PART/'CAGE_TOPOLOGY.md').write_text('''> 現在は2026-10-02の密閉空洞除去版です。以下の数値・解析は2026-10-01の変更前形状の履歴で、新形状の構造評価値ではありません。今回は再最適化・構造再解析を行っていません。全入力説明は [OPTIMIZATION_INPUTS.md](OPTIMIZATION_INPUTS.md)、現行の形状/印刷条件は [README.md](README.md) を参照してください。

'''+historic,encoding='utf-8')
    (ASSEMBLY/'README.md').write_text(f'''# 子機外装・WTE4の密閉空洞のない3段連結クランプ

2026-10-02: 既存最適化形状の材料内部にあった密閉空洞を埋めました。再最適化・構造再解析は実行していません。1物理ボディ・1境界シェル・密閉空洞0個を検査し、外形と取付穴を維持しています。

同じ半割りケージ2個で既存WTE4（Ø114.3×200 mm）を囲みます。ゴム1 mm（圧縮後0.8 mmは仮定）、バンド中心Z=40/100/160 mm、幅32 mm。固定4穴面側の上端にØ10.5 mmのロープ穴を計2個。M3×60は12本、ナット12個、OD12ワッシャ24枚、ゴム半周6枚です。

印刷入口は [parts/PRINT.md](parts/PRINT.md)。X90°回転済みSTL、{dimensions} mm、1個/プレート、同じ半割り2個。Bambu PETG Basic、255°C/70°C、100%インフィル、外周8、上下8層、0.20 mm、0.4 mmノズル、5 mmブリム、ベッドからのサポート。実スライス予測は{sliced['print_time_text']}・{sliced['filament_g']:.2f} g/個です。

**exploration_only: 吊り上げ使用の強度認定は未完了。** 旧形状は偏荷重変位1.079 mmが1 mm基準を超過し、独立メッシュ生成も停止。中実化後の構造再解析は未実施で、旧数値を新形状へ転用しません。4 kg完成機・2g・締付け150 N/本は前回の仮入力です。

- [初期モデルと全解析入力](../../parts/child/exterior/printed/child_wte4_suspension_clamp/OPTIMIZATION_INPUTS.md)
- [現行設計元と空洞除去記録](../../parts/child/exterior/printed/child_wte4_suspension_clamp/README.md)
- [配置の正本](placement.json) / [組立STEP](child_clamp_suspension.step)

工具/内側ワッシャを使う場合は、ゴムと容器を入れる前に取り付けます。材料内部の密閉空洞を埋める変更であり、容器の収納空間や機能穴は塞いでいません。
''',encoding='utf-8')
    index = ROOT/'docs/部品一覧.md'
    text = index.read_text(encoding='utf-8')
    text = '\n'.join('子機の新外装用（2026-10-02）: [WTE4の密閉空洞のない3段連結M3/PETGクランプ](../parts/child/exterior/printed/child_wte4_suspension_clamp/README.md)。半割り2個、ゴム1 mm、固定4穴面側上端のØ10.5吊り穴2個。既存最適化の内部密閉空洞を埋め、再最適化は未実施。[全解析入力](../parts/child/exterior/printed/child_wte4_suspension_clamp/OPTIMIZATION_INPUTS.md)。exploration_only、変更後の構造再解析・実機印刷・吊り上げは未認定。' if '子機の新外装用' in row and 'child_wte4_suspension_clamp' in row else row for row in text.splitlines())+'\n'
    index.write_text(text,encoding='utf-8')
    print('Updated current void-free documentation; original analysis figures remain explicitly historical.')


if __name__=='__main__':
    main()
