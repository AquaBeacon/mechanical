// =====================================================================
// child_cam_lid.scad — カメラポッド 押え蓋 (2個印刷)
//
// child_shell_fwd のカメラポッドに落とし込んだ DJI Osmo Action 6 を
// 上から押さえる。M4 蝶ボルト 2 本で着脱 (数秒)。
// 押えパッドの下面に 2mm EVA スポンジを貼り、締めると 0.6mm 潰れて
// カメラをポッド底の位置決めパッドへ押し付ける = Z の再現性が出る。
//
// 座標系 (この部品のローカル):
//   x = 0    : ポッドの X 中心 (レンズ軸。lens_dx=0 のとき)
//   y = 0    : ポッド後壁の外面
//   z = 0    : ポッド側壁の上端 (child_shell_fwd の pod_top)
//   → アセンブリでは translate([±75, 70.3, 145]) で置く
//
// 印刷向き: **上下逆さま** (z=lid_t の平面をベッドに置く)。
//   押えパッド・位置決めリムが上を向き、サポート不要。
// =====================================================================

/* [カメラ / ポッド (child_shell_fwd と一致させること)] */
cam_w     = 72.8;
cam_h     = 47.2;
cam_d     = 33.1;
cam_clr   = 0.6;
lens_y    = 110;
cam_ax_z  = 115;
pod_wall  = 7;
pod_rear  = 6;
hood      = 8;
pod_top   = 145;
lid_sc_y  = 90;             // 蓋ねじの y (グローバル)

/* [蓋] */
lid_t     = 10;             // 板厚
lid_ov    = 1.5;            // ポッド側壁より外へ出す量 (ねじの端距離 + 水切り)
m4_d      = 4.5;            // M4 蝶ボルト クリアランス
base_line = 150;            // 外形枠チェック用 (child_shell_fwd と一致)
foam_t    = 2.0;            // 押えパッドに貼る EVA スポンジ厚
preload   = 0.6;            // 締結時のスポンジ潰し代
pad_w     = 26;             // 押えパッド 幅 (Y)
pad_hw    = 30;             // 同 半幅 (X)
rim_t     = 3;              // 位置決めリム 幅
rim_h     = 2;              // 同 高さ
rim_clr   = 0.5;            // 同 クレードルとのすきま (片側)

/* [上面ボタンのアクセス窓 — 位置は要実測] */
win_on    = true;
win_hw    = 25;             // 半幅 (X)
win_y0    = 4;              // y 範囲 (ポッド後壁外面から)
win_y1    = 20;

$fn = 96;

// ---- 導出 -----------------------------------------------------------
in_hw    = (cam_w + cam_clr)/2;          // 36.7 クレードル内 半幅
in_y0    = lens_y - cam_d - cam_clr;     // 76.3 クレードル内 後端
pod_y0   = in_y0 - pod_rear;             // 70.3 ポッド後壁 外面 (= ローカル y=0)
lid_hw   = in_hw + pod_wall + lid_ov;    // 45.2
lid_len  = lens_y + hood - pod_y0;       // 47.7
cam_top  = cam_ax_z + cam_h/2;           // 138.6 カメラ上面 (グローバル z)
gap      = pod_top - cam_top;            // 6.4  蓋下面 → カメラ上面
pad_h    = gap - foam_t + preload;       // 押えパッド 高さ
sc_x     = in_hw + pod_wall/2;           // 40.2 蓋ねじ x (側壁の肉厚中心)
sc_y     = lid_sc_y - pod_y0;            // 19.7 同 y (ローカル)
rim_x    = in_hw - rim_clr;              // 位置決めリム 外側 x
rim_y0   = in_y0 - pod_y0 + rim_clr;     // 同 y 範囲 (クレードル内)
rim_y1   = lens_y - pod_y0 - rim_clr;

