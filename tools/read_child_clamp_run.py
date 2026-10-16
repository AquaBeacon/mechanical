"""Read an already solved CalculiX run with installed topopt's native reporter.

No solve, mesh changes, material changes or new failure/convergence algorithm.
Useful while a multi-mesh CLI job is still running; also records gap movement.
"""
from pathlib import Path
import json
import sys
import numpy as np
from topopt import ccx as lib
from topopt.cli import ccx as cli
from topopt.loadcase import load_case_from_json

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/"parts/child/exterior/printed/child_wte4_suspension_clamp"
work=PART/"_work/analysis"
h=float(sys.argv[1]) if len(sys.argv)>1 else 8.0
tag=f"child_wte4_suspension_clamp_half_h{h:.2f}"
solver_tag=tag+"_"+sys.argv[2] if len(sys.argv)>2 else tag
outdir=work/"mount_ccx"
study=load_case_from_json(str(work/"study_mount.json"))
mesh=cli.mesh_context(str(outdir/(tag+"_mesh.inp")))
mat,ortho,info=cli.material_model(study.material)
density=ortho.density_kg_m3
volume=lib.mass_properties(mesh["xyz"],mesh["elements"],density,ids=mesh["ids"])["volume_mm3"]
cases=cli.build_cases(study,mesh,map_mode="surface",density_kg_m3=density,volume_mm3=volume,load_split="consistent")
res=lib.parse_frd(str(outdir/(solver_tag+".frd")))
dat=lib.parse_dat(str(outdir/(solver_tag+".dat")))
assert len(res["steps"])==len(cases), "Missing solver results"
rows=[]
for i,case in enumerate(cases):
    c=dict(case=case["name"],required_safety_factor=case["required_safety_factor"],load_class=case["load_class"],worst_element_minimum=1.5)
    cli._case_results(c,case,res["steps"][i],res,mesh,ortho,study,0,dat,i,density,volume)
    rows.append(c)
result=dict(mesh_target_mm=h,nodes=len(mesh["ids"]),elements=len(mesh["elements"]),mesh_quality=lib.mesh_quality(mesh["xyz"],mesh["elements"],ids=mesh["ids"]),cases=rows)
(outdir/(solver_tag+"_read.json")).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
for c in rows:
    print(c["case"],"sf",c["safety_factor_p99_5"],"worst",c["worst_element_safety_factor"],"hotspot",c["hotspot"],"mode",c.get("governing_failure_mode"))
