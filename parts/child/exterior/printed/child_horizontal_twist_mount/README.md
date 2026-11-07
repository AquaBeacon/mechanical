## 2026-10-29 素手着脱への改訂（現行）

カメラ専用の受けは外向きのねじ横抜き溝付き。初回固定は工具を使用し、以後のカメラ着脱はノブと指掛けスペーサで行う。現行条件・締結経路・制約は各assembly READMEの最上段を参照。旧横ボルト・旧ゴム方式は使用しない。

# 2026-10-29 カメラ専用4点支持受け

カメラ専用 `camera_receiver` 分岐を追加。既存 `frame_receiver` と `light_twist` はライト用として形状・配置を維持する。カメラ用STLは `child_horizontal_twist_mount_camera_receiver.stl`。

子機外面X=-122上の既存穴だけを使う。Y60/Z100・160のM3×18を維持し、Y98/Z100・176の前側ガード固定を共締めする。後者はM3×25をM3×30へ2本交換し、頭側ワッシャを受けの外へ4 mm移す。内側ガード・ワッシャ・ナット位置はそのまま。38 mm離れた2列4点で受けを支える。側板・ガードに加工や再印刷は不要。

取付足厚4 mm。Y60/Z120・140には直径8 mmの工具通路を残す。C中心は(-122,105,130)へ前方10 mm移動し、カメラの向きを維持。カメラ側の全構成部品を一緒に移し、ライトは移さない。中央の手の予約域Y=-45..45を避ける。

各締結経路はねじ頭→頭側ワッシャ→受け足→側板→（ガード側の2点はガード・内側ワッシャ）→ナット。側板側2点のナットは内面の既存六角座へ入り、締付方向の底面を使う。ガード側は既存内側ワッシャとナットで受け・側板・ガードを共締めする。

共通接続形状は `scad/lib/camera_rotary_joint.scad`。組立・解除は[カメラ共通説明](../dji_osmo_action6_mount_m3/README.md)、検証結果と印刷入口は[子機assembly](../../../../../assemblies/child_horizontal_plate_frame/README.md)。実物の保持力・材料強度は未認定。後続の旧日付の記録は履歴。

---

# 子機側面・一体型twist治具 Rev.4

正本は child_horizontal_twist_mount.scad。frame_receiver（フレーム台座＋Cメス）、light_twist（既存ライト保持半割＋Cオス）の2バリアント。各1個、単一連結の印刷部品。既存33×81筒と押さえを流用。差し込み姿勢から60°回して停止すると上向き、その横の水平ノブで締めて固定する。QR面内角0°、ノブ軸は機体+Y。

[組立SCAD](../../../../../assemblies/child_horizontal_plate_frame/child_horizontal_plate_frame_light_view.scad) をOpenSCADで開きF5。`pose="locked"` は固定位置、`pose="entry"` は差込位置、`show_frame=false` は治具単体。こちらは配置正本から生成される確認ビュー。

寸法・取合い・中央の手の予約空間・印刷・金具・検証は [共通規格](../../../../../docs/child_horizontal_twist_interface.md)。位置・数量の正本は [assembly](../../../../../assemblies/child_horizontal_plate_frame/placement.json)。C形状は既存公開モジュールを再利用し、ライトは元のhalf_holder(front,mount_plate)を呼ぶ。寸法は共通SCADへ生成される。

製造メタデータの姿勢：frame_receiverは0°、light_twistはX90°で筒軸垂直・下端をベッドへ。一体2部品は0.1 mm層。メスは厚4の平坦な一体足、N=0で段差なし・サポート無効。ライトオスだけベッドからの外部サポートを使う。新しい接続部はR2・面取り0.6、M3穴入口0.3。C爪・カム・ゴム座と既存ホルダーの嵌合形状を保持する。

旧frame_adapter/light_adapterの設計と印刷一式はassembly内のRev.1履歴へ保持。現行variantsとplacementには含めない。カメラは2026-10-21に一体Cオス付き部品を追加した。下のカメラ用メス節を参照。TD04Aは今後の設計。

一体部品のCGAL出力に生じる数値的なT頂点の退化三角形は、既存clean_stl_degenerates.pyのEdge Flipだけで処理する。頂点・面数を保持し、外形・体積・双方向表面誤差0.001 mm以内、閉メッシュ、単一連結を検査する。Rev.4ではメス10面・オス1面を処理し、表面誤差最大4.00e−8 mm、体積・外形差0。底板同士は中央部だけ0.05 mm重ね、旧底板の角を重複させない。再生成ツールと製造メタデータへ同じ処理を組み込んだ。

Rev.4：追加フレーム4枚は引き続き側板内側、台座M3×18各2本、ライト軸X161/Y80、突出59.5 mm。ノブ中心(136,105.5,130)、水平+Y軸。平坦な厚4足の入り隅をR2に仕上げ、既存32×32のC底板4穴を復元する。CのN=4以上の嵌合形状は保持する。Rev.3までの生成元・配置・印刷一式をassemblyのside_twist_r3履歴へ保存。


## カメラ用メス（2026-10-21）

camera_receiverバリアントは同じframe_receiver()にreceiver_u=-35、dock_rotation=90を与える。左前の既存Y60/Z100・160穴、厚4の足、M3×18・内側ナットを流用。C中心(-122,95,130)、ノブ軸+Z。カメラを外側から見て右へ90°回し、通常の横向きにする。ライト用の2バリアントのメッシュは別途再レンダリング・全頂点比較し、元のバイト列を保持した。カメラ側は同じcamera_mount_twistを親子で共用。専用メスは取付足下、0.1 mm・Generic PETG・6壁・15% Gyroid・5 mmブリム、自動支持有効・ベッドからのみ。実支持経路は0.2 mmの初層だけ。部品STEPは単一有効ソリッドで外形・体積がSTLと一致。配置・数量・組付けは[assembly説明](../../../../../assemblies/child_horizontal_plate_frame/README.md)。
