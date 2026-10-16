2026-10-11現行センサ治具改訂：GNSSユニバーサル基板下面とLIS3MDL基板下面はともにZ56。GNSS一式は西6 mm、磁気センサはZ76から20 mm下げる。配置の正本と着脱手順はassemblies/parent_hand_service/README.md、検証は同assemblyのsensor_mount_report.md。下記の旧座標は当時の記録。

# Adafruit LIS3MDL磁気センサ（4479 / Switch Science 6266）

[製品](https://www.switch-science.com/products/6266)、[メーカー資料](https://learn.adafruit.com/lis3mdl-triple-axis-magnetometer/downloads)。購入品であり印刷しない。`ref/4479 LIS3MDL.step`はAdafruit公式の完成基板モデル。簡略基板へ置換せず、同じ座標系のSTEP/STLを生成する。公式EAGLEの4穴はØ2.5、ピッチ20.32×12.7 mm。穴位置は生成時にEAGLEから読み込む。

公式STEP外形25.4×17.78×4.53 mm、基板厚1.57 mm。販売記載の25.7×17.8×4.6 mmとの差は残し、外形を拡縮しない。実物の版・穴・外形を取合い試作で照合する。ヘッダーピンは装着しないモデル。

親機では原点X61.78/Y195/Z76、Z回転90°。基板外形X44–61.78/Y195–220.4。GNSS台の北西側片持ち棚へナイロンM2×8ボルト・M2ナットを各4個で固定する。ねじ頭Ø4×H1.6、ナット対辺4×H1.6は型番未選定の仮包絡。金属ねじに置き換えない。支持棚の穴Ø2.45、基板接触面Z76。使用する南向きSTEMMA QT端に幅6×奥行15×高さ5 mmの接続・直線進入包絡を確保する。北向き端はケース壁に近く、箱内では使用しない。実プラグ形状とケーブル保持は未確定。

配置は磁気性能の保証ではない。ANN-MB1は磁石内蔵（[メーカー資料・機械仕様](https://www.u-blox.com/sites/default/files/ANN-MB1_DataSheet_UBX-21005551.pdf)）。北西後端へ離したが、アンテナ磁石・鋼板、電源基板、電流配線の影響を含め、完成・通電・送信状態で測定範囲内で飽和していないことを確認し、磁気測定と校正を行う。近傍に鋼製工具・締結具・磁石を残さず、センサ向きとケースの軸対応を実機で記録する。

生成元`spec/build_parent_gnss.py`、寸法`scad/lib/parent_gnss.py`、配置・数量`assemblies/parent_hand_service/placement.json`。原本URLとSHA-256は`sources.json`、メーカーのライセンス・帰属文は`ref/license.txt`と`ref/vendor_README.md`に保持する。
