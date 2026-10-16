# 印刷一式

対象: `parent_oneplate`。同じ部品は表の数量だけ複製してください。

位置決め追加の試作。PETG・0.20 mm・壁6周・上下6層・40%・ブリム5 mm・通常サポートON。camera_mount.stlは既存品を再利用できる。初回の実物合わせと反復着脱試験は未実施。現行3MFはprint_jobs/repeatable_mount/。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [parent_oneplate_frame.stl](parent_oneplate_frame.stl) | 1 | 232 × 134 × 42 | [180, 0, 0] | 枠内 |
| [parent_oneplate_bar.stl](parent_oneplate_bar.stl) | 2 | 232 × 24 × 12 | [0.0, -0.0, -180.0] | 枠内 |
| [parent_oneplate_td_support.stl](parent_oneplate_td_support.stl) | 1 | 80 × 43.85 × 69 | [-90, 0, 0] | 枠内 |
| [camera_mount.stl](camera_mount.stl) | 1 | 100 × 87.45 × 84.5 | [0, 0, 0] | 枠内 |
| [parent_light_jaw.stl](parent_light_jaw.stl) | 1 | 50 × 14 × 8 | [-90.0, 0.0, -180.0] | 枠内 |
| [parent_oneplate_box_locator_side_left.stl](parent_oneplate_box_locator_side_left.stl) | 1 | 11 × 98 × 17.65 | [0, 0, 0] | 枠内 |
| [parent_oneplate_box_locator_side_right.stl](parent_oneplate_box_locator_side_right.stl) | 1 | 10.5 × 98 × 21.65 | [0, 0, 0] | 枠内 |
| [parent_oneplate_box_locator_end_fixed.stl](parent_oneplate_box_locator_end_fixed.stl) | 1 | 20 × 74 × 33 | [0, 0, 0] | 枠内 |
| [parent_oneplate_box_locator_end_push.stl](parent_oneplate_box_locator_end_push.stl) | 1 | 20 × 80 × 33 | [0, 0, 0] | 枠内 |
| [parent_oneplate_box_locator_pressure_pad.stl](parent_oneplate_box_locator_pressure_pad.stl) | 3 | 14 × 12 × 5.4 | [0, 0, 0] | 枠内 |
| [parent_oneplate_camera_stop.stl](parent_oneplate_camera_stop.stl) | 1 | 52 × 19 × 22.8 | [0, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。
