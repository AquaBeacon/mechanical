# spresense_service_stack

Sony公式Web配布のCXD5602PWBEXT1.stpとCXD5602PWBMAIN1.stpを実際に読み込んだ機械レビュー用モデル。
拡張基板下面をZ=0に正規化。メインXYは取付穴とB2BコネクタからX+11.29/Y+0。
メインの上面Z=6.2は嵌合高さの仮値。IMUは公式50×20.6×9.1 mmの包絡で、詳細ベンダCADではない。
SHA256とソースはsources.json、原本は../spresense_logger/ref/。
USB・SD・穴の詳細は公式STEPの実ソリッドを使用。旧簡易モデルの寸法・穴・端子位置は継承していない。
検証結果と制限はassemblies/parent_service_review/README.md参照。
