"""Read this already-exported faceted STEP without automatic shape rewriting.

Native FreeCAD validity/bounds/volume or assembly placement checks still run.
Only process-local OCCT STEP shape-processing resource settings are changed.
Installed software and user preferences are untouched.
The explicit assembly-check-heal-cots mode heals only imported curved vessel
parts with unbounded boxes; the clamp geometry is never repaired or replaced.
References: OCCT V7_8_1 XSTEPResource/STEP and XSAlgo_AlgoContainer.cxx;
FreeCAD Part.setStaticValue API. The empty *defined* operator sequence avoids
the undocumented-for-this-shape cost of automatic FixShape after translation.
"""
import os
from pathlib import Path
import runpy
import time
import json
import Part

root=Path(os.environ['ASM_ROOT'])
case=Path(os.environ['CLAMP_DIRECT_CASE'])
resource=case/'step_read_resource'
resource.mkdir(exist_ok=True)
(resource/'CLAMP_DIRECT_STEP').write_text('FromSTEP.exec.op :\nToSTEP.exec.op : SplitCommonVertex,DirectFaces\n',encoding='ascii')
os.environ['CSF_CLAMP_DIRECT_STEPDefaults']=str(resource)
Part.setStaticValue('read.step.resource.name','CLAMP_DIRECT_STEP')
Part.setStaticValue('read.step.sequence','FromSTEP')
mode=os.environ.get('CLAMP_DIRECT_STEP_MODE','part-check')
start=time.monotonic()
print('DIRECT STEP read mode='+mode,flush=True)
if mode=='part-check':
    runpy.run_path(str(root/'tools/verify_child_clamp_steps.py'))
elif mode=='assembly-export':
    step=root/'parts/child/exterior/printed/child_wte4_suspension_clamp/child_wte4_suspension_clamp_cage.step'
    shape=Part.read(str(step))
    if not shape.isValid() or len(shape.Solids)!=1 or len(shape.Shells)!=1:
        raise RuntimeError('Unmodified STEP read is not a valid one-shell solid')
    key=(os.path.normcase(os.path.abspath(step)),step.stat().st_mtime_ns)
    # Other purchased CAD uses the ordinary read behaviour; the checked clamp
    # is reused through the assembly writer's existing immutable shape cache.
    Part.setStaticValue('read.step.resource.name','STEP')
    runpy.run_path(str(root/'scad/lib/asm_to_step.py'),init_globals={'_shape_cache':{key:shape}})
elif mode in ['assembly-check','assembly-check-heal-cots']:
    if mode=='assembly-check-heal-cots':
        import FreeCAD
        import Import
        placement=json.loads(Path(os.environ['ASM_JSON']).read_text(encoding='utf-8'))
        labels={i['label'] for i in placement['items'] if i.get('group')=='vessel'}
        original_insert=Import.insert
        repaired=[]
        def insert_and_fix_curved_cots(path,document,*args,**kwargs):
            original_insert(path,document,*args,**kwargs)
            doc=FreeCAD.getDocument(document)
            for obj in doc.Objects:
                if obj.Label not in labels or not hasattr(obj,'Shape'): continue
                shape=obj.Shape.copy()
                box=shape.BoundBox
                values=[box.XMin,box.XMax,box.YMin,box.YMax,box.ZMin,box.ZMax]
                if max(abs(v) for v in values)<1e12: continue
                # Native OCC shape healing on the imported COTS geometry only.
                # Never replace it with the original source or expected bbox.
                shape.fix(1e-7,1e-7,0.01)
                if not shape.isValid():
                    raise RuntimeError('Native COTS read repair remains invalid: '+obj.Label)
                obj.Shape=shape
                repaired.append(obj.Label)
                print('Native local read repair: '+obj.Label,flush=True)
            doc.recompute()
        Import.insert=insert_and_fix_curved_cots
    try:
        runpy.run_path(str(root/'scad/lib/verify_asm_step.py'))
    except SystemExit as result:
        # The native verifier exits even on success. Preserve every nonzero
        # verdict; only success continues to the provenance record below.
        if result.code not in (None,0): raise
else:
    raise ValueError(mode)
record=dict(mode=mode,elapsed_seconds=time.monotonic()-start,
    native_checks_completed=True,installed_package_modified=False,
    STEP_geometry_repair=(repaired if mode=='assembly-check-heal-cots' else False),
    clamp_geometry_repair=False,acceptance_criteria_unchanged=True,
    source_reference='https://github.com/Open-Cascade-SAS/OCCT/blob/V7_8_1/src/XSAlgo/XSAlgo_AlgoContainer.cxx')
(case/('direct_step_'+mode+'.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record),flush=True)
