# 親機バッテリーボックス：子機の端フック＋ねじ1本

2026-10-12。子機内装の現行 `child_vtray_batt_floor.scad` と `child_vtray_batt_box.scad` を参照し、親機の蓋を2本の端フックで差し込み、反対側のねじ1本で固定する構造にした。子機の部品は変更していない。

## 操作

1. 電池とリードを収め、上面フォームを確認する。
2. 蓋を取付位置から南2 mm（ボックス局所−X）へずらして下ろす。
3. 北へ2 mm滑らせ、端の2本のフックを受けスロットへ差し込む。
4. 既存位置のM3×12ねじとM3ナットを各1個使って締める。

開くときは電源を切りリードを外し、ねじ1本を外す。蓋を南2 mm戻し、上へ持ち上げて電池を抜く。フックを弾性変形させる操作は不要。蓋の移動経路へ配線を固定しない。

## 形状と取合い

- フックの厚さ1.3・高さ3・差込み長2・根元長4 mm、片側すきま0.3 mm、端すきま0.5 mmを子機の現行SCADから直接読み込む。子機の5点断面と45°の差込み先端を親機の蓋面へ回転して用いる。
- フック2本は電池の外側、側壁の内側に配置。端壁に2本の貫通スロットを設け、スロット上の屋根厚は2.2 mm。蓋の長端は局所X104、フック先端X106、箱端X107 mm。
- 子機のM3×10皿ねじに対し、親機は既存ねじ座に合わせM3×12とM3ナットを使用する。ねじ位置は局所(12,5)。残る3本の蓋ねじ・ナットは使用しない。
- 蓋外周とフックを0.1 mm、ねじ穴入口とスロットの上下口縁を0.15 mm面取り。スロットの縦の案内稜と内部角は嵌合断面を維持する。蓋配線側の東角は6 mmの斜め逃げで容器コーナーを避ける。
- 蓋下面Z49・上面Z52、電池下面Z23、床厚3 mm、最大パック104×36×25 mmの剛体包絡、既存フォーム4枚を維持。フォームは実電池に合わせて調整する。
- 配線端40×26 mm全面開口、容器固定ねじ用Ø4.2工具穴を維持。最下段 `floor_plate` のSCAD・STEP・STL、MAIN固定板、子機の参照部品は変更前と同一SHA-256。

参照元のSHA-256は `battery_slide_lid_checks.json` に記録する。共通 `scad/lib/parent_battery_slide.py` が子機寸法と親機の取合いを結び、既存の電池台・蓋生成スクリプトから呼び出される。

## 印刷

**再印刷は `battery_base` と `parent_lipo_retainer_lid_slide` を各1個。** 印刷入口は [parts/PRINT.md](parts/PRINT.md)。印刷一式は9種類各1個を維持する。

PETG、X1Cの0.4 mmノズル、0.2 mm積層、4周壁、100%インフィル。電池台は従来姿勢、蓋は平らな上面をベッドへ向けるX180°。同梱STLは変換済み。サポート有効・45°閾値・ブリッジ除外で実形状をスライスした。

電池台は約45.66 g（支持約0.93 g）、蓋は約21.12 g（支持約0.04 g）。スロットとフック付近の少量の支持を側方から除去し、フック・溝・ナット座・工具穴のバリを確認する。現物での支持除去と嵌合は未検証。

## 検証

[battery_slide_lid_checks.json](battery_slide_lid_checks.json) の15項目PASS。実配置の干渉、2 mmの連続スライド、解除後の連続上抜き、2本のフックの直接持上げに対する掛かり、ねじによるスライド阻止、最大電池包絡、最下段の不変、配線開口を確認した。

子機の端すきまとスロットすきま、45°入口には公称約0.8 mmと面取り分の上下遊びがある。各フックを直接1.5 mm上げた位置で屋根との正の交差を確認し、解除せず上へ抜けない幾何学的保持を検査した。強度試験ではない。

面取り済みの実蓋を包む構成要素を使い、凸な平面輪郭を連続移動させたプリズムで経路を検査する。電池／microSDは `battery_sd_access_checks.json`、容器固定ねじ3本は `case_screw_access_checks.json`。14個の現行印刷メッシュの閉鎖・STEPとの外形／体積一致を確認し、変更2部品をOpenSCADで独立レンダリングした。閉状態と箱外状態の組立STEPを再生成して配置を照合する。集約は `validation_current.json`。

PETGの実嵌合、繰返し摩耗、実フォーム・リード、ねじ1本の締付けと波浪・落下・クリープは未検証。試作で操作を確認する。全体検査に残る今回と無関係の既存不備は `validation_current.json` に記録する。

確認画像は `_work/images/battery_slide_lid_closed.png`、`battery_slide_lid_released.png`、`battery_slide_lid_open.png`、`battery_slide_lid_section.png`。解析・スライス・変更前の原本は `_work/analysis/battery_child_reference_20261012/` に保持。

## 再生成

既存FreeCAD 1.0の `bin/python.exe` で `spec/build_parent_hand_service.py --battery-only`、`spec/export_parent_lipo_retainer.py --slide-lid-only`、`spec/refresh_parent_case_screw_meshes.py --battery-child-reference` を順に実行。通常Pythonで `spec/slice_parent_simple_stack.py --battery-child-reference after battery_base parent_lipo_retainer_lid_slide` と `spec/render_parent_battery_slide_lid.py --render` を実行する。

配置正本は `placement.json`、箱外確認は `service_placement.json`。既存 `scad/lib/asm_to_step.py` を `ASM_ROOT`・`ASM_JSON`・`STEP_OUT` で呼び、両STEPを更新する。最後に `tools/assembly_parts.py sync parent_hand_service`／`check parent_hand_service` を実行する。
