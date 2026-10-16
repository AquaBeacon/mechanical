"""Capture full mesher diagnostics with a native-supported Gmsh algorithm."""
from pathlib import Path
import argparse
import subprocess
from topopt.ccx import write_geo
from topopt.external import require


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('surface',type=Path)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--algorithm',type=int,choices=[1,10],default=10)
    p.add_argument('--mm',type=float,default=8)
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    geo=a.out/'mesh.geo'
    write_geo(str(geo),str(a.surface),a.mm,algorithm=a.algorithm)
    with (a.out/'gmsh.log').open('w',encoding='utf-8') as stream:
        r=subprocess.run([require('gmsh','clamp mesh diagnosis'),str(geo),'-3','-format','inp',
            '-o',str(a.out/'mesh.inp')],stdout=stream,stderr=subprocess.STDOUT,timeout=1800)
    print('exit',r.returncode)
    raise SystemExit(r.returncode)


if __name__=='__main__':main()
