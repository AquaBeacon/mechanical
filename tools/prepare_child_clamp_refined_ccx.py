"""Refine with native topopt, then remove only micrometre numerical slivers.

The native CCX CLI still refines/checks this surface at the requested size.
Pre-refinement to 0.99h prevents its float32 export from introducing a new
split after the validated precision weld. No FEM implementation is replaced.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import trimesh
from topopt.ccx import refine_stl
from clean_stl_degenerates import precision_weld,clean
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=analysis_case(PART)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mm',type=float,required=True)
    a=p.parse_args()
    source=CASE/'finished_cage.stl'
    folder=CASE/'ccx_prepared'/f'h{a.mm:g}'
    folder.mkdir(parents=True,exist_ok=True)
    dest=folder/'surface.stl'
    record=dict(native_refinement=refine_stl(str(source),str(dest),a.mm*.99))
    record['weld']=precision_weld(dest,allow_collinear=True)
    record['edge_flip']=clean(dest,binary=True)
    original=trimesh.load(source,force='mesh')
    result=trimesh.load(dest,force='mesh')
    record.update(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        surface_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
        volume_delta_mm3=float(abs(result.volume-original.volume)),
        bounds_delta_mm=float(np.max(abs(result.bounds-original.bounds))),
        max_edge_mm=float(result.edges_unique_length.max()),target_mm=a.mm)
    if record['volume_delta_mm3']>.1 or record['bounds_delta_mm']>.001 or record['max_edge_mm']>a.mm:
        raise RuntimeError('Native refined/welded surface changed geometry beyond tolerance')
    (folder/'preparation.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    study=json.loads((CASE/'study_final.json').read_text(encoding='utf-8'))
    study['part']=str(dest.resolve())
    study['_part_sha256']=record['surface_sha256']
    study['_reference_print_stl_sha256']=record['source_sha256']
    study['_surface_preparation']=record
    (folder/'study.json').write_text(json.dumps(study,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
