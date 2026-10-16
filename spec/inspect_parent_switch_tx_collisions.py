"""Diagnose exact interference locations without changing CAD."""
from parent_access_common import *
d,c=load()
for a,b in [('plate','box_bcas212310g'),('sony_upper_carrier','box_bcas212310g'),('gnss_universal_carrier','box_bcas212310g'),('main_lower_carrier','antenna_rack'),('main_carrier_mount_2','antenna_rack')]:
    sh=c[a].common(c[b]);print(a,b,'volume',sh.Volume,flush=True)
    for p in sh.Solids:print('intersection',p.BoundBox,flush=True)
for n in ['SW_PWR','SW_TX']:
    x,y=([27.26,199.54] if n=='SW_PWR' else [57.34,130.46])
    finger=Part.makeCylinder(10,73,v(x,y,47))
    for i,p in enumerate(c['p_pwr'].Solids):
        if common(p,finger)>.1:print(n,'PWR part',i,p.BoundBox,flush=True)
