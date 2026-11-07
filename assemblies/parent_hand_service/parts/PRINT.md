# 印刷一式

対象: `parent_hand_service`。同じ部品は表の数量だけ複製してください。

2026-10-29：床下面のM3六角ナット座11か所。上からの貫通ねじで固定。50mm一体支持枠を維持。手順は ../unified_support_report.md。電池本体・蓋の同時交換は ../battery_top_lid_report.md を参照。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [floor_plate.stl](floor_plate.stl) | 1 | 195.95 × 212.75 × 19.41 | [0, 0, 0] | 枠内 |
| [battery_base.stl](battery_base.stl) | 1 | 110.4 × 63.5 × 31 | [0, 0, 0] | 枠内 |
| [parent_lipo_retainer_lid_slide.stl](parent_lipo_retainer_lid_slide.stl) | 1 | 107.4 × 53 × 6 | [0, 0, 0] | 枠内 |
| [gnss_universal_carrier.stl](gnss_universal_carrier.stl) | 1 | 131 × 87 × 7.3 | [0, 0, 0] | 枠内 |
| [ann_mb1_coax_ring_service.stl](ann_mb1_coax_ring_service.stl) | 1 | 131 × 106 × 14 | [0, 0, 0] | 枠内 |
| [main_service_frame.stl](main_service_frame.stl) | 1 | 133.5 × 92.4997 × 17.4 | [0, 0, 0] | 枠内 |
| [antenna_service_shelf.stl](antenna_service_shelf.stl) | 1 | 132.4 × 72 × 22.4 | [180, 0, 0] | 枠内 |
| [cradle_floor_foot_0.stl](cradle_floor_foot_0.stl) | 1 | 9.2388 × 9.2388 × 11.6 | [0, 0, 0] | 枠内 |
| [cradle_floor_foot_1.stl](cradle_floor_foot_1.stl) | 1 | 9.2388 × 9.2388 × 11.6 | [0, 0, 0] | 枠内 |
| [cradle_floor_foot_2.stl](cradle_floor_foot_2.stl) | 1 | 9.2388 × 9.2388 × 11.6 | [0, 0, 0] | 枠内 |
| [cradle_floor_foot_3.stl](cradle_floor_foot_3.stl) | 1 | 9.2388 × 9.2388 × 11.6 | [0, 0, 0] | 枠内 |
| [power_adapter.stl](power_adapter.stl) | 1 | 82.995 × 109.698 × 5.5 | [0, 0, 0] | 枠内 |
| [sony_mount_plate.stl](sony_mount_plate.stl) | 1 | 65.5 × 77.46 × 6.65 | [0, 0, 0] | 枠内 |
| [sony_support_frame.stl](sony_support_frame.stl) | 1 | 64.7 × 79.6 × 50.8 | [0, 0, 0] | 枠内 |
| [gnss_support_frame.stl](gnss_support_frame.stl) | 1 | 131 × 81.5 × 50.8 | [0, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。

## モディファイア（印刷部品ではない）

- [modifiers/cradle_floor_foot_0_support_blocker.stl](modifiers/cradle_floor_foot_0_support_blocker.stl) を `cradle_floor_foot_0.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/cradle_floor_foot_1_support_blocker.stl](modifiers/cradle_floor_foot_1_support_blocker.stl) を `cradle_floor_foot_1.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/cradle_floor_foot_2_support_blocker.stl](modifiers/cradle_floor_foot_2_support_blocker.stl) を `cradle_floor_foot_2.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/cradle_floor_foot_3_support_blocker.stl](modifiers/cradle_floor_foot_3_support_blocker.stl) を `cradle_floor_foot_3.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/main_service_frame_support_blocker.stl](modifiers/main_service_frame_support_blocker.stl) を `main_service_frame.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/power_adapter_support_blocker.stl](modifiers/power_adapter_support_blocker.stl) を `power_adapter.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/antenna_service_shelf_support_blocker.stl](modifiers/antenna_service_shelf_support_blocker.stl) を `antenna_service_shelf.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/sony_support_frame_support_blocker.stl](modifiers/sony_support_frame_support_blocker.stl) を `sony_support_frame.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/gnss_support_frame_support_blocker.stl](modifiers/gnss_support_frame_support_blocker.stl) を `gnss_support_frame.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/floor_underside_nut_support_blocker.stl](modifiers/floor_underside_nut_support_blocker.stl) を `floor_plate.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/battery_lid_pilot_support_blocker.stl](modifiers/battery_lid_pilot_support_blocker.stl) を `battery_base.stl` と同じオブジェクトに読み込み、支持材禁止（support blocker）に設定。両方の相対座標を保持し、個別の自動整列をしない。
