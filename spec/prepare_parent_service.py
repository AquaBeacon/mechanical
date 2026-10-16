from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_service_review'; OUT.mkdir(exist_ok=True)
PCB=ROOT.parent/'hardware/pcb'
def footprints(board):
 text=(PCB/board/(board+'.kicad_pcb')).read_text(encoding='utf-8')
 starts=[m.start() for m in re.finditer(r'\(footprint ',text)]
 result={}
 for a,b in zip(starts,starts[1:]+[len(text)]):
  s=text[a:b]; ref=re.search(r'\(property "Reference" "([^"]+)"',s)
  at=re.search(r'\(at ([\d.-]+) ([\d.-]+)(?: ([\d.-]+))?\)',s)
  if ref and at: result[ref[1]]={'xy':[float(at[1]),float(at[2])],'angle':float(at[3] or 0),'drill':float(re.search(r'\(drill ([\d.]+)',s)[1]) if re.search(r'\(drill ([\d.]+)',s) else None}
 return result
main,pwr,tx=[footprints(b) for b in ['PARENT_MAIN','PARENT_PWR','TX_improved']]
# Plate origins: board southwest. Main/PWR mesh uses negative Y.
holes={
 'MAIN':[[2+main['H'+str(i)]['xy'][0],27+88-main['H'+str(i)]['xy'][1]] for i in range(1,5)],
 'PWR':[[6+pwr['H'+str(i)]['xy'][0],120+84-pwr['H'+str(i)]['xy'][1]] for i in range(1,5)],
 'TX':[[121+tx['H'+str(i)]['xy'][1],127+tx['H'+str(i)]['xy'][0]+4] for i in range(1,5)],
 'SONY':[[121+x,27.5+y] for x,y in [[2.54,54.61],[50.8,53.34],[7.62,2.54],[35.56,2.54]]]
}
folder=ROOT/'parts/parent/interior/printed/parent_plate_service'; folder.mkdir(exist_ok=True)
scad='''// Service revision: plate dimensions from existing BCAS drawing; hole XY generated from PCB and Sony CAD.
/* [Plate] */
px=183; py=203; pt=5; corner_cut=8;
boss_d=7; boss_h=6; pwr_boss_h=9.5;
m3_pilot=2.6; m4_d=4.5; pin_d=3.2; pin_h=6;
$fn=48;
'''
for k,v in holes.items(): scad+=k.lower()+'_h='+json.dumps(v)+';\n'
scad+='''module bore(d,h){cylinder(r=(d/2)/cos(180/12),h=h,$fn=12);}
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
'''
(folder/'parent_plate_service.scad').write_text(scad,encoding='utf-8')
asm=json.loads((ROOT/'assemblies/parent_interior_p1/placement.json').read_text(encoding='utf-8'))
asm['name']='parent_service_review';asm['note']='2026-09-26 revision: lid-open service. Official Sony CAD; IMU envelope pending CAD/stack measurement. LCD support not yet designed.'
for it in asm['items']:
 label=it['label']
 if label=='plate': it['part']='parts/parent/interior/printed/parent_plate_service';it.pop('file',None)
 if label in ['p_main','p_pwr','lipo_tray','lipo'] or label.startswith('main_spacer'): it['ops'][0]['translate'][1]+=25
 if label=='p_pwr':
  it['ops'][0]['translate'][2]+=3.5
  it['ops'][0]['translate'][0]+=4
 if label=='tx_improved':it['ops'][0]['translate'][1]+=50
 if label=='spresense':
  it['part']='parts/parent/interior/cots/spresense_service_stack';it['ops']=[{'translate':[134.5,41,24.8]}];it['note']='Sony STEP coordinates normalized so EXT PCB underside Z=0. IMU is an explicitly provisional envelope, not vendor CAD.'
 if label!='box_bcas212310g':it['note']='2026-09-26 service placement; '+it.get('note','')
(OUT/'placement.json').write_text(json.dumps(asm,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'hole_sources.json').write_text(json.dumps({'holes_plate_mm':holes,'main_ports':{k:main[k] for k in ['SD1','PICO1']},'pcb_sha256':{b:hashlib.sha256((PCB/b/(b+'.kicad_pcb')).read_bytes()).hexdigest() for b in ['PARENT_MAIN','PARENT_PWR','TX_improved']}},indent=2),encoding='utf-8')
print('Generated service plate and placement',holes)




from prepare_parent_lipo_retainer import integrate
integrate(OUT/'placement.json')
