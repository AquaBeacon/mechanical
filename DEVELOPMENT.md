# 開発ガイド

筐体・機構・印刷一式。

OpenSCADとFreeCAD CLIを使用します。assemblies/README.md で構成を選び、parts/PRINT.md から印刷データへ進みます。

## 入口

CAD・STL・3MFはGit LFSで公開しています。Git LFSを導入して `git lfs install`、clone後に必要なら `git lfs pull` を実行してください。LFSデータは約3 GiBです。Windowsでは一部の印刷ジョブのパスが長いため、下記のcloneオプションで長いパスを有効にし、できるだけ短い親フォルダへ取得してください。

- [assemblies/README.md](assemblies/README.md)
- [parts/README.md](parts/README.md)

## 検証

構造解析連携のテストには隣のtopoptパッケージが必要です。`python -m pip install -e "../topopt/topopt[test]"` で導入します。FreeCAD CLIがない環境ではCAD変換の確認範囲が制限されます。

```sh
python -m unittest discover -s tools/tests
```

## データと関連リポジトリ

このディレクトリがGitリポジトリのルートです。親の AquaBeacon-OSS は複数リポジトリの置き場です。横断開発では各リポジトリを同じ親ディレクトリに配置し、[全体の入口](https://github.com/AquaBeacon/workspace-tools)から関連設計へ進みます。単体checkoutでも本書のローカル入口を使用できます。

生データ・生成物・SDK・仮想環境は手元に保持し、公開対象を.gitignoreで区別します。追跡済みのファイルは.gitignoreだけでは除外されないので、`git status --short`と`git ls-files`を確認します。

ライセンスは[Apache 2.0](LICENSE)、第三者部分は[THIRD_PARTY.md](THIRD_PARTY.md)。

## 公開リポジトリ

GitHub: https://github.com/AquaBeacon/mechanical

```sh
git clone -c core.longpaths=true https://github.com/AquaBeacon/mechanical.git
```

公開ブランチはmainです。新設リポジトリは公開対象だけを初期履歴にし、過去の開発履歴と実験ログはローカルに保管します。
