"""Exact BRep fit and full vertical floor insertion against the corrected case."""
from parent_access_common import *
import sys
sys.path.insert(0,str(R/'scad/lib'));import parent_gnss as G
out=O/('_work/analysis/fixed_plates_20261011' if '--fixed-plates' in sys.argv else '_work/analysis/corner_mounts_20261011' if '--corner-mounts' in sys.argv else '_work/analysis/case_cad_correction_20261010');out.mkdir(parents=True,exist_ok=True)
d,c=load();case=c['box_bcas212310g'];rows=[]
case_dimensions=json.loads((R/'parts/parent/exterior/cots/bcas212310g/dimensions.json').read_text(encoding='utf-8'))
boss_top=case_dimensions['boss_top_z_mm']
names=['plate','p_main','p_pwr','tx_improved','spresense','lipo_tray','lipo_ret_lid','gnss_universal_carrier','antenna_rack','coax_ring','magnetometer']+corner_fixtures(c)+[n for n in c if n.startswith(('gnss_column_','sony_column_'))]
for n in names:
    volume=common(c[n],case)
    detail=[]
    if volume>.01:
        for s in c[n].common(case).Solids:
            b=s.BoundBox;detail.append(dict(mm3=s.Volume,bbox_mm=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]))
    rows.append(dict(part=n,overlap_mm3=volume,pass_=volume<.01,detail=detail))
print(json.dumps([r for r in rows if not r['pass_']],indent=2),flush=True)
# Exact swept union: extruding all the floor's faces parallel to Z covers every
# point traversed, including integral PWR/TX posts. Never substitute its bbox.
floor=c['plate'];sweep_parts=[]
if '--no-sweep' not in sys.argv:
    for face in floor.Faces:
        if abs(face.normalAt(0,0).z)>1e-6:
            try:sweep_parts.append(face.extrude(v(0,0,100)))
            except Part.OCCError:pass
    # Overlapping compounds may produce signed-volume artifacts. Check each
    # positive valid prism independently, as in the assembly path verifier.
    vol=common(floor,case)
    for prism in sweep_parts:
        if prism.Volume<0:prism.reverse()
        assert prism.isValid() and prism.Volume>0
        vol+=common(prism,case)
    rows.append(dict(part='floor vertical insertion from above',overlap_mm3=vol,pass_=vol<.01))
for i,(x,y) in enumerate(G.CASE_ANCHOR_XY):
    # Recesses create contact at the actual boss top, with no floating gap.
    contact=floor.distToShape(Part.makeCylinder(3,.01,v(x,y,boss_top-.01)))[0]
    rows.append(dict(part='anchor bearing '+str(i),gap_mm=contact,pass_=contact<.011))
data=dict(status='PASS' if all(r['pass_'] for r in rows) else 'FAIL',checks=rows,source='Actual current placement and drawing-derived BCAS STEP',limitations=['Unsectioned corner draft and physical molding tolerances remain unverified.','The body/corner profile must be checked against physical case or vendor STEP before printing release.'])
(out/('case_fit_before.json' if '--before' in sys.argv else 'case_fit_checks.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(data['status']);print(json.dumps([r for r in rows if not r['pass_']],indent=2))
if '--before' not in sys.argv:assert data['status']=='PASS'
