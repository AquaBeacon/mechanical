// =====================================================================
// test_bracket.scad - 動作確認用サンプル (Fusion360 編集向けクリーン版)
// L字ブラケット + M3 取付穴。基本形状(cube/cylinder)とブーリアンのみで構成し、
// STEP に変換したとき真の平面・円柱面になる = Fusion360 で選択・編集しやすい。
// 角丸/フィレットはあえて入れない -> 必要なら Fusion 側で追加する。
// F5 プレビュー / F6 レンダリング / STL 書き出し。
// =====================================================================

/* [基本寸法] */
plate_w  = 40;   // 底板の幅 (X)
plate_d  = 30;   // 底板の奥行 (Y)
wall_h   = 30;   // 立ち上がり壁の高さ (Z)
thick    = 4;    // 板厚

/* [取付穴] */
screw_d  = 3.2;  // M3 クリアランス穴 (公称3.0 + 0.2)
hole_inset = 7;  // 端からの穴中心距離 (X)

/* [補強リブ] */
gusset_run  = 14;  // リブが底板を這う長さ (Y)
gusset_rise = 20;  // リブが壁を這う高さ (Z)

/* [干渉チェック] */
clearance = 1.0;   // 穴とリブの間に最低限空ける隙間 (mm)

$fn = 64;          // 穴の分割数 (FreeCAD は cylinder を真円柱として復元)

// --- 位置(パラメータから導出) ------------------------------------------
hole_x   = [hole_inset, plate_w - hole_inset];   // 取付穴の X 位置 (底板・壁 共通)
gusset_x = [plate_w * 0.5 - 5, plate_w * 0.5 + 5]; // リブの X 中心 (中央寄り=穴を避ける)

// --- 干渉チェック: 壁穴とリブが X で重なっていないか ---------------------
// リブ半幅 + 穴半径 + clearance より近い穴があればビルドを止める。
min_dx = thick/2 + screw_d/2 + clearance;
for (hx = hole_x) for (gx = gusset_x)
    assert(abs(hx - gx) >= min_dx,
           str("干渉: 壁の取付穴 x=", hx, " と補強リブ x=", gx,
               " が近すぎます (必要間隔 ", min_dx, "mm)。",
               "hole_inset か gusset_x を調整してください。"));

// --- 部品 --------------------------------------------------------------
module gusset(cx) {
    // YZ 平面の直角三角形を X 方向へ thick 押し出し、内側コーナーへ
    translate([cx - thick/2, thick, thick])
        rotate([90, 0, 90])
            linear_extrude(height = thick)
                polygon([[0, 0], [gusset_run, 0], [0, gusset_rise]]);
}

difference() {
    union() {
        cube([plate_w, plate_d, thick]);          // 底板 (水平)
        cube([plate_w, thick, wall_h]);           // 立ち上がり壁 (Y=0 側)
        for (gx = gusset_x) gusset(gx);           // 補強リブ
    }

    // 底板の取付穴 (奥側)
    for (x = hole_x)
        translate([x, plate_d - hole_inset, -0.5])
            cylinder(d = screw_d, h = thick + 1);

    // 壁面の取付穴
    for (x = hole_x)
        translate([x, thick + 0.5, wall_h - hole_inset])
            rotate([90, 0, 0]) cylinder(d = screw_d, h = thick + 1);
}
