# 親機内装スペーサの印刷データ（2026-10-22）

印刷入口は [parts/PRINT.md](parts/PRINT.md)。MAINを含む独立スペーサ全12本を、5種類のSTLとして取り出せるようにした。取付座標・基板高さ・金属ねじは既存設計のまま。Sony右の下端だけ着座改善を行った。旧ランナーにもMAIN柱4本は含まれていたが、単体STLが印刷一式になく、部品一覧の説明もSony/GNSSの8本のまま残っていた。

| 取付先 | 同梱STL | 数量 | 本体高さ＋位置決め突起 | 外形／通し穴 |
|---|---|---:|---|---|
| MAIN固定板の下 | `main_corner_column.stl` | 4 | 14.3＋0 mm | Ø7／Ø3.45 mm |
| Sony固定板の西側 | `sony_column_left.stl` | 2 | 41.7＋0.8 mm | Ø7／Ø3.45 mm |
| Sony固定板の東側 | `sony_column_right.stl` | 2 | 41.7＋0.8 mm | 軸Ø5.4、下端5×9×高さ1.2／Ø3.45 mm |
| GNSS台の南側 | `gnss_column_front.stl` | 2 | 31.2＋0.8 mm | 9×9／Ø3.45 mm |
| GNSS台の北側 | `gnss_column_rear.stl` | 2 | 31.2＋0.8 mm | 8×6／Ø3.45 mm |

**表の12本を印刷したら、旧 `parent_stack_spacer_set.stl` は追加印刷しない。** 旧セットをすでに印刷した場合はSony右2本を新版へ交換し、他は欠品だけを補充する。現在の内装一式は13種類20個。スペーサ以外の8部品は各1個。

Sony右の旧Ø5.4 mm柱は床の開放M3ナット穴より細く、床との最短距離が0.25 mmあった。下端をY方向に9 mmへ広げ、穴の両端へ着座させる。足幅5 mm、厚さ1.2 mm、全体X外形5.4 mm、全高42.5 mm。東壁に向かうX幅、上のキーと固定板位置は維持し、角・根元は0.1 mm面取り。足の下端をZ0とし、柱全体を長くしない。新しい下端を含め、ケース・基板・ねじ等との干渉と床の接触面積を検査する。

## MAINの取り付け

床上面Z18.8 → MAIN柱14.3 mm → 固定板下面Z33.1。`main_mount_plate.stl` の板厚は2.4 mmで、基板直下の4個の座も同じ部品に一体化している。座上面Z41.95、MAIN基板下面Z42を維持する。**14.3 mmの柱だけで基板を直接支えず、固定板も1個使用する。** 既存のM3×25を1本、基板との共締めM3×30を3本、残りの基板穴M3×8を1本使用する。

| 柱ラベル | 箱内の中心X/Y mm | 上側の部品 |
|---|---|---|
| main_column_0 | 21 / 16.5 | 固定板の前側張出し座 |
| main_column_1 | 22.5 / 107.5 | 固定板＋基板の共締め座 |
| main_column_2 | 125.5 / 32 | 固定板＋基板の共締め座 |
| main_column_3 | 125.5 / 107.5 | 固定板＋基板の共締め座 |

Sony柱はM3×50を4本、GNSS柱はM3×40を4本で、既存の床ナットへ共締めする。スペーサは通し穴付きスリーブで、柱内部へのタップや印刷ねじは不要。Sony右は外径が小さいので左右を取り違えない。

## 一体化している支持部

| 取付先 | 含まれる印刷部品 | 独立スペーサの追加 |
|---|---|---|
| PWR基板4点 | `floor_plate.stl` の柱（Z18.8–28.25） | 不要 |
| TX基板4点 | `floor_plate.stl` の柱（Z18.8–24.75） | 不要 |
| 電池台4点 | `floor_plate.stl` の座（上面Z20） | 不要 |
| MAIN基板4点 | `main_mount_plate.stl` の座（上面Z41.95） | 不要 |
| Sony基板4点 | `sony_mount_plate.stl` の座（上面Z65.55） | 不要 |
| GNSSユニバーサル基板／LIS3MDL | `gnss_universal_carrier.stl` の梁・取付座 | 不要 |
| アンテナ・同軸巻き部 | `ann_mb1_internal_rack.stl`／`ann_mb1_coax_ring.stl` | 不要 |

GNSS受信基板は既存のピンヘッダー実装でユニバーサル基板へ載る。新たなスペーサを挟まない。購入品hex_spacerは現行内装に使わない。金属ねじ・ナット、アンテナ鋼板、フォームは印刷しない。

