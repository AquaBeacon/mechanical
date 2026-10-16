// =====================================================================
// foam_pad.scad — 独立気泡フォーム パッド 簡易モデル (購入品・切り出し)
//
// LiPo をベイの中で拘束するための発泡パッド。剛体 (PLA) で挟むと LiPo の膨張と
// 振動を逃がせないので、ここだけは 3D プリント部品ではなくフォームにする。
// 印刷対象ではない。シート (EPDM/PE 独立気泡、3mm / 2mm / 1.5mm 厚) から切る。
//
// 原点: 底面中心。l = X、w = Y、t = +Z (厚み)。
// =====================================================================

/* [寸法] */
l = 100;   // 長さ (X)
w = 34;    // 幅 (Y)
t = 3;     // 厚み (Z)

assert(l > 0 && w > 0 && t > 0, "寸法が不正");

service_cut=false;
difference(){
 translate([-l/2,-w/2,0]) cube([l,w,t]);
 // AF5.5 nut corners need a 3.4 mm radial envelope (old round boss: R3.1).
 if(service_cut) translate([38,-13,4.5]) rotate([-90,0,0]) cylinder(r=3.4,h=6,$fn=48);
}

echo(str("foam_pad ", l, " x ", w, " x ", t));
