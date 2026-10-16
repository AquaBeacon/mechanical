// =====================================================================
// child_shell_fwd.scad — 子機 外装 前半シェル (1個印刷)
//
// child_shell_aft と対で耐圧容器を挟む「ゲート」側。M5 蝶ボルト 4 本で外れ、
// 外すと容器を真上に抜ける。カメラ 2 台とライトはこちら側に載る。
//
// ★ 左右のカメラポッドを 1 部品に一体化してある。基線 (レンズ間隔) が
//   組立誤差の影響を受けず、単一部品の寸法として決まるようにするため。
//   base_line = 150.0 mm。ポッド底の位置決めパッドで Z も再現する。
//
//   持つもの: カメラポッド x2 (基線 150 / 前面開放 / フード 8mm)
//             / 底デッキ (= 前方バンパ + ベッド接地面) / ライト鞍座
//             / 縦フィン x8 (ポッド荷重をデッキとスキンへ流す)
//
// 座標系: Z = 上 (チューブ下端面が z=0)、+Y = カメラの向き(前)、X = 基線方向。
//         このシェルは y >= 0 側のみ。
// 印刷向き: このまま (Z が積層方向)。サポート不要。
//   底デッキ(z18..30)がベッド接地面 (約 200cm2) なので反りに強い。
//   幅 237 は X1-Carbon (256) にブリム 3mm 込みで収まる。ベッド中央に置くこと。
// =====================================================================

/* [耐圧容器 (STL 実測)] */
tube_od   = 114.3;
pad_t     = 1.2;            // 保護シート厚 (EVA/ゴム) 片側

/* [シェル共通 — child_shell_aft と同じ値にすること] */
skin_t    = 6;
shell_z0  = 18;
shell_z1  = 190;
rail_x0   = 56;
rail_x1   = 80;
rail_t    = 10;
boss_t    = 14;             // 前側ボルトボス厚み (後側は 24。ねじは M5x35)
bolt_x    = 70;
bolt_z    = [42, 150];
pin_z     = 100;
pin_d     = 6.4;            // aft のピン Ø6 に対する受け穴
flare_r   = 78;
flare_h   = 10;
m5_d      = 5.4;

/* [カメラ: DJI Osmo Action 6 (実寸 72.8 x 47.2 x 33.1)] */
cam_w     = 72.8;           // 横 (ランドスケープ)
cam_h     = 47.2;           // 縦
cam_d     = 33.1;           // 奥行 (レンズ軸方向)
cam_clr   = 0.6;            // クレードル クリアランス (両側合計)
lens_dx   = 0;              // レンズ軸の本体X中心からのずれ (外向き +)。**要実測**
cam_fov_h = 145;            // 水平画角 (155deg 対角からの推定)。**要確認**
cam_fov_v = 105;            // 垂直画角 (同上)
cam_fov_d = 155;            // 対角画角 (DJI 公称)

/* [基線とカメラ位置] */
base_line = 150;            // ★ レンズ間隔。解析で使う値。銘板は .md に記録
lens_y    = 110;            // レンズ面 (カメラ前面) の y。ポッド後壁がスキンに
                            // 食い込まない最小値 + 余裕 (assert 8 参照)
cam_ax_z  = 115;            // レンズ軸の z

/* [カメラポッド] */
pod_wall  = 7;              // 側壁 (M4 タップ代を持たせる)
pod_floor = 6;
pod_rear  = 6;
hood      = 8;              // 側壁/床がレンズ面より前へ出る量 (画角を蹴らない範囲)
pod_top   = 145;            // 側壁上端 = 蓋の座 (カメラ上面 +6.4)
pad_d     = 8;              // 底の位置決めパッド Ø
pad_h     = 0.8;            // 同 高さ (Z の再現性を出す)
tab_t     = 3;              // 前抜け止めタブ 出っ張り
tab_z1    = 102;            // 同 上端 (画角外に収めること)
m4_pilot  = 3.3;            // M4 タッピング下穴
lid_sc_y  = 90;             // 蓋ねじの y