## 印刷条件と検証

柱は平らな下面をベッドへ接地し、Z方向に積み、突起を上向きにする。同梱STLはその姿勢と原点へ変換済み。X1 Carbon、0.4 mmノズル、PETG、積層0.2 mm、壁4周、100%充填を使う。小さな接地面には外側3 mmブリムを付け、冷却後に取り除く。底面・上面・キーの高さを削らない。

外周0.1–0.15 mm面取りと、MAIN/Sonyの穴口の逃げを使用する。Sony右は下端の結合後に角と根元を0.1 mm面取りする。Ø3.45 mmの円形通し穴は、既存の嵌合とSTEP/STLの一致を保つため形状を引き継ぐ。新しい穴寸法やねじ山は導入しない。GNSS穴口を含む既存の機能稜は変更せず、必要ならバリだけを除く。

独立OpenSCADレンダリング、STEP/STLの閉形状・寸法・体積照合、12本の上下取付面と干渉、PWR/TX/電池/MAIN/Sonyの一体支持20点を [spacer_delivery_checks.json](spacer_delivery_checks.json) で検査する。実スライスの条件と結果は `print_jobs/spacers_20261022/manifest.json`、確認画像は `_work/images/spacer_delivery_*.png`。物理的な印刷、嵌合、締付け、強度・クリープの認定は未実施。

今回の結果は37検査合格、全13種類のSCAD/STEP一致、箱内123点／箱外121点の組立STEP照合合格。Sony右の床接触面積は各16.744 mm²。12本をまとめた [設定済み3MF](print_jobs/spacers_20261022/parent_spacers.3mf) は約15.0 g、予測約71分20秒。支持材自動検出を有効にし、45°・全表面・橋の除外なしで支持材押出し0、警告なし。最初の層とZ14.2/31.2/31.8/41.8/42.4 mmの実工具経路を確認し、各穴と上端が残ることを確認した。G2/G3の円弧も補間して表示している。

5種類の45°オーバーハング解析は `_work/analysis/spacer_delivery_20261022/*_overhang.json` に保存。検出面積は0–4.98 mm²で、Z0–0.1 mmの底縁面取りに限られる。実スライスではこの範囲を最初の0.2 mm層に含めて形成し、上方の独立した浮き島はない。面積解析だけを印刷成功の証明にはしない。新しいSony右の根元・外周は `_work/images/spacer_delivery_sony_foot.png` でも確認した（上端は観察用にZ4で切った断面で、実部品の上端ではない）。

印刷一式の出所・個数検査と作業ファイル配置検査は合格。ワークスペースは17リポジトリ・構造エラー0。ツール全体テストは42件中41件合格、1件は既存の子機 `child_wte4_suspension_clamp/spec/bambu_petg_basic_material.json` 欠落でエラー。全印刷一式の検査には変更前からある他構成7件の問題が残る。今回対象の `parent_hand_service` は合格。ログは `_work/logs/spacer_delivery_tools_tests.log`、`spacer_delivery_all_parts.log`、変更前比較は `spacer_delivery_baseline_all_parts.log`。

印刷一式に混在していた既存の電池蓋3MFは、内容・SHA-256を変えず `print_jobs/battery_lid_retained_20261022/` へ保管した。ルートの旧ZIPと日付の古いスライスは履歴資料で、今回の印刷入口は常にparts/PRINT.md。

## 再生成

部品の設計元は従来の `spec/build_parent_hand_service.py`、`spec/build_parent_stack_spacers.py`、`spec/build_parent_gnss.py` と各共通寸法。印刷用コピーを編集しない。形状を変えた場合は先に該当CADとSTLを再生成する。

```powershell
python spec/configure_parent_spacer_delivery.py
# FreeCADCmdで spec/verify_parent_spacer_delivery.py を実行（必要時 --pass --refresh-meshes）
python tools/assembly_parts.py sync parent_hand_service
python spec/slice_parent_spacers.py
python tools/assembly_parts.py check parent_hand_service
```

旧一括生成スクリプトを使った後も `configure_parent_spacer_delivery.py` で個別印刷指定へ戻す。`placement.json` と `service_placement.json` の部品位置は維持し、`print_config.json` の旧ランナー追加指定を外す。元のランナーCADも同じ新版の柱から再生成して整合を保つが、現行印刷一式には入れない。過去の検証・スライス記録は各日付の履歴として保持する。組立形状を変えた場合はFreeCADCmdで `spec/rebuild_parent_spacer_assemblies.py` を実行してclosed/service STEPを更新・検証する。
