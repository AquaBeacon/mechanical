// =====================================================================
// child_cam_bridge_v1.scad — カメラブリッジ トポロジー最適化の設計空間定義
//
// 現行 child_cam_bridge (328.1 cm³) を「機能面 = preserve」「空けておく空間 =
// obstacle」「残り = design_space」に分解して topopt (TO_printing/topopt) に渡す。
// **部品そのものではない。**
//
// 寸法はすべて child_cam_bridge.scad / child_side_bumper.scad / child_jaw_gate.scad
// の Customizer 値をそのまま再掲した **二重定義** である。元ファイルを直したら
// ここも直すこと (Body_Models/CLAUDE.md 設計規約 4)。
//
// part= で出力を選ぶ:
//   preserve       絶対に残す機能面 (密度 1)。小穴 (M5・ナットトラップ) は
//                  中実のまま置き、finish 段の cuts で切る
//   obstacle       絶対に空けておく空間 (密度 0)。design_space で切り、
//                  preserve を引いてから渡す
//   design_space   最適化が材料を置いてよい空間 (現行 bbox と同じ単純な箱)
//   preserve_solid finish 段で足し戻す形 (= preserve)
//   preserve_cuts  finish 段で引く穴 (obstacle 全部 + 小穴)
//   reference      人が見る用 (preserve 緑 + obstacle 赤 + design_space 灰)
//
// 座標系: 機体グローバル。X 左右 (基線) / Y 前後 (+Y 前 = カメラ向き) / Z 上。
// build_axis = Y (印刷は +Y up。md「印刷」節: 中央柱を床にした +Y up)。
// =====================================================================

/* [Build] */
part = "reference";  // [reference, preserve, obstacle, design_space, preserve_solid, preserve_cuts]

/* [HP40 / child_jaw_gate 側 (二重定義: child_jaw_gate.scad, child_cam_bridge.scad)] */
hp4_z         = 170;    // HP4 座中心 z
hp5_z         = 100;    // HP5 座中心 z
hpl_z         = 15;     // HP-L 座中心 z
hp_half       = 25;     // 座 (シェルフ) 半幅 (x, z とも)
hp_seat_y     = 74.35;  // 座面 (共通平面)。法線 +Y
hp_shelf_dep  = 12;     // シェルフ奥行き (座面から -Y へ)
hp_pitch_half = 20;     // M5 穴オフセット
hp_bolt_d     = 5.4;    // M5 クリアランス
adapter_t     = 6;      // 中央柱の板厚 (y)
gate_r_out    = 64.35;  // ゲート殻外径半径

/* [child_cam_mount 側 (二重定義: child_cam_mount.scad, child_cam_bridge.scad)] */
cm_lens_off_bot = 42.05;
cm_fin_x1       = 30;
cm_case_d       = 45.9;   // ケース奥行 (機体 Y)
cm_case_w       = 94.7;   // ケース幅 (横向きでは機体 X)
cm_case_h       = 84.1;   // ケース高さ (横向きでは機体 Z)
cm_plate_hw     = 22;     // 背面プレート半幅 (機体 Y)
cm_plate_hh     = 17;     // 背面プレート半高 (機体 X)
cm_fh_y         = 16;     // フレーム穴 Y オフセット
cm_fh_z         = 11;     // フレーム穴 X オフセット

/* [カメラ配置 (二重定義: child_cam_bridge.scad)] */
lens_z      = 125;
lens_x      = 75;
cam_y_shift = 14;
lens_y      = 106 + cam_y_shift;   // 120 (レンズ面)
fov_half    = 77.5;   // 対角 FOV 155° の半角 (水平 145° = 半角 72.5 を内包する保守側)
hood_len    = 8;      // レンズ面より前に material を許す量 (要件書 §2「フード 8mm 相当」)