// ---- 干渉・成立性チェック --------------------------------------------
assert(pad_h > 1.5, str("押えパッドが低すぎる (", pad_h, "mm)。pod_top を上げること"));
assert(pad_h + foam_t - preload == gap, "押え代の計算が合っていない");
assert(rim_h < gap - 1, str("位置決めリムがカメラ上面に当たる: rim_h=", rim_h, " gap=", gap));
assert(sc_x - m4_d/2 > in_hw + 0.5,
       str("蓋ねじがクレードル内腔に掛かる: ", sc_x - m4_d/2, " <= ", in_hw));
assert(sc_x + m4_d/2 < lid_hw - 2,
       str("蓋ねじの外側端距離不足: 残り ", lid_hw - sc_x - m4_d/2, "mm。lid_ov を増やすこと"));
// 蓋はポッドより少しだけ広い。機体の最大幅を決めるのでここで枠を確認する
assert(2*(base_line/2 + lid_hw) <= 250,
       str("蓋込みの全幅 ", 2*(base_line/2 + lid_hw), " が 250 超"));
assert(sc_y > 4 && sc_y < lid_len - 4, "蓋ねじの y 端距離不足");
assert(pad_hw + 1 < in_hw, "押えパッドがクレードルより広い (蓋が入らない)");
// rim_x はリムの**外側端**。クレードル内幅より小さければ落とし込める
assert(rim_x < in_hw - 0.2,
       str("位置決めリムがクレードルに入らない: ", rim_x, " >= ", in_hw));
assert(rim_t >= 2 && rim_t < 6, "位置決めリムの幅が不適当");
if (win_on) {
    assert(win_hw + 2 < rim_x - rim_t, "アクセス窓が位置決めリムに掛かる");
    assert(win_y1 < rim_y1 - 2 && win_y0 > rim_y0 - 4, "アクセス窓が位置決めリムに掛かる (Y)");
    assert(win_hw + 3 < sc_x - m4_d/2 || win_y1 + 3 < sc_y || win_y0 - 3 > sc_y,
           "アクセス窓が蓋ねじに掛かる");
}

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        translate([-lid_hw, 0, 0]) cube([2*lid_hw, lid_len, lid_t]);
        // 押えパッド x2 (下面。EVA スポンジを貼る面)
        for (py = [rim_y0 + 6, rim_y1 - 6 - pad_w])
            translate([-pad_hw, py, -pad_h]) cube([2*pad_hw, pad_w, pad_h]);
        // 位置決めリム (クレードルに落として蓋の XY を決める。カメラには当たらない)
        difference() {
            translate([-rim_x, rim_y0, -rim_h]) cube([2*rim_x, rim_y1-rim_y0, rim_h]);
            translate([-rim_x+rim_t, rim_y0+rim_t, -rim_h-1])
                cube([2*(rim_x-rim_t), rim_y1-rim_y0-2*rim_t, rim_h+2]);
        }
    }
    // M4 蝶ボルト 通し穴
    for (sx=[-1,1]) translate([sx*sc_x, sc_y, -pad_h-2]) cylinder(d=m4_d, h=lid_t+pad_h+4);
    // 上面ボタンのアクセス窓 (位置は要実測。win_on=false で塞げる)
    if (win_on)
        translate([-win_hw, win_y0, -2]) cube([2*win_hw, win_y1-win_y0, lid_t+4]);
    // 水抜き・通水
    for (sx=[-1,1]) translate([sx*15, lid_len-6, -2]) cylinder(d=6, h=lid_t+4);
}

echo(str("蓋 ", 2*lid_hw, " x ", lid_len, " x ", lid_t, " (パッド込み高さ ", lid_t+pad_h, ")"));
echo(str("押えパッド高さ=", pad_h, " + EVA ", foam_t, "mm → 潰し代 ", preload));
echo(str("アセンブリ配置: translate([±(base_line/2 - lens_dx), ", pod_y0, ", ", pod_top, "])"));
