"""Derived assembly views; placement.json remains the only placement authority."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
def main():
    source=A/'placement.json'
    data=json.loads(source.read_text(encoding='utf-8'))
    for name,layout in [('overview',data),('unloaded',dict(data,items=[x for x in data['items'] if x.get('removal_group') not in ['camera','td04a']]))]:
        inter=A/'_work/intermediate';inter.mkdir(parents=True,exist_ok=True)
        p=inter/('qr_'+name+'.json');p.write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        view=inter/('qr_'+name+'.scad')
        subprocess.run(['python',str(ROOT/'scad/lib/asm_gen.py'),str(p),str(view)],check=True,cwd=ROOT)
        # asm_gen infers root two levels above its input JSON. Derived inputs
        # live two levels deeper; adjust imports in this generated view only.
        view.write_text(view.read_text(encoding='utf-8').replace('import("../../','import("../../../../'),encoding='utf-8')
        out=A/'_work/images'/('qr_standing_'+name+'.png')
        cmd=[r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(out),'--imgsize=1500,1100','--viewall','--autocenter','--projection=o','--colorscheme=Tomorrow','--camera=0,0,0,72,0,225,0','-D','show_floats=false',str(view)]
        r=subprocess.run(cmd,capture_output=True,cwd=ROOT)
        (A/'_work/logs'/('qr_'+name+'_preview.log')).write_bytes(r.stdout+r.stderr)
        if r.returncode or b'WARNING' in r.stderr or b'ERROR' in r.stderr:raise RuntimeError(r.stderr.decode(errors='replace'))
    subprocess.run(['python',str(ROOT/'scad/lib/asm_gen.py'),str(source),str(A/'parent_exterior_view.scad')],check=True,cwd=ROOT)
if __name__=='__main__':main()
