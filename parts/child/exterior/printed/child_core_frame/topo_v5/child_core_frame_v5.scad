// =====================================================================
// child_core_frame_v5.scad — コアフレーム v5 トポロジー最適化の設計空間定義
//
// v4 (650 cm³) を「機能面 = preserve」「空けておく空間 = obstacle」「残り = design_space」
// に分解して topopt (TO_printing/topopt) に渡す。**部品そのものではない。**
// 寸法はすべて child_core_frame.scad (v4) の Customizer 値をそのまま使う
// (二重定義になるので v4 と同時に直すこと)。
//
// part= で出力を選ぶ:
//   preserve       絶対に残す機能面 (密度 1)。大きな空隙 (内腔・溝・手穴) は引いてある。
//                  小さな穴 (インサート・ピン・結束スロット) は中実のまま (finish 段で切る)
//   obstacle       絶対に空けておく空間 (密度 0)。preserve を引いてから渡す
//   design_space   最適化が材料を置いてよい空間 (y<=0 の箱 + ヒンジ柱)
//   preserve_solid finish 段で足し戻す形 (= preserve)
//   preserve_cuts  finish 段で引く穴 (obstacle 全部 + 小穴)
//   reference      人が見る用 (preserve 緑 + obstacle 赤 + design_space 灰)
//
// 座標系: 機体グローバル。build_axis = Z (+Z up 印刷、プレート = z -17)。
// =====================================================================

use <../../../../../../scad/lib/hardpoint.scad>

/* [Build] */
part = "reference";  // [reference, preserve, obstacle, design_space, preserve_solid, preserve_cuts]

/* [耐圧容器 (child_core_frame.scad v4 と同値)] */
tube_od    = 114.3;
cap_od     = 120.3;
cap_z0     = -13.8;
cap_z1     = -8.0;
flange_top = 208;
dome_ring_od = 120.3;
dome_ring_t  = 6.5;
eva_t      = 2.0;
eva_comp   = 0.8;
pocket_clr = 0.5;
pocket_rad = 0.75;
shell_t    = 6.0;
lip_b      = 2.7;
lip_t      = 3.0;

/* [ヒンジ] */
hinge_x    = -72;
hinge_y    = 10;
knu_od     = 16;
pin_d      = 5.4;
knu_h      = 30;
knu_gap    = 0.4;
cb_d       = 10;
cb_h       = 4;

/* [ラッチ受け] */
latch_x0   = 52;        // ボス x 範囲 (v4 の lf_x0=50 から 2 狭めた。ゲート側ボスは 52..72)
latch_x1   = 72;
latch_z    = [40, 170];
latch_hx   = 62;
ins_d      = 6.4;
boss_h     = 24;
boss_t     = 18;
latch_ins_h = 14;

/* [吊り耳ボス] */
lug_x      = 66;
lug_bolt_y = [-4, -16];
lug_boss_y = -22;
lug_boss_z = 204;
lug_x0     = 50;
lug_x1     = 72;

/* [把持バンド (preserve にする半殻の z 帯)] */
band_bot_z1 = -2;       // 下ポケット帯 z -17..-2 (コーン上端 -4.95 + リップ 3)
band_mid    = [92, 108];
band_top_z0 = 200;      // 上ポケット帯 z 200..218

/* [背面ケーブル溝 + 取っ手] */
py_y1      = -101;      // 背面壁 外面
gr_cx      = 18;
gr_w       = 10;
gr_d       = 8;
gr_ch      = 1;
ch_wall    = 2.5;       // 溝の側壁厚 (preserve)
ch_floor   = 4;         // 溝底の厚 (preserve)。v4 は 6 (壁 t14) — 残りは最適化に任せる
tie_z      = [0, 30, 60, 90, 155];
tie_w      = 5.5;
tie_h      = 3;
roof_z0    = 182;       // 溝の上端
bw_y1      = -87;       // v4 背面壁内面 (結束スロットの出口)
grip_z     = [145, 170];
grip_hw    = 30;
slot_hw    = 26;
slot_z     = [115, 145];
hand_y0    = -64;       // 指の入る空間の前端
hand_y1    = -88;       // 指の入る空間の後端 (バーの裏 1mm)

