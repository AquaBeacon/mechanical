// child_vtray_rib をデッキ先端から座まで滑らせたときの掃引体積とデッキの共通部分。
// 空なら「突起に当たらずに嵌まる」。end="bot"/"top"、z1 を伸ばすとショルダーに当たる (対照)。
B = "../../../";   // Body_Models ルート (この views/ から相対)
deck = str(B, "parts/child/interior/printed/child_vtray_deck/child_vtray_deck_t200.stl");
rib  = str(B, "parts/child/interior/printed/child_vtray_rib/child_vtray_rib.stl");
end = "bot";
zext = 0;      // 対照用: 掃引をさらに伸ばす
z0 = end == "bot" ? -30 : 191.5 - zext;
z1 = end == "bot" ? 8.5 + zext : 230;
intersection() {
    import(deck);
    translate([0, 0, z0]) linear_extrude(z1 - z0)
        projection(cut = true) translate([0, 0, -3]) import(rib);
}
