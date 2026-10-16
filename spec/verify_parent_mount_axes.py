"""Check generated mounting axes pass through the actual imported PCB holes."""
from parent_access_common import *
import sys
sys.path.insert(0,str(R/'scad/lib'))
import parent_gnss as G
d,c=load();holes=json.loads((O/'hole_sources.json').read_text(encoding='utf-8'));rows=[]
for key,host,z,diam in [('MAIN','p_main',G.MAIN_ORIGIN[2],3.0),('PWR','p_pwr',G.PWR_ORIGIN[2],3.0),('TX','tx_improved',G.TX_ORIGIN[2],3.0),('SONY','spresense',G.SONY_ORIGIN[2],2.4)]:
    for i,(x,y) in enumerate(holes[key]):
        probe=Part.makeCylinder(diam/2,1.4,v(x,y,z+.1));vol=common(probe,c[host])
        rows.append(dict(board=key,hole=i,xy_mm=[x,y],axis_probe_diameter_mm=diam,board_intersection_mm3=vol))
report=dict(status='PASS' if all(r['board_intersection_mm3']<.01 for r in rows) else 'FAIL',checks=rows,scope='Clear axis and stated shaft diameters through imported PCB substrate; thread retention and clamp torque are not structural verification.')
(O/'mount_axis_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report['status'],[r for r in rows if r['board_intersection_mm3']>=.01],flush=True)
assert report['status']=='PASS'