/* [デッキ / 中央柱 / ウイング (二重定義: child_cam_bridge.scad)] */
deck_t       = 8;
deck_top     = lens_z - cm_lens_off_bot - cm_fin_x1;  // 52.95
deck_bot     = deck_top - deck_t;                     // 44.95
col_hw       = hp_half;                 // 25
col_y0       = hp_seat_y;               // 74.35
col_y1       = hp_seat_y + adapter_t;   // 80.35
wing_x1      = 120;    // ウイング外端 x (= 240 枠の半分)
end_plate_t  = 6;
end_plate_z1 = 80;
front_web_y0 = lens_y + 2;   // 122 (レンズ面より 2mm 前 = 前縁バンパ前面の後ろ側)
front_web_y1 = lens_y + 8;   // 128 (前縁バンパ前面 = フード限界)
rear_y0      = 67;     // 現行デッキ/後ウェブ後端 (ゲート殻 x=0 の y64.35 から 2.65mm)

/* [マウント取付穴 (二重定義: child_cam_bridge.scad)] */
m5_clear     = 5.4;
nut_af       = 8.2;
nut_dep      = 4.0;
mount_y0     = lens_y - cm_case_d / 2;                     // 97.05
mount_hole_y = [mount_y0 - cm_fh_y, mount_y0 + cm_fh_y];   // 81.05, 113.05
mount_hole_dx = cm_fh_z;                                   // 11

/* [側面バンパ取合い (二重定義: child_side_bumper.scad)] */
bumper_t    = 9;
case_gap    = 2;
bump_bolt_y = [80, 116];
bump_bolt_z = 65;

/* [工具アクセス] */
tool_d      = 12;    // HP4/HP5 の M5×8 を差す/回すための直線アクセス径

/* [設計空間 = 現行 bbox と同じ単純な箱 (240 x 61 x 150.05)] */
// 広げなかった理由:
//   x: ±120 が 240 枠 (md assert)。これ以上は side_bumper (内面 124.35) と衝突
//   y1: lens_y + 8 = 128 がフード限界 (要件書 §2)。奥行 250 枠 (149) より手前
//   y0: 67 がゲート殻 (r64.35) からの 2.65mm 離隔 (md assert)
//   z0: 44.95。ここより下げると マウント M5 のナットトラップ開口 (デッキ下面)
//       が埋まる。HP-L 座上端 (40) + 2 の制約より先にこちらが効く
//   z1: 195 = HP4 座上端 (md assert)
ds_x0 = -wing_x1;         // -120
ds_x1 =  wing_x1;         //  120
ds_y0 = rear_y0;          //  67
ds_y1 = front_web_y1;     //  128
ds_z0 = deck_bot;         //  44.95
ds_z1 = hp4_z + hp_half;  //  195

/* [preserve の切り出し寸法] */
pres_col_pad_hz = hp_half;    // 座パッドの z 半幅 (25 → HP4 145..195 / HP5 75..125)
pres_fb_x0      = 30;         // 前縁バンパ preserve の内端 (工具アクセス x26 から 4mm 離す)
pres_ep_x0      = wing_x1 - end_plate_t;  // 114

/* [Hidden] */
fudge = 0.01;
BIG   = 400;
$fn = 64;

// ---- 導出値 ---------------------------------------------------------
case_x0 = lens_x - cm_case_w / 2;    // 27.65
case_x1 = lens_x + cm_case_w / 2;    // 122.35
case_y0 = mount_y0 - cm_case_d / 2;  // 74.1
case_y1 = lens_y;                    // 120
case_z0 = deck_top + cm_fin_x1;      // 82.95
case_z1 = case_z0 + cm_case_h;       // 167.05
mp_x0   = lens_x - cm_plate_hh;      // 58
mp_x1   = lens_x + cm_plate_hh;      // 92
mp_y0   = mount_y0 - cm_plate_hw;    // 75.05
mp_y1   = mount_y0 + cm_plate_hw;    // 119.05
mp_z0   = deck_top;                  // 52.95
mp_z1   = case_z0;                   // 82.95
shelf_y0 = hp_seat_y - hp_shelf_dep; // 62.35
hp4_z0 = hp4_z - hp_half;  hp4_z1 = hp4_z + hp_half;   // 145 .. 195
hp5_z0 = hp5_z - hp_half;  hp5_z1 = hp5_z + hp_half;   //  75 .. 125
fov_r1 = hood_len * tan(fov_half);   // 36.09 (y = lens_y + 8 での視野半径)
tool_x = [-hp_pitch_half, hp_pitch_half];
tool_z = [hp5_z - hp_pitch_half, hp5_z + hp_pitch_half,
          hp4_z - hp_pitch_half, hp4_z + hp_pitch_half];   // 80,120,150,190

