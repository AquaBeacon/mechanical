// =====================================================================
// dji_style_toggle_latch_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// Fixed host spacing. Positive hook undercut and EPDM preload. Rubber model is the closed envelope, not printable or a deformation simulation.
// =====================================================================

show_printed = true;
show_hardware = true;

if (show_printed) color("SlateGray") translate([0, 0, 0]) rotate([0, 0, 0])  import("../../parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch_base.stl");
if (show_printed) color("SteelBlue") translate([26, 0, 0]) rotate([0, 0, 0])  import("../../parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch_keeper.stl");
if (show_hardware) color("SeaGreen") translate([26, 0, 0]) rotate([0, 0, 0])  import("../../parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch_epdm.stl");
if (show_printed) color("Orange") translate([0, -9.2, 10.5]) rotate([0, -185, 0])  import("../../parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch_link.stl");
if (show_printed) color("Orange") translate([0, 4.4, 10.5]) rotate([0, -185, 0])  import("../../parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch_link.stl");
if (show_printed) color("DimGray") translate([-11.9543, 0, 9.45413]) rotate([0, 1.44005, 0])  import("../../parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch_lever.stl");
if (show_hardware) color("Silver") translate([0, 0, 10.5]) rotate([0, 0, 0])  import("../../parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch_axle_a.stl");
if (show_hardware) color("Silver") translate([-11.9543, 0, 9.45413]) rotate([0, 0, 0])  import("../../parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch_axle_b.stl");
