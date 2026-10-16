# 印刷一式

対象: `dji_style_toggle_latch`。同じ部品は表の数量だけ複製してください。

形状不一致の旧試作。写真の防水カメラハウジング用ラッチとは異なるため機体用に採用しない。元の試作条件は厚1mm EPDMシート、Bambu Lab PETG Basic、0.4mmノズル、0.2mm層、6周壁、100%インフィル。STLは履歴として保持。公開CAD調査はspec/dji_style_toggle_latch/PUBLIC_CAD_REVIEW.md。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [dji_style_toggle_latch_base.stl](dji_style_toggle_latch_base.stl) | 1 | 26 × 46 × 16 | [0, 0, 0] | 枠内 |
| [dji_style_toggle_latch_keeper.stl](dji_style_toggle_latch_keeper.stl) | 1 | 23 × 48 × 16.5 | [0, 0, 0] | 枠内 |
| [dji_style_toggle_latch_link.stl](dji_style_toggle_latch_link.stl) | 2 | 23 × 11 × 4.8 | [90, 0, 0] | 枠内 |
| [dji_style_toggle_latch_lever.stl](dji_style_toggle_latch_lever.stl) | 1 | 55.7951 × 28.8 × 20.8 | [180, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。
