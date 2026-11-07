"""Serial exports of the 5 mm camera-clamp revision."""
import os,sys,shutil,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
from export_camera_fixture_clamp import ROOT,run,compact
P=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
W=P/'_work/analysis/clamp_right5_20261029'/('export_'+datetime.now(timezone.utc).strftime('%H%M%S'));W.mkdir(parents=True)
e=os.environ.copy();e['PYTHONIOENCODING']='utf-8'
for i,stem in enumerate(['camera_mount_twist','camera_mount','camera_front_clamp']):
 d=W/str(i);d.mkdir();src=P/(stem+'.stl')
 try:compact(src,d/'m.stl',d/'compact.json')
 except ValueError:shutil.copy2(src,d/'m.stl')
 e.update(STL_IN=str(d/'m.stl'),STEP_OUT=str(d/'m.step'));run('scad/lib/stl_to_step.py',e,d/'export.log',600);shutil.copy2(d/'m.step',P/(stem+'.step'));print(stem,flush=True)
for name in ['parent_exterior','child_horizontal_plate_frame']:
 a=ROOT/'assemblies'/name
 import subprocess
 subprocess.run([sys.executable,str(ROOT/'scad/lib/asm_gen.py'),str(a/'placement.json'),str(a/(name+'_view.scad'))],check=True,timeout=60,capture_output=True)
 e.update(ASM_JSON=str(a/'placement.json'),ASM_ROOT=str(ROOT),STL_OUT=str(a/(name+'.stl')));run('scad/lib/asm_to_stl.py',e,W/(name+'_stl.log'),600)
 if name=='parent_exterior':
  e['STEP_OUT']=str(a/(name+'.step'));run('scad/lib/asm_to_step.py',e,W/(name+'_step.log'),600)
 print(name,flush=True)
e['CAMERA_STEP_JOB']=str(W/'job.json');e['CAMERA_STEP_REPORT']=str(W/'step_checks.json');e['ASM_ROOT']=str(ROOT)
(W/'job.json').write_text(json.dumps({'parts':[str((P/str(x)).relative_to(ROOT)).replace('\\','/') for x in ['camera_mount_twist','camera_mount','camera_front_clamp']]}))
run('spec/verify_camera_fixture_steps.py',e,W/'verify.log',600)
