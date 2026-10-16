// =====================================================================
// child_core_frame.scad — 子機 外装 コアフレーム (ワニ顎の固定側 + 背骨)
//
// 外装フレーム再設計の「おおもとのフレーム」(R8)。以下を 1 部品に持つ:
//   - ワニ顎の固定側半殻 (y<=0)。ポケットで容器のキャップ/ドームリムを捕捉
//   - ヒンジ (アフト側ナックル ×2、child_jaw_gate の隙間に入る)
//   - ラッチ受け (M5 熱圧入インサート ×2)
//   - アフトパイロン: 側壁 ×2 + 背面壁 (t14) + 屋根
//   - HP1 ペデスタル: 屋根の上 z190..218.5、座面 (0,-85,218.5) 法線 +Z (xdcr_socket 座)
//   - HP2/HP3: パイロン側面のハードポイント (HP40 規格、法線 ±X、座面 x=±44)
//   - 背面ケーブル溝 ×2 (幅10×深8) + 結束スロット
//   - 取っ手 (背面壁の把持バー + 手穴スロット)
//   - 吊り耳ボス ×2 (child_lug / child_top_crown を M5×2 で載せる、z=218 頂面)
//   - ヒンジピン抜け止めざぐり (上アフトナックル頂面 Ø10×4)
//   - 下部ガードボス ×2 (child_guard_ring のタブを受ける、方位角 210/330)
// v1 は手設計。トポロジー最適化 (topo_opt) の結果を見て窓・リブを調整する。
//
// 座標系: 機体グローバル (チューブ軸=Z、z=0 チューブ下端、+Y=前)。本部品は y<=0 側。
// 印刷向き: このまま (+Z up、全高 235)。吊り耳を別部品化したので直立印刷でよい
//   (フープ荷重が層面内)。屋根下面とナックル間隙のみ小サポート推奨。
// 荷重 (要件書 §3 + 改善要件 C6): L1 吊り (耳ボス経由 99N×2×係数)、L2 輸送 300N 任意方向、
//   L3 把持プリロード、L5 着底 (ガードボス)。全体系 FEA はステージ 5 で実施。
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

/* [ヒンジ (gate と共有)] */
hinge_x    = -72;
hinge_y    = 10;
knu_od     = 16;
pin_d      = 5.4;
knu_h      = 30;        // ゲート側ナックル高
knu_gap    = 0.4;

/* [ラッチ受け] */
lf_x0      = 50;        // 頂部の吊り耳ボスと共用するため gate(54) より広い
lf_x1      = 72;
lf_t       = 10;        // y -10..0
latch_z    = [40, 170];
latch_hx   = 62;        // gate と同値
ins_d      = 6.4;       // M5 熱圧入インサート下穴
boss_h     = 24;
boss_t     = 18;        // ラッチボスの y 厚 (y -18..0)。ノブボルト先端逃げのため 16→18
latch_ins_h = 14;       // インサート下穴 深さ (改善要件 §3.6 ノブボルト化で 12→14)

/* [吊り耳ボス (child_lug と二重定義)] */
lug_x      = 66;        // 耳ボルト列の x (±)。上ポケット壁 (r60.9) の外に置くこと
lug_bolt_y = [-4, -16]; // 耳 M5 の y (2 本、Y 方向に並べる)
lug_boss_y = -22;       // ボスの後端
lug_boss_z = 204;       // ボス下端 (頂面 218 まで厚肉化)

/* [パイロン] */
pw_x0      = 24;        // 側壁 内面
pw_x1      = 30;        // 側壁 外面
py_y0      = -50;       // 側壁 前端 (ボアが自動で切り詰める)
py_y1      = -101;      // 背面壁 外面
bw_t       = 14;        // 背面壁 厚 (改善要件 §3.3 で t6 → t14。外面 y=-101 は不動)
bw_hw      = 36;        // 背面壁 半幅
roof_z0    = 182;
roof_z1    = 190;

/* [取っ手] */
// 背面壁が全面 t14 になったので、旧「局所 12 厚の把持ブロック」は壁そのものになった
grip_z     = [145, 175];
slot_hw    = 26;        // 手穴スロット半幅
slot_z     = [115, 145];