/* [縦フィン (ポッド → デッキ / スキン)] */
fin_t     = 6;
fin_x     = [34.3, 60, 90, 115.2];   // 右ポッド側のフィン中心 x
fin_y0    = 40;             // 後端 (チューブ穴で削られる)

/* [底デッキ = 前方バンパ + ベッド接地面] */
deck_z1   = 30;
deck_y1   = 122;            // 機体の最前端
deck_ch   = 45;             // 前角の 45deg 面取り (流線形)
rim_y0    = 114;            // 前縁リム (バンパ)
rim_z1    = 46;

/* [水中ライト (未選定 / 割りクランプの下半分)] */
light_d   = 40;             // 胴径 **要選定**
light_z   = 58;             // 軸中心 z
light_y0  = 78;             // 鞍座 y 範囲
light_y1  = 118;
light_m4x = 28;             // 上クランプ M4 の x (±)
light_m4y = [86, 110];      // 同 y
light_blk = 35;             // 鞍座ブロック 半幅

/* [通水・結束] */
vent_d    = 10;
vent_a    = [0, 22, -22, 45, -45];   // +Y からの方位角
vent_z    = [45, 78, 111, 144];
tie_w     = 4;
tie_h     = 12;
tie_x     = [-100, -60, 60, 100];    // デッキ上の結束スロット x
tie_y     = 96;

$fn = 96;

// ---- 導出 -----------------------------------------------------------
bore_d   = tube_od + 2*pad_t;
bore_r   = bore_d/2;                 // 58.35
skin_r   = bore_r + skin_t;          // 64.35
pod_cx   = base_line/2 - lens_dx;    // ポッド (カメラ本体) の中心 x
in_hw    = (cam_w + cam_clr)/2;      // クレードル内 半幅
cam_z0   = cam_ax_z - cam_h/2;       // カメラ底面 z
flr_top  = cam_z0 - pad_h;           // ポッド床 上面
in_y0    = lens_y - cam_d - cam_clr; // クレードル内 後端
in_z1    = cam_z0 + cam_h + cam_clr; // クレードル内 上端
pod_x0   = pod_cx - in_hw - pod_wall;
pod_x1   = pod_cx + in_hw + pod_wall;
pod_y1   = lens_y + hood;            // ポッド前端 (フード)
half_w   = pod_x1;                   // 機体 半幅
corner   = sqrt(pow(in_hw,2) + pow((cam_h+cam_clr)/2,2));  // 画角の対角基準

// 障害物 (dx,dy,dz = レンズ基準) が画角に入るか
function in_fov(dx, dy, dz) =
    dy > 0 && abs(dx) < dy*tan(cam_fov_h/2) && abs(dz) < dy*tan(cam_fov_v/2);

// ---- 干渉・成立性チェック --------------------------------------------
// 1) 250 x 250 x 300 の外形枠
assert(2*half_w <= 250, str("全幅 ", 2*half_w, " が 250 超"));
assert(deck_y1 <= 125, str("前端 ", deck_y1, " が 125 超"));
assert(2*half_w + 6 <= 256, str("X1-Carbon のベッド 256 に入らない: ", 2*half_w));
// 2) フードが画角を蹴らないこと (対角が最も厳しい)
assert(hood*tan(cam_fov_d/2) < corner,
       str("フードが対角画角を蹴る: ", hood*tan(cam_fov_d/2), " >= ", corner));
assert(!in_fov(in_hw, hood, 0), "フード側壁が水平画角に入る");
assert(!in_fov(0, hood, (cam_h+cam_clr)/2), "フード床が垂直画角に入る");
// 3) 前抜け止めタブが画角に入らないこと
assert(!in_fov(in_hw - tab_t, pod_y1 - lens_y, cam_ax_z - tab_z1),
       str("前抜け止めタブが画角に入る (tab_z1 を下げる)"));
// 4) ライトが画角に入らないこと (最も内側・最も上・最も前の点で判定)
assert(!in_fov(base_line/2 - light_d/2, light_y1 - lens_y, cam_ax_z - (light_z + light_d/2)),
       str("ライトが画角に入る: 上端 z=", light_z + light_d/2, " 前端 y=", light_y1));
