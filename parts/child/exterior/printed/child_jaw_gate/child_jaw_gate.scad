// =====================================================================
// child_jaw_gate.scad — 子機 外装 ワニ顎ゲート v3 (2026-09-09 ラッチ平面座)
// v3: M5 軸位置は維持。頭ポケットを廃止し、平面座を y24 に移して容器/EVA を避ける。
// 過去の v2 FEA は参考値。座面とボルト長の変更について再評価・実物確認が必要。
//
// v2 (2026-09-06): v1 (308.3 cm³) を topopt の設計空間モデル (topo_v1/) で
// トポロジー最適化し、その荷重経路地図を cube / cylinder で作り直したもの。
// **機能面 (取合い値) は v1 と同一**。最適化が示したこと:
//   - 帯と帯の間の半殻には材料がほとんど要らない → 把持帯 ×3 だけ残す
//     (下 z -17..6 / 中 z 92..108 / 上 z 200..218)
//   - ヒンジ側には帯をまたぐ柱が立たない (コア側ナックルが占有域なので物理的に不可)。
//     ナックル ×3 は各々「自分と重なる帯」へ直接ブロックで落ちる
//   - ラッチ側は全高の柱が立つ (x 58..72、y 0..16 — ノブ通路の口 y=16 の下)
//   - 前面は HP 座 ×3 を縦キール 2 本 (x ±20) でつないだ「背骨」になる。
//     窓 ×4 とライザ/シェルフの塊 (v1) は廃止
//
// 座標系: 機体グローバル。チューブ軸 = Z (x=y=0)、チューブ下端面 z=0、+Y = 前。
//   本部品は y >= 0 側。印刷向き: このまま (+Z up、全高 235 < 250)。プレート = z -17。
// 相手部品: child_core_frame v5 (y <= 0 側) / child_cam_bridge (HP4/HP5) /
//   ユーザ設計ライトクランプ (HP-L)。
// 荷重 (要件書 §3 + 改善要件 C6): L1 吊り 3g / L2f 前方 300N / L2s 側方 300N /
//   L3 把持プリロード (支配的) / L4 前方衝突 / L2L ライト経由 300N。
//   study は topo_v1/child_jaw_gate_v1_study.json。
// =====================================================================

use <../../../../../scad/lib/hardpoint.scad>

/* [耐圧容器 (STL 実測。child_core_frame と二重定義 — 片方だけ直さない)] */
tube_od    = 114.3;
cap_od     = 120.3;    // アルミエンドキャップ露出リム
cap_z0     = -13.8;    // リム下面
cap_z1     = -8.0;     // リム上面
flange_top = 208;      // 上フランジ上面 = ドーム座面

/* [ドームキャップ (未購入・仮値 — 要実測)] */
dome_ring_od = 120.3;
dome_ring_t  = 6.5;

/* [把持 (EVA 面圧)] */
eva_t      = 2.0;
eva_comp   = 0.8;
pocket_clr = 0.5;
pocket_rad = 0.75;

/* [シェル] */
shell_t    = 6.0;
lip_b      = 2.7;
lip_t      = 3.0;

/* [把持帯 (v2: 半殻はこの 3 帯だけ。帯間の殻は廃止)] */
band_bot_z1 = 6;        // 下ポケット帯 上端 (最適化 preserve は -2。HP-L キールと
                        //   下ナックルブロックの根元を伸ばすため +8)
band_mid    = [92, 108];
band_top_z0 = 200;

/* [ヒンジ (-X 縁)] */
hinge_x    = -72;
hinge_y    = 10;
knu_od     = 16;
pin_d      = 5.4;      // M5 ピン
knu_h      = 30;
knu_gap    = 0.4;      // 互い違いの遊び (片側)
hf_t       = 18;       // ヒンジ腕ブロックの y 厚 (y 0..18)。L3 でここが曲げの効き代
                       //   (18 = hinge_y + knu_od/2 = ヒンジ開閉スイープの限界)
hf_x1      = -50;      // 腕の内端 (内腔差分でトリムされ実効 x ~ -57)
pin_cb_d   = 10;       // ピン抜け止めざぐり Ø (E リング用)
pin_cb_h   = 4;
// コア側ナックル z (二重定義: child_core_frame.scad の aknu)
core_knu_z = [[13.4, 85.1], [115.9, 187.6]];

