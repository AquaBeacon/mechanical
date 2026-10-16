// =====================================================================
// child_guard_ring.scad — 子機 外装 下部ガード (再設計版)
//
// 旧 child_bottom_guard の置き換え (docs/子機外装フレーム再設計_要件.md)。
// 役割: アルミエンドキャップとペネトレータの保護 / 着底脚 / バラスト座 (M6×5) /
//       テザーのストレインリリーフ。コアフレーム下面へ M5 ×4 (垂直、下から)。
//
// 構成: スキッドリング (r65..85, 下端 ring_z0) + 前・横の脚 3 本 (方位角 30/90/150)
//       + 後部ウォール 2 枚 (方位角 190..230 / 310..350) + その上の取付パッド。
// 開放域 (assert 検査):
//   - 中央 r < 55 は全高で素通し (ペネトレータ工具アクセス、キャップ下面)
//   - 後方セクタ (方位角 230..310 = -Y まわり ±40°) はリングより上が素通し
//     (全ケーブルがここから外へ出る)
// ワニ顎ゲートは z ≥ -17 で前方に開くので、本部品の上端は -17.2 (遊び 0.2)。
// 取付パッドのみ z=-17 でコアフレーム下面に接する (パッドは後半分なので
// ゲートの旋回域と重ならない)。
//
// 座標系: 機体グローバル。チューブ軸 = Z、チューブ下端 z=0、+Y = 前。
// 印刷向き: このまま (+Z up、リング下面がベッド)。サポートレス設計。
// 荷重ケース (要件書 §3):
//   L5 着底 (容器系 2.6kg × 3g ≈ 77N → 脚 3 本): 柱 1.1 MPa → PASS
//   L2 輸送 600N 側方 (リング弧 両端固定 L80 相当): 曲げ 7.5 MPa → PASS
// =====================================================================

/* [取合い (実測/確定値)] */
cap_bot    = -13.8;    // アルミキャップ下面
frame_bot  = -17.0;    // コアフレーム/ゲートの下端面

/* [ペネトレータ突出 (仮値 — 要実測!)] */
pene_len   = 20;       // キャップ下面からの突出量 (WetLink 想定の仮値)
ring_z0    = -60;      // リング下端 = 機体最下端 (2026-09-04 改善要件 §3.4: -37→-60。
                        // キャップ下面から 46mm = ペネトレータ 20 + 曲げ半径 25)

/* [リング] */
ring_r0    = 65;
ring_r1    = 85;
ring_h     = 6;

/* [脚 (前・横 ×3)] */
leg_az     = [30, 90, 150];   // +X から。90 = 前
leg_w      = 12;              // 接線方向
leg_r0     = 62;
leg_r1     = 82;

/* [後部ウォール ×2 (リングとは「足」で結合)] */
wall_r0    = 58.35;    // シェルと同径 (見た目と荷重経路をそろえる)
wall_r1    = 64.35;
wall_az    = [[190, 230], [310, 350]];
foot_r1    = 69;       // 足の外径 (リング ID 65 に 4mm 掛けて融合する)

/* [取付タブ ×2 (垂直板 + 水平 M5 ×2/枚、コアフレームの外面ボスへ)] */
tab_az     = [210, 330];
tab_r0     = 70;       // タブ内面 = コアフレーム側ボス外面 (二重定義)
tab_t      = 12;       // タブ厚 (半径方向)。2026-09-04: 8→12。ring_z0 -37→-60 で
                        // タブ下端 (ring_z1) から下側 M5 (z-9) までの片持ち長が
                        // 28→45mm に伸びたため column ではなく beam(cantilever) で
                        // 再検査、t=8 は interlayer 18.6MPa (>12 allow) で FAIL、t=12 で PASS
tab_w      = 34;       // タブ幅 (接線方向)
tab_z1     = 12;       // タブ上端
m5_d       = 5.4;
tabm5_z    = [-9, 4];  // M5 の z (コアフレーム側は z≥-17 に存在する)

/* [ケーブルカバー取付インサート座 ×2 (二重定義 — child_cable_cover と共有)] */
// 後部ウォール ×2 の開口 (230..310) に面する端 (wall1=230, wall2=310) を
// 半径方向に厚肉化し、M5 熱圧入インサート (Ø6.4 × 9、接線方向ボア) を各 1 本埋める。
cover_bolt_az        = [230, 310];  // ウォール端の方位角 (開口側)
cover_bolt_dir       = [1, -1];     // rotate([90*dir,0,0]) の符号。dir=+1→局所-Y (az減少=wall1材内)、
                                     // dir=-1→局所+Y (az増加=wall2材内) にボアする
cover_bolt_r         = 64;          // インサート中心半径
cover_bolt_z         = -26;         // インサート中心 z (2026-09-04: -35→-26。
                                     // child_cable_cover の出口穴 z=-40 と z 方向に分離し、
                                     // 出口穴がフランジ角度域を通っても干渉しないようにする)
