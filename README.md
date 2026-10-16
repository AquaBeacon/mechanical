# Body_Models — AquaBeacon 機体設計

Mitou26 AquaBeacon の機体 (筐体・機構パーツ) の 3D 設計リポジトリ。
パラメトリックな **OpenSCAD (.scad)** を設計ソースとして、
**STEP** (Fusion 360 で編集できるソリッド) と **STL** (確認用メッシュ)、
プレビュー画像を書き出す。単位は mm。

**全体モデルと印刷一式は [assembly一覧](assemblies/README.md) から開けます。** 各assemblyの `parts/PRINT.md` に必要なSTLと数量をまとめています。`parts/` だけコピーして印刷できます。

**FreeCAD雛形は [open_template.cmd](tools/cad_foundation/open_template.cmd) をエクスプローラーでダブルクリックして開けます。** リンクで起動できない場合は `tools/cad_foundation/` フォルダから実行してください。表 `Parameters` のB2〜B6で寸法を変更できます。

**[OpenSCAD / FreeCADの使い分け・MCP操作手順](docs/cad-foundation.md)**。`freecad` MCPを実装・登録済みで、ネイティブ生成・検査・寸法変更・STEP/STL出力・組立コピーに対応します。既存設計を上書きせず、独立した `.FCStd` と検証レポートを生成します。STEP取込では元のパラメトリック履歴は復元されません。軽量モデルへの作業分担と更新済み `3d-print-design` スキルの案内も同文書にまとめています。

- 部品一覧と進捗 → [docs/部品一覧.md](docs/部品一覧.md)
- 子機外装の現行・旧構成 → [モデル・組立・印刷の一覧](assemblies/README.md)
- 子機のシンプル筐体（縦置き200 mm・前後2分割＋ガード・M3後付けマウント穴、強度未合格の試作） → [モデル・組立・印刷](assemblies/child_simple_assembly/README.md)
- 配線・ケーブル・工具アクセスなど部品外の事項 → [docs/配線・ケーブル計画.md](docs/配線・ケーブル計画.md)
- 機体設計の全体像 → [docs/AquaBeacon_機体設計.md](docs/AquaBeacon_機体設計.md)
- 購入テザー30 mの輸送・保管リール → [設計・印刷・組立](parts/common/jigs/tether_storage_reel/tether_storage_reel.md)
- テザー30 m・一つの収納部／両側開口／印刷爪で着脱するカバー → [最新試作・印刷・組立](parts/common/jigs/tether_open_reel/tether_open_reel.md)
- 親機外装・小型1プレート版（X1 Carbon、5個を配置済み） → [印刷・組立](assemblies/parent_oneplate/README.md)
- 親機外装・従来M3直接固定版 → [設計](assemblies/parent_direct/README.md)
- 親機外装・従来一体化版 → [設計](assemblies/parent_light/README.md)
- 親機外装・従来の開放フレーム版 → [設計](assemblies/parent_open/README.md)
- 親機外装・従来クランプ案（全面底板） → [設計・データ](assemblies/parent_clamped/README.md)
- 親機外装・底ねじ固定案（カメラ・TD04Aマウント用ねじ穴） → [設計・データ](assemblies/parent_simple/README.md)
- 親機外装・従来の揺れ対策版（最下部センサー、一体型フィン） → [設計・組立・印刷](assemblies/parent_bottom_sensors/README.md)
- 親機の内外装統合（実測前の試作・残る干渉・実測一覧） → [統合モデル](assemblies/parent_integrated/README.md)

## フォルダ構成

```text
mechanical/
├── assemblies/                   全体・内装・構成違いの入口
│   ├── README.md                   モデルと印刷一式の索引
│   └── <name>/
│       ├── README.md / placement.json / 全体モデル
│       ├── parts/                  このフォルダだけで印刷できるSTL一式
│       │   ├── PRINT.md / manifest.json / DESIGN_NOTES.md
│       │   └── modifiers/          必要な局所充填モディファイア
│       └── _work/                  images/・logs/・intermediate/
├── parts/                        部品の設計元（共用品を再利用）
│   ├── child/, parent/             exterior・interior / printed・cots・pcb
│   └── common/                     共用品・ケーブル・治具
├── scad/lib/                     共通寸法・モジュール・CAD変換
├── tools/                        印刷一式の同期・整理・部品検索
├── docs/                         設計・配線・検証と整理方法
├── spec/                         既存の設計固有スクリプト・解析記録
├── print_jobs/                   従来のスライス設定・印刷履歴
└── outputs/                      従来の補助出力・履歴
```

設計元は1か所だけ管理し、assembly側には生成したSTLを配置します。基板・購入品は印刷一式に含めません。確認画像は各フォルダの `_work/images/` に集約しています。

設計元が取り込む最適化メッシュ等は、部品内の `spec/` に保持し、`manufacturing.json` の `source_dependencies` へ列挙します。これらの更新後も、印刷STLの再生成とassemblyの同期が必要です。

細かな有機形状は `manufacturing.json` に `"stl_export_format": "binstl"` を指定できます。両ビルドスクリプトがその部品だけをバイナリSTLで出力し、ASCII出力で近接頂点の小数桁が失われることを避けます。指定可能値は `binstl` / `asciistl`、未指定はOpenSCAD既定のままです。

