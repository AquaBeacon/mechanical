"""Update the current assembly metadata and instructions for the battery revision."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
for name in ['placement.json','service_placement.json']:
    p=O/name;j=json.loads(p.read_text(encoding='utf-8'))
    it=next(it for it in j['items'] if it['label']=='lipo_ret_nut_0')
    it['ops']=[op for op in it['ops'] if 'rotate' not in op]+[{'rotate':[0,0,90]}]
    j['battery_lid_design'].update(tool_opening_mm=8.0,nut_entry_roof_deg=50,local_support_blocker='battery_lid_nut_support_blocker')
    p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=O/'print_config.json';j=json.loads(p.read_text(encoding='utf-8'))
j['note']='2026-10-13 現行：電池下の容器固定ねじ用工具穴は8 mm。最下段floor_plateとコード巻き部は変更なし。蓋は2本の端フックを北へ2 mm差し込み、M3×12ねじ／M3ナットを各1個で固定。外すときはねじを外し南2 mm戻して上へ抜く。ナットの六角方向を穴へ合わせて側面から差し込む。ナット座は斜め天井と局所サポート禁止設定を使用。電池台はprint_jobs/battery_tool_nut_access_20261013/battery_base.3mfをプロジェクトとして開くと設定済み。STLを使う場合は同梱modifiers/battery_lid_nut_support_blocker.stlを電池台へ支持材禁止パーツとして追加し、同梱座標を維持する。モディファイアは印刷しない。今回の再印刷は電池台1個。蓋は2026-10-12のスライド版を使用（旧4本ねじ版なら蓋も交換）。全9種類各1個、PETG0.2 mm・4周壁・100%インフィル。蓋は上面をベッドへ向けた姿勢に変換済み。支持材とバリを確認。実嵌合と強度は試作で確認する。'
j['modifiers']=[dict(host='battery_base',source='parts/parent/interior/printed/parent_hand_service/battery_lid_nut_support_blocker.stl')]
note='assemblies/parent_hand_service/battery_tool_nut_access_report.md'
if note not in j['notes']:j['notes'].append(note)
p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
intro='2026-10-13：電池下の工具穴を8 mmへ拡大。蓋は2 mmスライド＋M3×12ねじ1本。ナット差込み口を50°の斜め天井にし、局所サポート禁止設定を同梱。電池台の設定済み3MFと詳しい手順はbattery_tool_nut_access_report.md。最下段とコード巻き部の形状は変更なし。'
for p in [O/'README.md',R/'parts/parent/interior/printed/parent_hand_service/README.md',R/'parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer.md']:
    t=p.read_text(encoding='utf-8');lines=t.splitlines()
    if intro not in t:lines[2:2]=[intro,'']
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
for rel in ['docs/部品一覧.md','docs/配線・ケーブル計画.md']:
    p=R/rel;t=p.read_text(encoding='utf-8')
    note='2026-10-13 親機電池台：工具穴8 mm、蓋は2 mmスライド＋ねじ1本。ナット座の斜め天井と支持材禁止パーツを使用。設定済み3MFはassemblies/parent_hand_service/print_jobs/battery_tool_nut_access_20261013/battery_base.3mf。印刷入口は同assemblyのparts/PRINT.md。配線端開口、電池位置、最下段と同軸巻き部は変更なし。'
    if note not in t:p.write_text(t+'\n\n'+note+'\n',encoding='utf-8')
