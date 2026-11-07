# 印刷一式

対象: `child_interior`。同じ部品は表の数量だけ複製してください。

2026-10-21 clearance revision: AF5.5 hex spacers, inscribed 3.5 mm through-bores; flange M3x26 pan x2, brace M3x30/M3x45 studs and two M3 nuts; no spacer tapping.

スペーサは child_spacer_set_set.stl を1セット印刷（10 mm×2、12 mm×1、30 mm×1）。外側AF5.5の六角、内接径3.5 mmのM3滑り穴、タップ不要。PETG／0.4 mmノズル／0.2 mm積層／壁4周／100%充填。幅0.8×厚0.4 mmのつなぎを冷却後に折り、跡を除く。左右フランジは首下26 mmのM3なべねじ2本（必要ならM3×30を26 mmに切断・面取り）。ブレースは金属M3×30／×45通しスタッド各1本と普通M3ナット2個で固定。旧短スタッドと旧上ねじ4本は使わない。実物の嵌合・締結強度は未検証。

電池ナット締結・印刷根元補強版。ケースM3×12＋普通M3ナット4組、床板M3×10皿＋普通M3ナット1組、前側フランジM3×16。ナットは二面幅5.5／厚2.4 mm。ケース・床板・ブレース100%、デッキ通常15%／根元100%、壁8周。床板の容器すきまは公称0.71 mm、仮組みを確認。強度試験未実施。 2026-10-04: RXクランプは左右連結4個。小部品を減らし、フランジ梁のくびれ・床板窓・ケース耳を補強。連結クランプ100%充填。配線はクランプ外側へ迂回。 2026-10-06:軸径4 mmの工具で組立順を指定。左右フランジMF10のオス突出長は現物確認待ち（CAD6 mm／取付記録4〜5 mm）。 2026-10-07：未使用ケーブルレール2本と固定ねじ8本を撤去。デッキの既存穴は残置（使用不要）。バッテリーの普通M3ナット5個は横差しポケットに収まり、樹脂との重なり・横挿入・床板着脱の122検査で干渉なし。ナットの熱圧入や造形途中の埋込みは不要。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [child_vtray_deck_t200.stl](child_vtray_deck_t200.stl) | 1 | 99.5136 × 183.5 × 22.7 | [90, 0, 0] | 枠内 |
| [child_vtray_rib.stl](child_vtray_rib.stl) | 1 | 87.5 × 87.5 × 6 | [0, 0, 0] | 枠内 |
| [child_vtray_batt_box.stl](child_vtray_batt_box.stl) | 1 | 55.4 × 119.5 × 33 | [-90, 0, 0] | 枠内 |
| [child_vtray_batt_floor.stl](child_vtray_batt_floor.stl) | 1 | 45.7 × 111 × 5.5 | [90, 0, 0] | 枠内 |
| [child_flange_brace.stl](child_flange_brace.stl) | 1 | 71.477 × 32.977 × 12 | [0, 0, 0] | 枠内 |
| [child_rx_edge_clamp_base_pair_mirrored.stl](child_rx_edge_clamp_base_pair_mirrored.stl) | 1 | 10.4 × 53 × 8 | [-90, 0, 0] | 枠内 |
| [child_rx_edge_clamp_cap_pair_mirrored.stl](child_rx_edge_clamp_cap_pair_mirrored.stl) | 1 | 10.4 × 41 × 3 | [90, 0, 0] | 枠内 |
| [child_rx_edge_clamp_base_pair.stl](child_rx_edge_clamp_base_pair.stl) | 1 | 10.4 × 53 × 8 | [-90, 0, 0] | 枠内 |
| [child_rx_edge_clamp_cap_pair.stl](child_rx_edge_clamp_cap_pair.stl) | 1 | 10.4 × 41 × 3 | [90, 0, 0] | 枠内 |
| [child_spacer_set_set.stl](child_spacer_set_set.stl) | 1 | 36.2888 × 8.75 × 30 | [0, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。

## モディファイア（印刷部品ではない）

- [modifiers/root_dense_modifier.stl](modifiers/root_dense_modifier.stl) を `child_vtray_deck_t200.stl` と同じオブジェクトに読み込み、モディファイアとして局所100%に設定。両方の相対座標を保持し、個別の自動整列をしない。
