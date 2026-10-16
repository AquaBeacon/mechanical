"""Rebuild the purchased-case reference from TAKACHI's original two-view DXF.

Host Python extracts analytic plan contours. FreeCAD creates draft walls and
separate body/cover solids. This is a drawing-derived reference, not vendor STEP.
Unspecified three-dimensional corner draft and screw threads remain documented.
"""
from pathlib import Path
import json, math, sys, hashlib, subprocess
R=Path(__file__).resolve().parents[1]
P=R/'parts/parent/exterior/cots/bcas212310g'
O=P/'_work/analysis/cad_correction_20261010';O.mkdir(parents=True,exist_ok=True)

def host():
    import ezdxf
    from shapely.geometry import LineString
    from shapely.ops import polygonize
    doc=ezdxf.readfile(P/'ref/BCAS212310G.dxf')
    x0,y0=2138.300000000003,455.258585011398
    entities=[]; circles=[]
    for e in doc.modelspace():
        if 'FF8E' not in e.dxf.layer:continue
        for q in e.virtual_entities() if e.dxftype()=='LWPOLYLINE' else [e]:
            k=q.dxftype()
            if k=='LINE':
                ps=[list(q.dxf.start)[:2],list(q.dxf.end)[:2]]
                row=dict(kind=k,handle=e.dxf.handle,start=ps[0],end=ps[1])
            elif k in ['ARC','CIRCLE']:
                a=q.dxf.start_angle if k=='ARC' else 0;b=q.dxf.end_angle if k=='ARC' else 360
                if b<=a:b+=360
                cx,cy=list(q.dxf.center)[:2];rad=q.dxf.radius
                ps=[[cx+rad*math.cos(math.radians(a+(b-a)*i/64)),cy+rad*math.sin(math.radians(a+(b-a)*i/64))] for i in range(65)]
                row=dict(kind=k,handle=e.dxf.handle,centre=[cx,cy],radius=rad,start_angle=a,end_angle=b)
            else:continue
            if not (min(x for x,y in ps)>=x0-1e-6 and max(x for x,y in ps)<=x0+230+1e-6 and min(y for x,y in ps)>=y0-1e-6 and max(y for x,y in ps)<=y0+210+1e-6):continue
            if k=='CIRCLE':circles.append(row);continue
            row['polyline']=[(round(x,6),round(y,6)) for x,y in ps]
            entities.append(row)
    polys=list(polygonize([LineString(q['polyline']) for q in entities]))
    main=max(polys,key=lambda p:p.area)
    main_outline=LineString(main.exterior.coords)
    outer_skin=next(p for p in polys if p.area>1000 and 2139.5<p.bounds[0]<2140.5)
    skin_outline=LineString(outer_skin.exterior.coords)
    profiles={}
    for name,line in [('opening',main_outline),('skin_outer',skin_outline)]:
        rows=[]
        for q in entities:
            # Every sampled point of this analytic curve must belong to the loop.
            if max(line.distance(__import__('shapely').geometry.Point(v)) for v in q['polyline'])>2e-6:continue
            q={k:v for k,v in q.items() if k!='polyline'}
            for k in ['start','end','centre']:
                if k in q:q[k]=[q[k][1]-y0,q[k][0]-x0]  # case X=DXF Y, case Y=DXF X
            rows.append(q)
        profiles[name]=rows
    ins=set();tap=set()
    for q in circles+entities:
        if q['kind'] not in ['CIRCLE','ARC']:continue
        c=q['centre'];xy=(round(c[1]-y0,5),round(c[0]-x0,5))
        if abs(q['radius']-1.7)<1e-8:tap.add(xy)
        if abs(q['radius']-2)<1e-8 and xy[0] in [25,185] and xy[1] in [25,205]:ins.add(xy)
    assert len(ins)==4 and len(tap)==12,(ins,tap)
    # The 3 / 7 callouts and the wall endpoints are read from section B-B,
    # rather than interpreting the 193.2 x173.2 clear span as a raised floor.
    def pt(handle,field):return doc.entitydb[handle].dxf.get(field)
    floor_y=pt('13601','start').y
    floor_t=floor_y-pt('135F4','start').y
    boss_top=floor_y-pt('135EE','start').y
    left_inner=[list(pt('13612',k))[:2] for k in ['start','end']]
    left_outer=[list(pt('1360B',k))[:2] for k in ['start','end']]
    def section(rows):return [[floor_y-y,x-x0] for x,y in rows]
    data=dict(source='TAKACHI BCAS212310G.dxf, 2026-02-24',source_sha256=hashlib.sha256((P/'ref/BCAS212310G.dxf').read_bytes()).hexdigest(),
        coordinate_system='Case X210 / Y230; main exterior floor datum Z0. External boss feet reach Z-1.',
        floor_thickness_mm=round(floor_t,6),boss_top_z_mm=round(boss_top,6),boss_height_mm=round(boss_top-floor_t,6),
        insert_xy_mm=sorted(ins),tapping_xy_mm=sorted(tap),profiles=profiles,inner_wall_section=section(left_inner),outer_wall_section=section(left_outer),
        body_seam_z_mm=80.0,body_tongue_top_z_mm=83.5,cover_seam_z_mm=80.3,cover_top_z_mm=100.3,cover_roof_bottom_z_mm=97.1,
        model_status='drawing_derived_fit_reference',limitations=['Manufacturer STEP not available for this model in the public product table.','Plan corner walls are extruded vertically; their unsectioned molding draft is not specified by these drawings.','Cover gasket uses the catalog 0.3 mm assembled offset. Thread helices, guide marks and hardware are omitted.','Exterior boss feet are drawing geometry at Z-1; catalog height100.3 is between the main floor and cover crown, not the lowest foot.','Fit must be confirmed against physical case or official 3D CAD before release.'])
    (P/'dimensions.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    kernel=Path('C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/python.exe')
    subprocess.run([str(kernel),str(Path(__file__).resolve()),'--kernel'],check=True,cwd=R)

def kernel():
    import FreeCAD as A, Part, MeshPart
    d=json.loads((P/'dimensions.json').read_text(encoding='utf-8'))
    def v(x=0,y=0,z=0):return A.Vector(x,y,z)
    def rr(inset,z):
        # All corner centers remain8.5 mm from the catalog outside edges.
        rad=8.5-inset;w=210-2*inset;h=230-2*inset
        coords=[(inset+rad,inset),(inset+w-rad,inset),(inset+w,inset+rad),(inset+w,inset+h-rad),(inset+w-rad,inset+h),(inset+rad,inset+h),(inset,inset+h-rad),(inset,inset+rad)]
        edges=[]
        for i in range(0,8,2):
            edges.append(Part.makeLine(v(*coords[i],z),v(*coords[(i+1)%8],z)))
            p0=coords[(i+1)%8];p1=coords[(i+2)%8]
            centres=[(210-8.5,8.5),(210-8.5,230-8.5),(8.5,230-8.5),(8.5,8.5)]
            cx,cy=centres[i//2];a=[-math.pi/4,math.pi/4,3*math.pi/4,5*math.pi/4][i//2]
            edges.append(Part.Arc(v(*p0,z),v(cx+rad*math.cos(a),cy+rad*math.sin(a),z),v(*p1,z)).toShape())
        return Part.Wire(edges)
    def contour(name,z=0):
        es=[]
        for q in d['profiles'][name]:
            if q['kind']=='LINE':es.append(Part.makeLine(v(*q['start'],z),v(*q['end'],z)))
            else:
                # DXF XY were transposed, so angle orientation is reversed.
                cx,cy=q['centre'];r=q['radius'];a=q['start_angle'];b=q['end_angle']
                pts=[v(cx+r*math.sin(math.radians(t)),cy+r*math.cos(math.radians(t)),z) for t in [a,(a+b)/2,b]]
                es.append(Part.Arc(*pts).toShape())
        groups=Part.sortEdges(es)
        assert len(groups)==1,(name,len(groups))
        wire=Part.Wire(groups[0]);assert wire.isClosed(),name
        return wire
    def at(section,z):
        (z0,q0),(z1,q1)=section
        return q0+(q1-q0)*(z-z0)/(z1-z0)
    outer_z=[0,1,75,75.5,80]
    outer_inset=[3.550234,at(d['outer_wall_section'],1),.95,.3,0]
    outer=Part.makeLoft([rr(q,z) for q,z in zip(outer_inset,outer_z)],True,True)
    inner=Part.makeLoft([rr(6.078495,3),rr(at(d['inner_wall_section'],3.5),3.5),rr(at(d['inner_wall_section'],76.5),76.5),rr(2.9,77),rr(2.9,84)],True,True)
    body=outer.cut(inner)
    # Retain both analytic inner wall contours, including the C-shaped corner
    # bays. A small cylinder at(9,9) alone misses their18 mm intrusion.
    corner_skin=Part.Face(contour('skin_outer',3)).cut(Part.Face(contour('opening',3))).extrude(v(0,0,77))
    body=body.fuse(corner_skin)
    lip=Part.Face(rr(1,80)).cut(Part.Face(rr(4,80))).extrude(v(0,0,3.5))
    body=body.fuse(lip)
    for points,base_r,top_r,hole_r in [(d['insert_xy_mm'],5,4.5,1.75),(d['tapping_xy_mm'],4.5,4,1.7)]:
        for x,y in points:
            boss=Part.makeCone(base_r,top_r,7,v(x,y,3)).cut(Part.makeCylinder(hole_r,8,v(x,y,2)))
            # Section shows the molding's small outside foot, not a floor rib.
            foot=Part.makeCylinder(top_r-.5,1,v(x,y,-1))
            body=body.fuse(boss).fuse(foot)
    for x in [9,201]:
        for y in [9,221]:
            body=body.fuse(Part.makeCylinder(5.25,77,v(x,y,3)))
            body=body.cut(Part.makeCylinder(2.1,81,v(x,y,-.5)))
    body=body.removeSplitter()
    clearance_wire=contour('opening').makeOffset2D(-.5)
    if clearance_wire.ShapeType!='Wire':clearance_wire=clearance_wire.Wires[0]
    assert clearance_wire.BoundBox.XMin>3.39 and clearance_wire.BoundBox.XMax<206.61
    clearance=Part.Face(clearance_wire).extrude(v(0,0,100))
    clearance.exportStep(str(P/'interior_corner_clearance.step'))
    # Separate closed lid; retain it as the existing lid_keepout item so all
    # lid-open service checks continue to exclude only the removed lid.
    cover=Part.makeLoft([rr(0,80.3),rr(1.2,100.3)],True,True)
    cover=cover.cut(Part.makeLoft([rr(5,80.2),rr(5.1235,97.1)],True,True))
    gasket_channel=Part.Face(rr(.8,80.2)).cut(Part.Face(rr(4.2,80.2))).extrude(v(0,0,3.6))
    cover=cover.cut(gasket_channel)
    for x in [9,201]:
        for y in [9,221]:cover=cover.cut(Part.makeCylinder(3,21,v(x,y,80)))
    cover=cover.removeSplitter()
    assert body.common(cover).Volume<.01,'Body/lid mating must be clear'
    checks=[]
    for stem,s in [('bcas212310g',body),('bcas212310g_cover',cover)]:
        assert s.isValid() and len(s.Solids)==1,(stem,len(s.Solids))
        s.exportStep(str(P/(stem+'.step')))
        mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.05,AngularDeflection=.1,Relative=False)
        mesh.write(str(P/(stem+'.stl')))
        pts,faces=mesh.Topology
        (P/(stem+'.scad')).write_text('// Drawing-derived COTS reference; generated by spec/build_bcas212310g.py. Not printable.\npolyhedron(points='+json.dumps([[q.x,q.y,q.z] for q in pts])+',faces='+json.dumps([list(f) for f in faces])+',convexity=10);\n',encoding='utf-8')
        b=s.BoundBox;checks.append(dict(part=stem,valid=s.isValid(),solids=len(s.Solids),bbox_mm=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],volume_mm3=s.Volume,mesh_closed=mesh.isSolid()))
    (O/'cad_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');print(json.dumps(checks,indent=2))

if __name__=='__main__':
    kernel() if '--kernel' in sys.argv else host()
