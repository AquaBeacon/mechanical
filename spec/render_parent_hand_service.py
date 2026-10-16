from pathlib import Path
import subprocess,json,runpy,os,re
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
I=O/'_work/images';I.mkdir(parents=True,exist_ok=True)
PY='C:/Python313/python.exe';OSC='C:/Program Files/OpenSCAD/openscad.exe'
for pose,src,cam in [('closed','placement.json','360,-290,300,105,115,35'),('service','service_placement.json','600,-320,350,220,115,35')]:
 view=O/(pose+'_view.scad')
 subprocess.run([PY,str(R/'scad/lib/asm_gen.py'),str(O/src),str(view)],check=True)
 view.write_text(re.sub(r'import\("([^\"]+)"\)',r'import("\1",convexity=20)',view.read_text(encoding='utf-8')),encoding='utf-8')
 subprocess.run([OSC,'-o',str(I/(pose+'.png')),'--imgsize=1400,1100','--projection=o','--viewall','--camera='+cam,str(view)],check=True,capture_output=True,creationflags=0x08000000)
print('Rendered installed and out-of-case poses')
# A derived inspection view reveals the fixed lower parts without the upper deck.
# This JSON is an exploration view only; placement.json remains canonical.
a=json.loads((O/'placement.json').read_text(encoding='utf-8'))
a['exploration_only']=True
a['items']=[it for it in a['items'] if it['label'] not in ['p_main','spresense','gnss_antenna','antenna_ground_plate','lid_keepout']]
C=O/'_work/intermediate';C.mkdir(parents=True,exist_ok=True)
src=C/'gnss_fixed_view.json';src.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8')
view=C/'gnss_fixed_view.scad'
ops=runpy.run_path(str(R/'scad/lib/asm_gen.py'))['ops_to_scad']
lines=['// Derived inspection view; placement.json is canonical.']
for it in a['items']:
 p=R/it['part']/(it.get('file',Path(it['part']).name)+'.stl')
 relative=os.path.relpath(p,C).replace('\\','/')
 lines.append(f'color("{it.get("color","Gray")}",{it.get("alpha",1)}) '+ops(it['ops'])+f' import("{relative}",convexity=20);')
view.write_text('\n'.join(lines),encoding='utf-8')
subprocess.run([OSC,'-o',str(I/'gnss_fixed.png'),'--imgsize=1400,1100','--projection=o','--viewall','--camera=380,460,300,105,115,40',str(view)],check=True,capture_output=True,creationflags=0x08000000)
# Open-lid top view at zero lift, with the native SD card approach highlighted.
a=json.loads((O/'placement.json').read_text(encoding='utf-8'))
a['items']=[it for it in a['items'] if it['label']!='lid_keepout']
lines=['// Derived access inspection at zero lift; placement.json is canonical.']
for it in a['items']:
 p=R/it['part']/(it.get('file',Path(it['part']).name)+'.stl')
 relative=os.path.relpath(p,C).replace('\\','/')
 lines.append(f'color("{it.get("color","Gray")}",{it.get("alpha",1)}) '+ops(it['ops'])+f' import("{relative}",convexity=20);')
lines += ['color([0,0.85,0.85,0.8]) translate([56.5,10.29,44]) cube([11,15,1]);',
          'color([0,0.85,0.85,0.8]) translate([159.66,118.72,67.5]) cube([11,15,1]);']
report=json.loads((O/'switch_tx_access_checks.json').read_text(encoding='utf-8'))
for sw in report['switches']:
 x,y=sw['centre_xy_mm']
 lines.append(f'color([1,0.2,0.1,0.35]) translate([{x},{y},47]) cylinder(r=10,h=40,$fn=64);')
view=C/'access_top_view.scad';view.write_text('\n'.join(lines),encoding='utf-8')
subprocess.run([OSC,'-o',str(I/'access_top.png'),'--imgsize=1400,1400','--projection=o','--viewall','--camera=105,115,600,105,115,0',str(view)],check=True,capture_output=True,creationflags=0x08000000)
# Front-right section makes the TX overhead reservation visible under Sony.
lines=['// Inspection: case hidden; cyan volume is reserved space, not a part.']
for it in a['items']:
 if it['label'] not in ['tx_improved','tx_top_keepout','sony_upper_carrier','spresense','plate']:continue
 p=R/it['part']/(it.get('file',Path(it['part']).name)+'.stl');relative=os.path.relpath(p,C).replace('\\','/')
 lines.append(f'color("{it.get("color","Gray")}",{it.get("alpha",1)}) '+ops(it['ops'])+f' import("{relative}",convexity=20);')
view=C/'tx_clearance_view.scad';view.write_text('\n'.join(lines),encoding='utf-8')
subprocess.run([OSC,'-o',str(I/'tx_clearance.png'),'--imgsize=1200,1000','--projection=o','--viewall','--camera=400,-190,160,130,130,45',str(view)],check=True,capture_output=True,creationflags=0x08000000)
# Isolated inspection section: hide the upper shelf above Z53 to reveal the
# complete annulus. This changes the view only, never the printable source.
lines=['// Exploration section only: upper antenna shelf hidden.']
for it in a['items']:
 if it['label'] not in ['antenna_rack','coax_ring','coax_coil_keepout']:continue
 p=R/it['part']/(it['file']+'.stl');relative=os.path.relpath(p,C).replace('\\','/')
 geometry=ops(it['ops'])+f' import("{relative}",convexity=20);'
 if it['label']=='antenna_rack':geometry='difference(){'+geometry+'translate([-100,-100,53]) cube([400,400,100]);}'
 lines.append(f'color("{it["color"]}",{it.get("alpha",1)}) '+geometry)
view=C/'coil_inspection_view.scad';view.write_text('\n'.join(lines),encoding='utf-8')
subprocess.run([OSC,'-o',str(I/'coil_inspection.png'),'--imgsize=1200,1000','--projection=o','--viewall','--camera=250,-200,280,60,60,35',str(view)],check=True,capture_output=True,creationflags=0x08000000)

# Isolated magnetometer mount; other electronics hidden only for inspection.
lines=['// Exploration view only: GNSS frame and magnetometer mounting detail.']
for it in a['items']:
 if it['label'] not in ['gnss_universal_carrier','gnss_universal_pcb','gnss_receiver','gnss_pin_headers','magnetometer'] and not it['label'].startswith(('mag_bolt_','mag_nut_','gnss_pcb_bolt_','gnss_pcb_nut_')):continue
 p=R/it['part']/(it.get('file',Path(it['part']).name)+'.stl');relative=os.path.relpath(p,C).replace('\\','/')
 lines.append(f'color("{it.get("color","Gray")}",{it.get("alpha",1)}) '+ops(it['ops'])+f' import("{relative}",convexity=20);')
view=C/'magnetometer_mount_view.scad';view.write_text('\n'.join(lines),encoding='utf-8')
subprocess.run([OSC,'-o',str(I/'magnetometer_mount.png'),'--imgsize=1400,1100','--projection=o','--viewall','--camera=-130,330,175,65,175,50',str(view)],check=True,capture_output=True,creationflags=0x08000000)
