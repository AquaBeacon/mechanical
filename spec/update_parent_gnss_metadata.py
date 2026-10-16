"""Keep manufacturing source dependencies and revision print metadata explicit."""
from pathlib import Path
from collections import Counter
import json,os
R=Path(__file__).resolve().parents[1]
def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['ann_mb1_internal_rack','gnss_universal_carrier','parent_hand_service']:
    p=R/'parts/parent/interior/printed'/name;f=p/'manufacturing.json'
    data=json.loads(f.read_text()) if f.exists() else {}
    source='spec/build_parent_hand_service.py' if name=='parent_hand_service' else 'spec/build_parent_gnss.py'
    refs=[source,'spec/remesh_parent_gnss_outputs.py','scad/lib/parent_gnss.py','scad/lib/cad_edge_finish.py','parts/parent/interior/cots/sparkfun_neo_f9p/ref/SparkFun NEO-F9P.brd','parts/parent/interior/cots/sparkfun_neo_f9p/ref/NEO-F9P.STEP']
    if name=='parent_hand_service':refs += ['scad/lib/parent_corner_mounts.py','spec/parent_switch_tx_body.py','spec/build_bcas212310g.py','parts/parent/exterior/cots/bcas212310g/dimensions.json','parts/parent/exterior/cots/bcas212310g/interior_corner_clearance.step']
    if name=='gnss_universal_carrier':refs += ['parts/parent/interior/cots/adafruit_lis3mdl/ref/Adafruit LIS3MDL.brd','parts/parent/interior/cots/adafruit_lis3mdl/ref/4479 LIS3MDL.step']
    data['source_dependencies']=[os.path.relpath(R/q,p).replace('\\','/') for q in refs]
    data['print_rotations_deg']={}
    if name=='parent_hand_service':
        data['non_print_files']=list(dict.fromkeys(data.get('non_print_files',[])+['tx_top_keepout','main_lower_carrier','sony_upper_carrier','main_offset_corner']+[f'sony_corner_{i}' for i in range(4)]))
        data['print_rotations_deg'].update({'guide_0':[0,-90,0],'guide_1':[0,-90,0],'guide_2':[0,90,0],'guide_3':[0,90,0]})
        data['print_rotations_deg'].update({f'service_prop_{i}':[0,90,0] for i in range(5)})
        data['print_rotations_deg'].update(main_corner_column=[0,0,0],main_mount_plate=[0,0,0],sony_mount_plate=[0,0,0])
    if name=='ann_mb1_internal_rack':data['print_rotations_deg']['ann_mb1_internal_rack']=[180,0,0]
    data['release_status']='fit_check_prototype'
    data['structural_print_conditions']=dict(material='PETG',layer_height_mm=.2,walls=4,infill_percent=100,build_axis='Z',note='Dense equivalent-solid assumption for historical FEA; current case-corrected geometry not structurally analyzed. Supports as PRINT.md. No fatigue/creep qualification.')
    write(f,data)
