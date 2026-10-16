// =====================================================================
// child_core_frame.scad — 子機 外装 コアフレーム v5 (ワニ顎の固定側 + 背骨、軽量化版)
//
// v5 (2026-09-06): v4 (650 cm³) を topopt の設計空間モデル (topo_v5/) でトポロジー最適化し、
// その荷重経路地図を cube / cylinder で作り直したもの。**機能面は v4 と同一** (取合い値は不変):
//   - ワニ顎の固定側: 把持帯 ×3 (下ポケット / 中央 / 上ポケット)。帯の間の半殻は廃止
//     (最適化は z 30..88 / 112..176 の殻に材料をほぼ置かなかった)
//   - ヒンジ (アフトナックル ×2 + ヒンジ側フランジ板)、ラッチ受け (ボス ×2 + ラッチ側フランジ板)
//   - 吊り耳ボス ×2 (z218 頂面)、下部ガードボス ×2 (方位角 210/330)
//   - 背面ケーブル溝 ×2 (チャンネル: 溝 10×8 + 側壁 2.5 + 底 4) + 結束スロット + 取っ手 (把持バー)
//     背面壁 t14 は廃止。溝チャンネルが柱を兼ねる (最適化の結果: 溝間の壁に材料は要らない)
//   - HP1 ペデスタル: 座面板 t4 + インサートボス + 中空の箱 (側壁/前壁/後壁 + 後端 45° ハンチ)
//   - HP2/HP3: 座面板 t4 + インサートボス + 上下棚 + 前柱 (x ±38..44) + 後柱
//   - 下部クロスバー + 平面斜材 (プレート上、z -17..7)、YZ 斜材 (座の後下角 → 前柱下端)
//   - ヒンジピン抜け止めざぐり (上アフトナックル頂面 Ø10×4)
//
// 座標系: 機体グローバル (チューブ軸=Z、z=0 チューブ下端、+Y=前)。本部品は y<=0 側。
// 印刷向き: このまま (+Z up、全高 235.5)。プレート = z -17。
// 荷重 (要件書 §3 + 改善要件 C6): L1 吊り 3g / L2 輸送 300 N (側方・ヒンジ側・後方) /
//   L3 把持プリロード / L5 着底。study は topo_v5/child_core_frame_v5_study.json。
// =====================================================================

use <../../../../../scad/lib/hardpoint.scad>

/* [耐圧容器 (child_jaw_gate と二重定義 — 片方だけ直さない)] */
tube_od    = 114.3;
cap_od     = 120.3;
cap_z0     = -13.8;
cap_z1     = -8.0;
flange_top = 208;
dome_ring_od = 120.3;   // 仮値
dome_ring_t  = 6.5;     // 仮値
eva_t      = 2.0;
eva_comp   = 0.8;
pocket_clr = 0.5;
pocket_rad = 0.75;
shell_t    = 6.0;
lip_b      = 2.7;
lip_t      = 3.0;

/* [把持帯 (v5: 半殻はこの 3 帯 + 縁ストリップだけ)] */
band_bot_z1 = 16;       // 下ポケット帯 上端 (ポケット + コーン + リップ 3 を含む)
band_mid    = [88, 112];
band_top_z0 = 196;      // 上ポケット帯 下端
strip_x     = 56;       // 縁ストリップ: |x| >= strip_x の半殻を全高で残す (ヒンジ/ラッチ縁の柱)

/* [ヒンジ (gate と共有)] */
hinge_x    = -72;
hinge_y    = 10;
knu_od     = 16;
pin_d      = 5.4;
knu_h      = 30;
knu_gap    = 0.4;
knb_y1     = 10;        // ナックル角ブロックの前端 (v4 は 18 = 円筒外径まで。v5 は円筒中心まで)
hf_t       = 12;        // ヒンジ側フランジ板 厚 (y -12..0)。v5b: 板は x -80..-50 全高 (ナックル柱を兼ねる)

/* [ラッチ受け] */
lf_x0      = 50;
lf_x1      = 72;
lf_t       = 10;        // ラッチ側フランジ板 厚 (y -10..0)
lfw_x      = [56, 66];  // ラッチ板の窓 (通し Y)
lfw_z      = [56, 150];
latch_z    = [40, 170];
latch_hx   = 62;
ins_d      = 6.4;
boss_h     = 24;
boss_t     = 18;        // ラッチボスの y 厚 (y -18..0)
latch_ins_h = 14;
latch_x0   = 52;        // ラッチボス x 範囲 (ゲート側ボス 52..72 と同じ)

/* [吊り耳ボス (child_lug / child_top_crown と二重定義)] */
lug_x      = 66;
lug_bolt_y = [-4, -16];
lug_boss_y = -22;
lug_boss_z = 204;

