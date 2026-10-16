"""Run existing topopt CLI at three bounded mesh sizes; collect its JSONs.

No FEM or convergence algorithm. report_child_clamp_analysis.py applies the
installed topopt convergence judge. Fine mesh 2.5 mm avoids the failed 2 mm
direct solver's excessive memory. The actual spacings are recorded, not called
an 8/4/2 mm study.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import hashlib

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/"parts/child/exterior/printed/child_wte4_suspension_clamp"
WORK=PART/"_work/analysis"


def main():
    out=WORK/"mount_ccx"
    out.mkdir(exist_ok=True)
    stl=WORK/"surface_remesh/child_wte4_suspension_clamp_half.stl"
    study=WORK/"study_mount.json"
    env=os.environ.copy()
    env.update(PYTHONIOENCODING="utf-8",OMP_NUM_THREADS="4",CCX_NPROC_EQUATION_SOLVER="4")
    record=dict(stl=str(stl),study=str(study),runs=[],native_sources=[],
                stl_sha256=hashlib.sha256(stl.read_bytes()).hexdigest(),
                study_sha256=hashlib.sha256(study.read_bytes()).hexdigest(),
                note="Collected unmodified JSON runs from installed topopt CLI. Spacings 5/3/2.5 mm; 2.5 uses native Delaunay after HXT crashed. Failed 2.4/2.5 HXT attempts remain in their original folders/logs.")
    for h in [5,3,2.5]:
        folder=out/f"h{h:g}"
        if h==2.5:
            folder=out/"h2.5_delaunay"
            env["TOPOPT_GMSH"]=str(ROOT/"tools/gmsh_clamp_delaunay.cmd")
        log=PART/"_work/logs"/f"round_pocket_ccx_h{h:g}.log"
        native=folder/"ccx_summary.json"
        if "--resume" in sys.argv and native.exists():
            previous=json.loads((out/"series_summary.json").read_text(encoding="utf-8"))
            assert previous.get("stl_sha256")==record["stl_sha256"] and previous.get("study_sha256")==record["study_sha256"]
            cached=json.loads(native.read_text(encoding="utf-8"))
            run_code=0 if cached.get("pass") else 1
        else:
          with log.open("a",encoding="utf-8") as stream:
            stream.write("\n--- Native CLI attempt ---\n")
            stream.flush()
            run=subprocess.run([sys.executable,"-u","-m","topopt","ccx",str(stl),
                                "--study",str(study),"--out",str(folder),"--mesh-mm",str(h),"--map","surface"],
                               cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT)
          run_code=run.returncode
        if not native.exists():
            raise RuntimeError(f"Native summary missing at {h} mm: see {log}")
        data=json.loads(native.read_text(encoding="utf-8"))
        record["runs"].extend(data["runs"])
        record["native_sources"].append(str(native))
        (out/"series_summary.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
        print(f"Mesh {h:g} mm finished, native exit {run_code}",flush=True)
        if run_code not in (0,1):
            raise RuntimeError("Native CLI operational failure")


if __name__=="__main__":
    main()
