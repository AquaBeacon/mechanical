// =====================================================================
// parent_plate.scad — 親機 防水ボックス内 マウントプレート (183×203 t5)
//
// 容器: タカチ BCAS212310G (BMP2123Z 互換プレート面 183×203、ボス上 z~10)。
// 配置は spec/parent_interior_layout.py の検証済みレイアウト
// (spec/_work/images/parent_layout_p1.png / _p2.png) に一致する。
//
// 基板の取付穴は .kicad_pcb の実座標から変換式で導出 (CLAUDE.md 規約):
//   PARENT_MAIN : Edge(0,0)-(112,88), 穴 (4.5,4.5)(107.5,4.5)(4.5,80)(107.5,80)
//   PARENT_PWR  : Edge(0,0)-(100,84), 穴 (5,5)(95,5)(5,79)(95,79)
//   TX_improved : Edge(-4,0)-(70,50), 穴 (0,4)(66,4)(0,46)(66,46)
// MAIN は kicad+Y を プレート -Y に向けて置く (ボタン/LED/DS3231 縁が北、
// microSD 縁が南)。PWR/TX は穴が対称なので向きはボスに影響しない。
//
// 固定: 北側2箇所 M4 皿ねじ (箱コーナー M4 インサートへ、蓋を開けて上から
// アクセス可)。南側は位置決めピン2本 (箱の M4 タッピングボス下穴 Ø3.4 へ挿す。
// 位置は タカチ図面 DXF の実座標: 箱 (65,25)/(105,25) → プレート (51.5,11.5)/(91.5,11.5))。
// 南東/南西コーナーインサートは使わない (基板下で工具が届かないため)。
// 高さ: プレート下面 z = 床3.8 + 箱ボス10 (仮) = 13.8 (箱底外面基準)。
// LiPo: P-MAIN 上のブリッジトレイ parent_lipo_tray (MAIN 穴に M3 MF25 スペーサ)。
//   最上段に置いて交換しやすくする (2026-08-28 人間指示)。
//
// パターン: pattern=1 カメラ外付け(Osmo) / pattern=2 PiZero+GSカメラ内蔵
//   p2 は底面ビューポート穴 Ø36 + カメラマウント下穴 + PiZero ボスを追加し、
//   TX ボスが (121,77)→(117,127) に移る (TX は PiZero 上に z+30 高架)。
//
// 印刷向き: 平置き (+Z 上)。サポート不要。PETG / インフィル 30-40%。
// =====================================================================

/* [パターン] */
pattern   = 1;      // 1=Osmo外付け / 2=PiZero+GSカメラ内蔵

/* [プレート] */
px        = 183;    // BMP2123Z 互換
py        = 203;
pt        = 5;
corner_cut= 8;      // 箱コーナー柱の逃げ 45°カット (要実測: BMP2123Z 実物照合)

/* [箱固定 (タカチ BCAS212310G)] */
m4_pitch_x = 160;   // コーナー M4 インサートピッチ (BMP2123Z カタログ a=160)
m4_pitch_y = 180;   //                              (BMP2123Z カタログ b=180)
m4_d      = 4.5;    // M4 皿ねじ通し穴
csk_d     = 9.0;    // 皿座グリ径 (M4 皿頭 Ø8 + 余裕)
pin_d     = 3.2;    // 南側位置決めピン径 (箱タッピングボス下穴 Ø3.4, 図面値)
pin_h     = 6;      // ピン突出 (プレート下面から)
// 箱の M4 タッピングボス (bcas212310g.scad tap_pos, 図面 DXF 実座標) → プレート座標
box_tap_south = [[65, 25], [105, 25]];          // 箱座標 (中央 145 は SPR ボスに近いので使わない)
plate_in_box  = [13.5, 13.5];                   // プレート左下の箱座標
pin_pos   = [for (b = box_tap_south) [b[0] - plate_in_box[0], b[1] - plate_in_box[1]]];  // (51.5,11.5)/(91.5,11.5)

