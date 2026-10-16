# spresense_logger — SPRESENSE 独立 IMU ロガー (購入品・簡易モデル)

SPRESENSE メインボード + 拡張ボード CXD5602PWBEXT1 + Multi-IMU Add-on の
スタック。親機防水ボックス内で独立モジュールとして `parent_plate` に載る
(P-MAIN には載らない。P-MAIN とは `J_SPR1` XH3 の同期線のみ、給電は別途 USB 等)。

| 項目 | 値 |
|---|---|
| 拡張ボード外形 | 68.6 × 53.5 (Sony 公称) |
| スタック全高 | ≈30 (**仮値・要実測**) |
| 取付穴 | **要実測** (`parent_plate` は inset 3.5 仮で穴を切っている) |
| 配置 | `parent_plate` (121, 2) に 90° 回転 (53.5 × 68.6) |

`spresense_logger.scad` はプレースホルダ (印刷対象外)。ヘッダ高さ 9 /
IMU 高さ 8 / メインボード位置 / microSD スロット位置はすべて仮。

## 要確認

- [ ] 拡張ボード取付穴の実位置・径 (Sony 図面 or 実測) → `parent_plate` の `spr_inset`
- [ ] スタック実高 (LiPo トレイ z=46 との干渉余裕に効く)
- [ ] 給電方法の確定 (USB micro-B を P-PWR 5V から / 電池単独か)
