"""Screening calculations only: never interpret these as assembly FEA or certification."""
import json
from pathlib import Path
O=Path(__file__).resolve().parents[1]/'assemblies/parent_hand_service'
# Official printed PETG modulus is typical, not a lower-bound design allowable.
E=1500.0
L=33.5
I=6**4/12
F=20/4
delta=F*L**3/(3*E*I)
report=dict(status='NOT_VERIFIED',requirement=dict(force_N=20,displacement_mm=.2),
 material=dict(name='PETG screening assumption',E_MPa=E,source='https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf',actual_print_material_verified=False),
 benchmark=dict(description='Four exposed 6 mm square sliders considered as equal-load independent cantilevers; ignores additional service props and guide/joint compliance. NOT a prediction or bound for the complete assembly.',length_mm=L,section_I_mm4=I,force_per_slider_N=F,tip_deflection_mm=delta,formula='F L^3 / (3 E I)',exceeds_target=delta>.2),
 clearances=dict(guide_width_mm=6.6,slider_width_mm=6,nominal_per_side_mm=.3,exceeds_displacement_target=True,comment='Clearance is not connector displacement; actual coupled free motion must be measured.'),
 conclusion='Support pads and edge ribs improve the PCB support geometry, but do not establish the 20 N / 0.2 mm case-relative requirement. Full load paths, Sony boards, joints and uplift remain unverified.',
 physical_test=dict(reference='Displacement indicator fixed to case, probe connector body; apply load with mating sacrificial plug/card fixture, not exposed contacts.',ports=['MAIN_USB','MAIN_SD','SONY_MAIN_USB','SONY_EXT_USB','SONY_SD'],poses=['closed','service with props installed'],directions=['insertion/extraction','both PCB-normal directions','both transverse directions'],force_steps_N=[0,5,10,15,20,0],acceptance='At 20 N, total connector displacement from unloaded position <=0.2 mm in each load case, no slipping/loosening/cracking, and no measurable residual displacement on unloading.',notes=['Measure PCB displacement separately to identify support compliance.','Do not subject battery to test force.','Record material, print direction, temperatures, fastener torques, shims and actual gap.','First test mechanically equivalent dummy boards/connector fixtures; functional connector ratings must be confirmed before applying 20 N to electronics.']))
(O/'rigidity_screening.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('NOT_VERIFIED; isolated-slider screening deflection:',round(delta,3),'mm')
