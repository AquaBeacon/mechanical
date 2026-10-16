> 現行の整理・共通作業規約は [AGENTS.md](../AGENTS.md) を優先する。この文書は既存のCAD検証と設計事故の記録を保持する。型番の選択は過去の確認を引き継ぐ。

# 既存CADの設計・検証手順

Mitou26 AquaBeacon の機体 (筐体・機構パーツ) 3D 設計リポジトリ。
設計ソースはパラメトリック OpenSCAD、成果物は Fusion 360 で編集できる **STEP** と
確認用 **STL** + プレビュー PNG。

## 設計フロー (この順序を守る)

```
0. 取合い相手の既存部品を「人間に確認」して確定させる  ← 必須ゲート。飛ばさない
1. 既存部品 (購入品/COTS) を parts/.../cots/ に用意し、寸法を .md に確定させる
2. それらを assemblies/<name>/placement.json に実配置してアセンブリを作る
3. 隙間・取合いを見て、必要な箇所を 3Dプリント部品として設計する
   3a. 細かい部品 (カメラ固定治具・持ち手・センサ座・コネクタ座) を先に設計する
   3b. フレーム/シェルは「残った空間」を設計領域としてトポロジー最適化する
   3c. 最適化密度/メッシュを直接平滑化し、機能寸法だけ局所復元する。単純な梁・柱・リングへ置き換えない（2026-10-05ユーザー指定）
4. 3Dプリント部品をアセンブリに追加して、干渉と部品外事項を再確認する
```

**購入品の寸法が仮値のまま 3Dプリント部品を作り込まない。**
仮値で進めるときは `.md` の「要確認」に必ず残し、依存する `.scad` 変数を明記する。

### ステップ 0: 既存部品の確認ゲート (必須)

**既存部品に接する・干渉を避ける・寸法を借りる設計を始める前に、必ず人間に
「どの部品か」を確認する。** 例外なし。間違えても何も壊れないのが問題で、
`.scad` はビルドでき assert も通りプレビューも正しく見えるのに、実物が合わない。

このリポジトリには間違える理由が実際に揃っている:

- **排他な 2 構成**が同居している (`child_assembly` 横置き / `child_vertical_assembly` 縦置き)
- **廃止済みの部品がディスク上に残っている** (`lipo_3s_5000` / `lipo_3s_2200`)
- **1 フォルダに複数バリアント** (`child_osmo_holder` の cradle / strap)
- **仮値が実測値と見分けがつかない** (`action_camera` は公称値のみ、`child_light_clamp` は `light_d=40` 仮)

手順:

```powershell
$S = "C:\Users\ryupc\.claude\skills\3d-print-design\scripts"
# 1. 候補を集める (どのアセンブリに属するか・状態・実寸まで出る)
python "$S\part_index.py" confirm --root . --for <新部品名> <キーワード>
# 2. 人間に「どれか」を聞く。候補が別アセンブリにまたがっていたら必ず構成も聞く
# 3. 答えを新部品フォルダに固定する
python "$S\part_index.py" lock --root . --for <新部品名> --ref <確定した部品> --confirmed `
       --value <変数名>=<mm> --note "人間確認 YYYY-MM-DD: ..."
# 4. 以後、ビルド前に毎回検証する (相手が変わっていたら DRIFT で落ちる)
python "$S\part_index.py" check --root .
```

`check` は「寸法の二重定義」(下記の設計規約 4) の追従漏れも同時に捕まえる。

#### 基板の取付穴は `.kicad_pcb` が唯一の正

**基板に接する部品 (トレイ・ボス・スペーサ座) を作るときは、取付穴の位置と
ねじ呼び径を `.md` からではなく `hardware/pcb/<BOARD>/<BOARD>.kicad_pcb`
から取ること。** `.md` は生成物であって正ではない。

2026-08-03 に、`child_vtray_deck` のボスが 3 基板すべてで実穴と合っていないのが
見つかった (MAIN が 17.5mm、RX が 1.56mm、PWR は `variants.txt` 経由で 1.6mm)。
`.scad` はビルドでき assert も通り、プレビューも正しく、`.md` も相互に一致して
いた — **全部の書類が揃って基板と違っていた**。RX に至っては実穴が M2 (Ø2.2) で、
M3 は物理的に通らなかった。

原因は「基板座標 → 機体座標の変換**結果**を手で書き写していた」こと。対策:

- `.scad` には `.kicad_pcb` の実座標をそのまま持ち、**変換式で**位置を導出する
  (`child_vtray_deck.scad` の `main_h_kx` / `main_h_ky` → `main_hx` / `main_hu`)
- **`variants.txt` で穴位置を上書きしない** (ビルド成果物だけが静かにずれる)
- 穴を持つ部品は機械可読な `HOLETABLE` を `echo()` する
- ビルド後に必ず突き合わせる:

```powershell
python scad\lib\verify_child_holes.py assemblies\child_vertical_assembly\placement.json `
       --root . --variant t200
```

