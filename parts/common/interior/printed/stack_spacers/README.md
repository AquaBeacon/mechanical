# 親機のスペーサセット

2026-10-22現行のparent_hand_serviceは、MAIN柱4、Sony左／右各2、GNSS前／後各2、計12本を個別STLで印刷する。MAIN14.3 mm、Sony41.7 mm＋キー0.8、GNSS31.2 mm＋キー0.8。固定板は別に印刷する。印刷入口はassemblies/parent_hand_service/parts/PRINT.md、対応表は同assemblyのspacer_delivery_report.md。旧ランナーと個別柱を重複印刷しない。

このフォルダのSony柱は既存の生成元spec/build_parent_stack_spacers.pyが正本。MAIN柱はparent_hand_service、GNSS柱はgnss_universal_carrierの既存正本を参照する。旧ランナーCADとset_members.jsonは履歴として保持する。形状と取合いを再定義しない。

Sony右は2026-10-22から5×9×高さ1.2 mmの下端を追加し、床の開放ナット穴をまたぐ。全体X幅5.4 mm・本体高さ41.7 mm・キー高さ0.8 mm・Ø3.45穴を維持する。下端・根元を含む外周は0.1 mm面取り。旧右柱の床との0.25 mmの隙間を解消するため、印刷済み旧ランナーの右柱2本は差し替える。ランナー自体も同じ新版STEPから再生成するが、現行印刷一式に重複追加しない。

幅1.2×高さ0.4×自由長1 mmの側面首を切り離す。座面・キー・穴を削らない。ランナーは廃棄。実物の切離し力・嵌合・締付け・波浪・クリープは未認定。印刷入口はassemblies/parent_hand_service/parts/PRINT.md。

## 過去の説明（履歴）

# 親機の切離し式支持セット

現行parent_hand_serviceでは、Sony柱4、GNSS柱4、MAIN支持4、Sony支持腕4を、16個の切離しランナー1枚で印刷する。source STEPを印刷姿勢へ回転・移動して結合し、形状を再定義しない。spec/build_parent_stack_spacers.pyが正本、set_members.jsonに出所・姿勢・位置・SHAを保存。

幅1.2×高さ0.4×自由長1 mmの側面首を切り離し、側面のバリだけを取る。座面・キー・穴は削らない。ランナーは組立に使わない。支持腕の局所サポートは実スライス結果に従う。印刷入口はassemblies/parent_hand_service/parts/PRINT.md。現物の切離し力・嵌合・保持は未検証。

## 過去の説明（履歴）

# 親機の印刷スペーサと切離しランナー

2026-10-10。生成元は `spec/build_parent_stack_spacers.py`、寸法は `scad/lib/parent_gnss.py`。購入品のhex_spacerとは別の印刷部品。配置・必要個数は親機 `placement.json`、セット内の位置と元STEPハッシュは `set_members.json`。

| スペーサ | 個数 | 本体高さ / 位置決め突起 | 外形 / 穴 |
|---|---:|---|---|
| Sony左 | 2 | 38 / 0.8 mm | Ø7 / Ø3.45 |
| Sony右 | 2 | 38 / 0.8 mm | Ø5.4 / Ø3.45 |
| GNSS前 | 2 | 31.2 / 0.8 mm | 既存9×9、穴Ø3.45 |
| GNSS後 | 2 | 31.2 / 0.8 mm | 既存8×6、穴Ø3.45 |

`parent_stack_spacer_set.stl` を原姿勢で **1枚**印刷すれば8本揃う。GNSS形状は元部品STEPを参照し、再定義しない。組立モデルでは個々のスペーサを配置、`print:false` と `print_set` でランナー印刷へ対応付ける。ランナーを組立に入れない。MAIN・PWR・TX・電池・アンテナ支持は既存印刷部品に一体化しており、別の購入スペーサを必要としない。

PETG、0.2 mm、4周壁、100%インフィル。全スペーサの底面をベッドへ接触させ、上端突起を上向きにする。ランナー幅2×高さ1、枝幅1.4×高さ1 mm。側面の接続部は幅1.2×高さ0.4×自由長1 mmで、0.2 mm積層の2層を想定。細い接続部を折るかニッパーで切り、側面だけを平らに仕上げる。底面・上面・位置決め突起・ねじ穴を削らない。ベアリング面、キーの機能稜、意図した切離し首以外は0.1–0.15 mm面取り。

Sonyは上端の突起を台下面へ入れ、既存M3×45の4本で床側金属ナットまで共締めする。床のナット下面16.2、ねじ頭座59.3、基板高さ65.6 mmを維持。実印刷の嵌合・切離し力・予圧と揺動保持は試作確認。支持不要かは同assemblyの実スライス結果を参照する。
