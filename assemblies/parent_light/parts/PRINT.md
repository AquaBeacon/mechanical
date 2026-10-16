# 印刷一式

対象: `parent_light`。同じ部品は表の数量だけ複製してください。

既存構成の印刷データを整理。強度・造形性の新規認証ではない。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [parent_light_frame.stl](parent_light_frame.stl) | 1 | 236 × 236 × 42 | [-180.0, 0.0, -0.0] | 枠内 |
| [parent_light_bar.stl](parent_light_bar.stl) | 2 | 236 × 24 × 12 | [0.0, -0.0, -180.0] | 枠内 |
| [parent_light_carrier.stl](parent_light_carrier.stl) | 1 | 210 × 88 × 67 | [-90.0, 0.0, 0.0] | 枠内 |
| [parent_camera_mount.stl](parent_camera_mount.stl) | 1 | 104 × 79.45 × 84.5 | [0.0, -0.0, 0.0] | 枠内 |
| [parent_light_jaw.stl](parent_light_jaw.stl) | 1 | 50 × 14 × 8 | [-90.0, 0.0, -180.0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。
