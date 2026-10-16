"""Verify automatic support generation on the supplied print orientations."""
from pathlib import Path
import json,subprocess,zipfile,hashlib,concurrent.futures,os
import trimesh
R=Path(__file__).resolve().parents[1];O=R/'assemblies'/os.environ.get('PARENT_SLICE_NAME','parent_light');W=O/'slice_validation';W.mkdir(exist_ok=True)
C=R/'print_jobs/parent_spar_bolted/slice_validation'
manifest=json.loads((O/'print_manifest.json').read_text())
previous={i['part']:i for i in json.loads((O/'slice_report.json').read_text())} if (O/'slice_report.json').exists() else {}
def run(i):
    n=i['part'];D=W/n;D.mkdir(exist_ok=True)
    cfg=json.loads((C/'process.json').read_text())
    cfg.update(enable_support='1',support_type='normal(auto)',bridge_no_support='1',support_threshold_angle='30',brim_width='5',print_settings_id='Parent rounded PETG 0.20 automatic supports')
    src=O/'prints'/(n+'.stl')
    if n in previous and previous[n]['sha256']==hashlib.sha256(src.read_bytes()).hexdigest() and (D/'process.json').exists() and json.loads((D/'process.json').read_text())==cfg:
        print(n+' reuse matching verified slice',flush=True);return previous[n]
    (D/'process.json').write_text(json.dumps(cfg,indent=2))
    src=O/'prints'/(n+'.stl');m=trimesh.load(src)
    m.apply_translation([138-m.bounds[:,0].mean(),128-m.bounds[:,1].mean(),-m.bounds[0,2]]);m.export(D/'placed.stl')
    cmd=[r'C:\Program Files\Bambu Studio\bambu-studio.exe','--debug','2','--datadir',str(D/'studio_data'),'--load-settings',str(C/'machine.json')+';'+str(D/'process.json'),'--load-filaments',str(C/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf',n+'.3mf','--outputdir',str(D),str(D/'placed.stl')]
    p=subprocess.run(cmd,capture_output=True,text=True,errors='replace',cwd=D)
    (D/'slice.log').write_text(p.stdout+p.stderr,encoding='utf-8')
    result=json.loads((D/'result.json').read_text());assert p.returncode==0 and result['return_code']==0,(n,result)
    plate=result['sliced_plates'][0]
    with zipfile.ZipFile(D/(n+'.3mf')) as z:gc=z.read('Metadata/plate_1.gcode').decode()
    features=[s for s in gc.splitlines() if s.startswith('; FEATURE:') and 'Support' in s]
    report=dict(part=n,quantity=i['quantity'],sha256=hashlib.sha256(src.read_bytes()).hexdigest(),support_feature_sections=len(features),grams=sum(f['total_used_g'] for f in plate['filaments']),seconds=plate['total_predication'],warnings=plate.get('warning_message',''),support_enabled=True)
    print(json.dumps(report),flush=True);return report
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: reports=list(pool.map(run,manifest))
(O/'slice_report.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
print('Total grams',sum(i['quantity']*i['grams'] for i in reports),'seconds',sum(i['quantity']*i['seconds'] for i in reports),flush=True)
