# TD04A固定治具 Rev.6

M4貫通穴＋ナット2組、設計ピッチ12 mm（ユーザー指定は約12 mm）、M4穴列基準でケーブル側へ60 mmの空間。送受信面は親機下向き・子機上向き。旧TD04Aモデルは表示・適合判断に使わない。

[印刷入口](parts/PRINT.md) / [設計と締結経路](../../parts/common/exterior/printed/td04a_bracket_mount/README.md) / [配置正本](placement.json)

![改訂治具と60 mmの予約域](_work/images/fixture_assembled.png)

親機はparent_exteriorの既存M5/20 mm穴、子機はchild_horizontal_plate_frameの既存側面M3/20 mm穴に配置。外装側板・主プレートの再加工は不要。緑の予約域は高さ60 mm、幅と奥行は仮値。青矢印は送受信方向だけを示し、本体形状を表さない。

[幾何検査](_work/analysis/geometry_checks.json)、[外装干渉・連続掃引によるナット保持](_work/analysis/cable_clearance_r6/exterior_checks.json)。耳厚3 mmの仮定でM4×14を表示。実物の正確な穴間隔、耳の厚み・座面、本体、ケーブル根元・曲げ半径、締付・実造形・強度は未確認。センサー側の締結成立を認定しない。

旧Rev.5の履歴は_work/analysis/cable_clearance_r6/history/。旧3MFは使用しない。再生成とねじの順序は設計説明を参照。
