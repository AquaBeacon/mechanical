// REVIEW INPUT: generated from historical setup; v3 latch updated.
// =====================================================================
// child_jaw_gate_v1.scad — ワニ顎ゲート トポロジー最適化の設計空間定義
//
// 現行 child_jaw_gate.scad (308.3 cm³) を「機能面 = preserve」「空けておく空間 =
// obstacle」「残り = design_space」に分解して topopt (topopt/topopt) に渡す。
// **部品そのものではない。** 相手側 child_core_frame/topo_v5/child_core_frame_v5.scad
// と同じ構成 (part= 切替 / obstacle は preserve を引いて渡す / 小穴は preserve 内では
// 中実にして finish 段の cuts で切る)。
//
// **寸法はすべて child_jaw_gate.scad の Customizer 値の二重定義**である。
// child_jaw_gate.scad を直したらこのファイルも同時に直すこと。
// 相手部品由来の値 (コア側ナックル z / child_cam_bridge のデッキ・キール・後ウェブ・
// 中央柱) も二重定義。出典は各 .md / .scad をコメントに書いた。
//
// part= で出力を選ぶ:
//   preserve       絶対に残す機能面 (密度 1)。大きな空隙 (内腔・ポケット) は引いてある。
//                  小さな穴 (M5 / インサート / ピン / ノブ頭ポケット) は中実のまま
//   obstacle       絶対に空けておく空間 (密度 0)。preserve を引いてから渡す
//   design_space   最適化が材料を置いてよい空間 (現行 bbox の箱)
//   preserve_solid finish 段で足し戻す形 (= preserve)
//   preserve_cuts  finish 段で引く穴 (obstacle 全部 + 小穴)
//   reference      人が見る用 (preserve 緑 + obstacle 赤 + design_space 灰)
//
// 座標系: 機体グローバル。チューブ軸 = Z、+Y = 前。本部品は y >= 0 側。
// build_axis = Z (+Z up 印刷、プレート = z -17)。
// =====================================================================

use <C:/Users/ryupc/WorkSpace/Mitou26/AquaBeacon-OSS/mechanical/scad/lib/hardpoint.scad>

/* [Build] */
part = "reference";  // [reference, preserve, obstacle, design_space, preserve_solid, preserve_cuts]

/* [耐圧容器 (child_jaw_gate.scad と同値)] */
tube_od    = 114.3;
cap_od     = 120.3;
cap_z0     = -13.8;
cap_z1     = -8.0;
flange_top = 208;
dome_ring_od = 120.3;   // 仮値 (未購入) — child_jaw_gate.md 要確認 1
dome_ring_t  = 6.5;     // 仮値
eva_t      = 2.0;
eva_comp   = 0.8;
pocket_clr = 0.5;
pocket_rad = 0.75;
shell_t    = 6.0;
lip_b      = 2.7;
lip_t      = 3.0;

/* [ヒンジ (-X 縁)] */
hinge_x    = -72;
hinge_y    = 10;
knu_od     = 16;
pin_d      = 5.4;
knu_h      = 30;
knu_gap    = 0.4;
pin_cb_d   = 10;        // ピン抜け止めざぐり (最上ナックル頂面)
pin_cb_h   = 4;

/* [ラッチ (+X 縁)] */
latch_z    = [40, 170];
latch_hx   = 62;
m5_d       = 5.4;
boss_y1 = 24;        // ボス前面 = ノブ頭の座
boss_h = 34;
knob_d     = 18;        // ノブ頭ポケット径
knob_dep   = 12;
knob_margin= 1;

/* [把持帯 (preserve にする半殻の z 帯。コア v5 と同値)] */
band_bot_z1 = -2;       // 下ポケット帯 z -17..-2
band_mid    = [92, 108];
band_top_z0 = 200;      // 上ポケット帯 z 200..218

/* [前面ハードポイント HP40 ×3] */
hp_half     = 25;       // 座 (シェルフ) 半幅
hp_seat_y   = 74.35;    // = r_out + 10 (下で assert)
seat_t      = 4;        // 座面板の厚 (preserve)
ins_boss_d  = 12;       // インサートまわりのボス径 (preserve)
hp_pitch    = 40;
hp_insert_h = 9;
hp_ins_d    = 6.4;
hp_cable_d  = 14;
// [名前, xc, zc, cable, cable_dep]
front_hp = [
    ["HP4",  0, 170, false, 0],
    ["HP5",  0, 100, false, 0],
    ["HP-L", 0,  15, true, 12],
];