/* [基板配置 (プレート左下原点, spec/parent_interior_layout.py と一致)] */
main_pos  = [2, 2];      // P-MAIN 112×88 (kicad+Y を南向きに反転)
pwr_pos   = [2, 95];     // P-PWR 100×84
spr_pos   = [121, 2];    // SPRESENSE 拡張 68.6×53.5 を 90° 回転 (53.5×68.6)
tx_pos_p1 = [121, 77];   // TX_improved 90°回転 (50×74) プレート直付け
tx_pos_p2 = [117, 127];  // p2: PiZero 上に z+30 高架 (穴は同ピッチ)
pizero_pos= [127, 135];  // p2: Pi Zero 2W 90°回転 (30×65)

/* [ボス] */
boss_d    = 7;      // M3 ボス外径
boss_h    = 6;      // ボス高さ = 基板スタンドオフ
pwr_boss_h = boss_h; // PWR裏面リードの逃げ。変更時は基板の配置Zも同量移動する。
m3_pilot  = 2.6;    // M3 セルフタップ下穴
pz_boss_d = 6;      // Pi Zero M2.5 ボス
pz_pilot  = 2.0;    // M2.5 セルフタップ下穴

/* [SPRESENSE 拡張ボード穴 (要確認: Sony 図面/実測で確定)] */
spr_inset = 3.5;    // 仮値。拡張ボード CXD5602PWBEXT1 の四隅 inset

/* [パターン2: カメラ] */
vp_off    = 54;     // ビューポート中心の箱中心からの +X オフセット (成立域 52..55。54 = cam_mount 脚と TX ボスの離隔)
vp_hole   = 36;     // プレート開口 (ビューポート Ø30 + 余裕)
cam_hole_sq = 44;   // parent_cam_mount の足穴 正方ピッチ (= foot_sq、二重定義。カメラ穴 34 とは別)
cam_pilot = 2.6;
cam_leg_d = 7.5;    // parent_cam_mount の脚径 (= leg_d)。プレート上の突起として干渉検査に入れる

/* [LCD ブラケット下穴 (北縁ストリップ, ブラケット未設計・仮値)] */
lcd_pos   = [[72, 192], [110, 192]];   // 箱タッピングボス (51.5/91.5/131.5, 191.5) の直上を避ける (図面 DXF)
lcd_pilot = 2.6;

/* [結束バンドスロット 3×10] */
slot_w    = 3;
slot_l    = 10;
slots     = [[116.5, 45], [116.5, 110], [176, 40], [176, 100], [176, 160]];

$fn = 48;

// ---- 導出値 (kicad 実座標 → プレート座標) ------------------------------
// MAIN: plate = [main_pos.x + kx, main_pos.y + (88 - ky)]
main_k  = [[4.5, 4.5], [107.5, 4.5], [4.5, 80], [107.5, 80]];
main_h  = [for (k = main_k) [main_pos[0] + k[0], main_pos[1] + 88 - k[1]]];
// PWR: 穴対称 → plate = [pwr_pos.x + kx, pwr_pos.y + ky]
pwr_k   = [[5, 5], [95, 5], [5, 79], [95, 79]];
pwr_h   = [for (k = pwr_k) [pwr_pos[0] + k[0], pwr_pos[1] + k[1]]];
// TX (90°回転): plate = [tx_pos.x + ky, tx_pos.y + (kx + 4)]
tx_pos  = pattern == 1 ? tx_pos_p1 : tx_pos_p2;
tx_k    = [[0, 4], [66, 4], [0, 46], [66, 46]];
tx_h    = [for (k = tx_k) [tx_pos[0] + k[1], tx_pos[1] + k[0] + 4]];
// SPRESENSE (90°回転, 板 53.5×68.6): inset 仮値
spr_h   = [for (u = [spr_inset, 53.5 - spr_inset], v = [spr_inset, 68.6 - spr_inset])
           [spr_pos[0] + u, spr_pos[1] + v]];
// Pi Zero (90°回転, 板 30×65, 穴ピッチ 23×58 inset3.5)
pz_h    = [for (u = [3.5, 26.5], v = [3.5, 61.5])
           [pizero_pos[0] + u, pizero_pos[1] + v]];
// 箱固定
m4_h    = [[px/2 - m4_pitch_x/2, py/2 + m4_pitch_y/2],
           [px/2 + m4_pitch_x/2, py/2 + m4_pitch_y/2]];   // 北側2箇所のみねじ