/* [背面ケーブル溝チャンネル ×2 (改善要件 §3.3)] */
py_y1      = -101;      // 溝の外面 (背面壁外面と同じ値を維持)
gr_cx      = 18;
gr_w       = 10;
gr_d       = 8;
gr_ch      = 1;
ch_wall    = 4;         // 溝の側壁厚 (v5: 2.5 → 4。最薄部を 4mm に揃えて FEA の mesh resolution を通す)
ch_floor   = 4;         // 溝底の厚 (溝底 y -93 → 内面 y -89)
tie_z      = [0, 30, 60, 90, 155];
tie_w      = 5.5;
tie_h      = 3;
gr_z1      = 182;       // 溝の上端 (v4 roof_z0)
bw_y1      = -87;       // 背面壁 内面 (結束スロットの出口)
bw_t       = 5;         // 背面壁 厚 (y -93..-88、v4 は t14)。v5b: L2 側方/後方の面内せん断板として復活
bw_hw      = 44;        // 背面壁 半幅 (前柱/後柱の外面まで)
bw_z0      = 7;         // 背面壁 下端 (下部クロスバーの上)

/* [取っ手] */
grip_z     = [145, 170];
grip_hw    = 30;        // 把持バー半幅 (中央部、y -101..-89)
grip_ext_x = 44;        // バーの延長 (x 30..44、後柱に結合)
slot_hw    = 26;        // 手穴 (v5 では壁が無いので、指空間の assert 用)
slot_z     = [115, 145];

/* [HP1 ペデスタル (中空の箱)] */
ped_x      = 30;
ped_y0     = -60;
ped_y1     = -110;
ped_z1     = 218.5;
hp1_cy     = -85;
dome_r_ped = 56.7;      // 仮値
pcab_d     = 12;
pcab_x     = 18;
pcab_y     = -92;
pcab_z0    = 174;
seat_t     = 4;         // 座面板厚
ins_boss_d = 15;        // インサートボス径 (Ø6.4 穴の周り 4.3mm)。Ø12 は壁 2.8 で FEA 最薄部、Ø14/Ø16 は既存の面 (前柱 y ±7、中央帯 z 88/112) にちょうど接して CSG→STEP が落ちる
pw_t       = 6;         // ペデスタル側壁/後壁 厚
pw_z0      = 182;       // 側壁 下端
pf_y0      = -66;       // 前壁 後端 (前壁 y -66..-54、上帯に載る)
pf_y1      = -54;
pf_z0      = 196;
pr_y0      = -93;       // 後壁 y -93..-87 (溝底の面と同一平面)
pr_y1      = -87;
pr_z0      = 170;       // 後壁 下端 (把持バー上端)
hau_z0     = 197.5;     // 後端ハンチ 下端 (y -93 で z 197.5 → y -110 で座面板下面 z 214.5 に収束。1.5mm の薄片を残さない)

/* [HP2/HP3 (HP40)] */
hp_face_x  = 44;
hp_cy      = -75;
hp_cz      = 100;
hp_pitch   = 40;
hp_ins_h   = 8;
hp_ins_d   = 6.4;
hp_cable_d = 14;
hp_pad     = 50;
hp_plate_z0 = 63;       // 座面板の下端 (座 75 より 12 下まで延ばして棚のガセットを支える)
hp_plate_z1 = 128;      // 座面板の上端 (インサート穴の端距離 2mm を確保、v4 の座ブロックと同じ)
shelf_x0   = 32;        // 上下棚 x 32..44
shelf_t    = 4;
shelf_y    = [-100, -50];
col_x0     = 38;        // 前柱/後柱 x 38..44
col_y      = [-62, -48];   // 前柱 y (殻に食い込む)
col_z      = [-17, 200];
head_x0    = 30;        // 前柱の頭 (x 30..44、ペデスタル前壁に結合)
head_y     = [-62, -52];   // 頭の y (x 30 で内腔 r_in+1 の外に収める)
head_z     = [160, 200];
rcol_y     = [-100, -90];  // 後柱 y
rcol_z     = [60, 150];
pw_x0      = 24;        // HP 中央 Ø14 の貫通先 (v4 パイロン内面)
hp_thru    = hp_face_x - pw_x0 + 2;

/* [下部クロス構造 (プレート上)] */
lb_y       = [-93, -80];
lb_z       = [-17, 7];
lb_hw      = 30;
diag_p0    = [25, -85];  // 平面斜材 始点 (チャンネル)
diag_p1    = [41, -58];  // 平面斜材 終点 (前柱)
diag_w     = 12;
strut_x    = [32, 44];   // YZ 斜材 x
strut_p0   = [-88, 78];  // (y, z) 座の後下角
strut_p1   = [-60, 20];  // (y, z) 前柱下端
strut_t    = 6;

/* [ヒンジピン抜け止めざぐり] */
cb_d       = 10;
cb_h       = 4;

/* [下部ガードボス (child_guard_ring と二重定義)] */
gb_az      = [210, 330];
gb_r1      = 70;
gb_r0      = 60;        // v5: r 60..70 (v4 は r_in から)
gb_w       = 34;
gb_z0      = -14;
gb_z1      = 10;
gb_m5_z    = [-9, 4];

/* [Hidden] */
fudge = 0.01;
BIG   = 400;
$fn = 120;