/* [コアフレーム側 (二重定義: child_core_frame/topo_v5、child_jaw_gate.md インタフェース節)] */
core_knu_z = [[13.4, 85.1], [115.9, 187.6]];  // コア側ナックル (ゲートの隙間に入る)
core_band  = 9;         // コア半殻 (y<=0) を宣言する帯の深さ (3 ボクセル)。
                        // design_space が y>=0 なので全深さを宣言しても格子を太らせるだけ

/* [child_cam_bridge 側の占有域 (二重定義: child_cam_bridge.scad)] */
brg_deck_z  = [44.95, 52.95];   // デッキ x -120..120、y 67..124
brg_deck_y0 = 67;
brg_clr     = 2.65;             // ゲート殻 (x=0 で y 64.35) との離隔 (ブリッジ側 assert)
brg_keel_z1 = 74;               // キール上端 (x±25、y 67..80.35)
brg_web_x0  = 27;               // 後ウェブ内端 (x ±27..120、y 67..73、z 44.95..160)
brg_web_z1  = 160;
brg_case_z1 = 167.05;           // カメラケース上端 (背面 y 74.1、x ±27..122)
brg_col_y1  = 80.35;            // 中央柱 前面 (x±25、y 74.35..80.35、z 44.95..195)

/* [設計空間 = 現行 bbox] */
ds_x0      = -80;
ds_x1      = 72;
ds_y0      = 0;
ds_y1      = 74.35;
ds_z0      = -17;
ds_z1      = 218;
obs_y1     = 77.35;     // obstacle の y 上限 (ds_y1 + 1 ボクセル)。これ以上は格子の無駄
knob_acc_d = 24;        // ノブ頭 (Ø16) の挿入・回転に要る通路径 (仮値 — 要確認)
knob_acc_h = 30;        // その通路の奥行き (y、ボス前面 y=16 から +Y へ)

/* [Hidden] */
fudge = 0.01;
BIG   = 400;
$fn = 96;

// ---- 導出値 (child_jaw_gate.scad と同式) --------------------------------
r_in     = tube_od/2 + (eva_t - eva_comp);        // 58.35
r_out    = r_in + shell_t;                        // 64.35
pkt_r    = cap_od/2 + pocket_rad;                 // 60.9
pb_z0    = cap_z0 - pocket_clr;                   // -14.3
pb_z1    = cap_z1 + pocket_clr;                   // -7.5
gate_z0  = pb_z0 - lip_b;                         // -17.0
pt_z0    = flange_top - pocket_clr;               // 207.5
pt_z1    = flange_top + dome_ring_t + pocket_clr; // 215.0
gate_z1  = pt_z1 + lip_t;                         // 218.0
gate_h   = gate_z1 - gate_z0;
cone_h   = pkt_r - r_in;                          // 2.55
knu_zc   = [gate_z0, (gate_z0+gate_z1)/2 - knu_h/2, gate_z1 - knu_h];  // -17 / 85.5 / 188
boss_half_x = knob_d/2 + knob_margin;             // 10
boss_x0  = latch_hx - boss_half_x;                // 52
boss_x1  = latch_hx + boss_half_x;                // 72
ins_boss_h = hp_insert_h + 1 + 2;                 // 12 (穴 9+1 + 底肉 2)
hp_ix    = [-hp_pitch/2, hp_pitch/2];
brg_y0   = brg_deck_y0 - brg_clr;                 // 64.35 = r_out。ここより外は空ける

// ---- 検査 -------------------------------------------------------------
assert(hp_seat_y == r_out + 10, "hp_seat_y が r_out + 10 と一致しない (二重定義のずれ)");
assert(ds_x1 - ds_x0 <= 240 && ds_y1 - ds_y0 <= 240 && ds_z1 - ds_z0 <= 240,
       "設計空間が X1C の実用範囲 (250 - 余白 5x2) を超える");
