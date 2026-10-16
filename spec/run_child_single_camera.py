"""Sequential detached GPU queue for the user's authorised topopt runs."""
from pathlib import Path
import os, json, subprocess, sys, time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_single_camera_topopt'
os.environ['PYTHONIOENCODING']='utf-8'
os.environ['TOPOPT_FREECAD']='C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/freecadcmd.exe'
phase=sys.argv[1] if len(sys.argv)>1 else 'exploration'
assert phase in ['exploration','validation']
state={'phase':phase,'started':time.time(),'pid':os.getpid(),'runs':[]}
def save():
    (OUT/f'{phase}_status.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
save()
for name in ['child_cam_bridge','child_jaw_gate','child_core_frame']:
    folder=OUT/name; study=folder/'study.json'
    # Include the transducer's direct local weight on its own seat.
    if name=='child_core_frame':
        data=json.loads(study.read_text(encoding='utf-8'))
        data['regions']['td04a_hp1']={'type':'box','min':[-30,-110,214.5],'max':[30,-60,219]}
        if not any(x['region']=='td04a_hp1' for x in data['cases'][0]['loads']):
            data['cases'][0]['loads'].append({'region':'td04a_hp1','force':[0,0,-9.4]})
        data['_td04a_load']='Provisional 0.32kg transducer/fastening at3g, rounded9.4N on HP1.'
        study.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    result_dir=folder/phase
    result_dir.mkdir(exist_ok=True)
    entry={'part':name,'started':time.time(),'status':'running'};state['runs'].append(entry);save()
    args=[sys.executable,'-m','topopt','run',str(study),'--model',str(result_dir),'--iters','80']
    if phase=='exploration':args.append('--quick')
    else:args.append('--converge')
    entry['command']=args;save()
    print('START',name,phase,flush=True)
    with (result_dir/'run.log').open('w',encoding='utf-8') as log:
        p=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT,cwd=ROOT)
        entry['pid']=p.pid;save();code=p.wait()
    entry.update(status='finished',exit_code=code,finished=time.time());save()
    print('FINISH',name,code,flush=True)
state['finished']=time.time();save()
print('QUEUE FINISHED',flush=True)
