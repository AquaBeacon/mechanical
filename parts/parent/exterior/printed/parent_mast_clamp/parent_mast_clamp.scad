// =====================================================================
// parent_mast_clamp.scad — 親機 マストクランプ (2個以上印刷)
// φ20アルミパイプ(マスト)を掴むスリット式ピンチクランプ+取付フランジ。
// 上側: 防水ボックス底に M5×4 で固定。下側: マストヘッドプレートに固定。
// パイプは貫通穴に通し、M4ピンチボルト2本で締める。
// 印刷向き: フランジを下に平置き。パイプ穴は垂直で真円が出る。
// =====================================================================

/* [パイプ] */
pipe_d    = 20.4;    // アルミパイプ実測OD + 0.4 (要フィットテスト)

/* [フランジ] */
flange_w  = 70;      // フランジ一辺
flange_t  = 6;       // フランジ厚
m5_p      = 56;      // M5 4穴ピッチ(±28) ※ブロック44角+M5頭の外側
m5_d      = 5.3;

/* [クランプブロック] */
block_w   = 44;      // ブロック一辺
block_h   = 50;      // ブロック高さ(フランジ上面から)
slit_w    = 3;       // スリット幅
m4_d      = 4.5;     // ピンチボルト
m4_x      = 16;      // ピンチボルト位置(パイプ中心からスリット側へ)
m4_z      = [15, 36];// ピンチボルト高さ(フランジ上面基準)
nut_w     = 7.8;     // M4ナット二面幅+余裕
nut_t     = 3.6;

$fn = 96;

// ---- チェック ---------------------------------------------------------
assert(m4_x - m4_d/2 > pipe_d/2 + 2.5, "ピンチボルトがパイプ穴と干渉");
assert(m4_x + m4_d/2 < block_w/2 + 8, "ピンチボルトがブロック外");
assert(block_w > pipe_d + 2*6, "ブロック肉厚不足(片側6mm)");
assert(m5_p/2 - 4.25 > block_w/2 + 0.5,
       "M5頭(Ø8.5)がクランプブロック側面と干渉: m5_p を広げる");
assert(flange_w/2 - m5_p/2 - m5_d/2 >= 4, "M5穴の端距離不足");
for (mz=m4_z) assert(mz > flange_t + m4_d/2 + 2 && mz < flange_t + block_h - m4_d/2 - 2,
                     "ピンチボルト高さがブロック外");

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        translate([-flange_w/2, -flange_w/2, 0]) cube([flange_w, flange_w, flange_t]);
        translate([-block_w/2, -block_w/2, flange_t - 0.1])
            cube([block_w, block_w, block_h + 0.1]);
    }
    // パイプ貫通穴
    translate([0, 0, -0.5]) cylinder(d=pipe_d, h=flange_t + block_h + 1);
    // スリット (パイプ穴 → +X面、ブロックのみ)
    translate([0, -slit_w/2, flange_t + 0.5])
        cube([block_w/2 + 1, slit_w, block_h + 1]);
    // ピンチボルト M4 ×2 (Y方向) + ナットトラップ(-Y面から横挿し)
    for (mz=m4_z) {
        translate([m4_x, -block_w/2 - 1, mz])
            rotate([-90, 0, 0]) cylinder(d=m4_d, h=block_w + 2);
        translate([m4_x - nut_w/2, -block_w/2 + 4, mz - nut_w/2])
            cube([nut_w, nut_t,
                  flange_t + block_h - (mz - nut_w/2) + 1]); // 上面まで抜くナット挿入スロット
    }
    // M5 フランジ穴 ×4
    for (sx=[-1,1]) for (sy=[-1,1])
        translate([sx*m5_p/2, sy*m5_p/2, -0.5]) cylinder(d=m5_d, h=flange_t + 1);
}