/* [ラッチ (+X 縁)] */
lf_x0      = 52;       // ラッチ柱 = ボスと同じ x 範囲 (内腔差分で実効 x ~57..72)
lf_x1      = 72;
lf_t       = 16;       // ラッチ柱の y 厚 (y 0..16 = ボス前面と面一)。
                       //   ノブ通路の口 (y=knob_y0=24) を越えないこと
latch_z    = [40, 170];
latch_hx   = 62;
m5_d       = 5.4;
boss_y1    = 24;       // 平面座。頭 Ø16 の全断面を圧縮 EVA の外へ出す
boss_h     = 34;       // 下面の 45° 補強が頭の支持面に掛からない高さ
knob_head_d = 16;      // 既存設計の頭径上限。購入品の実測は未確定
knob_margin = 2;       // 頭外周からボス x 端まで
knob_clearance = 0.5;  // 頭と圧縮 EVA の最小離隔
knob_acc_d = 24;       // ノブ挿入通路 Ø (仮値 — 要確認。obstacle と二重定義)
knob_acc_h = 30;       // 通路の奥行き (y = boss_y1 から +Y へ)

/* [前面ハードポイント HP40 ×3 + 縦キール] */
hp_half     = 25;      // 座面板 半幅 (x, z)
seat_t      = 6;       // 座面板 厚 (preserve は t4。L4 のたわみの 6 割が座面板自身の
                       //   曲げだったので 6 に増やした。voxel 2.0 の mesh resolution
                       //   (>=3 要素) もこれで通る)
ins_boss_d  = 12;      // インサートボス径 (preserve)
hp_pitch    = 40;
hp_insert_h = 9;       // インサート下穴深さ (M5×8 + 1)
keel_cx     = 20;      // 縦キール 中心 x (= hp_pitch/2、インサート列の直下)
keel_w      = 6;       // 縦キール 厚 (x)
keel_y0     = 40;      // キール後端の基準面 (内腔差分でトリムされる安全値)
// [名前, xc, zc, cable, cable_dep]
front_hp = [
    ["HP4",  0, 170, false, 0],
    ["HP5",  0, 100, false, 0],
    ["HP-L", 0,  15, true, 12],
];

/* [child_cam_bridge 占有域 (二重定義: child_cam_bridge.scad / topo_v1 obstacle)] */
brg_ix     = 27;       // 内側域の x 半幅 (|x| < 27 はデッキ+キールだけ)
brg_z      = [42.3, 74];   // 内側域の z 範囲 (デッキ z44.95 − 離隔 2.65 .. キール上端 74)

/* [機体レベル検査] */
env_half   = 125.0;

/* [Hidden] */
fudge = 0.01;
BIG   = 400;
$fn = 120;

// ---- 導出値 ---------------------------------------------------------
r_in     = tube_od/2 + (eva_t - eva_comp);      // 58.35 (EVA 圧縮後)
r_out    = r_in + shell_t;                      // 64.35
pkt_r    = cap_od/2 + pocket_rad;               // 60.9
pb_z0    = cap_z0 - pocket_clr;                 // -14.3
pb_z1    = cap_z1 + pocket_clr;                 // -7.5
gate_z0  = pb_z0 - lip_b;                       // -17.0
pt_z0    = flange_top - pocket_clr;             // 207.5
pt_z1    = flange_top + dome_ring_t + pocket_clr; // 215.0
gate_z1  = pt_z1 + lip_t;                       // 218.0
gate_h   = gate_z1 - gate_z0;                   // 235
cone_h   = pkt_r - r_in;                        // 2.55
knu_zc   = [gate_z0, (gate_z0+gate_z1)/2 - knu_h/2, gate_z1 - knu_h];  // -17 / 85.5 / 188

hp_seat_y   = r_out + 10;                       // 74.35 (座面)
hp_back_y   = hp_seat_y - seat_t;               // 70.35 (座面板の裏 = キール前端)
ins_boss_h  = hp_insert_h + 1 + 2;              // 12
hp_ix       = [-hp_pitch/2, hp_pitch/2];
brg_y0      = r_out;                            // 64.35 ブリッジ占有域の後面 = 殻外面

boss_half_x = knob_head_d/2 + knob_margin;      // 10
boss_x0     = latch_hx - boss_half_x;           // 52
boss_x1     = latch_hx + boss_half_x;           // 72
knob_y0     = boss_y1;                          // ノブ通路の口 (y)
knob_rz     = knob_acc_d/2;                     // 通路の z/x 半径 (12)

