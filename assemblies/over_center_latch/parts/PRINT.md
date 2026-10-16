# 印刷一式

対象: `over_center_latch`。同じ部品は表の数量だけ複製してください。

強度検証未完了の試作版。40 Nは実測校正が必要。構造解析の収束と固定部の局所応力は未解決で、100 N手押し耐力を認定しない。X1C PETG Basic / 0.4 nozzle / 0.2 layer / 6 walls / 100% infill. Four types, five printed pieces. M3x20 countersunk A, M3x35 cap B. No dedicated stop; hood seats on platform.

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [over_center_latch_base.stl](over_center_latch_base.stl) | 1 | 61.12 × 16.2974 × 70 | [90, 0, 0] | 枠内 |
| [over_center_latch_bail.stl](over_center_latch_bail.stl) | 2 | 16.799 × 8.8 × 3.6 | [90, 0, 0] | 枠内 |
| [over_center_latch_lever.stl](over_center_latch_lever.stl) | 1 | 68.4 × 19 × 44 | [90, 0, 0] | 枠内 |
| [over_center_latch_keeper.stl](over_center_latch_keeper.stl) | 1 | 47.9 × 8 × 70 | [90, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。
