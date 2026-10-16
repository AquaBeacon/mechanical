// =====================================================================
// child_jaw_gate.scad — 子機 外装 ワニ顎ゲート (前半分の顎)
//
// 外装フレーム再設計 (docs/子機外装フレーム再設計_要件.md R5/R6) +
// 改善要件 (docs/子機外装_改善要件.md §3.1/3.2/3.6, 2026-09-04)。
// 耐圧容器 (WTE4 4″×200) を「ワニの顎」のように前後 2 つの半殻で咥える。
// 本部品は可動側 (前)。コアフレーム (後・未設計) と次で結合する:
//   - ヒンジ: -X 縁、縦 M5 ピン (Ø5 ステンレス棒 or 長ボルト、全長 ~235)
//     ゲート側ナックル 3 個 / コアフレーム側 2 個 (互い違い、遊び 0.4)
//   - ラッチ: +X 縁、M5 ノブボルト ×2 (軸 = Y、コアフレーム側ナットトラップへ。
//     頭 Ø16 はゲート側ボスの Ø18 ポケットに沈める。§3.6)
//
// 2026-09-04 改訂:
//   - カメラブレード + 上下ガセットデッキを削除。カメラは新部品
//     `child_cam_bridge` が HP4/HP5 にボルト留めして保持する (§3.2)
//   - ライトパッド (M4×4 鞍座予約) を削除。前面ハードポイント HP4/HP5/HP-L
//     (§3.1 HP40 規格、scad/lib/hardpoint.scad) に置き換え
//   - ラッチボスに Ø18×深さ12 のノブボルト頭ポケット ×2 を追加 (§3.6)
//
// 軸方向の固定 (R5): 摩擦に頼らず、
//   - 下: アルミエンドキャップの露出リム (Ø120.3, z -13.8..-8) をポケットで捕まえる
//   - 上: ドーム押えリング (Ø120.3 仮, z 208.. ) をポケットで捕まえる
// 半径方向: チューブに EVA 2mm を巻き、ラッチ締結で 0.8mm 圧縮して面で把持する
// (アクリルに局所荷重を掛けない)。
//
// 座標系: 機体グローバルと同じ。チューブ軸 = Z 軸 (x=y=0)、
//   チューブ下端面 z=0、+Y = 前 (カメラの向き)。本部品は y >= 0 側。
// 印刷向き: このまま (+Z up、全高 235 < 250)。フープ応力が層面内に乗る。
//   ナックル中・上段の下面 (互い違いの隙間) のみ小サポート推奨。
// 荷重ケース (要件書 §3): L2 輸送 300 N 任意方向 (改善要件 C6) → ヒンジ/ラッチ各 ~150 N、
//   L3 把持プリロード (EVA 0.8mm 圧縮)。
//   quick_strength tube_clamp (t6×w36, F300): フープ 0.69 MPa → PASS (300N でも余裕)
//   quick_strength lug (Ø5.4, t20, F300): 面圧 2.8 MPa → PASS (層間許容でも)
// =====================================================================

use <../../../../../scad/lib/hardpoint.scad>

/* [耐圧容器 (STL 実測)] */
tube_od    = 114.3;
cap_od     = 120.3;    // アルミエンドキャップ露出リム
cap_z0     = -13.8;    // リム下面
cap_z1     = -8.0;     // リム上面 (下フランジ下面)
tube_top   = 200;      // チューブ上端
flange_top = 208;      // 上フランジ上面 = ドーム座面

/* [ドームキャップ (未購入・仮値 — 要実測)] */
dome_ring_od = 120.3;  // ドーム押えリング外径 (仮 = キャップと同じ)
dome_ring_t  = 6.5;    // リム厚 (仮)

/* [把持 (EVA 面圧)] */
eva_t      = 2.0;      // EVA シート厚 (チューブに巻く)
eva_comp   = 0.8;      // ラッチ締結での圧縮量 = プリロード
pocket_clr = 0.5;      // ポケットの z 方向片側クリアランス
pocket_rad = 0.75;     // ポケットの半径方向クリアランス

/* [シェル] */
shell_t    = 6.0;
lip_b      = 2.7;      // 下リップ厚 (キャップリムの下に回る)
lip_t      = 3.0;      // 上リップ厚

