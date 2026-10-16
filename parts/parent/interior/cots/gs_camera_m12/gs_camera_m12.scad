// =====================================================================
// gs_camera_m12.scad — RPi Global Shutter Camera + M12 4mm レンズ 簡易モデル
// 配置検討・アセンブリ用プレースホルダ。印刷対象ではない。
// パターン2 では箱底ビューポートへ「レンズ下向き」で使うため、
// 原点 = 基板下面中心 (0,0,0)、基板 +Z、レンズは -Z へ伸びる。
// 寸法は RPi 公称 38×38 + M12 レンズ仮値 (要実測)。
// =====================================================================

pcb_sq = 38;
pcb_t = 1.6;
hole_pitch = 34;    // 仮値 (要実測: 公式図面では 30? 要確認)
lens_d = 17;        // M12 レンズホルダ外径 (仮)
lens_l = 28;        // 基板下面からレンズ前面まで (仮)
mount_sq = 22;      // M12 ホルダ台座 (仮)

difference() {
    translate([-pcb_sq/2, -pcb_sq/2, 0]) cube([pcb_sq, pcb_sq, pcb_t]);
    for (x = [-hole_pitch/2, hole_pitch/2]) for (y = [-hole_pitch/2, hole_pitch/2])
        translate([x, y, -0.5]) cylinder(d=2.6, h=pcb_t + 1, $fn=24);
}
// M12 ホルダ台座 + レンズ (下向き)
translate([-mount_sq/2, -mount_sq/2, -12]) cube([mount_sq, mount_sq, 12]);
translate([0, 0, -lens_l]) cylinder(d=lens_d, h=lens_l - 12 + 0.1, $fn=48);
// CSI コネクタ (基板上面の縁)
translate([-11, pcb_sq/2 - 6, pcb_t]) cube([22, 5, 3]);
