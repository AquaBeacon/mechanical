# WTE4 アクリルチューブ (4" / 100mm シリーズ)

購入品 (COTS)。AquaBeacon 子機の耐圧容器 本体。

| 項目 | 値 |
|---|---|
| 区分 | 子機 / 外装 / 購入品 |
| メーカー | Blue Robotics |
| 型番 | BR-101052-200 / -300 / -400 |
| 製品ページ | https://bluerobotics.com/store/watertight-enclosures/wte-vp/ |
| 材質 | キャストアクリル (透明) |
| 使用数 | 1 (300mm を主用途。200/400 も所持) |

## 寸法・仕様 (メーカー公称)

| 長さ | 型番 | 質量 | 耐圧深度 |
|---|---|---|---|
| 200 mm | BR-101052-200 | 488 g | 140 m |
| 300 mm | BR-101052-300 | 746 g | 100 m |
| 400 mm | BR-101052-400 | 1004 g | 60 m |

- 内径 ID **101.6 ± 2.1 mm**
- 外径 OD **114.3 ± 0.8 mm**
- 両端に O リング当たり面が精密加工されている。端部にロッキングコード用のグランドと
  差込みスロットがあり、これがフランジとの**回り止め**も兼ねる。

## 実モデルからの実測 (このフォルダの STL)

| ファイル | バウンディングボックス | 体積 |
|---|---|---|
| `BR-101052-200_RevB.stl` | 200.00 × 114.24 × 114.18 mm | 405.5 cm³ |
| `BR-101052-300_RevB.stl` | 300.00 × 114.22 × 114.15 mm | 620.2 cm³ |
| `BR-101052-400_RevB.stl` | 400.00 × 113.91 × 114.30 mm | 827.3 cm³ |

**端部の座ぐり (STL を X でスライスして実測)**: 両端から **深さ約 20mm、Ø104.2**
に座ぐられている。ここに `wte4_flange` のピストン (Ø104 × 19) が入り、
ロッキングコードで固定される。中央部の内径は 101.5〜101.7 (= 公称 101.6)。

STL/STEP とも **軸 = X (0..長さ)、断面中心 = (57.15, 57.15)**。
アセンブリでは `rotate([0,0,90])` で軸を Y へ倒している (`assemblies/child_assembly/placement.json`)。

**STEP の座標系について (2026-09-02)**: ベンダ配布の STEP (`ref/` の zip 内) は
STL と違い **軸 = X (-長さ..0)、断面中心 = (0, 0)** で、placement.json (STL 基準) で
合成したアセンブリ STEP だけチューブが X 0..115 / Z -200..0 にずれていた。
このフォルダの `.step` は原本を `scad/lib/step_reframe.py` で STL 側へ
**(+長さ, +57.15, +57.15) 平行移動して書き直したもの** (STL 頂点→STEP 表面距離 0.000 mm で一致確認)。
原本は `ref/` の zip のまま。再生成するときは:

```powershell
$env:STEP_IN="<zip を展開した BR-101052-200_RevB.STEP>"; $env:STEP_OUT="parts\child\exterior\cots\wte4_acrylic_tube\BR-101052-200_RevB.step"
$env:TRANSLATE="200,57.15,57.15"; $env:STL_REF="parts\child\exterior\cots\wte4_acrylic_tube\BR-101052-200_RevB.stl"
& "C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe" scad\lib\step_reframe.py
```
(300 / 400 は TRANSLATE の第 1 成分を長さに合わせる)

## この寸法に依存している自作部品

| 部品 | 依存している値 |
|---|---|
| `child_clamp_base` / `child_clamp_strap` | `tube_od = 114.3` + `fit_clear 0.5` |
| `child_frame_plate` | クランプ中心 y = ±60 (チューブ長 300 前提) |
| `child_tray_deck` / `child_tray_rib` | フランジ貫通口 Ø88.5 (チューブ内径ではない) |

## 部品外の考慮

- **チューブ保護**: クランプのサドル面に薄ゴム/EVA シートを貼ること
  (アクリルへの点当たりでクラックが入る)。締め代はシート圧縮で確保する。
- **有効内長**: チューブ長 300 に対し、両端のフランジ挿入分とキャップのプラグ分だけ
  内部が短くなる。トレイ長 `tray_len` はこの**有効内長の実測待ち**(現状 281 は仮値)。
- **配線は後方キャップ側に集約**。前端(+Y)側はケーブル余裕ゾーン 30mm のみ。
- アクリルは有機溶剤・強アルカリで白化/クラックする。清掃は中性洗剤か水のみ。

## 要確認

1. 有効内長 (フランジ+キャッププラグ込み) の実測 → `child_tray_deck.tray_len` 確定
2. 使用する長さの最終決定 (現状 300mm 前提で全部品を設計)

## 出典

- [Watertight Enclosure — Blue Robotics](https://bluerobotics.com/store/watertight-enclosures/wte-vp/)
- 元配布データ: `ref/WTE4_ACRYLIC_TUBES_BR-101052-XXX.zip`