// 5) 前縁リム(バンパ)が画角に入らないこと
assert(!in_fov(base_line/2, deck_y1 - lens_y, cam_ax_z - rim_z1),
       str("前縁リムが画角に入る: rim_z1=", rim_z1, " を下げること"));
// 6) デッキ本体が画角に入らないこと
assert(!in_fov(base_line/2, deck_y1 - lens_y, cam_ax_z - deck_z1), "底デッキが画角に入る");
// 7) 締結まわり
assert(bolt_x - m5_d/2 > bore_r + 2, "締結M5がチューブ穴と干渉");
assert(bolt_x + m5_d/2 < rail_x1 - 4, "締結M5の端距離不足");
assert(pin_z + pin_d/2 < bolt_z[1] - 16 && pin_z - pin_d/2 > bolt_z[0] + 16,
       "位置決めピン穴がボルトボスと干渉");
// 8) ポッドとチューブ穴が干渉しないこと (ポッド後壁がチューブより前)
assert(in_y0 - pod_rear > skin_r + 2,
       str("ポッド後壁がスキンに食い込む: ", in_y0 - pod_rear, " <= ", skin_r + 2));
// 9) 左右ポッドが中央で衝突しないこと / ライト鞍座と干渉しないこと
assert(pod_x0 > 4, str("左右ポッドが中央で衝突: pod_x0=", pod_x0));
assert(light_blk < pod_x0 - 2 || light_z + light_d/2 + 2 < flr_top,
       "ライト鞍座がカメラポッドと干渉");
assert(light_m4x + 5 <= light_blk, "ライトクランプ M4 が鞍座ブロックからはみ出し");
assert(light_y0 >= light_m4y[0] - 8 && light_y1 >= light_m4y[1] + 8,
       "ライトクランプ M4 の端距離不足");
// 10) フィンがポッド床を支えられるピッチであること (ブリッジ 40mm 以下)
for (i = [0 : len(fin_x)-2])
    assert(fin_x[i+1] - fin_x[i] - fin_t <= 40,
           str("フィン間隔が広すぎてポッド床がブリッジできない: ",
               fin_x[i+1] - fin_x[i] - fin_t, "mm"));
assert(fin_x[0] - fin_t/2 >= pod_x0 - 0.01 && fin_x[len(fin_x)-1] + fin_t/2 <= pod_x1 + 0.01,
       "フィンがポッドの外にはみ出し");
// 11) 通水穴がフィン/レール/鞍座に掛からないこと
for (a = vent_a) {
    vx = abs(skin_r*sin(a));
    for (fx = fin_x)
        assert(abs(vx - fx) > (vent_d + fin_t)/2 + 1,
               str("通水穴 a=", a, " がフィン x=", fx, " に掛かる"));
    assert(vx + vent_d/2 < rail_x0 || skin_r*cos(a) - vent_d/2 > rail_t + 2,
           str("通水穴 a=", a, " が合わせ面レールに掛かる"));
}
assert(skin_r + 8 < light_y0 - 2, "通水穴の抜き代がライト鞍座に当たる");
// 12) 蓋まわり
assert(lid_sc_y > in_y0 + 6 && lid_sc_y < pod_y1 - 6, "蓋ねじの y が側壁の範囲外");
assert(pod_wall/2 - m4_pilot/2 >= 1.5,
       str("蓋ねじ下穴まわりの側壁残肉不足: ", pod_wall/2 - m4_pilot/2, "mm"));
assert(pod_top >= in_z1 + 4, str("ポッド側壁上端がカメラ上面に近すぎる: ", pod_top - in_z1));
assert(pod_top - 12 > flr_top, "蓋ねじの下穴がポッド床まで届いてしまう");
// 13) 抜け止めタブがカメラの挿入 (上から落とし込み) を邪魔しないこと
assert(tab_z1 > flr_top + 6, "抜け止めタブが低すぎて効かない");
assert(tab_t < in_hw - 20, "抜け止めタブが出過ぎてレンズ前を塞ぐ");

