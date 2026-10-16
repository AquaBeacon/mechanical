// =====================================================================
// child_bottom_guard.scad — 下部ガード (1個印刷)
//
// 縦置き子機の一番下。役割は 4 つ:
//   1. アルミエンドキャップとペネトレータを着底衝撃から守る
//   2. 容器の重量を 3 点パッドで受ける (シェルのクランプ力に頼らない軸方向ストッパ)
//   3. 陸上で自立させる脚 (スキッドリング Ø190)
//   4. バラスト (鉛) の取付座。取付位置を変えて吊り姿勢をトリムする
//
// ★ ケーブルは全部このガードの中を通る。中央 r<42 と後方 (-Y) 約 80deg の
//   セクタは**絶対に塞がない**。テザーは真下へ、TD04A/ライトは後方へ抜ける。
// ★ ペネトレータの締付け (3.5 / 14 N·m) は、このガードを外した状態で行う。
//   ガードは M5 x4 で child_shell_aft の底フレアに留まるだけ。
//
// 座標系: グローバルと同じ (z=0 = アクリルチューブ下端面)。
// 印刷向き: このまま。スキッドリング底面 (z=-37) が約 6700mm2 のベッド接地面。
//   斜めの脚は垂直から 21.6deg なのでサポート不要。
// =====================================================================

/* [耐圧容器 下端 (STL 実測)] */
cap_z       = -13.8;   // アルミエンドキャップ 下面 z
cap_scr_bcd = 108;     // キャップ取付 M3 の BCD (**要確認**。頭がパッドに当たらないこと)
pen_bcd     = 56;      // ペネトレータ BCD
pen_or      = 39;      // ペネトレータ外形の外端 半径 (BCD/2 + 六角半幅 11)

/* [キャップ支持パッド] */
pad_r0    = 42;
pad_r1    = 50;
pad_w     = 24;              // 接線方向 幅
arm_a     = [60, 180, 300];  // パッド/スポークの方位角 (0 = 真後ろ -Y)
post_z0   = -31;             // 支柱 下端 (スポーク上面)

/* [スキッドリング (脚)] */
// 脚 (leg_t=20) の根元がリングの帯幅に収まるように 20mm 幅にしてある。
// 細くすると脚の下側が宙に浮いて印刷できない (assert 4 参照)
ring_r0   = 79;
ring_r1   = 99;
ring_z0   = -37;
ring_z1   = -25;

/* [スポーク (リング ↔ 支柱)] */
spoke_w   = 30;
spoke_r1  = 88;
spoke_t   = 6;               // ring_z0 から上へ

/* [シェルへの取付 (child_shell_aft の guard_r / guard_a と一致させること)] */
lug_r     = 70;
lug_a     = [40, -40, 68, -68];
lug_z1    = 18;              // = child_shell_aft の shell_z0
lug_t     = 12;
lug_w     = 26;              // 接線方向
lug_rr    = 16;              // 半径方向
m5_d      = 5.4;

/* [脚 (リング ↔ 取付ラグ)] */
leg_w     = 24;              // 接線方向
leg_t     = 20;              // 半径方向
leg_r0    = 89;              // リング側 半径
leg_z0    = -30;             // リングに埋め込む深さ

/* [バラスト (鉛) 取付] */
bal_d     = 6.5;             // M6 通し穴
bal_r     = 89;
bal_a     = [0, 100, -100, 140, -140];

/* [結束 (テザーのストレインリリーフ)] */
tie_w     = 4;
tie_h     = 8;
tie_a     = [10, -10];

$fn = 96;

// ---- 導出 -----------------------------------------------------------
leg_dz   = lug_z1 - leg_z0;                       // 48
leg_dr   = leg_r0 - lug_r;                        // 19
leg_ang  = atan(leg_dr/leg_dz);                   // 21.6deg (垂直から)
leg_len  = sqrt(leg_dr*leg_dr + leg_dz*leg_dz);
// 2つの方位角のなす角 (0..180)。方位角は 300 と -60 のように同じ向きを指しうる
function angdiff(a, b) = abs(((a - b) % 360 + 540) % 360 - 180);
open_a   = min([for (a = concat(arm_a, lug_a)) angdiff(a, 0)]);  // 真後ろに最も近い構造

// ---- 干渉・成立性チェック --------------------------------------------
// 1) キャップ支持パッドが「ペネトレータ」と「キャップの M3 頭」の間に収まること
assert(pad_r0 > pen_or + 2,
       str("支持パッドがペネトレータに掛かる: pad_r0=", pad_r0, " 必要 >", pen_or + 2));
assert(pad_r1 < cap_scr_bcd/2 - 3,
       str("支持パッドがキャップの M3 頭に掛かる: pad_r1=", pad_r1,
           " 必要 <", cap_scr_bcd/2 - 3));
// 2) ケーブルの逃げ: 中央 r<pad_r0 が素通しで、真後ろに開いたセクタがあること
assert(open_a >= 25,
       str("真後ろのケーブル用セクタが狭い: 最寄り構造 ", open_a, "deg"));