/* [HP1 ペデスタル (xdcr_socket 座。2026-09-04 接触検査で容器貫通が出たため嵩上げ)] */
// 旧: 屋根頂面 z190 の (0,-75) に直付け → ソケット台座 60×60 と胴 r18 が
//     シェル壁 (r58.35..64.35) / チューブ / ドーム押えリングに 3〜4mm 食い込んでいた。
ped_x      = 30;        // ペデスタル半幅 (= パイロン側壁外面)
ped_y0     = -60;       // 前端 (シェル外面 r64.35 と union、ドーム断面から 3mm 以上)
ped_y1     = -110;      // 後端 (背面壁 y-101 より 9mm 後ろ = 45° ハンチで支える)
ped_z1     = 218.5;     // HP1 座面 z (フレーム頂面 218 より 0.5 上)
hp1_cy     = -85;       // HP1 座中心 y (M5 は ±20 → y -105/-65)
dome_r_ped = 56.7;      // z=218.5 でのドーム断面半径。**仮値** (発注元指定 2026-09-04)
pcab_d     = 12;        // ペデスタル縦ケーブル穴 Ø (背面溝 → 座面)
pcab_x     = 18;        // 縦穴 x (±) = 背面溝と同じ
pcab_y     = -92;       // 縦穴 y。指示の -97 だと HP1 インサート (±20,-105) と 0.95mm 干渉する
pcab_z0    = 174;       // 縦穴 下端 (溝の中)
hau_y0     = -83;       // 屋根ハンチの後端 (縦穴 y-98..-86 を避ける。旧 -100)

/* [HP2/HP3 パイロン側面ハードポイント (改善要件 §3.1 HP40)] */
// 値は scad/lib/hardpoint.scad 由来 (use なので定数は見えない → ここに再掲)
hp_face_x  = 44;        // 座面 x (±)、法線 ±X
hp_cy      = -75;       // 座中心 y (HP1 と同じ y)
hp_cz      = 100;       // 座中心 z
hp_pitch   = 40;        // HP_PITCH  (M5 ±20)
hp_ins_h   = 8;         // HP_INSERT_H (実掘り深さは +1 = 9)
hp_ins_d   = 6.4;       // HP_INSERT_D
hp_cable_d = 14;        // HP_CABLE_D
hp_x0      = 30;        // 座ブロック 内側 x = パイロン側壁外面
hp_y0      = -50;       // 座ブロック 前端
hp_y1      = -101;      // 座ブロック 後端 (背面壁外面と面一)
hp_z0      = 72;
hp_z1      = 128;
hp_ch      = 5;         // 内前角の 45° 面取り (チューブ内腔 r58.35 を避ける)

/* [背面ケーブル溝 ×2 (改善要件 §3.3)] */
gr_cx      = 18;        // 溝中心 x (±)
gr_w       = 10;        // 溝幅
gr_d       = 8;         // 溝深さ (y -101 → -93)
gr_ch      = 1;         // 溝口の 45° 面取り (側壁足 x=24 に当てないため 1mm)
tie_z      = [0, 30, 60, 90, 155];  // 結束スロット中心 z
tie_w      = 5.5;       // 結束スロット 幅 (x)
tie_h      = 3;         // 結束スロット 高さ (z)

/* [ヒンジピン抜け止めざぐり (改善要件 §3.7)] */
cb_d       = 10;        // ざぐり Ø
cb_h       = 4;         // ざぐり深さ

/* [下部ガードボス (child_guard_ring と二重定義)] */
gb_az      = [210, 330];
gb_r1      = 70;        // ボス外面 = ガードタブ内面
gb_w       = 34;        // 接線方向幅 → 方位角に換算
gb_z0      = -14;
gb_z1      = 10;
gb_m5_z    = [-9, 4];

/* [窓 (アフト側、パイロン空洞に開く)] */
win_az     = [225, 315];
win_zb     = [[12, 100], [108, 178]];   // topo 反映: 上下へ延長
win_w      = 28;

/* [トポロジー最適化の反映 (2026-08-02, topo/ の密度マップ)] */
// ラッチ板の中抜き (ボス z 帯 28..52 / 158..182 は残す)。
// ヒンジ板は径方向幅 ~6mm しかないので抜かない (密度マップの暗部はボア隣接ボクセル)
lfw_x      = [56, 66];
lfw_zb     = [[62, 148]];
// パイロン側壁の中抜き ×2/壁 (壁 y -50..-101 の中央部)
// v4: 背面壁 t14 化で後端を -81 へ、HP2/3 座ブロック (z 72..128) を避けて z 帯を移動
pww_y      = [-81, -59];
pww_zb     = [[28, 70], [130, 168]];
pww_ch     = 10;        // 窓四隅の 45° 面取り

