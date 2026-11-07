# 印刷一式

対象: `child_horizontal_plate_frame`。同じ部品は表の数量だけ複製してください。

2026-10-29 素手で着脱するカメラ接続試作。機体1台につきカメラ本体1・専用受け1・指掛け付きUスペーサ2・ノブ2・蓋2を印刷。M3×30六角頭2本とM3普通ナット2個を使用。初回受け固定は工具を使用する。通常はノブを緩めてスペーサ、ねじの順に外して回す。実印刷・物理操作・締結強度・クリープ・爪の耐久は未認定。詳細と旧3MFの扱いはREADME最上段を参照。 前側押さえとカメラ本体の現行3MFは print_jobs/camera_clamp_right5_20261029/。その他の手回し部品・受けは print_jobs/camera_hand_release_20261029/。X1C・0.4 mmノズル・Generic PETG・0.1 mm層・6壁・15% Gyroid。カメラ本体・受け・スペーサ・ノブはベッドからの自動サポート、蓋はサポートなし。スペーサの指掛け下面と各支持部のサポートを除去し、溝・ナット座・蓋アームを破損しないようにする。各3MFは1個入りでスペーサ・ノブ・蓋は各2個必要。旧3MFは使わない。 子機受けは既存4穴を使い、側板側M3×18が2本、ガード共締めはM3×25からM3×30へ2本交換する。接続中心は(-122,113,130) mm。

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
| [child_horizontal_twist_mount_camera_receiver.stl](child_horizontal_twist_mount_camera_receiver.stl) | 1 | 120 × 96 × 18.5 | [0, 0, 0] | 枠内 |
| [camera_mount_twist.stl](camera_mount_twist.stl) | 1 | 114 × 81.9414 × 84.4914 | [0, 0, 0] | 枠内 |
| [td04a_bracket_mount_child_side_up.stl](td04a_bracket_mount_child_side_up.stl) | 1 | 45 × 26 × 75 | [0, 0, 0] | 枠内 |
| [camera_front_clamp.stl](camera_front_clamp.stl) | 1 | 24.9828 × 24.9828 × 59.9828 | [0, 0, 0] | 枠内 |
| [camera_hand_spacer.stl](camera_hand_spacer.stl) | 2 | 22.5 × 10 × 10.5 | [0, 0, 0] | 枠内 |
| [camera_hand_knob.stl](camera_hand_knob.stl) | 2 | 19.9249 × 19.9249 × 3.8 | [0, 0, 0] | 枠内 |
| [camera_hand_knob_cap.stl](camera_hand_knob_cap.stl) | 2 | 12.1036 × 12.1036 × 0.8 | [0, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。
