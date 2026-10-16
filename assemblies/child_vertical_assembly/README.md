**印刷一式:** [parts/PRINT.md](parts/PRINT.md)（STL・数量・モディファイア） · **確認画像:** [_work/images/](_work/images/)

2026-10-07：未使用ケーブルレール2本と固定ねじ8本を撤去。デッキの既存穴は残置（使用不要）。バッテリーの普通M3ナット5個は横差しポケットに収まり、樹脂との重なり・横挿入・床板着脱の122検査で干渉なし。ナットの熱圧入や造形途中の埋込みは不要。 詳細は[ねじ組立手順](../../spec/child_interior_reinforcement/FASTENER_ASSEMBLY.md)。

# child_vertical_assembly

- [child_vertical_assembly.md](child_vertical_assembly.md)
- [child_lcd_service_view.scad](child_lcd_service_view.scad)
- [child_vertical_assembly.step](child_vertical_assembly.step)
- [child_vertical_assembly.stl](child_vertical_assembly.stl)
- [child_vertical_assembly_interior.step](child_vertical_assembly_interior.step)
- [child_vertical_assembly_interior.stl](child_vertical_assembly_interior.stl)
- [child_vertical_assembly_view.scad](child_vertical_assembly_view.scad)

構成と既存の未検証事項は上の設計説明を参照してください。

現行内装はM3統一・サポート削減版。[変更と印刷設定](../../spec/child_interior_reinforcement/M3_SUPPORT_REVISION.md)。RXのØ2.2基板穴は未使用、M3外周クランプ4組で保持。印刷一式には必要な鏡像STLとモディファイアを含み、印刷姿勢へ回転済みです。

現行締結は [電池・フランジ補強改訂](../../spec/child_interior_reinforcement/BOLTED_MOUNT_REVISION.md)。電池ケースM3×12＋普通ナット4組、床板M3×10皿＋普通ナット1組、前側フランジM3×16。デッキ根元80 mm・一体リブ拡幅、ブレース梁12 mm。強度試験は未実施です。

2026-10-04：RXクランプを左右連結して8→4個、フランジブレースの途中のくびれを補強、床板窓とケース取付部を改訂。[設計・印刷・配線変更](../../spec/child_interior_reinforcement/PRINT_STRENGTH_REVISION.md)。

2026-10-06：[ねじ一覧・工具条件・組立順](../../spec/child_interior_reinforcement/FASTENER_ASSEMBLY.md)を追加。レールねじの工具通路を修正。MF10スペーサのオス突出長は現物確認待ち。
