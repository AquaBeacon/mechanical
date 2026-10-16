"""Apply the selected full-length side-groove assembly metadata and print entry."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
operation='Disconnect power lead, remove four tray mount screws, lift closed battery module90 mm, remove one lid screw, slide lid south108 mm, then extract pack'
for name in ['placement.json','service_placement.json']:
    p=O/name;j=json.loads(p.read_text(encoding='utf-8'))
    j['battery_lid_design'].update(type='full_length_side_grooves_and_one_screw',release_translation_box_mm=[0,-108,0],module_lift_mm=90,operation=operation,rail_length_mm=107.4,side_groove_depth_mm=1.2,clearance_mm=.3)
    j['access_revision']['battery']=operation
    p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=O/'print_config.json';j=json.loads(p.read_text(encoding='utf-8'))
j['note']='2026-10-13 全長側溝版：電池台と蓋を各1個再印刷。蓋を配線側の端から両側の全長溝へ108 mm差し込み、M3×12ねじ／M3ナット各1個で固定する。箱内で全長分を引き出せないため、電源リードを外し、台の固定ねじ4本を外して閉じたボックスを上へ約90 mm持ち上げ、蓋ねじ1本を外して引き抜く。基板を外す必要はない。最下段、MAIN固定板、同軸巻き部と工具穴8 mmは維持。電池台はprint_jobs/battery_side_grooves_20261013/battery_base.3mfをプロジェクトとして開く。ナット座と側溝の支持材禁止設定済み。STLの場合はmodifiers内の支持材禁止パーツ2個を同梱座標で追加し、単体印刷しない。蓋は上面をベッドへ向けた同梱姿勢。9種類各1個、PETG0.2 mm・4周壁・100%インフィル。旧2 mmフック版の電池台／蓋を混ぜない。実印刷でバリ、嵌合と締付けを確認する。'
note='assemblies/parent_hand_service/battery_side_grooves_report.md'
if note not in j['notes']:j['notes'].append(note)
p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
intro='2026-10-13 全長側溝改訂：蓋を端から全長107.4 mmの両側溝へ差し込み、M3×12ねじ1本で固定。開く際は台の固定ねじ4本を外して閉じた電池ボックスを上へ約90 mm持ち上げ、蓋を南108 mm引き抜く。基板・最下段・同軸巻き部は変更なし。電池台と蓋を各1個再印刷。現行手順はbattery_side_grooves_report.md。'
for p in [O/'README.md',R/'parts/parent/interior/printed/parent_hand_service/README.md',R/'parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer.md']:
    t=p.read_text(encoding='utf-8');lines=t.splitlines()
    if intro not in t:lines[2:2]=[intro,'']
    t='\n'.join(lines)+'\n'
    t=t.replace('電池蓋のM3ねじ1本を外し、蓋を南2 mm滑らせて上へ外し、電池を上へ取り出す。','電源リードと台固定ねじ4本を外し、閉じた電池ボックスを上へ約90 mm持ち上げる。蓋のM3ねじ1本を外し、南108 mmへ引き抜いて電池を取り出す。')
    t=t.replace('蓋を南2 mmの解除位置から下ろして北へ2 mm滑らせ、M3×12ねじ1本を締める。','蓋を配線側の端から両側溝へ全長分滑らせ、M3×12ねじ1本を締める。')
    p.write_text(t,encoding='utf-8')
for rel in ['docs/部品一覧.md','docs/配線・ケーブル計画.md']:
    p=R/rel;t=p.read_text(encoding='utf-8')
    note='2026-10-13 全長側溝版：親機の電池蓋は両側の溝へ端から全長分を差し込み、ねじ1本で固定。開く際は台固定ねじ4本を外して閉じたボックスを上へ約90 mm持ち上げ、蓋を108 mm引き抜く。電源リードを先に外し、ボックスの持上げ経路へ配線を結束しない。現行印刷はassemblies/parent_hand_service/parts/PRINT.md、詳細はbattery_side_grooves_report.md。'
    if note not in t:p.write_text(t+'\n\n'+note+'\n',encoding='utf-8')