/* [ヒンジ (-X 縁)] */
hinge_x    = -72;      // ピン軸 x
hinge_y    = 10;       // ピン軸 y
knu_od     = 16;
pin_d      = 5.4;      // M5 ピン
knu_h      = 30;       // ゲート側ナックル高さ
knu_gap    = 0.4;      // 互い違いの遊び (片側)
hf_t       = 8;        // ヒンジ側フランジ板厚 (y)
hf_x0      = -64;      // フランジ板の外縁 (ナックルアームとの境界)

/* [ラッチ (+X 縁)、ノブボルト頭ポケット込み (改善要件 §3.6)] */
lf_t       = 10;       // ラッチ側フランジ板厚 (y)
lf_x0      = 54;
lf_x1      = 70;
boss_y1    = 16;       // ボスの前面 (ノブボルト頭の座)
boss_h     = 24;       // ボス高さ (z)
latch_z    = [40, 170];
m5_d       = 5.4;
knob_d     = 18;       // ノブ頭ポケット径 (頭 Ø16 用クリアランス)
knob_dep   = 12;       // ポケット深さ (前面から −Y へ)
knob_margin= 1;         // ポケット半径からボス幅への片側余裕

/* [窓 (軽量化・水抜き)] */
win_zb     = [[20, 90], [110, 185]];  // 窓の z 範囲 (屋根 45° 込み)
win_az     = [42.5, 137.5];           // 窓中心の方位角 (+X から)
win_w      = 44;                      // 窓の接線方向幅

/* [前面ハードポイント HP40 ×3 (改善要件 §3.1/§3.2)]
   HP4 (カメラブリッジ上) / HP5 (カメラブリッジ下) / HP-L (前向きライト)。
   座は共通平面 y=hp_seat_y、法線 +Y。座ブロックは x/z 中心 ±hp_half を
   半殻へ union し、内腔キャビティ差分が自動でトリムする (hp_back_y は
   キャビティより内側まで深く取り、境界形状を追わずに済ませる)。
   二重定義相手: child_cam_bridge (HP4/HP5)、ユーザ設計ライトクランプ (HP-L)。 */
hp_half     = 25;      // 座 (シェルフ) 半幅 (x, z とも)。M5 穴 ±20 + 壁厚を収める
hp_shelf_dep= 12;       // シェルフの奥行き (座面から −Y へ。インサート穴+ケーブル穴を包含)
hp_riser_half = 15;     // シェルフを支えるライザ半幅 (窓の方位角から十分離すため hp_half より狭い)
hp_back_y   = 40;       // ライザの奥行き基準面 (内腔差分でトリムされる安全値)
hp_insert_h = 9;        // インサート下穴深さ (M5×9 用。hardpoint.scad 既定の 8 より深い)
// [名前, xc, zc, cable, cable_dep]
// HP-L は 2026-09-04 コーディネータ指示で z45→z15 に下げた
// (child_cam_bridge のデッキ z45..53 との干渉回避)。
front_hp = [
    ["HP4",  0, 170, false, 0],
    ["HP5",  0, 100, false, 0],
    ["HP-L", 0,  15, true, 12],
];

/* [機体レベル検査] */
env_half   = 125.0;

/* [Hidden] */
fudge = 0.01;
$fn = 120;

// ---- 導出値 ---------------------------------------------------------
r_in     = tube_od/2 + (eva_t - eva_comp);      // 58.35 (EVA 圧縮後)
r_out    = r_in + shell_t;                      // 64.35
pkt_r    = cap_od/2 + pocket_rad;               // 60.9
pb_z0    = cap_z0 - pocket_clr;                 // 下ポケット床
pb_z1    = cap_z1 + pocket_clr;                 // 下ポケット天井
gate_z0  = pb_z0 - lip_b;                       // 部品下端 (-17.0)
pt_z0    = flange_top - pocket_clr;             // 上ポケット床 (207.5)
pt_z1    = flange_top + dome_ring_t + pocket_clr; // 上ポケット天井
gate_z1  = pt_z1 + lip_t;                       // 部品上端
gate_h   = gate_z1 - gate_z0;
cone_h   = pkt_r - r_in;                        // 45° 遷移コーン高さ (2.55)
knu_zc   = [gate_z0, (gate_z0+gate_z1)/2 - knu_h/2, gate_z1 - knu_h]; // 下端基準
latch_hx = (lf_x0 + lf_x1)/2;                   // ボルト x (62)

