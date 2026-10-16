> 2026-10-04現行：小部品連結・フランジ梁・床板窓・ケース耳の改訂は [設計記録](../../../../../spec/child_interior_reinforcement/PRINT_STRENGTH_REVISION.md)。以下の旧版寸法・個数・配線記述より優先します。

> 現行：電池はM3ねじ＋普通ナット5個による締結、デッキ根元と前側ブレースを印刷補強。詳細は `spec/child_interior_reinforcement/BOLTED_MOUNT_REVISION.md`。以下の旧寸法・ねじ・PASS記述は履歴で、今回の強度保証には使わない。

> 現行: M3統一・サポート削減版。印刷姿勢・変更は spec/child_interior_reinforcement/M3_SUPPORT_REVISION.md。以下は旧版履歴を含みます。

> 2026-09-27現行: Bambu PLA Matte向け、60 mm根元・20 mm固定座・局所フランジ受け足、前側梁10 mm。印刷設定と解析の限界は spec/child_interior_reinforcement/PLA_MATTE_REVISION.md。以下の旧寸法・材料待ち記述は履歴です。

> 現行版: 印刷部品による閉じた耳・31 mm根元補強。追加の金属スリーブ・板は廃止。強度解析は材料／荷重条件待ち。詳しくは `spec/child_interior_reinforcement/PRINTED_REINFORCEMENT.md`。以下は過去の履歴を含む。

# child_flange_brace — LCD撤去後の下フランジ固定ブレース

現行再補強版：本体8 mm厚、前側フォーク12 mm厚、皿ねじなし。
左右はM3 MF30/MF12、M3×12なべ、5.7 mm鋼製スリーブと1 mm押さえ板を使用。
前側は12.2 mm鋼製スリーブと1.5 mm押さえ板、M3×18なべ。
各押さえ板と樹脂の隙間0.2 mm。以下の旧寸法は履歴。

2026-09-26。旧LCD支持アーチの下側を構造専用に置換した。
既存BR-101040下フランジ、200 mm縦置き内装をユーザー確認済み。

- C-MAINの下側2穴をM3 MF30 / MF17スペーサで共締め。
- ブレースのねじは従来どおりM3×10皿ねじ。
- フランジBCD94の90°穴へM3×12。座面Z27、ねじ込み4 mm。
- アーチ幅4.8→6.4 mm、固定耳ウェブ幅5.2→12 mm。
- 固定耳は接線方向に11.2 mmへ拡幅。チューブまで約1.1 mm。
- LCDヒンジとLCD固定用の下穴を撤去。

印刷はモデル上面Z5をベッドへ向けて裏返す。0.4 mmノズル、
外周5周以上、0.2 mm積層を目安にし、固定耳は密な充填にする。
形状補強であり、許容荷重を実験で保証したものではない。