ファセットSTEPが大きい部品は `"step_coplanar_merge": true` を指定できます。`tools/compact_coplanar_mesh.py` が同一平面の三角形をまとめたSTEP専用入力を `_work/intermediate/` に作り、体積・外形・表面差・閉メッシュを検査してからFreeCADでソリッドへ変換します。印刷STLは変更しません。
詳しくは [整理方法](docs/folder-organization.md)。

上流仕様 (AquaBeacon 仕様書・購入物品リスト) はワークスペース共通の `../docs/` (`Mitou26/AquaBeacon-OSS/docs/`) に一元管理。

### 部品フォルダの中身

| ファイル | 内容 |
|---|---|
| `<name>.scad` | 設計ソース (3Dプリント部品のみ) |
| `<name>.step` | Fusion 360 で開くのはこれ |
| `<name>.stl` | 形状の即確認・スライサ用 |
| `_work/images/<name>_preview.png` | iso / front / top / side の 4 面 |
| `<name>.md` | 寸法・取合い・印刷向き・部品外の考慮・要確認事項 |
| `variants.txt` | 同じ .scad から寸法違いを出す場合のみ |
| `ref/` | データシート PDF、ベンダ配布 zip など |

購入品 (cots) は `.scad` がなく、ベンダのファイル名のまま置いてある。
`.md` に**製品ページ URL と寸法**を記録している。

## ビルド

```powershell
.\build.ps1                                                # 3Dプリント部品を全部
.\build.ps1 parts\child\interior\printed\child_tray_deck   # 個別 (フォルダを指定)
.\build.ps1 -Assemblies                                    # アセンブリ
.\build.ps1 -NoStep                                        # STL + プレビューだけ (高速)
```

Git Bash なら `./build.sh` (引数は同じ、`--assemblies` / `--no-step`)。
STL/STEPは**入力と同じ部品フォルダ**、画像はその中の `_work/images/` に出ます。ビルド後にassemblyの印刷一式も同期します。アセンブリはSTEPと同時にSTLも出力し、
`interior` グループがある場合は軽量な `<assembly>_interior.stl` も生成する。

必要なツール (インストール済み):

- OpenSCAD `C:\Program Files\OpenSCAD\openscad.exe`
- FreeCAD 1.0 `…\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe`
- Python (プレビュー生成に matplotlib)

既存STLから印刷一式だけ作り直す場合：

```powershell
python tools/assembly_parts.py sync
python tools/assembly_parts.py check
python tools/tidy_workspace.py check
```

## Fusion 360 での編集

`<部品フォルダ>/<name>.step` を開く (ファイル → 開く、またはデータパネルへドラッグ)。
STEP はソリッド (B-Rep) として読み込まれ、面・エッジを選択して
押し出し / フィレット / 穴編集ができる。

アセンブリ全体は `assemblies/<名前>/<名前>.step` を開く
(子機内装なら `assemblies/child_interior/child_interior.step`)。
各部品が実配置で、`placement.json` の `label` の名前を持つコンポーネントとして入っている。
部品を個別に編集・解析したいときは `assemblies/<名前>/<名前>_fusion.json` を
Fusion のスクリプト `aquabeacon_bridge` (ユーティリティ > アドイン > スクリプト) で
取り込むと、部品ごとの STEP が実配置の別コンポーネントになる。

> 寸法を変えるときは STEP を直接いじるより、対応する **.scad のパラメータ**を
> 変更して再ビルドするほうがパラメトリックさを保てる。

## 設計上の約束

1. **角丸・フィレットは .scad で作らず Fusion 側で付ける。**
   `hull()` / `offset()` を使うと STEP が微小平面にファセット化されて編集しづらくなる
   (`test_bracket` で 426 面 vs 18 面)。
2. **穴とリブ等の干渉は `.scad` 冒頭の `assert()` で止める。**
   watertight でも意図しない食い込みは起こる。ビルド後にプレビュー PNG でも目視する。
3. **ケーブル・工具アクセス・サービスループなど部品外の事項を必ず見る。**
   部品同士が当たらなくても、これで成立しない設計は失敗している。

## 現在の状態

子機は 12 部品が設計済みで、アセンブリ (STEP + プレビュー) が組めている。
親機は最新外装とP1内装を統合した198部品の試作アセンブリを作成済み。
PWR裏面リードの干渉を修正。SPRESENSE簡易モデルと支持部、テザー引込部と
電池トレイの取合いは実測後に解消する。詳細と現在の残作業は上記統合モデルを参照。

**従来構成の未解決事項** (親機最新版は統合モデルの実測一覧を参照):

1. TD04A 振動子の胴径・胴長の実測
2. チューブ有効内長の実測
3. ケーブルの選定と外径実測 (ペネトレータ型番が決まらない)
4. `xdcr_socket` 親機バリアント (20°) が assert で停止中
5. 基板 3D モデルの入手
6. マストヘッドプレート・防水ボックスマウントの設計

## 開発とライセンス

CAD・印刷データの取得にはGit LFSを使用します。Windowsでは `git clone -c core.longpaths=true https://github.com/AquaBeacon/mechanical.git` で長いパスを有効にしてください。詳しい取得手順は開発ガイドに記載しています。

[開発ガイド](DEVELOPMENT.md)にセットアップ・入口・確認方法をまとめています。自作部分は [Apache License 2.0](LICENSE)。[第三者素材・依存の扱い](THIRD_PARTY.md)も参照してください。
