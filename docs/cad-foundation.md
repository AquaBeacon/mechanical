# OpenSCAD / FreeCAD CAD基盤

2026-10-11。既存設計を移行せず追加したCAD基盤。`freecad` MCPを実装・Codexへ登録済み。共通の実行基盤は `tools/cad_foundation/`。現行の部品・配置・ビルド・印刷一式を自動で上書きしない。

## FreeCAD雛形を開く

1. エクスプローラーで `mechanical\tools\cad_foundation` を開き、**`open_template.cmd` をダブルクリック**する。確認済み雛形の場所を探してFreeCADで開く。古い雛形を自分で変更していた場合も上書きせず、別の確認済み雛形を選ぶか新規生成する。
2. モデルが見えなければFreeCADの「表示 → 標準ビュー → 全体を表示」（`V`、続けて `F`）を使う。
3. 左のツリーの **`Parameters`** をダブルクリックし、値の列 **B2〜B6** を編集する。長さ・幅・厚さ・穴径・穴間隔に対応する。必要ならF5で再計算する。
4. 変更を残すときは「名前を付けて保存」で検討用ファイルを作る。

リンクのクリックがCodex内でファイル表示になる場合、そこで開こうとせずエクスプローラーから実行する。代替はFreeCADの「ファイル → 開く」で `model.FCStd` を選ぶ。チャットでは「FreeCADで雛形を開いて」と依頼すれば `freecad_open_document` を使える。バッチ生成・検査だけの依頼ではGUIを開かない。

```powershell
# ターミナルから開く場合（Body_Models直下）
.\tools\cad_foundation\open_template.cmd
```

## 採用する方針

| 対象 | 設計元 | 人が変更する場所 |
|---|---|---|
| 板、スペーサ、単純な固定具、寸法違いの量産 | OpenSCAD、または既存のPython生成元 | SCADのパラメータ／生成元の寸法 |
| スケッチ拘束、複数フィーチャ、曲面や機構寸法を対話的に調整する新規部品 | FreeCADのネイティブ形状履歴 | Spreadsheetの名前付き寸法、Sketcher、Pad/Pocket等 |
| 既存組立の静的配置・確認 | `placement.json` | JSONが正本。生成FCStdのPlacement編集は検討コピー |
| 関節・開閉動作のある機構 | 部品の設計元＋機構定義 | FreeCADの関節・拘束を段階導入。現段階のFCStd出力は動作拘束を持たない |
| トポロジー最適化後の有機形状 | 最適化密度場／メッシュ＋直接平滑化工程 | 元工程の条件と局所的な機能面。単純図形に作り直さない |

**形状の単純さだけで決めず、「どの寸法を誰が変更するか」で選ぶ。** 単純な板でも、人が頻繁に穴位置を変更するならFreeCADネイティブが適する。既存のPython生成設計を、編集可能性のためだけにSCADとFreeCADへ二重実装しない。

ネイティブ部品も正本は1つ。採用時に、(A) FCStdを人が編集する正本にする、または (B) Python生成元を正本にしFCStdは生成物にする、のどちらかを部品説明に記録する。後者のFCStdに加えた手修正は、生成元へ戻さなければ次回再生成で失われる。既存部品の正本は今回変更しない。

## 履歴から引き継いだ判断

このディレクトリにはGit履歴がないため、以下は保存済み文書・生成コード・検証記録を根拠にしている。

| 既存の問題・事実 | 今回の対応 |
|---|---|
| WTE4のベンダSTEPとSTLで原点が異なった | 組立に読むSTEPとSTLの外形を照合。異なる場合は停止し、自動で位置合わせしない |
| CSG取込でhull等が失われ、STEP体積が大幅減 | 閉じた参照STLがある場合はSTEP体積も照合。STEPが読めたことだけで合格にしない |
| 古いSTLやSTEPを再利用し、更新したつもりになる | 毎回新しい実行フォルダ。入力SHA-256、出力SHA-256、再読込検証を記録 |
| 部品・配置・印刷コピーが混同される | 既存の正本と `assembly_parts.py` を維持。新ツールに製造物への書戻し機能を持たせない |
| ラッチにJSON→Python→SCADの生成系が既にある | 生成元を引き継ぐ。新しい部品ファイルを並列に設計しない |
| STL座標移動後のfloat32丸めで微小な辺が潰れる | 印刷STLは既存の再読込検査を継続。FCStd用コピーから印刷一式を差し替えない |

