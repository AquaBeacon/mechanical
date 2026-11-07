"""Two X1C/PETG review plates with canonical local support blockers."""
from pathlib import Path
import copy,datetime,hashlib,json,subprocess,uuid,zipfile,xml.etree.ElementTree as E
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from slice_parent_spacers import paths

ROOT=Path(__file__).resolve().parents[1];ASM=ROOT/'assemblies/parent_hand_service'
WORK=ASM/'_work/analysis/retrofit_20261024/slicing';JOB=ASM/'print_jobs/retrofit_20261024'
EXE='C:/Program Files/Bambu Studio/bambu-studio.exe'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(cmd,folder,purpose):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.Popen(cmd,cwd=folder,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace',creationflags=0x08000000)
    record=dict(pid=p.pid,start_utc=started,purpose=purpose,command=cmd)
    write(folder/(purpose+'_process.json'),record);print('PROCESS '+json.dumps(record),flush=True)
    try:out,_=p.communicate(timeout=240)
    except subprocess.TimeoutExpired:
        p.terminate();out,_=p.communicate(timeout=10);raise
    (folder/(purpose+'.log')).write_text(out,encoding='utf-8')
    record.update(exit_code=p.returncode,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());write(folder/(purpose+'_process.json'),record)
    assert p.returncode==0,(purpose,out[-3000:])

def attach_blocker(seed,destination,base,blocker):
    with zipfile.ZipFile(seed) as z:data={n:z.read(n) for n in z.namelist()}
    core='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';prod='http://schemas.microsoft.com/3dmanufacturing/production/2015/06'
    E.register_namespace('',core);E.register_namespace('p',prod)
    model=E.fromstring(data['3D/3dmodel.model']);component=model.find('.//{'+core+'}component')
    childpath=component.attrib['{'+prod+'}path'].lstrip('/');child=E.fromstring(data[childpath])
    settings=E.fromstring(data['Metadata/model_settings.config']);host=settings.find('object')
    matrix=host.find("part/metadata[@key='matrix']").attrib['value']
    resources=child.find('{'+core+'}resources');index=max(int(o.attrib['id']) for tree in [model,child] for o in tree.findall('.//{'+core+'}object'))+1
    blocker=blocker.copy();blocker.apply_translation(-base.bounds.mean(axis=0))
    obj=E.SubElement(resources,'{'+core+'}object',id=str(index),type='model');mesh=E.SubElement(obj,'{'+core+'}mesh')
    vv=E.SubElement(mesh,'{'+core+'}vertices');ff=E.SubElement(mesh,'{'+core+'}triangles')
    for v in blocker.vertices:E.SubElement(vv,'{'+core+'}vertex',**{k:format(float(a),'.9g') for k,a in zip('xyz',v)})
    for f in blocker.faces:E.SubElement(ff,'{'+core+'}triangle',**{k:str(int(a)) for k,a in zip(['v1','v2','v3'],f)})
    extra=copy.deepcopy(component);extra.attrib['objectid']=str(index);extra.attrib['{'+prod+'}UUID']=str(uuid.uuid4());model.find('.//{'+core+'}components').append(extra)
    part=E.SubElement(host,'part',id=str(index),subtype='support_blocker',uuid=str(uuid.uuid4()))
    E.SubElement(part,'metadata',key='name',value='Nut and blind-hole support exclusions');E.SubElement(part,'metadata',key='matrix',value=matrix)
    for key,value in [('3D/3dmodel.model',model),(childpath,child),('Metadata/model_settings.config',settings)]:data[key]=E.tostring(value,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in data.items():z.writestr(n,b)

def main():
    WORK.mkdir(parents=True,exist_ok=True);JOB.mkdir(parents=True,exist_ok=True)
    manifest=read(ASM/'parts/manifest.json');entries={r['stem']:r for r in manifest['parts']}
    blockers={r['host']:r for r in manifest['modifiers']}
    box_records={r['host']:r['boxes'] for r in read(WORK.parent/'support_blockers.json')}
    plates=[ [('main_service_frame',25,32),('antenna_service_shelf',25,142),('power_adapter',165,32)],
             [('ann_mb1_coax_ring_service',25,32),('gnss_fixed_column_0',180,32),('gnss_fixed_column_1',200,32),('gnss_fixed_column_2',220,32),('gnss_sony_shared_column',232,32),('sony_fixed_column_0',180,60),('sony_fixed_column_1',200,60),('sony_fixed_column_3',220,60)]+
             [('cradle_floor_foot_'+str(i),180+20*i,90) for i in range(4)]+[('sony_mount_plate',180,150)] ]
    index={p.stem:p for p in Path('C:/Program Files/Bambu Studio/resources/profiles/BBL').rglob('*.json')}
    def resolve(name):
        d=read(index[name]);result={}
        if d.get('inherits'):result.update(resolve(d['inherits']))
        for item in d.get('include',[]):result.update(resolve(item))
        result.update(d);result.pop('inherits',None);result.pop('include',None);return result
    machine=resolve('Bambu Lab X1 Carbon 0.4 nozzle');machine['curr_bed_type']='Textured PEI Plate'
    process=resolve('0.20mm Standard @BBL X1C')
    process.update(print_settings_id='Parent retrofit PETG 0.2 wall4 solid with nut blockers',layer_height='0.2',initial_layer_print_height='0.2',wall_loops='4',top_shell_layers='5',bottom_shell_layers='5',sparse_infill_density='100%',sparse_infill_pattern='zig-zag',brim_type='outer_only',brim_width='3',enable_support='1',support_type='normal(auto)',support_on_build_plate_only='0',support_threshold_angle='45',dont_support_bridges='0',support_top_z_distance='0.2',support_bottom_z_distance='0.2',support_object_xy_distance='0.35',support_interface_top_layers='2',enable_prime_tower='0',skirt_loops='0')
    for n,d in [('machine',machine),('process',process),('filament',resolve('Generic PETG'))]:write(WORK/(n+'.json'),d)
    records=[]
    for number,members in enumerate(plates,1):
        folder=WORK/('plate_'+str(number));folder.mkdir(exist_ok=True)
        meshes=[];mods=[];placed=[];forbidden=[]
        for name,x,y in members:
            entry=entries[name];source=ASM/'parts'/entry['file'];assert sha(source)==entry['sha256']
            mesh=trimesh.load_mesh(source);shift=np.array([x,y,0])-mesh.bounds[0];mesh.apply_translation(shift);meshes.append(mesh)
            placed.append(dict(stem=name,file=entry['file'],sha256=entry['sha256'],bounds=mesh.bounds.tolist()))
            if name in blockers:
                mod=trimesh.load_mesh(ASM/'parts'/blockers[name]['file']);mod.apply_translation(shift);mods.append(mod)
                # Source -> print pose/bed -> plate transform, shared with sync.
                angle=np.radians(entry['rotation_deg']);rotation=trimesh.transformations.euler_matrix(*angle)
                original=trimesh.load_mesh(ROOT/entry['source']) if 'source' in entry else trimesh.load_mesh(ROOT/entry['part']/(name+'.stl'))
                original.apply_transform(rotation);translation=-original.bounds[0]+shift
                for b in box_records[name]:
                    corners=trimesh.bounds.corners(np.array([b[:3],np.array(b[:3])+b[3:]]));corners=trimesh.transform_points(corners,rotation)+translation
                    lo,hi=corners.min(axis=0),corners.max(axis=0)
                    # MAIN arms start at Z37.1, feet print datum is33.4.
                    # Supports below that open underside are removable from below;
                    # they are not inside a bore or captive nut pocket.
                    if name=='main_service_frame' and b[3]==4.2 and b[4]==4.2:lo[2]=max(lo[2],3.7)
                    forbidden.append([lo.tolist(),hi.tolist()])
        base=trimesh.util.concatenate(meshes);blocked=trimesh.util.concatenate(mods);staged=folder/'placed.stl';base.export(staged)
        common=[EXE,'--debug','2','--datadir',str(folder/'studio_data'),'--load-settings',str(WORK/'machine.json')+';'+str(WORK/'process.json'),'--load-filaments',str(WORK/'filament.json'),'--arrange','0','--orient','0']
        run(common+['--slice','0','--export-3mf','seed.3mf','--outputdir',str(folder),str(staged)],folder,'seed')
        attach_blocker(folder/'seed.3mf',folder/'blocked.3mf',base,blocked)
        project='retrofit_plate_'+str(number)+'.3mf'
        run(common+['--slice','0','--export-3mf',project,'--outputdir',str(folder),str(folder/'blocked.3mf')],folder,'slice')
        result=read(folder/'result.json');assert result['return_code']==0,result
        with zipfile.ZipFile(folder/project) as z:
            assert z.testzip() is None
            config=E.fromstring(z.read('Metadata/model_settings.config'));assert len(config.findall("object/part[@subtype='support_blocker']"))==1
            (folder/'plate_1.gcode').write_bytes(z.read('Metadata/plate_1.gcode'))
        segments=paths(folder/'plate_1.gcode');bounds=np.concatenate([p for _,f,p in segments if f!='Custom'])
        support=[p for _,f,p in segments if f.lower().startswith('support')]
        bad=0
        if support:
            mid=np.concatenate([(p[:-1]+p[1:])/2 for p in support])
            for lo,hi in forbidden:bad+=int(np.count_nonzero(np.all(mid>np.array(lo)+.2,axis=1)&np.all(mid<np.array(hi)-.2,axis=1)))
        for member in placed:
            bb=np.array(member['bounds']);zs=[z for z,f,p in segments if f=='Outer wall' and np.all(p[:,:2].mean(axis=0)>=bb[0,:2]-.05) and np.all(p[:,:2].mean(axis=0)<=bb[1,:2]+.05)]
            member['outer_wall_z']=[min(zs),max(zs)] if zs else None
            member['present']=bool(zs and min(zs)<=.21 and max(zs)>=bb[1,2]-.4)
        good=all(m['present'] for m in placed) and bad==0 and np.all(bounds[:,:2].min(axis=0)>.25) and np.all(bounds[:,:2].max(axis=0)<255.75)
        record=dict(plate=number,passed=bool(good),members=placed,support_segments=len(support),support_segments_inside_blockers=bad,extrusion_bounds=bounds.min(axis=0).tolist()+bounds.max(axis=0).tolist(),result=result,source_stl_sha256=sha(staged),three_mf_sha256=sha(folder/project),profile='X1C 0.4 / Generic PETG / 0.2mm / 4 walls / 100% / auto supports45deg / bridge exemption OFF / local blockers')
        records.append(record);write(folder/'review.json',record)
        # Actual extruding layers: model blue, support orange.
        fig,axs=plt.subplots(2,3,figsize=(13,9));layers=sorted(set(z for z,f,p in segments if f!='Custom'))
        for ax,target in zip(axs.flat,[.2,2.6,4,10,14,max(layers)-.2]):
            z=min(layers,key=lambda a:abs(a-target))
            for is_support,color in [(False,'#24658f'),(True,'#de8c2b')]:
                lines=[p[:,:2] for zz,f,p in segments if abs(zz-z)<.001 and f!='Custom' and f.lower().startswith('support')==is_support]
                if lines:ax.add_collection(LineCollection(lines,colors=color,linewidths=.35))
            ax.set(xlim=(0,256),ylim=(0,256),aspect='equal',title=f'Z {z:.2f} mm');ax.grid(alpha=.1)
        fig.suptitle(f'Retrofit plate {number}: actual G-code / blue=model, orange=support')
        fig.tight_layout();fig.savefig(ASM/f'_work/images/retrofit_plate_{number}_layers.png',dpi=140);plt.close(fig)
        assert good,record
        (JOB/project).write_bytes((folder/project).read_bytes())
        print('PLATE_PASS '+str(number),flush=True)
        del segments,bounds,base,blocked,meshes,mods
    write(JOB/'manifest.json',dict(passed=all(r['passed'] for r in records),plates=records,limitations=['Physical printing and bridge quality remain unverified; inspect nut pockets and remove accessible support before assembly.']))
if __name__=='__main__':main()

