"""Build only the added common purchased M4 screw variants, never print copies."""
from pathlib import Path
import os, subprocess

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT / "parts/common/interior/cots/screw"
WORK=ROOT / "assemblies/parent_oneplate/_work/logs"

def main():
    WORK.mkdir(parents=True,exist_ok=True)
    for length in (12,14,16,20,25):
        name=f"screw_m4x{length}_socket"
        stl=PART / (name+".stl")
        command=[r"C:\Program Files\OpenSCAD\openscad.exe","-o",str(stl),"--export-format","asciistl",
                 "-D","d=4","-D",f"l={length}","-D","head_d=7","-D","head_h=4",str(PART / "screw.scad")]
        run=subprocess.run(command,capture_output=True,text=True)
        (WORK / (name+".log")).write_text(run.stdout+run.stderr,encoding="utf-8")
        run.check_returncode()
        env=dict(os.environ,STL_IN=str(stl),STEP_OUT=str(PART / (name+".step")))
        run=subprocess.run([r"C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe",str(ROOT / "scad/lib/stl_to_step.py")],env=env,capture_output=True,text=True,errors="replace")
        (WORK / (name+"_step.log")).write_text(run.stdout+run.stderr,encoding="utf-8")
        run.check_returncode()
        print("Built purchased hardware",name,flush=True)

if __name__=="__main__":
    main()