bands       = [[gate_z0, band_bot_z1], band_mid, [band_top_z0, gate_z1]];

// ---- 干渉・成立性チェック -------------------------------------------
// (1) 把持・ポケット
assert(r_in < cap_od/2 - 1.0,  "下リップがキャップリムを捕まえていない (掛かり<1mm)");
assert(r_in < dome_ring_od/2 - 1.0, "上リップがドームリングを捕まえていない");
assert(pkt_r > cap_od/2 + 0.3, "ポケット径のクリアランス不足");
assert(band_bot_z1 >= pb_z1 + cone_h + 2, "下ポケット帯がコーン上端 +2 より低い");
assert(band_top_z0 <= pt_z0 - 4, "上ポケット帯が上ポケットより 4mm 以上下から始まらない");
assert(band_mid[0] > pb_z1 + cone_h && band_mid[1] < pt_z0, "中央把持帯がポケットに掛かる");
assert(gate_h <= 250, "X1C の高さ 250 を超える");

// (2) ヒンジ
assert((knu_od - pin_d)/2 >= 4.5, "ナックル壁厚 < 4.5mm");
assert((knu_od - pin_cb_d)/2 >= 3, "ざぐり周囲のナックル壁厚 < 3mm");
assert(pin_cb_h < knu_h - 4, "ざぐりがナックル高さに対して深すぎる");
assert(hinge_x - knu_od/2 >= -env_half + 45, "ヒンジが 250 枠 (保護代 45) を超える");
assert(hf_t <= hinge_y + knu_od/2 + fudge,
       "ヒンジ腕ブロックがヒンジ開閉スイープ (x<hinge_x, y>18) に入る");
assert(hf_x1 > -r_in + 4, "ヒンジ腕の内端が内腔まで届いていない (トリム後に痩せる)");
// ゲート側ナックル ×3 と コア側ナックル ×2 が互い違いに噛み合う (二重定義の追従検査)
assert(abs(core_knu_z[0][0] - (knu_zc[0] + knu_h)) - knu_gap < 0.05 + fudge,
       "コア下ナックル 下端が ゲート下ナックル 上端 + 遊びと合わない");
assert(abs(knu_zc[1] - core_knu_z[0][1]) - knu_gap < 0.05 + fudge,
       "ゲート中ナックル 下端が コア下ナックル 上端 + 遊びと合わない");
assert(abs(core_knu_z[1][0] - (knu_zc[1] + knu_h)) - knu_gap < 0.05 + fudge,
       "コア上ナックル 下端が ゲート中ナックル 上端 + 遊びと合わない");
assert(abs(knu_zc[2] - core_knu_z[1][1]) - knu_gap < 0.05 + fudge,
       "ゲート上ナックル 下端が コア上ナックル 上端 + 遊びと合わない");
// ヒンジ腕ブロックは「自分のナックル z 範囲」だけに置く = コア側ナックル柱と z で交わらない
for (i = [0:2], b = core_knu_z)
    assert(knu_zc[i] + knu_h <= b[0] + fudge || knu_zc[i] >= b[1] - fudge,
           str("ゲートナックル ", i, " がコア側ナックル柱と z で重なる"));

// (3) ラッチ + ノブボルト挿入通路 (前ワーカー §7-1: v1 は通路が塞がっていた)
assert(boss_x1 <= env_half - 45,  "ラッチボスが 250 枠 (保護代 45) を超える");
assert(latch_hx - m5_d/2 >= lf_x0 + 2 && lf_x1 - latch_hx - m5_d/2 >= 2,
       "ラッチ穴の x 端距離不足");
assert(boss_h/2 - m5_d/2 >= 4, "ラッチ穴の z 端距離不足");
assert(boss_y1 >= lf_t && lf_t >= 4, "ラッチ座の厚さ不足");
assert(knob_head_d > m5_d && knob_margin >= 2, "頭の支持面またはボス端距離不足");
assert(latch_hx > knob_head_d/2 && boss_y1 > 0, "頭の離隔計算の前提違反");
assert(sqrt(pow(latch_hx - knob_head_d/2, 2) + pow(boss_y1, 2)) >= r_in + knob_clearance,
       "ノブ頭が容器/EVA に干渉する: 平面座を前へ出す必要あり");
