"""Author explicitly provisional FEA cases; geometry remains the SCAD source."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assemblies/child_simple_assembly'

def box(lo,hi): return dict(type='box',min=lo,max=hi)
def case(name,support,force_region,force):
    return dict(name=name,load_class='normal',supports=[dict(region=r,fix='xyz') for r in support],loads=[dict(region=force_region,force=force)])

for suffix in ['front','rear','guard']:
    n='child_simple_'+suffix
    regions={}
    if suffix=='guard':
        for s in [-1,1]:
            for t in [-1,1]:
                for z in [-7,5]:
                    regions[f'bolt_{s}_{t}_{z}']=box([s*100-5,33 if t==1 else -37,z-3],[s*100+5,37 if t==1 else -33,z+3])
        support=list(regions)
        regions['floor']=box([-111,-85,-86],[111,85,-81])
        cases=[case('landing_300N',support,'floor',[0,0,300]),case('transport_X_300N',support,'floor',[300,0,0]),case('transport_Y_300N',support,'floor',[0,300,0])]
    else:
        sign=1 if suffix=='front' else -1
        for s in [-1,1]:
            for z in [20,180]:
                regions[f'bolt_{s}_{z}']=box([s*77-5,0 if sign==1 else -5,z-5],[s*77+5,5 if sign==1 else 0,z+5])
        support=list(regions)
        zc=100 if suffix=='front' else 190
        regions['pad']=box([-24,78 if sign==1 else -83,zc-24],[24,83 if sign==1 else -78,zc+24])
        for s in [-1,1]:
            regions[f'lift_{s}']=box([s*77-6,0 if sign==1 else -10,203],[s*77+6,10 if sign==1 else 0,218])
        regions['bottom']=box([-71,0 if sign==1 else -71,-19],[71,71 if sign==1 else 0,-14])
        cases=[case('mount_pull_100N',support,'pad',[0,sign*100,0]),case('vessel_axial_300N',['lift_-1','lift_1'],'bottom',[0,0,-300])]
    data=dict(part=str(ROOT/'parts/child/exterior/printed'/n/(n+'.stl')),units='mm_N_MPa',material='PETG',build_axis='Z' if suffix=='guard' else 'Y',ground_axis='Z',printer='X1C',safety_factor=4,max_deflection_mm=2,voxel_mm=3,regions=regions,cases=cases,
              _scope='Screening only: ideal fixed bolt patches, no bolt preload, EVA contact or joint slip. 300N inherited transport/landing envelope; 100N mount load is a design assumption. Do not cite an unconverged run as final strength.')
    (OUT/(n+'_study.json')).write_text(json.dumps(data,indent=2),encoding='utf-8')
print(OUT)
