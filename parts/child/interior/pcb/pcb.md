# 子機 基板 3D モデル 置き場

> **2026-07-31: 3 基板とも配置済み。**
> `child_main/` `child_pwr/` `rx_improved_mini/` (KiCad 実モデル)。
> 内装への反映は `docs/子機内装_収まり検討.md` と
> `parts/child/interior/printed/child_vtray_*` を参照。
> 以下はモデルを**追加・更新する**ときの手順。

ここに**子機 (水中ユニット) の基板 1 枚につき 1 フォルダ**で 3D モデルを置く。
`parts/` の他の部品と同じ扱い (1 部品 1 フォルダ / 中に step・stl・プレビュー・md)。

## フォルダの作り方

```
parts/child/interior/pcb/
└── rx_board/                     ← 基板名 = フォルダ名 (小文字スネークケース)
    ├── rx_board.step             ← Fusion/アセンブリで使う本体 (必須)
    ├── rx_board.stl              ← 確認用 (あれば)
    ├── rx_board_preview.png      ← プレビュー画像 (必須)
    ├── rx_board.md               ← 寸法・取付穴・コネクタ・要求空間 (必須)
    └── ref/                      ← 元データ (KiCad の VRML/STEP、回路図PDF など)
```

- **1 基板 1 フォルダ / 1 md**。リビジョン違いは同じフォルダに
  `rx_board_rev_b.step` のように並べ、md に差分を書く。
- 名前は英数小文字。日本語ファイル名は OpenSCAD の `import()` で使わない。

## md に必ず書くこと

寸法だけでなく、**基板の外側で場所を取るもの**を書く。ここが機体設計の入力になる。

| 項目 | なぜ必要か |
|---|---|
| 外形 (W × D) と板厚 | ベイ内寸を決める |
| 取付穴の位置と径 | 取付ボスの位置を決める |
| **最大部品高さ (表面 / 裏面)** | ベイ壁高さとチューブ断面に収まるかを決める |
| **コネクタの位置と向き、必要な抜き差し空間** | 引き出し方向・サービスループを決める |
| **ケーブルの引き出し方向と本数** | 配線路と結束点を決める |
| 発熱部品 | 密閉容器内の温度上昇 |
| 高背部品 (電解コン、シールド缶など) | 干渉の主因 |

## プレビューの作り方

STL があるなら:

```powershell
$env:PYTHONIOENCODING="utf-8"
python "C:\Users\ryupc\.claude\skills\3d-print-design\scripts\inspect_mesh.py" `
  parts\child\interior\pcb\rx_board\rx_board.stl
```

`<name>_preview.png` (iso / front / top / side の 4 面) と外形・体積が出る。

## 置いた後にやること

1. `parts/child/interior/printed/child_vtray_deck/child_vtray_deck.scad` の
   外形・取付穴・高さ (`main_*` / `rx_*` / `pwr_*`) を実測値へ直して再ビルド。
   assert がチューブに収まるかを検査する
2. `assemblies/child_vertical_assembly/placement.json` の `ops` を更新して
   `.\build.ps1 -Assemblies assemblies\child_vertical_assembly` で干渉確認
3. `docs/配線・ケーブル計画.md` にコネクタとケーブルを追記
