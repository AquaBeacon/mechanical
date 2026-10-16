// =====================================================================
// parent_float_segment.scad — 親機 リング浮子 1/4セグメント (4個印刷)
// OD300 / ID140 / 高さ80 のリングを4分割した上面開放シェル。
// 印刷後に2液発泡ウレタンを充填し、表面はエポキシ塗布(仕様メモ準拠)。
// 隣接セグメントとは端面のM5ボルト2本+Ø8ダウエルピン1本(市販ロッド)で
// 結合。ボルト/ナットはキャビティ側(上開口)から工具アクセスする。
// 中央開口Ø140に防水ボックスマウント(別途)が載る。
// 印刷向き: このまま(開口上)。壁は垂直・底閉止でサポート不要。
// bbox ~150×150 で220角ベッドに収まる。
// =====================================================================

/* [リング] */
ring_od  = 300;
ring_id  = 140;
ring_h   = 80;
wall     = 3;      // 側壁厚
floor_t  = 3;      // 底厚

/* [端面ジョイント] */
end_t    = 8;      // 端面(角度方向)の壁厚
m5_d     = 5.3;
bolt_r   = [95, 130];  // ボルトの半径位置
bolt_z   = 40;         // ボルト高さ
pin_d    = 8.3;        // ダウエルØ8 + 0.3
pin_r    = 112.5;      // ピン半径位置
pin_z    = 20;         // ピン高さ
pin_dp   = 12;         // ピン穴深さ(片側)

$fn = 180;

// ---- 導出 -----------------------------------------------------------
r_out  = ring_od/2;  r_in = ring_id/2;
// 端面壁の角度幅(中央半径で end_t を確保)
r_mid  = (r_out + r_in)/2;
a_wall = end_t / r_mid * 180/PI;    // ≈ 4.17°

// ---- チェック ---------------------------------------------------------
assert(r_out - r_in > 2*wall + 20, "リング断面が薄すぎ");
for (br=bolt_r)
    assert(br > r_in + m5_d && br < r_out - m5_d, "ボルト半径位置がリング外");
assert(abs(pin_r - r_mid) < (r_out - r_in)/2 - pin_d, "ピン位置がリング外");
assert(bolt_z > floor_t + m5_d && bolt_z < ring_h - m5_d, "ボルト高さ不正");
// ボルトとピンの干渉(端面内での距離)
for (br=bolt_r)
    assert(sqrt(pow(br - pin_r, 2) + pow(bolt_z - pin_z, 2)) > (m5_d + pin_d)/2 + 3,
           "端面のボルトとピンが接近");

// ---- 90°くさび (0°..90°を +X/+Y 象限で) --------------------------------
module wedge(a0, a1, r) {
    // 原点扇形 (a0..a1, 半径r) の多角形
    n = max(2, ceil((a1 - a0)/3));
    polygon(concat([[0,0]],
        [for (i=[0:n]) [r*cos(a0 + (a1-a0)*i/n), r*sin(a0 + (a1-a0)*i/n)]]));
}

difference() {
    // 外殻: 1/4リング
    linear_extrude(height = ring_h)
        intersection() {
            difference() { circle(r=r_out); circle(r=r_in); }
            wedge(0, 90, r_out + 1);
        }
    // キャビティ: 側壁 wall・端面 a_wall・底 floor_t を残し上開放
    translate([0, 0, floor_t])
        linear_extrude(height = ring_h)
            intersection() {
                difference() { circle(r=r_out - wall); circle(r=r_in + wall); }
                wedge(a_wall, 90 - a_wall, r_out + 1);
            }
    // 端面ボルト穴 M5 ×2 (0°端面: 法線=Y / 90°端面: 法線=X)
    for (br=bolt_r) {
        translate([br, -1, bolt_z]) rotate([-90, 0, 0])
            cylinder(d=m5_d, h=end_t + 6);        // 0°面 (y=0)
        translate([-1, br, bolt_z]) rotate([0, 90, 0])
            cylinder(d=m5_d, h=end_t + 6);        // 90°面 (x=0)
    }
    // ダウエルピン穴 (両端面、深さ pin_dp)
    translate([pin_r, -0.5, pin_z]) rotate([-90, 0, 0])
        cylinder(d=pin_d, h=pin_dp + 0.5);
    translate([-0.5, pin_r, pin_z]) rotate([0, 90, 0])
        cylinder(d=pin_d, h=pin_dp + 0.5);
}

echo(str("端面角度壁=", a_wall, "°  リング全体の排水量=",
         PI*(r_out*r_out - r_in*r_in)*ring_h/1e6, "L(全没時)"));