/* [Hidden] */
fudge = 0.01;
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
// ゲート側ナックル: z [-17..13], [85.5..115.5], [188..218] → アフトは隙間 2 つ
gknu_zc  = [frame_z0, (frame_z0+frame_z1)/2 - knu_h/2, frame_z1 - knu_h];
aknu     = [[gknu_zc[0] + knu_h + knu_gap, gknu_zc[1] - knu_gap],
            [gknu_zc[1] + knu_h + knu_gap, gknu_zc[2] - knu_gap]];
gb_haz   = asin((gb_w/2) / ((r_out + gb_r1)/2)) ; // ガードボス半角 (~14.6°)
bw_y1    = py_y1 + bw_t;                        // 背面壁 内面 y = -87
gr_y0    = py_y1 + gr_d;                        // 溝底 y = -93
gr_x0    = gr_cx - gr_w/2;                      // 13
gr_x1    = gr_cx + gr_w/2;                      // 23
// HP 座ブロックの内前角 45° 面取り面: s*x - y = hp_cut_c (原点からの距離 hp_cut_c/sqrt2)
hp_cut_c = hp_ch + hp_x0 - hp_y0;               // 85
hp_cut_u = hp_cut_c / sqrt(2);                  // 60.10
hp_iy    = [hp_cy - hp_pitch/2, hp_cy + hp_pitch/2];   // -95 / -55
hp_iz    = [hp_cz - hp_pitch/2, hp_cz + hp_pitch/2];   //  80 / 120
hp_thru  = hp_face_x - pw_x0 + 2;               // 中央 Ø14 を空洞 (x<24) まで貫通
cb_z     = aknu[1][1];                          // 上アフトナックル頂面 z = 187.6
ped_z0   = roof_z1;                             // ペデスタル下端 = 屋根上面 190
ped_hz0  = ped_z0 - (abs(ped_y1) - abs(py_y1)); // 45° ハンチ下端 = 181 (9mm を 45°)
hp1_iy   = [hp1_cy - hp_pitch/2, hp1_cy + hp_pitch/2]; // -105 / -65
hp1_thru = ped_z1 - roof_z0 + 1;                // 中央 Ø14 を屋根下 (空洞) まで貫通

// ---- 検査 -------------------------------------------------------------
assert(r_in < cap_od/2 - 1.0 && r_in < dome_ring_od/2 - 1.0, "リップの掛かり不足");
assert(sqrt(lug_x*lug_x + pow(min([for (y = lug_bolt_y) abs(y)]), 2)) - ins_d/2
       > pkt_r + 1.5, "耳ボス M5 が上ポケットの壁に食い込む (壁 < 1.5mm)");
assert(lug_x - ins_d/2 >= lf_x0 + 2 && lug_x + ins_d/2 <= lf_x1 - 2,
       "耳ボス M5 の x 端距離不足");
assert(min(lug_bolt_y) - ins_d/2 >= lug_boss_y + 2, "耳ボス M5 の y 端距離不足");
assert(latch_z[0] > gb_z1 + boss_h/2 + 4,   "ラッチ下ボスがガードボスに掛かる");
assert(pw_x1 < r_in,                        "パイロン側壁が把持面より広い");
assert(bw_hw >= pw_x1 + 4,                  "背面壁が側壁を覆えない");
assert(slot_hw <= bw_hw - 6,                "手穴が背面壁からはみ出す");
assert(grip_z[0] == slot_z[1],              "把持バーはスロット直上に置く");
assert(bw_t >= gr_d + 6, "(c) 溝底の残り壁 < 6mm");
assert(roof_z0 > win_zb[1][1] + 2,          "上窓が屋根を削る");
win_half = asin(win_w/2/r_in);
assert(min(win_az) - win_half > 208 + 2 && max(win_az) + win_half < 332 - 2,
       "窓が側壁とシェルの接合線 (方位角 ~208/332) を削る");
assert(min(win_az) + win_half < 242 - 2 && max(win_az) - win_half > 298 + 2,
       "窓がパイロン側壁 (方位角 ~242..250 / 290..298) を削る");