// ---- 検査 -----------------------------------------------------------
assert(ds_x1 - ds_x0 <= 240 && ds_y1 - ds_y0 <= 240 && ds_z1 - ds_z0 <= 240,
       "設計空間が X1C 実用枠 (250 - 余白 5x2 = 240) を超える");
assert(ds_y0 - gate_r_out >= 2.6, "設計空間後端がゲート殻 (r64.35) に 2.6mm 未満で接近");
assert(ds_z0 >= hpl_z + hp_half + 2, "設計空間下端が HP-L 座上端 (40) + 2 より低い");
assert(ds_z1 <= hp4_z + hp_half, "設計空間上端が HP4 座上端 (195) を超える");
assert(ds_y1 <= lens_y + hood_len, "設計空間前端がフード限界 (レンズ面 +8) を超える");
assert(case_x1 + case_gap + bumper_t <= 140, "側面バンパ外面が 280 枠 (半幅 140) を超える");
// FOV: preserve のうち最も前 (y=ds_y1) にある前縁バンパ/端板の最上端 z=80。
// レンズ軸 (lens_z=125) からの半径方向距離が視野半径 fov_r1 を上回ること。
fov_dz = lens_z - end_plate_z1;                 // 45
assert(fov_dz > fov_r1, "前縁バンパ/端板の上端が FOV 円錐 (半角 77.5°) に入る");
assert(atan(fov_dz / hood_len) > fov_half, "前縁バンパ前面が FOV 半角の内側");
// 工具アクセス (x 14..26) と 前縁バンパ preserve (x >= 30) が 1 ボクセル以上離れる
assert(pres_fb_x0 - (max(tool_x) + tool_d / 2) >= 3,
       "工具アクセス穴と前縁バンパ preserve が 3mm 未満で接近 (obstacle が preserve を貫く)");
assert(pres_ep_x0 > max(tool_x) + tool_d / 2, "工具アクセス穴が端板 preserve に届く");
echo(str("design_space = ", [ds_x1 - ds_x0, ds_y1 - ds_y0, ds_z1 - ds_z0],
         "  vol = ", (ds_x1-ds_x0)*(ds_y1-ds_y0)*(ds_z1-ds_z0), " mm3"));
echo(str("FOV: 半径 ", fov_r1, " @ y=", ds_y1, " / preserve 最近接 dz = ", fov_dz));

// ---- preserve / obstacle の AABB 総当り検査 ---------------------------
// box = [x0,x1,y0,y1,z0,z1]。厳密不等号なので面接触 (共有面) は非干渉扱い。
function box_overlap(a, b) =
    (a[0] < b[1]) && (b[0] < a[1]) &&
    (a[2] < b[3]) && (b[2] < a[3]) &&
    (a[4] < b[5]) && (b[4] < a[5]);

preserve_boxes = [
    ["column",   [-col_hw, col_hw, col_y0, col_y1, hp5_z0, hp4_z1]],
    ["mount_R",  [mp_x0, mp_x1, mp_y0, mp_y1, deck_bot, deck_top]],
    ["mount_L",  [-mp_x1, -mp_x0, mp_y0, mp_y1, deck_bot, deck_top]],
    ["endp_R",   [pres_ep_x0, wing_x1, ds_y0, ds_y1, deck_bot, end_plate_z1]],
    ["endp_L",   [-wing_x1, -pres_ep_x0, ds_y0, ds_y1, deck_bot, end_plate_z1]],
    ["fbump_R",  [pres_fb_x0, wing_x1, front_web_y0, front_web_y1, deck_bot, end_plate_z1]],
    ["fbump_L",  [-wing_x1, -pres_fb_x0, front_web_y0, front_web_y1, deck_bot, end_plate_z1]],
];

