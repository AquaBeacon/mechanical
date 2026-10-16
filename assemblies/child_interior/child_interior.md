> 2026-09-27現行: PLA Matte向け固定根元補強。60 mm根元・20 mm固定座・局所フランジ受け足を追加。印刷設定と解析結果は spec/child_interior_reinforcement/PLA_MATTE_REVISION.md。以下は旧版の履歴を含みます。

> 2026-09-27現行版：下リブ廃止、WetLink M10×5実配置、電池サービスねじをZ36へ移動。手順と検証は `spec/child_interior_reinforcement/SERVICE_REVISION.md`。以下は旧版の履歴を含みます。

> 現行版: 印刷部品による閉じた耳・31 mm根元補強。追加の金属スリーブ・板は廃止。強度解析は材料／荷重条件待ち。詳しくは `spec/child_interior_reinforcement/PRINTED_REINFORCEMENT.md`。以下は過去の履歴を含む。

# child_interior — 子機内装 (200mm WTE4 縦置き) サブアセンブリ

**現行：左右の固定耳を12 mm厚の開いたフォークとし、鋼製スリーブと押さえ板で
締め付け力を受ける再補強版。C-MAINを2 mm上げた。**
印刷・金属部品・ねじ一覧は [再補強の詳細](../../spec/child_interior_reinforcement/CRUSH_PROOF.md)。
下記は旧版を含む履歴。

## 現行構成：2026-09-26 LCD撤去・固定部補強

LCD一式を撤去し、下側の支持アーチは専用 `child_flange_brace` へ交換した。
デッキ左右の固定ラグは接線方向へ拡幅し、根元に斜めリブを追加。
下フランジの3点固定と基板位置は維持している。
C-MAINの上側2穴はLCDスペーサを外してM3×8なべねじで固定する。
変更・印刷・組立の詳細は [補強記録](../../spec/child_interior_reinforcement/README.md)。
以下のLCD関連記述と旧BOMは変更前の履歴。現在の部品一覧は `placement.json` を参照。

親機の [parent_interior_p1](../parent_interior_p1/parent_interior_p1.md) と同じ位置づけの
**内装だけのサブアセンブリ**。`child_vertical_assembly` の interior グループと同一配置で、
取合い確認用にアクリルチューブ + 上下フランジを透明表示する。
外装シェル / カメラは含まない。下エンドキャップ (5×M10) と上ドーム (参考モデル) は容器グループに含む
(2026-09-03 追加。プレビューの容器は半透明で、内装が透けて見える)。

配置根拠: [docs/子機内装_収まり検討.md](../../docs/子機内装_収まり検討.md) /
[docs/子機内装_サービス設計.md](../../docs/子機内装_サービス設計.md) (組立・印刷・サービス手順の正)。

## 2026-09-03 最終状態 — 電池 35×26×110、床板着脱方式、ハーネス 9 本モデル化

Zeee 3S 2200 (102×34×23) から **35×26×110** (型番未確定) へ変更。

### 電池・ハードウェア

| 対象 | 仕様 |
|---|---|
| LiPo | 35×26×110 @ z 21..131、リード −Z 出し。+Z は 1.5t リップ (z 132..133.5)、−Z は 6t 端壁 (z 14..20、貫通口内にリード切欠き) |
| 床板 | `child_vtray_batt_floor` 39.4×3×111.5、−Z タブ (皿ねじ M3×8 ×1、貫通口内)、フック ×2 (x 18.4..19.7) がリップのスロットへ。**電池交換: XT30 を抜く → 皿ねじ 1 本を外す → 床板を −Z へ 2mm ずらしてフックを外す → −Y へ抜く → 電池が −Y へ出る。MAIN/RX/箱は外さない** |
| 電池リード | 切って付け直す (ユーザー確認済み): 電源リードは短く切って XT30 メス、基板側は `J_BAT` パッド直付けのピグテール (XT30 オス)。嵌合ペアは +X レール溝内 z 25..55。硬直 50mm/XT60 は元コネクタ側のものなので無くなり、クレードルは不要になった |
| ハーネス動作 | `parts/common/cabling/child_harness/` (9 バリアント、世界座標、keep-out モデル) として完全モデル化・アセンブリ追加。推奨カット長 (実長 ×1.2): xh9_pwr 141 / xh6_rx 165 / xh7_lcd 100 / xh3_teth 192 / xh4_temp 202 / xh2_leak 216 / xh4_prs 182 / bat 電源リード 37 / bat ピグテール 164 / 充電リード 29 / led 277。ハーネス経路は同ファイルを正とする |
| J_BAT / J_LED | コネクタ未実装。ピグテール始点はパッド直付け (コネクタ嵌合不可: 壁までが 14mm) |

