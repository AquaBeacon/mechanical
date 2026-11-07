"""Rev.4 review views derived exclusively from the current placement."""
from pathlib import Path
import json,subprocess

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'

def main(prefix='bolt_on_plate'):
    data=json.loads((A/'placement.json').read_text(encoding='utf-8'))
    work=A/'_work/intermediate';work.mkdir(parents=True,exist_ok=True)
    for name,angle,hide in [('overview',72,False),('underside',145,True),('top',0,True)]:
        layout=data
        if hide:
            layout=dict(data,items=[r for r in data['items'] if r['label'] in
                ['open_frame','sensor_carrier','camera_qr_female'] or
                r['label'].startswith(('bolt_on_','carrier_','qr_female_'))])
        if name=='top':layout=dict(data,items=[r for r in data['items'] if r['label']=='open_frame'])
        p=work/f'{prefix}_{name}.json'
        p.write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        view=p.with_suffix('.scad')
        subprocess.run(['python',str(ROOT/'scad/lib/asm_gen.py'),str(p),str(view)],check=True,cwd=ROOT)
        view.write_text(view.read_text(encoding='utf-8').replace('import("../../','import("../../../../'),encoding='utf-8')
        azimuth=0 if name=='top' else 225
        cmd=[r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(A/'_work/images'/f'{prefix}_{name}.png'),
             '--imgsize=1500,1100','--viewall','--autocenter','--projection=o','--colorscheme=Tomorrow',
             f'--camera=0,0,0,{angle},0,{azimuth},0','-D','show_floats=false']
        if hide:
            cmd+=['-D','show_vessel=false','-D','show_pads=false']
        r=subprocess.run(cmd+[str(view)],capture_output=True,cwd=ROOT)
        (A/'_work/logs'/f'{prefix}_{name}_preview.log').write_bytes(r.stdout+r.stderr)
        if r.returncode or b'WARNING' in r.stderr or b'ERROR' in r.stderr:raise RuntimeError(r.stderr.decode(errors='replace'))
    subprocess.run(['python',str(ROOT/'scad/lib/asm_gen.py'),str(A/'placement.json'),str(A/'parent_exterior_view.scad')],check=True,cwd=ROOT)

if __name__=='__main__':main()