// ビューポート (箱中心 = プレート中心)
vp_c    = [px/2 + vp_off, py/2];
cam_h   = [for (u = [-1, 1], v = [-1, 1])
           [vp_c[0] + u*cam_hole_sq/2, vp_c[1] + v*cam_hole_sq/2]];

// ---- フィーチャ表 (x, y, 実効半径, 種別 0=切欠き/1=突起, 名前) ----------
slot_r  = sqrt(pow(slot_w/2, 2) + pow(slot_l/2, 2));
feats = concat(
    [for (i = [0:1]) [m4_h[i][0], m4_h[i][1], csk_d/2, 0, str("M4csk", i)]],
    [for (i = [0:len(pin_pos)-1]) [pin_pos[i][0], pin_pos[i][1], pin_d/2 + 1, 1, str("pin", i)]],
    [for (i = [0:3]) [main_h[i][0], main_h[i][1], boss_d/2, 1, str("main", i)]],
    [for (i = [0:3]) [pwr_h[i][0], pwr_h[i][1], boss_d/2, 1, str("pwr", i)]],
    [for (i = [0:3]) [tx_h[i][0], tx_h[i][1], boss_d/2, 1, str("tx", i)]],
    [for (i = [0:3]) [spr_h[i][0], spr_h[i][1], boss_d/2, 1, str("spr", i)]],
    [for (i = [0:len(lcd_pos)-1]) [lcd_pos[i][0], lcd_pos[i][1], lcd_pilot/2, 0, str("lcd", i)]],
    [for (i = [0:len(slots)-1]) [slots[i][0], slots[i][1], slot_r, 0, str("slot", i)]],
    pattern == 2 ? concat(
        [[vp_c[0], vp_c[1], vp_hole/2, 0, "viewport"]],
        [for (i = [0:3]) [cam_h[i][0], cam_h[i][1], cam_leg_d/2, 1, str("cam", i)]],   // 脚 Ø7.5 が載る (突起扱い)
        [for (i = [0:3]) [pz_h[i][0], pz_h[i][1], pz_boss_d/2, 1, str("pz", i)]]
    ) : []
);

// ---- 干渉チェック (総当り) ---------------------------------------------
min_web = 2.0;    // 切欠きが絡むペアの最小ウェブ
min_gap = 0.5;    // 突起同士の最小隙間
for (i = [0:len(feats)-2]) for (j = [i+1:len(feats)-1]) {
    a = feats[i]; b = feats[j];
    d = sqrt(pow(a[0]-b[0], 2) + pow(a[1]-b[1], 2));
    need = a[2] + b[2] + ((a[3] == 0 || b[3] == 0) ? min_web : min_gap);
    assert(d >= need, str("干渉: ", a[4], " - ", b[4], " d=", d, " 要 ", need));
}
// プレート内 (縁マージン 1.5) + コーナーカットから離れていること
for (f = feats) {
    assert(f[0] - f[2] >= 1.5 && f[0] + f[2] <= px - 1.5 &&
           f[1] - f[2] >= 1.5 && f[1] + f[2] <= py - 1.5, str("縁に接近: ", f[4]));
    for (c = [[0,0],[px,0],[0,py],[px,py]]) {
        m = abs(f[0]-c[0]) + abs(f[1]-c[1]);   // L1 距離 vs 45°カット
        assert((m - corner_cut)/sqrt(2) >= f[2] + min_web,
               str("コーナーカットに接近: ", f[4]));
    }
}
// ビューポートの成立条件 (マストフランジ 70 角 / 浮子開口 Ø140)
if (pattern == 2) {
    assert(vp_off >= 35 + 15 + 2, "VP がマストフランジと干渉");
    assert(vp_off + 15 <= 70, "VP が浮子開口 Ø140 の外");
}

// 箱のタッピングボス (10 個, 図面) のうちプレート下に来るものは、プレートのボス/穴と
// 重ならないこと (ピンを挿す 2 個以外はプレートが上に載るだけ)
box_taps = concat([for (sx=[-1,1], sy=[-1,1]) [105+sx*80, 115+sy*40]],
                  [for (sx=[-1,0,1], sy=[-1,1]) [105+sx*40, 115+sy*90]]);