hp_seat_y   = r_out + 10;                       // 74.35 (シェル中心面外面 + 10)
boss_half_x = knob_d/2 + knob_margin;           // ノブポケットが収まるボス半幅 (10)
boss_x0     = latch_hx - boss_half_x;
boss_x1     = latch_hx + boss_half_x;

// ---- 干渉・成立性チェック -------------------------------------------
assert(r_in < cap_od/2 - 1.0,  "下リップがキャップリムを捕まえていない (掛かり<1mm)");
assert(r_in < dome_ring_od/2 - 1.0, "上リップがドームリングを捕まえていない");
assert(pkt_r > cap_od/2 + 0.3, "ポケット径のクリアランス不足");
assert((knu_od - pin_d)/2 >= 4.5, "ナックル壁厚 < 4.5mm");
pin_cb_d = 10;   // ピン抜け止めざぐり Ø (E リング用)、最上ナックル頂面
pin_cb_h = 4;    // ざぐり深さ
assert((knu_od - pin_cb_d)/2 >= 3, "ざぐり周囲のナックル壁厚 < 3mm");
assert(pin_cb_h < knu_h - 4, "ざぐりがナックル高さに対して深すぎる");
assert(hinge_x + knu_od/2 <= hf_x0, "ナックルがヒンジフランジ板に食い込む");
assert(hinge_x - knu_od/2 >= -env_half + 45, "ヒンジが 250 枠 (保護代 45) を超える");
assert(boss_x1 <= env_half - 45,  "ラッチボスが 250 枠 (保護代 45) を超える");
assert(latch_hx - m5_d/2 >= lf_x0 + 2 && lf_x1 - latch_hx - m5_d/2 >= 2,
       "ラッチ穴の x 端距離不足");
assert(boss_h/2 - m5_d/2 >= 4, "ラッチ穴の z 端距離不足");
assert(gate_h <= 250, "X1C の高さ 250 を超える");
win_half = asin(win_w/2 / r_in);   // 窓の方位角半幅 (~22.1°)
assert(min(win_az) - win_half > 8,  "窓がラッチ縁の平面部に掛かる");
assert(max(win_az) + win_half < 172, "窓がヒンジ縁の平面部に掛かる");

// ラッチ側ノブボルト頭ポケット (§3.6)
assert(boss_y1 - knob_dep >= 4 - 1e-6, "ノブポケット底の残り厚 < 4mm");
assert(sqrt(boss_x1*boss_x1 + boss_y1*boss_y1) <= 80,
       "ノブボルト頭が r80 の包絡から出る");

// 前面ハードポイント HP4/HP5/HP-L (§3.1)
shell_y_at20 = sqrt(r_out*r_out - 20*20);   // 61.2 (x=±20 でのシェル外面 y)
// (c) 窓 (方位角 42.5/137.5) とシェルフ/ライザが重ならない。
// シェルフ・ライザは軸対称の直方体なので、窓に最も近い角 (x=±half, y=その角の
// 手前側 y) の方位角が窓縁 (min(win_az)+win_half) より外側にあれば重ならない。
shelf_corner_az = atan2(hp_seat_y - hp_shelf_dep, hp_half);
// ライザの実材は r>=r_in でしか残らない (内腔差分でトリムされるため)。
// r=r_in での外縁の方位角が最小 (=最も窓寄り) になる。
riser_corner_az = atan2(sqrt(max(r_in*r_in - hp_riser_half*hp_riser_half, 0)), hp_riser_half);
win_edge_az = min(win_az) + win_half;   // 42.5 側の窓縁 (~64.7°、90°に近い方)
for (hp = front_hp) {
    xc = hp[1]; zc = hp[2];
    // (a) インサート穴がシェル壁に食い込まない (穴の −Y 端が壁外面より前)
    assert(hp_seat_y - hp_insert_h >= shell_y_at20,
           str(hp[0], ": インサート穴がシェル壁に食い込む"));
    assert(shelf_corner_az - win_edge_az > 1.5,
           str(hp[0], ": シェルフが窓に掛かる"));
    assert(riser_corner_az - win_edge_az > 1.5,
           str(hp[0], ": ライザが窓に掛かる"));
    // (d) 全高 ≤ 250 (gate_h の assert で担保済み)
}
// (b) HP 座同士が重ならない (z 方向、同一 x 帯なので z 帯の非重複だけで足りる。総当り)
for (i = [0 : len(front_hp) - 1], j = [0 : len(front_hp) - 1])
    if (i < j)
        assert(abs(front_hp[i][2] - front_hp[j][2]) > 2*hp_half,
               str(front_hp[i][0], "/", front_hp[j][0], ": HP 座ブロックが z 方向に重なる"));
