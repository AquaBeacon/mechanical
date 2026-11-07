**印刷一式:** [parts/PRINT.md](parts/PRINT.md)（STL・数量・モディファイア） · **確認画像:** [_work/images/](_work/images/)

2026-10-21 通し穴改訂：スペーサ外側を二面幅5.5 mmの六角、穴を内接径3.5 mmに変更。M3ねじが滑って通り、タップ不要。10 mm×2・12 mm×1・30 mm×1をつなぎ付き1セットで印刷する。左右フランジは首下26 mmのM3なべねじ2本（必要ならM3×30を26 mmに切断・面取り）、ブレースはM3×30／×45スタッド各1本＋普通M3ナット2個で固定。以前の短いスタッドと上ねじ4本は使わない。[設計・取付・印刷条件](../../parts/child/interior/printed/child_spacer_set/child_spacer_set.md)。実物の嵌合・締結強度は未検証。

スペーサセットはX1C／PETG／0.2 mmでスライス検証する。[スライス済み3MF](print_jobs/child_spacer_set/child_spacer_set_set.3mf)はこのセット専用。parts内に残っていた旧ブレース／RXクランプの3MFは内容を変えずprint_jobsへ移動し、[SHA-256と移動記録](print_jobs/retained_jobs_20261021.json)を保存した。

2026-10-07：未使用ケーブルレール2本と固定ねじ8本を撤去。デッキの既存穴は残置（使用不要）。バッテリーの普通M3ナット5個は横差しポケットに収まり、樹脂との重なり・横挿入・床板着脱の122検査で干渉なし。ナットの熱圧入や造形途中の埋込みは不要。 詳細は[ねじ組立手順](../../spec/child_interior_reinforcement/FASTENER_ASSEMBLY.md)。

# child_interior

- [child_interior.md](child_interior.md)
- [child_interior.scad](child_interior.scad)
- [child_interior.step](child_interior.step)
- [child_interior.stl](child_interior.stl)
- [child_interior_interior.stl](child_interior_interior.stl)
- [child_interior_view.scad](child_interior_view.scad)
- [Light_Gassyli_Holder.stl](Light_Gassyli_Holder.stl)

構成と既存の未検証事項は上の設計説明を参照してください。

現行内装はM3統一・サポート削減版。[変更と印刷設定](../../spec/child_interior_reinforcement/M3_SUPPORT_REVISION.md)。RXのØ2.2基板穴は未使用、M3外周クランプ4組で保持。印刷一式には必要な鏡像STLとモディファイアを含み、印刷姿勢へ回転済みです。

既存の電池ケース用スライサプロジェクトは [print_jobs/child_vtray_batt_box.3mf](print_jobs/child_vtray_batt_box.3mf) へ内容を変えず保存しました。今回のSTLを再読み込みしてからスライスしてください。

現行締結は [電池・フランジ補強改訂](../../spec/child_interior_reinforcement/BOLTED_MOUNT_REVISION.md)。電池ケースM3×12＋普通ナット4組、床板M3×10皿＋普通ナット1組、前側フランジM3×16。デッキ根元80 mm・一体リブ拡幅、ブレース梁12 mm。強度試験は未実施です。

2026-10-04：RXクランプを左右連結して8→4個、フランジブレースの途中のくびれを補強、床板窓とケース取付部を改訂。[設計・印刷・配線変更](../../spec/child_interior_reinforcement/PRINT_STRENGTH_REVISION.md)。

旧ブレースのスライサプロジェクトは[print_jobs/child_flange_brace.3mf](print_jobs/child_flange_brace.3mf)へ内容を変えず保存。現在のSTLを再読み込みして使用してください。

2026-10-06：[ねじ一覧・工具条件・組立順](../../spec/child_interior_reinforcement/FASTENER_ASSEMBLY.md)を追加。レールねじの工具通路を修正。MF10スペーサのオス突出長は現物確認待ち。
