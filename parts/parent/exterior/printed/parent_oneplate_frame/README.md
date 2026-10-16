# 親機・再現位置決めフレーム

親機のBCAS212310G箱、TD支持部、既存カメラマウントを載せる開放型フレーム。外形232×134×42 mm。箱底をZ=0とし、デッキ上面はZ=-0.8 mm、下面はZ=-12 mm。箱底は三つの局所基準面XY=(-96,-55)、(-96,55)、(96,0) mmで支持する。面全体の平板支持ではない。

箱固定用のM5全ねじ4本の穴、上側バーと既存カメラマウントの取付穴を持つ。カメラマウントの取付面基準は右端X=2 mm、後端Y=44.5 mm。TD支持部用のキー溝は中心(75,-55) mm、12×12×2 mmで、支持部の11.6 mmキーを受ける。部品配置はassemblyの `placement.json` を参照する。

設計元は `spec/prepare_parent_oneplate.py` と `spec/parent_oneplate_frame_sources.py`、共通寸法は `scad/lib/parent_oneplate_interfaces.scad`。生成SCADを直接編集しない。製造向きは `manufacturing.json` を参照する。

三つの支持面高さ、箱との接触、取付ねじ・工具・ケーブルの通路は現物確認が必要。支持面を研磨して高さを変えない。強度・反復着脱性能の認定はない。
