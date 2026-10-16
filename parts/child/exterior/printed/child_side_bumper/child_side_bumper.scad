// =====================================================================
// child_side_bumper.scad — 子機 カメラ側面バンパ (左右共通 ×2)
//
//   子機外装_改善要件 (2026-09-04) §3.2、コーディネータ 2026-09-04 決定に基づく。
//   防水ケース側面 (x=±122.35) の外側に立つ t9 の板。`child_cam_bridge` の
//   ウイング端板フランジ (x=±wing_x1) へ M5×2 で締結する。輸送時はブリッジ
//   ごと外れる (C7「外せる部品」)。左右共通形状、機体では x=+/-133.35 側に
//   同一形状をミラー配置する (placement.json の mirror で対応、本体は左側
//   (sign=-1, x<0) を基準に作る)。
//
//   規約: cube/cylinder + boolean のみ。
// =====================================================================

/* [child_cam_mount / カメラ配置 (二重定義: child_cam_mount.scad, child_cam_bridge.scad)] */
lens_x       = 75;      // レンズ中心 |x|
lens_z       = 125;     // レンズ中心 z
cam_y_shift  = 14;
lens_y       = 106 + cam_y_shift;   // 120
cm_case_d    = 45.9;    // ケース奥行 (Y)
cm_case_w    = 94.7;    // ケース幅 (横向きでは機体 X 方向、cam_mount の case_w)
cm_case_h    = 84.1;    // ケース高さ (横向きでは機体 Z 方向)
// 2026-09-04 修正: 横向きでは「ケース幅」(case_w) が機体 X。旧式は case_h/2 を
// 使っており誤り (117.05 になっていた)。child_cam_bridge.scad と同じ式に統一。
case_outer_x = lens_x + cm_case_w / 2;  // 122.35 (ケース側面 |x|)

/* [child_cam_bridge 側 (二重定義: child_cam_bridge.scad)] */
deck_top     = lens_z - 42.05 - 30;   // 52.95 (cm_lens_off_bot=42.05, cm_fin_x1=30)
deck_bot     = deck_top - 8;          // 44.95
case_z0      = deck_top + 30;         // 82.95 (register 面 = ケース底)
case_z1      = case_z0 + cm_case_h;   // 167.05 (ケース上端)
case_y0      = lens_y - cm_case_d;    // 74.1
wing_x1      = 120;      // ウイング外端 (バンパ取付フランジの機体 x)
end_plate_t  = 6;
end_plate_z1 = 80;        // 2026-09-04 修正: 端板上端 (child_cam_bridge.scad front_web_z1/end_plate_z1 と同値)
bump_bolt_y  = [80, 116];   // child_cam_bridge.scad と同値 (二重定義)
bump_bolt_z  = 65;          // z<=78 (end_plate_z1-2) に収める — 両ファイルで同値

/* [バンパ本体] */
bumper_t   = 9;      // 板厚 (X 方向、立て壁部)
case_gap   = 2;       // ケース側面とのクリアランス
top_margin = 5;       // ケース上端 + 5 まで覆う
bot_margin = case_z0 - deck_bot; // バンパ下端はデッキ面まで (フランジ締結のため)
y_margin   = 5;        // ケース前後 +5 ずつ

/* [L 形フット (2026-09-04 追加): ブリッジ端板の外面 (x=wing_x1) まで内側へ
   延長し密着させる。check_asm_contacts で FLOATING (4.35mm 浮き) が検出された
   ため追加した。ケース底面 (case_z0=82.95) より下の帯のみ (ケースと干渉しない)。] */
foot_z1 = 78;   // フット上端。end_plate_z1(80) の 2mm 手前、ケース底面よりずっと下

/* [締結: M5×2、ブリッジ端板フランジへ。バンパ側は通し穴+皿ざぐり、
   ブリッジ側 (child_cam_bridge.scad) がナットトラップを持つ] */
m5_clear = 5.4;
head_d   = 9.5;   // M5 皿/丸頭の逃げ (工具アクセス)
head_dep = 4.0;

/* [機体レベル検査] */
env_half = 140;   // 280/2

/* [Hidden] */
fudge = 0.01;
$fn = 48;