// ---- 共通モジュール ---------------------------------------------------
// 軸 = +Y (0..h)、稜が +Z を向くティアドロップ穴 (cube + cylinder のみ)。
module teardrop_py(d, h) {
    r = d/2;
    rotate([-90,0,0]) union() {
        cylinder(d=d, h=h);
        rotate([0,0,225]) cube([r, r, h]);
    }
}

// ---- 部品 -------------------------------------------------------------
module skin() {                       // 半円筒スキン + 底フレア
    intersection() {
        union() {
            translate([0,0,shell_z0]) cylinder(r=skin_r, h=shell_z1-shell_z0);
            translate([0,0,shell_z0]) cylinder(r1=flare_r, r2=skin_r, h=flare_h);
        }
        translate([-200,0,shell_z0]) cube([400,200,400]);      // y>=0 のみ
    }
}

module rail_pair() {                  // 合わせ面レール + ボルトボス
    for (s=[-1,1]) mirror([s<0?1:0,0,0]) {
        translate([rail_x0, 0, shell_z0])
            cube([rail_x1-rail_x0, rail_t, shell_z1-shell_z0]);
        for (bz=bolt_z)
            translate([rail_x0, 0, bz-16]) cube([rail_x1-rail_x0, boss_t, 32]);
    }
}

module deck() {                       // 底デッキ (前方バンパ + ベッド接地面)
    difference() {
        union() {
            translate([-half_w, 0, shell_z0]) cube([2*half_w, deck_y1, deck_z1-shell_z0]);
            translate([-half_w, rim_y0, shell_z0])            // 前縁リム
                cube([2*half_w, deck_y1-rim_y0, rim_z1-shell_z0]);
        }
        // 前角を 45deg に落として流線形にする (丸めは Fusion で付ける)
        for (s=[-1,1]) mirror([s<0?1:0,0,0])
            translate([half_w, deck_y1, shell_z0-2]) rotate([0,0,45])
                translate([0,-100,0]) cube([100, 200, rim_z1-shell_z0+4]);
    }
}

module fins() {                       // 縦フィン (ポッド荷重をデッキ/スキンへ)
    for (s=[-1,1]) mirror([s<0?1:0,0,0]) for (fx=fin_x)
        translate([fx-fin_t/2, fin_y0, deck_z1-2])
            cube([fin_t, pod_y1-fin_y0, flr_top-deck_z1+2]);
}

module pods() {                       // カメラポッド (前面開放・上面開放)
    for (s=[-1,1]) mirror([s<0?1:0,0,0]) {
        translate([pod_x0, in_y0-pod_rear, flr_top-pod_floor])
            cube([pod_x1-pod_x0, pod_y1-(in_y0-pod_rear), pod_top-(flr_top-pod_floor)]);
        // 底の位置決めパッド x3 (カメラの Z 基準)
        for (p = [[pod_cx-25, in_y0+8], [pod_cx+25, in_y0+8], [pod_cx, lens_y-8]])
            translate([p[0], p[1], flr_top]) cylinder(d=pad_d, h=pad_h);
        // 前抜け止めタブ (上から落とし込めて、前へは抜けない)
        for (sx=[-1,1])
            translate([pod_cx + sx*in_hw - (sx>0 ? tab_t : 0), lens_y, flr_top])
                cube([tab_t, hood, tab_z1-flr_top]);
    }
}

module light_saddle() {               // ライト割りクランプの下半分
    translate([-light_blk, light_y0, shell_z0])
        cube([2*light_blk, light_y1-light_y0, light_z-shell_z0]);
}

// ---- 切り欠き ---------------------------------------------------------
module cut_bore() {
    translate([0,0,shell_z0-6]) cylinder(d=bore_d, h=shell_z1-shell_z0+12);
}

module cut_aft_half() {               // 合わせ面 (y=0) より後ろを落とす
    translate([-300,-300,-50]) cube([600,300,500]);
}