cover_bolt_pad_deg   = 11;          // ボス角度幅 (端から材内へ。インサート長9+2 が収まる最小 9.85° に余裕を付けた値)
cover_bolt_r1        = 68;          // ボス外径 (tab_r0=70 に 2mm クリアランス)
cover_bolt_insert_d  = 6.4;         // M5 熱圧入インサート下穴
cover_bolt_insert_len = 9;          // インサート深さ (ボア長)
// ボスは ring_z1..top_z の全高でウォールと同じ高さにする (途中の高さだけ厚肉化すると
// 下面がリングとウォールの間で宙に浮き、printability のオーバーハングが悪化するため)。

/* [バラスト M6 ×5 (後ろ寄り)] */
bal_d      = 6.6;
bal_r      = 75;
bal_az     = [198, 234, 270, 306, 342];
bal_cb_d   = 11.5;     // 頭の座ぐり (下面から)
bal_cb_h   = 4;

/* [テザー結束スロット ×2 (リング後方)] */
tie_az     = [262, 278];
tie_w      = 4;        // 接線方向
tie_r0     = 68;
tie_r1     = 76;

/* [検査] */
env_half   = 125.0;
open_ctr_r = 55;       // 中央素通し半径
open_sec   = [230, 310]; // 後方開放セクタ

/* [Hidden] */
fudge = 0.01;
$fn = 120;

// ---- 導出値 ---------------------------------------------------------
top_z    = -17.2;              // 脚・ウォール上端 (ゲート旋回域 -17 に遊び 0.2)
ring_z1  = ring_z0 + ring_h;
leg_h    = top_z - ring_z1;
cover_bolt_boss_z0 = ring_z1;   // ウォールと同じ下端 (リング上面に接し、宙に浮かない)
cover_bolt_boss_z1 = top_z;     // ウォールと同じ上端

// ---- 干渉・成立性チェック -------------------------------------------
assert(ring_z0 <= cap_bot - pene_len - 3, "ペネトレータがリング下端より下に出る");
assert(ring_r1 <= env_half - 5, "リングが 250 枠 (保護代 5) を超える");
assert(ring_r0 >= open_ctr_r && wall_r0 >= open_ctr_r && leg_r0 >= open_ctr_r,
       "中央素通し r<55 を塞いでいる");
for (a = leg_az)
    assert(a < open_sec[0] && (a > open_sec[1] - 360), "脚が後方開放セクタ内にある");
for (w = wall_az)
    assert(w[1] <= open_sec[0] || w[0] >= open_sec[1], "ウォールが後方開放セクタに掛かる");
assert(foot_r1 >= ring_r0 + 3, "足がリングに 3mm 以上掛かっていない (分離する)");
for (a = tab_az)
    assert(a < open_sec[0] || a > open_sec[1], "タブが後方開放セクタ内にある");
assert(tab_r0 >= wall_r1 + 2, "タブとウォールの半径方向すきま < 2 (別部材)");
assert(tab_r0 + tab_t <= ring_r1 - 2, "タブがリング外縁からはみ出す");
assert(min(tabm5_z) - m5_d/2 >= frame_bot + 3, "下側 M5 がコアフレーム下端に近すぎる");
assert(tab_z1 - max(tabm5_z) >= m5_d/2 + 4, "上側 M5 のタブ上端距離不足");
assert(bal_r - bal_cb_d/2 > ring_r0 + 1 && bal_r + bal_cb_d/2 < ring_r1 - 1,
       "バラスト座ぐりがリング縁に掛かる");

// カバー取付インサート座 (cover_bolt_*) の成立性
assert(len(cover_bolt_az) == 2 && len(cover_bolt_dir) == 2,
       "cover_bolt_az/dir は 2 要素 (ウォール1端/ウォール2端)");
assert(cover_bolt_r - wall_r0 >= 3, "インサート座 内側肉厚 < 3");
assert(cover_bolt_r1 - cover_bolt_r >= 3, "インサート座 外側肉厚 < 3");
assert(cover_bolt_r1 + 2 <= tab_r0, "インサートボスがタブに 2mm 未満で近接");
assert(cover_bolt_z - cover_bolt_insert_d/2 - 3 >= ring_z1
       && cover_bolt_z + cover_bolt_insert_d/2 + 3 <= top_z,
       "インサート穴周囲の z 方向肉厚 < 3 (ボス高さ ring_z1..top_z 内)");
assert(cover_bolt_insert_len + 2 <= cover_bolt_pad_deg * 3.14159265/180 * cover_bolt_r,
       "インサート深さ + 余裕がボスの周方向長さを超える");
// ボルト頭が z<ring_z0(=-60) に出ないことは child_cable_cover 側 (座ぐり z) で検査する。
echo(str("ガード z ", ring_z0, " .. ", top_z, " / リング OD ", 2*ring_r1));
echo(str("cover_bolt (機体座標): az=", cover_bolt_az, " r=", cover_bolt_r,
         " z=", cover_bolt_z, " insert Ø", cover_bolt_insert_d, "x", cover_bolt_insert_len));

