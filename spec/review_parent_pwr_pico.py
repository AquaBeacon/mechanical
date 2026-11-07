"""Review original PWR orientation and measured17mm Pico envelope, read-only."""
from pathlib import Path
import json
import FreeCAD as A
import Part

def build(doc,parameters):
    root=Path(__file__).resolve().parents[1];base=root/'assemblies/parent_hand_service'
    current=json.loads((base/'placement.json').read_text(encoding='utf-8'))
    old=json.loads((base/'_work/analysis/retrofit_20261024/placement_before_retrofit.json').read_text(encoding='utf-8'))
    cache={}
    def placed(row):
        folder=root/row['part'];path=folder/(row.get('file',folder.name)+'.step')
        if str(path) not in cache:cache[str(path)]=Part.read(str(path))
        s=cache[str(path)].copy()
        for op in reversed(row.get('ops',[])):
            for axis,ang in zip([A.Vector(1,0,0),A.Vector(0,1,0),A.Vector(0,0,1)],op.get('rotate',[0,0,0])):
                if ang:s.rotate(A.Vector(),axis,ang)
            if 'translate' in op:s.translate(A.Vector(*op['translate']))
        return s
    labels={'plate','p_main','p_pwr','gnss_universal_carrier','gnss_universal_pcb','magnetometer','gnss_receiver','gnss_sma_plug','antenna_ground_plate','gnss_antenna','main_service_frame','antenna_service_shelf','power_adapter','coax_ring','coax_service_loop','coax_receiver_service','box_bcas212310g','lid_keepout','lipo','lipo_tray','lipo_ret_lid','spresense','sony_mount_plate','tx_improved'}
    scene={r['label']:placed(r) for r in current['items'] if r['label'] in labels or r['label'].startswith(('gnss_fixed_','sony_fixed_','gnss_sony_','cradle_floor_','retrofit_'))}
    pwr=placed(next(r for r in old['items'] if r['label']=='p_pwr'))
    if parameters.get('scan',0):
        scans=[]
        for south in [14,17,20,23]:
            for lift in [7,5.5]:
                bodies={'p_pwr':pwr.copy()};bodies['p_pwr'].translate(A.Vector(0,-south,lift))
                for name,x in [('xt_bat',42.3),('xt_tx',76.3)]:bodies[name]=Part.makeBox(17.4,20,9.2,A.Vector(x-8.7,95.849125-south,27.895+lift))
                hits=[]
                for a,s in bodies.items():
                    for b,t in scene.items():
                        if b in {'p_pwr','power_adapter'} or b.startswith('retrofit_'):continue
                        if not s.BoundBox.intersect(t.BoundBox):continue
                        aa=[q for q in s.Solids if q.BoundBox.intersect(t.BoundBox)];bb=[q for q in t.Solids if q.BoundBox.intersect(s.BoundBox)]
                        if not aa or not bb:continue
                        overlap=Part.makeCompound(aa).common(Part.makeCompound(bb))
                        if overlap.Volume>.001:
                            q=overlap.BoundBox;hits.append(dict(a=a,b=b,volume=overlap.Volume,bounds=[q.XMin,q.YMin,q.ZMin,q.XMax,q.YMax,q.ZMax]))
                row=dict(south=south,lift=lift,hits=hits);scans.append(row);print('SCAN='+json.dumps(row),flush=True)
        obj=doc.addObject('PartDesign::Feature','ReviewMarker');obj.Shape=Part.makeBox(1,1,1);return [obj]
    south=parameters.get('south',11);lift=parameters.get('lift',7)
    pwr.translate(A.Vector(0,-south,lift));scene['p_pwr']=pwr
    # PICO1 at(30,84.6),180deg, model offset(8.89,-24.13):
    # assembly centre(39.11,51.53). Existing model XY 21x53.6 plus0.5mm per side.
    # MAIN board underside45 + FR4 1.6; measured height17 above top.
    scene['pico_17mm']=Part.makeBox(22,54.6,17,A.Vector(28.11,24.23,46.6))
    scene['pico_18mm_guard']=Part.makeBox(22,54.6,18,A.Vector(28.11,24.23,46.6))
    for name,x in [('xt_bat',42.3),('xt_tx',76.3)]:
        scene[name]=Part.makeBox(17.4,20,9.2,A.Vector(x-8.7,95.849125-south,27.895+lift))
    rows=[]
    targets=list(scene)
    for a in ['p_pwr','xt_bat','xt_tx','pico_17mm','pico_18mm_guard']:
        for b in targets:
            if b in {'p_pwr','xt_bat','xt_tx','pico_17mm','pico_18mm_guard'}:continue
            if a.startswith('pico') and (b=='p_main' or b.startswith('retrofit_main_pcb_')):continue
            if a=='p_pwr' and b.startswith('retrofit_pwr_pcb_'):continue
            s,t=scene[a],scene[b];v=0.0
            if s.BoundBox.intersect(t.BoundBox):
                aa=[q for q in s.Solids if q.BoundBox.intersect(t.BoundBox)];bb=[q for q in t.Solids if q.BoundBox.intersect(s.BoundBox)]
                if aa and bb:
                    overlap=Part.makeCompound(aa).common(Part.makeCompound(bb));v=overlap.Volume
            row=dict(a=a,b=b,overlap_mm3=v)
            if v>.001:
                q=overlap.BoundBox;row['overlap_bounds']=[q.XMin,q.YMin,q.ZMin,q.XMax,q.YMax,q.ZMax]
            if a.startswith('pico') and b in {'main_service_frame','antenna_service_shelf','antenna_ground_plate','gnss_antenna','coax_service_loop'}:row['distance_mm']=s.distToShape(t)[0]
            rows.append(row)
            if v>.001:print('HIT '+json.dumps(row),flush=True)
    report=dict(parameters=dict(south=south,lift=lift,pwr_rotation=0),checks=rows,pico_envelope=[28.11,24.23,46.6,50.11,78.83,63.6],limitations=['Pico full XY prism includes0.5mm lateral margin; actual height supplied by user.','XT mating plug width/height inferred from body plus2mm; 20mm insertion depth.'])
    print('PWR_PICO_REVIEW='+json.dumps(report),flush=True)
    obj=doc.addObject('PartDesign::Feature','ReviewMarker');obj.Shape=Part.makeBox(1,1,1);return [obj]