### 構成変更

**新部品**: `child_vtray_batt_floor` (床板)、`lipo_35x26x110`、`parts/common/cabling/child_harness` (9 本)。
**廃止**: `child_vtray_batt_gate`、`child_vtray_xt60_cradle` と `xt60_rigid_run` は**同日中に廃止** (アセンブリから除外、フォルダ残置)。
**復活**: `child_vtray_cable_rail` ×2 (個数 1→2、底に窓追加)。

### 検証 (2026-09-03 最終)

- `verify_child_interior.py` 全 85 アイテム PASS (床板タブは貫通口内で余裕 0.68 = WARN、意図どおり)
- `check_asm_contacts.py --ignore-threads` FLOATING 0、貫通は「プラグ↔基板ヘッダ」「ピグテール始点↔基板 STL 内 XT30PW (未実装)」「電池リード始点↔リードスタブ」「ハーネス同士」のみ (設計どおり)。レール貫通は窓と経路修正で 0

## 2026-08-28: 浮いていた部品をすべて固定した

「浮いている部品がある」指摘を受け、`scad/lib/check_asm_contacts.py` (部品対ごとの最小距離 +
貫通検査) で全内装部品を調べた。結果、**浮いていたのは RX 基板 (デッキまで 4.7 mm、スペーサ未モデル)**
のほか、ねじ・スペーサが 1 本もモデル化されておらず、さらに「0.04 mm で接触」と見えていた 4 箇所が
実は**貫通**だった。

| 貫通していた箇所 | 深さ | 直し方 |
|---|---|---|
| LCD モジュール ↔ ベゼル前板 | 2.0 | LCD を前板 2 + フォーム 0.8 の奥 (y=40.7) へ移動。旧モデルの「背面 8mm ピン + 20×50 キャリア包絡」はデータシート (rev 1B) と違ったので、実物どおり**長辺の面内ピン 1.5 ピッチ ×8 を背面へ 90° 曲げて 4mm にトリム**した形に作り直した |
| 電池箱のフランジアンカー腕 ↔ デッキ板 (+ ケーブルレール) | 2.7 | アンカーを `child_vtray_batt_box` から **`child_vtray_deck` のラグ** (x 44.8..48.5、z 29..34.5) へ移設 |
| ヒンジ枠の取付ラグ ↔ LCD アーチ | 2.6 | ラグをアーチと同じ Z 帯からアーチ内側面 (z 27..32 / 112..117) へ移し、M3×10 を軸方向に締める |
| ヒンジ枠のナックル ↔ ドア板 | 1.1 | ドア板の縁にナックル逃げ切欠き (x ≤ −15、±7.8) |

固定のために実体化した購入品 (全部 `placement.json` に載っている):

