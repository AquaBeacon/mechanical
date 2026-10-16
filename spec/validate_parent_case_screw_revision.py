"""Current case-access revision: reuse existing geometry/assembly validators."""
from pathlib import Path
import sys,json,runpy,os,io,contextlib,traceback
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'spec'))
import parent_access_common as C
O=C.O;D=O/'_work/analysis/case_screw_access_20261012'
placement,scene=C.load();original_load=C.load
def cached(name='placement.json'):
    return (placement,{n:s.copy() for n,s in scene.items()}) if name=='placement.json' else original_load(name)
C.load=cached
known=['verify_parent_case_screw_access','verify_parent_magnetometer_access','verify_parent_gnss_access','verify_parent_switch_tx_access','verify_parent_battery_sd_access','verify_parent_wave_assembly','verify_parent_wave_retention']
selected=[name for name in sys.argv if name in known] or known
checks=[]
for name in known:
    if name in selected:continue
    log=(D/(name+'.log')).read_text(encoding='utf-8')
    checks.append(dict(check=name,status='FAIL' if 'Traceback' in log else 'PASS'))
for name in selected:
    out=io.StringIO();status='PASS'
    try:
        with contextlib.redirect_stdout(out):runpy.run_path(str(R/'spec'/(name+'.py')),run_name='__main__')
    except Exception:
        status='FAIL';out.write(traceback.format_exc())
    (D/(name+'.log')).write_text(out.getvalue(),encoding='utf-8')
    checks.append(dict(check=name,status=status));print(name,status,flush=True)
    (D/'validation_run.json').write_text(json.dumps(dict(status='PASS' if all(q['status']=='PASS' for q in checks) else 'FAIL',checks=checks),indent=2),encoding='utf-8')
if '--checks-only' in sys.argv:
    assert all(q['status']=='PASS' for q in checks)
    raise SystemExit(0)
for pose,name in [('closed','placement.json'),('service','service_placement.json')]:
    os.environ.update(ASM_JSON=str(O/name),ASM_ROOT=str(R),STEP_OUT=str(O/(pose+'.step')))
    out=io.StringIO()
    with contextlib.redirect_stdout(out):runpy.run_path(str(R/'scad/lib/asm_to_step.py'),run_name='__main__')
    (D/(pose+'_export.log')).write_text(out.getvalue(),encoding='utf-8')
for stem in ['main_mount_plate','battery_base','ann_mb1_coax_ring']:
    sys.argv=['verify_parent_hand_service.py','--part',stem,'--no-assemblies']
    try:runpy.run_path(str(R/'spec/verify_parent_hand_service.py'),run_name='__main__')
    except SystemExit as e:assert e.code in [None,0]
sys.argv=['verify_parent_hand_service.py','--assembly-only']
runpy.run_path(str(R/'spec/verify_parent_hand_service.py'),run_name='__main__')
out=dict(status='PASS' if all(q['status']=='PASS' for q in checks) else 'FAIL',checks=checks)
(D/'validation_run.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
assert out['status']=='PASS'