p=R/'parts/parent/interior/printed/parent_lipo_retainer';f=p/'manufacturing.json';d=json.loads(f.read_text())
d['source_dependencies']=[os.path.relpath(R/q,p).replace('\\','/') for q in ['spec/prepare_parent_lipo_retainer.py','spec/export_parent_lipo_retainer.py','spec/remesh_parent_gnss_outputs.py']];write(f,d)
a=R/'assemblies/parent_hand_service'
placement=json.loads((a/'placement.json').read_text(encoding='utf-8'))
props=[{'part':it['part'],'file':it['file'],'quantity':1,'labels':[it['label']]} for it in placement['service_only'] if it['file'].startswith('service_prop_')]
props.append({'part':'parts/common/interior/printed/stack_spacers','file':'parent_stack_spacer_set','quantity':1,'labels':['print_runner_12_spacers']})
write(a/'print_config.json',{'status':'fit_check_prototype','note':'サポート・材料削減改訂：床は幅7.5 mm・高さ9.96 mmの開放格子、固定座を連結。アンテナ台と同軸リング、GNSS台と支柱4本をキー付きで分割し既存長ねじで共締め。MAIN/Sony台とアンテナ台はX180度で印刷、その他は設計元の姿勢。PETG 0.2 mm・4周壁・100%インフィル。支持材はスライス検証を参照、GNSS磁気棚など局所張出しは支持が残る。LiPo・両SD・電源2スイッチ・TX上方20 mm・箱外MAIN USB・OD100/ID75/H10を維持。巻き束は外壁4窓の柔らかい糸込みで指定包絡に収める。分割キーの嵌合と締結・揺動・クリープ、閉蓋受信・磁気精度は実物確認。','notes':['docs/配線・ケーブル計画.md','assemblies/parent_hand_service/wave_rigidity_report.md','assemblies/parent_hand_service/print_economy_report.md'],'extra_parts':props})
f=a/'manufacturing_parts.json';d=json.loads(f.read_text());d['printed_parts']=['battery_base','floor_plate','main_mount_plate','sony_mount_plate'];d['metal_fasteners']={'underside_fixture_M3x8':16,'main_pwr_tx_M3x8':12,'sony_M2_5x6':4};d['additional_printed_parts']=[{'part':'parts/parent/interior/printed/ann_mb1_internal_rack','file':'ann_mb1_internal_rack','quantity':1},{'part':'parts/parent/interior/printed/gnss_universal_carrier','file':'gnss_universal_carrier','quantity':1},{'part':'parts/parent/interior/printed/gnss_universal_carrier','file':'gnss_edge_cap','quantity':1},{'part':'parts/parent/interior/printed/gnss_universal_carrier','file':'gnss_edge_cap_front','quantity':1},{'part':'parts/parent/interior/printed/parent_lipo_retainer','file':'parent_lipo_retainer_lid_narrow','quantity':1}];d['nonmagnetic_fasteners']={'LIS3MDL_nylon_M2x8':4,'LIS3MDL_nylon_M2_nut':4};d['note']='Placement is canonical. Current fixed carrier variant: no lift guides, props or stop pins; previous rigidity evidence is historical.';write(f,d)
config=json.loads((a/'print_config.json').read_text(encoding='utf-8'))
config['note']='2026-10-10：ナット座下面を床格子下面まで連結し、Sony上台の囲い壁を撤去。印刷スペーサ4本で上段を支え、GNSS支柱4本と合わせ8本を切離しランナー1枚で印刷。MAIN/Sony台・アンテナ台はX180度、ランナーは突起を上向き。PETG0.2 mm・4周壁・100%インフィル、局所支持は実スライス結果に従う。LiPo・両SD・両電源スイッチ・TX上方20 mm・箱外MAIN USB・同軸OD100/ID75/H10は維持。切離し後は側面のバリを除き、キー・座面・穴を削らない。実物の嵌合、締結、揺動とクリープは未確認。'
config['note'] += ' 2026-10-11容器訂正：床厚3・ボス上面Z10・四隅に対応。床座下面Z10、ケース固定M4×12を4本。LiPo北3.6 mm、TX南4 mm、GNSS後左脚東2.6 mm。図面にない成形形状と公差、現行形状の剛性は未認定。'
config['note']='2026-10-11：MAIN/Sonyの両方に固定板を設ける。板は大きな矩形肉抜き、基板は4か所のねじ座だけで浮かせ、ピンごとの逃げ加工を使わない。板は平らな下面をベッドへ向ける。スペーサ12個は切離しランナー1枚。PETG0.2 mm・4周壁・100%インフィル。側面の首とバリだけを除き、座面・キー・穴は削らない。実嵌合・締付け・波浪・クリープは未検証。'
config['notes']=['docs/配線・ケーブル計画.md','assemblies/parent_hand_service/fixed_plate_report.md']
write(a/'print_config.json',config)
d['metal_fasteners'].pop('case_M4x8_button',None)
d['metal_fasteners']['case_M4x12_button']=4
d['metal_fasteners'].pop('underside_fixture_M3x8',None)
d['metal_fasteners'].pop('sony_carrier_M3x45',None)
d['metal_fasteners'].update(floor_M3_nuts=16,main_combined_M3x30=3,main_carrier_M3x25=1,main_pwr_tx_M3x8=9,sony_carrier_M3x50=4,gnss_frame_M3x40=4,antenna_rack_M3x50=4)
d['purchased_fasteners_by_file']=dict(Counter(it.get('file',Path(it['part']).name) for it in placement['items'] if '/cots/screw' in it['part'] or it['label'].startswith(('mag_bolt_','mag_nut_','lipo_ret_bolt_','lipo_ret_nut_'))))
d['additional_printed_parts'] += [{'part':'parts/parent/interior/printed/ann_mb1_internal_rack','file':'ann_mb1_coax_ring','quantity':1},{'part':'parts/parent/interior/printed/gnss_universal_carrier','file':'gnss_column_front','quantity':2},{'part':'parts/parent/interior/printed/gnss_universal_carrier','file':'gnss_column_rear','quantity':2}]
d['additional_printed_parts'] += [{'part':'parts/common/interior/printed/stack_spacers','file':f,'quantity':2,'print_set':'parent_stack_spacer_set'} for f in ['sony_column_left','sony_column_right']]
d['additional_printed_parts'] += [{'part':'parts/parent/interior/printed/parent_hand_service','file':stem,'quantity':qty,'print_set':'parent_stack_spacer_set'} for stem,qty in [('main_corner_column',4)]]
d['print_sets']=[{'part':'parts/common/interior/printed/stack_spacers','file':'parent_stack_spacer_set','quantity':1,'contents':'Sony columns4; GNSS columns4; MAIN columns4'}]
write(f,d)

# Current sensor fixture revision: historical caps stay out of the print set.
d['additional_printed_parts']=[it for it in d['additional_printed_parts'] if not it['file'].startswith('gnss_edge_cap')]
d['sensor_fixture_revision']='2026-10-11: four M3x10/nuts for universal PCB; existing nylon M2x8/nuts for LIS3MDL'
d['metal_fasteners'].update(gnss_pcb_M3x10=4,gnss_pcb_M3_nuts=4)
write(f,d)
config=json.loads((a/'print_config.json').read_text(encoding='utf-8'))
config['notes']=list(dict.fromkeys(config['notes']+['assemblies/parent_hand_service/sensor_mount_report.md']))
config['note']+=' 2026-10-11センサ固定改訂：GNSS基板穴75×55 mm、端から2.5 mm、M3×10／M3ナット各4。前後押さえは廃止。GNSS一式は西6 mm・基板高さ維持。LIS3MDL下面Z56、四隅固定の低い矩形枠。再印刷はGNSS台1個。現行スライスと着脱条件はsensor_mount_report.mdを参照。'
write(a/'print_config.json',config)