// ---- モジュール -----------------------------------------------------
// 方位角セクタ (span <= 90°) の楔。原点まわり、z0..z0+h
module wedge(az0, az1, z0, h) {
    intersection() {
        rotate([0, 0, az0]) translate([0, 0, z0]) cube([200, 200, h]);
        rotate([0, 0, az1 - 90]) translate([0, 0, z0 - fudge])
            cube([200, 200, h + 2*fudge]);
    }
}
// 円筒アニュラスのセクタ
module ring_sector(r0, r1, az0, az1, z0, h) {
    intersection() {
        difference() {
            translate([0, 0, z0]) cylinder(r = r1, h = h);
            translate([0, 0, z0 - fudge]) cylinder(r = r0, h = h + 2*fudge);
        }
        wedge(az0, az1, z0 - fudge, h + 2*fudge);
    }
}

// ---- 形状 -----------------------------------------------------------
difference() {
    union() {
        // スキッドリング
        difference() {
            translate([0, 0, ring_z0]) cylinder(r = ring_r1, h = ring_h);
            translate([0, 0, ring_z0 - fudge]) cylinder(r = ring_r0, h = ring_h + 2*fudge);
        }
        // 脚 ×3
        for (a = leg_az)
            rotate([0, 0, a])
                translate([leg_r0, -leg_w/2, ring_z1 - fudge])
                    cube([leg_r1 - leg_r0, leg_w, leg_h + fudge]);
        // 後部ウォール ×2 + 足 (リング ID へ半径方向に掛けて融合する)
        for (w = wall_az) {
            ring_sector(wall_r0, wall_r1, w[0], w[1], ring_z1 - fudge, leg_h + fudge);
            ring_sector(wall_r0, foot_r1, w[0], w[1], ring_z0, ring_h);
        }
        // 取付タブ ×2 (リング上の垂直板。コアフレーム外面ボスへ水平 M5 ×2)
        for (a = tab_az)
            rotate([0, 0, a])
                translate([tab_r0, -tab_w/2, ring_z1 - fudge])
                    cube([tab_t, tab_w, tab_z1 - ring_z1 + fudge]);
        // カバー取付インサート座ボス ×2 (ウォール端を半径方向に厚肉化)
        // wall1 (190..230) の端=230 は az が減る側 (218..230) に、
        // wall2 (310..350) の端=310 は az が増える側 (310..322) に肉を足す。
        ring_sector(wall_r0, cover_bolt_r1,
            cover_bolt_az[0] - cover_bolt_pad_deg, cover_bolt_az[0],
            cover_bolt_boss_z0, cover_bolt_boss_z1 - cover_bolt_boss_z0);
        ring_sector(wall_r0, cover_bolt_r1,
            cover_bolt_az[1], cover_bolt_az[1] + cover_bolt_pad_deg,
            cover_bolt_boss_z0, cover_bolt_boss_z1 - cover_bolt_boss_z0);
    }

    // タブ M5 ×4 (軸 = 半径方向、水平)
    for (a = tab_az, z = tabm5_z)
        rotate([0, 0, a]) translate([tab_r0 - fudge, 0, z])
            rotate([0, 90, 0]) cylinder(d = m5_d, h = tab_t + 2*fudge, $fn = 32);

    // バラスト M6 ×5 + 下面座ぐり (天井は 45° コーン)
    for (a = bal_az) rotate([0, 0, a]) {
        translate([bal_r, 0, ring_z0 - fudge])
            cylinder(d = bal_d, h = ring_h + 2*fudge, $fn = 32);
        translate([bal_r, 0, ring_z0 - fudge])
            cylinder(d = bal_cb_d, h = bal_cb_h + fudge, $fn = 32);
        translate([bal_r, 0, ring_z0 + bal_cb_h])
            cylinder(d1 = bal_cb_d, d2 = bal_d, h = (bal_cb_d - bal_d)/2, $fn = 32);
    }

    // テザー結束スロット ×2 (リング貫通)
    for (a = tie_az)
        rotate([0, 0, a])
            translate([tie_r0, -tie_w/2, ring_z0 - fudge])
                cube([tie_r1 - tie_r0, tie_w, ring_h + 2*fudge]);

    // カバー取付インサート下穴 ×2 (M5 熱圧入 Ø6.4 × 9、接線方向ボア、端面から材内へブラインド)
    for (i = [0, 1])
        rotate([0, 0, cover_bolt_az[i]])
            translate([cover_bolt_r, 0, cover_bolt_z])
                rotate([90 * cover_bolt_dir[i], 0, 0])
                    cylinder(d = cover_bolt_insert_d, h = cover_bolt_insert_len + fudge, $fn = 32);
}