assert(gb_z1 < win_zb[0][0], "ガードボスが下窓に掛かる (z)");
// ---- v4 追加フィーチャの検査 ----
// (a) HP2/3 座ブロックがチューブ内腔 (EVA 面 r_in) に侵入しない
assert(hp_cut_u >= r_in + 1.0, "(a) HP 座ブロックの面取り面がチューブ内腔に近すぎる");
assert(sqrt(pow(hp_x0 + hp_ch, 2) + pow(hp_y0, 2)) >= r_in + 1.0 &&
       sqrt(pow(hp_x0, 2) + pow(hp_y0 - hp_ch, 2)) >= r_in + 1.0,
       "(a) HP 座ブロックの内前角がチューブ内腔に侵入");
assert(hp_x0 >= pw_x1, "HP 座ブロックがパイロン側壁とつながらない");
assert(hp_face_x - hp_thru < pw_x0, "HP 中央 Ø14 がパイロン空洞に届かない");
assert(min([for (y = hp_iy) abs(y)]) - hp_ins_d/2 >= abs(hp_y0) + 1.5 &&
       abs(hp_y1) - max([for (y = hp_iy) abs(y)]) - hp_ins_d/2 >= 1.5,
       "HP インサート穴が座ブロックの y 端を破る");
assert(min(hp_iz) - hp_ins_d/2 >= hp_z0 + 2 && max(hp_iz) + hp_ins_d/2 <= hp_z1 - 2,
       "HP インサート穴が座ブロックの z 端を破る");
assert(hp_face_x - hp_ins_h - 1 >= hp_x0 + 2,
       "HP インサート下穴の底が座ブロックを抜ける");
// (b) 結束スロットと取っ手の手穴の z 距離 >= 8
assert(min([for (z = tie_z) (z + tie_h/2 <= slot_z[0])
                            ? slot_z[0] - (z + tie_h/2)
                            : (z - tie_h/2) - slot_z[1]]) >= 8,
       "(b) 結束スロットが取っ手の手穴に 8mm 以内まで近づく");
assert(gr_x1 + gr_ch <= pw_x0, "溝口の面取りがパイロン側壁の足を削る");
assert(gr_x1 + gr_ch <= bw_hw - 4, "溝が背面壁の x 端からはみ出す");
assert(gr_x0 - gr_ch > 0, "左右の溝が中央で合流する");
assert(tie_w <= gr_w - 2 && min(tie_z) - tie_h/2 > frame_z0 &&
       max(tie_z) + tie_h/2 < roof_z0 - 4, "結束スロットが溝の外へ出る");
// HP1 ペデスタル
assert(abs(ped_y0) - dome_r_ped >= 3.0, "ペデスタル前端が z218.5 のドーム断面に 3mm 以内");
assert(sqrt(pow(hp_pitch/2, 2) + pow(ped_y0, 2)) <= r_out,
       "HP1 前列インサートの前がシェル (r_out) で裏打ちされない");
assert(min([for (y = hp1_iy) abs(y)]) - hp_ins_d/2 - abs(ped_y0) >= 1.5 &&
       abs(ped_y1) - max([for (y = hp1_iy) abs(y)]) - hp_ins_d/2 >= 1.5,
       "HP1 インサートとペデスタル y 端の残り肉不足");
assert(ped_x - hp_pitch/2 - hp_ins_d/2 >= 2, "HP1 インサートとペデスタル x 端の残り肉不足");
assert(ped_x <= lf_x0 - 4 && ped_x <= bw_hw, "ペデスタルが吊り耳ボス/背面壁からはみ出す");
assert(ped_z1 > frame_z1 && ped_z0 == roof_z1, "ペデスタルの z 位置が不正");
assert(ped_z0 - ped_hz0 == abs(ped_y1) - abs(py_y1), "ペデスタル後端ハンチが 45° でない");
assert(ped_hz0 > max(tie_z) + tie_h/2 + 4 && ped_hz0 < ped_z0,
       "ハンチ下端が背面壁の外 (or 最上段の結束スロットに掛かる)");
// ペデスタル縦ケーブル穴 Ø12 ×2
assert(sqrt(pow(pcab_x - hp_pitch/2, 2) + pow(pcab_y - min(hp1_iy), 2))
       >= pcab_d/2 + hp_ins_d/2 + 2, "縦穴と HP1 後列インサートの残り肉 < 2mm");
