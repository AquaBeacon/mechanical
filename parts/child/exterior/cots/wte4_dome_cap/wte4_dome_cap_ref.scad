// =====================================================================
// wte4_dome_cap_ref.scad — WTE4 4in アクリルドーム **参考モデル (仮)**
//
// これは購入品の代用モデル。メーカー公称値 (内R43.5 / 肉厚3.75 / M3x12) から
// 起こしたもので、**押えリングの厚み・差込み深さ・球心位置は未確認**。
// 実物入手後にベンダ配布の STEP へ差し替えること。
//
// ファイル名を意図的にフォルダ名と変えてある → build.ps1 のビルド対象外。
// 更新するときは手動で:
//   openscad -o <abs>/wte4_dome_cap_ref.stl <abs>/wte4_dome_cap_ref.scad
//
// 座標系: 軸 = Z、z=0 が押えリングの座面 (= フランジ上面に当たる面)。
// =====================================================================

ring_od   = 114.3;   // 押えリング OD (**要確認**。child_shell_aft の dome_ring_od)
ring_h    = 6;       // 座面から上に出るリングの高さ (**要確認**)
plug_d    = 88;      // フランジ貫通口へ差し込むプラグ Ø (**要確認**)
plug_h    = 4.2;     // 同 深さ (**要確認**)
dome_ir   = 43.5;    // ドーム内半径 (メーカー公称)
dome_t    = 3.75;    // ドーム肉厚 (メーカー公称)

$fn = 96;

dome_or = dome_ir + dome_t;          // 47.25
apex    = ring_h + dome_or;          // 座面からドーム頂点まで = 53.25

difference() {
    union() {
        cylinder(d=ring_od, h=ring_h);              // 押えリング
        translate([0,0,-plug_h]) cylinder(d=plug_d, h=plug_h);   // プラグ
        translate([0,0,ring_h]) difference() {      // ドーム (半球シェル)
            sphere(r=dome_or);
            sphere(r=dome_ir);
            translate([-100,-100,-100]) cube([200,200,100]);     // 下半分を落とす
        }
    }
    translate([0,0,-plug_h-1]) cylinder(d=2*dome_ir, h=plug_h+ring_h+2);  // 内腔
}

echo(str("座面からの高さ (= dome_h) = ", apex, " / プラグ深さ ", plug_h));
