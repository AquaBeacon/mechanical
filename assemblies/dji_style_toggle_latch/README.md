# 旧試作：写真と形状が異なる組込用レバー留め具

**状態：exploration_only。** ユーザー確認により、写真の防水カメラハウジング用ラッチとは形状が違う。下記STLは過去試作の記録で、機体用の採用・印刷指示ではない。[公開CAD調査](../../spec/dji_style_toggle_latch/PUBLIC_CAD_REVIEW.md)と[CC0参考STL](../../parts/common/jigs/dji_style_toggle_latch/ref/README.md)を参照して再設計する。

汎用の手動着脱ラッチ試作。手持ちの厚1 mm EPDMシートを固定側のくぼみの奥面・天井・左右面へ貼ります。主片20.8×14.43 mmと側面片4×12.5 mm（上側奥角R3）2枚に切ります。無発泡シートを仮定しており、発泡材や接着層の厚みは現物確認が必要です。フックのゴム座はありません。

細くなっていた斜めの付け根を連続した厚肉L形に変更。先端厚2.8→4.2 mm、付け根R1.2→R2.5、外角R0.8。幅20 mm。受けを取付板端へ寄せ、取付板35×46→19×48 mm（面積約43%減）、閉時の原点間隔28→26 mm。ゴムと爪の厚みを確保するため受け全高は14→16.5 mmです。

[印刷入口：parts/PRINT.md](parts/PRINT.md)。Bambu Lab PETG Basicで印刷4種類5点。M3×25・M3×35各1本、ナット2個、EPDM3片は印刷しません。**この版の台座・受け・レバーをセットで使用してください。受けの穴はx=−12,−4、y=±19です。**

[貼付・取付・設計への組込](../../parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch.md) / [断面](_work/images/epdm_contact_section.png) / [貼付位置](_work/images/epdm_keeper.png) / [開閉](_work/images/open_close.gif)。緑がEPDM。受けの開口下をホストの板で塞がないでください。

閉時の奥面で公称0.15 mm圧縮、動作中の幾何上の最大は約0.343 mm。公称回り込み3.15 mmで段差へ掛かります。接着層は含まず、実物で受け位置を調整します。ゴムのCADは残る空間の表示で、弾性解析ではありません。EPDMはガタ取り用であり、この開放溝は防水シールではありません。

[検証結果](_work/analysis/geometry/report.json)：231姿勢で剛体干渉なし、先端から付け根までの実STL最小厚4.2 mm、穴・工具通路・上方向の引っ掛かりを確認。実保持力・疲労・剥離は未検証です。試作Bambu Lab PETG Basic、6周壁、100%インフィル。局所サポートと清掃はPRINT.md参照。機体側の取付板・穴位置、荷重、指の操作空間は未確定です。

配置正本placement.json。組立STEPはdji_style_toggle_latch.step。8点（印刷5、金属包絡2、ゴム包絡1）。組立STLを丸ごと印刷しません。直前版は部品の_work/analysis/before_full_recess_epdm/に保存。
