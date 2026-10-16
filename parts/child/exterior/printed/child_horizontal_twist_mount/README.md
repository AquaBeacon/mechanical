# 子機側面・一体型twist治具 Rev.4

正本は child_horizontal_twist_mount.scad。frame_receiver（フレーム台座＋Cメス）、light_twist（既存ライト保持半割＋Cオス）の2バリアント。各1個、単一連結の印刷部品。既存33×81筒と押さえを流用。差し込み姿勢から60°回して停止すると上向き、その横の水平ノブで締めて固定する。QR面内角0°、ノブ軸は機体+Y。

[組立SCAD](../../../../../assemblies/child_horizontal_plate_frame/child_horizontal_plate_frame_light_view.scad) をOpenSCADで開きF5。`pose="locked"` は固定位置、`pose="entry"` は差込位置、`show_frame=false` は治具単体。こちらは配置正本から生成される確認ビュー。

寸法・取合い・中央の手の予約空間・印刷・金具・検証は [共通規格](../../../../../docs/child_horizontal_twist_interface.md)。位置・数量の正本は [assembly](../../../../../assemblies/child_horizontal_plate_frame/placement.json)。C形状は既存公開モジュールを再利用し、ライトは元のhalf_holder(front,mount_plate)を呼ぶ。寸法は共通SCADへ生成される。

製造メタデータの姿勢：frame_receiverは0°、light_twistはX90°で筒軸垂直・下端をベッドへ。一体2部品は0.1 mm層。メスは厚4の平坦な一体足、N=0で段差なし・サポート無効。ライトオスだけベッドからの外部サポートを使う。新しい接続部はR2・面取り0.6、M3穴入口0.3。C爪・カム・ゴム座と既存ホルダーの嵌合形状を保持する。

旧frame_adapter/light_adapterの設計と印刷一式はassembly内のRev.1履歴へ保持。現行variantsとplacementには含めない。カメラ・TD04Aは機器側寸法未確定で、今後Cオスを直接治具へ統合する。

一体部品のCGAL出力に生じる数値的なT頂点の退化三角形は、既存clean_stl_degenerates.pyのEdge Flipだけで処理する。頂点・面数を保持し、外形・体積・双方向表面誤差0.001 mm以内、閉メッシュ、単一連結を検査する。Rev.4ではメス10面・オス1面を処理し、表面誤差最大4.00e−8 mm、体積・外形差0。底板同士は中央部だけ0.05 mm重ね、旧底板の角を重複させない。再生成ツールと製造メタデータへ同じ処理を組み込んだ。

Rev.4：追加フレーム4枚は引き続き側板内側、台座M3×18各2本、ライト軸X161/Y80、突出59.5 mm。ノブ中心(136,105.5,130)、水平+Y軸。平坦な厚4足の入り隅をR2に仕上げ、既存32×32のC底板4穴を復元する。CのN=4以上の嵌合形状は保持する。Rev.3までの生成元・配置・印刷一式をassemblyのside_twist_r3履歴へ保存。
