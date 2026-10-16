# 印刷一式

対象: `parent_integrated`。同じ部品は表の数量だけ複製してください。

既存構成の印刷データを整理。強度・造形性の新規認証ではない。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [parent_spar_beam_lower.stl](parent_spar_beam_lower.stl) | 1 | 180 × 32 × 32 | [-0.0, 90.0, 0.0] | 枠内 |
| [parent_spar_beam_upper.stl](parent_spar_beam_upper.stl) | 1 | 107 × 32 × 32 | [180.0, 90.0, 0.0] | 枠内 |
| [parent_spar_coupler_half.stl](parent_spar_coupler_half.stl) | 1 | 54 × 64 × 26.75 | [-90.0, 0.0, -180.0] | 枠内 |
| [parent_spar_coupler_half_mirrored.stl](parent_spar_coupler_half_mirrored.stl) | 1 | 54 × 64 × 26.75 | [-90.0, 0.0, -180.0] | 枠内 |
| [parent_spar_ballast_body.stl](parent_spar_ballast_body.stl) | 1 | 120 × 120 × 51 | [0.0, -0.0, -180.0] | 枠内 |
| [parent_spar_ballast_lid.stl](parent_spar_ballast_lid.stl) | 1 | 120 × 120 × 6 | [0.0, -0.0, -180.0] | 枠内 |
| [parent_spar_gps_bridge.stl](parent_spar_gps_bridge.stl) | 1 | 183 × 96 × 100 | [-0.0, 90.0, 0.0] | 枠内 |
| [parent_deck.stl](parent_deck.stl) | 1 | 216 × 236 × 60 | [-180.0, 0.0, -0.0] | 枠内 |
| [parent_rope_keel_adapter.stl](parent_rope_keel_adapter.stl) | 1 | 60 × 60 × 48 | [-180.0, 0.0, 180.0] | 枠内 |
| [parent_fin_cartridge.stl](parent_fin_cartridge.stl) | 1 | 225 × 225 × 130 | [0.0, -0.0, 0.0] | 枠内 |
| [parent_sensor_carrier.stl](parent_sensor_carrier.stl) | 1 | 210 × 141 × 55 | [90.0, -0.0, -0.0] | 枠内 |
| [parent_td04a_clamp_body.stl](parent_td04a_clamp_body.stl) | 1 | 64 × 60 × 27 | [90.0, -0.0, 180.0] | 枠内 |
| [parent_td04a_clamp_cap.stl](parent_td04a_clamp_cap.stl) | 1 | 58 × 32 × 19 | [-90.0, 0.0, -180.0] | 枠内 |
| [dji_osmo_action6_mount.stl](dji_osmo_action6_mount.stl) | 1 | 104 × 79.45 × 84.5 | [0.0, -0.0, 0.0] | 枠内 |
| [parent_plate_integrated.stl](parent_plate_integrated.stl) | 1 | 183 × 203 × 20.5 | [0, 0, 0] | 枠内 |
| [parent_lipo_tray.stl](parent_lipo_tray.stl) | 1 | 112 × 84.5 × 17 | [0, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。
