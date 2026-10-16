# 防水カメラハウジング用ラッチの公開CAD調査

2026-09-29。目的は機体の素手脱着用ラッチ。写真 `parts/common/jigs/dji_style_toggle_latch/_work/images/IMG_4265.jpg` から `IMG_4268.jpg` の二軸・三折り形状を参照する。防水ケースそのものの再現ではない。

| 資料 | 公開データ | 評価 |
|---|---|---|
| [GoPro Hero 9 Waterproof Case Clasp](https://www.printables.com/model/591613-gopro-hero-9-waterproof-case-clasp) | CC0、STL/3MF。STLを `parts/common/jigs/dji_style_toggle_latch/ref/` に保存 | 薄いU字状レバーと先端の掛かり形状の参考。金属ヒンジ軸・元ケースが必要で、単体では固定できない。 |
| [GoPro Hero 3 case latch](https://cults3d.com/en/3d-model/gadget/gopro-hero-3-case-latch) | CC BY、LatchとLockの2 STL | 二段ロックの参考候補。公開ページのAI利用条件を含め、再利用範囲は別途確認。 |
| [GoPro 7 Waterproof Enclosure Latch](https://cults3d.com/en/3d-model/tool/gopro-7-waterproof-enclosure-latch) | 有料STEP、可動クラスプ1点 | 編集可能なB-repの候補だが購入していない。 |
| [Over-Center Toggle Latch](https://www.printables.com/model/1548353-over-center-toggle-latch) | 無償STL、CC BY-NC-SA | 完全なトグル構造の参考。カメラハウジングの薄いクラスプとは形状が異なる。 |

写真のラッチに相当するDJI純正防水ケースの公開CADは、今回の検索では確認できなかった。公開されているGoPro交換用モデルはレバー単品が中心で、機体への取付台座・受け・EPDMの寸法は提供しない。

既存 `dji_style_toggle_latch.scad` は写真の薄いU字レバーと軸配置を再現できていないとのユーザー確認があった。既存STLの外形検査や231姿勢の剛体干渉検査は、写真との形状一致を示すものではない。再設計した[汎用二軸試作](../../assemblies/camera_housing_clasp/README.md)はCC0参考STLの外形比率と開口を参考に、Bambu Lab PETG Basicと厚1 mm EPDMの独立した機体取付構成とした。元ケース互換ではない。
