"""Collect final mesh and slicer evidence, BOM, and a print-only zip."""
from pathlib import Path
import json,sys,hashlib,zipfile,collections
import trimesh
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_parent_spar_bolted import ROOT,OUT,PRINT,SPECS
report={}; total_g=0; total_s=0
for p in sorted(PRINT.glob('*.stl')):
 key=p.stem.removeprefix('parent_spar_');q=SPECS.get(key,('','',1))[2]
 m=trimesh.load(p,force='mesh')
 assert m.is_watertight and len(m.split())==1,p
 assert max(m.extents)<=250 and abs(m.bounds[0,2])<.05,p
 assert m.extents[0]+10<=236 and m.extents[1]+10<=250,p
 result=json.loads((PRINT/'slice_validation'/p.stem/'result.json').read_text(encoding='utf-8'))
 assert result['return_code']==0,p
 plate=result['sliced_plates'][0]
 mass=sum(f['total_used_g'] for f in plate['filaments'])
 duration=plate['total_predication']
 total_g+=q*mass;total_s+=q*duration
 report[p.stem]={'quantity':q,'size_mm':m.extents.tolist(),'watertight':True,'bodies':1,'volume_cm3':float(m.volume/1000),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'slice_return_code':0,'slice_warning':plate.get('warning_message',''),'filament_g_including_support_and_brim':mass,'estimated_seconds':duration}
OUT.joinpath('print_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
hardware=json.loads(OUT.joinpath('fasteners.json').read_text(encoding='utf-8'))
counts=collections.Counter(x['type'] for x in hardware)
lines=['# 金具数量（形状モデル集計）','','金属ねじ棒・ねじ・ナット・座金は印刷しない。寸法はmm。','', '|金具|個数|','|---|---:|']
lines += [f'|{name}|{count}|' for name,count in sorted(counts.items())]
lines += ['', '別途：既存デッキ用M5インサート12個・M4インサート4個、浮体用シール4本、錘用金属リング（外径50 / 内径9、合計高さ30）。カメラねじは純正品との実物適合確認が必要。ねじの長さは座面からの長さ。ナイロック等で抜止めする場合はナット高さ増分に合わせて長さを調整する。','', 'M6長ナットは二面幅10・長さ18のモデル。標準ナットはM4高さ3.2 / M5高さ4 / M6高さ5 / M8高さ6.5。座金は厚さ1、外径M4=9 / M5=10 / M6=12 / M8=16。インサートの外径・長さは既存デッキ図に合わせる。']
OUT.joinpath('fastener_bom.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
summary=['# X1 Carbon 印刷用セット','','16種類・23点。STLは印刷向きに調整済み。1部品ずつスライス検証。','', 'Generic PETG / Textured PEI Plate / 0.4 mm nozzle / 0.20 mm / 壁6周 / 上下6層 / Gyroid 40% / 外側ブリム5 mm / 自動通常サポート。Bambu Studio X1 Carbon設定の禁止領域を維持。XY中心(138,128)へ置く。','', f'スライサー見積合計（数量分、ブリム・サポート込み）：約{total_g/1000:.2f} kg、約{total_s/3600:.1f}時間。実機時間・完成品重量ではない。','', '|ファイル|数量|外形 mm|','|---|---:|---|']
summary += [f'|{name}.stl|{d["quantity"]}|'+ ' × '.join(f'{v:g}' for v in d['size_mm'])+'|' for name,d in report.items()]
summary += ['', '組立STEP・固定方法・シール・未検証条件は assemblies/parent_spar_bolted/README.md を参照。浮体は実機で水密試験と浮力・傾斜試験を行う。箱・機器・金属錘・金具・シールは購入品。']
PRINT.joinpath('PRINT.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
with zipfile.ZipFile(OUT/'parent_spar_X1C_prints.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in PRINT.glob('*.stl'):z.write(p,p.name)
 z.write(PRINT/'PRINT.md','PRINT.md')
 z.write(OUT/'README.md','ASSEMBLY.md');z.write(OUT/'fastener_bom.md','FASTENERS.md')
 for p in (PRINT/'slice_validation').glob('*.json'):
  if p.stem in ['machine','process','filament']:z.write(p,'profiles/'+p.name)
print('PASS',len(report),'types',sum(d['quantity'] for d in report.values()),'prints',round(total_g),'g',round(total_s/3600,1),'hours')
