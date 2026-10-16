// =====================================================================
// spresense_logger.scad — SPRESENSE 独立 IMU ロガー 簡易モデル (購入品)
// 拡張ボード CXD5602PWBEXT1 (68.6×53.5) + メインボード (50×20.6) +
// Multi-IMU Add-on を積んだスタックの配置検討・アセンブリ用プレースホルダ。
// 印刷対象ではない。寸法は Sony 公称 + スタック高さ仮値 (要実測)。
// 原点: 拡張ボード左下 (0,0,0)。X=68.6 / Y=53.5 / Z=上。
// =====================================================================

/* [拡張ボード (公称)] */
ext_w = 68.6;
ext_d = 53.5;
pcb_t = 1.6;

/* [メインボード (公称 50×20.6)、ヘッダ約 9mm 上に載る (仮)] */
main_w = 50;
main_d = 20.6;
header_h = 9;      // 仮値 (要実測)

/* [Multi-IMU Add-on (公称 20×25 級、メイン上に約 8mm) 仮] */
imu_w = 25;
imu_d = 20.6;
imu_h = 8;         // 仮値 (要実測)

/* [下面リード余裕] */
under_h = 3;

// 拡張ボード
translate([0, 0, 0]) cube([ext_w, ext_d, pcb_t]);
// 下面リード (簡易)
translate([4, 4, -under_h]) cube([ext_w - 8, ext_d - 8, under_h]);
// メインボード (拡張ボードの片側に寄せる: コネクタ位置は仮)
translate([9, (ext_d - main_d)/2, pcb_t + header_h]) {
    cube([main_w, main_d, pcb_t]);
    // Multi-IMU Add-on
    translate([main_w - imu_w - 2, 0, pcb_t]) cube([imu_w, imu_d, imu_h]);
}
// microSD スロット目印 (拡張ボード縁, 仮)
translate([ext_w - 16, 8, pcb_t]) cube([15, 12, 3]);