// ---- 導出値 (gate と同式) --------------------------------------------
r_in     = tube_od/2 + (eva_t - eva_comp);
r_out    = r_in + shell_t;
pkt_r    = cap_od/2 + pocket_rad;
pb_z0    = cap_z0 - pocket_clr;
pb_z1    = cap_z1 + pocket_clr;
frame_z0 = pb_z0 - lip_b;                       // -17.0
pt_z0    = flange_top - pocket_clr;
pt_z1    = flange_top + dome_ring_t + pocket_clr;
frame_z1 = pt_z1 + lip_t;                       // 218.0
frame_h  = frame_z1 - frame_z0;
cone_h   = pkt_r - r_in;
gknu_zc  = [frame_z0, (frame_z0+frame_z1)/2 - knu_h/2, frame_z1 - knu_h];
aknu     = [[gknu_zc[0] + knu_h + knu_gap, gknu_zc[1] - knu_gap],
            [gknu_zc[1] + knu_h + knu_gap, gknu_zc[2] - knu_gap]];
gb_haz   = asin((gb_w/2) / ((r_out + gb_r1)/2));
gr_y0    = py_y1 + gr_d;                        // 溝底 y = -93
gr_x0    = gr_cx - gr_w/2;                      // 13
gr_x1    = gr_cx + gr_w/2;                      // 23
ch_x0    = gr_x0 - ch_wall;                     // 10.5
ch_x1    = gr_x1 + ch_wall;                     // 25.5
ch_y1    = gr_y0 + ch_floor;                    // -89
hp_iy    = [hp_cy - hp_pitch/2, hp_cy + hp_pitch/2];   // -95 / -55
hp_iz    = [hp_cz - hp_pitch/2, hp_cz + hp_pitch/2];   //  80 / 120
hp_y0    = hp_cy + hp_pad/2;                    // -50
hp_y1    = hp_cy - hp_pad/2;                    // -100
hp_z0    = hp_cz - hp_pad/2;                    // 75
hp_z1    = hp_cz + hp_pad/2;                    // 125
hp1_iy   = [hp1_cy - hp_pitch/2, hp1_cy + hp_pitch/2]; // -105 / -65
hp1_thru = ped_z1 - pw_z0 + 1;                  // 中央 Ø14 を箱の中 (空洞) まで貫通
cb_z     = aknu[1][1];                          // 187.6
ped_z0   = ped_z1 - seat_t;                     // 座面板 下面 214.5
hau_run  = abs(ped_y1) - abs(pr_y0);            // ハンチの奥行 17 (y -93 → -110)

// ---- 検査 -------------------------------------------------------------
assert(r_in < cap_od/2 - 1.0 && r_in < dome_ring_od/2 - 1.0, "リップの掛かり不足");
assert(band_bot_z1 >= pb_z1 + cone_h + lip_t, "下ポケット帯がコーン上端 + リップより低い");
assert(band_top_z0 <= pt_z0 - 4, "上ポケット帯が上ポケットより 4mm 以上下から始まらない");
assert(strip_x < r_out && strip_x >= lf_x0, "縁ストリップの x がフランジ板/殻と整合しない");
assert(sqrt(lug_x*lug_x + pow(min([for (y = lug_bolt_y) abs(y)]), 2)) - ins_d/2
       > pkt_r + 1.5, "耳ボス M5 が上ポケットの壁に食い込む (壁 < 1.5mm)");
assert(lug_x - ins_d/2 >= lf_x0 + 2 && lug_x + ins_d/2 <= lf_x1 - 2, "耳ボス M5 の x 端距離不足");
assert(min(lug_bolt_y) - ins_d/2 >= lug_boss_y + 2, "耳ボス M5 の y 端距離不足");
assert(latch_z[0] - boss_h/2 > gb_z1 + 4, "ラッチ下ボスがガードボスに掛かる");
assert(lfw_z[0] - latch_z[0] - boss_h/2 >= 4 && latch_z[1] - boss_h/2 - lfw_z[1] >= 4, "ラッチ板窓がボスに近すぎる");
assert(lfw_x[0] >= lf_x0 + 2 && lfw_x[1] <= lf_x1 - 4, "ラッチ板窓の x 端距離不足");
assert(bw_hw >= hp_face_x && bw_z0 >= lb_z[1] - 1 && gr_y0 + bw_t <= bw_y1 + fudge, "背面壁の範囲が下部バー/後壁/溝と整合しない");
assert(boss_t - latch_ins_h >= 4, "ラッチインサート穴の底の残り肉 < 4mm");
assert(latch_x0 >= lf_x0 && latch_hx - ins_d/2 >= latch_x0 + 2 && latch_hx + ins_d/2 <= lf_x1 - 2,
       "ラッチインサートがボスの x 端を破る");
// 溝チャンネルと取っ手
assert(ch_x0 > 0 && ch_x1 <= grip_hw, "溝チャンネルが中心を跨ぐか把持バーからはみ出す");
assert(ch_floor >= 3, "溝底が 3mm 未満");
assert(gr_x1 + gr_ch <= ch_x1, "溝口の面取りがチャンネル側壁を抜ける");
assert(tie_w <= gr_w - 2 && min(tie_z) - tie_h/2 > frame_z0 && max(tie_z) + tie_h/2 < gr_z1 - 4,
       "結束スロットが溝の外へ出る");