assert(sqrt(pow(pcab_x, 2) + pow(pcab_y - hp1_cy, 2)) >= pcab_d/2 + hp_cable_d/2 + 2,
       "縦穴と HP1 中央 Ø14 の残り肉 < 2mm");
assert(pcab_x + pcab_d/2 <= ped_x - 4 && pcab_x - pcab_d/2 >= 4,
       "縦穴がペデスタルの x 端/中心に近すぎる");
assert(abs(pcab_y) + pcab_d/2 <= abs(ped_y1) - 4, "縦穴がペデスタル後端に近すぎる");
assert(pcab_y - pcab_d/2 <= gr_y0 && pcab_y + pcab_d/2 > bw_y1,
       "縦穴が背面溝とパイロン空洞をつないでいない");
assert(pcab_z0 < roof_z0 - 4 && pcab_z0 > max(tie_z) + tie_h/2,
       "縦穴の下端が背面溝の中にない");
assert(hau_y0 >= pcab_y + pcab_d/2 + 2, "屋根ハンチが縦穴に掛かる");
// (d) ヒンジピン抜け止めざぐりの残り壁
assert((knu_od - cb_d)/2 >= 3, "(d) ざぐり周りのナックル壁厚 < 3mm");
assert(cb_d > pin_d + 2 && cb_h + 6 <= aknu[1][1] - aknu[1][0],
       "(d) ざぐりがナックル高さに対して深すぎる");
// HP 座ブロックと側壁窓の z 干渉
assert(pww_zb[0][1] + 2 <= hp_z0 && pww_zb[1][0] - 2 >= hp_z1,
       "側壁窓が HP2/3 座ブロックに掛かる (窓が塞がれる)");
assert(pww_ch*2 <= (pww_y[1] - pww_y[0]) - 2 &&
       pww_ch*2 <= min([for (zb = pww_zb) zb[1] - zb[0]]) - 2,
       "側壁窓の 45° 面取りが窓を食い尽くす");
// ラッチインサート (ノブボルト化)
assert(boss_t - latch_ins_h >= 4, "ラッチインサート穴の底の残り肉 < 4mm");
// topo 反映カットの検査
assert(lfw_zb[0][0] - latch_z[0] - boss_h/2 >= 8 &&
       latch_z[1] - boss_h/2 - lfw_zb[0][1] >= 8, "ラッチ板窓がボスに近すぎる");
assert(lfw_x[0] >= lf_x0 + 2 && lfw_x[1] <= lf_x1 - 4, "ラッチ板窓の x 端距離不足");
assert(pww_y[0] >= py_y1 + bw_t + 6 && pww_y[1] <= py_y0 - 8,
       "側壁窓が背面壁/前端に近すぎる");
assert(pww_zb[1][1] <= roof_z0 - 12, "側壁上窓が屋根ハンチに近すぎる");
assert(pww_zb[0][0] >= frame_z0 + 30, "側壁下窓が下ポケット帯に近すぎる");
echo(str("frame z ", frame_z0, "..", frame_z1, " / アフトナックル z ", aknu));
echo(str("HPTABLE HP1 (0,", hp1_cy, ",", ped_z1, ") n=+Z / HP2 (", hp_face_x, ",", hp_cy,
         ",", hp_cz, ") n=+X / HP3 (", -hp_face_x, ",", hp_cy, ",", hp_cz, ") n=-X"));
echo(str("PEDESTAL x +-", ped_x, " y ", ped_y1, "..", ped_y0, " z ", ped_z0, "..", ped_z1,
         " / haunch z ", ped_hz0, " / vcable D", pcab_d, " @ (+-", pcab_x, ",", pcab_y, ")"));
echo(str("GROOVE x +-", gr_cx, " w", gr_w, " d", gr_d, " z ", frame_z0, "..", roof_z0,
         " / tie z ", tie_z, " / counterbore z ", cb_z));