obstacle_boxes = concat([
    ["case_R",     [case_x0, case_x1, case_y0, case_y1, case_z0, case_z1]],
    ["case_L",     [-case_x1, -case_x0, case_y0, case_y1, case_z0, case_z1]],
    ["mplate_R",   [mp_x0, mp_x1, mp_y0, mp_y1, mp_z0, mp_z1]],
    ["mplate_L",   [-mp_x1, -mp_x0, mp_y0, mp_y1, mp_z0, mp_z1]],
    ["shelf_HP4",  [-hp_half, hp_half, shelf_y0, hp_seat_y, hp4_z0, hp4_z1]],
    ["shelf_HP5",  [-hp_half, hp_half, shelf_y0, hp_seat_y, hp5_z0, hp5_z1]],
], [ for (sx = tool_x, tz = tool_z)
       [str("tool_", sx, "_", tz),
        [sx - tool_d/2, sx + tool_d/2, col_y1, ds_y1 + 1, tz - tool_d/2, tz + tool_d/2]] ]);

for (pb = preserve_boxes)
    for (ob = obstacle_boxes)
        assert(!box_overlap(pb[1], ob[1]), str(pb[0], " が obstacle ", ob[0], " と交差する"));

// ---- obstacle の元 ----------------------------------------------------
// カメラ + 防水ケースの実体 (AABB、左右)
module cam_case() {
    for (s = [-1, 1])
        translate([s > 0 ? case_x0 : -case_x1, case_y0, case_z0])
            cube([case_x1 - case_x0, case_y1 - case_y0, case_z1 - case_z0]);
}
// child_cam_mount 本体 (背面プレート〜レジスタ面) の占有域
module cam_mount_body() {
    for (s = [-1, 1])
        translate([s > 0 ? mp_x0 : -mp_x1, mp_y0, mp_z0])
            cube([mp_x1 - mp_x0, mp_y1 - mp_y0, mp_z1 - mp_z0 + fudge]);  // ケースと面共有しないよう +fudge
}
// レンズの視野円錐 (半角 fov_half、レンズ面より前のみ。フード 8mm まで)
module fov_cone() {
    for (s = [-1, 1])
        translate([s * lens_x, lens_y, lens_z]) rotate([-90, 0, 0])
            cylinder(r1 = 0, r2 = (hood_len + 4) * tan(fov_half), h = hood_len + 4);
}
// ゲート HP シェルフ (HP4/HP5)。座面 y=74.35 より後ろの帯
module hp_shelves() {
    for (zc = [hp4_z, hp5_z])
        translate([-hp_half, shelf_y0, zc - hp_half])
            cube([2 * hp_half, hp_seat_y - shelf_y0, 2 * hp_half]);
}
// HP4/HP5 の M5x8 を差す/回す工具アクセス (座面前方 y80.35 から設計空間前端まで)
module tool_access() {
    for (sx = tool_x, tz = tool_z)
        translate([sx, col_y1, tz]) rotate([-90, 0, 0])
            cylinder(d = tool_d, h = ds_y1 - col_y1 + 2, $fn = 32);
}
module obstacle_declared() {
    cam_case();
    cam_mount_body();
    fov_cone();
    hp_shelves();
    tool_access();
}
// 設計空間の 1 ボクセルぶん外まででクリップする (領域外の obstacle はグリッドを
// 太らせるだけで何も保持しない — design-space.md「Cost」)
module ds_clip() {
    translate([ds_x0 - 3, ds_y0 - 3, ds_z0 - 3])
        cube([ds_x1 - ds_x0 + 6, ds_y1 - ds_y0 + 6, ds_z1 - ds_z0 + 6]);
}
module obstacle_all() {
    difference() {
        intersection() { obstacle_declared(); ds_clip(); }
        preserve_bodies();   // 小穴は preserve の中では obstacle にしない (finish 段で切る)
    }
}

