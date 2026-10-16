# 親機 基板 3D モデル 置き場

> **2026-07-31: 3 基板を配置済み。**
> `parent_main/` (112×88) `parent_pwr/` (100×84) `tx_improved/` (75.43×50)。
> **`parent_plate.scad` の footprints / hole_in はまだ仮値のまま** — 下の手順で更新すること。
> SPRESENSE 本体・Multi-IMU Add-on・GNSS モジュールのモデルは未入手。

ここに**親機 (水上ユニット) の基板 1 枚につき 1 フォルダ**で 3D モデルを置く。
フォルダの作り方・md に書く項目は `parts/child/interior/pcb/pcb.md` と同じ。

## 親機で置くことになる基板 (`parent_plate.scad` の footprints より)

| ラベル | 内容 | 想定外形 (仮値) |
|---|---|---|
| **実測値 (KiCad モデル)** | `parent_main` / `parent_pwr` / `tx_improved` | **112×88 / 100×84 / 75.43×50** |
| `RS485` | RS485 データ | 38 × 24 |
| `BUCK` | 5V 降圧 | 32 × 30 |
| `RTC` | RTC | 34 × 24 |
| `SPR` | SPRESENSE + IMU | 50 × 33 |
| `GPS` | NEO-M9N | 40 × 40 |
| `TX` | TX 基板 | 40 × 45 |
| `TERM` | 端子台 | 40 × 20 |

**現在の `parent_plate` の取付穴は「外形四隅から inset 4mm」の仮置き**で、
実際の穴位置ではない。モデルが揃ったら実穴位置に置き換えること。

```
parts/parent/interior/pcb/
├── tx_board/
│   ├── tx_board.step
│   ├── tx_board_preview.png
│   ├── tx_board.md
│   └── ref/
└── spresense/
    └── ...
```

## 置いた後にやること

1. `parts/parent/interior/printed/parent_plate/parent_plate.scad` の
   `footprints` と `hole_in` を実測値へ置換 → 再ビルド
2. **高さ**を確認する。`parent_plate` は 2D 配置しか見ていないので、
   ボックス蓋・GPS アンテナ上空との干渉は別途チェックが要る
3. `.scad` の**ケーブルグランド引込みゾーン**
   (下: 125,5,30,25 / 上GPS: 75,150,25,25) を侵していないか確認
4. `docs/配線・ケーブル計画.md` にコネクタとケーブルを追記
5. 親機アセンブリ (`assemblies/parent_assembly/`) を起こす
