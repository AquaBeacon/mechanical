# 印刷一式

対象: `parent_hand_service`。同じ部品は表の数量だけ複製してください。

2026-10-13 全長側溝版：電池台と蓋を各1個再印刷。蓋を配線側の端から両側の全長溝へ108 mm差し込み、M3×12ねじ／M3ナット各1個で固定する。箱内で全長分を引き出せないため、電源リードを外し、台の固定ねじ4本を外して閉じたボックスを上へ約90 mm持ち上げ、蓋ねじ1本を外して引き抜く。基板を外す必要はない。最下段、MAIN固定板、同軸巻き部と工具穴8 mmは維持。電池台はprint_jobs/battery_side_grooves_20261013/battery_base.3mfをプロジェクトとして開く。ナット座と側溝の支持材禁止設定済み。STLの場合はmodifiers内の支持材禁止パーツ2個を同梱座標で追加し、単体印刷しない。蓋は上面をベッドへ向けた同梱姿勢。9種類各1個、PETG0.2 mm・4周壁・100%インフィル。旧2 mmフック版の電池台／蓋を混ぜない。実印刷でバリ、嵌合と締付けを確認する。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [floor_plate.stl](floor_plate.stl) | 1 | 195.95 × 212.75 × 19.41 | [0, 0, 0] | 枠内 |
| [battery_base.stl](battery_base.stl) | 1 | 110.4 × 63.5 × 29 | [0, 0, 0] | 枠内 |
| [parent_lipo_retainer_lid_slide.stl](parent_lipo_retainer_lid_slide.stl) | 1 | 107.4 × 48.9 × 6 | [180, 0, 0] | 枠内 |
| [main_mount_plate.stl](main_mount_plate.stl) | 1 | 111.5 × 97.9993 × 8.85 | [0, 0, 0] | 枠内 |
| [sony_mount_plate.stl](sony_mount_plate.stl) | 1 | 63.9995 × 83.9991 × 5.05 | [0, 0, 0] | 枠内 |
| [gnss_universal_carrier.stl](gnss_universal_carrier.stl) | 1 | 131 × 87 × 7.3 | [0, 0, 0] | 枠内 |
| [ann_mb1_internal_rack.stl](ann_mb1_internal_rack.stl) | 1 | 130 × 78 × 42.6 | [180, 0, 0] | 枠内 |
| [ann_mb1_coax_ring.stl](ann_mb1_coax_ring.stl) | 1 | 131 × 105.992 × 14 | [0, 0, 0] | 枠内 |
| [parent_stack_spacer_set.stl](parent_stack_spacer_set.stl) | 1 | 188 × 16.5 × 42.5 | [0, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。

## モディファイア（印刷部品ではない）

- [modifiers/battery_lid_nut_support_blocker.stl](modifiers/battery_lid_nut_support_blocker.stl) を `battery_base.stl` と同じオブジェクトに読み込み、モディファイアとして局所100%に設定。両方の相対座標を保持し、個別の自動整列をしない。
- [modifiers/battery_slide_rail_support_blocker.stl](modifiers/battery_slide_rail_support_blocker.stl) を `battery_base.stl` と同じオブジェクトに読み込み、モディファイアとして局所100%に設定。両方の相対座標を保持し、個別の自動整列をしない。
