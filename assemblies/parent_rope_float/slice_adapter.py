from pathlib import Path
import subprocess,json,trimesh
r=Path.cwd();out=r/'print_jobs/parent_rope_float';work=out/'adapter_slice';work.mkdir(exist_ok=True)
p=out/'parent_rope_keel_adapter.stl';m=trimesh.load(p);m.apply_translation([138-m.bounds[:,0].mean(),128-m.bounds[:,1].mean(),-m.bounds[0,2]]);m.export(work/'placed.stl')
cfg=r/'print_jobs/parent_spar_bolted/slice_validation'
a=[r'C:\Program Files\Bambu Studio\bambu-studio.exe','--debug','2','--datadir',str(work/'studio_data'),'--load-settings',str(cfg/'machine.json')+';'+str(cfg/'process.json'),'--load-filaments',str(cfg/'filament.json'),'--arrange','0','--orient','0','--slice','0','--outputdir',str(work),str(work/'placed.stl')]
p=subprocess.run(a,capture_output=True,text=True);(work/'slice.log').write_text(p.stdout+p.stderr,encoding='utf-8');d=json.loads((work/'result.json').read_text());assert d['return_code']==0,d;print('Adapter X1C slice PASS',m.extents)
