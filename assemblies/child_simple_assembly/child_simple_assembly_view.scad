// =====================================================================
// child_simple_assembly_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// Simple vertical enclosure. M3 40x40 camera and TD04A interfaces; mounts added later. Dome is a provisional reference. User confirmed vertical OD114.3 x 200 on 2026-09-16.
// 座標系: X left/right; +Y front; Z up; tube bottom z=0; mm
// =====================================================================

show_vessel = true;
show_frame = true;

if (show_vessel) color("Gainsboro") translate([0, 0, -3.8]) rotate([180, 0, 0]) translate([-60.15, -57.15, 0])  import("../../parts/child/exterior/cots/wte4_end_cap_5xm10/WTE4-M-END-CAP-5XM10-R2.stl");
if (show_frame) color("SteelBlue")  import("../../parts/child/exterior/printed/child_simple_front/child_simple_front.stl");
if (show_frame) color("SeaGreen")  import("../../parts/child/exterior/printed/child_simple_rear/child_simple_rear.stl");
if (show_frame) color("DimGray")  import("../../parts/child/exterior/printed/child_simple_guard/child_simple_guard.stl");
if (show_vessel) color("LightSteelBlue", 0.6) translate([0, 0, 19]) rotate([180, 0, 0]) translate([-57.15, -57.15, 0])  import("../../parts/child/exterior/cots/wte4_flange/BR-101040_RevC.stl");
if (show_vessel) color("LightSteelBlue", 0.6) translate([0, 0, 181]) translate([-57.15, -57.15, 0])  import("../../parts/child/exterior/cots/wte4_flange/BR-101040_RevC.stl");
// 参考モデル (仮)。dome_h 要実測
if (show_vessel) color("PowderBlue", 0.35) translate([0, 0, 208])  import("../../parts/child/exterior/cots/wte4_dome_cap/wte4_dome_cap_ref.stl");
if (show_vessel) color("LightSteelBlue", 0.3) rotate([0, -90, 0]) translate([0, -57.15, -57.15])  import("../../parts/child/exterior/cots/wte4_acrylic_tube/BR-101052-200_RevB.stl");
