"""Render actual camera fixture meshes in their authoritative assembly poses."""
from pathlib import Path
import json,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from prepare_child_horizontal_plate_frame import matrix
OSC=r'C:\Program Files\OpenSCAD\openscad.exe'

def main():
    for name in ['parent_exterior','child_horizontal_plate_frame']:
        a=ROOT/'assemblies'/name;p=json.loads((a/'placement.json').read_text(encoding='utf-8'))
        for context in [False,True]:
            rows=[]
            for r in p['items']:
                label=r['label'];camera='camera' in label
                nearby=(label in ['left_side_frame','left_front_guard'] if name.startswith('child') else r.get('file')=='parent_oneplate_frame')
                if not(camera or (context and nearby)):continue
                if 'case' in label:continue
                path=ROOT/r['part']/(r.get('file',Path(r['part']).name)+'.stl')
                color=[.7,.73,.76,.4] if nearby else ([.18,.48,.67,1] if 'receiver' in label or 'female' in label else [.95,.55,.17,1])
                if r.get('group') in ['fasteners','hardware']:color=[.55,.57,.59,1]
                if 'spacer' in label:color=[.26,.66,.42,1]
                rows.append('color('+json.dumps(color)+') multmatrix('+json.dumps(matrix(r['ops']).tolist())+') import('+json.dumps(path.as_posix())+');')
            stem='camera_fixture_20261029_'+('installed' if context else 'detail')
            src=a/'_work/intermediate'/(stem+'.scad');src.parent.mkdir(parents=True,exist_ok=True);src.write_text('\n'.join(rows),encoding='utf-8')
            out=a/'_work/images'/(stem+'.png');out.parent.mkdir(parents=True,exist_ok=True)
            camera='0,0,0,65,0,235,0' if name.startswith('child') else '0,0,0,120,0,35,0'
            cmd=[OSC,'-o',str(out),'--imgsize=1400,1000','--viewall','--autocenter','--projection=o','--colorscheme=Tomorrow','--camera='+camera,str(src)]
            proc=subprocess.Popen(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            record=dict(pid=proc.pid,started=time.time(),purpose=stem,owner='camera_fixture_20261029')
            try:stdout,stderr=proc.communicate(timeout=90)
            except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=15);raise
            record.update(exit_code=proc.returncode,exited=proc.poll() is not None)
            (a/'_work/logs'/(stem+'.process.json')).write_text(json.dumps(record),encoding='utf-8')
            (a/'_work/logs'/(stem+'.log')).write_bytes(stdout+stderr)
            if proc.returncode or b'ERROR' in stderr or b'WARNING' in stderr:raise RuntimeError(stderr.decode(errors='replace'))
            print(out,flush=True)
if __name__=='__main__':main()