これは `.kicad_pcb` の Edge.Cuts とマウントホール実座標を `placement.json` の
行列で機体座標へ移し、OpenSCAD が実際に吐く `HOLETABLE` と比較する。
ねじ呼び径 ↔ ドリル径の整合 (M3 を Ø2.2 に通そうとしていないか) も見る。
人間が不在のとき (自動再開中など) は `--confirmed` を付けずに lock し、
進捗ファイルの「人間確認待ち」に積んで、確認不要な作業を先に進めること。

#### 「浮いている部品」と「貫通」はアセンブリごとに機械検査する

```powershell
python scad\lib\check_asm_contacts.py assemblies\child_interior\placement.json --root . --ignore-threads
```

全部品対の最小表面距離と、表面サンプルを 0.1 mm 内側へ押した点が相手の内部にあるか (= 貫通) を出す。
2026-08-28 に子機内装で **RX 基板が 4.7 mm 浮いており、「0.04 mm で接触」に見えた 4 箇所が貫通**だった
(LCD/ベゼル前板 2.0、電池箱アンカー/デッキ 2.7、枠ラグ/アーチ 2.6、ナックル/ドア板 1.1)。
ねじ・スペーサは実体として `placement.json` に置く (`parts/common/interior/cots/screw` / `hex_spacer`)。
`--ignore-threads` はセルフタップ下穴へのねじの食い込み (設計どおり) を除外する。FLOATING と貫通が 0 になるまで
アセンブリは完成ではない。

#### 部品の STEP と STL は同じ座標系でなければならない (アセンブリ STEP だけがずれる)

プレビュー PNG と `check_asm_contacts.py` は **STL** を、アセンブリ STEP (Fusion で開くもの) は
各部品の **STEP** を、同じ `placement.json` で合成する。部品の STEP と STL の原点が違うと
**プレビューも接触検査も正しいのに Fusion で開いた STEP だけ部品がずれる**。
2026-09-02 に子機内装で発覚: Blue Robotics WTE4 系 (チューブ / フランジ / エンドキャップ) は
ベンダ配布の STL が角原点、STEP が断面中心原点で、チューブが Z -200..0 に、フランジが XY -57.15 に飛んでいた。
さらに `hull()` / `teardrop` を含む printed 部品 3 点 (`child_lcd_support` / `child_lcd_cradle_bezel` /
`child_lcd_hinge_frame`) は FreeCAD の CSG 取り込みが hull を落として **体積 94% 減の STEP を黙って書いていた**。

対策 (すべて導入済み):

```powershell
$FC = "C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe"
# 全アセンブリの全部品について STEP と STL の外形・体積を突き合わせる (NG があれば exit 1)
$env:ASM_ROOT = (Get-Location).Path; & $FC scad\lib\check_step_vs_stl.py
# アセンブリ STEP を読み戻し、各部品が placement.json の位置にあるか (build.ps1 -Assemblies が自動で回す。-NoVerify で省略)
$env:ASM_JSON = "assemblies\child_interior\placement.json"; $env:STEP_IN = "assemblies\child_interior\child_interior.step"
& $FC scad\lib\verify_asm_step.py
```

- **ベンダ STEP を置くときは必ず `check_step_vs_stl.py` を通す。** 原点が違えば `scad/lib/step_reframe.py` で
  STL 側へ平行移動して書き直し (原本は `ref/` の zip に残す)、その `.md` に TRANSLATE 値を書く。
  placement.json は STL 基準のまま触らない。