根拠：[設計事故と検証手順](design-workflow.md)、[既存組立STEP生成](../scad/lib/asm_to_step.py)、[CSG変換検査](../scad/lib/csg_to_step.py)、[ラッチ設計元](../parts/common/jigs/over_center_latch/README.md)、[印刷出所管理](folder-organization.md)。旧文書の「角丸をFusionで付ける」は当時の経路の説明で、新規FreeCADネイティブ部品では最終形状に含めてSTEP/STLへ同じ形を出す。最適化形状を基本図形へ置換する根拠にはしない。

## すぐ使える機能

リポジトリ直下で実行する。追加パッケージ不要。Pythonと既存のFreeCADCmdを使う。

```powershell
# 読み取りのみ。対象、個数、使用STEP/STL、欠落をJSONで表示
python tools/cad_foundation/cli.py plan assemblies/over_center_latch

# 既存8部品から、自立したFreeCAD確認・配置編集ファイルを作成
python tools/cad_foundation/cli.py assembly assemblies/over_center_latch

# 寸法編集可能なネイティブ雛形。製品の部品ではない
python tools/cad_foundation/cli.py demo
```

コマンドは生成した `model` と `report` の絶対パスをJSONで返す。`model.FCStd` はFreeCADで普通に開く。既存GUIは起動・操作しない。FreeCADが見つからなければ `FREECADCMD` 環境変数または `--freecad <freecadcmd.exeのパス>` を指定できる。

今回生成して再読込まで確認したもの： [ラッチ組立FCStd](../tools/_work/analysis/cad_foundation/20261011T072456Z_523ac72c/model.FCStd) / [その検証結果](../tools/_work/analysis/cad_foundation/20261011T072456Z_523ac72c/report.json)、[寸法編集できる雛形FCStd](../tools/_work/analysis/cad_foundation/20261011T072512Z_55ebb6eb/model.FCStd) / [その検証結果](../tools/_work/analysis/cad_foundation/20261011T072512Z_55ebb6eb/report.json)。いずれも生成時点の検討コピー。

- `plan` はCADエンジンを起動せず、ファイルを作らない。`items` と旧 `parts`、バリアントの `file` を読む。欠落があれば終了コード1。
- `assembly` は原本を読み取り、入力を実行フォルダへコピーして処理する。部品の欠落は全体失敗。プレビューで非表示のグループも含め全行を取り込む。
- STEP/STP優先、無ければSTLを **メッシュ参照** として取り込む。重いメッシュ→ソリッド変換を自動実行しない。ネイティブFCStd設計元からの履歴付き組立取込は未実装。
- 並進・回転はFreeCADのPlacementに保持。鏡像・スケールは形状へ適用し、オブジェクトの `TransformMode` に記録。`SourcePath` / `SourceSHA256` / `SourceOps` / `Editability` を各部品に付ける。
- 部品は編集しやすい個別の `Part::Feature` または `Mesh::Feature` としてグループ化。同じ部品の変更を全インスタンスへ連動させるApp::Linkや関節拘束は、今回の静的コピーには含めない。
- 40部品超は既定で停止。計画を確認して必要なら `--max-components 200` 等で明示的に増やす。既定タイムアウト120秒、`--timeout` で変更可能。並列CAD処理や全構成の自動再ビルドはしない。
- 専用設定ファイルでFreeCADCmdを起動する。常用FreeCADの設定・プラグインは変更しない。MCPはCodex起動時にローカルstdioサーバーとして読み込まれ、GUIへ常時接続しない。

### 「開ける」と「寸法編集できる」の違い

| ファイルの中身 | できること | 復元されないもの |
|---|---|---|
| STEP→FCStdのB-Rep | 配置変更、面を使った追加加工、直接形状編集の起点 | 元のスケッチ拘束、寸法名、設計意図 |
| STL→FCStdのメッシュ | 配置・参照表示、メッシュとしての加工 | 円柱面・穴フィーチャ・寸法履歴 |
| ネイティブFCStd | Spreadsheetと形状履歴の編集・再計算 | 自動的な実機適合や強度保証 |