// ---- モジュール --------------------------------------------------------
module window_cut(az, z0, z1, w) {
    sd = w / sqrt(2);
    rotate([0, 0, az]) difference() {
        translate([40, -w/2, z0]) cube([40, w, z1 - z0]);
        for (s = [-1, 1])
            translate([39, s*w/2, z1]) rotate([45, 0, 0])
                translate([0, -sd/2, -sd/2]) cube([42, sd, sd]);
    }
}
// HP2/HP3 の座ブロック (s = +1 / -1)。内前角を 45° 面取りしてチューブ内腔を避ける
module hp_pad_block(s) {
    difference() {
        translate([s > 0 ? hp_x0 : -hp_face_x, hp_y1, hp_z0])
            cube([hp_face_x - hp_x0, hp_y0 - hp_y1, hp_z1 - hp_z0]);
        rotate([0, 0, -s*45])
            translate([s > 0 ? -300 : -hp_cut_u, -300, hp_z0 - 1])
                cube([300 + hp_cut_u, 600, hp_z1 - hp_z0 + 2]);
    }
}
module wedge(az0, az1, z0, h) {
    intersection() {
        rotate([0, 0, az0]) translate([0, 0, z0]) cube([200, 200, h]);
        rotate([0, 0, az1 - 90]) translate([0, 0, z0 - fudge]) cube([200, 200, h + 2*fudge]);
    }
}