- `csg_to_step.py` は `STL_REF` (build.ps1 が渡す) と外形 0.5 mm / 体積 2% で照合し、違えば STEP を書かずに
  終了 → build.ps1 が STL→STEP (ファセット) にフォールバックする。ログに
  `CSG->STEP result does not match the STL` が出た部品は hull/offset/teardrop を使っている。
  Fusion で面を選んで編集したい部品なら、設計規約 1 のとおり hull を cube/cylinder に書き直す。
- アセンブリ STEP は `Import.export` で書く (`asm_to_step.py`)。`Part.export` だとラベルが消えて
  Fusion では "Open CASCADE STEP translator N" という無名ボディが 2000 個超並び、部品を選べない。

## 従来のフォルダ規約（現行規約はAGENTS.mdを優先）

```
parts/<child|parent|common>/<exterior|interior>/<cots|printed>/<部品名>/
parts/<child|parent>/interior/pcb/<基板名>/      基板 3D モデル
parts/common/cabling/<ケーブル名>/               ケーブル (部品外事項)
parts/common/jigs/<治具名>/                      治具 (機体部品ではない)
assemblies/<アセンブリ名>/
scad/lib/                                        共通モジュールと変換スクリプト
docs/                                            設計方針・一覧・配線計画
spec/                                            回路検証・配置最適化の計算スクリプト類
../docs/                                         上流仕様 (AquaBeacon 仕様書。ワークスペース共通、パスはプロジェクトルート起点)
```

- **1 部品 = 1 フォルダ = 1 md**。フォルダ名 = 部品名 = `.scad` 名 = `.md` 名。
  ビルド対象の判定にこの一致を使っているので崩さないこと。
- 部品フォルダの中身: `<name>.scad` / `<name>.step` / `<name>.stl` /
  `_work/images/<name>_preview.png` / `<name>.md` / (必要なら) `variants.txt` / `ref/`
- 購入品は `.scad` が無く、ベンダのファイル名のまま置く (型番が情報なので改名しない)。
  PDF・ベンダ配布 zip は同じフォルダの `ref/` に入れる。
- 同じ部品の複数ファイル (長さ違い等) は 1 フォルダにまとめ、md で使い分けを書く。
- `interior` = 容器/ボックスの中身、`exterior` = 外に出るもの。
  両ユニットで共用するものは `common`。
- 日本語ファイル名は `.md` のみ。`.scad` / `.step` / `.stl` は英数小文字スネークケース。

## ビルド

```powershell
.\build.ps1                                                # printed 部品を全部
.\build.ps1 parts\child\interior\printed\child_tray_deck   # 個別 (フォルダ指定)
.\build.ps1 -Assemblies                                    # アセンブリ全部
.\build.ps1 -Assemblies assemblies\child_assembly          # アセンブリ個別
.\build.ps1 -NoStep                                        # STL + PNG だけ (高速)
```

Git Bash は `./build.sh` (同じ引数、`--assemblies` / `--no-step`)。

STL/STEPは**入力と同じ部品フォルダ**に出る。プレビューは `_work/images/`、CSGは `_work/intermediate/` に出る。中間 `.csg` は自動削除される。

### 内部の流れ

- 部品: `openscad` で STL と CSG → FreeCAD `freecadcmd` が `scad/lib/csg_to_step.py` で
  CSG を B-Rep ソリッドに変換 → STEP。最後に `inspect_mesh.py` が
  `_work/images/<name>_preview.png` (iso/front/top/side の 4 面) と外形・水密性を出す。
- アセンブリ: `placement.json` → `scad/lib/asm_gen.py` が `<name>_view.scad` を生成
  → OpenSCAD で 4 面 PNG。`scad/lib/asm_to_step.py` が各部品の STEP を
  実配置で合成して `<name>.step` (部品ラベルが製品名になる)。最後に
  `scad/lib/verify_asm_step.py` が STEP を読み戻して配置を検証する (`-NoVerify` で省略)。

### ツールのパス (インストール済み)

| ツール | パス |
|---|---|
| OpenSCAD | `C:\Program Files\OpenSCAD\openscad.exe` |
| FreeCAD 1.0 | `C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe` |
| inspect_mesh.py | `C:\Users\ryupc\.claude\skills\3d-print-design\scripts\inspect_mesh.py` |

