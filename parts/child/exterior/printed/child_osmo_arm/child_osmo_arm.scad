// =====================================================================
// child_osmo_arm.scad — 子機 Osmoアーム (左右共通、2個印刷)
// child_frame_plate の側縁に M5×4 で固定し、GoPro互換2フィンガー
// マウントを基線 125 / 150 / 175 mm (片側) の3位置に持つ。
// カメラの前傾(下向き20°)はGoProナックルの角度で調整する。
// 座標系: X=外向き(フレーム中心が x=0)、Y=前後。プレートと同じ向きで
// フレームプレートの上面に重ね、下からM5ボルト+ナットで共締め。
// 印刷向き: 平置き(このまま)。フィンガーは垂直壁で無サポート。
// =====================================================================

/* [取付部 (child_frame_plate と一致)] */
hole_x   = [70, 90];   // M5 X位置 (フレーム座標)
hole_y   = 30;         // M5 Y(±)
m5_d     = 5.3;
pad_x0   = 60;         // 取付パッドの内側端
pad_x1   = 100;        // 取付パッドの外側端 (=プレート端と一致)
pad_y    = 80;         // 取付パッド幅(Y)
arm_t    = 6;          // 板厚

/* [ビーム] */
beam_w   = 40;         // ビーム幅(Y)
rib_h    = 10;         // 縁リブ高さ
rib_t    = 4;          // 縁リブ厚

/* [GoProフィンガー] */
base_line = [125, 150, 175]; // 基線半値 = フィンガー中心のX位置
fin_t    = 3.0;        // フィンガー厚
fin_gap  = 3.4;        // フィンガー間隔 (カメラ側3枚爪の中1枚分)
fin_w    = 15;         // フィンガー奥行(Y)
fin_h    = 16;         // フィンガー高さ
pin_d    = 5.2;        // M5ノブボルト穴
pin_z    = 10;         // 穴中心高さ(ビーム上面から)

$fn = 64;

// ---- 導出 -----------------------------------------------------------
beam_x1 = base_line[2] + fin_w/2 + 3;   // ビーム外端
fin_off = fin_gap/2 + fin_t/2;          // フィンガー中心の振り分け

// ---- チェック ---------------------------------------------------------
assert(base_line[0] - fin_w/2 > pad_x1, "最内フィンガーが取付パッドに乗り上げ");
assert(pin_z + pin_d/2 < fin_h - 1.5, "ピン穴がフィンガー上端に接近");
for (i=[0:1])
    assert(base_line[i+1] - base_line[i] >= fin_w + 8,
           "フィンガー同士のピッチ不足(カメラ幅と要照合)");

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // 取付パッド
        translate([pad_x0, -pad_y/2, 0]) cube([pad_x1 - pad_x0, pad_y, arm_t]);
        // ビーム (パッドから外へ)
        translate([pad_x1 - 0.1, -beam_w/2, 0])
            cube([beam_x1 - pad_x1 + 0.1, beam_w, arm_t]);
        // 縁リブ (ビーム両縁、曲げ剛性)
        for (sy=[-1,1])
            translate([pad_x1 - 0.1, sy*beam_w/2 - (sy>0 ? rib_t : 0), 0])
                cube([beam_x1 - pad_x1 + 0.1, rib_t, arm_t + rib_h]);
        // GoPro 2フィンガー ×3位置
        // 板面の法線=X(基線方向) → ピボット軸がX → カメラは前後にピッチ
        // (下向き20°はナックル角で設定)。
        for (bx=base_line) for (s=[-1,1])
            translate([bx + s*fin_off - fin_t/2, -fin_w/2, arm_t])
                cube([fin_t, fin_w, fin_h]);
    }
    // M5 取付穴 ×4
    for (hx=hole_x) for (sy=[-1,1])
        translate([hx, sy*hole_y, -0.5]) cylinder(d=m5_d, h=arm_t+1);
    // フィンガーピン穴 (X方向貫通)
    for (bx=base_line)
        translate([bx - fin_off - fin_t/2 - 1, 0, arm_t + pin_z])
            rotate([0, 90, 0]) cylinder(d=pin_d, h=2*(fin_off + fin_t/2) + 2);
}

echo(str("フィンガー中心X=", base_line, " → 基線=", [for (b=base_line) 2*b], "mm"));