/* [HP1 ペデスタル] */
ped_x      = 30;
ped_y0     = -60;
ped_y1     = -110;
ped_z1     = 218.5;
hp1_cy     = -85;
pcab_d     = 12;
pcab_x     = 18;
pcab_y     = -92;
pcab_z0    = 174;
seat_t     = 4;         // 座面板の厚 (preserve)
ins_boss_d = 12;        // インサートまわりのボス径 (preserve)
hp_pitch   = 40;
hp_ins_h   = 8;
hp_ins_d   = 6.4;
hp_cable_d = 14;

/* [HP2/HP3] */
hp_face_x  = 44;
hp_cy      = -75;
hp_cz      = 100;
hp_pad     = 50;
pw_x0      = 24;        // v4 パイロン側壁内面 (HP 中央穴の貫通先)
hp_thru    = hp_face_x - pw_x0 + 2;

/* [下部ガードボス] */
gb_az      = [210, 330];
gb_r1      = 70;
gb_r0      = 62;        // preserve の内径 (v4 は r_in から)
gb_w       = 34;
gb_z0      = -14;
gb_z1      = 10;
gb_m5_z    = [-9, 4];
tab_r1     = 95;        // ガードリングのタブ + ボルトアクセスを空ける外径
tab_haz    = 18;

/* [設計空間] */
ds_x0      = -80;
ds_x1      = 72;
ds_y0      = -110;
ds_y1      = 0;
ds_z0      = -17;
ds_z1      = 218.5;
hp_env_x1  = 90;        // HP2/3 の外側に何も置かない範囲

/* [Hidden] */
fudge = 0.01;
BIG   = 400;
$fn = 96;

// ---- 導出値 (v4 と同式) ------------------------------------------------
r_in     = tube_od/2 + (eva_t - eva_comp);      // 58.35
r_out    = r_in + shell_t;                      // 64.35
pkt_r    = cap_od/2 + pocket_rad;               // 60.9
pb_z0    = cap_z0 - pocket_clr;
pb_z1    = cap_z1 + pocket_clr;
frame_z0 = pb_z0 - lip_b;                       // -17.0
pt_z0    = flange_top - pocket_clr;
pt_z1    = flange_top + dome_ring_t + pocket_clr;
frame_z1 = pt_z1 + lip_t;                       // 218.0
frame_h  = frame_z1 - frame_z0;
cone_h   = pkt_r - r_in;
gknu_zc  = [frame_z0, (frame_z0+frame_z1)/2 - knu_h/2, frame_z1 - knu_h];
aknu     = [[gknu_zc[0] + knu_h + knu_gap, gknu_zc[1] - knu_gap],
            [gknu_zc[1] + knu_h + knu_gap, gknu_zc[2] - knu_gap]];
cb_z     = aknu[1][1];
gb_haz   = asin((gb_w/2) / ((r_out + gb_r1)/2));
gr_y0    = py_y1 + gr_d;                        // -93
gr_x0    = gr_cx - gr_w/2;                      // 13
gr_x1    = gr_cx + gr_w/2;                      // 23
ch_x0    = gr_x0 - ch_wall;                     // 10.5
ch_x1    = gr_x1 + ch_wall;                     // 25.5
ch_y1    = gr_y0 + ch_floor;                    // -89
hp_iy    = [hp_cy - hp_pitch/2, hp_cy + hp_pitch/2];
hp_iz    = [hp_cz - hp_pitch/2, hp_cz + hp_pitch/2];
hp1_iy   = [hp1_cy - hp_pitch/2, hp1_cy + hp_pitch/2];
hp1_thru = ped_z1 - roof_z0 + 1;
hp_y0    = hp_cy + hp_pad/2;                    // -50
hp_y1    = hp_cy - hp_pad/2;                    // -100
hp_z0    = hp_cz - hp_pad/2;                    // 75
hp_z1    = hp_cz + hp_pad/2;                    // 125

// ---- 検査 -------------------------------------------------------------
assert(ds_x1 - ds_x0 <= 240 && ds_y1 - ds_y0 + 18 <= 240 && ds_z1 - ds_z0 <= 240,
       "設計空間が X1C の実用範囲 (250 - 余白 5×2) を超える");