### 環境の落とし穴 (実際に踏んだもの)

- `openscad` の CSG 出力は**絶対パス**が必要。相対パスだと
  "Can't open file for export"。
- `build.ps1` に**複数パスを渡すときはカンマ区切り** (`.\build.ps1 a,b,c`)。
  空白区切りだと最初の 1 つしかビルドされない (PowerShell の `[string[]]` 束縛)。
- `placement.json` を PowerShell の `Set-Content -Encoding UTF8` で書くと **BOM が付いて
  `asm_gen.py` の `json.load` が落ちる** ("Unexpected UTF-8 BOM")。JSON は python か
  BOM なしで書くこと (実際に 2026-08-28 に p1 アセンブリのビルドが 1 回落ちた)。
- `freecadcmd` はファイル引数を「開く文書」として扱うので、I/O パスは
  **環境変数**で渡す (`OPENSCAD` / `CSG_IN` / `STEP_OUT`、アセンブリは
  `ASM_JSON` / `ASM_ROOT` / `STEP_OUT`)。`OPENSCAD` を渡さないと hull/offset ノードで
  "OpenSCAD executable unavailable"。
- PowerShell から python を呼ぶときは `PYTHONIOENCODING=utf-8`
  (cp932 で em-dash が落ちる)。build.ps1 の先頭で設定済み。
- **OpenSCAD プレビューは宣言順に描く**ので、半透明 (alpha<1) の容器を先に書くと、その奥の
  不透明部品が深度バッファで隠れて**内装が 1 つも写らない** (2026-09-03 child_interior で発生)。
  `asm_gen.py` が不透明 → 半透明 (alpha 降順) に並べ替えて出力するので、placement.json の順序は自由。
  手書きの view .scad では半透明を最後に書くこと。
- `build.ps1` は **PowerShell 5.1** で動くこと。`&&` / `??` / 三項演算子は使えない。
  日本語を含むので **UTF-8 BOM 付き**で保存する (BOM なしだと文字化けする)。
- **`variants.txt` に日本語コメントを書くときも UTF-8 BOM + CRLF にすること。**
  PowerShell 5.1 の `Get-Content` は BOM 無し UTF-8 を cp932 として読むため、
  行末の日本語 (「。」など) の最終バイトが Shift-JIS のリードバイトと解釈されて
  **直後の改行を食い、次の行が前の行に連結される**。実際にこれでバリアント定義が
  1 行まるごと消え、`t200` が無言でビルドされなかった。

## 設計規約 (検証済み・必ず守る)

### 1. STEP をきれいに保つ

`.scad` は **cube / cylinder / polygon + ブーリアン (union/difference/intersection)**
だけで作る。これらは STEP で**真の平面・真円柱面**になり Fusion で選択・編集できる。

`hull()` / `offset()` / `minkowski()` による角丸は STEP で**無数の微小平面に
ファセット化**される (有効なソリッドだが編集しづらい)。
→ **角丸・フィレットは .scad で作らず Fusion 側で付ける。**

実測: `test_bracket` 角丸あり版 = 426 面 / 基本形状のみ = **18 面**。
`scad/lib/util.scad` の hull 系モジュールは「STL から直接印刷する治具」だけに使う
(`xdcr_pole_jig` は 438 面。治具なので許容している)。

### 2. フィーチャ干渉は assert で止める

watertight でも**穴が壁/リブ/ボスに意図せず食い込む**ことは起こる
(過去に取付穴と補強リブが重なった)。自動の健全性チェックでは捕まらない。

- フィーチャ位置は必ずパラメータから導出する (`hole_x`, `gusset_x` 等)。
- `.scad` 冒頭に **`assert()` で最低クリアランスを検査**し、干渉する寸法なら
  ビルドを止める。実装例は `parts/common/jigs/test_bracket/test_bracket.scad`
  (`min_dx = thick/2 + screw_d/2 + clearance`)。
- **穴・ボスが 3 個以上ある面は、個別の assert ではなく「フィーチャ表 + 総当り」に
  すること。** 個別に書くと必ず組合せが抜ける。実装例は
  `child_vtray_deck.scad` の `tops` / `holes` (`[X, Z, 半径, 名前]` の表を作り、
  穴×穴・ボス×穴・スリット×両方を全ペア検査する)。
  **半径には「ねじ頭の座」を入れる** — バカ穴だけ見ると、頭が隣のボスに
  乗っている状態を見逃す (実際に 2 箇所で起きた)。