assert(boss_h/2 - (boss_y1 - lf_t) >= knob_head_d/2 + 1,
       "下面の 45 度補強がノブ頭の平面支持領域に掛かる");
assert(knob_acc_d >= knob_head_d + 2*knob_clearance, "ノブ挿入通路が頭より狭い");
assert(sqrt(boss_x1*boss_x1 + boss_y1*boss_y1) <= 80, "ノブボルト頭が r80 の包絡から出る");
// --- ノブ挿入通路 (x latch_hx±12、y >= knob_y0、z latch_z±12) に材料が無いこと。
//     通路と重なりうる部材ごとに距離で検査する (OpenSCAD は空虚を測れないため)。
assert(lf_t <= knob_y0 + 1e-9, "ラッチ柱の前面がノブ通路の口を越える");
assert(boss_y1 <= knob_y0 + 1e-9, "ラッチボスの前面がノブ通路の口を越える");
for (z = latch_z) {
    // 把持帯 ×3: 全周の殻なので z で離すしかない
    for (b = bands)
        assert(b[1] <= z - knob_rz - fudge || b[0] >= z + knob_rz + fudge,
               str("把持帯 z ", b, " がノブ通路 (z ", z - knob_rz, "..", z + knob_rz, ") を塞ぐ"));
    // ヒンジ腕ブロック: x で離れている
    assert(hf_x1 <= latch_hx - knob_rz - fudge, "ヒンジ腕がノブ通路の x 範囲に入る");
    // 前面キール + HP 座面板 + インサートボス: x で離れている
    assert(keel_cx + keel_w/2 <= latch_hx - knob_rz - fudge, "縦キールがノブ通路の x 範囲に入る");
    assert(max([for (hp = front_hp) hp[1]]) + hp_half + (ins_boss_d - hp_pitch)/2
           <= latch_hx - knob_rz - fudge, "HP 座がノブ通路の x 範囲に入る");
}

// (4) 前面ハードポイント + 縦キール + ブリッジ占有域
shell_y_at20 = sqrt(r_out*r_out - pow(hp_pitch/2, 2));   // 61.15
assert(hp_seat_y == r_out + 10, "hp_seat_y が r_out + 10 と一致しない (二重定義のずれ)");
assert(hp_seat_y - hp_insert_h >= shell_y_at20, "インサート穴がシェル外面に食い込む");
assert(ins_boss_h >= hp_insert_h + 3, "インサートボスの底の残り肉 < 3mm");
assert(keel_cx == hp_pitch/2, "縦キールがインサート列の直下にない");
assert(keel_cx + keel_w/2 <= hp_half, "縦キールが座面板の幅からはみ出す");
assert(keel_cx - keel_w/2 - hp_cable_d()/2 >= 1,
       "縦キールが HP-L の中央ケーブル穴に掛かる");
assert(keel_y0 < r_in - 4, "キール後端が内腔差分でトリムされない (痩せた板になる)");
assert(keel_cx + keel_w/2 < brg_ix, "縦キールが child_cam_bridge の外側占有域 (|x|>=27) に入る");
// HP 座同士が z で重ならない (総当り)
for (i = [0 : len(front_hp) - 1], j = [0 : len(front_hp) - 1])
    if (i < j)
        assert(abs(front_hp[i][2] - front_hp[j][2]) > 2*hp_half,
               str(front_hp[i][0], "/", front_hp[j][0], ": HP 座が z 方向に重なる"));
// HP 座 (y >= hp_back_y) が child_cam_bridge の内側占有域 (z 42.3..74) と重ならない
for (hp = front_hp)
    assert(hp[2] + hp_half <= brg_z[0] - fudge || hp[2] - hp_half >= brg_z[1] - fudge,
           str(hp[0], ": 座面板が child_cam_bridge の占有域 z ", brg_z, " に掛かる"));
// 上ポケットと HP4 の穴 / 下ポケットと HP-L の穴
hp4_hole_top = front_hp[0][2] + hp_half;
assert(front_hp[0][0] == "HP4" && front_hp[2][0] == "HP-L", "front_hp の並びが想定と違う");
assert(pt_z0 - hp4_hole_top > 4, "上ポケットと HP4 の穴が近すぎる");
assert(front_hp[2][2] - hp_pitch/2 > pb_z1 + 2, "HP-L の穴が下ポケットの z 範囲に近すぎる");
assert(front_hp[2][2] + hp_half <= brg_z[0] - fudge, "HP-L 座がブリッジ占有域に掛かる");

