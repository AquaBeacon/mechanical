# child_interior views (2026-09-03)

`child_interior_view.scad` を OpenSCAD で `-D show_vessel=false` で描画したもの。

| ファイル | 視点 |
|---|---|
| 01_batt_side_-Y | 電池側 (−Y) 正面 |
| 02_lcd_side_+Y | LCD / MAIN 側 (+Y) 正面 |
| 03_side_+X / 04_side_-X | 左右側面 |
| 05_from_below / 06_from_above | 下 / 上から |
| 07_iso_batt_low | 電池側 斜め下から |
| 08_iso_harness_high | −X ハーネス側 斜め上から |
| 09_close_floor_screw | 床板の皿ねじ・リード切欠き・下リブ開口の拡大 |
| 10_close_xt30_rail | +X レール溝の XT30 ペアの拡大 |
| 11_close_rx_harness | RX J2 と −X レール上端の拡大 |
| 12_close_pwr_jbat | C-PWR 上面 (J_MAIN XH9 / J_BAT ピグテール) の拡大 |
| ../_work/images/views/contact_sheet.png | 上記 12 枚の一覧 |
| 13_rib_fit_bot_exploded / 14_rib_fit_bot_seated / 15_rib_fit_top_seated | センタリングリブ (青) とデッキ先端の取合い。差し込み前 / 下側着座 (M2.5 止めねじ) / 上側着座。`rib_fit_view.scad` の `mode` で切替 |

再生成 (Git Bash、assemblies/child_interior で):

```bash
O="/c/Program Files/OpenSCAD/openscad.exe"
"$O" -D show_vessel=false -o views/01_batt_side_-Y.png --imgsize=1200,1500 --camera=0,-700,100,0,0,100 --projection=p child_interior_view.scad
# --camera=eyeX,eyeY,eyeZ,centerX,centerY,centerZ。他の視点は同じ形式で eye を変える
```

リブ取合い図と挿入経路の検査 (Git Bash、assemblies/child_interior/views で):

```bash
O="/c/Program Files/OpenSCAD/openscad.exe"
"$O" -o ../_work/images/views/13_rib_fit_bot_exploded.png --imgsize=1200,900 --camera=0,-8,-4,62,0,35,230 --colorscheme=Tomorrow -D 'mode="bot_exploded"' rib_fit_view.scad
"$O" -o ../_work/images/views/14_rib_fit_bot_seated.png   --imgsize=1200,900 --camera=0,-8,4,62,0,35,200   --colorscheme=Tomorrow -D 'mode="bot_seated"'   rib_fit_view.scad
"$O" -o ../_work/images/views/15_rib_fit_top_seated.png   --imgsize=1200,900 --camera=0,-8,196,62,0,35,200 --colorscheme=Tomorrow -D 'mode="top_seated"'   rib_fit_view.scad
# 挿入経路の掃引検査: 「Current top level object is empty」= リブがデッキのどこにも当たらず座まで入る
"$O" -o sweep_bot.stl -D 'end="bot"' rib_sweep.scad
"$O" -o sweep_top.stl -D 'end="top"' rib_sweep.scad
# 対照 (掃引を 2mm 伸ばすとショルダーに掛かって非空になる): -D 'end="bot"' -D 'zext=2'
```
