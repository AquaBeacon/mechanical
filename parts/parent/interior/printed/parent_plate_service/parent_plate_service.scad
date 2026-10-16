// Service revision: plate dimensions from existing BCAS drawing; hole XY generated from PCB and Sony CAD.
/* [Plate] */
px=183; py=203; pt=5; corner_cut=8;
boss_d=7; boss_h=6; pwr_boss_h=9.5;
m3_pilot=2.6; m4_d=4.5; pin_d=3.2; pin_h=6;
$fn=48;
main_h=[[6.5, 110.5], [109.5, 110.5], [6.5, 35.0], [109.5, 35.0]];
pwr_h=[[11.0, 199.0], [101.0, 199.0], [11.0, 125.0], [101.0, 125.0]];
tx_h=[[125.0, 131.0], [125.0, 197.0], [167.0, 131.0], [167.0, 197.0]];
sony_h=[[123.54, 82.11], [171.8, 80.84], [128.62, 30.04], [156.56, 30.04]];
module bore(d,h){cylinder(r=(d/2)/cos(180/12),h=h,$fn=12);}
for (h=concat(main_h,pwr_h,tx_h,sony_h)) echo("HOLETABLE",h,m3_pilot);
difference(){
 union(){
  linear_extrude(pt) polygon([[corner_cut,0],[px-corner_cut,0],[px,corner_cut],[px,py-corner_cut],[px-corner_cut,py],[corner_cut,py],[0,py-corner_cut],[0,corner_cut]]);
  for(h=concat(main_h,tx_h,sony_h)) translate([h[0],h[1],pt]) cylinder(d=boss_d,h=boss_h);
  for(h=pwr_h) translate([h[0],h[1],pt]) cylinder(d=boss_d,h=pwr_boss_h);
  for(h=[[51.5,11.5],[91.5,11.5]]) translate([h[0],h[1],-pin_h]) cylinder(d=pin_d,h=pin_h+.2);
 }
 for(h=concat(main_h,tx_h,sony_h)) translate([h[0],h[1],-.1]) bore(m3_pilot,pt+boss_h+.2);
 for(h=pwr_h) translate([h[0],h[1],-.1]) bore(m3_pilot,pt+pwr_boss_h+.2);
 for(h=[[11.5,11.5],[171.5,11.5]]){
  translate([h[0],h[1],-.1]) bore(m4_d,pt+.2);
  translate([h[0],h[1],pt-2.55]) cylinder(d1=m4_d,d2=9,h=2.65);
 }
 // Cable ties kept clear of USB/SD corridors and board bosses.
 for(h=[[116.5,70],[176,110],[176,160]]) translate([h[0]-1.5,h[1]-5,-.1]) cube([3,10,pt+.2]);
}
