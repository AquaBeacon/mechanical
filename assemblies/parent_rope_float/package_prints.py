from pathlib import Path
import json,hashlib,zipfile,collections
r=Path.cwd();out=r/'assemblies/parent_rope_float';pr=r/'print_jobs/parent_rope_float'
checks=json.loads((out/'print_checks.json').read_text());old=json.loads((r/'assemblies/parent_spar_bolted/print_checks.json').read_text());mass=secs=0
lines=['# 紐接続版：X1 Carbon印刷セット','','浮き2個と紐は購入品です。円柱浮体・固定ロッドはこのセットに含みません。','', '|部品|数量|外形 mm|','|---|---:|---|']
for n,d in checks.items():
 p=pr/(n+'.stl');sha=hashlib.sha256(p.read_bytes()).hexdigest()
 if n in old:
  assert sha==old[n]['sha256'],n
  g=old[n]['filament_g_including_support_and_brim'];t=old[n]['estimated_seconds']
  d['slice_evidence']='Unchanged STL SHA256 matches previously X1C-sliced file'
 else:
  a=json.loads((pr/'adapter_slice/result.json').read_text());assert a['return_code']==0
  plate=a['sliced_plates'][0];g=sum(f['total_used_g'] for f in plate['filaments']);t=plate['total_predication'];d['slice_evidence']='adapter_slice/result.json, return_code 0'
 d['sha256']=sha;d['slice_return_code']=0
 mass+=g*d['quantity'];secs+=t*d['quantity']
 lines.append('|'+n+'|'+str(d['quantity'])+'|'+' x '.join(f'{v:g}' for v in d['size_mm'])+'|')
lines+=['',f'数量分のスライサー見積もり：約{mass/1000:.2f} kg、約{secs/3600:.1f}時間（サポート・ブリム込み）。完成品重量ではありません。','', 'PETG / 0.4 mm / 0.20 mm / 壁6周 / 上下6層 / Gyroid 40% / 外側ブリム5 mm / 自動通常サポート / Textured PEI。各部品のXY中心を(138,128)へ配置。既存X1 Carbon禁止領域を維持。浮力・強度と浮き実寸は実機確認が必要。']
(pr/'PRINT.md').write_text('\n'.join(lines),encoding='utf-8');(out/'print_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
counts=collections.Counter(x['type'] for x in json.loads((out/'fasteners.json').read_text()))
(out/'fastener_bom.md').write_text('# 紐接続版の金具\n\n|種類|数量|\n|---|---:|\n'+'\n'.join(f'|{k}|{v}|' for k,v in sorted(counts.items()))+'\n\n別途：左右の浮き2個、紐2本、既存デッキに適合するM4インサート4個・M5インサート12個。浮きの固定に剛体部品は使わない。\n',encoding='utf-8')
with zipfile.ZipFile(out/'parent_rope_float_X1C_prints.zip','w',zipfile.ZIP_DEFLATED) as z:
 for n in checks:z.write(pr/(n+'.stl'),n+'.stl')
 z.write(pr/'PRINT.md','PRINT.md');z.write(out/'README.md','ASSEMBLY.md');z.write(out/'fastener_bom.md','FASTENERS.md')
print(len(checks),'types',sum(x['quantity'] for x in checks.values()),'parts',round(mass),'g',round(secs/3600,1),'hours')
