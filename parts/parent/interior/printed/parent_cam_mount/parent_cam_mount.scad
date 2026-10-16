// =====================================================================
// parent_cam_mount.scad — GS カメラ (M12 レンズ) 下向き保持フレーム (p2)
//
// 役割: RPi Global Shutter Camera (38 角) を**レンズ下向き**で parent_plate
//   (p2) のビューポート開口 Ø36 の上に保持する。カメラ基板は本フレームの
//   上面に載り、M12 ホルダ台座 (22 角 ×12) とレンズ (Ø17) が中央開口と
//   プレート開口を通って下へ伸びる。
// 固定: プレートへ M3×25 なべ ×4 (脚 Ø7.5 h15 を貫通してプレートの下穴 Ø2.6 に
//   セルフタップ。parent_plate cam_h, 正方ピッチ cam_hole_sq=44 = 本ファイル foot_sq)。
//   カメラは M2.5 セルフタップ ×4 (穴ピッチ cam_pitch=34 仮)。基板は 0.3
//   クリアランスのポケット (リム h1.5) で位置決め。
// 高さ: 脚 15 + フレーム t3 → カメラ基板下面 = プレート上面 + 18 (z=36.8 箱底外面基準)、
//   レンズ前面 = 基板下面 - 28 = z≈8.8 (箱床上面 3.8 から 5mm。窓部品
//   parent_cam_port 未設計のため要確認)。
// 印刷向き: 平置き (+Z 上)。サポート不要。PETG / インフィル 30%。
// =====================================================================

/* [カメラ (gs_camera_m12 と二重定義)] */
cam_sq     = 38;      // 基板外形
cam_pitch  = 34;      // 取付穴ピッチ (仮値 — 公式図面/実測で確定)
cam_hole_d = 2.6;     // 基板穴 (M2.5)
base_sq    = 22;      // M12 ホルダ台座
lens_d     = 17;

/* [フレーム] */
t          = 3;       // フレーム厚
rim_h      = 1.5;     // 基板位置決めリム
rim_w      = 2.5;
pocket_clr = 0.3;     // 基板ポケット片側クリアランス
open_sq    = 27;      // 中央開口 (台座 22 + 片側 2.5)

/* [プレート固定 (parent_plate cam_hole_sq / cam_pilot と二重定義)] */
foot_sq    = 44;      // 4 穴の正方ピッチ
foot_d     = 3.4;     // M3 通し穴 (なべ小ねじ M3×8 → プレート下穴 Ø2.6 にセルフタップ)
foot_pad   = 9;       // 足まわりの肉 (穴中心から外縁まで)
head_clr   = 7;       // ねじ頭 (なべ M3 Ø5.5) の座: リムの角をこの径で抜く
leg_d      = 7.5;     // 脚径 (parent_plate cam_leg_d と二重定義。TX ボスとの離隔で決まる)
leg_h      = 15;      // 脚高さ (カメラ基板下面 = プレート上面 + leg_h + t)

/* [カメラねじ] */
cam_pilot  = 2.0;     // M2.5 セルフタップ下穴 (t3 に 3 山)

$fn = 48;

// ---- 導出 -----------------------------------------------------------
pocket = cam_sq + 2*pocket_clr;                 // 38.6
outer  = max(pocket + 2*rim_w, foot_sq + 2*foot_pad);   // 62
foot_h = [for (u = [-1, 1], v = [-1, 1]) [u*foot_sq/2, v*foot_sq/2]];
cam_h  = [for (u = [-1, 1], v = [-1, 1]) [u*cam_pitch/2, v*cam_pitch/2]];

// ---- 成立性チェック --------------------------------------------------
assert(open_sq > base_sq + 2, "中央開口が M12 台座に対して狭い");
assert(open_sq > lens_d + 2, "中央開口がレンズに対して狭い");
// カメラ穴と中央開口の肉 (穴縁 → 開口縁)
assert(cam_pitch/2 - cam_hole_d/2 - open_sq/2 >= 1.5,
       str("カメラ穴と中央開口の肉厚不足: ", cam_pitch/2 - cam_hole_d/2 - open_sq/2));
// カメラ穴とプレート足穴 (同じ対角線上)
assert((foot_sq - cam_pitch)/2 * sqrt(2) >= cam_hole_d/2 + foot_d/2 + 2,
       "カメラ穴とプレート足穴が接近");
// 足穴のねじ頭 (Ø6) の座はリムの角を Ø head_clr で抜いて確保する。
// その抜きが基板 (ポケット内の板) に触れないこと
assert((foot_sq/2 - cam_sq/2) * sqrt(2) >= head_clr/2 + 0.5,
       "足穴のねじ頭座がカメラ基板の角に掛かる");
assert(outer/2 - foot_sq/2 >= foot_d/2 + 2, "足穴が外縁に接近");
assert(leg_d/2 - foot_d/2 >= 1.8, "脚の肉厚不足 (M3 通し穴まわり)");
assert(leg_d/2 <= foot_pad, "脚がフレーム外縁からはみ出す");

echo(str("parent_cam_mount: outer ", outer, " sq, t", t, " rim ", rim_h, " legs ", leg_d, "x", leg_h,
         "  foot_sq ", foot_sq, "  cam_pitch ", cam_pitch,
         "  cam board bottom = plate top + ", leg_h + t));

// ---- 本体 (原点 = 脚下面中心 = プレート上面のビューポート中心) -----------
translate([0, 0, leg_h]) difference() {
    union() {
        translate([-outer/2, -outer/2, 0]) cube([outer, outer, t]);
        // 脚 (フレーム下、足穴位置)
        for (h = foot_h) translate([h[0], h[1], -leg_h]) cylinder(d = leg_d, h = leg_h + 0.01);
        // 位置決めリム (ポケット外周)
        translate([-pocket/2 - rim_w, -pocket/2 - rim_w, t])
            cube([pocket + 2*rim_w, pocket + 2*rim_w, rim_h]);
    }
    // 基板ポケット
    translate([-pocket/2, -pocket/2, t]) cube([pocket, pocket, rim_h + 1]);
    // 中央開口 (台座 + レンズ)
    translate([-open_sq/2, -open_sq/2, -0.5]) cube([open_sq, open_sq, t + rim_h + 1]);
    // カメラ M2.5 下穴
    for (h = cam_h) translate([h[0], h[1], -0.5]) cylinder(d = cam_pilot, h = t + 1);
    // プレート固定 M3 通し穴 (脚を貫通) + リム角のねじ頭座
    for (h = foot_h) {
        translate([h[0], h[1], -leg_h - 0.5]) cylinder(d = foot_d, h = leg_h + t + rim_h + 1);
        translate([h[0], h[1], t]) cylinder(d = head_clr, h = rim_h + 1);
    }
    // CSI コネクタ側 (+Y) のリム切欠き (フレキ引出し)
    translate([-12, pocket/2 - 0.5, t]) cube([24, rim_w + 1, rim_h + 1]);
}