// ---- 形状 --------------------------------------------------------------
difference() {
    union() {
        // 半殻 (y <= 0)
        difference() {
            translate([0, 0, frame_z0]) cylinder(r = r_out, h = frame_h);
            translate([-r_out - 1, 0, frame_z0 - fudge])
                cube([2*r_out + 2, r_out + 1, frame_h + 2*fudge]);
        }
        // ヒンジ側フランジ板 (y -8..0)
        translate([-64, -8, frame_z0]) cube([64 - r_in + 8, 8, frame_h]);
        // アフトナックル ×2 (角ブロック + 円筒、ゲートの隙間に入る)
        for (b = aknu) {
            translate([hinge_x - knu_od/2, -8, b[0]])
                cube([knu_od, hinge_y + knu_od/2 + 8, b[1] - b[0]]);
            translate([hinge_x, hinge_y, b[0]]) cylinder(d = knu_od, h = b[1] - b[0]);
        }
        // ラッチ側フランジ板 (y -10..0) + ラッチボス ×2 (y -18..0、v4 でノブボルト用に +2)
        translate([lf_x0, -lf_t, frame_z0]) cube([lf_x1 - lf_x0, lf_t, frame_h]);
        for (z = latch_z)
            translate([lf_x0, -boss_t, z - boss_h/2])
                cube([lf_x1 - lf_x0, boss_t, boss_h]);
        // 吊り耳ボス ×2 (z 204..218 を y -22..0 に厚肉化)
        translate([lf_x0, lug_boss_y, lug_boss_z])
            cube([lf_x1 - lf_x0, -lug_boss_y, frame_z1 - lug_boss_z]);
        translate([-lf_x1, lug_boss_y, lug_boss_z])
            cube([lf_x1 - lf_x0, -lug_boss_y, frame_z1 - lug_boss_z]);
        // パイロン側壁 ×2 (ボアが前端を切り詰める)
        for (s = [-1, 1])
            translate([s == 1 ? pw_x0 : -pw_x1, py_y1, frame_z0])
                cube([pw_x1 - pw_x0, py_y0 - py_y1, roof_z1 - frame_z0]);
        // 側壁の足 (t8、z -17..8) — L2 側方で下端帯に SF1.75 が出た補強
        for (s = [-1, 1])
            translate([s == 1 ? pw_x0 : -(pw_x0 + 8), py_y1, frame_z0])
                cube([8, py_y0 - py_y1, 25]);
        // 背面壁 (全高 t14。旧「取っ手ゾーンだけ 12 厚」は壁そのものに吸収)
        translate([-bw_hw, py_y1, frame_z0]) cube([2*bw_hw, bw_t, roof_z1 - frame_z0]);
        // HP2/HP3 の座ブロック ×2 (パイロン側壁外面 x=±30 → 座面 x=±44)
        for (s = [-1, 1]) hp_pad_block(s);
        // 屋根 + 下面ハンチ 45° (ブリッジ幅 48 → 28)。ハンチは縦ケーブル穴を避けて y hau_y0..
        translate([-bw_hw, py_y1, roof_z0]) cube([2*bw_hw, py_y0 - py_y1, roof_z1 - roof_z0]);
        for (sh = [-1, 1])
            translate([sh*pw_x0, hau_y0, roof_z0]) rotate([0, 45, 0])
                translate([-10*sqrt(2)/2, 0, -10*sqrt(2)/2])
                    cube([10*sqrt(2), py_y0 - 1 - hau_y0, 10*sqrt(2)]);
        // HP1 ペデスタル (屋根の上 z190..218.5)。前端はシェル外面と union
        translate([-ped_x, ped_y1, ped_z0])
            cube([2*ped_x, ped_y0 - ped_y1, ped_z1 - ped_z0]);
        // 背面壁より後ろ 9mm を支える 45° ハンチ (y+z >= ped_z0+ped_y1 の側を残す)
        difference() {
            translate([-ped_x, ped_y1, ped_hz0])
                cube([2*ped_x, py_y1 - ped_y1, ped_z0 - ped_hz0]);
            rotate([45, 0, 0]) translate([-ped_x - 1, -400, -400])
                cube([2*ped_x + 2, 400 + (ped_z0 + ped_y1)/sqrt(2), 800]);
        }
        // 下部ガードボス ×2 (シェル外面の径方向パッド)
        for (az = gb_az)
            intersection() {
                difference() {
                    translate([0, 0, gb_z0]) cylinder(r = gb_r1, h = gb_z1 - gb_z0);
                    translate([0, 0, gb_z0 - fudge]) cylinder(r = r_in, h = gb_z1 - gb_z0 + 2*fudge);
                }
                wedge(az - gb_haz, az + gb_haz, gb_z0 - fudge, gb_z1 - gb_z0 + 2*fudge);
            }
    }

    // 内腔 + ポケット + 45° コーン (gate と同一式)
    translate([0, 0, frame_z0 - fudge]) cylinder(r = r_in, h = frame_h + 2*fudge);
    translate([0, 0, pb_z0]) cylinder(r = pkt_r, h = pb_z1 - pb_z0);
    translate([0, 0, pb_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);
    translate([0, 0, pt_z0]) cylinder(r = pkt_r, h = pt_z1 - pt_z0);
    translate([0, 0, pt_z1 - fudge]) cylinder(r1 = pkt_r, r2 = r_in, h = cone_h + fudge);

    // 窓 ×4 (パイロン空洞に開く)
    for (zb = win_zb, az = win_az) window_cut(az, zb[0], zb[1], win_w);

    // ヒンジピン Ø5.4
    translate([hinge_x, hinge_y, frame_z0 - fudge])
        cylinder(d = pin_d, h = frame_h + 2*fudge, $fn = 32);

    // ラッチ M5 インサート下穴 ×2 (y=0 面から、深さ 14 — ノブボルト先端逃げ)
    // ノブ頭 (Ø16) を沈めるポケットは child_jaw_gate 側の責務。ここは通し座のみ
    for (z = latch_z)
        translate([latch_hx, -latch_ins_h, z])
            rotate([-90, 0, 0]) cylinder(d = ins_d, h = latch_ins_h + fudge, $fn = 32);

    // 吊り耳 M5 インサート下穴 ×4 (z=218 頂面から、深さ 10)
    for (sx = [-1, 1], yy = lug_bolt_y)
        translate([sx*lug_x, yy, frame_z1 - 10])
            cylinder(d = ins_d, h = 10 + 2*fudge, $fn = 32);

    // 取っ手: 手穴スロット (上角 45°) — 背面壁を貫通
    hs = 16 * sqrt(2) / 2;
    translate([0, 0, 0]) difference() {
        translate([-slot_hw, py_y1 - 1, slot_z[0]])
            cube([2*slot_hw, bw_t + 2, slot_z[1] - slot_z[0]]);
        for (s = [-1, 1])
            translate([s*slot_hw, py_y1 - 2, slot_z[1]]) rotate([0, 45, 0])
                translate([-hs/2, 0, -hs/2]) cube([hs, bw_t + 4, hs]);
    }

    // HP1 (ペデスタル頂面 z=218.5、中心 (0,-85)、法線 +Z) — xdcr_socket 座
    translate([0, hp1_cy, ped_z1])
        hp40_cut(cable = true, through_t = hp1_thru, insert_h = hp_ins_h);
    translate([0, hp1_cy, ped_z1]) hp40_arrow();
    // ペデスタル縦ケーブル穴 Ø12 ×2 (背面溝 → 屋根 → 座面。溝が屋根で塞がらないように)
    for (s = [-1, 1])
        translate([s*pcab_x, pcab_y, pcab_z0])
            cylinder(d = pcab_d, h = ped_z1 - pcab_z0 + fudge, $fn = 48);

    // ラッチ板の窓 (通し Y、四隅 45° — 角の応力集中を FEA が検出したため) — topo 反映
    for (zb = lfw_zb) {
        lsd = 8 * sqrt(2);   // 角チャンファ 8mm
        difference() {
            translate([lfw_x[0], -lf_t - 1, zb[0]])
                cube([lfw_x[1] - lfw_x[0], lf_t + 2, zb[1] - zb[0]]);
            for (sx = [0, 1], sz = [0, 1])
                translate([lfw_x[sx], -lf_t - 2, zb[sz]]) rotate([0, 45, 0])
                    translate([-lsd/2, 0, -lsd/2]) cube([lsd, lf_t + 4, lsd]);
        }
    }
    // パイロン側壁の窓 ×4 (通し X、四隅 45°) — topo 反映
    for (s = [-1, 1], zb = pww_zb) {
        psd = pww_ch * sqrt(2);  // 角チャンファ (v2 で下後角に SF1.59 が出た対策)
        difference() {
            translate([s*27 - 4, pww_y[0], zb[0]])
                cube([8, pww_y[1] - pww_y[0], zb[1] - zb[0]]);
            for (sy = [0, 1], sz = [0, 1])
                translate([s*27 - 5, pww_y[sy], zb[sz]]) rotate([45, 0, 0])
                    translate([0, -psd/2, -psd/2]) cube([10, psd, psd]);
        }
    }

    // HP2 / HP3: M5 インサート ×4 (座面 x=±44 から内向き 9) + 中央 Ø14 (空洞まで貫通)
    // hardpoint.scad の hp40_cut() をローカル +Z → ±X へ回して使う。矢印は +Y を向く
    for (s = [-1, 1]) {
        translate([s*hp_face_x, hp_cy, hp_cz]) rotate([0, s*90, 0])
            hp40_cut(cable = true, through_t = hp_thru, insert_h = hp_ins_h);
        translate([s*hp_face_x, hp_cy, hp_cz]) rotate([0, s*90, 0]) hp40_arrow();
    }

    // 背面ケーブル溝 ×2 (幅 10 × 深 8、y -101..-93、z -17..182) + 口の 45° 面取り
    for (s = [-1, 1]) {
        translate([s*gr_cx - gr_w/2, py_y1 - fudge, frame_z0 - fudge])
            cube([gr_w, gr_d + fudge, roof_z0 - frame_z0 + fudge]);
        cd45 = gr_ch * sqrt(2);
        for (sx = [-1, 1])
            translate([s*gr_cx + sx*gr_w/2, py_y1, frame_z0 - fudge]) rotate([0, 0, 45])
                translate([-cd45/2, -cd45/2, 0])
                    cube([cd45, cd45, roof_z0 - frame_z0 + 2*fudge]);
    }
    // 結束スロット (5.5 × 3、軸 Y、溝底 y-93 → パイロン空洞 y-87 を貫通)
    for (s = [-1, 1], z = tie_z)
        translate([s*gr_cx - tie_w/2, gr_y0 - fudge, z - tie_h/2])
            cube([tie_w, bw_y1 - gr_y0 + 2, tie_h]);

    // ヒンジピン抜け止めざぐり Ø10 × 4 (上アフトナックル頂面 z=187.6 から下向き)
    translate([hinge_x, hinge_y, cb_z - cb_h])
        cylinder(d = cb_d, h = cb_h + fudge, $fn = 48);

    // ゲート側 (y>=0 かつ r<=r_out) を削る — アフトナックル角ブロックの角が
    // ゲートの半殻 (x -64.3..-64.0, y 0..5.4) に食い込んでいた (2026-09-04 接触検査)
    intersection() {
        translate([0, 0, frame_z0 - 2*fudge]) cylinder(r = r_out, h = frame_h + 4*fudge);
        translate([-r_out - 1, 0, frame_z0 - 3*fudge])
            cube([2*r_out + 2, r_out + 1, frame_h + 6*fudge]);
    }

    // 下部ガード M5 インサート ×4 (ボス外面から径方向、深さ 8)
    for (az = gb_az, z = gb_m5_z)
        rotate([0, 0, az]) translate([gb_r1 - 8, 0, z])
            rotate([0, 90, 0]) cylinder(d = ins_d, h = 8 + fudge, $fn = 32);

}