| 部品 | 数 | 用途 |
|---|---|---|
| M3 MF30 / MF17 六角スペーサ | 2 / 2 | C-MAIN 取付穴に立て、LCD アーチのボスを受ける (MAIN 固定兼用)。**旧記載の 35/20 はボス中心までの寸法で、端面基準では 30/17 が正** |
| M3×10 皿 (JIS 頭径 5.5) | 4 | アーチボスの +Y 面に面一で沈める (なべ頭だとアクリルまで 0.6 mm しかない) |
| M3 MF10 六角スペーサ | 2 | 下フランジ BCD94 M3 穴に立て、デッキのラグを受ける (ねじ込み 4〜5 mm) |
| M3×10 なべ | 2 + 2 + 8 | フランジラグ / ヒンジ枠ラグ / ケーブルレール ×2 (ワッシャ Ø7 は MAIN 基板端 44 に当たるので使わない) |
| M3×12 なべ/キャップ | 1 | 下フランジ BCD94 **90°** 穴 (0, +47)。下 LCD アーチの固定耳を貫きフランジ内面へ直接 (2026-09-03) |
| M3×8 なべ | 4 + 4 | CHILD_PWR / 電池箱の耳 |
| M3×8 皿 | 1 | 電池箱の床板 (−Z タブ → 端壁の柱の Ø2.5 下穴) |
| M2 FF6 六角スペーサ + M2×6 / M2×5 | 4 + 4 + 4 | RX 基板をデッキ下面に吊る (実穴 Ø2.2 = M2) |
| M3 全ねじ 105 mm + M3 ナット ×2 | 1 | LCD ドアのヒンジ。**上下アーチのヒンジボス (Ø3.4) で両端を受け、アーチの外側でナット止め**。旧案の M3×60 頭付きピンはドア板端に頭が当たった |
| M2.5×12 低頭 / M2.5×6 | 1 / 4 | ドアラッチ / 後クランプ棒 |
| 独立気泡フォーム | 5 + 2 | LiPo: clipo_top 3t (106×33) / clipo_side 2t (106×24) ×2 / clipo_end 1t (20×24) ×2。LCD 背面: 0.8t (26×5) ×2 をクランプ棒の下に (圧縮 0.5 でモデル化)。**LiPo は膨張と振動を逃がすため PLA で剛に挟まない** |

同時に直した部品側の変更: `child_lcd_cradle` はヒンジ葉を ±8..20.5 に短縮 (クランプ棒 z 72±23.4 と
干渉していた)、クランプ座をポケット全深 8.8 に (フォーム越しに押す)、クランプ下穴ボスを板の輪郭内に
限定 (ヒンジロッドに当たっていた)。`child_lcd_support` にヒンジロッド用ボス (Ø7、穴 Ø3.4) を追加。

## 座標系

X=左右 / Y=前後 (+Y が LCD 表示面) / Z=上。**アクリルチューブ下端面が z=0**。
`child_vertical_assembly` と同一。

## 構成 (内装 88 アイテム + 容器 5)

