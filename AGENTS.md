# Body_Models 作業規約

## 設計と配置の正本

- トポロジー最適化の後処理は、最適化メッシュ／密度場を直接平滑化して使う。荷重経路を参考にしただけのリング・柱・梁などの単純図形へ置き換えない（2026-10-05ユーザー指定）。取付穴・ねじ座面・接触面などの機能寸法だけを局所的に復元し、連結性・最小肉厚・干渉・変更後の強度を再検証する。失敗時は最適化条件か平滑化条件を修正し、単純図形への再構成で代用しない。

- mm単位。OpenSCAD、Python生成CAD、FreeCAD CLI、STL/STEPを使用する。
- 単純な部品・確定寸法のバリアントはOpenSCADを基本とする。人が寸法・スケッチ履歴を編集する部品や複雑な機構はFreeCADネイティブを使う。SCAD／Python生成元／FCStdの正本を部品ごとに1つ定め、STEP取込を元の設計履歴の復元と扱わない。
- 部品定義は `parts/<unit>/<exterior|interior>/printed/<part>/` に1か所だけ置く。共用品は `parts/common/`、治具は `parts/common/jigs/`。基板は `pcb/`、購入品は `cots/`。
- `scad/lib/` の共通寸法・モジュールを再利用する。同じ部品をassemblyごとに設計し直したり、寸法定義をコピーしたりしない。
- 配置・バリアント・必要個数の正本は各assemblyの `placement.json`。`items` が標準、既存リールの `parts` も読み込める。`file` でバリアントを指定する。
- 既存のPython生成CADは元の生成スクリプトを更新する。出力SCADと生成スクリプトを別々の設計にしない。
- 既存の実験・旧版は勝手に現行部品へ昇格しない。旧版を再利用する場合はassemblyの文書と取合いを確認する。
- 「おもりA/B/C」は `parts/common/exterior/cots/ballast_inventory.json` の名称・モデル対応・1個あたりの質量を参照する（A=60 g、B=60 g、C=1000 g）。人向け索引は `docs/部品一覧.md`。CAD体積から申告質量を上書きしない。

## 毎回の開始時

1. 対象の `assemblies/<name>/README.md`、`placement.json`、`parts/manifest.json` と関連部品の説明を読む。
2. 新規部品を作る前に `python tools/part_catalog.py <キーワード>` で既存の設計元・使用assemblyを検索する。同じ機能・取合いなら既存部品または同じSCADのバリアントを使う。
3. 新しい取合い相手の型番・寸法・構成が未確定なら確認する。今回または既存記録で確認済みの選択は引き継ぎ、同じ確認を繰り返さない。仮寸法は文書と変数に明記する。
4. `assemblies/README.md` の索引で内装・全体・旧構成を区別する。フォルダ名や更新日時だけで現行版を選ばない。
5. FreeCAD作業は登録済み `freecad` MCPの `freecad_status` で環境を確認し、[CAD基盤](docs/cad-foundation.md) の該当操作を使う。OpenSCADは既存 `cad` MCPを使える。MCPが未接続なら同じCLIを使い、別の生成系を作らない。

## フォルダの役割と納品

```text
assemblies/<name>/
  README.md                  全体モデル・組立・状態の入口
  placement.json             配置の正本（ある構成のみ）
  print_config.json           追加部品・モディファイア等の例外（必要時のみ）
  <name>.step / .stl          組立モデル（既存の別名も保持）
  <name>_view.scad            確認ビュー。自動生成なら編集しない
  parts/                     このフォルダだけコピーして印刷できる実ファイル一式
    *.stl                    印刷用。ソースではなく自動生成コピー
    PRINT.md                 数量・姿勢・材料・注意事項
    DESIGN_NOTES.md           設計元文書の控え
    manifest.json            元ファイル・個数・変換・SHA-256
    modifiers/               スライサ用モディファイア。部品として印刷しない
  _work/
    images/                  操作用スクリーンショット、プレビュー、解析図
    logs/                    ログ
    intermediate/            CSG等の中間ファイル
```