`demo` はSpreadsheet `Parameters` → 拘束スケッチ `Outline` → `Pad` → 穴スケッチ `Holes` → `Pocket` を作る。FreeCADでParametersのB2〜B6を編集する。長さ・幅・厚さ・穴径・穴間隔は説明用の値で、実取付先の設計ではない。長さ80→100 mmで体積が3,600 mm³増え、戻すと元の形状になることを**保存・再読込後**に自動確認する。任意の寸法の組合せを保証する汎用部品テンプレートではない。

ネイティブ雛形はPython用の独自Proxyを使わないので、生成スクリプトをインストールしなくてもFreeCAD標準のフィーチャを編集できる。表と寸法を連動する仕組みは [FreeCAD公式Spreadsheet資料](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Spreadsheet_Workbench.md) と [式の資料](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Expressions.md) に基づく。

## 出力・競合・検証の境界

```text
tools/cad_foundation/                 CLI、FreeCAD処理、ネイティブ雛形
  skills/cad-foundation/SKILL.md       将来の配布に添付するスキル原稿
tools/_work/analysis/cad_foundation/<UTC時刻_識別子>/
  job.json                           使用入力・ハッシュ・配置・実行ID
  model.FCStd                        独立した検討コピー
  report.json                        FreeCAD版、再読込結果、編集検査、限界
  intermediate/                      入力スナップショットと専用設定
  logs/freecad.log                    この実行だけのログ
```

既存のrunは上書きしない。原本がコピー中または処理中に変われば失敗とし、出力を現行モデルとして採用しない。失敗runも原因確認用に残す。新ツールの正常終了はプロセス終了コードだけでなく、今回のIDと一致する検証レポートが `passed` の場合に限る。

検証するのは、STEPの有効ソリッド、STEP/STLの外形差0.5 mm以内・閉じたSTLとの体積差2%以内、FCStd再読込後の外形・体積・ソリッド数／メッシュ状態の保持。これらは旧変換の誤りを検出する粗い整合検査であり、穴位置や表面全体の一致を証明しない。閉じていない参照STLとSTL不在はレポートに明示する。

**SCAD・Python生成元に対するSTEP/STLの最新性、実取付穴、干渉、可動範囲、ケーブル・工具通路、最小肉厚、強度は別の検証。** `passed` はCAD交換と再読込の検査結果であり、製造承認ではない。正本変更時は従来の再ビルド・同期・検査を実行する。

## 人の修正を正本へ戻す手順

1. 生成FCStdを別名保存し、変更した部品・寸法・配置を記録する。元runは比較用に保持する。
2. 位置変更は部品のSourcePath / SourceOpsとJSONの該当行を照合し、正本の `placement.json` へ反映する。鏡像・スケール込みの配置を単純なXYZ角へ転記しない。現在は自動逆変換を提供しない。
3. 形状変更は、その部品の既存SCAD・Python生成元へ戻す。FreeCAD正本へ移行する場合は対象部品単位で明示し、生成・製造依存関係も切り替える。検討コピーを無言で正本へ昇格しない。
4. 対象だけ再ビルドし、形状・干渉・実寸の検証後に既存 `assembly_parts.py sync` / `check` を使う。FCStdコピーを印刷セットの原本にしない。

今回のツールは1までを補助する。作業中のCADに対して2〜4を自動で実行しない。

## モデルを使い分ける

| 仕事 | 担当の目安 | 渡す情報 |
|---|---|---|
| 寸法・取合いが確定した単純部品、既存バリアント追加 | 利用可能な軽量モデル、明確な実装はmedium | 既存設計元、確定寸法、座標、加工・印刷制約、合否条件、所有ファイル |
| 説明追記、寸法表抽出、既知結果の要約 | 軽量モデル、low | 対象ファイルと必要な出力だけ |
| 独立した検査の実行 | 軽量〜バランス型、medium | 検査コマンドと受け入れ条件。設計合格を推測させない |
| 新しい取合い、荷重条件、機構、topopt、原因不明の不具合 | 主担当／高性能モデル | 判断に必要な根拠と失敗の最小再現 |

主担当が部品の役割・取合い・許容差を確定し、実装担当はその範囲で作る。軽量担当も実際のレンダリング、メッシュ、寸法等の検査を省略しない。取合いの不確定、仕様変更が必要、同じ原因の失敗が続く場合は主担当へ戻す。同じ長文履歴を全員に渡さず、結論・変更ファイル・検証結果・未解決点だけ返す。小さな単独作業では委任の起動コストを避ける。

