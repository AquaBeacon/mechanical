---
name: cad-foundation
description: Body_ModelsのOpenSCAD・FreeCAD設計元を選び、登録済みFreeCAD MCPでネイティブ生成・組立コピー・寸法編集・STEP/STL出力を行う。既存CADを二重管理せず、軽量モデルへの作業委任も支援する。
---

# CAD foundation

Body_Models用の配布原稿。リポジトリ外へインストールするときも、作業対象のBody_Modelsルートを確認してから下記の相対パスを解決する。現在は `freecad` MCPを登録済み。普段使う `3d-print-design` スキルもFreeCAD対応へ更新済み。

## 最初に読むもの

ルートの `AGENTS.md` と対象assemblyのREADME・placement・parts/manifest、対象部品の説明を読む。設計元の選択やFreeCAD編集の依頼なら `docs/cad-foundation.md` の該当節を読む。全履歴・全解析ログを一度に読み込まない。新規部品の前に `python tools/part_catalog.py <keyword>` で既存設計を探す。

## 設計元と編集可能性

- 確定寸法の単純形状・バリアントはOpenSCADを基本とし、既存のPython生成元があればそこを直す。
- 対話的な寸法変更、複雑なフィーチャ、機構設計にはFreeCADネイティブを検討する。単純形状でも人が頻繁に編集するならネイティブが適する。
- SCAD、Python、FCStdのどれが正本かを部品ごとに一つ定める。既存設計を勝手に移行しない。生成FCStdの手修正を再生成で消さないよう、別名の検討コピーとする。
- STEP取込は形状・配置を編集する起点で、元の寸法履歴は復元しない。STL取込はメッシュ参照。ネイティブのSpreadsheet・Sketcher・Pad/Pocketと区別して伝える。
- topoptの生メッシュを印刷部品へ昇格しない。最適化密度／メッシュを直接平滑化し、機能部だけ局所復元する。単純なリング・柱・梁へ再構成しない。

## 既存設計を妨げない利用

まず `freecad_status`。配置は `freecad_plan_assembly` → `freecad_export_assembly`、新規ネイティブ部品はレビュー済み生成元から `freecad_build_native`、既存FCStdは `freecad_inspect_document` → `freecad_edit_parameters` / `freecad_export_document` を使う。操作仕様は `docs/cad-foundation.md`。`build(doc, parameters)` の生成元は信頼したコードだけを実行し、依存ファイルを明記する。関節拘束・GUI変更の自動書戻しは未対応。

ユーザーが雛形の表示を求めた場合は `tools/cad_foundation/open_template.cmd`、または `freecad_open_document` を使う。ParametersのB2〜B6で寸法編集できる。MCPが見えないときだけ設定のfreecadサーバーを再起動し、再接続までの代替は以下のCLI。

```powershell
python tools/cad_foundation/cli.py plan assemblies/<name>
python tools/cad_foundation/cli.py assembly assemblies/<name>
python tools/cad_foundation/cli.py demo
```

`plan` は読取専用。`assembly` / `demo` は `tools/_work/analysis/cad_foundation/<run>/` に独立コピーを作り、絶対パスをJSONで返す。40部品の既定上限を上げる前に対象を確認する。作業中のGUI・常用設定・モデル正本・印刷一式を変更しない。実装は `tools/cad_foundation/` にあり、CLIかそれを包むMCPを使う。未提供のMCPを呼べると仮定しない。

今回のrun IDと一致する `report.json` がpassedであることを確認する。成功終了・ファイル存在だけで検証済みとしない。原本変更、入力欠落、STEP/STL差異、タイムアウトはレポート／ログを調べる。元モデルの変更を避けるための無関係な再ビルド・同期・整理は実行しない。

配置変更を採用する場合は `placement.json` へ戻す。現在は自動逆変換なし。鏡像・スケールは形状に焼き込まれ、PlacementのXYZだけでは元のopsを復元できない。形状変更は正本へ戻して対象を再ビルドし、既存の検証・印刷同期を行う。

## 軽量モデルへの委任

寸法・取合い・加工条件・合否条件が確定した独立部品や説明更新は、利用可能な軽量モデルへ委任できる。仕様が明確な実装・検証はmedium、単純な抽出・文書更新はlowを目安にする。小さな単独修正は直接処理してよい。主担当のモデル設定を変えない。

委任ツールの引数でモデルとeffortを指定する。全履歴forkが設定を継承する環境では、履歴なしと必要なbriefを渡す。指定値・実際の設定を確認できない場合、安く実行できたと断言しない。委任先には次を渡す。

- 所有ファイルと既存設計元、関連する取合いだけ。
- 確定寸法・座標・単位・公差、荷重／材料／印刷姿勢の既知条件。
- 出力形式と合否条件、実行可能な検証コマンド。
- 他の作業者が同時作業中であり、他者の変更を戻さないこと。

返答は変更ファイル・検証結果・未解決点に絞る。新しい取合いの選定、強度条件、複雑な機構、topoptや原因不明の失敗は主担当が判断する。担当の能力に関係なく形状・実寸・干渉の検証を省略しない。速度やトークン削減率を保証しない。

## 納品

FCStd・検証レポートのパスと、何を編集できるかを示す。CLIのpassedは交換・再読込の検証だけで、動作・干渉・強度・製造承認ではない。新規部品の公開や印刷セットへの採用には元のAGENTS.mdの検証を適用する。
