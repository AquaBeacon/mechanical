B = "../../../";   // Body_Models ルート (この views/ から相対)
deck = str(B, "parts/child/interior/printed/child_vtray_deck/child_vtray_deck_t200.stl");
rib  = str(B, "parts/child/interior/printed/child_vtray_rib/child_vtray_rib.stl");
scr  = str(B, "parts/common/interior/cots/screw/screw_m2_5x6.stl");
mode = "bot_exploded";   // bot_exploded / bot_seated / top_seated
bot = mode != "top_seated";
zc  = bot ? [-40, 45] : [155, 240];
rib_z = bot ? 2.5 : 191.5;
scr_z = bot ? 0 : 200;
dz  = mode == "bot_exploded" ? -16 : 0;
color("Orange", 1) intersection() { import(deck); translate([-60, -60, zc[0]]) cube([120, 120, zc[1] - zc[0]]); }
color("SteelBlue", mode == "bot_exploded" ? 0.7 : 1) translate([0, 0, rib_z + dz]) import(rib);
if (mode != "bot_exploded") color("Silver", 1) translate([0, -6, scr_z]) rotate([-90, 0, 0]) import(scr);
