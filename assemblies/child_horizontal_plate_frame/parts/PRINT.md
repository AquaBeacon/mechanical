# 印刷一式

対象: `child_horizontal_plate_frame`。同じ部品は表の数量だけ複製してください。

Rev.4 現構成17種類・24個、未印刷13種類・19個。側板2・底板1・クランプ上下各1は印刷済み、元STLのSHAと配置を保持。追加フレーム4枚は側板内側。段差なしの一体メスは厚4、M3×18各2本。既存33×81ホルダーを流用、60°回して停止すると上向き、横のノブは水平+Y、突出59.5 mm、中央Y±45は手の通路。X1C / PETG Basic、0.4 mmノズル、8壁、100%充填、5 mmブリム、Textured PEI。一体メス・オスは0.1 mm層、他は0.2 mm層。ライトオスだけベッドからの外部サポート（上下離隔0.2）、他はサポート無効。STLは印刷姿勢へ変換済み。筒内・機構内部にサポートを入れず、除去後に爪・カム・ロック・実ライトの嵌合を確認する。旧版STLと3MFを混ぜない。嵌合・荷重試験用。詳細は同梱DESIGN_NOTES.mdのCHILD-HORIZONTAL-TWIST-C-R4。 トップフレーム改良（2026-10-12）：クランプ締付ねじ6本の真上に工具穴φ10、正12角形、入口0.4 mm面取り。工具軸φ8×70 mmは仮包絡。縁に近い2穴を局所拡幅、入口直近の検査断面の最小残存肉厚は約3.3 mm。トップは従来向きで1個。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [child_horizontal_plate_frame_side.stl](child_horizontal_plate_frame_side.stl) | 2 | 230 × 230 × 12 | [0, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_guard_front_inner.stl](child_horizontal_plate_frame_guard_front_inner.stl) | 1 | 94 × 148 × 8 | [0, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_guard_front_inner_mirrored.stl](child_horizontal_plate_frame_guard_front_inner_mirrored.stl) | 1 | 94 × 148 × 8 | [0, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_guard_rear_inner.stl](child_horizontal_plate_frame_guard_rear_inner.stl) | 1 | 96 × 148 × 8 | [0, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_guard_rear_inner_mirrored.stl](child_horizontal_plate_frame_guard_rear_inner_mirrored.stl) | 1 | 96 × 148 × 8 | [0, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_rotation_key.stl](child_horizontal_plate_frame_rotation_key.stl) | 1 | 35.5 × 57.5429 × 35 | [90, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_rotation_key_mirrored.stl](child_horizontal_plate_frame_rotation_key_mirrored.stl) | 1 | 35.5 × 57.5429 × 35 | [90, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_bottom.stl](child_horizontal_plate_frame_bottom.stl) | 1 | 220 × 230 × 33.25 | [0, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_top.stl](child_horizontal_plate_frame_top.stl) | 1 | 220 × 220 × 12 | [0, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_clamp_support.stl](child_horizontal_plate_frame_clamp_support.stl) | 4 | 98 × 43.2 × 34 | [0, 0, 0] | 枠内 |
| [child_wte4_petg_clamp_upper_linked.stl](child_wte4_petg_clamp_upper_linked.stl) | 1 | 163.696 × 62 × 160 | [0, 0, 0] | 枠内 |
| [child_wte4_petg_clamp_lower_linked.stl](child_wte4_petg_clamp_lower_linked.stl) | 1 | 163.696 × 62 × 160 | [0, 0, 0] | 枠内 |
| [child_horizontal_plate_frame_ballast_cap.stl](child_horizontal_plate_frame_ballast_cap.stl) | 4 | 82 × 30.2452 × 12 | [0, 0, 0] | 枠内 |
| [child_horizontal_twist_mount_frame_receiver.stl](child_horizontal_twist_mount_frame_receiver.stl) | 1 | 52 × 84 × 18 | [0, 0, 0] | 枠内 |
| [child_horizontal_twist_mount_light_twist.stl](child_horizontal_twist_mount_light_twist.stl) | 1 | 65 × 27.75 × 81 | [90, 0, 0] | 枠内 |
| [quick_release_prototypes_twist_knob.stl](quick_release_prototypes_twist_knob.stl) | 1 | 16 × 14.5236 × 10 | [0, 0, 0] | 枠内 |
| [child_simple_light_mount_cap.stl](child_simple_light_mount_cap.stl) | 1 | 65 × 19.75 × 81 | [0.0, -0.0, 0.0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。
