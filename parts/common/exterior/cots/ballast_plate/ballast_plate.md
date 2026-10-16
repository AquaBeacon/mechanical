# 所有バラスト：おもりA・B（設計用モデル）

2026-09-27、ユーザー提供写真と会話で確認した実物の配置・取合い確認用CAD。
購入品/COTS扱い。3Dプリント用の代替おもりではない。
初回登録（2026-09-27）時点では使用assembly・必要個数・材質は未指定。現在の子機4枚フレームでの採用は末尾の採用節を参照。
質量はユーザー申告（2026-09-27）：**おもりA=60 g/個、おもりB=60 g/個**。
今後「おもりA」「おもりB」は以下の対応モデルを指す。体積から推定した質量ではない。
全バラストの名称・質量・モデル対応は `../ballast_inventory.json` と `docs/部品一覧.md` を参照。

| バリアント | 出力名 | 長さX | 幅Y | 厚さZ | 穴 |
|---|---|---:|---:|---:|---|
| A | ballast_plate_a.step / .stl | 142 | 19 | 4 | なし |
| B | ballast_plate_b.step / .stl | 163.5 | 16 | 3 | M5ボルト用貫通穴4個、ねじ山なし |

単位mm。原点は底面中心。Xが長手、Yが幅、Zが厚さ。底面Z=0。
Bの穴軸はZ方向、中心Y=0（幅方向の端から8）。
左端からの穴中心Xは20、57.5、106、143.5。
モデル座標Xは-61.75、-24.25、24.25、61.75。
穴間隔37.5、48.5、37.5、両端オフセット20。全長との一致をSCADで検査する。

## 仮値と簡略化

ユーザー確認済みなのはM5ボルトを通す貫通穴という用途。実際の穴径は未計測。
`b_hole_d_provisional=5.5` mmを設計用の仮値として採用した。
実取付穴を確定する場合は実物を測り、この変数を更新して再ビルドする。
タップ・座ぐり・皿もみは作らない。角丸・面取りの寸法は未提供のため、外形は直方体とする。
FDM用の穴径補正、収縮補正、象足対策は適用しない。
質量・重心・浮力・強度をこのモデルの材質や体積から確定しない。

## 原本と再生成

寸法原本：`ref/IMG_4263.HEIC`（穴図）、`ref/IMG_4264.HEIC`（A/B寸法）。
画像内のその他のスケッチは今回のモデル対象ではない。
正本は `ballast_plate.scad`、`variants.txt`でA/Bを選択する。

```powershell
.\build.ps1 parts\common\exterior\cots\ballast_plate
# STEPを読み戻して寸法・体積・4穴の円筒面を検査
& 'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe' tools\verify_ballast_plate.py
```

再生成ログと検査結果は `_work/logs/`、プレビューは `_work/images/`。
SCADの `use` で `ballast_plate(length,width,thickness,hole_x_from_left,hole_d)` を再利用できる。
assembly登録時は `part` にこの部品フォルダ、`file` にA/Bの出力ファイルを指定する。

## 検証結果（2026-09-27）

OpenSCADレンダリング、STL閉メッシュ、STEP単一ソリッド・有効形状を確認。
STEP/STLの外形・原点・体積を照合。AのSTEP体積10792 mm³、Bは約7562.90047 mm³。
BのSTEP円筒面を読み戻し、4穴の中心・半径2.75・Z方向・厚さ全体の貫通を確認。
上面と4方向のプレビューを生成。部品単体の形状検査は合格。
実物の穴径、相手部品との干渉、ボルト・工具の通路は取付先未指定のため未検証。

管理ツール9テストと `tidy_workspace.py check` は合格。
全体ビルドの印刷同期・全体 `assembly_parts.py check` は既存の別構成の指摘で未合格：
`child_interior` / `child_vertical_assembly` のCAD・印刷データ不一致、
`child_interior` の管理外3MF、`dji_style_toggle_latch` のmanifest未作成。
このCOTSモデルは上記構成へ追加されておらず、印刷一式の対象でもない。
詳しい出力は `_work/logs/build.log` と `assembly_parts_check.log` に保持。

## 子機4枚フレームでの採用（2026-10-09）

`child_horizontal_plate_frame` の細長い錘はユーザー指定によりBのみ4個。各4穴にM5×12を通し、下面のAF8×厚4ナットへ固定する。配置はassemblyのplacement.jsonが正本。共通のB形状と申告質量60 gは変更しない。4穴位置はSTEPから取合いSCADへ抽出する。実穴径は引き続き未計測。
