"""Build purchased antenna and floor fasteners from common SCAD/variants."""
from pathlib import Path
import os,subprocess,shlex
R=Path(__file__).resolve().parents[1];P=R/'parts/common/interior/cots/screw'
C=P/'_work/intermediate';L=P/'_work/logs';C.mkdir(parents=True,exist_ok=True);L.mkdir(parents=True,exist_ok=True)
osc='C:/Program Files/OpenSCAD/openscad.exe'
fc='C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/freecadcmd.exe'
for line in (P/'variants.txt').read_text().splitlines():
    tokens=shlex.split(line,comments=True,posix=False)
    if not tokens or tokens[0] not in ['m4x12','nut_m4','m4x8_button','m4x12_button','m3x40']:continue
    stem='screw_'+tokens[0];defs=[x for t in tokens[1:] for x in ['-D',t]]
    for target in [P/(stem+'.stl'),C/(stem+'.csg')]:
        subprocess.run([osc,'-o',str(target),*defs,str(P/'screw.scad')],check=True,capture_output=True,creationflags=0x08000000)
    env=dict(os.environ,CSG_IN=str(C/(stem+'.csg')),STEP_OUT=str(P/(stem+'.step')),OPENSCAD=osc,STL_REF=str(P/(stem+'.stl')))
    result=subprocess.run([fc,str(R/'scad/lib/csg_to_step.py')],env=env,capture_output=True,creationflags=0x08000000)
    (L/(stem+'.log')).write_bytes(result.stdout+result.stderr)
    assert result.returncode==0 and (P/(stem+'.step')).exists(),stem
    print(stem,'built',flush=True)
