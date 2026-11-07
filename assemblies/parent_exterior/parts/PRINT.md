# 印刷一式

対象: `parent_exterior`。同じ部品は表の数量だけ複製してください。

2026-10-29 素手で着脱するカメラ接続試作。機体1台につきカメラ本体1・専用受け1・指掛け付きUスペーサ2・ノブ2・蓋2を印刷。M3×30六角頭2本とM3普通ナット2個を使用。初回受け固定は工具を使用する。通常はノブを緩めてスペーサ、ねじの順に外して回す。実印刷・物理操作・締結強度・クリープ・爪の耐久は未認定。詳細と旧3MFの扱いはREADME最上段を参照。 前側押さえとカメラ本体の現行3MFは print_jobs/camera_clamp_right5_20261029/。その他の手回し部品・受けは print_jobs/camera_hand_release_20261029/。X1C・0.4 mmノズル・Generic PETG・0.1 mm層・6壁・15% Gyroid。カメラ本体・受け・スペーサ・ノブはベッドからの自動サポート、蓋はサポートなし。スペーサの指掛け下面と各支持部のサポートを除去し、溝・ナット座・蓋アームを破損しないようにする。各3MFは1個入りでスペーサ・ノブ・蓋は各2個必要。旧3MFは使わない。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [parent_oneplate_frame.stl](parent_oneplate_frame.stl) | 1 | 240 × 134 × 20 | [0, 0, 0] | 枠内 |
| [camera_mount_twist.stl](camera_mount_twist.stl) | 1 | 114 × 81.9414 × 84.4914 | [0, 0, 0] | 枠内 |
| [parent_oneplate_box_locator_pressure_pad.stl](parent_oneplate_box_locator_pressure_pad.stl) | 3 | 14 × 12 × 5.4 | [0, 0, 0] | 枠内 |
| [parent_oneplate_stand.stl](parent_oneplate_stand.stl) | 2 | 52 × 180 × 20 | [0, 90, 0] | 枠内 |
| [parent_oneplate_camera_qr_female.stl](parent_oneplate_camera_qr_female.stl) | 1 | 60 × 114 × 28.5 | [0, 0, 0] | 枠内 |
| [parent_oneplate_bar.stl](parent_oneplate_bar.stl) | 1 | 244 × 146 × 20 | [0, 0, 0] | 枠内 |
| [parent_oneplate_box_locator_side_left.stl](parent_oneplate_box_locator_side_left.stl) | 1 | 15 × 98 × 15.8 | [0, 0, 0] | 枠内 |
| [parent_oneplate_box_locator_side_right.stl](parent_oneplate_box_locator_side_right.stl) | 1 | 14.5 × 98 × 22.8 | [0, 0, 0] | 枠内 |
| [parent_oneplate_box_locator_end_fixed.stl](parent_oneplate_box_locator_end_fixed.stl) | 1 | 47 × 74 × 20 | [0, 90, 0] | 枠内 |
| [parent_oneplate_box_locator_end_push.stl](parent_oneplate_box_locator_end_push.stl) | 1 | 51 × 80 × 20 | [0, 90, 0] | 枠内 |
| [td04a_bracket_mount_parent_down.stl](td04a_bracket_mount_parent_down.stl) | 1 | 75 × 42 × 26 | [0, -90, 0] | 枠内 |
| [camera_front_clamp.stl](camera_front_clamp.stl) | 1 | 24.9828 × 24.9828 × 59.9828 | [0, 0, 0] | 枠内 |
| [camera_hand_spacer.stl](camera_hand_spacer.stl) | 2 | 22.5 × 10 × 10.5 | [0, 0, 0] | 枠内 |
| [camera_hand_knob.stl](camera_hand_knob.stl) | 2 | 19.9249 × 19.9249 × 3.8 | [0, 0, 0] | 枠内 |
| [camera_hand_knob_cap.stl](camera_hand_knob_cap.stl) | 2 | 12.1036 × 12.1036 × 0.8 | [0, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。