- **相手部品を「全長」で表す変数は、その全長の中に全部品が収まっていること
  まで assert する。** `child_vtray_batt_box` はゲート板を `box_len` の外に
  置いていたため、`rx_z0 >= box_z0 + box_len` を満たしたまま RX 基板を貫通した。
- ビルド後は `_work/images/<name>_preview.png` の front/top/side で穴と構造部が離れているか**目視**する。
- **assert が止めたら「assert を緩める」のではなく形状を直す。**
  現在 `xdcr_socket` の親機バリアント (tilt 20°) が assert で停止中 — これは正しい挙動。

### 3. 部品外の事項を必ず考慮する

ケーブル・コネクタ・工具アクセス・サービスループ・最小曲げ半径・
ストレインリリーフ・水抜き・カメラ視野・重心。
**部品同士が当たらなくても、これらで成立しない設計は失敗している。**

- 部品の `.md` に「部品外の考慮」節を必ず書く。
- 全体は `docs/配線・ケーブル計画.md` に集約する。部品を足したらここも更新する。
- アセンブリの `.md` に「未反映 (モデルに入っていないもの)」を明記し、
  それが揃うまで**干渉確認は完了していない**と書く。

### 4. 寸法の二重定義に注意

`child_clamp_base` と `child_clamp_strap` のように、**同じ値を 2 ファイルに
書いている箇所がある** (`tube_od` / `fit_clear` / `m4_x` / `band_w` 等)。
片方だけ直さないこと。関係は各 `.md` の「インタフェース」節に書いてある。

## 強度・造形性の検証 (必須)

