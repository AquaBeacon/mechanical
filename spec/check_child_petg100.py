"""Close the CAD review loop, then screen actual manufactured geometry."""
from pathlib import Path
import json, os, subprocess, sys
import trimesh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_petg100_design'
os.environ['PYTHONIOENCODING']='utf-8'
names=['child_jaw_gate','child_core_frame','child_cam_bridge']
metrics={}
for name in names:
    folder=OUT/name;p=folder/f'{name}.scad';s=p.read_text(encoding='utf-8')
    if name=='child_jaw_gate':
        s=s.replace('box3([-88,0,ds_z0],[-50,30,ds_z1]);','box3([-72,10,ds_z0],[-50,30,ds_z1]);')
    if name=='child_core_frame':
        s=s.replace('translate([ds_x0, 0, ds_z0]) cube([hinge_x + knu_od/2 + 1 - ds_x0, hinge_y + knu_od/2 + 1, ds_z1 - ds_z0]);',
                    'translate([hinge_x-knu_od/2, 0, ds_z0]) cube([knu_od+1, hinge_y+knu_od/2+1, ds_z1-ds_z0]);')
        s=s.replace('small_holes();scene_voids();','small_holes();scene_voids();grooves();tie_slots();tie_backspace();cable_cavity();hand_room();')
    if name!='child_cam_bridge':
        p.write_text(s,encoding='utf-8')
        with (folder/'manufactured.log').open('w',encoding='utf-8') as log:
            subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(folder/'manufactured.stl'),'-D','part="manufactured"',str(p)],stdout=log,stderr=log,check=True)
    m=trimesh.load(folder/'manufactured.stl',force='mesh')
    metrics[name]={'volume_cm3':float(m.volume/1000),'mass_kg':float(m.volume*1.27e-6),'watertight':bool(m.is_watertight),
                   'bounds_mm':m.bounds.tolist(),'shell_volumes_cm3':[float(c.volume/1000) for c in m.split()]}
    assert m.is_watertight
(OUT/'geometry_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
bm=metrics['child_cam_bridge']['mass_kg'];gm=metrics['child_jaw_gate']['mass_kg']
for name in names:
    folder=OUT/name
    for fn in ['fea.json','search.json']:
        p=folder/fn;d=json.loads(p.read_text(encoding='utf-8'))
        if name!='child_cam_bridge':
            for key in ['pocket_bot','pocket_top','band_mid']:
                old=d['regions'][key]
                d['regions'][key]={'type':'cylinder','axis':'Z','centre':[0,0,0],'r':62.35 if key!='band_mid' else 60.35,'range':[old['min'][2],old['max'][2]]}
            d['_contact_support']='Rigid vessel/EVA approximation, only inner radial contact layer, not entire thickened band. Pocket r<=62.35; mid-band r<=60.35. Real EVA/contact compliance remains unmeasured.'
        if name=='child_jaw_gate':
            f=(bm+.35)*9.81*3
            for ld in d['cases'][0]['loads']:ld['force']=[0,0,-f/2]
        elif name=='child_core_frame':
            f=(gm+bm+.35)*9.81*3
            for ld in d['cases'][0]['loads']:
                if ld['region'] in ['latch_lo','latch_hi']:ld['force']=[0,0,-f/2]
        p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for name in names:
    folder=OUT/name;dest=folder/'screening';dest.mkdir(exist_ok=True)
    args=[sys.executable,'-m','topopt','fea',str(folder/'fea.json'),'--out',str(dest),'--voxel','3','--no-png']
    print('FEA',name,flush=True)
    with (dest/'run.log').open('w',encoding='utf-8') as log:
        result=subprocess.run(args,stdout=log,stderr=log,cwd=ROOT)
    print('EXIT',name,result.returncode,flush=True)
