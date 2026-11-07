"""Conservative continuous vertical extraction check by adaptive solid covers."""
import json
import FreeCAD as A,Part

def verify(doc,scene):
    moving=['main_mount_plate','p_main','antenna_ground_plate','gnss_antenna']
    fixed=['p_pwr','power_adapter','coax_ring','coax_coil_keepout','box_bcas212310g','lipo','lipo_tray','lipo_ret_lid','spresense','tx_improved','gnss_universal_carrier','sony_mount_plate']
    fixed += [n for n in scene if 'fixed_column' in n or n=='gnss_sony_shared_column' or n.startswith('cradle_floor_foot_')]
    obstacles=[(name,q,q.BoundBox) for name in fixed for q in scene[name].Solids]
    travel=120.;records=[]
    def overlaps(s,t):
        c=s.common(t);return 0. if c.isNull() else c.Volume
    for name in moving:
        stack=[scene[name]];count=0;clear=0;unresolved=[]
        while stack and count<3500:
            s=stack.pop();count+=1;b=s.optimalBoundingBox(False,False)
            prism=Part.makeBox(b.XLength,b.YLength,b.ZLength+travel,A.Vector(b.XMin,b.YMin,b.ZMin))
            possible=[(n,q) for n,q,bb in obstacles if prism.BoundBox.intersect(bb)]
            hits=[n for n,q in possible if overlaps(prism,q)>1e-5]
            if not hits:clear+=1;continue
            lengths=[b.XLength,b.YLength,b.ZLength]
            axis=max(range(3),key=lambda i:lengths[i])
            if lengths[axis]<.15:
                unresolved.append(dict(bounds=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],obstacles=sorted(set(hits))))
                continue
            lo=[b.XMin,b.YMin,b.ZMin];sizes=lengths[:];sizes[axis]/=2
            for side in [0,1]:
                p=lo[:];p[axis]+=side*sizes[axis]
                clip=Part.makeBox(*sizes,A.Vector(*p))
                cut=s.common(clip)
                if not cut.isNull() and cut.Volume>1e-6:stack.append(cut)
            if count%100==0:print('SWEEP_PROGRESS='+json.dumps(dict(part=name,nodes=count,pending=len(stack))),flush=True)
        row=dict(part=name,travel_mm=travel,nodes=count,clear_cover_boxes=clear,unresolved=unresolved,pending=len(stack),
                 continuous_envelope_pass=not unresolved and not stack)
        records.append(row);print('SWEEP='+json.dumps(row),flush=True)
    # Exact straight tool envelopes for service nuts and case anchor access.
    from parent_case_access import tool
    from parent_service_retrofit import BASE_HEAD_Z
    import parent_gnss as G
    tool_rows=[]
    tool_fixed=fixed+['main_mount_plate','p_main','antenna_ground_plate','gnss_antenna']
    probes=[('case_anchor_'+str(i),tool(i)) for i in [0,2]]
    probes += [('cradle_bolt_'+str(i),Part.makeCylinder(3.2,100,A.Vector(x,y,BASE_HEAD_Z+.01))) for i,(x,y) in enumerate(G.RACK_FOOT_XY)]
    for label,p in probes:
        hits=[]
        for n in tool_fixed:
            if label.startswith('case_anchor') and n in moving:continue # module removed first
            if p.BoundBox.intersect(scene[n].BoundBox):
                vol=overlaps(p,scene[n])
                if vol>.001:hits.append(dict(part=n,volume_mm3=vol))
        tool_rows.append(dict(label=label,hits=hits))
    report=dict(status='GEOMETRY_ONLY',motion=records,tools=tool_rows,
                method='Adaptive exact solid clipping; each retained piece is covered by a bounding prism over the ENTIRE +Z120mm path. A zero common volume certifies each conservative cover; unresolved cells are never a pass.',
                limitations=['Disconnect wiring before extraction; cable flexibility and user grip not modeled.','Service head/driver passage OD6.4; case anchors are accessed AFTER module removal.','No physical assembly or strength validation.'])
    print('SERVICE_REPORT='+json.dumps(report),flush=True)
    o=doc.addObject('Part::Feature','verification_marker');o.Label='SERVICE CHECK MARKER - NOT PRINTABLE'
    o.Shape=Part.makeBox(1,1,1);o.addProperty('App::PropertyString','Report');o.Report=json.dumps(report)
    return [o]
