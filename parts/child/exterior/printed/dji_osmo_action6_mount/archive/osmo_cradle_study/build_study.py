import json
import pathlib
import subprocess
import trimesh

root = pathlib.Path(__file__).resolve().parent
exe = 'C:/Program Files/OpenSCAD/openscad.com'
report = {}
for name in ('base', 'receiver', 'pad'):
    output = root / (name + '.stl')
    subprocess.run([exe, '-D', f'part="{name}"', '-o', str(output),
                    str(root / 'osmo_cradle_study.scad')], check=True)
    mesh = trimesh.load_mesh(output)
    report[name] = dict(watertight=bool(mesh.is_watertight),
                        components=len(mesh.split()), bounds=mesh.bounds.tolist())
    assert mesh.is_watertight and len(mesh.split()) == 1
(root / 'mesh_check.json').write_text(json.dumps(report, indent=2))
subprocess.run([exe, '--imgsize=1100,850', '--autocenter', '--viewall',
                '--camera=0,0,0,65,0,35,250', '-o', str(root / 'preview.png'),
                str(root / 'osmo_cradle_study.scad')], check=True)
print(json.dumps(report, indent=2))