// ---- 導出値 -----------------------------------------------------------
inner_x = case_outer_x + case_gap;      // 124.35 (バンパ内面)
outer_x = inner_x + bumper_t;           // 133.35 (バンパ外面)
z0      = deck_bot;                      // 44.95 (下端、フランジで締結)
z1      = case_z1 + top_margin;         // 172.05 (上端)
y0      = case_y0 - y_margin;           // 69.1
y1      = lens_y + y_margin;            // 125

// ---- 干渉・成立性チェック -----------------------------------------------
assert(inner_x - case_outer_x >= case_gap - 1e-6, "ケース側面とのクリアランス不足");
assert(outer_x <= env_half, "バンパ外面が 280 枠 (半幅140) を超える");
assert(z0 <= deck_bot + 1e-6, "バンパ下端がブリッジデッキ面より高い (締結フランジに届かない)");
assert(z1 >= case_z1 + top_margin - 1e-6, "バンパ上端がケース上端+5 未満");
for (by = bump_bolt_y) {
    assert(by >= y0 + 3 && by <= y1 - 3,
           "バンパ締結穴がバンパ端から 3mm 未満");
}
assert(bump_bolt_z >= z0 + 5 && bump_bolt_z <= end_plate_z1 - 2,
       "バンパ締結穴がブリッジ端板フランジの高さ範囲 (z<=end_plate_z1-2=78) の外");
// フットがブリッジ端板の外面 (x=wing_x1) まで密着して届くこと (旧: inner_x=124.35
// までしかなく wing_x1=120 との間に 4.35mm の隙間があり FLOATING だった)
assert(inner_x > wing_x1, "フットが端板の外面 (wing_x1) まで届かない");
// フットはケース底面 (case_z0) より 1mm 以上下 (ケースと干渉しない。x 方向は
// フット (~120..133.35) とケース (~27.65..122.35) が 120..122.35 で重なるが、
// z 方向を分離することで回避する)
assert(foot_z1 <= case_z0 - 1, "フットがケース底面に 1mm 未満で接近/食い込む");
assert(foot_z1 > z0, "フット高さが 0 以下");

echo(str("バンパ x = ", inner_x, " .. ", outer_x, " (外面 ", outer_x, " <= ", env_half, ")"));
echo(str("バンパ y = ", y0, " .. ", y1, "  z = ", z0, " .. ", z1));
echo(str("フット x = ", wing_x1, " .. ", outer_x, " (端板外面 wing_x1=", wing_x1,
         " に密着) z = ", z0, " .. ", foot_z1));

// ---- 形状 (左側基準: x < 0 側。機体では child_cam_bridge の左ウイングに
//      沿わせる。右側は placement.json で mirror = [1,0,0] を掛ける) ----
module bumper_solid() {
    // メインの立て壁 (ケース側面ガード、全高)
    translate([-outer_x, y0, z0])
        cube([outer_x - inner_x, y1 - y0, z1 - z0]);
    // L 形フット (ケース底面より下の帯のみ。ブリッジ端板の外面 x=wing_x1 まで
    // 内側へ延長して密着させる — 2026-09-04 追加、FLOATING 修正)
    translate([-outer_x, y0, z0])
        cube([outer_x - wing_x1, y1 - y0, foot_z1 - z0]);
}

module bumper_holes() {
    // 通し穴 + 頭の逃げは、フット追加後は外面から端板外面 (wing_x1) まで
    // 全長を貫通させる (旧: 立て壁の厚み分 (9mm) しか貫通していなかった)
    full_h = outer_x - wing_x1;   // 13.35 (外面から端板外面まで)
    for (by = bump_bolt_y) {
        // 通し穴 (軸 X)
        translate([-outer_x - fudge, by, bump_bolt_z])
            rotate([0, 90, 0])
                cylinder(d = m5_clear, h = full_h + 2 * fudge, $fn = 32);
        // 頭の逃げ (外面側)
        translate([-outer_x - fudge, by, bump_bolt_z])
            rotate([0, 90, 0])
                cylinder(d = head_d, h = head_dep + fudge, $fn = 32);
    }
}

difference() {
    bumper_solid();
    bumper_holes();
}
