"""Bounded foundation build/validation for the straight-up battery lid."""
from pathlib import Path
from datetime import datetime, timezone
import json, sys, subprocess, shutil, time
R=Path(__file__).resolve().parents[1]
W=R/'assemblies/parent_hand_service/_work/analysis/battery_top_lid_20261029'
def write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    W.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(R/'tools/cad_foundation'))
    from service import CadService
    processes=[]; original=subprocess.Popen
    def tracked(*args,**kw):
        p=original(*args,**kw)
        processes.append((p,dict(pid=p.pid,start_utc=datetime.now(timezone.utc).isoformat(),command=args[0] if args else kw.get('args'),owner='battery_top_lid_20261029')))
        write(W/'processes.json',[d for p,d in processes]);return p
    subprocess.Popen=tracked
    deps=['spec/build_parent_hand_service.py','scad/lib/parent_gnss.py','scad/lib/cad_edge_finish.py','scad/lib/parent_case_access.py','scad/lib/parent_battery_slide.py','parts/child/interior/printed/child_vtray_batt_floor/child_vtray_batt_floor.scad','parts/parent/interior/printed/parent_lipo_retainer/dimensions.json','parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer_pads.step']
    generator='spec/build_parent_battery_top_lid.py';params={};key='build'
    if '--refresh' in sys.argv:
        key='refresh';generator='spec/refresh_parent_battery_siblings.py';deps=[]
        d=json.loads((R/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
        for item in d['items']:
            if item.get('print'):
                n=item.get('file',item['part'].split('/')[-1]);p=item['part']+'/'+n+'.step'
                params[n]=p;deps.append(p)
    if '--verify' in sys.argv:
        key='verify';generator='spec/verify_parent_battery_top_lid.py'
        layout=R/'assemblies/parent_hand_service/placement.json'
        deps+=['spec/parent_access_common.py',layout.relative_to(R).as_posix()]
        deps += [(Path(i['part'])/(i.get('file',Path(i['part']).name)+'.step')).as_posix() for i in json.loads(layout.read_text(encoding='utf-8'))['items']]
        for name in ['battery_base','parent_lipo_retainer_lid_slide']:
            rel='assemblies/parent_hand_service/_work/intermediate/top_lid_'+name+'.step'
            deps.append(rel);params[name]=rel
    try:
        for attempt in range(21):
            try:
                result=CadService(root=R).build_native(generator,parameters=params,dependencies=sorted(set(deps)),timeout=240)
                break
            except RuntimeError as exc:
                if 'batch is busy' not in str(exc) or attempt==20:raise
                print('Waiting for shared CAD batch',flush=True);time.sleep(15)
        write(W/(key+'_run.json'),result)
        if key=='build' and result['status']=='passed':
            for name,row in result['exports'].items():
                target=R/'assemblies/parent_hand_service/_work/intermediate'/('top_lid_'+name+'.step')
                target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(row['step'],target)
        if key=='refresh' and result['status']=='passed':
            for name,row in result['exports'].items():shutil.copyfile(row['stl'],(R/params[name]).with_suffix('.stl'))
        print(json.dumps(result,ensure_ascii=False),flush=True)
    finally:
        for p,d in processes:d.update(exit_code=p.poll(),ended_utc=datetime.now(timezone.utc).isoformat())
        write(W/'processes.json',[d for p,d in processes])
if __name__=='__main__':main()