module cut_bolts() {                  // 締結 M5 通し (蝶ボルト頭は前側)
    for (s=[-1,1]) mirror([s<0?1:0,0,0]) for (bz=bolt_z)
        translate([bolt_x, -3, bz]) teardrop_py(m5_d, boss_t+8);
}

module cut_pins() {                   // aft のピン受け
    for (s=[-1,1]) mirror([s<0?1:0,0,0])
        translate([bolt_x, -1, pin_z]) teardrop_py(pin_d, 9);
}

module cut_pod_inside() {             // クレードル内腔 + 上面開放 + 水抜き
    for (s=[-1,1]) mirror([s<0?1:0,0,0]) {
        // レンズ面まで: クレードル幅いっぱい (上面開放)
        translate([pod_cx-in_hw, in_y0, flr_top])
            cube([2*in_hw, lens_y-in_y0, pod_top-flr_top+2]);
        // レンズ面より前: 抜け止めタブを残して開放 (フード側壁は残す)
        translate([pod_cx-in_hw+tab_t, lens_y-0.01, flr_top])
            cube([2*(in_hw-tab_t), pod_y1-lens_y+4, pod_top-flr_top+2]);
        // タブより上も開放 (画角を蹴らないため)
        translate([pod_cx-in_hw, lens_y-0.01, tab_z1])
            cube([2*in_hw, pod_y1-lens_y+4, pod_top-tab_z1+2]);
        for (dx=[-22,22])                                      // 床の水抜き
            translate([pod_cx+dx, in_y0+14, flr_top-pod_floor-2])
                cylinder(d=6, h=pod_floor+4);
        for (dx=[-24,0,24])                                    // 後壁の通水・軽量化
            translate([pod_cx+dx, in_y0-pod_rear-2, cam_ax_z]) teardrop_py(14, pod_rear+4);
    }
}

module cut_lid_screws() {             // 蓋 M4 タッピング下穴 (側壁の上面)
    for (s=[-1,1]) mirror([s<0?1:0,0,0]) for (sx=[-1,1])
        translate([pod_cx + sx*(in_hw + pod_wall/2), lid_sc_y, pod_top-12])
            cylinder(d=m4_pilot, h=13);
}

module cut_light() {                  // ライト胴の鞍 + 上クランプ M4 下穴
    translate([0, light_y0-2, light_z]) rotate([-90,0,0])
        cylinder(d=light_d, h=light_y1-light_y0+4);
    translate([-light_d/2, light_y0-2, light_z])               // 上半分を開放
        cube([light_d, light_y1-light_y0+4, light_d]);
    for (sx=[-1,1]) for (ly=light_m4y)
        translate([sx*light_m4x, ly, light_z-14]) cylinder(d=m4_pilot, h=15);
}

module cut_vents() {
    for (a=vent_a) for (z=vent_z)
        rotate([0,0,a]) translate([0, bore_r-6, z]) teardrop_py(vent_d, 20);
}

module cut_ties() {                   // デッキ上の結束スロット (ライト配線用)
    for (tx=tie_x) for (s=[-1,1])
        translate([tx - tie_h/2, tie_y + s*7 - tie_w/2, shell_z0-2])
            cube([tie_h, tie_w, deck_z1-shell_z0+4]);
}

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        skin();
        rail_pair();
        deck();
        fins();
        pods();
        light_saddle();
    }
    cut_bore();
    cut_aft_half();
    cut_bolts();
    cut_pins();
    cut_pod_inside();
    cut_lid_screws();
    cut_light();
    cut_vents();
    cut_ties();
}

echo(str("★ 基線 base_line = ", base_line, " mm (レンズ間隔)"));
echo(str("レンズ位置 = (±", base_line/2, ", ", lens_y, ", ", cam_ax_z, ")"));
echo(str("外形 W=", 2*half_w, "  y=0..", deck_y1, "  z=", shell_z0, "..", shell_z1));
echo(str("フード ", hood, "mm / 対角画角の余裕 ", corner - hood*tan(cam_fov_d/2), "mm"));
echo(str("ポッド内寸 ", 2*in_hw, " x ", lens_y-in_y0, " x ", in_z1-flr_top));
