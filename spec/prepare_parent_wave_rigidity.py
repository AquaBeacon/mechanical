"""Snapshot real finished CAD and author input studies for native topopt/CCX.

This is input preparation only. No mesh, FEM solver or acceptance implementation.
All supports are ideal bolted interfaces; PCB/case/joint compliance is separate.
"""
from pathlib import Path
import sys,json,shutil,hashlib,subprocess
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scad/lib'))
import parent_gnss as G
O=R/'assemblies/parent_hand_service/_work/analysis/wave_rigidity_20261009'
tag=sys.argv[1] if len(sys.argv)>1 else 'baseline'
assert tag.isidentifier();D=O/tag;D.mkdir(parents=True,exist_ok=True)
def region(lo,hi):return dict(type='box',min=lo,max=hi)
def patch(x,y,z,r=2.9):return region([x-r,y-r,z-.2],[x+r,y+r,z+.02])
parts={
 'gnss_frame':dict(part='gnss_universal_carrier',file='gnss_universal_carrier',feet=G.UNIVERSAL_FRAME_FOOT_XY,
   patches=[region([75,139,55.8],[78,219,56.02]),region([132,139,55.8],[135,219,56.02])]+[patch(x,y,76,2.4) for x,y in G.magnetometer_mounting_xy()],
   masses=[.08/2,.08/2]+[.005/4]*4),
 'sony_carrier':dict(part='parent_hand_service',file='sony_upper_carrier',feet=G.SONY_CARRIER_FOOT_XY,
   patches=[patch(G.SONY_ORIGIN[0]-x,G.SONY_ORIGIN[1]-y,65.6,3) for x,y in [[2.54,54.61],[50.8,53.34],[7.62,2.54],[35.56,2.54]]],masses=[.04/4]*4),
 'main_carrier':dict(part='parent_hand_service',file='main_lower_carrier',feet=G.MAIN_CARRIER_FOOT_XY,
   patches=[region([18,24,41.7],[130,112,41.97])],masses=[.15]),
 'antenna_rack':dict(part='ann_mb1_internal_rack',file='ann_mb1_internal_rack',feet=G.RACK_FOOT_XY,
   patches=[region([16,30,63.4],[104,90,63.62]),region([10,10,21.5],[110,110,21.82])],masses=[.18,.12],transform=[60,60,G.RACK_BASE_Z]),
 'floor_plate':dict(part='parent_hand_service',file='floor_plate',feet=G.CASE_ANCHOR_XY,foot_z=13.84,foot_r=5,
   patches=[patch(x,y,18.8,3.6) for pts in [G.MAIN_CARRIER_FOOT_XY,G.SONY_CARRIER_FOOT_XY,G.RACK_FOOT_XY,G.UNIVERSAL_FRAME_FOOT_XY] for x,y in pts],
   masses=[m/4 for m in [.27,.15,.45,.14] for i in range(4)]),
}
# Direct PWR/TX/battery load regions come from actual generated placement/holes.
assembly=json.loads((R/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
holes=json.loads((R/'assemblies/parent_hand_service/hole_sources.json').read_text())
for key,m,z in [('PWR',.10,28.25),('TX',.10,24.75)]:
 parts['floor_plate']['patches'] += [patch(x,y,z,3.4) for x,y in holes[key]]
 parts['floor_plate']['masses'] += [m/4]*4
parts['floor_plate']['patches'] += [patch(*G.battery_xy(x,y),20,3.4) for x,y in [[0,0],[103,0],[0,55.5],[103,55.5]]]
parts['floor_plate']['masses'] += [.30/4]*4
for name,data in parts.items():
 if len(sys.argv)>2 and name not in sys.argv[2:]:continue
 p=D/name;p.mkdir()
 source=R/'parts/parent/interior/printed'/data['part']/data['file']
 if name=='sony_carrier' and '--stack-joints' in sys.argv:
  subprocess.run(['C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/python.exe',str(R/'spec/export_parent_stack_analysis.py'),str(p)],check=True)
 else:
  for ext in ['step','stl']:shutil.copy2(source.with_suffix('.'+ext),p/(name+'.'+ext))
 # Explicit uniform-volume self-weight is physically equivalent to rho*g.
 # Native CCX moment_error currently omits DLOAD gravity (cli/ccx.py:1010).
 # Keep solver/acceptance unchanged; include self-weight in ordinary CLOADs.
 code='import FreeCAD as A,Part,sys; print(Part.read(sys.argv[1]).Volume)'
 volume=float(subprocess.check_output(['C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/python.exe','-c',code,str(p/(name+'.step'))],text=True).strip())
 self_mass=volume*1.27e-6
 # Rack is modeled in its original local coordinates; transform regions only.
 offset=data.get('transform',[0,0,0])
 reg={f'foot_{i}':patch(x-offset[0],y-offset[1],data.get('foot_z',18.8)-offset[2],data.get('foot_r',2.8)) for i,(x,y) in enumerate(data['feet'])}
 reg.update({f'payload_{i}':r for i,r in enumerate(data['patches'])})
 reg['self_mass']=region([-1000,-1000,-1000],[1000,1000,1000])
 for k,r in reg.items():
  if k.startswith('payload'):
   for bound in ['min','max']:r[bound]=[a-b for a,b in zip(r[bound],offset)]
 supports=[dict(region=f'foot_{i}',fix='xyz') for i in range(len(data['feet']))]
 cases=[]
 for axis in range(3):
  for sign in [-1,1]:
   direction=[0,0,0];direction[axis]=sign
   loads=[]
   for i,mass in enumerate(data['masses']):
    force=[0,0,0];force[axis]=sign*mass*2*9.80665
    loads.append(dict(region=f'payload_{i}',force=force))
   force=[0,0,0];force[axis]=sign*self_mass*2*9.80665
   loads.append(dict(region='self_mass',force=force))
   cases.append(dict(name='wave_2g_'+'XYZ'[axis]+('+' if sign>0 else '-'),supports=supports,loads=loads))
 # Existing 20N port target retained separately from the six wave cases.
 # Loads select the actual printed bearing bed, not the deformable PCB/socket.
 port = G.MAIN_SD_MOUTH if name=='main_carrier' else G.SONY_SD_MOUTH if name=='sony_carrier' else None
 if port:
  z=41.95 if name=='main_carrier' else 65.55
  ports={'sd':region([port[0]-5,port[1]+1,z-.25],[port[0]+5,port[1]+7,z+.02])}
  if name=='main_carrier':ports['usb']=region([24,24,41.7],[54,44,41.97])
  for label,regn in ports.items():
   reg[label]=regn
   for axis in range(3):
    for sign in [-1,1]:
     force=[0,0,0];force[axis]=20*sign
     weights=[dict(region=f'payload_{i}',force=[0,0,-m*9.80665]) for i,m in enumerate(data['masses'])]
     cases.append(dict(name='port20N_'+label+'_'+'XYZ'[axis]+('+' if sign>0 else '-'),supports=supports,loads=[dict(region=label,force=force),dict(region='self_mass',force=[0,0,-self_mass*9.80665])]+weights))
 study=dict(part=name+'.stl',material='PETG',build_axis='Z',units='mm_N_MPa',printer='X1C',safety_factor=3,max_deflection_mm=.2,walls=4,infill=1.,regions=reg,cases=cases,
  _what='Finished printed fixture with its payload mass budget, 2g resultant all six directions; not drop certification.',
  _payload_mass_kg=data['masses'],_self_mass_kg=self_mass,_self_mass_input='CAD volume x1270kg/m3 as uniform-volume consistent CLOAD; native moment_error omits DLOAD gravity; solver unchanged',_limitations=['Ideal fixture-to-floor bolt constraints; floor/case/joint/PCB compliance omitted','Generic dry23C dense PETG orthotropic card, no machine-specific measurement','Payload masses are upper design budgets, require weighing actual hardware','Manufacturing release requires actual assembly retention and wave-cycle tests'])
 (p/'study.json').write_text(json.dumps(study,indent=2),encoding='utf-8')
 (p/'inputs.json').write_text(json.dumps(dict(source=source.relative_to(R).as_posix(),sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir() if f.is_file()}),indent=2),encoding='utf-8')
print(D)
