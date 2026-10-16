// =====================================================================
// child_frame_plate.scad — 子機 フレームベースプレート
// 中央にWTE4チューブクランプ×2(child_clamp_base)、左右端にOsmoアーム
// (child_osmo_arm)、前縁に水中ライト、後方コーナーにTD04Aソケット
// (xdcr_socket、チューブ横で上向き)、中央下面沿いにおもりスロット。
// 座標系: X=左右(基線方向)、Y=前後(チューブ軸/進行方向、+Y=前)、原点=中心。
// 印刷向き: 平置き。ベッド250角に収まらない場合は45°置き or 2分割(要相談)。
// =====================================================================

/* [プレート] */
plate_x   = 200;    // 幅 (左右)
plate_y   = 300;    // 長さ (前後) ※ベッドに載らない場合は2分割を相談
plate_t   = 6;      // 板厚

/* [チューブクランプ (child_clamp_base と一致)] */
clamp_cy  = 60;     // クランプ中心の前後位置(±)
clamp_cd  = 54;     // クランプ底板の奥行(干渉チェック用)
clamp_cw  = 180;    // クランプ底板の幅(干渉チェック用)
clamp_mx  = 80;     // クランプM5 X(±)
clamp_my  = 20;     // クランプM5 Y(クランプ中心から±)

/* [Osmoアーム取付 (child_osmo_arm と一致)] */
arm_hx    = [70, 90];   // アームM5 X位置(両側)
arm_hy    = 30;         // アームM5 Y(±)

/* [TD04Aソケット取付 (xdcr_socket と一致、後方左右コーナー)] */
xd_cx     = 70;     // ソケット中心X(±両舷どちらでも付くよう左右対称に設ける)
xd_cy     = 120;    // ソケット中心Y(後方= -Y側)
xd_base   = 60;     // ソケットベース一辺(干渉チェック用)
xd_pitch  = 40;     // ソケットM5ピッチ(±20) ※xdcr_socket の hole_p と一致

/* [水中ライト取付 (前縁)] */
light_hx  = 15;     // M4 X(±)
light_hy  = [100, 120]; // M4 Y(前方+Y)

/* [おもりスロット] */
w_slot_x  = 30;     // スロット中心X(±)
w_slot_w  = 10;     // スロット幅
w_slot_l  = 140;    // スロット長さ(Y)

/* [穴径] */
m5_d      = 5.3;
m4_d      = 4.5;
grid_d    = 5.3;    // 汎用40mmグリッド穴

$fn = 64;

// ---- 干渉チェック -----------------------------------------------------
// 部品footprint同士(クランプ底板 vs XDソケットベース)が重ならないこと
assert(xd_cy - xd_base/2 > clamp_cy + clamp_cd/2 + 2,
       str("XDソケットベース(y", -(xd_cy - xd_base/2),
           ")が後クランプ底板(y", -(clamp_cy + clamp_cd/2), ")に乗り上げ"));
// XDソケットベースがプレート内に収まること
assert(xd_cy + xd_base/2 <= plate_y/2 && xd_cx + xd_base/2 <= plate_x/2,
       "XDソケットベースがプレートからはみ出し");
// 全ボルト穴の最近接ペア距離 (穴径+3mm 以上)
hole_list = concat(
    [for (sy=[-1,1], sx=[-1,1], dy=[-1,1]) [sx*clamp_mx, sy*clamp_cy + dy*clamp_my]],
    [for (sx=[-1,1], hx=arm_hx, sy=[-1,1]) [sx*hx, sy*arm_hy]],
    [for (sx=[-1,1], dx=[-1,1], dy=[-1,1]) [sx*xd_cx + dx*xd_pitch/2, -xd_cy + dy*xd_pitch/2]],
    [for (sx=[-1,1], hy=light_hy) [sx*light_hx, hy]]);
for (i=[0:len(hole_list)-2]) for (j=[i+1:len(hole_list)-1])
    assert(norm(hole_list[i]-hole_list[j]) >= m5_d + 3,
           str("穴同士が接近: ", hole_list[i], " と ", hole_list[j]));
// 縁距離
assert(plate_y/2 - max(light_hy[0], light_hy[1]) - m4_d/2 >= 4, "ライトM4の端距離不足");
assert(plate_y/2 - xd_cy - xd_pitch/2 - m5_d/2 >= 4, "XDソケットM5の端距離不足");
// おもりスロットとクランプM5
assert(w_slot_x + w_slot_w/2 + 2 < clamp_mx - m5_d/2,
       "おもりスロットとクランプM5が干渉(X)");

// ---- 本体 -------------------------------------------------------------
difference() {
    translate([-plate_x/2, -plate_y/2, 0]) cube([plate_x, plate_y, plate_t]);

    // チューブクランプ M5 ×4 ×2箇所 (前後クランプ)
    for (sy=[-1,1]) for (sx=[-1,1]) for (dy=[-1,1])
        translate([sx*clamp_mx, sy*clamp_cy + dy*clamp_my, -0.5])
            cylinder(d=m5_d, h=plate_t+1);

    // Osmoアーム M5 ×4 ×両側
    for (sx=[-1,1]) for (hx=arm_hx) for (sy=[-1,1])
        translate([sx*hx, sy*arm_hy, -0.5]) cylinder(d=m5_d, h=plate_t+1);

    // TD04Aソケット M5 ×4 ×両舷後方 (左右どちらにも付けられる)
    for (sx=[-1,1]) for (dx=[-1,1]) for (dy=[-1,1])
        translate([sx*xd_cx + dx*xd_pitch/2, -xd_cy + dy*xd_pitch/2, -0.5])
            cylinder(d=m5_d, h=plate_t+1);

    // 水中ライト M4 (前縁中央)
    for (sx=[-1,1]) for (hy=light_hy)
        translate([sx*light_hx, hy, -0.5]) cylinder(d=m4_d, h=plate_t+1);

    // おもりスロット (M8ボルト/ベルト通し)
    for (sx=[-1,1])
        translate([sx*w_slot_x - w_slot_w/2, -w_slot_l/2, -0.5])
            cube([w_slot_w, w_slot_l, plate_t+1]);

    // 汎用40mmグリッド (他と2.65+2mm以上離れたセルのみ)
    for (gx=[-80:40:80]) for (gy=[-120:40:120]) {
        clash =
            // クランプ穴近傍
            (abs(abs(gy)-clamp_cy) <= clamp_my + 8 && abs(abs(gx)-clamp_mx) <= 8) ||
            // アーム穴近傍
            (abs(gy) <= arm_hy + 8 && abs(gx) >= arm_hx[0] - 8) ||
            // XD穴近傍
            (abs(gy + xd_cy) <= xd_pitch/2 + 8 && abs(abs(gx)-xd_cx) <= xd_pitch/2 + 8) ||
            // ライト穴近傍
            (gy >= light_hy[0] - 8 && abs(abs(gx)-light_hx) <= 8) ||
            // おもりスロット近傍
            (abs(gy) <= w_slot_l/2 + 8 && abs(abs(gx)-w_slot_x) <= w_slot_w/2 + 8);
        if (!clash)
            translate([gx, gy, -0.5]) cylinder(d=grid_d, h=plate_t+1);
    }
}