「見た目が丈夫そう」で設計を終えない。**荷重を N で書いてから形を決める。**
道具は `3d-print-design` スキル (`C:\Users\ryupc\.claude\skills\3d-print-design\`)。
詳細は同スキルの `references/structural-design.md`。

```
1. 荷重ケースを .md に書く (何 N / どこから入る / どこで受ける / 係数)
       係数: 定常 1、取り回し 3〜5、落下 10
2. python scripts\quick_strength.py beam|plate|boss|lug|column|tube_clamp ...
       断面が通るまで直す。ここで落ちる設計は FEA する価値がない
3. .scad を書く → build.ps1
4. python scripts\printability.py <stl> --load-axis <主引張方向>
       X1C 実用枠 250x250x250。姿勢は構造の決定事項 (層間が弱い)
5. python scripts\fea_check.py <study.json> --out <dir>
       mesh resolution が PASS しない限り数値は信用しない
6. たわみと安全率を .md に記録する (どの荷重ケースかを必ず添える)
```

FDM の要点: **層間 (Z) の引張強度は面内 (XY) の 5〜7 割しかない。**
吊り耳・持ち手・ボルトフランジのような引張部材を、層をまたぐ向きに印刷しない。
`printability.py --load-axis` がその姿勢に減点を付ける。

全部品の造形性は一括監査できる (購入品・基板は自動で除外される):

```powershell
python "$S\printability.py" parts --audit --json docs\x1c_audit.json
```

既知の造形性の問題 → 詳細は [docs/X1C造形性監査.md](X1C造形性監査.md):

- **造形枠 (実用 250³) に入らないのは 3 点**: `child_frame_plate` (Y=300)、
  `child_tray_deck` (Y=281)、`child_vtray_deck_t300` (Z=304)。
  分割位置はモデル座標で出るので `.scad` にそのまま入る。接合は
  `assets/scad_modules/joints.scad`。**分割後は接合部を弱点として FEA をやり直す。**
- `child_tray_rib` の最薄部が 0.73mm で、0.4mm ノズルの 2 周 (0.8mm) を下回る。
- `child_shell_aft` は吊り下げ荷重が Z なので、モデル姿勢のまま (+Z 上) 印刷すると
  荷重が層間に直交する。**`+Y 上` で印刷すること** (造形枠にも収まる)。
- クランプ類はオーバーハングが 20〜28% ある。45° 面取りで減らせる (フィレットでは減らない)。

## フレームのトポロジー最適化

ユーザーが最適化形状を直接使うよう指定した場合は、以下の単純なリブへの再構成を行わず、密度場を既存topoptの機能で平滑化する。穴・座面・取付面・ゴム接触面は共通CADから復元し、平滑化・寸法復元を終えた実STLを同じ荷重/材料/拘束条件で再解析する。全荷重ケースと局所応力の制約を最適化側にも含める。原密度場・平滑化条件・材料軸・出力ハッシュを保持し、設計元が取り込む生成メッシュを `manufacturing.json` の `source_dependencies` に記録する。STL由来のSTEPがファセット形状になることは明記する。

閉メッシュでも面積ゼロの三角形を含むことがある。実面積も検査し、必要な部品だけ `manufacturing.json` の `degenerate_edge_flip_files` へSTLの拡張子を除いたファイル名を指定する。build.ps1/build.shは `tools/clean_stl_degenerates.py --configured` でMeshLabのEdge Flipを使い、三角形数・符号付き空洞体積・外形を保ち、双方向の頂点/面中心の表面差0.001 mm以内を検査する。Edge Collapse、デシメーション、穴埋めへの代用はしない。pymeshlabが必要。独立解析用のGmshアダプタはPython版Gmshのnative batchを使い、GUI実行ファイルで失われるエラー出力を記録する。

内部空洞があるSTLの閉じた境界面は複数になるが、物理的には1つの部品であり得る。外向きの外殻と内向きの空洞面を区別して検査する。`stl_to_step.py` は全境界を1つのソリッドにし、空洞を中実の別ソリッドへ変換しない。STLとSTEPの体積を照合し、STEPを読み戻してソリッド数・空洞・外形を確認する。FreeCAD統合テスト `tools/tests/test_stl_to_step.py` は、内部空洞と離れた2つの中実部品の両方を検査する。

`scripts/topo_opt.py`。詳細は同スキルの `references/topology-optimization.md`。

**出力は部品ではなく「材料が要る場所の地図」。** 生メッシュをそのまま部品にしない
(STEP がファセット化して設計規約 1 に反する)。必ず次の順で進める:

1. 細部品を先に設計・配置する → それらが keep-out になり、設計領域が定まる
2. 全荷重ケースを同時に入れて最適化する (1 ケースだけだと他方向に対して機構になる)
   `filter_mm` は最小部材寸法。X1C なら 4mm 以上にしないと再現できない形が出る
3. 出力の `ribs` レポートを見て、**cube / cylinder のパラメトリック .scad に作り直す**
4. 同じ study で `fea_check.py` を回し、最適化解のコンプライアンスと比べる
   (±20% に入っていれば作り直しは成功)

## Fusion 360 連携

詳細は同スキルの `references/fusion360-bridge.md`。

**`.scad` が唯一の正。Fusion は「見る・仕上げる・解析する」場所であって、
形状を定義する二つ目の場所にしない。**

取り込み方は 2 つ。**眺める・断面・干渉確認**なら A、**部品ごとに編集・解析**するなら B。

```powershell
# A. アセンブリ STEP をそのまま開く (ファイル > 開く / データパネルへドラッグ)
#    assemblies\<asm>\<asm>.step — 部品ラベルが名前付きコンポーネントになる (1 ファイル、70MB 級)
# B. 部品 STEP を実配置で個別コンポーネントとして取り込む (bridge 導入済み)
python "$S\install_fusion_bridge.py"                       # 1 回だけ (導入済み)
python "$S\fusion_manifest.py" assemblies\child_interior --root .   # <asm>_fusion.json を作る
# Fusion: ユーティリティ > アドイン > スクリプト > aquabeacon_bridge > 実行 > 1 > その JSON を選ぶ
```

Fusion 側で付けてよいのは**角丸・面取りなど装飾のみ**。書き出しは
`<name>_fusion.step` という別名になるのでビルド成果物を潰さない。
寸法を変えたくなったら Fusion ではなく `.scad` のパラメータを直して再ビルドする。
Fusion で面が選べない (微小面だらけ) 部品は STL→STEP フォールバックで作られたもの
(`hull()` 由来、上記「部品の STEP と STL は同じ座標系」を参照)。

## バリアント (同じ .scad から寸法違いを出す)

部品フォルダに `variants.txt` を置く。

```
# <接尾辞>  <変数=値> ...
child   tilt_deg=0
parent  tilt_deg=20
```

出力は `<name>_<接尾辞>.stl` / `.step` / `_preview.png`。
文字列値は `part="body"` のように書く (build 側でエスケープする)。
バリアントを定義したら**接尾辞なしの成果物は消す** (古いまま残るため)。

## アセンブリ

`placement.json` が唯一の情報源。`<name>_view.scad` は**自動生成なので編集しない**。

```json
{ "part": "parts/child/interior/printed/child_tray_deck",
  "file": "省略時はフォルダ名", "label": "表示名",
  "group": "tray", "color": "Orange", "alpha": 0.35,
  "note": "生成 .scad にコメントとして出る",
  "ops": [ {"translate":[0,141,49.35]}, {"rotate":[0,0,180]} ] }
```

`ops` は OpenSCAD と同じく**外側から順に**適用される
(`translate` → `rotate` → `translate` の入れ子と同じ)。
`mirror` / `scale` も使える。STEP 合成側 (`asm_to_step.py`) が同じ行列を組む。

アセンブリをビルドする前に**構成部品をすべてビルドしておくこと**。
STEP が無い部品は MISSING として飛ばされる。

## 新しい部品を追加するとき

0. **取合い相手を人間に確認して `part_index.py lock --confirmed` で固定する**
1. 荷重ケースを決め、`quick_strength.py` で断面を通す
2. `parts/<unit>/<int|ext>/printed/<name>/` を作り `<name>.scad` を置く
3. 冒頭に用途・取付先・印刷向きのコメント、続けて Customizer 変数、
   導出値、**`assert()` の干渉チェック**を書く
4. `.\build.ps1 parts\...\<name>` でビルドし、preview PNG を目視確認
5. `printability.py` で X1C 造形可否と印刷姿勢を確定する (載らないなら分割)
6. 荷重を受ける部品は `fea_check.py` でたわみと安全率を確認する
7. `<name>.md` を書く (役割 / 主要寸法 / インタフェース / 干渉チェック /
   **荷重ケースと安全率・たわみ** / 印刷向き / **部品外の考慮** / 要確認)
8. `assemblies/<asm>/placement.json` に追加してアセンブリを再ビルド
9. `docs/部品一覧.md` に行を追加する
10. `part_index.py check --root .` が通ることを確認する
11. 基板に取り付く部品なら `scad/lib/verify_child_holes.py` が PASS することを
    確認する (`.kicad_pcb` の実穴との突き合わせ)

## 変更したら合わせて直すもの

| 変えたもの | 一緒に直す |
|---|---|
| 部品の寸法 | 依存する相手部品の `.scad` (二重定義)、両方の `.md` |
| 部品の位置 | `assemblies/*/placement.json`、アセンブリの `.md` |
| 部品の追加・削除 | `placement.json`、`docs/部品一覧.md` |
| ケーブル・貫通部 | `docs/配線・ケーブル計画.md`、関係する部品の `.md` |
| 購入品の選定 | その部品の `.md` (URL と寸法)、依存する `.scad` の変数 |

## README.md について

`README.md` は**人間用**。必要な情報だけを書き、LLM 向けの指示は書かない。
共通作業規約は `AGENTS.md` に集約する。

## 印刷用STLの座標移動と保存精度（2026-10-08）

横置き4枚フレームの設計元は閉メッシュでも、ベッドへ移してバイナリSTLに保存すると、float32の丸めによって微小な辺が潰れ、印刷コピーに開いた辺やゼロ面が発生した。側板・底板・上部で再現。スライス成功だけでは検出できない。

`manufacturing.json` の `portable_stl_export_format: "stl_ascii"` を当該部品に指定し、変換後の座標精度を保つ。`assembly_parts.py sync` は保存したSTLを読み直し、閉鎖性・巻き方向・元メッシュのEuler数とゼロ面数を確認する。形状を平滑化・再構成したり、コピーを手編集して補修したりしない。出所とコピーのSHAは従来どおりmanifestへ記録する。印刷姿勢・鏡像は同じ変換を使う。座標移動だけで四面体の短辺が潰れる再現例を `tools/tests/test_assembly_parts.py` に含める。
