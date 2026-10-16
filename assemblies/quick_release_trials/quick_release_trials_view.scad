// =====================================================================
// quick_release_trials_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// A/C M3x40 thumb bolts and recessed nuts; C cam draws 0.60 mm over 60 degrees, upper plane Z24.5; two 5x8x1.0 mm rubber pads retained in 0.4 mm deep male-lid pockets (5.4x8.4), nominal compression 0.10 mm. Rubber/metal not printed. No load rating.
// 座標系: mm, Z up; A at X=-55, B at X=0, C at X=55
// =====================================================================

color("SlateGray") translate([-55, 0, 0])  import("../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes_slide_female.stl");
color("Orange") translate([-55.5, 0, 25]) rotate([180, 0, 0])  import("../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes_slide_male.stl");
color("SteelBlue") translate([-55, 0, 0])  import("../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes_slide_gib.stl");
color("SeaGreen") translate([-36.5, 0, 12]) rotate([0, 90, 0])  import("../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes_knob.stl");
color("SlateGray")  import("../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes_snap_female.stl");
color("Orange") translate([0, -0.15, 3.3])  import("../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes_snap_male.stl");
color("SlateGray") translate([55, 0, 0])  import("../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes_twist_female.stl");
color("Orange") translate([55, 0, 24.5]) rotate([180, 0, 0])  import("../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes_twist_male.stl");
color("SeaGreen") translate([75.5, 0, 14]) rotate([0, 90, 0])  import("../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes_twist_knob.stl");