for (a = arm_a) assert(angdiff(a, 0) > 25, "スポークが真後ろのケーブル用セクタを塞ぐ");
// 3) 支柱がスポークの上に載ること
assert(pad_r0 >= 42 && pad_r1 <= spoke_r1, "支柱がスポークからはみ出し");
assert(pad_w <= spoke_w, "支柱がスポークより広い");
assert(post_z0 == ring_z0 + spoke_t, "支柱の下端がスポーク上面と合っていない");
// 4) 脚とラグ
assert(leg_ang < 45, str("脚の傾きが 45deg 超でサポートが要る: ", leg_ang));
assert(leg_t >= lug_rr, "脚が細くてラグ下面が宙に浮く");
assert(leg_w >= lug_w - 4, "脚が細くてラグ下面が宙に浮く (接線方向)");
assert(leg_r0 - leg_t/2 >= ring_r0 - 0.01 && leg_r0 + leg_t/2 <= ring_r1 + 0.01,
       str("脚の根元がリングの帯からはみ出して宙に浮く: 脚 r ",
           leg_r0 - leg_t/2, "..", leg_r0 + leg_t/2, " / リング r ", ring_r0, "..", ring_r1));
assert(leg_z0 > ring_z0 + 2 && leg_z0 < ring_z1, "脚の根元がリングの中に入っていない");
// 5) 外形枠と高さ
assert(2*ring_r1 <= 250, str("スキッド径 ", 2*ring_r1, " が 250 超"));
assert(ring_z0 >= -40, "全高が 300 を超える (ring_z0 を上げること)");
assert(lug_z1 - ring_z0 <= 256, "X1-Carbon のベッド高さに入らない");
// 6) バラスト穴・結束スロットが脚/スポークに掛からないこと
for (a = bal_a) {
    for (b = concat(arm_a, lug_a))
        assert(2*bal_r*sin(angdiff(a,b)/2) > (bal_d + max(leg_w, spoke_w))/2 + 3,
               str("バラスト穴 a=", a, " が構造 a=", b, " に掛かる (弦長 ",
                   2*bal_r*sin(angdiff(a,b)/2), ")"));
    assert(bal_r + bal_d/2 < ring_r1 - 2 && bal_r - bal_d/2 > ring_r0 + 2,
           "バラスト穴の端距離不足");
}
for (a = tie_a) assert(angdiff(a, 0) < open_a - 8, "結束スロットが脚に掛かる");
assert(tie_h < ring_z1 - ring_z0 - 3, "結束スロットがリングの高さに入らない");

// ---- 部品 -------------------------------------------------------------
module skid_ring() {
    difference() {
        translate([0,0,ring_z0]) cylinder(r=ring_r1, h=ring_z1-ring_z0);
        translate([0,0,ring_z0-1]) cylinder(r=ring_r0, h=ring_z1-ring_z0+2);
    }
}

module spokes() {                     // リング ↔ 支柱 (ベッドに接する層)
    for (a=arm_a) rotate([0,0,a])
        translate([-spoke_w/2, -spoke_r1, ring_z0])
            cube([spoke_w, spoke_r1-pad_r0, spoke_t]);
}

module posts() {                      // 支柱。上面がキャップ支持パッド
    for (a=arm_a) rotate([0,0,a])
        translate([-pad_w/2, -pad_r1, post_z0])
            cube([pad_w, pad_r1-pad_r0, cap_z-post_z0]);
}

module legs() {                       // リング ↔ 取付ラグ (垂直から 21.6deg)
    for (a=lug_a) rotate([0,0,a])
        translate([0, -leg_r0, leg_z0]) rotate([-leg_ang, 0, 0])
            translate([-leg_w/2, -leg_t/2, 0]) cube([leg_w, leg_t, leg_len+8]);
}

module lugs() {                       // シェル底フレアへの取付座
    for (a=lug_a) rotate([0,0,a])
        translate([-lug_w/2, -lug_r-lug_rr/2, lug_z1-lug_t])
            cube([lug_w, lug_rr, lug_t]);
}

// ---- 切り欠き ---------------------------------------------------------
module cut_top() {                    // ラグ上面 (z=lug_z1) より上を落とす
    translate([-300,-300,lug_z1]) cube([600,600,300]);
}

module cut_bolts() {                  // シェルへの M5 x4
    for (a=lug_a) rotate([0,0,a])
        translate([0, -lug_r, lug_z1-lug_t-2]) cylinder(d=m5_d, h=lug_t+4);
}

module cut_ballast() {                // 鉛の取付穴 (位置を変えて吊り姿勢をトリム)
    for (a=bal_a) rotate([0,0,a])
        translate([0, -bal_r, ring_z0-2]) cylinder(d=bal_d, h=ring_z1-ring_z0+4);
}

module cut_ties() {                   // テザーのストレインリリーフ
    for (a=tie_a) rotate([0,0,a])
        translate([-tie_w/2, -ring_r1-3, (ring_z0+ring_z1)/2 - tie_h/2])
            cube([tie_w, ring_r1-ring_r0+6, tie_h]);
}

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        skid_ring();
        spokes();
        posts();
        legs();
        lugs();
    }
    cut_top();
    cut_bolts();
    cut_ballast();
    cut_ties();
}

echo(str("スキッド Ø", 2*ring_r1, " / 全高 ", lug_z1-ring_z0, " (z ", ring_z0, "..", lug_z1, ")"));
echo(str("脚の傾き ", leg_ang, "deg / 長さ ", leg_len));
echo(str("キャップ支持パッド r ", pad_r0, "..", pad_r1, " x3 (ペネトレータ外端 r", pen_or,
         " / キャップ M3 頭 r", cap_scr_bcd/2, " の間)"));
echo(str("真後ろのケーブル用セクタ ±", open_a, "deg"));