| 部品 | 位置 (z) | 固定 |
|---|---|---|
| `child_vtray_deck_t200` | -2..202 | 上下フランジ内端面に突き当て + 下フランジ BCD94 0°/180°: MF10 スペーサ → デッキラグ → M3×10 |
| `child_vtray_rib` ×2 | 2.5..8.5 / 191.5..197.5 | デッキ先端 (幅 76 の素の板) からスロット 76.4×4.4 で差し込み、内側ショルダー (幅 84、z 9.5 / 190.5) に当てる。先端側は板を貫く M2.5×6 なべ (z 0 / 200) が抜け止め。ねじ 1 本外せば抜ける。挿入経路の掃引検査は `views/rib_sweep.scad`、拡大図は `views/13..15_rib_fit_*.png` |
| `child_vtray_cable_rail` ×2 (power / signal) | 20..130 | デッキ Z=37/77 の Ø3.4 → M3×10 ×4 セルフタップ (底に窓) |
| `child_vtray_batt_box` | 14..133.5 | 耳 M3×8 ×4 (X ±24, z 32/110、デッキ上面から) |
| `child_vtray_batt_floor` | 14..131.5 (板 20..131.5 + タブ 14..20) | M3×8 皿 ×1 (−Z タブ) + フック ×2 (+Z リップのスロット) |
| LiPo 35×26×110 | 21..131 | 床板上 (y −40..−14, x ±17.5)。フォーム 上 3 / 側 2 ×2 / 端 1 ×2 (clipo_*) |
| CHILD_MAIN v4.1 | 20..124 | M3 MF30/17 スペーサのオス ×4 (LCD アーチ共締め) |
| CHILD_PWR v2.1 | 126..188 | M3×8 ×4 |
| RX_improved_mini | 134..180 | M2 FF6 ×4 + M2×6 (デッキ側) + M2×5 (基板側) |
| `child_harness` 9 本 | 各経路 | keep-out 形状 (世界座標)。xh9_pwr / xh6_rx / xh7_lcd / xh3_teth / xh4_temp / xh2_leak / xh4_prs / bat / led。経路と推奨カット長は `parts/common/cabling/child_harness/child_harness.md` |
| `child_lcd_support_lower` / `_upper` | 19.3..27 / 117..122 | スペーサ端面 + M3×10 皿。**lower は下フランジ BCD94 90° の固定耳付き** → M3×12 でフランジ内面へ |
| `child_lcd_hinge_frame` | 21.5..122.5 | ラグ M3×10 ×2 → アーチ下穴 |
| `child_lcd_cradle_bezel` + NHD-C0216CiZ + `_bar` ×2 | 40..104 | ヒンジロッド + ラッチ / クランプ M2.5×6 ×4 + フォーム |

## 検証 (2026-08-28)

```powershell
python scad\lib\verify_child_interior.py assemblies\child_interior\placement.json --root .
python scad\lib\check_asm_contacts.py assemblies\child_interior\placement.json --root . --ignore-threads
```

- 包絡: 全 75 内装アイテム (フランジスペーサのオス部 = フランジ金属内は `skip_envelope`) が
  ID101.6 / 端部 Ø88.5 の包絡内。律速はリブ 0.50 (意図的) / デッキ 1.08 / アーチ 2.55 / LCD ドア 2.80。
- 接触: **FLOATING 0 件**。`--ignore-threads` 無しで残るのは「ねじ・スペーサのオスが下穴 (Ø2.8/2.5/1.6) に
  食い込む」設計どおりの食い込みのみ。
- STEP 合成: 80 部品 (内装 77 + 容器 3)、MISSING 0。`child_vertical_assembly` も同じ interior 行で 89 部品、MISSING 0。

### 2026-09-02: Fusion で開いた STEP がずれていた件

プレビュー PNG と接触検査は正しかったが、`child_interior.step` はチューブが Z -200..0、
フランジが XY -57.15 にずれ、LCD アーチ/ベゼル/ヒンジ枠は形そのものが壊れていた。
原因は **部品の STEP と STL の座標系不一致** (ベンダ STEP の原点違い、hull() 部品の CSG→STEP 破損)。
アセンブリ側の `placement.json` は正しかったので触っていない。対策と検査は `CLAUDE.md`
「部品の STEP と STL は同じ座標系でなければならない」を参照。再ビルド後
`scad/lib/verify_asm_step.py` で **80 部品すべて配置一致 (max 0.12 mm)** を確認済み。

## ファイル

- `child_interior.step` / `.stl` — 容器込み。`child_interior_interior.stl` — 内装のみ (軽量)。
  STEP は `label` 名のコンポーネントを持つ (Fusion でブラウザから部品を選べる)
- `child_interior_fusion.json` — Fusion の `aquabeacon_bridge` スクリプト用マニフェスト
  (部品 STEP を実配置で個別コンポーネントとして取り込む)
- `child_interior_{iso,front,top,side}.png` — 容器込み。`child_interior_interior_*.png` — `show_vessel=false`。
  `_work/images/child_interior_interior_batt.png` (電池箱・床板・+X レールの電源リード)、`_work/images/child_interior_interior_harness.png` (−X レールのハーネス束と RX J2) は 2026-09-03 の手動レンダ。`views/` に 12 方向 (6 面 + 斜め 2 + 拡大 4) と一覧 `contact_sheet.png`。再生成コマンドは views/README.md
