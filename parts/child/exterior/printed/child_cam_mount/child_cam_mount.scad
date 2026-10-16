// =====================================================================
// child_cam_mount.scad — 子機 カメラマウント (縦向き防水ケース用)
//
// DJI Osmo Action 6 を純正防水ケースに入れたまま「縦向き (ポートレート)」に
// 保持する小部品。ケース底面の DJI クイックリリース デュアルタブ
// (GoPro 2 フィンガー互換) を本部品の 3 フィンガーで受け、M5 ボルト 1 本で
// 締結する。ケース底面はフィンガー脇の 2 本の柱の前面 (レジスタ面) に
// 突き当たり、ヨー/ピッチの再現性を出す。
//
// 縦向き配置: ケース底面 (タブ側) は機体中心を向く (内向き)。左右のカメラで
// 同一部品を使う (本部品は y=0 面に対して対称)。
// コアフレーム側インタフェース: 背面プレートの M5 ×4 (y=±16, z=±11)。
//
// ★ 寸法はすべて公称/推定の仮値 (2026-08-02 ユーザ指示: 実測は後日)。
//   実測後に [防水ケース] ブロックを置換して再ビルドすること。
//
// 座標系 (部品ローカル): +X = ケース側 (機体では内→外)、+Y = 前 (レンズ向き)、
//   +Z = 上。背面プレートの背面が x=0。
// 印刷向き: このまま (z=-17 の底面をベッドへ)。フィンガーの間隙 3.4mm は
//   16mm ブリッジで printable (タブ側クリアランス 0.4 が垂れを吸収)。
//   荷重 (カメラ慣性によるフィンガー曲げ) の引張は XY 面内。
// 荷重ケース: L2 輸送 = カメラ+ケース 0.26 kg × 10g ≈ 26 N (全方向)。
//   quick_strength beam (b=48,t=3,L=20,F=30): 8.3 MPa / 許容 12 → PASS
//   quick_strength lug  (hole=5.2,t=9,F=60): 面圧 1.3 MPa → PASS
// =====================================================================

/* [防水ケース (公称・仮値 — 要実測)] */
case_w    = 94.7;    // ケース幅 (縦向きでは Z 方向 = 上下)
case_h    = 84.1;    // ケース高さ (縦向きでは X 方向 = 基線方向)
case_d    = 45.9;    // ケース奥行 (レンズ軸 Y 方向)
lens_off_bot = 42.05; // レジスタ面 (fin_x1, ケース底面の突き当て) →レンズ軸の距離。
                      // 仮 = case_h/2。要実測。★横向き搭載 (child_cam_bridge) でも
                      // 同じ定義で使う (デッキ高さ導出は bridge 側で
                      // deck_top = lens_z - lens_off_bot - fin_x1 として計算する)

/* [クイックリリース タブ (GoPro 互換想定・仮値 — 要実測)] */
tab_t     = 3.0;     // ケース側タブ 1 枚の厚さ
tab_w     = 16.0;    // タブ幅 (Y 方向)
tab_len   = 18.0;    // ケース底面からのタブ突出量
tab_hole_off = 9.0;  // ケース底面 → タブ穴中心の距離 (仮)
tab_clr   = 0.4;     // タブ厚に対する間隙の遊び

/* [フィンガー] */
fin_t     = 3.0;     // 本部品フィンガー厚
fin_w     = 16.0;    // フィンガー幅 (Y)
fin_len   = 22.0;    // フィンガー長 (X)。タブ 18 より長くして頭の逃げを作る
bolt_d    = 5.2;     // M5 通し
hex_af    = 8.1;     // M5 ナットトラップ 二面幅 (+0.1)
hex_dep   = 5.0;

/* [背面プレート (コアフレームへ M5 ×4)] */
plate_t   = 8.0;
plate_hw  = 22.0;    // 半幅 (Y)
plate_hh  = 17.0;    // 半高 (Z)
fh_y      = 16.0;    // フレーム穴 Y 位置 (±)
fh_z      = 11.0;    // フレーム穴 Z 位置 (±)
m5_d      = 5.4;     // M5 クリアランス

/* [レジスタ柱 (ケース底面の突き当て)] */
post_w    = 6.0;     // 柱の幅 (Y)
post_gap  = 2.4;     // フィンガー側面 → 柱内面のクリアランス
post_top  = 12.0;    // 柱の上端 z

/* [機体レベル検査 (仮値)] */
base_line = 150.0;   // ステレオ基線
env_half  = 140.0;   // 全幅 280 の半分 (2026-09-04 子機外装_改善要件 C5/C8: 250→280 に緩和)
bumper_min = 5.0;    // 外側に残す保護構造の最小代 (旧・縦向き検査用、現在は未使用)
bumper_t  = 9.0;     // child_side_bumper の板厚 (二重定義: child_side_bumper.scad と揃える)

/* [Hidden] */
fudge = 0.01;

// ---- 導出値 ---------------------------------------------------------
gap_t    = tab_t + tab_clr;               // フィンガー間隙 3.4
fin_x0   = plate_t;                       // フィンガー根元
fin_x1   = plate_t + fin_len;             // フィンガー先端 = レジスタ面
bolt_x   = fin_x1 - tab_hole_off;         // タブ穴と揃う M5 位置
stack_h  = 3*fin_t + 2*gap_t;             // 15.8
fin_zc   = [-(fin_t+gap_t), 0, fin_t+gap_t]; // フィンガー中心 z (-6.4/0/+6.4)
ped_top  = fin_zc[0] - fin_t/2;           // 台座上面 = 最下フィンガー下面 (-7.9)
post_y0  = fin_w/2 + post_gap;            // 柱内面 (10.4)
post_y1  = post_y0 + post_w;              // 柱外面 (16.4)
head_d   = 16.0;                          // M5 ノブ頭の想定径 (工具レス)
cam_outer = base_line/2 + (case_h - lens_off_bot); // レンズ外側のケース張り出し