assert(min([for (z = tie_z) (z + tie_h/2 <= slot_z[0]) ? slot_z[0] - (z + tie_h/2)
                                                       : (z - tie_h/2) - slot_z[1]]) >= 8,
       "結束スロットが取っ手の手穴 (指空間) に 8mm 以内まで近づく");
assert(grip_z[0] == slot_z[1], "把持バーは指空間の直上に置く");
assert(grip_ext_x >= hp_face_x, "バーの延長が後柱まで届かない");
assert(lb_z[0] == frame_z0, "下部クロス構造はプレートに載せる (サポートレス)");
// HP2/3
assert(hp_face_x - seat_t - (hp_ins_h + 1) >= head_x0, "HP2/3 インサートボスが柱の頭より内側に出る");
assert(min([for (y = hp_iy) abs(y)]) - hp_ins_d/2 >= abs(hp_y0) + 1.5 &&
       abs(hp_y1) - max([for (y = hp_iy) abs(y)]) - hp_ins_d/2 >= 1.5, "HP インサート穴が座面板の y 端を破る");
assert(min(hp_iz) - hp_ins_d/2 >= hp_plate_z0 + 2 && max(hp_iz) + hp_ins_d/2 <= hp_plate_z1 - 2, "HP インサート穴が座面板の z 端を破る");
assert(hp_face_x - hp_thru < pw_x0 + fudge, "HP 中央 Ø14 が空洞に届かない");
assert(shelf_y[0] <= min(hp_iy) - hp_ins_d/2 - 1 && shelf_y[1] >= max(hp_iy) + hp_ins_d/2 + 1,
       "棚がインサートボスを覆わない");
assert(hp_plate_z0 <= hp_z0 - (hp_face_x - shelf_x0), "座面板の下延長が棚ガセット (45°) の下端に届かない");
assert(hp_z1 - shelf_t - (hp_face_x - shelf_x0) >= hp_z0 + shelf_t + 2, "上棚のガセットが下棚に掛かる");
assert(sqrt(pow(col_x0, 2) + pow(col_y[1], 2)) >= r_in + 1.0 &&
       sqrt(pow(head_x0, 2) + pow(head_y[1], 2)) >= r_in + 1.0, "前柱/頭がチューブ内腔に侵入 (bore で削る前提でも 1mm 確保)");
assert(sqrt(pow(hp_face_x, 2) + pow(col_y[0], 2)) > r_out, "前柱の後端が殻の外に出ていない");
assert(rcol_y[0] <= hp_y1 && rcol_y[1] >= hp_y1 + 1, "後柱が座面板の後端に重ならない");
assert(rcol_z[1] >= grip_z[0] + 2 && rcol_z[0] <= hp_plate_z0 + 2, "後柱が把持バー/座面板に重ならない");
assert(hp_face_x <= lf_x0 - 4, "HP 座面が吊り耳ボス/ラッチ板より外に出る");
assert(min(col_z) == frame_z0, "前柱はプレートから立てる");
// ペデスタル
assert(abs(ped_y0) - dome_r_ped >= 3.0, "ペデスタル前端が z218.5 のドーム断面に 3mm 以内");
assert(min([for (y = hp1_iy) abs(y)]) - hp_ins_d/2 - abs(ped_y0) >= 1.5 &&
       abs(ped_y1) - max([for (y = hp1_iy) abs(y)]) - hp_ins_d/2 >= 1.5, "HP1 インサートとペデスタル y 端の残り肉不足");
assert(ped_x - hp_pitch/2 - hp_ins_d/2 >= 2, "HP1 インサートとペデスタル x 端の残り肉不足");
assert(ped_x <= lf_x0 - 4, "ペデスタルが吊り耳ボスからはみ出す");
assert(ped_z0 - (hp_ins_h + 1) > pcab_z0, "HP1 インサートボス下端が縦穴の下端より低い");
assert(sqrt(pow(pcab_x - hp_pitch/2, 2) + pow(pcab_y - min(hp1_iy), 2)) >= pcab_d/2 + hp_ins_d/2 + 2,
       "縦穴と HP1 後列インサートの残り肉 < 2mm");
assert(sqrt(pow(pcab_x, 2) + pow(pcab_y - hp1_cy, 2)) >= pcab_d/2 + hp_cable_d/2 + 2, "縦穴と HP1 中央 Ø14 の残り肉 < 2mm");
assert(pcab_y - pcab_d/2 <= gr_y0 && pcab_y + pcab_d/2 > pr_y1, "縦穴が背面溝とペデスタル空洞をつないでいない");
assert(pcab_z0 < gr_z1 - 4 && pcab_z0 > max(tie_z) + tie_h/2, "縦穴の下端が背面溝の中にない");
assert(pr_y0 == gr_y0, "後壁は溝底 (y -93) と同一平面に置く");
assert(pr_z0 == grip_z[1], "後壁は把持バーの上に載せる");
assert(abs(hau_z0 + hau_run - ped_z0) < 0.01, "後端ハンチ (45°) の先端は座面板の下面にちょうど収束させる (薄片を残すと FEA の最薄部になる)");
assert(hau_z0 <= ped_z0 - (hp_ins_h + 1 + 2) + (abs(min(hp1_iy)) - abs(pr_y0)) - hp_ins_d/2 - 3.5,
       "HP1 後列インサートボスがハンチ面より下に出る");
