# フォルダ整理と印刷一式

2026-10-15：リポジトリ名を `mechanical` とし、AquaBeacon-OSS配下へ移動しました。部品・assemblyの内部配置と印刷一式は維持しています。開発手順とGit LFSは [DEVELOPMENT.md](../DEVELOPMENT.md)、全体の対応表は [移行記録](https://github.com/AquaBeacon/docs/blob/main/maintainer/migration.md) を参照してください。

2026-09-27に整理。assemblyの入口は [構成一覧](../assemblies/README.md)。全体のSTEP/STLと同じフォルダの `parts/PRINT.md` から、印刷に必要な部品と数量を確認できる。

## 設計元を増やさず、印刷は1フォルダで完結

共通の設計元は従来の `parts/` と `scad/lib/` に残す。assemblyの `parts/` はそこから生成した実STLの印刷セット。リンクではないので、そのフォルダだけコピーしてスライサに読み込める。

同じ形の必要個数は `placement.json` から集計する。鏡像部品は反転を反映した別STL。スケールは回転を含む配置から導出し、剛体の組立位置は除いている。印刷姿勢を適用後、最小XYZを0へ移動する。モディファイアには対象と同じ変換を適用し、相対位置を保持する。

`manifest.json` に設計元、個数、配置ラベル、印刷変換、元STLと印刷STLのSHA-256を記録する。`check` は配置変更・設計元変更・コピー変更・余分な印刷ファイルを検出する。

基板・購入品・ケーブル・金属部品・フォーム・予約空間は印刷セットへ含めない。printedフォルダにある例外は、その設計元の `manufacturing.json` に明記した。

## 更新

```powershell
# 形状変更時は先に設計元からSTL/STEPをビルドする
.\build.ps1 parts\child\interior\printed\child_vtray_deck
.\build.ps1 -Assemblies assemblies\child_interior

# 既存データの整理・再梱包だけなら
python tools/tidy_workspace.py apply
python tools/assembly_parts.py sync
python tools/assembly_parts.py check
python tools/tidy_workspace.py check
```

`sync` はCADの再ビルドではない。設計元を変更したら先にSTL/STEPを更新する。共有部品を変更したときは全構成を同期する。`python tools/part_catalog.py <keyword>` で設計元と使用構成を検索できる。

有機的な最適化形状を設計元SCADへ取り込む場合、入力メッシュはその部品の `spec/` に置き、`manufacturing.json` の `source_dependencies` に部品フォルダからの相対パスを列挙する。入力STL/密度データの変更も出所検査で検出し、古い印刷STLのまま同期しない。平滑化前の探索メッシュや解析ログは引き続き `_work/analysis/<case>/` に保持する。

近接頂点を持つ有機形状は、部品の `manufacturing.json` に `stl_export_format: "binstl"` を指定してバイナリSTLを出力できる。`build.ps1` / `build.sh` 共通で `binstl` / `asciistl` を受け付け、未指定の部品はOpenSCAD既定形式を使う。形式指定で不良メッシュを許容せず、閉メッシュ・面積ゼロ三角形・取合いを引き続き検査する。

`step_coplanar_merge: true` はSTEP専用入力の同一平面三角形を統合する。`tools/compact_coplanar_mesh.py` の入力・検査記録は `_work/intermediate/` と `_work/analysis/` に保持する。元の印刷STLを変更せず、体積・外形・表面差・閉メッシュの検査後にFreeCADへ渡す。両ビルドスクリプトがこの設定を読む。

## 画像・履歴

確認画像は各assembly・部品の `_work/images/` に集約した。画像の旧サブフォルダ構成はその下で保持している。直下のログは `_work/logs/`、CSGは `_work/intermediate/`。移動先とファイルハッシュは `tools/_work/tidy_journal.json` に記録した。

既存の解析、設計版、スライス設定、ZIPは記録として残す。旧 `prints/` とルート `print_jobs/` は過去の出力・スライス資料であり、新しい印刷データの入口はassembly内の `parts/` とする。従来スクリプトの動的な出力先は旧構成を使う場合があるため、実行後に `tidy_workspace.py apply` を行う。汎用ビルドは整理を自動実行する。

OpenSCAD・FreeCADのCLIとPythonで再現可能なため、今回MCPや追加インストールは必要なかった。

### 任意利用のFreeCAD検討コピー（2026-10-11追加）

`tools/cad_foundation/` は既存設計を変更しないCAD交換CLI、ネイティブ雛形、`freecad` MCPサーバー、配布用スキルを保持する。使い方は [CAD基盤](cad-foundation.md)。出力は `tools/_work/analysis/cad_foundation/<run>/` の `model.FCStd`、STEP/STL、入力スナップショット、検証レポート、`logs/`、`intermediate/` に限定する。既存部品の正本や第二の印刷一式にはしない。MCP用Python環境は `tools/cad_foundation/.venv/` に分離し、Codex設定に `freecad` を登録済み。自動同期・GUI常時接続は行わない。ネイティブFCStdを部品の正本として採用するときも、従来の部品フォルダに1か所だけ置き、説明と製造依存関係を更新する。

## 受け入れ条件

- 各assemblyに `parts/PRINT.md` とmanifestがあり、印刷対象は実STLで同梱されている。
- 必要個数と鏡像が配置から導出され、非印刷モデルが混ざらない。
- 局所充填モディファイアを同梱し、部品との相対座標を維持する。
- 設計定義をassemblyの印刷セットへコピーしない。
- 共通設計元・配置・STLの変更と印刷コピーの手編集を検出する。
- 確認画像と直下の作業ログは `_work/` に収まり、既存文書の画像参照が移動先を指す。

探索だけの `child_single_camera_topopt` は印刷部品未確定と明記している。旧部品には250 mm枠外の形状や `child_top_crown` の非多様体エッジがある。各印刷手順に残し、フォルダ整理を形状・強度の合格判定へ読み替えない。
