# 印刷一式

対象: `quick_release_trials`。同じ部品は表の数量だけ複製してください。

内蔵固定ナット版、9種類9点。A上側板10 mm、C上側板6 mm。A/CともM3×40六角ボルト、合計ボルト2・ナット2・ワッシャ2。固定ナットとノブ内ボルト頭は六角で回り止めし、少量のエポキシで脱落防止（ねじ山へ付けない）。Cはノブ付きボルトを右へ抜き60°戻す。A押さえは外側X面を下、Bメスは入口を上。STLは姿勢・接地済み。PETG、0.4 mmノズル、0.2 mm層、5周壁、上下6層、40% infillは仮条件。まずサポートOFFで短い橋・C爪根元をスライス確認。必要なら外側だけ局所サポート。ナットポケット・横穴・C回転溝はサポート禁止。詳細はDESIGN_NOTES.md。実造形・強度・接着保持未検証。 外周フィレット付き: 取付板縦角R3・上縁R0.8、受け縦角R1、ノブ自由端R0.8。 Cは下降カム溝で60°回すと0.60 mm引込み。厚さ1.0 mmゴムを5×8 mmに2枚切り、Cオス（蓋）の下面X=±10.5 mmにある5.4×8.4×0.4 mmの開放くぼみへ薄く接着。ゴムの0.6 mmがくぼみから出て、メス上面は平坦。公称圧縮0.10 mm。ゴムは印刷しない。Cオス・メスは0.1 mm層で試作。材質・硬さ・接着方法・操作力は実物確認。

STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。

| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |
|---|---:|---|---|---|
| [quick_release_prototypes_slide_female.stl](quick_release_prototypes_slide_female.stl) | 1 | 40 × 40 × 16.2 | [0, 0, 0] | 枠内 |
| [quick_release_prototypes_slide_male.stl](quick_release_prototypes_slide_male.stl) | 1 | 40 × 40 × 16 | [0, 0, 0] | 枠内 |
| [quick_release_prototypes_slide_gib.stl](quick_release_prototypes_slide_gib.stl) | 1 | 8.4 × 20 × 11.5 | [0, 90, 0] | 枠内 |
| [quick_release_prototypes_knob.stl](quick_release_prototypes_knob.stl) | 1 | 22 × 19.7198 × 10 | [0, 0, 0] | 枠内 |
| [quick_release_prototypes_snap_female.stl](quick_release_prototypes_snap_female.stl) | 1 | 40 × 10 × 39 | [-90, 0, 0] | 枠内 |
| [quick_release_prototypes_snap_male.stl](quick_release_prototypes_snap_male.stl) | 1 | 40 × 48 × 4 | [0, 0, 0] | 枠内 |
| [quick_release_prototypes_twist_female.stl](quick_release_prototypes_twist_female.stl) | 1 | 40 × 40 × 18 | [0, 0, 0] | 枠内 |
| [quick_release_prototypes_twist_male.stl](quick_release_prototypes_twist_male.stl) | 1 | 40 × 40 × 14 | [0, 0, 0] | 枠内 |
| [quick_release_prototypes_twist_knob.stl](quick_release_prototypes_twist_knob.stl) | 1 | 16 × 14.5236 × 10 | [0, 0, 0] | 枠内 |

回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。

`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。
