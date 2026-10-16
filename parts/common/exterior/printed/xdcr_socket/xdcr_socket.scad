// =====================================================================
// xdcr_socket.scad — TD04A 振動子ソケット (子機/親機 共用)
// 円筒ソケットに TD04A(実測Ø26仮定+0.4)を差し込み、結束バンド2本で保持。
// - 子機: tilt_deg=0 のまま child_frame_plate 後方コーナーへ。開口を上に
//   向け、振動子は上向き(親機と対面)。
// - 親機: tilt_deg=20 で再ビルドし、マストヘッドプレートの下面に開口を
//   下に向けて取付(下向き前傾20°)。
// 印刷向き: ベースを下に平置き。ソケットは垂直円筒で無サポート
// (tilt>0 のときはスカートが45°を保証)。
// =====================================================================

/* [傾き] */
tilt_deg  = 0;       // ソケット軸の傾き(0=垂直 / 親機は20)

/* [取付ベース] */
base_w    = 60;
base_t    = 6;
hole_p    = 40;      // M5 4穴ピッチ(±20) ※frame plate の xd_pitch と一致
m5_d      = 5.3;

/* [ソケット] */
xdcr_d    = 26.4;    // TD04A胴径(要実測) + 0.4
wall      = 5;       // ソケット肉厚
depth     = 32;      // 差込み深さ
floor_t   = 6;       // ソケット底厚
cable_d   = 9;       // 底のケーブル/水抜き穴
tie_w     = 5.5;     // 結束バンドスロット幅
tie_t     = 3;       // 同 厚み
tie_z     = [12, 24];// スロット高さ(ソケット底面基準)

$fn = 96;

// ---- 導出 -----------------------------------------------------------
boss_od  = xdcr_d + 2*wall;          // 36.4
boss_h   = floor_t + depth;          // 38
skirt_od = boss_od + 2*boss_h*tan(tilt_deg) + 4;

// ---- チェック ---------------------------------------------------------
assert(tilt_deg <= 25, "傾き25°超は片持ちが大きすぎる(要形状見直し)");
assert(hole_p/2 + m5_d/2 + 2 < base_w/2, "M5穴の端距離不足");
assert(boss_od/2 + boss_h*tan(tilt_deg) < base_w/2 + 10,
       "傾きでソケットがベースから大きくはみ出し");
// M5頭(Ø8.5)がソケットのスカートに乗り上げないこと
assert(sqrt(2)*hole_p/2 - 4.25 > skirt_od/2 + 0.5,
       str("M5頭がスカートと干渉: 頭内縁 ", sqrt(2)*hole_p/2 - 4.25,
           " < スカート半径 ", skirt_od/2));

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // ベース
        translate([-base_w/2, -base_w/2, 0]) cube([base_w, base_w, base_t]);
        // ソケットボス (傾きは X軸回り)
        rotate([tilt_deg, 0, 0]) union() {
            cylinder(d=boss_od, h=boss_h);
            // スカート(傾き時の付け根補強・45°保証)
            cylinder(d1=skirt_od, d2=boss_od, h=(skirt_od-boss_od)/2);
        }
    }
    // ソケット内腔
    rotate([tilt_deg, 0, 0]) translate([0, 0, floor_t])
        cylinder(d=xdcr_d, h=boss_h);
    // 底ケーブル穴 (ソケット軸沿いに貫通)
    rotate([tilt_deg, 0, 0]) translate([0, 0, -base_t - 3])
        cylinder(d=cable_d, h=floor_t + base_t + 6);
    // 結束バンドスロット (ソケットを水平に貫通、バンドは外周を回す)
    for (tz=tie_z)
        rotate([tilt_deg, 0, 0])
            translate([-boss_od/2 - 2, -tie_t/2, floor_t + tz - tie_w/2])
                cube([boss_od + 4, tie_t, tie_w]);
    // M5 取付穴 ×4 (±hole_p/2)
    for (sx=[-1,1]) for (sy=[-1,1])
        translate([sx*hole_p/2, sy*hole_p/2, -0.5])
            cylinder(d=m5_d, h=base_t + 1);
}
