"""Actual STEP checks for case anchoring and wave-retention interfaces."""
from parent_access_common import *
import sys
sys.path.insert(0,str(R/'scad/lib'));import parent_gnss as G
d,c=load();rows=[];access=[]
case_dims=json.loads((R/'parts/parent/exterior/cots/bcas212310g/dimensions.json').read_text(encoding='utf-8'))
boss_top=case_dims['boss_top_z_mm']
for i,(x,y) in enumerate(G.CASE_ANCHOR_XY):
 n='case_anchor_'+str(i)
 if n not in c:continue
 bolt=c[n];b=bolt.BoundBox
 probe=Part.makeCylinder(2.1,G.CASE_ANCHOR_SEAT_Z-boss_top-.01,v(x,y,boss_top+.01))
 bore_volume=common(probe,c['plate'])
 head=Part.makeCylinder(3.9,2.2,v(x,y,G.CASE_ANCHOR_SEAT_Z))
 head_overlap=common(head,c['plate'])
 obstacles=collisions(bolt,c,[n,'plate','box_bcas212310g'])
 engagement=boss_top-b.ZMin
 rows.append(dict(name=n,axis_xy_mm=[x,y],head_top_mm=b.ZMax,nominal_case_engagement_mm=engagement,floor_bore_overlap_mm3=bore_volume,head_recess_overlap_mm3=head_overlap,collisions=obstacles,pass_=not obstacles and bore_volume<.01 and head_overlap<.01 and abs(b.ZMax-19)<.01 and 4<engagement<7))
 tool=Part.makeCylinder(2,100-19,v(x,y,19))
 own=common(tool,c['plate'])
 rows.append(dict(name=n+' driver clears integral floor posts',overlap_mm3=own,pass_=own<.01))
 access.append(dict(anchor=n,remove_before_driver=[q['part'] for q in collisions(tool,c,[n,'box_bcas212310g','coax_coil_keepout','tx_top_keepout'])]))
for n in ['plate','gnss_universal_carrier','antenna_rack','coax_ring',]+corner_fixtures(c)+[n for n in c if n.startswith(('gnss_column_','sony_column_'))]:
 rows.append(dict(name=n+' valid single solid',pass_=c[n].isValid() and len(c[n].Solids)==1))
# Every new split retains a shaped locator and the existing axial through-bolt.
# Test its clearance and a0.3mm lateral movement that must meet the pocket wall.
for host,moving in [(sony_corner_for_foot(i),'sony_column_'+str(i)) for i in range(4)]+[('coax_ring','antenna_rack')]+[('gnss_universal_carrier','gnss_column_'+str(i)) for i in range(4)]:
 fitted=common(c[host],c[moving])
 shifted=c[moving].copy();shifted.translate(v(.3,0,0));stop=common(c[host],shifted)
 rows.append(dict(name=moving+' keyed split clearance/translation stop',installed_overlap_mm3=fitted,shift_0_3mm_overlap_mm3=stop,pass_=fitted<.1 and stop>.1))
out=dict(status='PASS' if all(r['pass_'] for r in rows) else 'FAIL',checks=rows,case_anchor_service=access,
 limitations=['Drawing-derived insert top Z10; screw/pilot geometric overlap is not thread engagement analysis. Exact insert depth and selected screw require physical confirmation.','Anchor driver access requires the listed obstructions removed; not a one-piece interior extraction procedure.','Carrier long bolts use16 top-loaded M3 metal nuts. Torque, creep, loosening and physical wave-cycle retention unmeasured.','Lacing is soft cord, packed inside the user coil envelope including knots; actual installation/clearance required.'])
(O/'wave_retention_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(out['status'],[r for r in rows if not r['pass_']]);assert out['status']=='PASS'