// ---- 干渉・成立性チェック -------------------------------------------
assert(gap_t >= tab_t + 0.3,               "フィンガー間隙がタブ厚+0.3を下回る");
assert(fin_len > tab_len + 2,              "フィンガーがタブより短い (頭の逃げ不足)");
assert(bolt_x - head_d/2 > plate_t + 1,    "M5 ノブ頭が背面プレートに当たる");
assert(fin_w/2 - bolt_d/2 >= 2,            "フィンガーの穴縁距離 < 2mm");
assert(fin_w/2 > hex_af/2 + 2,             "ナットトラップの側壁 < 2mm");
assert(plate_hw - fh_y >= m5_d,            "フレーム穴の Y 端距離不足");
assert(plate_hh - fh_z >= m5_d,            "フレーム穴の Z 端距離不足");
assert(post_y1 <= plate_hw,                "レジスタ柱がプレートからはみ出す");
assert(case_d/2 <= plate_hw + 1,           "ケース底面が柱で受けきれない (目安)");
// 250 枠検査 (縦向き搭載時代のもの) は横向き復帰 (C8) により無効。
// 280 枠検査 (横向き, 2026-09-04 改善要件 §1 C5/C8, §3.2):
//   base_line/2 + case_w/2 + bumper_t <= env_half
assert(base_line/2 + case_w/2 + bumper_t <= env_half,
       "横向き搭載でケース+側面バンパが 280 枠を超える");
echo(str("機体でのケース外側張り出し |X| (横向き, バンパ込み) = ",
         base_line/2 + case_w/2 + bumper_t, " (枠 ", env_half, ")"));
echo(str("レジスタ面のグローバル |X| = ", base_line/2 - lens_off_bot,
         " → プレート背面 |X| = ", base_line/2 - lens_off_bot - fin_x1));

// ---- モジュール -----------------------------------------------------
cham = 1.2;   // フィンガー下面縁の 45° 面取り (オーバーハング面積の削減)

// 稜線上のダイヤモンド断面カッター (軸 = X)。稜の両面に c の 45° 面取りを作る
module edge_cham_x(len, c) {
    s = c * sqrt(2);
    rotate([45, 0, 0]) translate([0, -s/2, -s/2]) cube([len, s, s]);
}
// 同、軸 = Y
module edge_cham_y(len, c) {
    s = c * sqrt(2);
    rotate([0, 45, 0]) translate([-s/2, 0, -s/2]) cube([s, len, s]);
}

// 水平穴 (軸 +X) のティアドロップ: 45° 屋根で自己支持にする (サポートレス規約)
module td_hole_x(d, h) {
    r = d/2;
    rotate([0, 90, 0]) linear_extrude(height = h)
        union() {
            circle(r = r, $fn = 32);
            polygon([[-1.414*r, 0], [0, r], [0, -r]]);
        }
}

// ---- 形状 -----------------------------------------------------------
difference() {
    union() {
        // 背面プレート
        translate([0, -plate_hw, -plate_hh])
            cube([plate_t, 2*plate_hw, 2*plate_hh]);
        // 台座 (最下フィンガーを兼ねてベッドまで下ろす)
        translate([fin_x0, -fin_w/2, -plate_hh])
            cube([fin_len, fin_w, ped_top + plate_hh + fin_t]);
        // 中・上フィンガー
        for (i = [1, 2])
            translate([fin_x0, -fin_w/2, fin_zc[i] - fin_t/2])
                cube([fin_len, fin_w, fin_t]);
        // レジスタ柱 ×2 (前面 = ケース底面の突き当て面)
        for (s = [-1, 1])
            translate([fin_x0, s == 1 ? post_y0 : -post_y1, -plate_hh])
                cube([fin_len, post_w, post_top + plate_hh]);
    }
    // フレーム M5 ×4 (ティアドロップ: 横穴の天井を 45° に)
    for (sy = [-1, 1], sz = [-1, 1])
        translate([-fudge, sy*fh_y, sz*fh_z])
            td_hole_x(m5_d, plate_t + 2*fudge);
    // タブ M5 (垂直通し)
    translate([bolt_x, 0, -plate_hh - fudge])
        cylinder(d = bolt_d, h = 2*plate_hh + 2*fudge, $fn = 32);
    // 中・上フィンガー下面の縁を 45° 面取り (±Y の稜と先端 +X の稜)
    for (i = [1, 2]) {
        zb = fin_zc[i] - fin_t/2;
        for (s = [-1, 1])
            translate([fin_x0 - fudge, s*fin_w/2, zb])
                edge_cham_x(fin_len + 2*fudge, cham);
        translate([fin_x1, -fin_w/2 - fudge, zb])
            edge_cham_y(fin_w + 2*fudge, cham);
    }
    // ナットトラップ (底面)。天井は 45° コーンで自己支持にする
    translate([bolt_x, 0, -plate_hh - fudge])
        cylinder(d = hex_af / cos(30), h = hex_dep + fudge, $fn = 6);
    translate([bolt_x, 0, -plate_hh + hex_dep - fudge])
        cylinder(d1 = hex_af / cos(30), d2 = bolt_d,
                 h = (hex_af/cos(30) - bolt_d)/2 + fudge, $fn = 32);
}
