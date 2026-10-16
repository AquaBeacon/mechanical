"""Prepare isolated setup inputs; never run optimisation."""
from pathlib import Path
import json, re, shutil, subprocess, sys, os

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assemblies/child_frame2_assembly/topopt_review_20260910'
PARTS = ROOT / 'parts/child/exterior/printed'
os.environ['PYTHONIOENCODING'] = 'utf-8'
models = [('child_core_frame','topo_v5','child_core_frame_v5'),
          ('child_jaw_gate','topo_v1','child_jaw_gate_v1'),
          ('child_cam_bridge','topo_v1','child_cam_bridge_v1')]

for name, old, base in models:
    source = PARTS / name / old
    dest = OUT / name
    geo = dest / 'inputs'
    geo.mkdir(parents=True, exist_ok=True)
    data = json.loads((source / f'{base}_study.json').read_text(encoding='utf-8'))
    data['_review_status'] = 'Setup review only; optimisation not authorised. 2026-09-10.'
    data['_what'] = name + ': current interface setup review, not a finished part'
    data['design']['filter_mm'] = 9.0
    data['design']['symmetry'] = []
    data['_review_changes'] = 'Filter 9 mm = 3 voxels; no imposed symmetry for asymmetric loads. Historical interfaces retained except current gate v3 latch.'
    scad = (source / f'{base}.scad').read_text(encoding='utf-8')
    scad = re.sub(r'use <[^>]*hardpoint.scad>', f'use <{(ROOT / "scad/lib/hardpoint.scad").as_posix()}>', scad)
    if name == 'child_jaw_gate':
        scad = re.sub(r'boss_y1\s*=\s*16;', 'boss_y1 = 24;', scad)
        scad = re.sub(r'boss_h\s*=\s*24;', 'boss_h = 34;', scad)
        # Current v3 has a flat seat, no recessed knob pocket.
        start = scad.index('        translate([latch_hx, boss_y1, z]) rotate([90, 0, 0]) union()')
        end = scad.index('\n    }\n    hp_holes();', start)
        scad = scad[:start] + scad[end:]
        original = 'translate([boss_x0, 0, z - boss_h/2]) cube([boss_x1 - boss_x0, boss_y1, boss_h]);'
        replacement = '''difference() {
            translate([boss_x0, 0, z - boss_h/2]) cube([boss_x1-boss_x0,boss_y1,boss_h]);
            bd = (boss_y1-16)*sqrt(2);
            translate([boss_x0-1,16,z-boss_h/2]) rotate([-45,0,0])
                translate([0,-bd,-bd]) cube([boss_x1-boss_x0+2,bd,bd]);
        }'''
        assert original in scad
        scad = scad.replace(original, replacement)
        for region, z in [('latch_lo',40),('latch_hi',170)]:
            # Surface slab including one voxel below the flat y=24 seat.
            data['regions'][region] = {'type':'box','min':[52,20,z-8],'max':[72,24.5,z+8]}
        data['_preserve'] = 'Historical functional bands / HP seats / hinge; latch replaced by v3 flat y24 seat, h34 with underside chamfer; no knob pocket.'
        data['_obstacle'] += ' REVIEW UPDATE: knob access now starts at y24; old y16 pocket removed.'
    scad_path = geo / 'geometry.scad'
    scad_path.write_text('// REVIEW INPUT: generated from historical setup; v3 latch updated.\n'+scad, encoding='utf-8')
    for kind in ['preserve','obstacle','design_space','preserve_cuts']:
        target = geo / f'{kind}.stl'
        if name != 'child_jaw_gate':
            shutil.copy2(source/'02_setup'/f'{base}_{kind}.stl', target)
        else:
            with (geo/f'{kind}.log').open('w', encoding='utf-8') as log:
                subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(target),'-D',f'part="{kind}"',str(scad_path)],stdout=log,stderr=log,check=True)
        print(name, kind, flush=True)
    data['geometry']['preserve'] = {'interfaces':'inputs/preserve.stl'}
    data['geometry']['obstacle'] = {'keep_out':'inputs/obstacle.stl'}
    data['geometry']['design_space'] = 'inputs/design_space.stl'
    data['finish']['add'] = {'interfaces':'inputs/preserve.stl'}
    data['finish']['cut'] = {'features':'inputs/preserve_cuts.stl'}
    data['_geometry_source'] = 'inputs/geometry.scad; core/bridge meshes copied from historical interface envelopes, gate meshes re-rendered for v3.'
    study = dest / 'study.json'
    study.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SETUP',name,flush=True)
    with (dest/'setup.log').open('w',encoding='utf-8') as log:
        result = subprocess.run([sys.executable,'-m','topopt','setup',str(study),'--out',str(dest/'setup'),'--iters','80'],stdout=log,stderr=log)
    print('SETUP EXIT',name,result.returncode,flush=True)