for (b = box_taps) {
    bp = [b[0] - plate_in_box[0], b[1] - plate_in_box[1]];
    inside = bp[0] > 0 && bp[0] < px && bp[1] > 0 && bp[1] < py;
    if (inside) for (f = feats) if (f[3] == 0 || f[4][0] == "p" && f[4][1] == "i")
        assert(sqrt(pow(f[0]-bp[0],2) + pow(f[1]-bp[1],2)) >= f[2] + 4 + 0.5 ||
               (f[4][0] == "p" && f[4][1] == "i" && sqrt(pow(f[0]-bp[0],2) + pow(f[1]-bp[1],2)) < 0.01),
               str("箱タッピングボス ", bp, " がプレート切欠き ", f[4], " に掛かる"));
}
echo(str("parent_plate: 下面 z = 13.8 (箱底外面基準)  pin_pos = ", pin_pos));

// ---- HOLETABLE (機械可読, 検証スクリプト突合せ用) ----------------------
for (f = feats)
    echo(str("HOLETABLE,", f[4], ",", f[0], ",", f[1], ",",
             f[3] == 0 ? f[2]*2 : (f[4][0]=="p" && f[4][1]=="z" ? pz_pilot :
                                   f[4][0]=="p" && f[4][1]=="i" ? pin_d : m3_pilot)));

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // プレート (コーナー 45° カット)
        difference() {
            cube([px, py, pt]);
            // 45° コーナーカット: 回転正方形 (半対角 = corner_cut) を各角に置く
            cs = corner_cut * sqrt(2);
            for (c = [[0,0], [px,0], [px,py], [0,py]])
                translate([c[0], c[1], -0.5]) rotate([0, 0, 45])
                    translate([-cs/2, -cs/2, 0]) cube([cs, cs, pt+1]);
        }
        // M3 ボス (MAIN/PWR/TX/SPR)
        for (h = concat(main_h, tx_h, spr_h))
            translate([h[0], h[1], pt]) cylinder(d=boss_d, h=boss_h);
        for (h = pwr_h)
            translate([h[0], h[1], pt]) cylinder(d=boss_d, h=pwr_boss_h);
        // Pi Zero ボス (p2)
        if (pattern == 2)
            for (h = pz_h) translate([h[0], h[1], pt]) cylinder(d=pz_boss_d, h=boss_h);
        // 南側位置決めピン (下向き)
        for (p = pin_pos)
            translate([p[0], p[1], -pin_h]) cylinder(d=pin_d, h=pin_h + 1);
    }
    // 北側 M4 皿穴
    for (h = m4_h) {
        translate([h[0], h[1], -0.5]) cylinder(d=m4_d, h=pt+1);
        translate([h[0], h[1], pt - 2.55]) cylinder(d1=m4_d, d2=csk_d, h=2.6);
    }
    // M3 下穴 (ボス貫通 — 水抜きを兼ねる)
    for (h = concat(main_h, tx_h, spr_h))
        translate([h[0], h[1], -0.5]) cylinder(d=m3_pilot, h=pt + boss_h + 1);
    for (h = pwr_h)
        translate([h[0], h[1], -0.5]) cylinder(d=m3_pilot, h=pt + pwr_boss_h + 1);
    // Pi Zero 下穴 (p2)
    if (pattern == 2)
        for (h = pz_h)
            translate([h[0], h[1], -0.5]) cylinder(d=pz_pilot, h=pt + boss_h + 1);
    // LCD ブラケット下穴
    for (p = lcd_pos)
        translate([p[0], p[1], -0.5]) cylinder(d=lcd_pilot, h=pt+1);
    // 結束バンドスロット
    for (s = slots)
        translate([s[0] - slot_w/2, s[1] - slot_l/2, -0.5]) cube([slot_w, slot_l, pt+1]);
    // パターン2: ビューポート開口 + カメラマウント下穴
    if (pattern == 2) {
        translate([vp_c[0], vp_c[1], -0.5]) cylinder(d=vp_hole, h=pt+1);
        for (h = cam_h)
            translate([h[0], h[1], -0.5]) cylinder(d=cam_pilot, h=pt+1);
    }
}
