// ============================================================
// AquaBeacon 振動子ポール治具 (TD04A pole jig)
// VP25塩ビポール(縦)にクランプし、TD04Aを水平に保持する。
// 対面測距試験(E1)で送受それぞれのポールに1個ずつ使用。
// part="body"(本体) と part="cap"(クランプ蓋) を個別にエクスポート。
// 印刷向き: どちらも底面(ポール溝と直交の平面)を下にしてそのまま印刷。
// 寸法は要実測: pole_d(実測VP25外径~32mm), xdcr_d/xdcr_len(TD04A実測)
// ============================================================
include <../../../../scad/lib/util.scad>

$fn = 96;

/* [Part selection] */
part = "body";        // [body, cap]

/* [Pole (vertical)] */
pole_d    = 32.4;     // VP25実測外径 + すべり嵌め余裕(要フィットテスト)
clamp_h   = 40;       // ポールを掴む高さ
clamp_gap = 3;        // 本体とキャップの締め代ギャップ(両側合計)

/* [Transducer cradle (horizontal)] */
xdcr_d    = 26.0;     // TD04A胴径(要実測) + 0.5クリアランス
xdcr_len  = 55;       // クレードル長(振動子胴長以下)
tie_w     = 5.5;      // 結束バンド幅(4.8mm帯用)
tie_t     = 2.5;      // 結束バンド厚み穴
tie_n     = 2;        // 結束バンド本数

/* [Structure] */
wall      = 6;        // 主要肉厚
bolt_d    = 4;        // M4クランプボルト
bolt_head = 8;        // M4ナベ頭径
arm_len   = 18;       // ポール中心→クレードル中心の水平距離(短いほど剛)
chamf     = 0.8;      // 底面チャンファ(エレファントフット対策)

// ---- 導出寸法 ----
pole_r    = pole_d/2;
xd_r      = xdcr_d/2;
body_w    = pole_d + 2*wall + 2*(bolt_d+2*wall);   // ボルト耳込み幅
body_d    = pole_r + arm_len + xd_r + wall;        // ポール中心~クレードル外面
body_h    = clamp_h;
bolt_span = pole_d + wall + bolt_d;                // 左右ボルト間隔
cap_t     = wall;                                   // キャップ厚

module bolt_holes(h) {
    for (sx=[-1,1])
        translate([sx*bolt_span/2, 0, -1])
            hole(bolt_d+CLEAR_FIT, h+2, fn=10);
}

// ---------------- 本体 ----------------
module body() {
    difference() {
        union() {
            // ベースブロック(底チャンファ付き、一筆書きの単一footprint)
            translate([-body_w/2, -pole_r-wall, 0])
                box_rounded(body_w, body_d + pole_r + wall, body_h, r=3, chamfer=chamf);
        }
        // ポール縦溝(半円+締め代: キャップ側へ開放)
        translate([0,0,-1]) hole(pole_d, body_h+2, fn=48);
        // 開放スリット(キャップ側): ポール溝~前面を切り欠いてC字にする
        translate([-pole_d/2, -pole_r-wall-1, -1])
            cube([pole_d, pole_r+1, body_h+2]);
        // クランプボルト穴(縦中央に1段)
        translate([0, 0, body_h/2]) rotate([90,0,0])
            translate([0,0,-(pole_r+wall+1)]) bolt_holes(pole_r+wall+2);
        // 振動子クレードル溝(水平・上開放の半円樋 → サポート不要)
        translate([0, pole_r+arm_len, body_h])
            rotate([0,90,0])
                cylinder(h=xdcr_len+2, d=xdcr_d, center=true);
        // 結束バンドスロット(クレードル溝の下をくぐる)
        for (i=[0:tie_n-1])
            translate([-xdcr_len/2 + (i+0.5)*xdcr_len/tie_n, pole_r+arm_len, body_h - xd_r - tie_t - 1.5])
                rotate([90,0,0])
                    translate([-tie_w/2, 0, -(xd_r+wall)])
                        cube([tie_w, tie_t, 2*(xd_r+wall)]);
    }
}

// ---------------- クランプ蓋 ----------------
module cap() {
    difference() {
        translate([-body_w/2, 0, 0])
            box_rounded(body_w, wall + clamp_gap, clamp_h, r=3, chamfer=chamf);
        // ポール当たり面(浅い半円で食いつき)
        translate([0, wall+clamp_gap+pole_r-2, -1])
            hole(pole_d, clamp_h+2, fn=48);
        // ボルト貫通穴+頭座グリ
        translate([0, 0, clamp_h/2]) rotate([-90,0,0]) {
            translate([0,0,-1]) bolt_holes(wall+clamp_gap+2);
            for (sx=[-1,1])
                translate([sx*bolt_span/2, 0, -0.01])
                    hole(bolt_head+CLEAR_FIT, 3, fn=12);
        }
    }
}

if (part=="body") body();
else cap();
