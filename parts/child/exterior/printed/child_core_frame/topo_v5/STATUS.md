# child_core_frame v5 軽量化 — 進捗 (2026-09-06)

目的: v4 (650 cm³) をトポロジー最適化 (`TO_printing/topopt`、設計空間モデル) で軽量化する。
機能面 (ポケット帯・ヒンジ・ラッチ・耳ボス・ガードボス・背面溝・取っ手・HP1/HP2/HP3) は preserve。

## 手順と状態

| # | 段階 | 状態 |
|---|---|---|
| 1 | 設計空間定義 `child_core_frame_v5.scad` (preserve / obstacle / design_space / cuts) | 済 |
| 2 | `topopt setup` 検証 (voxel 3、grid 66×63×86、free 90,980 セル、preserve 186 cm³) | 済 OK |
| 3 | `topopt run --model . --iters 80 --voxel 3` (volfrac 0.10、6 ケース) | 済 (6.9 h、他 2 部品と GPU 共有)。400.7 cm³、未収束 (0.0049 > 0.002)。最終 FEA は `extract --solver cuda:jacobi` で再実行 (`extract2.log`) |
| 4 | 結果の読み取り (`slices_{x,y,z}.png`、領域別体積) | 済 |
| 5 | プリミティブで `child_core_frame.scad` v5 を再構築 (v4 は `archive/v4/`) | 済 (a 438 → b 517 → c 493 → d 495 → e 504 → f 503 → g/h ボス径 → i 505.2 cm³ 確定) |
| 6 | `topopt compare` (`compare_a/b/c`) / `topopt print` / `topopt overhang` / `topopt fea` 1.33 mm (`fea_v5/`, `fea_e/`) | compare・print 済。fine FEA: `fea_v5`/`fea_e`/`fea_f` (1.33 mm) と `fea_g` (1.25 mm) は全ケース たわみ・p99.5 PASS、mesh resolution は最薄部 (溝側壁 2.5 → 4、ハンチ薄片、ボス壁 2.8/3.8) を順に直して `fea_i` (Ø15 ボス、1.25 mm) を実行中 |
| 7 | md・interfaces.json・アセンブリ・部品一覧の更新 | 済 (最終 FEA 表 = `fea_i115` 1.15 mm + `fea_i` 1.25 mm の交差確認) |
| 9 | 3 部品を組んだ `child_frame2_assembly` の再ビルド・接触・輸送包絡検査 | 済 (0 NG、貫通は COTS のみ、包絡 266.7 × 238 × 321.2) |
| 8 | 取合いロック (guard_ring / top_crown → core_frame) | 再ロック済み **人間確認待ち** (値は不変) |

## 並行作業 (別ワーカー)

- `child_cam_bridge/topo_v1/` — 最適化済 (328 → 181 cm³) → **再構築完了 v2 = 266.5 cm³ (−19 %)**、4 ケース fine FEA PASS (mesh PASS)、STEP 1 ソリッド。目標 230 は未達 (preserve 124 cm³ + cube 縛り。工具アクセス Ø12→10 等の緩和は判断待ち)
- `child_jaw_gate/topo_v1/` — 最適化済 (308 → 176 cm³) → **再構築完了 v2 = 211.5 cm³ (−31 %)**、7 ケース fine FEA PASS、STEP 1 ソリッド。ノブボルト挿入通路 Ø24 を確保。**判断待ち: ノブ頭 Ø16 が容器 (r57.15) / EVA に 1.8〜3 mm 食い込む → `latch_hx` 62→66 (コアと同時変更) or 頭径縮小**

## 決めたこと

- 設計空間 = v4 の外形箱 + ヒンジ柱 (y 0..18)。外形は広げない
- preserve は座面板 t4 + インサートボス Ø12 まで絞った。残りは最適化が決める
- 荷重 6 ケース: L1 吊り 3g / L2 側方 300 N / L2 ヒンジ側着地 300 N / L2 後方 300 N / L3 把持プリロード / L5 着底 600 N
- 自己支持 45° + 12 mm までのサポート柱を許容
- 最適化が出した「溝の後ろのループ板」は不採用 (溝の機能優先)、t5 のせん断板で代替
- 合格基準: 全ケース たわみ ≤ 1.0 mm、SF p99.5 ≥ 3.0 (最悪要素は所見として記録)

## 印刷準備 (2026-09-06)

各部品 `print/` に印刷姿勢 STL・PRINT.md・ベッド上レンダー。`Body_Models/print_jobs/<部品>/<部品>.3mf` は Bambu Studio 02.05 CLI でスライス済み (PETG、0.20 Strength、壁 4・上下 5・gyroid 40 %・サポート 45°)。見積: コア 23 h 56 m / 667 g、ゲート 10 h 39 m / 297 g、ブリッジ 8 h 47 m / 270 g (旧版は 712 / 356 / 316 g)。

## 人間確認待ち

0. **ゲートのノブボルト頭 Ø16 と容器の干渉** (上記)。`latch_hx` はコア/ゲート二重定義なので両方同時に変える

1. guard_ring / top_crown の取合いロック再確認 (`part_index.py lock --confirmed`)
2. L3 把持プリロード 300 N/本 の妥当性 (fine FEA で最悪要素が 3 を切る箇所はラッチボス角の応力集中)
3. 最適化の未収束 (80 反復) — 必要なら 120 反復で再 run (GPU 単独なら 1 時間程度)