- `contacts.json` — 接触検査の生データ (部品対ごとの最小距離・貫通深さ)

## 未反映 (モデルに入っていないもの)

- LCD の I2C チャージポンプ用コンデンサ (VOUT/C1±) — ハーネス側の小基板に載せる想定。位置未定
- LCD バックライト K/A ピン (+Z 端、モデル化済み) の配線
- ヒンジロッド下端のナイロック / ラッチねじの抜け止め O リング
- ペネトレータ (エンドキャップからの突出部) / O リング / ロッキングコード (エンドキャップ本体とドームは容器グループに入れた)
- 外部ケーブル (ペネトレータ側) の長さ、LCD 小基板の位置とそのハーネス実長

## 更新手順

内装の配置は **`scad/lib/sync_child_interior.py` が唯一の生成元**で、
`assemblies/child_interior/placement.json` と `assemblies/child_vertical_assembly/placement.json` の
interior 行に同じものを書き出す。手で片方だけ直さないこと。

```powershell
python scad\lib\sync_child_interior.py
.\build.ps1 -Assemblies assemblies\child_interior,assemblies\child_vertical_assembly
python scad\lib\verify_child_interior.py assemblies\child_interior\placement.json --root .
python scad\lib\check_asm_contacts.py assemblies\child_interior\placement.json --root . --ignore-threads
python scad\lib\verify_child_holes.py assemblies\child_vertical_assembly\placement.json --root . --variant t200
```

## 2026-09-03 下フランジ固定を 3 点化 (0° / 180° / 90°)

「エンドキャップの 4 穴で内装全体を固定する」依頼。まず穴の所在を確定した:
**内装固定用の 4× M3 (BCD 94, 0/90/180/270°) はエンドキャップではなくフランジ BR-101040 の内面**にある
(STEP を FreeCAD カーネルで抽出 + Blue Robotics WTE データシート Rev C.5。エンドキャップにあるのは
キャップ固定用 6× Ø3.2 貫通 BCD108 と M10 ×5 のみ) →
`parts/child/exterior/cots/wte4_flange/_work/images/ref/BR-101040_hole_map.png`。

| 穴 | 位置 | 使用 | 部品 |
|---|---|---|---|
| 0° / 180° | (±47, 0) | ○ (既存) | `child_vtray_deck` ラグ (z 29..34.5) + M3 MF10 スペーサ + M3×10 |
| 90° | (0, +47) | **○ (追加)** | `child_lcd_support_lower` の固定耳 (足 z 19.3) + **M3×12** 直接 |
| 270° | (0, −47) | × | 電池箱の床 (y −43) が 0.75 mm 手前まで来ており、床の着脱経路を塞がずにラグを付けられる部品が無い |
| 上フランジ ×4 | z=181 面 | × | 内面が下向きで、ねじを下から回す工具アクセスが無い (貫通口 Ø88.5 の外側 r=47) |

90° をデッキから取れない理由: (0, +47) とデッキ (y −10..−6) の間に C-MAIN (x ±44, y 1..21) があり、
r=47 の弧で回り込むと DS3231 スタック (42, 21.1) = r 47.0 に当たる。下 LCD アーチは C-MAIN の真上
(z 22..27) にあり、耳を 2.7 mm 下へ伸ばすだけでフランジ内面に届く。

検証: `check_asm_contacts.py --ignore-threads` で FLOATING 0、印刷部品/金物の貫通 0
(ハーネス同士・ハーネス/基板の貫通はケーブルモデル同士の重なりで 2026-09-03 電池改修時から既知)。
`verify_asm_step.py` 89 アイテム 0 NG。断面 (x=0) で M3×12 の先端がフランジのねじ穴内 z=15 (タップ底 13) に収まることを確認。