assert(head_z[1] == col_z[1] && head_z[0] < pw_z0, "前柱の頭がペデスタル側壁に届かない");
assert(pf_z0 >= band_top_z0 && pf_y1 > -r_out, "ペデスタル前壁が上帯に載らない");
// 干渉: 前柱・頭がラッチ板/吊り耳ボスと離れている
assert(hp_face_x + 2 <= lf_x0, "前柱の頭がラッチ側フランジ板に当たる");
// ざぐり
assert((knu_od - cb_d)/2 >= 3, "ざぐり周りのナックル壁厚 < 3mm");
assert(cb_d > pin_d + 2 && cb_h + 6 <= aknu[1][1] - aknu[1][0], "ざぐりがナックル高さに対して深すぎる");
echo(str("frame z ", frame_z0, "..", frame_z1, " / アフトナックル z ", aknu));
echo(str("HPTABLE HP1 (0,", hp1_cy, ",", ped_z1, ") n=+Z / HP2 (", hp_face_x, ",", hp_cy,
         ",", hp_cz, ") n=+X / HP3 (", -hp_face_x, ",", hp_cy, ",", hp_cz, ") n=-X"));
echo(str("PEDESTAL x +-", ped_x, " y ", ped_y1, "..", ped_y0, " z ", pw_z0, "..", ped_z1,
         " / haunch z ", hau_z0, " / vcable D", pcab_d, " @ (+-", pcab_x, ",", pcab_y, ")"));
echo(str("GROOVE x +-", gr_cx, " w", gr_w, " d", gr_d, " z ", frame_z0, "..", gr_z1,
         " / tie z ", tie_z, " / counterbore z ", cb_z));