echo(str("gate z ", gate_z0, " .. ", gate_z1, " (h=", gate_h, ")"));
echo(str("BANDS ", bands, " / knuckles ", knu_zc, " / core knuckles ", core_knu_z));
echo(str("LATCH plate x ", lf_x0, "..", lf_x1, " y 0..", lf_t,
         " / boss x ", boss_x0, "..", boss_x1, " y 0..", boss_y1,
         " / knob channel D", knob_acc_d, " @ (x", latch_hx, ", y>=", knob_y0, ", z ", latch_z, ")"));
echo(str("KEEL x +-", keel_cx, " w", keel_w, " y ..", hp_seat_y,
         " / bridge keepout |x|<", brg_ix, " y>=", brg_y0, " z ", brg_z));
echo(str("HPTABLE HP4 (0,", hp_seat_y, ",170) / HP5 (0,", hp_seat_y, ",100) / HP-L (0,",
         hp_seat_y, ",15) n=+Y"));

// hardpoint.scad の定数を式で使うための関数 (変数直接参照は use では見えない)
function hp_cable_d() = 14;   // = HP_CABLE_D (二重定義: scad/lib/hardpoint.scad)

// ---- モジュール -----------------------------------------------------
// cube / cylinder + ブーリアンのみ (設計規約 1)。hull/offset/minkowski/polygon 禁止。

// 半殻の z 帯 (y >= 0)。内腔・ポケットは最後にまとめて引く
module band(z0, z1) {
    intersection() {
        translate([0, 0, z0]) cylinder(r = r_out, h = z1 - z0);
        translate([-BIG/2, 0, z0 - fudge]) cube([BIG, BIG, z1 - z0 + 2*fudge]);
    }
}

