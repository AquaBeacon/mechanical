"""Run existing access checks together with the measured sensor fixture checks."""
from pathlib import Path
import json, runpy, sys, traceback
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'spec'))
import parent_access_common as C
O=C.O; W=O/'_work/analysis/sensor_mounts_20261011'
placement,scene=C.load()
def isolated_scene(name='placement.json'):
    if name!='placement.json':return original_load(name)
    return placement,{n:s.copy() for n,s in scene.items()}
original_load=C.load;C.load=isolated_scene
known=['verify_parent_sensor_mounts','verify_parent_magnetometer_access','verify_parent_gnss_access','verify_parent_switch_tx_access','verify_parent_battery_sd_access','verify_parent_wave_assembly']
# FreeCADCmd includes its own script path and --pass in sys.argv.
selected=[a for a in sys.argv if a in known] or known
previous=W/'validation_run.json'
results=json.loads(previous.read_text())['checks'] if len(selected)<len(known) and previous.exists() else []
results=[r for r in results if r['check'] in known and r['check'] not in selected]
for name in selected:
    print('CHECK START',name,flush=True)
    try:
        runpy.run_path(str(R/'spec'/(name+'.py')),run_name='__main__')
        results.append(dict(check=name,status='PASS'))
    except Exception:
        results.append(dict(check=name,status='FAIL',error=traceback.format_exc()))
        print(results[-1]['error'],flush=True)
    print('CHECK END',results[-1]['status'],name,flush=True)
report=dict(status='PASS' if all(r['status']=='PASS' for r in results) else 'FAIL',checks=results)
(W/'validation_run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('SENSOR REVISION',report['status'],flush=True)
