"""Retry the existing finest CalculiX deck with its built-in ICCG solver.

Only *STATIC's SOLVER option changes. No mesh, material, BC or force changes.
See CalculiX 2.23 manual, section *STATIC (p601 PDF / printed p600).
This is external solver operation, not an implementation of FEM or ICCG.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
from topopt.ccx import converged, parse_frd

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/"parts/child/exterior/printed/child_wte4_suspension_clamp"
OUT=PART/"_work/analysis/mount_ccx"
TAG="child_wte4_suspension_clamp_half_h2.00"


def main():
    src=OUT/(TAG+".inp")
    txt=src.read_text(encoding="utf-8")
    assert txt.count("*STATIC\n")==8
    dst=OUT/(TAG+"_iccg.inp")
    dst.write_text(txt.replace("*STATIC\n","*STATIC,SOLVER=ITERATIVE CHOLESKY\n"),encoding="utf-8")
    env=os.environ.copy()
    env["OMP_NUM_THREADS"]="4"
    env["CCX_NPROC_EQUATION_SOLVER"]="4"
    log=PART/"_work/logs/ccx_h2_iccg.log"
    with log.open("w",encoding="utf-8") as stream:
        run=subprocess.run([r"C:\Users\ryupc\Tools\calculix_2.23_4win\ccx_static.exe",dst.stem],
                           cwd=OUT,env=env,stdout=stream,stderr=subprocess.STDOUT)
    okay,note=converged(log.read_text(encoding="utf-8",errors="replace"))
    frd=dst.with_suffix(".frd")
    result=dict(returncode=run.returncode,solver="CalculiX built-in ITERATIVE CHOLESKY",
                source_inp_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
                retry_inp_sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),
                convergence_note=note,complete_steps=0,pass_check=False)
    if run.returncode==0 and okay and frd.exists():
        steps=parse_frd(str(frd))["steps"]
        result["complete_steps"]=sum(bool(s["displacement"] and s["stress"]) for s in steps)
        result["pass_check"]=result["complete_steps"]==8
    (OUT/"iccg_execution.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["pass_check"] else 1)


if __name__=="__main__":
    main()
