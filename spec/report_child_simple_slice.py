"""Verify sliced 3MF settings, bound actual extrusion paths and package plates."""
from pathlib import Path
import hashlib
import json
import math
import re
import zipfile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'print_jobs/child_simple'
WORK=OUT/'slice_validation'
records=json.loads((WORK/'results.json').read_text())
summary={}
fig,axes=plt.subplots(1,3,figsize=(15,5.6))
for ax,suffix in zip(axes,['front','rear','guard']):
    record=records[suffix]
    name='child_simple_'+suffix
    source=OUT/(name+'_print.stl')
    assert record['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
    assert record['returncode']==0 and record['result']['return_code']==0
    project=OUT/(name+'_x1c_petg.3mf')
    with zipfile.ZipFile(project) as z:
        assert z.testzip() is None
        settings=json.loads(z.read('Metadata/project_settings.config'))
        for k,v in [('wall_loops','6'),('sparse_infill_density','100%'),('enable_support','1'),('layer_height','0.2')]:
            assert str(settings[k])==v,(suffix,k,settings.get(k))
        assert settings['printer_settings_id']=='Bambu Lab X1 Carbon 0.4 nozzle'
        assert settings['filament_type']==['PETG']
        assert settings['curr_bed_type']=='Textured PEI Plate'
        (WORK/suffix/'plate_thumbnail.png').write_bytes(z.read('Metadata/plate_1.png'))
    path=WORK/suffix/'plate_1.gcode'
    p=np.zeros(3)
    e=0.0
    erel=True
    xyzrel=False
    feature='Custom'
    bounds=np.array([[np.inf,np.inf],[-np.inf,-np.inf]])
    lines={'Part':[],'Support':[],'Brim':[]}
    count=0
    headers={}
    for line in path.open(encoding='utf-8',errors='replace'):
        if line.startswith('; ') and ' = ' in line:
            k,v=line[2:].rstrip('\r\n').split(' = ',1)
            headers[k]=v
        if line.startswith('; FEATURE: '):
            feature=line.split(':',1)[1].strip()
        code=line.split(';',1)[0].strip()
        if not code: continue
        cmd=code.split()[0]
        if cmd=='M83': erel=True
        elif cmd=='M82': erel=False
        elif cmd=='G90': xyzrel=False
        elif cmd=='G91': xyzrel=True
        elif cmd in ('G0','G1','G2','G3','G92'):
            args={k:float(v) for k,v in re.findall(r'([XYZEIJ])([-+]?\d*\.?\d+)',code)}
            old=p.copy()
            for i,k in enumerate('XYZ'):
                if k in args: p[i]=(p[i]+args[k]) if xyzrel and cmd!='G92' else args[k]
            delta=0.0
            if 'E' in args:
                delta=args['E'] if erel else args['E']-e
                e=(e+args['E']) if erel and cmd!='G92' else args['E']
            if cmd=='G92' or delta<=0 or feature in ('Custom','Undefined') or np.linalg.norm(old[:2]-p[:2])<1e-7: continue
            points=np.vstack([old[:2],p[:2]])
            if cmd in ('G2','G3') and ('I' in args or 'J' in args):
                c=old[:2]+[args.get('I',0),args.get('J',0)]
                r=np.linalg.norm(c-old[:2])
                start=math.atan2(old[1]-c[1],old[0]-c[0])
                end=math.atan2(p[1]-c[1],p[0]-c[0])
                direction=1 if cmd=='G3' else -1
                sweep=((end-start)*direction)%(2*math.pi)
                for angle in (0,math.pi/2,math.pi,3*math.pi/2):
                    if ((angle-start)*direction)%(2*math.pi)<=sweep+1e-8:
                        points=np.vstack([points,c+r*np.array([math.cos(angle),math.sin(angle)])])
            bounds[0]=np.minimum(bounds[0],points.min(axis=0))
            bounds[1]=np.maximum(bounds[1],points.max(axis=0))
            count+=1
            if p[2]<=0.201:
                group='Support' if 'Support' in feature else 'Brim' if feature in ('Brim','Skirt') else 'Part'
                lines[group].append([old[:2].copy(),p[:2].copy()])
    assert bounds[0,0]>18 and bounds[0,1]>3 and bounds[1].max()<253,(suffix,bounds)
    for k,v in [('sparse_infill_density','100%'),('sparse_infill_pattern','zig-zag'),('wall_loops','6'),('enable_support','1')]:
        assert headers[k]==v,(suffix,k,headers.get(k))
    plate=record['result']['sliced_plates'][0]
    summary[suffix]=dict(project=project.name,sha256=hashlib.sha256(project.read_bytes()).hexdigest(),seconds=plate['total_predication'],filament_g=sum(f['total_used_g'] for f in plate['filaments']),warning=plate.get('warning_message',''),extrusion_xy_bounds_mm=bounds.tolist(),extruding_segments=count,settings_verified=True,sliced=True)
    for group,color in [('Brim','#d79330'),('Support','#87959c'),('Part','#2579a7')]:
        ax.add_collection(LineCollection(lines[group],colors=color,linewidths=0.45,label=group))
    ax.add_patch(Rectangle((0,0),256,256,fill=False,edgecolor='#333333'))
    ax.add_patch(Rectangle((0,0),18,28,color='#dc655b',alpha=0.6))
    ax.set(xlim=(-5,261),ylim=(-5,261),aspect='equal',xlabel='X (mm)',ylabel='Y (mm)',title=suffix.upper()+' / first layer')
axes[0].legend(loc='upper left',fontsize=8)
fig.suptitle('X1 Carbon / PETG / 0.20 mm / 6 walls / 100% infill / supports enabled')
fig.tight_layout()
fig.savefig(OUT/'plate_layouts.png',dpi=160)
(OUT/'print_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')

def duration(s):
    m=round(s/60)
    return f'{m//60}時間{m%60:02d}分'
rows=[]
for suffix,label in [('front','前枠'),('rear','後枠'),('guard','灰色ガード')]:
    r=summary[suffix]
    rows.append(f"| [{label}]({r['project']}) | {duration(r['seconds'])} | {r['filament_g']:.0f} g |")
text='''# Bambu Studioで印刷する — 子機シンプル筐体r3

2026-09-17：rear中央にライト用M3・4穴・40×40 mmを追加。front印刷済みの場合はrearだけ新版を印刷する。frontとguardのデータは変更なし。

各3MFは**1部品・1プレート、スライス済み**。印刷向き・サポート・設定を保存してある。
プリンタへの送信・実機印刷は行っていない。

## ファイルと見積もり

| 3MF | 推定時間 | PETG（サポート・ブリム込み） |
|---|---:|---:|
'''+ '\n'.join(rows)+f"\n\n合計 **{duration(sum(r['seconds'] for r in summary.values()))}、約{sum(r['filament_g'] for r in summary.values())/1000:.2f} kg**。実機の時間・消費量は変動する。\n"+'''
## 印刷手順

1. 使うプレートの3MFをBambu Studioで**プロジェクトとして開く**。
2. **X1 Carbon／0.4 mmノズル／Textured PEI Plate／PETG**が実機と一致することを確認する。
3. 「プレビュー」でサポートが有効であることを確認する。モデルの向きを変えない。
4. 「プレートを印刷」で実機とPETGのスプール／AMSスロットを選ぶ。3部品を各1個印刷する。

1部品あたりの必要量は上表を参照。残量には余裕を持たせる。
別のプリンタ・材質・プレートを使う場合は対応する設定でスライスし直す。

## 保存した条件

- Bambu Studio 02.08.02.61。既存のX1C/Generic PETGシステムプリセットを使用。
- 0.20 mm、外周6周、上下6層、100%直線インフィル、外側ブリム3 mm。
- 通常自動サポート、モデル上にもサポート可、上下接触隙間0.20 mm、XY隙間0.35 mm。
- モデルとサポートは同じPETG。100%インフィルは強度合格を意味しない。
- 印刷台前左の禁止領域を維持し、実際の押出経路（サポート・ブリム込み）が範囲内にあることを検査。
- 3部品ともスライサー警告なし。ZIP破損検査と、3MF内およびG-code内の設定を照合済み。

![各プレートの初層経路。青=部品、灰=サポート、橙=ブリム、赤=禁止領域](plate_layouts.png)

## 印刷後

サポートを外し、M3通し穴のバリを取る。ガードは**M3×35の8本＋外付けナット8個＋ワッシャ16枚**で固定。
ねじ・ナットの埋め込み作業は不要。[組立仕様](../../assemblies/child_simple_assembly/README.md)を参照。

**試作モデル**：スライス成功は強度合格ではない。前工程の強度解析は未収束・一部基準未達で、
実運用前の荷重確認が残っている。r3のライト追加形状は強度解析未実施。[強度検証記録](../../assemblies/child_simple_assembly/verification.md)。
'''
(OUT/'START_HERE.md').write_text(text,encoding='utf-8')
with zipfile.ZipFile(OUT/'child_simple_x1c_petg_3mf.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    for r in summary.values(): z.write(OUT/r['project'],r['project'])
    z.write(OUT/'START_HERE.md','START_HERE.md')
    z.write(OUT/'plate_layouts.png','plate_layouts.png')
    z.write(OUT/'print_summary.json','print_summary.json')
print(json.dumps(summary,indent=2),flush=True)
