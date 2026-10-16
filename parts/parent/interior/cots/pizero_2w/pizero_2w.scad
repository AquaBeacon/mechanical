// =====================================================================
// pizero_2w.scad — Raspberry Pi Zero 2 W 簡易モデル (購入品)
// 配置検討・アセンブリ用プレースホルダ。印刷対象ではない。
// 原点: 基板左下 (0,0,0)。X=65 / Y=30 / Z=上。穴 4-Ø2.75 (58×23, inset3.5)。
// =====================================================================

pcb_w = 65;
pcb_d = 30;
pcb_t = 1.6;

difference() {
    cube([pcb_w, pcb_d, pcb_t]);
    for (x = [3.5, 61.5]) for (y = [3.5, 26.5])
        translate([x, y, -0.5]) cylinder(d=2.75, h=pcb_t + 1, $fn=24);
}
// SoC + メモリ (概略)
translate([25, 9, pcb_t]) cube([12, 12, 1.5]);
// microSD (端から張出し)
translate([-1.5, 10.5, pcb_t]) cube([12, 12, 1.5]);
// CSI コネクタ (端)
translate([61, 6, pcb_t]) cube([4, 17, 1.2]);
// microUSB ×2 + miniHDMI (縁)
for (x = [37, 50]) translate([x, 0, pcb_t]) cube([8, 6, 3]);
translate([9, 0, pcb_t]) cube([11, 7.5, 3]);
