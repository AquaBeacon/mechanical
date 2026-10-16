2026-10-11現行センサ治具改訂：GNSSユニバーサル基板下面とLIS3MDL基板下面はともにZ56。GNSS一式は西6 mm、磁気センサはZ76から20 mm下げる。配置の正本と着脱手順はassemblies/parent_hand_service/README.md、検証は同assemblyのsensor_mount_report.md。下記の旧座標は当時の記録。

# SparkFun GPS-23288 / NEO-F9P

実機検証：[2026-10-08 RTK-GNSS動作検証レポート](_work/analysis/rtk_gnss_20261008/README.md)。USB/COM認識が確認できず、測位・RTK・PPKは未検証。OS検出ログとグラフを同レポート配下へ保存。

Switch Science 9456。原本はref/の公式EAGLE ZIPとu-blox公式NEO-F9P.STEP。SHA-256、抽出した外形43.18×43.18・切欠き・4取付穴Ø3.302はdimensions.jsonへ記録。

完成SparkFun基板の公式STEPは取得できていない。`sparkfun_neo_f9p.step`は公式EAGLE外形に、取得したu-bloxモジュールSTEPを配置し、USB/Qwiic/SMAの仮包絡を足した再構成モデル。`neo_f9p_vendor_module.step`は取得したモジュールの変換モデル。完成基板全体を公式CADとして扱わない。

ユニバーサル基板60×80 mmはユーザー確定。基板厚1.6、ヘッダー6 mm、XH 24×11×30、SMAプラグ長14・径8は仮値。XH極数・実装辺・高さを確定して実装モデルへ置換する。すべて購入品・予約空間で印刷対象外。

取得元： https://github.com/u-blox/3D-Step-Models-Library/blob/master/POS/NEO-F9P.STEP および https://docs.sparkfun.com/SparkFun_u-blox_NEO-F9P/ 。生成元はspec/build_parent_gnss.py。
