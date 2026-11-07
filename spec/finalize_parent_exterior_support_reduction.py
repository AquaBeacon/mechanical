"""Publish design/print notes only from the final revision's passing evidence."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
W=A/'_work/analysis/support_reduction'

def main():
    geometry=json.loads((W/'geometry_checks.json').read_text(encoding='utf-8'))
    steps=json.loads((W/'step_checks.json').read_text())
    audit=json.loads((W/'slice_audit.json').read_text())
    assert all(r['passed'] for r in (geometry,steps,audit))
    assert all(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest()==r['sha256'] for r in geometry['meshes'])
    production=json.loads((A/'print_jobs/support_reduction/validation.json').read_text())
    detection=json.loads((W/'support_detection/validation.json').read_text())
    assert len(production)==11 and all(r['passed'] and r['bed_fits'] and r['support_filament_mm']==0 for r in production)
    frame=next(r for r in production if r['file']=='parent_oneplate_frame.stl')
    residual=[r for r in detection if r['support_filament_mm']>0]
    assert {r['file'] for r in residual}<={'camera_mount.stl','parent_oneplate_stand.stl','parent_oneplate_camera_qr_female.stl','parent_oneplate_camera_qr_male.stl'}
    table='\n'.join(f"| {r['file']} | {r['support_filament_mm']:.1f} | 0 |" for r in residual)
    seconds=frame['seconds'];hour=int(seconds//3600);minute=round(seconds%3600/60)
    tail=f'''## 印刷と再生成

印刷一式は11種類14個。[parts/PRINT.md](parts/PRINT.md)と同フォルダのSTLを使用する。旧緑色4部品を単独印刷しない。STLには印刷姿勢を反映済み。主プレートは下面Z=-20を下、TD支持はY=-90°、角度ストップはX=-90°。脚はY=90°、その他は製造メタデータに従う。組立の回転を重ねない。

PETG Basic・X1 Carbon・0.4 mm、0.2 mm層・8壁・100%充填。QRは0.1 mm層。ブリムは主プレート2 mm、TD支持6 mm、他3 mm。主プレートは3 mmだとBambuの自動配置で前側の押出がベッド外へ出るため2 mmにし、実経路を再検査した。camera_mountは上記の専用条件（Generic PETG・6壁・15% Gyroid）を優先する。ブリムは支持材とは別に付く。

**現行3MFはprint_jobs/support_reduction/の各部品フォルダ。全11種類で実G-codeの支持材押出0を確認した。** 主プレート・TD支持・角度ストップを含む7種類は自動支持を有効のまま使用する。自動検出は45°、モデル上の支持も許可して検査した。旧universal_plate、bolt_on_plate、qr_standing等の3MFは履歴で現行へ流用しない。

カメラ本体・脚・QRの4種類には、自動検出すると次の小さな候補が残る。機能形状を維持し、最大4.2 mmの短い橋渡し・45°の縁を実経路で確認したうえで、製造用3MFではサポートなしにしている。「自動検出でも0」の部品と同じ扱いにはしない。実印刷の橋品質・定着は未確認。

| 部品 | 自動検出時の支持フィラメント / mm | 製造用支持 / mm |
|---|---:|---:|
{table}

自動検出を有効にした全11種類の3MF・設定・結果は[_work/analysis/support_reduction/support_detection/](_work/analysis/support_reduction/support_detection/)へ保存。製造用と同じSTLハッシュで照合した。自動検出の出力を隠して全品を形状だけで支持不要と認定するものではない。

![印刷姿勢](_work/images/support_reduction_print_poses.png)

![最初の層と穴屋根の実経路](_work/images/support_reduction_detail_layers.png)

主プレートの見積りは{frame['grams']:.1f} g・約{hour}時間{minute}分。Rev.5の支持込み898 g・18時間53分から、約{898-frame['grams']:.1f} g減少。同じX1C/PETG Basic・層厚・壁数・充填で、ブリムは3→2 mmへ変更したスライサー見積りであり実測値ではない。

正本はspec/prepare_parent_oneplate.py、spec/parent_oneplate_frame_sources.py、spec/parent_oneplate_sensor_sources.pyと既存revision_sources・共通SCAD。部品をビルドしてからtools/assembly_parts.py sync parent_exteriorを実行する。STEPは既存scad/lib/stl_to_step.pyのSTL_IN/STEP_OUTで現行STLから再生成する。角度ストップはmanufacturing.jsonに従いtools/compact_coplanar_mesh.pyを先に使う。spec/verify_parent_exterior_qr_steps.pyをPARENT_REVISION=support_reductionで実行する。STEPは形状交換用で設計履歴の正本ではない。

検証入口はspec/verify_parent_exterior_support_reduction.py。スライスはspec/slice_parent_exterior_support_reduction.py --detect-onlyを先に実行してから、同じスクリプトを引数なしで実行する。保存結果の監査はspec/review_parent_exterior_support_reduction.py、文書更新はspec/finalize_parent_exterior_support_reduction.py。旧配置移行スクリプトは現行へ実行しない。

## 現行形状の検証結果

閉メッシュ・単一連結、native判定の不正辺/縮退0。組立部品と金具同士の意図しない干渉0。予備15箇所の実穴・ナット座・厚7 mm/径12 mm治具・M4x25先端と工具通路、三点基準、TD左/上基準、12 mmの端面腕を検査した。ロープ4箇所は径10.4 mmの上下通過を脚・箱・金具込みで確認し、面取り付近の肉厚も実メッシュのレイ交差で確認する。QRの5°刻み60°回転・80 mm抜去と横ボルト45 mm抜去も合格。

[幾何検査](_work/analysis/support_reduction/geometry_checks.json)、[部品STEP照合](_work/analysis/support_reduction/step_checks.json)、[製造用スライス](print_jobs/support_reduction/validation.json)、[保存3MF・実経路監査](_work/analysis/support_reduction/slice_audit.json)。部品STEP11種類は単一有効ソリッドで外形・体積がSTLと一致。全体はparent_exterior.step/.stl、構造別名はparent_oneplate_structure.step。配置93部品の照合結果は_work/logs/support_reduction_assembly_build.logを参照する。

変更前のRev.5設計元・部品・配置・説明は[history/](_work/analysis/support_reduction/history/)に保存。実印刷、実ケース/金属ブラケットの仮寸法、ケーブル、締結、強度・クリープ・浮力は未認定。サポート量の削減を強度試験の代用にはしない。

対象の印刷一式の出所・個数とファイル配置を検査する。対象外の既存構成には未管理3MF・出所不整合が残る。共通テストは42件中41件合格、既存child_wte4_suspension_clampの材料JSON欠落1件でエラー。ログは_work/logs/support_reduction_global_parts_check.log、support_reduction_unittest.log、support_reduction_tidy_check.log。
'''
    path=A/'README.md';source=path.read_text(encoding='utf-8').split('## 印刷と再生成')[0]
    path.write_text(source+tail,encoding='utf-8')
    summary=dict(passed=True,assembly_items=93,printed_types=11,printed_pieces=14,spare_M4_holes=15,
                 primary_auto_support_free=audit['primary_support_free'],all_production_support_free=audit['all_production_support_free'],
                 all_detector_support_free=audit['all_detector_support_free'],residual_detection=residual,
                 frame_grams=frame['grams'],frame_seconds=seconds,physical_print_verified=False)
    (W/'validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print('Published Rev.6 notes:',frame['grams'],'g',seconds,'s; physical print unverified')

if __name__=='__main__':main()