// (e) 上ポケット (z ~207.5..) と HP4 の穴 (z 190, 深さ9) が離れている
hp4_hole_top = front_hp[0][2] + hp_half;   // 190 (HP4 は front_hp[0])
assert(pt_z0 - hp4_hole_top > 4, "上ポケットと HP4 の穴が近すぎる");
// (f) HP-L の穴 (z −5、y 65.35..74.35) が下ポケット (pkt_r 60.9, z −13.8..−8) に届かない
// (2026-09-04 コーディネータ指示。穴の z は下ポケット z 範囲 [pb_z0,pb_z1] の外、
//  かつ穴の最内端 y = hp_seat_y − hp_insert_h がシェル外面 y61.2 より前なので自動的に満たす)
hpl = front_hp[2];
assert(hpl[0] == "HP-L", "front_hp[2] が HP-L でない (table 順序を確認)");
hpl_bottom_hole_z = hpl[2] - 20;   // -5
assert(hpl_bottom_hole_z > pb_z1 + 2, "HP-L の穴が下ポケットの z 範囲に近すぎる");
assert(hp_seat_y - hp_insert_h > shell_y_at20, "HP-L の穴の最内端がシェル外面より奥に届く");

echo(str("gate z ", gate_z0, " .. ", gate_z1, " (h=", gate_h, ")"));
echo(str("ヒンジ側最外 x = ", hinge_x - knu_od/2, " / ラッチ側最外 x = ", boss_x1));

// ---- モジュール -----------------------------------------------------
// linear_extrude / polygon は FreeCAD の CSG→STEP 変換を壊すので使わない
// (cube / cylinder + ブーリアンのみ — 設計規約 1)。

// 45° 切妻屋根付きの窓カッター (半径方向に r 40..80 を貫く箱、
// 上部両角をダイヤモンド (45° 回転 cube) で欠いて五角形にする)
module window_cut(az, z0, z1, w) {
    sd = w / sqrt(2);   // 屋根ダイヤモンドの辺 (半対角 = w/2)
    rotate([0, 0, az]) difference() {
        translate([40, -w/2, z0]) cube([40, w, z1 - z0]);
        for (s = [-1, 1])
            translate([39, s*w/2, z1]) rotate([45, 0, 0])
                translate([0, -sd/2, -sd/2]) cube([42, sd, sd]);
    }
}

// 前面ハードポイント 1 個ぶんの座ブロック (union 側)。
// 座面 y=hp_seat_y、法線 +Y。2 段構成:
//   シェルフ (x/z ±hp_half、奥行き hp_shelf_dep): インサート穴+ケーブル穴を収める広い座面
//   ライザ (x/z ±hp_riser_half、シェルフ〜シェル): 窓の方位角から十分離すため狭くする
// (assert (c) 参照)。シェル内腔差分でトリムされる深さ (hp_back_y) まで奥に置く。
module hp_front_pad(xc, zc) {
    translate([xc - hp_half, hp_seat_y - hp_shelf_dep, zc - hp_half])
        cube([2*hp_half, hp_shelf_dep, 2*hp_half]);
    translate([xc - hp_riser_half, hp_back_y, zc - hp_half])
        cube([2*hp_riser_half, hp_seat_y - hp_shelf_dep - hp_back_y, 2*hp_half]);
}

// 前面ハードポイント 1 個ぶんの穴 (difference 側)。
// hardpoint.scad はローカル +Z が座面法線。rotate(a=180, v=[0,1,1]) は
//   ローカル+Z → 機体+Y (法線)、ローカル+Y → 機体+Z (方向記号を刻むなら +Z を指す)
// を同時に満たす回転 (X 軸だけの回転では両立しないため)。
// hp40_arrow() は linear_extrude(polygon) を使い CSG→STEP 変換を壊す
// (本ファイル冒頭の規約どおり) ため、ここでは刻印しない。向きは
// インサートパターンの非対称性が無いので現物では六角スペーサ等で管理する。
module hp_front_cut(xc, zc, cable, cable_dep) {
    translate([xc, hp_seat_y, zc]) rotate(a = 180, v = [0, 1, 1])
        hp40_cut(cable = cable, insert_h = hp_insert_h,
                 through_t = cable ? cable_dep : hp_insert_h + 4);
}

