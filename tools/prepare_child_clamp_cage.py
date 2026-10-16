"""Author/render the connected three-band cage study; native topopt does FEA.

Geometry and interface values come from the existing canonical SCAD echo.
Historical single-clamp studies are intentionally left untouched.
"""
from pathlib import Path
import ast
import hashlib
import json
import math
import subprocess
import argparse

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE = PART / '_work/analysis/connected_cage_rubber1_v065'
SCAD = PART / 'child_wte4_suspension_clamp.scad'
OPENSCAD = r'C:\Program Files\OpenSCAD\openscad.com'


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def main():
    global CASE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case')
    parser.add_argument('--parameters', type=Path)
    parser.add_argument('--volfrac', type=float, default=.65)
    parser.add_argument('--symmetry-x', action='store_true')
    parser.add_argument('--incremental-cases', action='store_true',
                        help='Add handling increments; retain every combined preload case')
    args = parser.parse_args()
    if args.case:
        if Path(args.case).name != args.case: raise ValueError('Case must be a basename')
        CASE = PART/'_work/analysis'/args.case
    if (CASE/'study_cage.json').exists(): raise FileExistsError('Preserve previous study')
    CASE.mkdir(parents=True, exist_ok=True)
    parameters = json.loads(args.parameters.read_text(encoding='utf-8')) if args.parameters else {}
    save(CASE/'design_parameters.json', parameters)
    defines = [arg for key,value in parameters.items() for arg in ['-D',key+'='+json.dumps(value)]]
    rendered = {}
    for name, model in [('design_space', 'cage_space'), ('preserve', 'cage_preserve'), ('cuts', 'cage_cuts')]:
        cmd = [OPENSCAD, '-o', str(CASE/(name+'.stl')), '-D', f'model="{model}"', *defines, str(SCAD)]
        run = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        rendered[name] = run.stdout+run.stderr
        (CASE/(name+'_render.log')).write_text(rendered[name], encoding='utf-8')
        run.check_returncode()
    def echo(tag):
        line = next(x[6:] for x in rendered['design_space'].splitlines() if x.startswith(f'ECHO: ["{tag}"'))
        values = ast.literal_eval(line)
        return dict(zip(values[1::2], values[2::2]))
    d, c = echo('CLAMP_INTERFACE'), echo('CAGE_INTERFACE')
    save(CASE/'interface.json', {'clamp': d, 'cage': c})
    regions = {}
    # Eye skin selected through the full width, including a finite bearing patch.
    regions['rope_pin'] = dict(type='cylinder', axis='X', centre=c['eye'],
        r=c['rope_hole_d']/2+2.0, range=[-c['eye_width']/2-.1, c['eye_width']/2+.1])
    contact = []
    washers = []
    preload = 150.0
    angles = [math.radians(-15-30*i) for i in range(6)]
    radial = 4*preload/-sum(math.sin(a) for a in angles)
    # Six separated near-seat patches per band, never extending into free shell.
    for ib, centre in enumerate(c['centres']):
        z0 = centre-d['band_width']/2
        for ia, angle in enumerate(angles):
            name = f'contact_{ib}_{ia}'
            regions[name] = dict(type='cylinder', axis='Z',
                centre=[(d['inner_r']-7)*math.cos(angle), (d['inner_r']-7)*math.sin(angle), 0],
                r=10, range=[centre-d.get('contact_width',d['band_width'])/2+4,
                            centre+d.get('contact_width',d['band_width'])/2-4])
            contact.append((ib, name, angle))
        for ix, x in enumerate([-d['bolt_x'], d['bolt_x']]):
            for iz, z in enumerate(d['bolt_zs']):
                name = f'washer_{ib}_{ix}_{iz}'
                regions[name] = dict(type='cylinder', axis='Y', centre=[x, 0, z0+z], r=6,
                    range=[-d['ear_t']-d.get('split_gap',1.6)/2-.05,
                           -d['ear_t']-d.get('split_gap',1.6)/2+2.05])
                washers.append(name)
    support = [dict(region='rope_pin', fix='xyz')]
    weight = 4*9.80665
    # One half and its one eye carry the whole 4 kg, including printed hardware.
    # Clamp sharing: worst band 50%, other two 25%; evaluate all three locations.
    def loads(shares, force, tight=True):
        result = [dict(region=n, force=[0, preload, 0]) for n in washers] if tight else []
        for ib, name, a in contact:
            f = [shares[ib]*v/6 for v in force]
            if tight:
                f[0] += radial*math.cos(a)
                f[1] += radial*math.sin(a)
            result.append(dict(region=name, force=f))
        return result
    cases = []
    def case(name, force, shares, tight=True, abnormal=False):
        cases.append(dict(name=name, load_class='abnormal' if abnormal else 'normal',
            supports=support, loads=loads(shares, force, tight)))
    case('preload_only', [0, 0, 0], [1/3]*3)
    for ib in range(3):
        shares = [.25]*3
        shares[ib] = .5
        case(f'lift_static_band{ib+1}', [0, 0, -weight], shares)
        case(f'lift_2g_band{ib+1}', [0, 0, -2*weight], shares, abnormal=True)
    for direction in [-1, 1]:
        case(f'skew_x_{direction:+d}_2g', [direction*weight, 0, -2*weight], [.5,.25,.25], abnormal=True)
    for direction in [-1, 1]:
        case(f'skew_y_{direction:+d}_2g', [0, direction*weight, -2*weight], [.5,.25,.25], abnormal=True)
    if args.incremental_cases:
        # Separate incremental compliance keeps the shared 150 N/bolt preload
        # from dominating every normalised objective. Combined cases stay intact.
        for ib in range(3):
            shares=[.25]*3
            shares[ib]=.5
            case(f'increment_lift_2g_band{ib+1}',[0,0,-2*weight],shares,tight=False,abnormal=True)
        for axis in ['x','y']:
            for direction in [-1,1]:
                force=[direction*weight,0,-2*weight] if axis=='x' else [0,direction*weight,-2*weight]
                case(f'increment_skew_{axis}_{direction:+d}_2g',force,[.5,.25,.25],tight=False,abnormal=True)
    study = dict(units='mm_N_MPa', material='BAMBU-PETG-BASIC', build_axis='Y', raster_axis='Z',
        infill=1.0, walls=8, printer='X1C', safety_factor=3.0, max_deflection_mm=1.0,
        voxel_mm=2.0, regions=regions, cases=cases, required_cases=[x['name'] for x in cases],
        geometry=dict(design_space=str(CASE/'design_space.stl'),
            preserve={'functional_interfaces': dict(stl=str(CASE/'preserve.stl'), attach=[dict(type='all')])},
            obstacle={'exact_voids': str(CASE/'cuts.stl')}, clearance_mm=0),
        design=dict(volfrac=args.volfrac, filter_mm=6.0, overhang=False, symmetry=['X'] if args.symmetry_x else [], optimizer='mma',
            stress=dict(safety_factor=3.0, p_norm=8, relax_q=.5, samples='all')),
        finish=dict(voxel_mm=1.0, smooth_mm=1.0,
            add={'functional_interfaces': str(CASE/'preserve.stl')},
            cut={'exact_voids': str(CASE/'cuts.stl')}),
        _what='Three M3 clamp bands connected by native stress-constrained topology with a 10.5mm lifting eye on each mounting-face half.',
        _why='Confirmed 1mm rubber; provisional 20% compression. 4kg completed vessel; full load on ONE half/eye conservatively. 2g handling inherited.',
        _boundary='Rigid pin skin at the ONE lifting eye. All three bands transfer friction loads to this eye; no frame screws or cap screws fixed. Balanced per-band clamping washer/seat preload. Surface mapping on independent CCX.',
        _limits='Provisional rubber pressure/friction and dry short-term PETG card. Pin constraint does not model rope bearing/contact or full mating-half flexibility. No wet slip, creep or impact proof.',
        _orientation='Rotate source cage +90deg about X, then translate to bed; source Y build axis, Z raster. Main lifting axis Z is within layer plane.',
        _interfaces='Reuse canonical M3 four-hole pads, 3.5mm clearances, 36x16 pitch; no new mating hardware. Eye diameter is unthreaded M10-size 10.5mm, two identical halves.',
        _material_card=str(PART/'spec/bambu_petg_basic_material.json'),
        _source_sha256=hashlib.sha256(SCAD.read_bytes()).hexdigest())
    save(CASE/'study_cage.json', study)
    solid = {k:v for k,v in study.items() if k not in ['geometry','design','finish','voxel_mm']}
    solid.update(part=str(CASE/'design_space.stl'),resolution_mm=2.0)
    save(CASE/'study_solid_bound.json',solid)
    print(CASE/'study_cage.json')


if __name__ == '__main__':
    main()
