# 部品の設計元

子機は `child/`、親機は `parent/`、共用品は `common/`。機体部品は exterior / interior の下で printed（印刷）、cots（購入品）、pcb（基板）に分ける。治具は `common/jigs/`。

このフォルダは再利用する設計元です。印刷一式は [assembly一覧](../assemblies/README.md) の各 `parts/PRINT.md` から開いてください。

`python tools/part_catalog.py <keyword>` で部品名・設計元・使用構成を検索できます。同じ部品のバリアントは既存SCADとvariants.txtで管理し、assemblyごとに設計をコピーしません。

各部品の確認画像は `_work/images/`、作業ログは `_work/logs/`。製品原本は `ref/` に保持します。
