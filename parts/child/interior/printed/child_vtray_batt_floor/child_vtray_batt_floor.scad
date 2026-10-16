include <../../../../../scad/lib/child_interior_mounts.scad>
// Removable battery floor, nut-bolted service revision 2026-10-01.
// M3x8 at local X22.5/Z16 (world Z36), accessible with tube removed,
// while interior stays secured to the lower flange.
// Remove screw, slide -Z by 2 mm, then withdraw -Y.
// Lower plate edge world Z22.5 -> Z20.5 during release; flange face Z19.
// Upper retaining hooks remain outside the battery. No lower screw tab.
// Coordinates are shared with child_vtray_batt_box; origin world Z20.

/* [箱との取合い (child_vtray_batt_box と一致させること)] */
cav_x      = 20;      // 箱の内幅の半分
floor_y1   = -40;     // 板の上面 (LiPo が載る面)
floor_t    = 3;       // 板厚
cav_l      = 112;     // 端壁上面 (z=0) からリップまで
lip_t      = 1.5;     // リップの厚み (Z)
end_t      = 6;       // −Z 端壁の厚み (板のタブはこの下に入る)
slot_x0    = 10.5;    // 端壁の柱の半幅 (タブはこれより狭く)
side_clear = 0.3;     // 板と壁の片側クリアランス
end_clear  = 0.5;     // 板の +Z 端とリップのすきま

/* [フック (+Z 端)] */
hook_w     = 1.3;     // 厚み (X)。箱の hook_w と一致
hook_h     = 3;       // 高さ (Y): 板上面の 0.5mm 下から 2.5mm 上まで
hook_l     = 2;       // リップのスロットへの差し込み長 (Z) = リップ厚 + 0.5
hook_base  = 4;       // 板の上に載る根元の長さ (Z)

/* [−Z タブと皿ねじ] */
tab_x      = 7;       // タブの半幅 (柱の半幅より狭く。貫通口 r43.75 の中: rad(7,-43)=43.6)
tab_t      = 3;       // タブの厚み (板と面一 → 寝かせて印刷してもサポート不要)
service_x = ci_service_x;
service_r = 2.8;
plate_z0 = 2.5; // lower edge stays above flange after the 2 mm release slide
screw_d    = 3.4;     // M3 バカ穴
csk_d      = 5.8;     // 皿頭の座ぐり径 (JIS M3 頭 5.5 + 0.3)
service_z = ci_service_z;
screw_z    = service_z;      // local coordinate, world Z36

/* [軽量化・確認窓] */
win_z      = [34, 78];
win_l      = 22;
win_w      = 14;
window_corner_r = 3; // Spread load around the viewing windows.
window_edge_chamfer = 0.3; // Both faces; lower rim grows at 45 degrees.

$fn = 48;

// ---- 導出 -------------------------------------------------------------
plate_x  = cav_x - side_clear;        // 18.7
plate_z1 = cav_l - end_clear;         // 111.5
floor_y0 = floor_y1 - floor_t;        // -43
hook_y0  = floor_y1 - 0.5;            // -40.5
hook_x0  = plate_x - hook_w;          // 17.3

// ---- 成立性チェック ---------------------------------------------------
assert(tab_x < slot_x0 - 0.2, "タブが柱より広い");
assert(csk_d/2 + 1 < tab_x, "皿座ぐりがタブの縁に近すぎる");
assert((csk_d - screw_d)/2 <= tab_t - 0.5, "皿座ぐりがタブを突き抜ける");
assert(sqrt(tab_x*tab_x + (floor_y1 - tab_t)*(floor_y1 - tab_t)) <= 43.75, "タブが下フランジ貫通口 (r43.75) に入らない");
assert(20 + plate_z0 - hook_l > 19 + 1, "Release slide crosses flange face");
assert(hook_l <= lip_t + 0.5 + 0.01, "フックがリップを突き抜ける");
assert(plate_z1 + hook_l <= cav_l + lip_t, "フックがリップの外へ出る");
for (z = win_z) {
    assert(z - win_l/2 > 3 && z + win_l/2 < plate_z1 - 3, str("窓 (Z=", z, ") が板の端にかかる"));
    assert(win_w/2 < plate_x - 3, "窓が板の縁にかかる");
}

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // 板 (箱の壁の間)
        translate([-plate_x, floor_y0, plate_z0]) ci_chamfer_box([2*plate_x, floor_t, plate_z1-plate_z0]);
        // 14 mm long tab spreads nut preload into the floor; no small round ear.
        translate([16,floor_y0,screw_z-ci_service_half_z])
            ci_chamfer_box([ci_service_outer_x-16,floor_t,2*ci_service_half_z]);
        // +Z フック ×2 (板の上に根元を載せ、リップのスロットへ hook_l 突き出す)
        for (sx = [-1, 1])
            translate([sx > 0 ? hook_x0 : -plate_x,0,0])
                rotate([90,0,90]) linear_extrude(hook_w)
                    polygon([[hook_y0,plate_z1-hook_base],[hook_y0,plate_z1],
                             [hook_y0+hook_l,plate_z1+hook_l],
                             [hook_y0+hook_h,plate_z1+hook_l],
                             [hook_y0+hook_h,plate_z1-hook_base]]);
    }
    // 皿ねじ: バカ穴 + 90° 座ぐり (板の下面側)
    translate([service_x, floor_y1 - tab_t - 0.5, screw_z]) rotate([-90, 0, 0]) cylinder(d = screw_d, h = tab_t + 1, $fn = 24);
    translate([service_x, floor_y1 - tab_t - 0.01, screw_z]) rotate([-90, 0, 0])
        cylinder(d1 = csk_d, d2 = screw_d, h = (csk_d - screw_d)/2, $fn = 24);
    // Smaller rounded windows leave 12.7 mm side bands instead of 9.7 mm.
    for (z = win_z)
        translate([0,floor_y0,z]) rotate([-90,0,0]) window_cut();
}

module window_profile(extra=0) {
    offset(r=window_corner_r+extra,$fn=48)
        square([win_w-2*window_corner_r,win_l-2*window_corner_r],center=true);
}
module window_cut() {
    assert(window_corner_r>0 && 2*window_corner_r<min(win_w,win_l));
    assert(window_edge_chamfer>0 && 2*window_edge_chamfer<floor_t);
    translate([0,0,-0.01]) linear_extrude(floor_t+0.02) window_profile();
    for (top=[false,true]) translate([0,0,top ? floor_t : 0])
        scale([1,1,top ? -1 : 1]) hull() {
            translate([0,0,-0.01]) linear_extrude(0.01) window_profile(window_edge_chamfer);
            translate([0,0,window_edge_chamfer]) linear_extrude(0.01) window_profile();
        }
}

echo(str("child_vtray_batt_floor: ", 2*plate_x, " x ", floor_t, " x ", plate_z1,
         " (+ タブ z ", -end_t, "..0, フック +", hook_l, ")  皿ねじ M3 @ z ", screw_z));