- 人が使う印刷データの入口は必ず `assemblies/<name>/parts/PRINT.md`。印刷に必要なSTLとモディファイアを同じ `parts/` 内へ含める。リンク・シンボリックリンク・他フォルダのSTLを読ませる構成で納品しない。
- `assemblies/*/parts/` のSCADを新しく作らない。STLコピーを直接編集しない。共通部品の設計元を直して再ビルド・同期する。
- `manufacturing.json` の `non_print_files` で、printedフォルダに同居する金属部品・フォーム・予約空間を除外する。購入品を印刷部品へ分類しない。
- 印刷向きは設計元の `manufacturing.json` の `print_rotations_deg` に保存する。assembly固有の変更のみ `print_config.json` の `orientations` を使う。組立の移動・回転と印刷姿勢を混同しない。
- 鏡像とスケールは生成ツールがSTLへ反映する。左右部品を同じSTL2個として数えない。モディファイアには対象部品と同じ変換を掛ける。
- ビューだけ・最適化の探索だけの構成は `exploration_only` と明記する。最適化生メッシュを印刷用部品として配布しない。
- 既存 `prints/`・`print_jobs/`・ZIPは履歴・スライス設定の資料。新しい設計原本や第2の印刷一式を作らない。必要な3MFを納品する場合はassembly内の `print_jobs/` にまとめ、対象STLのハッシュと材料・設定を添える。

## 作業ファイルを散らかさない

- assembly・部品ごとに、そのフォルダ内の `_work/images/` へすべての確認用画像を保存する。ルートにPNG、スクリーンショット、操作画像を置かない。
- ログとCSGはそれぞれ `_work/logs/`、`_work/intermediate/`。新しい解析・試行は `_work/analysis/<case>/` にまとめる。既存解析のデータ構成・原本は保持する。
- 部品フォルダにも同じ `_work/` 規約を適用する。メーカー資料の原本は `ref/` に保持し、LLMが作る確認画像を原本へ混ぜない。
- 再生成用コードは `tools/`（汎用管理）または既存 `spec/`（設計固有）へ置く。`final2`、`new`、`tmp` の並列フォルダを増やさない。
- 履歴を消して整理しない。移動は参照を更新し、モデルを変更せず、移動記録を保持する。

## コマンドと完了前の検証

```powershell
python tools/part_catalog.py child_vtray     # 既存部品と使用構成を探す
.\build.ps1 parts\child\interior\printed\child_vtray_deck
.\build.ps1 -Assemblies assemblies\child_interior
python tools/tidy_workspace.py apply       # 旧スクリプト実行後の画像・ログ整理
python tools/assembly_parts.py sync child_interior
python tools/assembly_parts.py check       # 全印刷一式の出所・個数・古さを検査
python tools/tidy_workspace.py check       # 画像と中間ファイルの散在を検査
python -m unittest discover -s tools/tests
```

- `build.ps1` / `build.sh` は画像を `_work/images/` に出し、印刷一式を同期する。設計固有の旧スクリプト実行後も必ず整理・同期・検査を行う。
- `sync` は既存STLからの再梱包。CADを再生成する操作ではない。SCAD・Python生成元・共通寸法を変えたら、先にSTL/STEPを再ビルドする。
- 配置・設計元・STL・モディファイアの変更、数量の不一致、コピーの手編集を `check` で検出する。指摘を無視して完成扱いしない。
- 新規の形状変更ではOpenSCADレンダリング、閉メッシュ、STEP/STL外形・体積、組立干渉、実取付穴、ケーブルと工具の通路を確認する。強度を主張するときは荷重・材料・積層方向・メッシュ収束の根拠が必要。
- 既存の非多様体メッシュや造形枠外部品は印刷手順に明記する。`known_mesh_issues` は既知不具合の記録専用で、新しい不具合を通すために追加しない。
- 詳しい既存CAD検証手順と寸法事故の記録は [設計・検証手順](docs/design-workflow.md) にある。関連する形状を変更するときに参照する。

## 文書・ツールを合わせて更新する

- 部品変更はその説明、使用assembly、印刷一式、必要に応じて `docs/部品一覧.md` を同じ作業で更新する。
- 構成・配置・印刷条件を変えたらassemblyのREADMEと設定を更新する。配線変更は `docs/配線・ケーブル計画.md` に反映する。
- 整理規約とコマンドを変更したら `README.md`、`docs/folder-organization.md`、対応ツールを更新し、docsの増減時は `docs/README.md` も更新する。
- OpenSCADとFreeCADのCLIを再現可能な実行基盤とし、通常の操作入口は既存 `cad` MCPと追加した `freecad` MCPを使う。FreeCAD出力は独立runへ保存し、正本へ戻すときだけ部品・配置・製造依存関係を明示的に更新する。GUIを開くのはユーザーが表示・編集を求めたときに限る。
- PowerShell 5.1対応を保つ。`build.ps1` はUTF-8 BOM付き、JSONはBOMなしUTF-8。FreeCAD CLIの入出力は既存の環境変数で渡す。