assert(ds_z0 == gate_z0 && ds_z1 == gate_z1, "設計空間の z が現行部品の z 範囲と違う");
assert(ds_x0 <= hinge_x - knu_od/2 && ds_x1 >= boss_x1, "設計空間がヒンジ/ラッチを含まない");
assert(ds_y1 >= hp_seat_y, "設計空間が HP 座面を含まない");
assert(band_bot_z1 >= pb_z1 + cone_h + 2, "下ポケット帯がコーン上端 +2 より低い");
assert(band_top_z0 <= pt_z0 - 4, "上ポケット帯が上ポケットより 4mm 以上下から始まっていない");
assert(band_mid[0] > pb_z1 + cone_h && band_mid[1] < pt_z0, "中央把持帯がポケットに掛かる");
// ゲート側ナックル ×3 とコア側ナックル ×2 が互い違いに噛み合う (遊び knu_gap)
assert(abs(core_knu_z[0][0] - (knu_zc[0] + knu_h)) - knu_gap < 0.05 + fudge,
       "コア側ナックル 下端が ゲート下ナックル 上端 + 遊びと合わない");
assert(abs(knu_zc[1] - core_knu_z[0][1]) - knu_gap < 0.05 + fudge,
       "ゲート中ナックル 下端が コア側ナックル 上端 + 遊びと合わない");
assert(abs(core_knu_z[1][0] - (knu_zc[1] + knu_h)) - knu_gap < 0.05 + fudge,
       "コア上ナックル 下端が ゲート中ナックル 上端 + 遊びと合わない");
assert(abs(knu_zc[2] - core_knu_z[1][1]) - knu_gap < 0.05 + fudge,
       "ゲート上ナックル 下端が コア上ナックル 上端 + 遊びと合わない");
// HP 座は互いに z で重ならない (総当り)
for (i = [0 : len(front_hp) - 1], j = [0 : len(front_hp) - 1])
    if (i < j)
        assert(abs(front_hp[i][2] - front_hp[j][2]) > 2*hp_half,
               str(front_hp[i][0], "/", front_hp[j][0], ": HP 座が z 方向に重なる"));
// HP 座 (x ±25) と ブリッジ後ウェブ (|x| >= 27) が x で離れている
assert(brg_web_x0 > hp_half, "後ウェブの内端が HP 座の外幅より内側にある");
// ブリッジのデッキ/キールが HP-L 座 (z<=40) と HP5 座 (z>=75) に掛からない
assert(brg_deck_z[0] - brg_clr > front_hp[2][2] + hp_half,
       "デッキ (離隔込み) が HP-L 座に掛かる");
assert(brg_keel_z1 < front_hp[1][2] - hp_half, "キール上端が HP5 座に掛かる");
// インサートボスがシェル外面より外に出ている (内腔・シェル帯と別体)
shell_y_at20 = sqrt(r_out*r_out - pow(hp_pitch/2, 2));   // 61.15
assert(hp_seat_y - ins_boss_h >= shell_y_at20 + 1,
       "インサートボスの内端がシェル外面に食い込む");
// ノブ頭ポケット
assert(boss_y1 - knob_dep >= 4 - 1e-6, "ノブポケット底の残り厚 < 4mm");
assert(boss_half_x >= knob_d/2 + 1 - 1e-6, "ボス幅がノブポケットを収められない");
echo(str("v1 setup: r_in ", r_in, " r_out ", r_out, " gate z ", gate_z0, "..", gate_z1,
         " knu_zc ", knu_zc, " bands ", [gate_z0, band_bot_z1], band_mid, [band_top_z0, gate_z1]));

// ---- 共通モジュール --------------------------------------------------
module half_y_pos(z0, z1) {            // y>=0 の半空間 (z 帯)
    translate([-BIG/2, 0, z0]) cube([BIG, BIG, z1 - z0]);
}
module band(z0, z1) {                  // 半殻の z 帯 (内腔・ポケットは bore_void で引く)
    intersection() {
        translate([0, 0, z0]) cylinder(r = r_out, h = z1 - z0);
        half_y_pos(z0 - fudge, z1 + fudge);
    }
}

