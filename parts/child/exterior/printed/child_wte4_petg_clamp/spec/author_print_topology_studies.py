"""Author native topopt studies; contains no solver or reconstructed structure."""
from pathlib import Path
import json
import numpy as np
import trimesh

PART = Path(__file__).resolve().parents[1]
INPUT = PART / '_work/analysis/topology_print'

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    request_path = PART/'spec/print_topology_request.json'
    request = json.loads(request_path.read_text(encoding='utf-8'))
    request['status'] = 'load_conditions_confirmed_setup_pending'
    request['confirmed'].update(supported_mass_upper_bound_kg=1.0,
        handling_acceleration_g=2.0, handling_resultant_N=19.6133)
    request['provisional'].update(required_safety_factor=2.0,
        bolt_preload_sensitivity_N_per_bolt=[50, 100, 150],
        material_card='generic PETG orthotropic; not measured X1C properties')
    request['missing'] = []
    request['note'] = 'User mass <1 kg and 2x handling bound, 2026-10-08. Preload is an assumption, not a torque specification. Production adoption requires finished geometry checks.'
    save(request_path, request)
    regions = {}
    for station, z in enumerate([0, 120]):
        regions[f'mount{station}'] = dict(type='box', min=[-28,59,z+2], max=[28,64,z+38])
        regions[f'crown{station}'] = dict(type='box', min=[-12,56,z+3], max=[12,62,z+37])
        regions[f'contact{station}'] = dict(type='cylinder', axis='Z', centre=[0,0,0], r=61.95, range=[z+.1,z+39.9])
        for side, x in [('left',-67.8481282),('right',67.8481282)]:
            regions[f'{side}_ear{station}'] = dict(type='box', min=[x-10,11,z+3], max=[x+10,15,z+37])
        for side, x in [('left',-42),('right',42)]:
            regions[f'{side}_shoulder{station}'] = dict(type='box', min=[x-4,38,z+3], max=[x+4,46,z+37])
        for bolt, (x, axial) in enumerate([(-67.8481282,10),(-67.8481282,30),(67.8481282,20)]):
            regions[f'bolt_seat{station}_{bolt}'] = dict(type='box',
                min=[x-4,13,z+axial-4],max=[x+4,15,z+axial+4])
    regions['join_surfaces'] = dict(type='box', min=[-83,.8,-1], max=[83,62.8,161])
    supports = [dict(region=f'mount{i}',fix='xyz') for i in [0,1]]
    cases=[]
    # Area centroids of actual preserved CAD patches give the force-couple arms.
    # Net force and moment are audited independently; voxel discretisation is
    # checked again by setup/final FEA rather than mistaken for exact contact.
    preserved = trimesh.load(INPUT/'upper_preserve.stl',force='mesh')
    def centre(region):
        r=regions[region]
        box=trimesh.creation.box(extents=np.subtract(r['max'],r['min']),
            transform=trimesh.transformations.translation_matrix(np.add(r['min'],r['max'])/2))
        patch=trimesh.boolean.intersection([preserved,box],engine='manifold')
        return patch.center_mass
    centres={name:centre(name) for name in regions if 'crown' in name or 'shoulder' in name}
    crown_y=float(np.mean([centres[f'{side}_shoulder{i}'][1] for i in [0,1] for side in ['left','right']]))
    shoulder_arm=float(np.mean([centres[f'right_shoulder{i}'][0]-centres[f'left_shoulder{i}'][0] for i in [0,1]]))
    axial_arm=float(centres['crown1'][2]-centres['crown0'][2])
    def remote_loads(axis):
        force=[0.,0.,0.]; force[axis]=19.6133/4
        loads=[dict(region=f'{side}_shoulder{i}',force=force.copy()) for i in [0,1] for side in ['left','right']]
        if axis==0:
            q=19.6133*crown_y/(2*shoulder_arm)
            loads += [dict(region=f'{side}_shoulder{i}',force=[0,sign*q,0])
                for i in [0,1] for side,sign in [('left',-1),('right',1)]]
        elif axis==2:
            q=19.6133*crown_y/axial_arm
            loads += [dict(region=f'{side}_shoulder{i}',force=[0,sign*q/2,0])
                for i,sign in [(0,-1),(1,1)] for side in ['left','right']]
        return loads
    for axis in range(3):
        cases.append(dict(name=f'handling_{"XYZ"[axis]}_2g', supports=supports,
            loads=remote_loads(axis)))
    # A temporarily unsupported station during handling exercises the axial link.
    # Same full 2g resultant at the vessel centre, with only station 0 attached.
    for axis in [0,1,2]:
        cases.append(dict(name=f'one_station_transfer_{"XYZ"[axis]}_2g',
            supports=[dict(region='mount0',fix='xyz')],
            loads=remote_loads(axis)))
    cases.append(dict(name='assumed_preload_150N_per_bolt',
        supports=[dict(region=f'contact{i}',fix='xyz') for i in [0,1]],
        loads=[dict(region=f'bolt_seat{i}_{bolt}', force=[0,-150,0])
               for i in [0,1] for bolt in range(3)]))
    for half in ['upper','lower']:
        preserve = str(INPUT/f'{half}_preserve.stl')
        study = dict(
            _what=f'{half} linked clamp, vertical X1C printing',
            _why='Minimise material with an actual density field and self support; keep the rubber skin, mount faces, ears, bores and nut entries.',
            _not_a_part='exploration_only until smoothing, exact interfaces, connectedness, finished CCX convergence and slicer validation pass',
            _load_basis='User: vessel plus contents <1 kg; 2x selfweight sufficient. Bound =19.6133 N at [0,0,80], transferred by force couples to actual preserved contact patches. Signs reverse in linear elasticity. One-station cases represent temporary attachment during assembly.',
            _preload='150 N/bolt provisional upper sensitivity bound (50/100/150 N linear scaling), not measured and not a torque recommendation. Contact skin fixed for local ear response; no friction/contact/slip/creep prediction.',
            _material='Generic PETG orthotropic registry card; no printer-specific coupon calibration. Solid 100% infill assumption.',
            units='mm_N_MPa',material='PETG',build_axis='Z',raster_axis='X',
            printer='X1C',safety_factor=2.0,max_deflection_mm=1.0,voxel_mm=2.0,
            geometry=dict(preserve={'interfaces':dict(stl=preserve,attach=['join_surfaces'])},
                design_space=str(INPUT/f'{half}_design_space.stl'),
                obstacle={'functional_voids':str(INPUT/f'{half}_cuts.stl')}),
            regions=regions,cases=cases,required_cases=[c['name'] for c in cases],
            design=dict(volfrac=.35,filter_mm=6.0,overhang=True,symmetry=[],move=.05),
            finish=dict(voxel_mm=.6,smooth_mm='auto',add={'interfaces':preserve},
                cut={'functional_voids':str(INPUT/f'{half}_cuts.stl')}))
        # This obstacle is derived from the assembly's actual driver paths by
        # prepare_access_obstacles.py. Keep it when regenerating the studies.
        access = INPUT/'lower_access_tool_obstacles.stl'
        if half == 'lower' and access.exists():
            study['geometry']['obstacle']['C_retainer_driver_access'] = str(access)
            study['finish']['cut']['C_retainer_driver_access'] = str(access)
            study['_tool_access'] = 'Assembly-derived C-retainer driver paths; regenerate with prepare_access_obstacles.py after placement changes.'
        save(PART/f'spec/{half}_print_topology_study.json',study)
    audit=[]
    for case in cases[:6]:
        resultant=sum((np.asarray(load['force']) for load in case['loads']),np.zeros(3))
        moment=sum((np.cross(centres[load['region']],load['force']) for load in case['loads']),np.zeros(3))
        expected=np.cross([0,0,80],resultant)
        error=float(np.linalg.norm(moment-expected))
        if error>1: raise RuntimeError(f'Remote moment mismatch: {case["name"]}: {error} Nmm')
        audit.append(dict(case=case['name'],force_N=resultant.tolist(),moment_Nmm=moment.tolist(),
            reference_point_mm=[0,0,80],moment_error_Nmm=error))
    save(INPUT/'load_resultant_audit.json',dict(method='CAD material patch volume centroids; final node discretisation remains approximate',
        centres_mm={k:v.tolist() for k,v in centres.items()},cases=audit))
    print('Authored upper and lower studies: 7 cases, separated shoulder loads/mount supports, 2 mm voxels, 6 mm filter, move .05, volfrac .35, +Z self support.')

if __name__ == '__main__':
    main()
