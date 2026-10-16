from pathlib import Path
import json,collections,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assemblies/parent_bottom_sensors';PRINT=ROOT/'print_jobs/parent_bottom_sensors'
checks=json.loads((OUT/'print_checks.json').read_text())
counts=collections.Counter(f['type'] for f in json.loads((OUT/'fasteners.json').read_text()))
lines=['# X1 Carbon 印刷セット：下向きカメラ・TD04A版','','STLは印刷向きです。浮き2個・紐・金具・箱・センサーは購入品です。','', '|部品|数量|印刷寸法 mm|','|---|---:|---|']
mass=seconds=0
for name,d in checks.items():
 assert d['slice_return_code']==0 and d['sha256']==hashlib.sha256((PRINT/(name+'.stl')).read_bytes()).hexdigest(),name
 mass+=d['quantity']*d['filament_g_including_support_and_brim'];seconds+=d['quantity']*d['estimated_seconds']
 lines.append(f"|{name}|{d['quantity']}|"+' × '.join(f'{v:g}' for v in d['size_mm'])+'|')
lines+=['',f'13種類14点。スライサー見積もり：約{mass/1000:.2f} kg、約{seconds/3600:.1f}時間（サポート・ブリム込み）。完成品重量ではありません。','', 'PETG / 0.4 mm / 0.20 mm / 壁6周 / 上下6層 / Gyroid 40% / 外側ブリム5 mm / 自動通常サポート / Textured PEI。XY中心を(138,128)へ配置し、X1 Carbonの禁止領域を維持。', '', 'TD04Aは胴径26・胴長55の仮寸法。実物でクランプ適合を確認してから本印刷してください。カメラケース・浮きも実測未確定。組立方法と検証の範囲はASSEMBLY.mdを参照。']
(PRINT/'PRINT.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'fastener_bom.md').write_text('# 金具一覧\n\n|種類|数量|\n|---|---:|\n'+'\n'.join(f'|{k}|{v}|' for k,v in sorted(counts.items()))+'\n\n別途：デッキ用M4インサート4個、M5インサート8個（中央4・GPS側面4）。未使用座のインサートは任意。ねじ・座金・ナットは購入品。M4×65の長尺品は調達確認が必要。既存カメラ用軸ねじは純正仕様との照合が必要。\n',encoding='utf-8')
with zipfile.ZipFile(OUT/'parent_bottom_sensors_X1C_prints.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in checks:z.write(PRINT/(name+'.stl'),name+'.stl')
 for source,target in [(PRINT/'PRINT.md','PRINT.md'),(OUT/'README.md','ASSEMBLY.md'),(OUT/'fastener_bom.md','FASTENERS.md'),(OUT/'print_checks.json','print_checks.json')]:z.write(source,target)
print('Packaged',round(mass),'g',round(seconds/3600,1),'hours',flush=True)