// ---- モジュール --------------------------------------------------------
module half_y_neg(z0, z1) { translate([-BIG/2, -BIG, z0]) cube([BIG, BIG, z1 - z0]); }
module wedge(az0, az1, z0, h) {
    intersection() {
        rotate([0, 0, az0]) translate([0, 0, z0]) cube([200, 200, h]);
        rotate([0, 0, az1 - 90]) translate([0, 0, z0 - fudge]) cube([200, 200, h + 2*fudge]);
    }
}
// 半殻の z 帯 (y<=0)。内腔・ポケットは最後に引く
module band(z0, z1) {
    intersection() {
        translate([0, 0, z0]) cylinder(r = r_out, h = z1 - z0);
        half_y_neg(z0 - fudge, z1 + fudge);
    }
}
// 内腔 + ポケット + 45° コーン (gate と同一式)
module bore_void() {
    translate([0, 0, frame_z0 - 3]) cylinder(r = r_in, h = frame_h + 8);
    translate([0, 0, pb_z0]) cylinder(r = pkt_r, h = pb_z1 - pb_z0);
    translate([0, 0, pb_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
    translate([0, 0, pt_z0]) cylinder(r = pkt_r, h = pt_z1 - pt_z0);
    translate([0, 0, pt_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
}
// YZ 面内の斜材 (x0..x1、(y0,z0) → (y1,z1)、厚 t を法線方向に)
module strut_yz(x0, x1, p0, p1, t) {
    dy = p1[0] - p0[0]; dz = p1[1] - p0[1];
    L = sqrt(dy*dy + dz*dz); a = atan2(dz, dy);
    translate([x0, p0[0], p0[1]]) rotate([a, 0, 0]) translate([0, 0, -t/2]) cube([x1 - x0, L, t]);
}
// XY 面内の斜材 (z0..z1、(x0,y0) → (x1,y1)、幅 w)
module strut_xy(p0, p1, w, z0, z1) {
    dx = p1[0] - p0[0]; dy = p1[1] - p0[1];
    L = sqrt(dx*dx + dy*dy); a = atan2(dy, dx);
    translate([p0[0], p0[1], z0]) rotate([0, 0, a]) translate([0, -w/2, 0]) cube([L, w, z1 - z0]);
}
// 45° チャンファ用の切り取りブロック: 稜 (x, z) を通り、+X 側に向かって下がる面より下 (x 方向に幅 w)
module chamfer_cut_x(x_edge, z_edge, y0, y1, w, s) {
    // s = +1: x_edge から +X へ w だけ、z が z_edge から w だけ下がる三角柱を切る
    translate([x_edge, y0 - 1, z_edge]) rotate([0, s*45, 0])
        translate([s > 0 ? 0 : -w*sqrt(2), 0, -w*sqrt(2)]) cube([w*sqrt(2), y1 - y0 + 2, w*sqrt(2)]);
}

// ---- 形状 --------------------------------------------------------------
difference() {
    union() {
        // ==== 把持帯 ×3 + 縁ストリップ (半殻) ====
        band(frame_z0, band_bot_z1);
        band(band_mid[0], band_mid[1]);
        band(band_top_z0, frame_z1);
        intersection() {
            band(frame_z0, frame_z1);
            union() {
                translate([strip_x, -BIG/2, frame_z0 - 1]) cube([BIG, BIG, frame_h + 2]);
                translate([-BIG - strip_x, -BIG/2, frame_z0 - 1]) cube([BIG, BIG, frame_h + 2]);
            }
        }
        // ==== ヒンジ側フランジ板 (x -80..-50、y -12..0、全高 = ヒンジ柱) + アフトナックル ×2 ====
        translate([hinge_x - knu_od/2, -hf_t, frame_z0]) cube([-(hinge_x - knu_od/2) - r_in + hf_t, hf_t, frame_h]);
        for (b = aknu) {
            translate([hinge_x - knu_od/2, -hf_t, b[0]])
                cube([knu_od, knb_y1 + hf_t, b[1] - b[0]]);
            translate([hinge_x, hinge_y, b[0]]) cylinder(d = knu_od, h = b[1] - b[0]);
        }
        // ==== ラッチ側フランジ板 (y -12..0、窓付き) + ラッチボス ×2 ====
        difference() {
            translate([lf_x0, -lf_t, frame_z0]) cube([lf_x1 - lf_x0, lf_t, frame_h]);
            lsd = 8 * sqrt(2);
            difference() {
                translate([lfw_x[0], -lf_t - 1, lfw_z[0]]) cube([lfw_x[1] - lfw_x[0], lf_t + 2, lfw_z[1] - lfw_z[0]]);
                for (sx = [0, 1], sz = [0, 1])
                    translate([lfw_x[sx], -lf_t - 2, lfw_z[sz]]) rotate([0, 45, 0])
                        translate([-lsd/2, 0, -lsd/2]) cube([lsd, lf_t + 4, lsd]);
            }
        }
        // ==== 背面壁 (x ±44、y -93..-87、z 7..182、手穴 52×30 上角 45°) ====
        difference() {
            translate([-bw_hw, gr_y0, bw_z0]) cube([2*bw_hw, bw_t, gr_z1 - bw_z0]);
            hs = 16 * sqrt(2) / 2;
            difference() {
                translate([-slot_hw, gr_y0 - 1, slot_z[0]]) cube([2*slot_hw, bw_t + 2, slot_z[1] - slot_z[0]]);
                for (s = [-1, 1])
                    translate([s*slot_hw, gr_y0 - 2, slot_z[1]]) rotate([0, 45, 0])
                        translate([-hs/2, 0, -hs/2]) cube([hs, bw_t + 4, hs]);
            }
        }
        for (z = latch_z)
            difference() {
                translate([latch_x0, -boss_t, z - boss_h/2]) cube([lf_x1 - latch_x0, boss_t, boss_h]);
                // 下面 45° (サポートレス)
                translate([latch_x0 - 1, -boss_t, z - boss_h/2]) rotate([-45, 0, 0])
                    translate([0, -(boss_t - lf_t)*sqrt(2), -(boss_t - lf_t)*sqrt(2)])
                        cube([lf_x1 - latch_x0 + 2, (boss_t - lf_t)*sqrt(2), (boss_t - lf_t)*sqrt(2)]);
            }
        // ==== 吊り耳ボス ×2 (z 204..218、y -22..0) ====
        for (sx = [-1, 1])
            difference() {
                translate([sx > 0 ? lf_x0 : -lf_x1, lug_boss_y, lug_boss_z])
                    cube([lf_x1 - lf_x0, -lug_boss_y, frame_z1 - lug_boss_z]);
                translate([sx > 0 ? lf_x0 - 1 : -lf_x1 - 1, lug_boss_y, lug_boss_z]) rotate([-45, 0, 0])
                    translate([0, -(-lug_boss_y - lf_t)*sqrt(2), -(-lug_boss_y - lf_t)*sqrt(2)])
                        cube([lf_x1 - lf_x0 + 2, (-lug_boss_y - lf_t)*sqrt(2), (-lug_boss_y - lf_t)*sqrt(2)]);
            }
        // ==== 下部ガードボス ×2 (r 60..70 の帯、方位角 210/330) ====
        for (az = gb_az)
            intersection() {
                difference() {
                    translate([0, 0, gb_z0]) cylinder(r = gb_r1, h = gb_z1 - gb_z0);
                    translate([0, 0, gb_z0 - fudge]) cylinder(r = gb_r0, h = gb_z1 - gb_z0 + 2*fudge);
                }
                wedge(az - gb_haz, az + gb_haz, gb_z0 - fudge, gb_z1 - gb_z0 + 2*fudge);
            }
        // ==== 背面ケーブル溝チャンネル ×2 (全高、溝は後で引く) ====
        for (s = [-1, 1])
            translate([s > 0 ? ch_x0 : -ch_x1, py_y1, frame_z0]) cube([ch_x1 - ch_x0, ch_y1 - py_y1, gr_z1 - frame_z0]);
        // ==== 把持バー (中央 y -101..-89、両端は y -101..-87 で後柱へ) ====
        translate([-grip_hw, py_y1, grip_z[0]]) cube([2*grip_hw, ch_y1 - py_y1, grip_z[1] - grip_z[0]]);
        for (s = [-1, 1])
            translate([s > 0 ? grip_hw - 2 : -grip_ext_x, py_y1, grip_z[0]])
                cube([grip_ext_x - grip_hw + 2, pr_y1 - py_y1, grip_z[1] - grip_z[0]]);
        // ==== 下部クロスバー + 平面斜材 ×2 (プレート上 z -17..7) ====
        translate([-lb_hw, lb_y[0], lb_z[0]]) cube([2*lb_hw, lb_y[1] - lb_y[0], lb_z[1] - lb_z[0]]);
        for (s = [-1, 1])
            strut_xy([s*diag_p0[0], diag_p0[1]], [s*diag_p1[0], diag_p1[1]], diag_w, lb_z[0], lb_z[1]);
        // ==== HP2/HP3: 座面板 + インサートボス + 上下棚 (+45° ガセット) + 前柱 (+頭) + 後柱 + YZ 斜材 ====
        for (s = [-1, 1]) {
            // 座面板 (x 40..44、z 63..128)
            translate([s > 0 ? hp_face_x - seat_t : -hp_face_x, hp_y1, hp_plate_z0])
                cube([seat_t, hp_pad, hp_plate_z1 - hp_plate_z0]);
            // インサートボス ×4
            for (yy = hp_iy, zz = hp_iz)
                translate([s*hp_face_x, yy, zz]) rotate([0, -s*90, 0]) cylinder(d = ins_boss_d, h = hp_ins_h + 1 + 2);
            // 上棚 (z 121..125) と 下棚 (z 75..79)、どちらも下面に 45° ガセット (座面板に載る)
            difference() {
                translate([s > 0 ? shelf_x0 : -hp_face_x, shelf_y[0], hp_z1 - shelf_t - (hp_face_x - shelf_x0)])
                    cube([hp_face_x - shelf_x0, shelf_y[1] - shelf_y[0], (hp_face_x - shelf_x0) + shelf_t]);
                chamfer_cut_x(s > 0 ? shelf_x0 : -shelf_x0, hp_z1 - shelf_t, shelf_y[0], shelf_y[1], hp_face_x - shelf_x0, s);
            }
            difference() {
                translate([s > 0 ? shelf_x0 : -hp_face_x, shelf_y[0], hp_z0 - (hp_face_x - shelf_x0)])
                    cube([hp_face_x - shelf_x0, shelf_y[1] - shelf_y[0], (hp_face_x - shelf_x0) + shelf_t]);
                chamfer_cut_x(s > 0 ? shelf_x0 : -shelf_x0, hp_z0, shelf_y[0], shelf_y[1], hp_face_x - shelf_x0, s);
            }
            // 前柱 (x 38..44、y -62..-48、z -17..200) + 頭 (x 30..44、z 160..200、下面 45°)
            translate([s > 0 ? col_x0 : -hp_face_x, col_y[0], col_z[0]])
                cube([hp_face_x - col_x0, col_y[1] - col_y[0], col_z[1] - col_z[0]]);
            difference() {
                translate([s > 0 ? head_x0 : -hp_face_x, head_y[0], head_z[0]])
                    cube([hp_face_x - head_x0, head_y[1] - head_y[0], head_z[1] - head_z[0]]);
                chamfer_cut_x(s > 0 ? head_x0 : -head_x0, head_z[0] + (col_x0 - head_x0), head_y[0], head_y[1], col_x0 - head_x0, s);
            }
            // 後柱 (x 38..44、y -100..-90、z 60..150)
            translate([s > 0 ? col_x0 : -hp_face_x, rcol_y[0], rcol_z[0]])
                cube([hp_face_x - col_x0, rcol_y[1] - rcol_y[0], rcol_z[1] - rcol_z[0]]);
            // YZ 斜材: 座の後下角 (y -88, z 78) → 前柱下端 (y -60, z 20)
            strut_yz(s > 0 ? strut_x[0] : -strut_x[1], s > 0 ? strut_x[1] : -strut_x[0], strut_p0, strut_p1, strut_t);
        }
        // ==== HP1 ペデスタル (中空の箱) ====
        // 座面板 (z 214.5..218.5) + インサートボス ×4
        translate([-ped_x, ped_y1, ped_z0]) cube([2*ped_x, ped_y0 - ped_y1, seat_t]);
        // ボスはペデスタルの平面内 (y >= -110) に収める (後列ボスがはみ出さないように)。
        // intersection は 1 ボスずつ 2 子で書く (group を含む intersection は FreeCAD の CSG 取り込みで空になる)
        for (sx = [-1, 1], yy = hp1_iy)
            intersection() {
                translate([sx*hp_pitch/2, yy, ped_z0 - hp_ins_h - 1 - 2]) cylinder(d = ins_boss_d, h = hp_ins_h + 1 + 2 + fudge);
                translate([-ped_x, ped_y1, ped_z0 - 30]) cube([2*ped_x, ped_y0 - ped_y1, 30 + seat_t + 1]);
            }
        // 側壁 ×2 (x ±24..30、y -93..-60、z 182..214.5、前柱の頭に 2mm 重ねる。下面は 45°)
        for (s = [-1, 1])
            difference() {
                translate([s > 0 ? ped_x - pw_t : -ped_x, pr_y0, pw_z0]) cube([pw_t, head_y[0] + 2 - pr_y0, ped_z0 - pw_z0 + fudge]);
                chamfer_cut_x(s > 0 ? ped_x - pw_t : -(ped_x - pw_t), pw_z0 + pw_t, pr_y0, head_y[0] + 2, pw_t, s);
            }
        // 前壁 (x ±30、y -70..-52、z 194..214.5、上帯に載る。内腔は後で引く)
        translate([-ped_x, pf_y0, pf_z0]) cube([2*ped_x, pf_y1 - pf_y0, ped_z0 - pf_z0 + fudge]);
        // 後壁 (x ±30、y -93..-87、z 170..214.5、把持バーの上)
        translate([-ped_x, pr_y0, pr_z0]) cube([2*ped_x, pr_y1 - pr_y0, ped_z0 - pr_z0 + fudge]);
        // 後端ハンチ 45° (y -93 → -110 で z 196 → 213、座面板の下)
        difference() {
            translate([-ped_x, ped_y1, hau_z0]) cube([2*ped_x, pr_y0 - ped_y1, ped_z0 - hau_z0 + fudge]);
            translate([-ped_x - 1, pr_y0, hau_z0]) rotate([45, 0, 0])
                translate([0, -400, -400]) cube([2*ped_x + 2, 400, 400]);
        }
    }

    // ==== 引く側 ====
    bore_void();
    // ヒンジピン Ø5.4 + 抜け止めざぐり
    translate([hinge_x, hinge_y, frame_z0 - fudge]) cylinder(d = pin_d, h = frame_h + 2*fudge, $fn = 32);
    translate([hinge_x, hinge_y, cb_z - cb_h]) cylinder(d = cb_d, h = cb_h + fudge, $fn = 48);
    // ラッチ M5 インサート下穴 ×2 (y=0 面から深さ 14)
    for (z = latch_z)
        translate([latch_hx, -latch_ins_h, z]) rotate([-90, 0, 0]) cylinder(d = ins_d, h = latch_ins_h + fudge, $fn = 32);
    // 吊り耳 M5 インサート下穴 ×4 (z=218 頂面から深さ 10)
    for (sx = [-1, 1], yy = lug_bolt_y)
        translate([sx*lug_x, yy, frame_z1 - 10]) cylinder(d = ins_d, h = 10 + 2*fudge, $fn = 32);
    // 下部ガード M5 インサート ×4 (ボス外面から径方向、深さ 8)
    for (az = gb_az, z = gb_m5_z)
        rotate([0, 0, az]) translate([gb_r1 - 8, 0, z]) rotate([0, 90, 0]) cylinder(d = ins_d, h = 8 + fudge, $fn = 32);
    // 背面ケーブル溝 ×2 (幅 10 × 深 8、z -17..182) + 口の 45° 面取り
    for (s = [-1, 1]) {
        translate([s*gr_cx - gr_w/2, py_y1 - fudge, frame_z0 - fudge]) cube([gr_w, gr_d + fudge, gr_z1 - frame_z0 + fudge]);
        cd45 = gr_ch * sqrt(2);
        for (sx = [-1, 1])
            translate([s*gr_cx + sx*gr_w/2, py_y1, frame_z0 - fudge]) rotate([0, 0, 45])
                translate([-cd45/2, -cd45/2, 0]) cube([cd45, cd45, gr_z1 - frame_z0 + 2*fudge]);
    }
    // 結束スロット (5.5 × 3、溝底 → チャンネル内面 / 空洞)
    for (s = [-1, 1], z = tie_z)
        translate([s*gr_cx - tie_w/2, gr_y0 - fudge, z - tie_h/2]) cube([tie_w, bw_y1 - gr_y0 + 2, tie_h]);
    // HP1 (座面 z218.5、中心 (0,-85)) + ペデスタル縦ケーブル穴 Ø12 ×2
    translate([0, hp1_cy, ped_z1]) hp40_cut(cable = true, through_t = hp1_thru, insert_h = hp_ins_h);
    for (s = [-1, 1])
        translate([s*pcab_x, pcab_y, pcab_z0]) cylinder(d = pcab_d, h = ped_z1 - pcab_z0 + fudge, $fn = 48);
    // HP2 / HP3
    for (s = [-1, 1])
        translate([s*hp_face_x, hp_cy, hp_cz]) rotate([0, s*90, 0])
            hp40_cut(cable = true, through_t = hp_thru, insert_h = hp_ins_h);
    // ゲート側 (y>=0 かつ r<=r_out) を削る (ナックル角ブロックの角がゲート半殻に入らないように)
    intersection() {
        translate([0, 0, frame_z0 - 2*fudge]) cylinder(r = r_out, h = frame_h + 4*fudge);
        translate([-r_out - 1, 0, frame_z0 - 3*fudge]) cube([2*r_out + 2, r_out + 1, frame_h + 6*fudge]);
    }
}