assert(band_bot_z1 >= pb_z1 + cone_h + 2, "下ポケット帯がコーン上端 +2 より低い");
assert(band_top_z0 <= pt_z0 - 4, "上ポケット帯が上ポケットより 4mm 以上下から始まっていない");
assert(ch_x0 > 0 && ch_x1 <= grip_hw, "溝チャンネルが中心を跨ぐか把持バーからはみ出す");
assert(hand_y1 <= ch_y1 + 1 + fudge, "指空間がバー/溝チャンネルの裏 (y -89) に食い込む");
assert(grip_z[0] == slot_z[1], "把持バーは手穴直上に置く");
assert(hp_face_x - seat_t - (hp_ins_h + 1) >= 30, "HP2/3 インサートボスがパイロン側壁 x30 より内側に出る");
assert(ped_z1 - seat_t - (hp_ins_h + 1) > pcab_z0, "HP1 インサートボス下端が縦穴の下端より低い");
assert(sqrt(pow(pcab_x - hp_pitch/2, 2) + pow(pcab_y - min(hp1_iy), 2)) >= pcab_d/2 + hp_ins_d/2 + 2,
       "縦穴と HP1 後列インサートの残り肉 < 2mm");
assert(gb_r1 - gb_r0 >= 8, "ガードボスのインサート深さ 8 が preserve に収まらない");
assert(latch_x0 >= 52, "ラッチボスがゲート側ボス (52..72) より内側に出る");
echo(str("v5 setup: r_in ", r_in, " r_out ", r_out, " aknu ", aknu, " band ", [frame_z0, band_bot_z1], band_mid, [band_top_z0, frame_z1]));

// ---- 共通モジュール --------------------------------------------------
module half_y_neg(z0, z1) {            // y<=0 の半空間 (z 帯)
    translate([-BIG/2, -BIG, z0]) cube([BIG, BIG, z1 - z0]);
}
module wedge(az0, az1, z0, h) {
    intersection() {
        rotate([0, 0, az0]) translate([0, 0, z0]) cube([200, 200, h]);
        rotate([0, 0, az1 - 90]) translate([0, 0, z0 - fudge]) cube([200, 200, h + 2*fudge]);
    }
}
module band(z0, z1) {                  // 半殻の z 帯 (内腔・ポケットは bore_void で引く)
    intersection() {
        translate([0, 0, z0]) cylinder(r = r_out, h = z1 - z0);
        half_y_neg(z0 - fudge, z1 + fudge);
    }
}

