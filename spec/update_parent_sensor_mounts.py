"""Apply sensor-fixture datums to the existing placement without rebuilding peers."""
from pathlib import Path
import copy, json, sys
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'scad/lib'))
import parent_gnss as G
O=R/'assemblies/parent_hand_service'

def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

d=json.loads((O/'placement.json').read_text(encoding='utf-8'))
d['items']=[it for it in d['items'] if not it['label'].startswith(('gnss_edge_cap_', 'gnss_cap_screw_', 'gnss_pcb_bolt_', 'gnss_pcb_nut_'))]
by={it['label']:it for it in d['items']}
for name in ['gnss_receiver','gnss_sma_plug','gnss_pin_headers']:
    by[name]['ops']=[{'translate':G.BOARD_ORIGIN},{'rotate':G.BOARD_ROTATION}]
by['gnss_universal_pcb']['ops']=[{'translate':G.UNIVERSAL_ORIGIN}]
by['gnss_xh_keepout']['ops']=[{'translate':G.XH_KEEPOUT_PROVISIONAL[:3]}]
by['magnetometer']['ops']=[{'translate':G.MAG_ORIGIN},{'rotate':G.MAG_ROTATION}]
for i,(x,y) in enumerate(G.magnetometer_mounting_xy()):
    by[f'mag_bolt_{i}']['ops']=[{'translate':[x,y,G.MAG_ORIGIN[2]+G.MAG_PCB_THICKNESS]}]
    by[f'mag_nut_{i}']['ops']=[{'translate':[x,y,G.MAG_SHELF_BOTTOM_Z-G.MAG_NUT_AF_HEIGHT[1]]}]
for i,(x,y) in enumerate(G.universal_mounting_xy()):
    for kind,stem,z in [('bolt','screw_m3x10',G.UNIVERSAL_ORIGIN[2]+G.UNIVERSAL_SIZE[2]),('nut','screw_nut_m3',G.UNIVERSAL_BEAM_BOTTOM_Z-2.4)]:
        d['items'].append(dict(label=f'gnss_pcb_{kind}_{i}',part='parts/common/interior/cots/screw',file=stem,group='interior',color='Silver',ops=[{'translate':[x,y,z]}]))
d['moving_labels']=[it['label'] for it in d['items'] if it['group']=='interior' and it['label'] not in ['lid_keepout','tx_top_keepout']]
d['gnss_design'].update(universal_carrier_mm=G.UNIVERSAL_SIZE[:2],mounting_hole_pitch_mm=G.UNIVERSAL_HOLE_PITCH,mounting_holes_xy_mm=G.universal_mounting_xy(),mount='Four M3x10 bolts and M3 nuts; edge caps removed',hole_measurement='User confirmed 2026-10-11: 75x55 pitch, 2.5 mm from all edges; M3 nominal, actual PCB drill diameter unmeasured',fixture_revision='GNSS cartridge translated -6 mm X, unchanged Z56; existing four floor interfaces retained')
d['magnetometer_design'].update(date='2026-10-11',mount='Coplanar rectangular frame connected to GNSS west rail and rear beam, four vendor 2.5 mm holes, nylon M2x8/nuts',origin_mm=G.MAG_ORIGIN)
write(O/'placement.json',d)
service=copy.deepcopy(d);service['name']='service'
service['items']=[it for it in service['items'] if it['label'] not in ['lid_keepout','tx_top_keepout']]
for it in service['items']:
    if it['label'] in d['moving_labels']:it['ops'].insert(0,{'translate':d['service_translation_mm']})
write(O/'service_placement.json',service)
mp=json.loads((O/'manufacturing_parts.json').read_text(encoding='utf-8'))
mp['additional_printed_parts']=[it for it in mp['additional_printed_parts'] if not it['file'].startswith('gnss_edge_cap')]
mp['purchased_fasteners_by_file'].pop('screw_m2x6',None)
mp['purchased_fasteners_by_file']['screw_m3x10']=4
mp['purchased_fasteners_by_file']['screw_nut_m3']+=4 if not mp.get('sensor_fixture_revision') else 0
mp['sensor_fixture_revision']='2026-10-11: four M3x10/nuts for universal PCB; existing nylon M2x8/nuts for LIS3MDL'
mp['metal_fasteners'].update(gnss_pcb_M3x10=4,gnss_pcb_M3_nuts=4)
write(O/'manufacturing_parts.json',mp)
pc=json.loads((O/'print_config.json').read_text(encoding='utf-8'))
note=' 2026-10-11センサ固定改訂：GNSS台だけ再印刷。基板穴75×55 mm・端から2.5 mm、M3×10とM3ナット各4。前後押さえは廃止。GNSS一式は西6 mm・高さ維持。LIS3MDL下面Z56、低い矩形枠の四隅へ既存ナイロンM2×8／ナット各4。枠の下面・ナット座は局所支持を検討し、現行スライスはsensor_mount_report.mdを参照。支柱ランナーほかは形状変更なし。'
pc['note']=pc['note'].split(' 2026-10-11センサ固定改訂：',1)[0]+note
pc['notes']=list(dict.fromkeys(pc['notes']+['assemblies/parent_hand_service/sensor_mount_report.md']))
write(O/'print_config.json',pc)
print('Updated only GNSS/magnetometer items, hardware and fixture metadata')
