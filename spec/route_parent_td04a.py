"""TD04A 5 mm cable route and clearance audit; purchased cable, not a print.

python spec/route_parent_td04a.py
Creates an analytic line/arc route for FreeCAD and a sampled inspection mesh.
"""
from pathlib import Path
import json
import sys
import math
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scad/lib'))
from check_asm_contacts import load
OUT = ROOT / 'parts/common/cabling/parent_td04a_cable'
DIAMETER = 5.0  # User supplied, 2026-09-10.
RADIUS = 30.0  # Provisional centreline bend radius, not a cable manufacturer rating.
MARGIN = 1.0
SAMPLE_STEP = 0.25


def route():
    # Box bottom frame. Through the existing upper D8 eye at (65,-75,-385).
    # The TD04A rear centre is provisional until the sensor exit is measured.
    vertices = np.array([[65,-40,-438], [65,-40,-385], [65,-190,-385],
                         [65,-190,65], [-20,-190,65], [-20,-137,65]], dtype=float)
    corners = []
    for i in range(1, len(vertices)-1):
        a,b,c = vertices[i-1:i+2]
        u=(b-a)/np.linalg.norm(b-a); v=(c-b)/np.linalg.norm(c-b)
        angle=math.acos(np.clip(u@v,-1,1)); trim=RADIUS*math.tan(angle/2)
        start=b-u*trim; end=b+v*trim
        normal=np.cross(u,v); normal/=np.linalg.norm(normal)
        centre=start+np.cross(normal,u)*RADIUS
        radial=(start-centre)/RADIUS
        middle=centre+RADIUS*(radial*math.cos(angle/2)+np.cross(normal,radial)*math.sin(angle/2))
        points=np.array([centre+RADIUS*(radial*math.cos(t)+np.cross(normal,radial)*math.sin(t))
                         for t in np.linspace(0,angle,math.ceil(RADIUS*angle/SAMPLE_STEP)+1)])
        corners.append((start,end,middle,points,angle))
    segments=[]; samples=[]; previous=vertices[0]; length=0
    for index,(start,end,middle,points,angle) in enumerate(corners):
        direction=vertices[index+1]-vertices[index]
        assert (start-previous)@direction >= 0, 'Bend tangencies overlap'
        distance=np.linalg.norm(start-previous)
        segments.append(dict(kind='line',start=previous.tolist(),end=start.tolist()))
        samples.extend(np.linspace(previous,start,max(2,math.ceil(distance/SAMPLE_STEP)+1))[:-1])
        segments.append(dict(kind='arc',start=start.tolist(),middle=middle.tolist(),end=end.tolist()))
        samples.extend(points[:-1]); length+=distance+RADIUS*angle; previous=end
    assert (vertices[-1]-previous)@(vertices[-1]-vertices[-2]) > 0
    distance=np.linalg.norm(vertices[-1]-previous)
    segments.append(dict(kind='line',start=previous.tolist(),end=vertices[-1].tolist()))
    samples.extend(np.linspace(previous,vertices[-1],math.ceil(distance/SAMPLE_STEP)+1))
    return segments,np.array(samples),length+distance


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    segments,points,length=route()
    data=dict(diameter_mm=DIAMETER,bend_radius_mm=RADIUS,margin_mm=MARGIN,
              bend_radius_status='PROVISIONAL',length_mm=length,
              endpoint_status='TD rear-centre and gland exterior face are existing reference geometry; measure before final fit',
              segments=segments)
    (OUT/'route.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    np.save(OUT/'centreline.npy',points)
    # Polyline cylinders are only a visual reference; analytic STEP/STL are exported by FreeCAD.
    scad='// Purchased cable route; not printable. Generated from route.json.\n'
    scad+='cable_d=5;\nclearance=0; // set 1 for occupied-space review\n$fn=24;\n'
    scad+='points='+json.dumps(points.round(5).tolist())+';\n'
    scad+='for(i=[0:len(points)-2]) hull(){translate(points[i]) sphere(d=cable_d+2*clearance); translate(points[i+1]) sphere(d=cable_d+2*clearance);}\n'
    (OUT/'parent_td04a_cable.scad').write_text(scad,encoding='utf-8')
    asm=json.loads((ROOT/'assemblies/parent_integrated/placement.json').read_text(encoding='utf-8'))
    checks=[]
    for it in asm['items']:
        if it['group'] in ['cabling','cable_clearance'] or it['label']=='td04a_envelope':
            continue
        mesh=load(ROOT,it)
        pad=DIAMETER/2+MARGIN+2
        candidate=points[np.all(points>=mesh.bounds[0]-pad,axis=1)&np.all(points<=mesh.bounds[1]+pad,axis=1)]
        if not len(candidate):
            continue
        _,dist,_=trimesh.proximity.closest_point(mesh,candidate)
        inside=mesh.contains(candidate) if mesh.is_watertight else np.zeros(len(candidate),bool)
        gap=float(dist.min()-DIAMETER/2)
        # At the gland face the cable intentionally enters the purchased seal opening.
        required=0 if it['label']=='pen_td04a' else MARGIN
        checks.append(dict(part=it['label'],minimum_surface_gap_mm=gap,
                           conservative_gap_mm=gap-SAMPLE_STEP/2,
                           required_mm=required,inside_count=int(inside.sum()),
                           watertight=bool(mesh.is_watertight),
                           passed=bool(gap-SAMPLE_STEP/2>=required and not inside.any())))
    data['checks']=checks
    data['passed']=all(c['passed'] for c in checks)
    data['method']='Centreline spacing <=0.25mm, point-to-triangle distance minus radius; conservative gap subtracts half the spacing. Nonwatertight obstacles have no inside test; sensor endpoint is intentional contact. Floats/ropes only checked at modeled pose.'
    (OUT/'clearance_checks.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    print('Cable length',round(length,1),'mm; checks',checks,flush=True)
    return 0 if data['passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