// ---- 空間 (obstacle の元) ---------------------------------------------
// 内腔 + ポケット + 45° コーン (v4 と同式)。容器と EVA が入る空間
module bore_void() {
    translate([0, 0, ds_z0 - 3]) cylinder(r = r_in, h = ds_z1 - ds_z0 + 6);
    translate([0, 0, pb_z0]) cylinder(r = pkt_r, h = pb_z1 - pb_z0);
    translate([0, 0, pb_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
    translate([0, 0, pt_z0]) cylinder(r = pkt_r, h = pt_z1 - pt_z0);
    translate([0, 0, pt_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
}
// ゲートの半殻 (y>=0 かつ r<=r_out)。コアはここに材料を出さない
module gate_half() {
    intersection() {
        translate([0, 0, ds_z0 - 3]) cylinder(r = r_out, h = ds_z1 - ds_z0 + 6);
        translate([-BIG/2, 0, ds_z0 - 4]) cube([BIG, BIG/2, ds_z1 - ds_z0 + 8]);
    }
}
// ゲート側ナックル ×3 が占める柱 (アフトナックルの隙間)。x -81..-63、y 0..19
module gate_knuckles() {
    zs = [[ds_z0 - 1, aknu[0][0]], [aknu[0][1], aknu[1][0]], [aknu[1][1], ds_z1 + 1]];
    for (z = zs)
        translate([hinge_x - knu_od/2 - 1, 0, z[0]])
            cube([knu_od + 2, hinge_y + knu_od/2 + 1, z[1] - z[0]]);
}
// 背面ケーブル溝 ×2 (幅 10 × 深 8) と口の面取り
module grooves() {
    for (s = [-1, 1]) {
        translate([s*gr_cx - gr_w/2, py_y1 - 1, ds_z0 - 1])
            cube([gr_w, gr_d + 1, roof_z0 - ds_z0 + 1]);
        cd45 = gr_ch * sqrt(2);
        for (sx = [-1, 1])
            translate([s*gr_cx + sx*gr_w/2, py_y1, ds_z0 - 1]) rotate([0, 0, 45])
                translate([-cd45/2, -cd45/2, 0]) cube([cd45, cd45, roof_z0 - ds_z0 + 1]);
    }
}
// 結束スロット (溝底 → 空洞) と、その裏でバンドを通す小空間
module tie_slots() {
    for (s = [-1, 1], z = tie_z)
        translate([s*gr_cx - tie_w/2, gr_y0 - fudge, z - tie_h/2])
            cube([tie_w, bw_y1 - gr_y0 + 2, tie_h]);
}
module tie_backspace() {
    for (s = [-1, 1], z = tie_z)
        if (z < slot_z[0])
            translate([s*gr_cx - 5, bw_y1 - 1, z - 6]) cube([10, 12, 12]);
}
// 手穴 + 指の空間 (把持バーの下と裏)
module hand_room() {
    // 手穴: 背面壁を貫通 (v4 と同じ 52 × 30)、外面より 2mm 手前から指空間まで
    translate([-slot_hw, py_y1 - 2, slot_z[0]]) cube([2*slot_hw, hand_y1 - (py_y1 - 2) + 1, slot_z[1] - slot_z[0]]);
    // 指の空間: 手穴の奥 (バー下) とバーの裏 (z 115..182)
    translate([-slot_hw, hand_y1, slot_z[0]]) cube([2*slot_hw, hand_y0 - hand_y1, roof_z0 - slot_z[0]]);
}
// ケーブルの空洞: HP2/3 中央穴の出口 (x 22) から背面壁内面 (結束スロット) まで
module cable_cavity() {
    for (s = [-1, 1])
        translate([s > 0 ? 6 : -pw_x0, bw_y1 - 1, hp_cz - 16]) cube([pw_x0 - 6, hand_y0 - bw_y1 + 1, 32]);
}
// ペデスタル縦ケーブル穴 Ø12 ×2 と HP1 の穴
module hp1_holes() {
    for (s = [-1, 1])
        translate([s*pcab_x, pcab_y, pcab_z0]) cylinder(d = pcab_d, h = ds_z1 - pcab_z0 + 5, $fn = 48);
    translate([0, hp1_cy, ped_z1]) hp40_cut(cable = true, through_t = hp1_thru, insert_h = hp_ins_h);
}
// HP2/3 の穴
module hp23_holes() {
    for (s = [-1, 1])
        translate([s*hp_face_x, hp_cy, hp_cz]) rotate([0, s*90, 0])
            hp40_cut(cable = true, through_t = hp_thru, insert_h = hp_ins_h);
}
// HP2/3 の外側 (アクセサリ + ボルト) を空ける
module hp23_envelope() {
    for (s = [-1, 1])
        translate([s > 0 ? hp_face_x : -hp_env_x1, hp_y1 - 1, hp_z0 - 4])
            cube([hp_env_x1 - hp_face_x, hp_y0 - hp_y1 + 2, hp_z1 - hp_z0 + 8]);
}
// ガードリングのタブ (r70..82) + ボルトアクセス
module guard_tabs() {
    for (az = gb_az)
        intersection() {
            difference() {
                translate([0, 0, ds_z0 - 1]) cylinder(r = tab_r1, h = 12.5 - ds_z0 + 1);
                translate([0, 0, ds_z0 - 2]) cylinder(r = gb_r1, h = 12.5 - ds_z0 + 3);
            }
            wedge(az - tab_haz, az + tab_haz, ds_z0 - 1, 12.5 - ds_z0 + 1);
        }
}
// 小穴 (preserve の中を通る。解析では中実、finish 段で切る)
module small_holes() {
    translate([hinge_x, hinge_y, ds_z0 - 3]) cylinder(d = pin_d, h = ds_z1 - ds_z0 + 6, $fn = 32);
    translate([hinge_x, hinge_y, cb_z - cb_h]) cylinder(d = cb_d, h = cb_h + 1, $fn = 48);
    for (z = latch_z)
        translate([latch_hx, -latch_ins_h, z]) rotate([-90, 0, 0]) cylinder(d = ins_d, h = latch_ins_h + 1, $fn = 32);
    for (sx = [-1, 1], yy = lug_bolt_y)
        translate([sx*lug_x, yy, frame_z1 - 10]) cylinder(d = ins_d, h = 10 + 1, $fn = 32);
    for (az = gb_az, z = gb_m5_z)
        rotate([0, 0, az]) translate([gb_r1 - 8, 0, z]) rotate([0, 90, 0]) cylinder(d = ins_d, h = 8 + 1, $fn = 32);
    hp1_holes();
    hp23_holes();
    tie_slots();
}

// ---- preserve (機能面) ---------------------------------------------------
module preserve_bodies() {
    // 把持帯 ×3 (下ポケット / 中央 / 上ポケット)
    band(frame_z0, band_bot_z1);
    band(band_mid[0], band_mid[1]);
    band(band_top_z0, frame_z1);
    // アフトナックル ×2 (円筒のみ。角ブロックは最適化に任せる)
    for (b = aknu)
        translate([hinge_x, hinge_y, b[0]]) cylinder(d = knu_od, h = b[1] - b[0]);
    // ラッチボス ×2
    for (z = latch_z)
        translate([latch_x0, -boss_t, z - boss_h/2]) cube([latch_x1 - latch_x0, boss_t, boss_h]);
    // 吊り耳ボス ×2
    for (sx = [-1, 1])
        translate([sx > 0 ? lug_x0 : -lug_x1, lug_boss_y, lug_boss_z])
            cube([lug_x1 - lug_x0, -lug_boss_y, frame_z1 - lug_boss_z]);
    // 下部ガードボス ×2 (r 62..70 の帯)
    for (az = gb_az)
        intersection() {
            difference() {
                translate([0, 0, gb_z0]) cylinder(r = gb_r1, h = gb_z1 - gb_z0);
                translate([0, 0, gb_z0 - fudge]) cylinder(r = gb_r0, h = gb_z1 - gb_z0 + 2*fudge);
            }
            wedge(az - gb_haz, az + gb_haz, gb_z0 - fudge, gb_z1 - gb_z0 + 2*fudge);
        }
    // 背面ケーブル溝チャンネル ×2 (溝 + 側壁 2.5 + 底 4)
    for (s = [-1, 1])
        translate([s > 0 ? ch_x0 : -ch_x1, py_y1, frame_z0]) cube([ch_x1 - ch_x0, ch_y1 - py_y1, roof_z0 - frame_z0]);
    // 把持バー
    translate([-grip_hw, py_y1, grip_z[0]]) cube([2*grip_hw, ch_y1 - py_y1, grip_z[1] - grip_z[0]]);
    // HP1 ペデスタル座面板 + インサートボス ×4
    translate([-ped_x, ped_y1, ped_z1 - seat_t]) cube([2*ped_x, ped_y0 - ped_y1, seat_t]);
    for (sx = [-1, 1], yy = hp1_iy)
        translate([sx*hp_pitch/2, yy, ped_z1 - hp_ins_h - 1 - 2]) cylinder(d = ins_boss_d, h = hp_ins_h + 1 + 2);
    // HP2/3 座面板 + インサートボス ×4 (法線 ±X)
    for (s = [-1, 1]) {
        translate([s > 0 ? hp_face_x - seat_t : -hp_face_x, hp_y1, hp_z0]) cube([seat_t, hp_pad, hp_pad]);
        for (yy = hp_iy, zz = hp_iz)
            translate([s*hp_face_x, yy, zz]) rotate([0, -s*90, 0])
                cylinder(d = ins_boss_d, h = hp_ins_h + 1 + 2);
    }
}
module preserve_all() {
    difference() {
        preserve_bodies();
        bore_void();
        gate_half();
        grooves();
        hand_room();
    }
}

// ---- obstacle (部品の外の空間。preserve を引いて渡す) ---------------------
module obstacle_declared() {
    bore_void();
    gate_half();
    gate_knuckles();
    grooves();
    tie_slots();
    tie_backspace();
    hand_room();
    cable_cavity();
    hp1_holes();
    hp23_holes();
    hp23_envelope();
    guard_tabs();
}
module obstacle_all() {
    difference() {
        obstacle_declared();
        preserve_bodies();   // 小穴は preserve の中では obstacle にしない (finish 段で切る)
    }
}

// ---- design_space -----------------------------------------------------
module design_space() {
    translate([ds_x0, ds_y0, ds_z0]) cube([ds_x1 - ds_x0, ds_y1 - ds_y0, ds_z1 - ds_z0]);
    // ヒンジ柱 (y 0..18): アフトナックルを設計空間の中に入れる
    translate([ds_x0, 0, ds_z0]) cube([hinge_x + knu_od/2 + 1 - ds_x0, hinge_y + knu_od/2 + 1, ds_z1 - ds_z0]);
}

// ---- finish 段 --------------------------------------------------------
module preserve_cuts() {
    obstacle_declared();
    small_holes();
}

// ---- 出力 -------------------------------------------------------------
if (part == "preserve" || part == "preserve_solid") preserve_all();
else if (part == "obstacle") obstacle_all();
else if (part == "design_space") design_space();
else if (part == "preserve_cuts") preserve_cuts();
else {
    color("green") preserve_all();
    color("red", 0.5) obstacle_all();
    %design_space();
}