// ---- 空間 (obstacle の元) ---------------------------------------------
// 内腔 + 上下ポケット + 45° コーン。容器 (チューブ + EVA + キャップ/ドームリム) が入る。
// y < -core_band は design_space (y>=0) の外なので宣言しない — 宣言すると領域 bbox が
// y -67 まで伸び、何も拘束しない固定 0 セルに格子の 4 割を使ってしまう
module bore_void() {
    intersection() {
        union() {
            translate([0, 0, ds_z0 - 3]) cylinder(r = r_in, h = ds_z1 - ds_z0 + 6);
            translate([0, 0, pb_z0]) cylinder(r = pkt_r, h = pb_z1 - pb_z0);
            translate([0, 0, pb_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
            translate([0, 0, pt_z0]) cylinder(r = pkt_r, h = pt_z1 - pt_z0);
            translate([0, 0, pt_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
        }
        translate([-BIG/2, -core_band, ds_z0 - 5]) cube([BIG, BIG, ds_z1 - ds_z0 + 10]);
    }
}
// コアフレームの半殻 (y<=0 かつ r<=r_out)。ゲートはここに材料を出さない。
// design_space が y>=0 なので、合わせ面を宣言する 3 ボクセルぶんだけ書く
// (全深さを宣言すると領域 bbox が y -64 まで伸びて格子が 1.6 倍になるだけで何も拘束しない)
module core_half() {
    intersection() {
        translate([0, 0, ds_z0 - 3]) cylinder(r = r_out, h = ds_z1 - ds_z0 + 6);
        translate([-BIG/2, -core_band, ds_z0 - 4]) cube([BIG, core_band, ds_z1 - ds_z0 + 8]);
    }
}
// コア側ナックル ×2 が占める柱 (ゲートナックルの隙間)。x -81..-63、y 0..19
module core_knuckles() {
    for (b = core_knu_z)
        translate([hinge_x - knu_od/2 - 1, 0, b[0]])
            cube([knu_od + 2, hinge_y + knu_od/2 + 1, b[1] - b[0]]);
}
// ヒンジの開閉スイープ + 工具アクセス: ピン軸より外 (x < hinge_x) かつナックル上 (y > 18)。
// ここに材料を置くと 90° 開くときにコア側ナックル柱を掃く (child_jaw_gate.md 部品外の考慮)
module hinge_swing() {
    translate([ds_x0 - 3, hinge_y + knu_od/2, ds_z0 - 3])
        cube([hinge_x - (ds_x0 - 3), obs_y1 - (hinge_y + knu_od/2), ds_z1 - ds_z0 + 6]);
}
// ノブボルトの挿入通路 + 指 (工具) の空間: ラッチボス前面 (y=16) から +Y へ Ø24。
// 現行部品はこの通路が半殻 (方位角 ~15..25°) で塞がっており、頭 Ø16 を
// ポケットまで差し込めない。ここを obstacle にして最適化に空けさせる。
module finger_room() {
    for (z = latch_z)
        translate([latch_hx, boss_y1, z]) rotate([-90, 0, 0])
            cylinder(d = knob_acc_d, h = knob_acc_h, $fn = 48);
}
// child_cam_bridge の占有域 + 離隔。ゲート殻の外面 (y = brg_y0 = 64.35) より前は空ける
module bridge_zone() {
    // 外側 (|x| >= 27): デッキ + 後ウェブ + カメラケース背面
    for (s = [-1, 1])
        translate([s > 0 ? brg_web_x0 : ds_x0 - 3, brg_y0, brg_deck_z[0] - brg_clr])
            cube([s > 0 ? ds_x1 + 3 - brg_web_x0 : -brg_web_x0 - (ds_x0 - 3),
                  obs_y1 - brg_y0, brg_case_z1 - (brg_deck_z[0] - brg_clr)]);
    // 内側 (|x| < 27): デッキ (z 44.95..52.95) + キール (z ..74)
    translate([-brg_web_x0, brg_y0, brg_deck_z[0] - brg_clr])
        cube([2*brg_web_x0, obs_y1 - brg_y0, brg_keel_z1 - (brg_deck_z[0] - brg_clr)]);
}
// HP 座の外側 (アクセサリ + M5 ボルト頭): ブリッジ中央柱 / ライトクランプ
module hp_envelope() {
    for (hp = front_hp)
        translate([hp[1] - hp_half, hp_seat_y, hp[2] - hp_half])
            cube([2*hp_half, obs_y1 - hp_seat_y, 2*hp_half]);
}
// HP40 の穴 (インサート下穴 ×4 + HP-L の中央 Ø14)
module hp_holes() {
    for (hp = front_hp)
        translate([hp[1], hp_seat_y, hp[2]]) rotate(a = 180, v = [0, 1, 1])
            hp40_cut(cable = hp[3], insert_h = hp_insert_h,
                     through_t = hp[3] ? hp[4] : hp_insert_h + 4);
}
// 小穴 (preserve の中を通る。解析では中実、finish 段で切る)
module small_holes() {
    // ヒンジピン Ø5.4 通し + 抜け止めざぐり Ø10×4 (最上ナックル頂面)
    translate([hinge_x, hinge_y, ds_z0 - 3]) cylinder(d = pin_d, h = ds_z1 - ds_z0 + 6, $fn = 32);
    translate([hinge_x, hinge_y, gate_z1 - pin_cb_h]) cylinder(d = pin_cb_d, h = pin_cb_h + 1, $fn = 48);
    // ラッチ M5 通し穴 ×2 (軸 Y) + ノブ頭ポケット Ø18×12 (底 45° コーン)
    for (z = latch_z) {
        translate([latch_hx, -1, z]) rotate([-90, 0, 0]) cylinder(d = m5_d, h = boss_y1 + 2, $fn = 32);

    }
    hp_holes();
}

// ---- preserve (機能面) ------------------------------------------------
module preserve_bodies() {
    // 把持帯 ×3 (下ポケット / 中央 / 上ポケット)
    band(gate_z0, band_bot_z1);
    band(band_mid[0], band_mid[1]);
    band(band_top_z0, gate_z1);
    // ゲート側ナックル ×3 (円筒のみ。アーム/フランジ板は最適化に任せる)
    for (zc = knu_zc)
        translate([hinge_x, hinge_y, zc]) cylinder(d = knu_od, h = knu_h);
    // ラッチボス ×2 (ノブ頭ポケットを持つ側。ポケットは finish 段で切る)
    for (z = latch_z)
        difference() {
            translate([boss_x0, 0, z - boss_h/2]) cube([boss_x1-boss_x0,boss_y1,boss_h]);
            bd = (boss_y1-16)*sqrt(2);
            translate([boss_x0-1,16,z-boss_h/2]) rotate([-45,0,0])
                translate([0,-bd,-bd]) cube([boss_x1-boss_x0+2,bd,bd]);
        }
    // 前面ハードポイント ×3: 座面板 (t4) + インサートボス (Ø12 × 12) ×4
    for (hp = front_hp) {
        translate([hp[1] - hp_half, hp_seat_y - seat_t, hp[2] - hp_half])
            cube([2*hp_half, seat_t, 2*hp_half]);
        for (dx = hp_ix, dz = hp_ix)
            translate([hp[1] + dx, hp_seat_y, hp[2] + dz]) rotate([90, 0, 0])
                cylinder(d = ins_boss_d, h = ins_boss_h);
    }
}
module preserve_all() {
    difference() {
        preserve_bodies();
        bore_void();
        translate([-BIG/2, -BIG, ds_z0 - 5]) cube([BIG, BIG, ds_z1 - ds_z0 + 10]);  // y<0 を落とす
    }
}

// ---- obstacle (部品の外の空間。preserve を引いて渡す) ---------------------
module obstacle_declared() {
    bore_void();
    core_half();
    core_knuckles();
    hinge_swing();
    finger_room();
    bridge_zone();
    hp_envelope();
    hp_holes();
}
module obstacle_all() {
    difference() {
        obstacle_declared();
        preserve_bodies();   // 小穴は preserve の中では obstacle にしない (finish 段で切る)
    }
}

// ---- design_space -----------------------------------------------------
// 単純な箱 = 現行部品の bbox。ヒンジ柱はナックルが y 2..18 にあるので y>=0 で自然に入る
module design_space() {
    translate([ds_x0, ds_y0, ds_z0]) cube([ds_x1 - ds_x0, ds_y1 - ds_y0, ds_z1 - ds_z0]);
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