モデル名を永続設定に固定せず、その環境で利用可能なモデル・effortを選ぶ。委任時のツール引数へモデル・effortを明示し、全履歴forkによる親モデルの継承に注意する。この作業では `gpt-6-luna` / medium を指定し、雛形と単体テストの実装を分担した。速度・トークン削減率は測定しておらず保証しない。

## 登録済みMCPと更新済みスキル

[添付スキル](../tools/cad_foundation/skills/cad-foundation/SKILL.md) はリポジトリ内の配布原稿。普段の入口となる **`C:\Users\ryupc\.agents\skills\3d-print-design\SKILL.md` も直接更新済み**で、FreeCADの分岐と `references/freecad-workflow.md` を追加した。印刷姿勢・穴形状・全エッジの仕上げに関する既存ルールは保持している。旧スキルは `tools/_work/analysis/cad_foundation/skill_update_backup/SKILL.md` に保存。

サーバー名は `freecad`。専用 `.venv` のMCP Python SDK 1.30.0を使用し、`C:\Users\ryupc\.codex\config.toml` に登録済み。既存設定の内容を保持し、設定バックアップは同ディレクトリの `backups/cad-foundation/` に保存した。サーバー起動待ち30秒、ツール待ち300秒、FreeCAD個別処理の既定120秒・上限240秒。

| MCPツール（実装済み） | 入力 | 処理と戻り値 |
|---|---|---|
| `freecad_status` | なし | 実行環境、FreeCADCmd、workspace |
| `freecad_plan_assembly` | placement、offset、limit | 読取専用の構成・欠落・編集可能性 |
| `freecad_export_assembly` | placement、max_components、timeout | 独立した組立FCStd、検証レポート |
| `freecad_create_demo` | timeout | 寸法履歴付きFCStd、STEP/STL、再読込・編集検査 |
| `freecad_build_native` | generator、parameters、dependencies | レビュー済み生成元からFCStdとSTEP/STLを作る |
| `freecad_inspect_document` | path、offset、limit | FCStd／STEP／STLの物体名・形状・寸法表エイリアスを検査 |
| `freecad_edit_parameters` | path、updates、sheet、object_names | 寸法表の名前付き入力を変更した別FCStdとSTEP/STL |
| `freecad_export_document` | path、object_names | 指定した最終ソリッドのSTEP/STLとFCStdコピー |
| `freecad_read_report` | run_id | 保存した検証結果 |
| `freecad_open_document` | path | 明示依頼時だけFreeCAD GUIを起動して保存済みモデルを開く |

パスは設定されたworkspace内に限定。生成・検査のFreeCAD処理はworkspace単位のOSロックで同時実行を避ける。FreeCAD子プロセスの標準入力は閉じ、MCP通信の入力を誤って読まない。`open_document` 以外はGUIを起動しない。

### 次回の接続確認

新しいチャットで `freecad_status` を呼ぶ。ツールが表示されなければ **Codexの設定 → MCP servers → freecad → Restart** を使う。作業中のアプリ全体を自動再起動はしていない。登録内容は `codex mcp get freecad` で確認できる。設定の共有とRestart操作は [OpenAI公式MCP手順](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) を参照。

再セットアップ時のみ：

```powershell
python -m venv tools/cad_foundation/.venv
tools\cad_foundation\.venv\Scripts\python.exe -m pip install -r tools/cad_foundation/requirements.txt
python -X utf8 tools/cad_foundation/register_mcp.py
```

登録スクリプトは既存の同名サーバー設定が異なる場合に停止し、無関係な設定を変えない。同じ設定なら何も追加しない。MCP本体は `mcp_server.py`、操作本体は `service.py` と既存CLI／FreeCAD workerに分離した。SDKの [stdio仕様](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) に従い、ログは通信stdoutへ混ぜない。

### 新規ネイティブ部品の生成契約

`freecad_build_native` は `parts/`・`spec/`・`tools/cad_foundation/recipes/` 内の**レビューしたPython生成元**を実行する。コード文字列・shell commandをMCP引数で受け取らない。生成元は信頼済みの実行コードであり、サンドボックスではない。`build(doc, parameters)` は渡された文書に標準フィーチャを作り、最終物体のリストを返す。原本・設定・外部ファイルへ書き込む副作用を含めない。生成スクリプトも正本として従来の部品フォルダ／specへ置く。

同梱例は `tools/cad_foundation/recipes/plate.py`。呼出例：

