"""Author adapter FEA; preserve only real occupied bolt neighborhoods for setup.

No optimisation or FEM solver is implemented here. All analyses stay in topopt.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_open_frame'
OUT=ROOT/'assemblies/child_exterior_horizontal/_work/analysis/clamp_link_fea'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    source=PART/'child_exterior_open_frame_clamp_link.stl'
    d=json.loads((PART/'spec/clamp_interface.json').read_text(encoding='utf-8'))['interface']['CLAMP_INTERFACE']
    face=abs(d['mount_y'])+1
    regions={}
    for i,y in enumerate([-10,10]):regions['frame_'+str(i)]=dict(type='cylinder',axis='X',centre=[0,y,0],r=4.5,range=[140,144.1])
    for i,(y,z) in enumerate([(y,z) for y in [-8,8] for z in [-d['frame_pitch_x']/2,d['frame_pitch_x']/2]]):
        regions['cage_'+str(i)]=dict(type='cylinder',axis='X',centre=[0,y,z],r=4.5,range=[face-.05,face+8])
    forces=[('vertical_down_3g',[0,0,-50]),('vertical_up_3g',[0,0,50]),
            ('radial_out',[30,0,-16.35]),('radial_in',[-30,0,-16.35]),
            ('axial_forward',[0,30,-16.35]),('axial_rear',[0,-30,-16.35])]
    study=dict(units='mm_N_MPa',material='PETG',build_axis='Y',raster_axis='X',infill=1.,walls=8,
      printer='X1C',safety_factor=3.,max_deflection_mm=1.,part=str(source),regions=regions,
      cases=[dict(name=n,supports=[dict(region='frame_'+str(i),fix='xyz') for i in range(2)],
            loads=[dict(region='cage_'+str(i),force=[x/4 for x in f]) for i in range(4)]) for n,f in forces],
      required_cases=[n for n,f in forces],
      _what='Finished bolt-on adapter. No optimisation or upstream cage analysis.',
      _why='Provisional 10 kg vehicle at 3g / six equal connections=49.03325 N; rounded upward to 50 N including connector weight. Lateral 30 N plus static vertical 16.35 N.',
      _limits='Generic PETG provisional card; ideal fixed bolt neighborhoods. No clamp/joint/preload/creep/underwater/tether qualification.',
      _part_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    (OUT/'study.json').write_text(json.dumps(study,indent=2)+'\n',encoding='utf-8')
    mesh=trimesh.load(source,force='mesh');preserve={}
    patches=OUT/'setup_inputs';patches.mkdir(exist_ok=True)
    for name,reg in regions.items():
        a,b=reg['range'];cylinder=trimesh.creation.cylinder(radius=reg['r'],height=b-a,sections=40)
        matrix=trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]);matrix[:3,3]=[(a+b)/2,*reg['centre'][1:]]
        cylinder.apply_transform(matrix)
        patch=trimesh.boolean.intersection([mesh,cylinder],engine='manifold')
        assert patch.is_volume and patch.volume>0
        target=patches/(name+'.stl');patch.export(target);preserve[name]=str(target)
    setup=dict(study,geometry=dict(design_space=str(source),preserve=preserve))
    (OUT/'setup_study.json').write_text(json.dumps(setup,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