// ---- preserve (機能面) ------------------------------------------------
module preserve_bodies() {
    // (1) 中央柱 = HP40 アダプタ板 (z 75..195 で連続): ゲートにボルト留めする面と
    //     M5x8 の座。**2026-09-05 v1a で HP4/HP5 の 2 パッドから連続板へ変更**。
    //     理由: 2 パッドを別々に置いて両方 fix xyz にすると HP5 だけで完全拘束が
    //     効いてしまい、最適化が HP4 を繋ぐ動機を持たない (v1 の run で HP4 パッド
    //     544 セルが単独コンポーネントとして残り connected=false になった)。
    //     現行部品も中央柱は z 44.95..195 の連続板であり、HP40 の 8 本は 1 枚の
    //     アダプタ板で受けるのが正しい取合い。
    translate([-col_hw, col_y0, hp5_z0])
        cube([2 * col_hw, col_y1 - col_y0, hp4_z1 - hp5_z0]);
    // (2) child_cam_mount の座 (デッキ厚全体。上面が register 面、下面がナットトラップ開口)
    for (s = [-1, 1])
        translate([s > 0 ? mp_x0 : -mp_x1, mp_y0, deck_bot])
            cube([mp_x1 - mp_x0, mp_y1 - mp_y0, deck_t]);
    // (3) 側面バンパ端板 (外面 x=±120 が バンパ L 形フットの密着面、M5x2 の座)
    for (s = [-1, 1])
        translate([s > 0 ? pres_ep_x0 : -wing_x1, ds_y0, deck_bot])
            cube([end_plate_t, ds_y1 - ds_y0, end_plate_z1 - deck_bot]);
    // (4) 前縁バンパ (レンズ面より 2mm 前 .. フード限界 8mm。L4 正面衝突の荷重導入面)
    for (s = [-1, 1])
        translate([s > 0 ? pres_fb_x0 : -wing_x1, front_web_y0, deck_bot])
            cube([wing_x1 - pres_fb_x0, front_web_y1 - front_web_y0,
                  end_plate_z1 - deck_bot]);
}
module preserve_all() { preserve_bodies(); }

// ---- design_space ------------------------------------------------------
module design_space() {
    translate([ds_x0, ds_y0, ds_z0])
        cube([ds_x1 - ds_x0, ds_y1 - ds_y0, ds_z1 - ds_z0]);
}

// ---- 小穴 (preserve の中を通る。解析では中実、finish 段で切る) ------------
// HP4/HP5 の M5x8 (軸 Y、中央柱を貫通)
module column_holes() {
    for (zc = [hp4_z, hp5_z], sx = tool_x, sz = [-hp_pitch_half, hp_pitch_half])
        translate([sx, col_y0 - fudge, zc + sz]) rotate([-90, 0, 0])
            cylinder(d = hp_bolt_d, h = adapter_t + 2 * fudge, $fn = 32);
}
// マウント M5 通し穴 + 下面ナットトラップ (軸 Z) — child_cam_bridge.scad の mount_bolt()
module mount_bolt(x, y) {
    translate([x, y, deck_bot - fudge]) cylinder(d = m5_clear, h = deck_t + 2*fudge, $fn = 32);
    translate([x, y, deck_bot - fudge]) cylinder(d = nut_af / cos(30), h = nut_dep + fudge, $fn = 6);
    translate([x, y, deck_bot + nut_dep - fudge])
        cylinder(d1 = nut_af / cos(30), d2 = m5_clear,
                 h = (nut_af / cos(30) - m5_clear)/2 + fudge, $fn = 32);
}
// バンパ締結ナットトラップ (軸 X、端板厚の範囲内) — child_cam_bridge.scad の bump_nut()
// (2026-09-04 修正済みの版。穴長は end_plate_t、トラップは外面から nut_dep のみ)
module bump_nut(sign, y) {
    ang = -90 * sign;
    translate([sign * (wing_x1 + fudge), y, bump_bolt_z]) rotate([0, ang, 0])
        cylinder(d = m5_clear, h = end_plate_t + 2 * fudge, $fn = 32);
    translate([sign * (wing_x1 + fudge), y, bump_bolt_z]) rotate([0, ang, 0])
        cylinder(d = nut_af / cos(30), h = nut_dep + fudge, $fn = 6);
}
module small_holes() {
    column_holes();
    for (s = [-1, 1], dx = [-mount_hole_dx, mount_hole_dx], y = mount_hole_y)
        mount_bolt(s * lens_x + dx, y);
    for (s = [-1, 1], y = bump_bolt_y) bump_nut(s, y);
}

// ---- finish 段 ---------------------------------------------------------
module preserve_cuts() {
    intersection() { obstacle_declared(); ds_clip(); }
    small_holes();
}

// ---- 出力 --------------------------------------------------------------
if (part == "preserve" || part == "preserve_solid") preserve_all();
else if (part == "obstacle") obstacle_all();
else if (part == "design_space") design_space();
else if (part == "preserve_cuts") preserve_cuts();
else {
    color("green") preserve_all();
    color("red", 0.5) obstacle_all();
    %design_space();
}
