# 親機：電池下の工具穴とスライド蓋のねじ座

2026-10-13。電池下の防水容器固定ねじへ工具を通す穴を、4.2 mmから有効径8 mmへ拡大。12角の補正穴で、両入口を0.2 mm面取りした。変更は上側の電池台。最下段 `floor_plate`、MAIN固定板、GNSSのコード巻き部のSCAD・STEP・STLは同じSHA-256を維持する。コード巻き部の改訂はユーザーの取消しにより採用していない。

## 蓋とナット

蓋は子機を参照した端フック2本を使用。南2 mmへずらした位置で載せ、北へ2 mmスライドして嵌める。M3×12ねじとM3ナットを各1個で固定する。外すときはねじを外し、南2 mmへ戻して上へ抜く。電池の収納寸法、配線端40×26 mm開口、蓋下面Z49／上面Z52と既存フォーム4枚を維持する。

ナット座の水平天井を、六角穴からねじ穴へ絞る斜め天井へ変更。側面の差込み口は50°の三角屋根で、入口上辺を0.1 mm面取りした。六角ナット座AF5.8 mmと底面Z41.5を維持し、AF5.5／厚2.4 mmのM3ナットを側面から入れる。組立モデルのナットをZ90°回して、穴の六角方向へ合わせた。内部の六角保持角と斜め屋根の稜は、ナットの保持寸法と急な印刷断面を保つ機能稜として残す。ナットを先に入れてから蓋を固定する。

![ナット差込み口](_work/images/battery_nut_mouth.png)

## 印刷データ

入口は [parts/PRINT.md](parts/PRINT.md)。今回の再印刷は電池台 `battery_base` 1個。蓋は2026-10-12の `parent_lipo_retainer_lid_slide` を使用する。旧4本ねじの蓋を印刷済みなら、スライド蓋も1個印刷する。

電池台は [設定済み3MF](print_jobs/battery_tool_nut_access_20261013/battery_base.3mf) をBambu Studioで**プロジェクトとして開く**。ナット座とねじ穴だけ支持材を禁止するパーツを組み込み済み。PETG、X1Cの0.4 mmノズル、0.2 mm積層、4周壁、100%インフィル、支持有効45°／ブリッジ除外。電池台の底面をベッドへ向ける。

STLで使う場合は `parts/battery_base.stl` に `parts/modifiers/battery_lid_nut_support_blocker.stl` を**支持材禁止パーツ**として追加し、同梱座標を維持する。モディファイアは単体で印刷しない。形状だけを読み込んで自動支持を付けると、この穴が塞がることがある。斜め天井だけでは支持材を完全に抑えられなかったため、局所禁止設定と併用する。他の取付座には自動支持を残している。

蓋は平らな上面をベッドへ向けた姿勢。9種類各1個の構成は維持し、印刷一式内のSTLは変換済み。電池台の残る支持とバリを取り、ナット挿入・フック・工具穴を実物で確認する。3MFと対応STLのハッシュ、材料・設定は同じ `print_jobs` の `manifest.json` に記録する。

## 検証

- `battery_slide_lid_checks.json`：蓋の連続2 mmスライドと上抜き、電池包絡、ねじ1本による抜け止め、ナットの連続側面挿入と屋根の保持、電池台だけに対する直径7.8 mm工具包絡を確認。
- `battery_nut_print_checks.json`：設定済み3MFの実G-codeを読み、ナット差込み口とねじ通路に支持材の押出しが0件であることを確認。直線・円弧の経路と0.25 mmのビード余裕を含む保守的な領域で判定する。
- `battery_sd_access_checks.json` と `case_screw_access_checks.json`：電池／SD操作と容器固定ねじ3本の工具経路を確認。最下段の穴寸法は維持するため、実際のねじ操作は従来の長軸2.5 mm六角レンチを使用する。
- 変更部品のOpenSCAD独立レンダリング、閉メッシュ、STEP/STL外形・体積、両組立STEPと配置を照合。集約は `validation_current.json`。

これは形状と指定スライス設定の検証。実印刷の嵌合・支持材除去・締付け・繰返し操作と強度は未検証。別の材料やスライサ設定では再スライスして穴内部を確認する。既存の他assemblyの印刷一式／子機材料カードの不備は今回の対象検査と分けて記録する。

解析と変更前の原本は `_work/analysis/battery_tool_nut_access_20261013/`。再生成は既存 `spec/build_parent_hand_service.py --battery-only`、`spec/refresh_parent_case_screw_meshes.py --battery-tool-nut`、`spec/slice_parent_simple_stack.py --battery-tool-nut after battery_base parent_lipo_retainer_lid_slide`、`spec/prepare_parent_battery_support_project.py` の順。最後に `spec/verify_parent_battery_nut_print.py` と機能検査、印刷一式の同期・検査を行う。

支持材禁止パーツの3MF形式は [Bambu Studioの実装](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/Format/bbs_3mf.cpp) を参照し、実スライサへの再読込みと再出力で保持されることを確認した。