```json
{
  "generator": "tools/cad_foundation/recipes/plate.py",
  "parameters": {"length": 90},
  "dependencies": ["tools/cad_foundation/native_template.py"]
}
```

相対importや入力ファイルは `dependencies` へ明記し、コピーしたソースだけから再生成できるようにする。生成元や依存ファイルを実行中に変更すると失敗にする。独自Python ProxyよりFreeCAD標準のSketcher・Pad/Pocket・Part・Spreadsheetを使い、人のPCで再編集できる履歴を残す。最終形状の名前はFCStdの `CADFoundationInfo.OutputNames` に記録する。

`edit_parameters` は `{"length": 100}` のような既存のエイリアスと有限の数値を受け取り、その入力の単位を保持する。セル番地や計算式の上書きは受け付けない。生成履歴の `Body` と途中の `Pad` を同時に書き出すなどの重複は拒否する。任意の手作成FCStdは、まずinspectで名前を確認し、`object_names` に最終ソリッドを明示する。外部ドキュメントリンクを持つFCStdの依存梱包は未対応。

**新規部品の形状・寸法履歴を作れるが、関節の自動推定・動作保証は行わない。** 非同期ジョブ管理・取消、形状履歴付き組立App::Link、GUI配置の正本への差分反映、製造正本への自動採用は後続機能。現在の静的placementから関節の種類を推測しない。

## 受け入れ条件と実施結果

```powershell
python -m unittest discover -s tools/tests -p "test_cad_foundation*.py" -v
tools\cad_foundation\.venv\Scripts\python.exe -X utf8 tools/cad_foundation/smoke_mcp.py --from-config
python -m unittest discover -s tools/tests
python tools/assembly_parts.py check
python tools/tidy_workspace.py check
```

| 受け入れ条件 | 確認 |
|---|---|
| `plan` が元ファイルも生成物も変更しない | 一時fixtureの全ファイルを前後比較 |
| `items` / 旧 `parts`、バリアント、行順、グループを保持 | 単体テスト |
| 欠落、領域外パス、不正な変換を検出 | 単体テスト、実行時の全体失敗 |
| 並進・回転順、鏡像、非等方スケールが正しい | FreeCAD実機で既知寸法のソリッドとメッシュを数値比較 |
| 原本を保存先に使わず、既存FCStdを上書きしない | 新run限定、スナップショット検査、上書き拒否の実機テスト |
| 原点ずれSTEPを黙って採用しない | 100 mmずらした合成入力が失敗する実機テスト |
| FCStdを開き直しても形状が一致 | 合成fixtureと既存ラッチ8部品で確認 |
| 人が使う標準フィーチャに寸法変更が伝播する | ネイティブ雛形を再読込して80→100→80 mmを確認 |

基盤テストは17件すべてPASS。全体42テストは41件PASS・既存材料JSON欠落の1件ERROR。入力コピー中の編集、計画後の配置編集、同時処理、MCP操作入口のパス・値制約も確認した。登録済み設定から実サーバーを起動するstdio結合試験は7シナリオPASS（初期化・10ツール列挙、境界拒否、ネイティブ作成と検査、寸法編集、STEP/STL出力、生成元＋依存コピー、鏡像付き組立）。[登録済みMCPの検証記録](../tools/_work/analysis/cad_foundation/stdio_ncs88i6g/smoke-report.json)。

GUIでの操作感や画面表示は未確認。実機のFreeCADCmd 1.0.0で保存・再読込・形状再計算を検証した。新規製品形状、強度合格、既存製造セットの不具合修正は今回の成果に含めない。

2026-10-11の全体チェックでは、今回変更していない次の問題が残った。現行設計を妨げないため修復・同期・移動は実施していない。

- 既存の `test_clamp_bambu_material` が `parts/child/exterior/printed/child_wte4_suspension_clamp/spec/bambu_petg_basic_material.json` の欠落でエラー。
- `assembly_parts.py check`：`child_interior` の `child_flange_brace.3mf` / `child_rx_edge_clamp_base_pair.3mf` が未管理。`parent_oneplate` はCAD/config出所の変更を検出。その他25構成はPASS。
- `tidy_workspace.py check` はPASS。今回のスキルは `python -X utf8 .../skill-creator/scripts/quick_validate.py` でPASS（Windowsの既定cp932読込を避ける）。