// ---- 形状 -----------------------------------------------------------
difference() {
    union() {
        // 半殻 (y >= 0)
        difference() {
            translate([0, 0, gate_z0]) cylinder(r = r_out, h = gate_h);
            translate([-r_out - 1, -r_out - 1, gate_z0 - fudge])
                cube([2*r_out + 2, r_out + 1, gate_h + 2*fudge]);
        }
        // ヒンジ側フランジ板 (全高)
        translate([hf_x0, 0, gate_z0])
            cube([-hf_x0 - r_in + 8, hf_t, gate_h]);   // x hf_x0..(-r_in+8)
        // ゲート側ナックル ×3 + アーム
        for (zc = knu_zc) {
            translate([hinge_x, hinge_y, zc]) cylinder(d = knu_od, h = knu_h);
            translate([hinge_x, 2, zc])
                cube([hf_x0 - hinge_x + fudge, hinge_y + knu_od/2 - 2, knu_h]);
        }
        // 前面ハードポイント座ブロック ×3 (HP4 / HP5 / HP-L)
        for (hp = front_hp) hp_front_pad(hp[1], hp[2]);
        // ラッチ側フランジ板 (全高)
        translate([lf_x0, 0, gate_z0]) cube([lf_x1 - lf_x0, lf_t, gate_h]);
        // ラッチボス ×2 (ノブポケットぶん幅を広げる)
        for (z = latch_z)
            translate([boss_x0, 0, z - boss_h/2])
                cube([boss_x1 - boss_x0, boss_y1, boss_h]);
    }

    // 内腔 (EVA 込みの把持面)
    translate([0, 0, gate_z0 - fudge]) cylinder(r = r_in, h = gate_h + 2*fudge);
    // 下ポケット (エンドキャップリム) + 45° 遷移コーン
    translate([0, 0, pb_z0]) cylinder(r = pkt_r, h = pb_z1 - pb_z0);
    translate([0, 0, pb_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
    // 上ポケット (ドーム押えリング) + 45° 遷移コーン
    translate([0, 0, pt_z0]) cylinder(r = pkt_r, h = pt_z1 - pt_z0);
    translate([0, 0, pt_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);

    // 窓 ×4 (45° 屋根付き)
    for (zb = win_zb, az = win_az) window_cut(az, zb[0], zb[1], win_w);

    // ヒンジピン Ø5.4 (全高通し)
    translate([hinge_x, hinge_y, gate_z0 - fudge])
        cylinder(d = pin_d, h = gate_h + 2*fudge, $fn = 32);

    // ヒンジピン抜け止めざぐり (2026-09-05、改善要件 §3.7): 最上ナックル頂面 (z gate_z1) に
    // Ø10 × 深さ 4。E リング/止め輪を頂面より下に沈める (コアフレーム側 z187.6 のざぐりは
    // 組立不能のため、実用の抜け止めはここ)
    translate([hinge_x, hinge_y, gate_z1 - pin_cb_h])
        cylinder(d = pin_cb_d, h = pin_cb_h + fudge, $fn = 48);

    // ラッチ M5 ×2 (軸 Y)。Ø5.4 の横穴は X1C で許容 (上面のわずかな垂れは
    // クリアランス穴なので実害なし。teardrop は STEP 品質優先で不採用)
    for (z = latch_z)
        translate([latch_hx, -fudge, z])
            rotate([-90, 0, 0]) cylinder(d = m5_d, h = boss_y1 + 2*fudge, $fn = 32);

    // ラッチ側ノブボルト頭ポケット ×2 (Ø18、深さ12、前面 y=boss_y1 から −Y へ。
    // 横穴なので盲穴底に 45° コーンを付けてオーバーハングを解消)
    for (z = latch_z)
        translate([latch_hx, boss_y1, z]) rotate([90, 0, 0]) union() {
            cylinder(d = knob_d, h = knob_dep - knob_d/2, $fn = 48);
            translate([0, 0, knob_dep - knob_d/2])
                cylinder(d1 = knob_d, d2 = 0, h = knob_d/2, $fn = 48);
        }

    // 前面ハードポイント HP4/HP5/HP-L: インサート下穴 ×4 + (HP-L のみ) 中央ケーブル穴
    for (hp = front_hp) hp_front_cut(hp[1], hp[2], hp[3], hp[4]);
}