// 内腔 + 上下ポケット + 45° 遷移コーン (child_core_frame と同一式)
module bore_void() {
    translate([0, 0, gate_z0 - 3]) cylinder(r = r_in, h = gate_h + 6);
    translate([0, 0, pb_z0]) cylinder(r = pkt_r, h = pb_z1 - pb_z0);
    translate([0, 0, pb_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
    translate([0, 0, pt_z0]) cylinder(r = pkt_r, h = pt_z1 - pt_z0);
    translate([0, 0, pt_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
}

// child_cam_bridge の占有域 (|x| < brg_ix、y >= r_out、z 42.3..74) +
// 上端に 45° の立ち上がり (キール前部の下面をサポートレスにする)。
// 立ち上がりは y <= hp_back_y に限る (HP5 座面板 y >= hp_back_y を切らない)
module bridge_keepout() {
    translate([-brg_ix, brg_y0, brg_z[0]]) cube([2*brg_ix, BIG, brg_z[1] - brg_z[0]]);
    ramp = hp_back_y - brg_y0;   // 6
    difference() {
        translate([-brg_ix, brg_y0, brg_z[1]]) cube([2*brg_ix, ramp, ramp]);
        translate([-brg_ix - 1, brg_y0, brg_z[1]]) rotate([45, 0, 0]) cube([2*brg_ix + 2, BIG, BIG]);
    }
}

// ノブボルト挿入通路 (Ø knob_acc_d、ボス前面 y=knob_y0 から +Y へ)。
// assert で材料が無いことを保証しているが、二重の保険として実際に引く
module knob_channel() {
    for (z = latch_z)
        translate([latch_hx, knob_y0, z]) rotate([-90, 0, 0])
            cylinder(d = knob_acc_d, h = knob_acc_h, $fn = 48);
}

// 前面ハードポイント 1 個ぶんの座 (union 側): 座面板 t4 + インサートボス Ø12 ×4。
// (topo_v1 の preserve と同形状)
module hp_pad(xc, zc) {
    translate([xc - hp_half, hp_back_y, zc - hp_half])
        cube([2*hp_half, seat_t, 2*hp_half]);
    for (dx = hp_ix, dz = hp_ix)
        translate([xc + dx, hp_seat_y, zc + dz]) rotate([90, 0, 0])
            cylinder(d = ins_boss_d, h = ins_boss_h);
}

// 前面ハードポイント 1 個ぶんの穴 (difference 側)。
// hardpoint.scad はローカル +Z が座面法線。rotate(a=180, v=[0,1,1]) で
// ローカル +Z → 機体 +Y。hp40_arrow() は polygon を使うので呼ばない (STEP 規約)
module hp_cut(xc, zc, cable, cable_dep) {
    translate([xc, hp_seat_y, zc]) rotate(a = 180, v = [0, 1, 1])
        hp40_cut(cable = cable, insert_h = hp_insert_h,
                 through_t = cable ? cable_dep : hp_insert_h + 4);
}

// ---- 形状 -----------------------------------------------------------
difference() {
    union() {
        // ==== 把持帯 ×3 (半殻。帯間の殻は最適化の結果 廃止) ====
        for (b = bands) band(b[0], b[1]);

        // ==== ヒンジ: ナックル Ø16 ×3 + 腕ブロック (各ナックルの z 範囲だけ) ====
        // 腕ブロックは x -80..-50 (内腔でトリムされ実効 -80..-57)、y 0..hf_t=18。
        // L3 (ピン −Y 300N) の曲げは y 深さで効く → v1 の y 0..8 から 18 に増やした
        // (18 = hinge_y + knu_od/2 = ヒンジ開閉スイープの限界)
        for (zc = knu_zc) {
            translate([hinge_x, hinge_y, zc]) cylinder(d = knu_od, h = knu_h);
            translate([hinge_x - knu_od/2, 0, zc])
                cube([hf_x1 - (hinge_x - knu_od/2), hf_t, knu_h]);
        }

        // ==== ラッチ: 全高の柱 (y 0..lf_t=16) + 平面座ボス ×2 (y 0..24) ====
        translate([lf_x0, 0, gate_z0]) cube([lf_x1 - lf_x0, lf_t, gate_h]);
        // lf_t == boss_y1 のときボスは柱に完全に含まれる (下面の 45° 面取りは不要)。
        // ボスを浅くしたときのために形状は残す
        for (z = latch_z)
            difference() {
                translate([boss_x0, 0, z - boss_h/2])
                    cube([boss_x1 - boss_x0, boss_y1, boss_h]);
                if (boss_y1 > lf_t) {
                    // ボスが柱より前に出るぶん (y lf_t..boss_y1) の下面を 45° にする
                    bd = (boss_y1 - lf_t) * sqrt(2);
                    translate([boss_x0 - 1, lf_t, z - boss_h/2]) rotate([-45, 0, 0])
                        translate([0, -bd, -bd]) cube([boss_x1 - boss_x0 + 2, bd, bd]);
                }
            }

        // ==== 前面: HP 座 ×3 + 縦キール ×2 (x ±20、全高、前面は座面 y=74.35 と面一) ====
        for (hp = front_hp) hp_pad(hp[1], hp[2]);
        for (s = [-1, 1])
            translate([s*keel_cx - keel_w/2, keel_y0, gate_z0])
                cube([keel_w, hp_seat_y - keel_y0, gate_h]);
    }

    // ---- 引く側 ----
    bore_void();                       // 内腔 + 上下ポケット + 45° コーン
    bridge_keepout();                  // child_cam_bridge 占有域 (+45° 立ち上がり)
    knob_channel();                    // ノブボルト挿入通路 ×2 (assert と二重の保険)

    // ヒンジピン Ø5.4 (全高通し) + 抜け止めざぐり (最上ナックル頂面)
    translate([hinge_x, hinge_y, gate_z0 - fudge])
        cylinder(d = pin_d, h = gate_h + 2*fudge, $fn = 32);
    translate([hinge_x, hinge_y, gate_z1 - pin_cb_h])
        cylinder(d = pin_cb_d, h = pin_cb_h + fudge, $fn = 48);

    // ラッチ M5 通し穴 ×2 (軸 Y)
    for (z = latch_z)
        translate([latch_hx, -fudge, z])
            rotate([-90, 0, 0]) cylinder(d = m5_d, h = boss_y1 + 2*fudge, $fn = 32);

    // 頭ポケットは設けない。y=boss_y1 の平面で頭を受ける。

    // 前面ハードポイント: インサート下穴 ×4 + (HP-L のみ) 中央ケーブル穴
    for (hp = front_hp) hp_cut(hp[1], hp[2], hp[3], hp[4]);
}
