"""Rev.5 migration: retain sensor mounts, integrate fixed green locators."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'

def main():
    p=A/'placement.json'
    data=json.loads(p.read_text(encoding='utf-8'))
    data['items']=[r for r in data['items'] if not r['label'].startswith('bolt_on_')]
    data['note']='Rev.5: 15 spare M4 axes on a masked 30 mm grid; four fixed vessel locators integral with main plate. TD04A and camera C mounts remain detachable; moving pressure pads remain separate.'
    data['coordinate_system']='Box datums Z=0; main plate top -0.8, underside -20; integral end arms -18..-8; C interface -30; ground -72. Spare nut floors -7.3, example screw tips -2.'
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p=A/'print_config.json';config=json.loads(p.read_text(encoding='utf-8'))
    camera_note=(' camera_mount'+config['note'].split(' camera_mount',1)[1]) if ' camera_mount' in config.get('note','') else ''
    config['status']='prototype_universal_plate'
    config['note']=('Rev.5: 予備M4穴15箇所、30 mmピッチ。緑色の固定位置決め部4個は主プレートと一体化し、M4固定ねじ8本・ナット8個を廃止。'
        'TD04A・カメラ治具は別体。動く圧力パッド3個は別体で調整を維持。PETG Basic・X1 Carbon・0.4 mm、8壁・100%・3 mmブリム。'
        '主プレートは0.2 mm層、三点基準を上、normal(auto)/snug・ベッド上のみ・raft_first_layer_expansion=0。'
        '現行プレート3MFはprint_jobs/universal_plate/。旧プレート用3MFは履歴で流用しない。予備ナットは必要箇所だけ箱設置前に挿入。'
        '取付例は厚7 mm治具+M4x25、先端Z=-2。実締結・強度・クリープ・浮力は未認定。'+camera_note)
    p.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Configured Rev.5: integrated locators, 15 spare holes; 8 screws and 8 nuts removed.')

if __name__=='__main__':main()
