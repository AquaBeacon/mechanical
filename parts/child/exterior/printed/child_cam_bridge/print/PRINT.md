# child_cam_bridge v2 — 印刷指示 (X1-Carbon)

`child_cam_bridge_print.stl` は印刷姿勢に回転済み・ベッド (z=0) 中央に置いた STL。Bambu Studio にそのまま読み込める。
スライス済みプロジェクトは `mechanical/print_jobs/child_cam_bridge/child_cam_bridge.3mf` (設定込み)。

| 項目 | 指示 |
|---|---|
| 材料 | **PETG** (Bambu PETG Basic プロファイル、テクスチャ PEI プレート) |
| 姿勢 | **+Y up: ゲートに当たる面 (y = 67) を下にして寝かせる。最適化の build_axis と同じ** — 向きを変えない (FEA の層方向がこの姿勢) |
| 外形 | 240 × 150 × 61 mm (X1C 256 × 256 × 256 に収まる) |
| レイヤ / ノズル | 0.20 mm / 0.4 mm (`0.20mm Strength` ベース) |
| 壁 / 上下 | **壁 4 周 / 上下 5 層** |
| インフィル | **gyroid 40 %** (板厚 4〜6 mm の部材はほぼ壁だけで埋まる) |
| サポート | 自動サポート (45°)。中央柱の座面 (ベッドから 7.35 mm の水平面) にサポートが乗るので面出し前提。オーバーハング 24.5 % |
| ブリム | 外側 5 mm |
| 見積 (Bambu Studio 02.05 CLI) | **8 h 47 m、270 g** (サポート・ブリム込み)、423 層 |

- 
HP4/HP5 座面 (M5×8 で共締め) はサポート跡を平らに仕上げる- デッキ下面のナットトラップ (4 mm) はブリッジで出る
- `../_work/images/print/child_cam_bridge_on_bed.png` = この姿勢でベッドに置いたレンダー (写真ではない)
