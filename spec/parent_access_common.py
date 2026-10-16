"""Exact STEP placement and broad-phase solid culling for parent CAD checks."""
import FreeCAD as A, Part
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
O=R/'assemblies/parent_hand_service'
def v(*p):return A.Vector(*p)
def load(name='placement.json'):
    d=json.loads((O/name).read_text(encoding='utf-8'));scene={}
    for it in d['items']:
        s=Part.read(str(R/it['part']/(it.get('file',Path(it['part']).name)+'.step')))
        for op in reversed(it['ops']):
            if 'rotate' in op:
                for axis,ang in zip([v(1,0,0),v(0,1,0),v(0,0,1)],op['rotate']):s.rotate(v(0,0,0),axis,ang)
            if 'translate' in op:s.translate(v(*op['translate']))
        scene[it['label']]=s
    return d,scene
def common(s,t):
    if not s.BoundBox.intersect(t.BoundBox):return 0
    aa=[p for p in s.Solids if p.BoundBox.intersect(t.BoundBox)]
    bb=[p for p in t.Solids if p.BoundBox.intersect(s.BoundBox)]
    if not aa or not bb:return 0
    return Part.makeCompound(aa).common(Part.makeCompound(bb)).Volume
def collisions(sh,scene,exclude=()):
    out=[]
    for n,t in scene.items():
        if n in ['lid_keepout'] or n in exclude:continue
        vol=common(sh,t)
        if vol>.1:out.append(dict(part=n,mm3=round(vol,4)))
    return out

def corner_fixtures(scene):
    """Actual independent MAIN/Sony supports, or historical carrier labels."""
    return [n for n in scene if n in ['main_lower_carrier','sony_upper_carrier','main_offset_corner','main_mount_plate','sony_mount_plate'] or n.startswith(('main_column_','sony_corner_'))]

def sony_corner_for_foot(i):return 'sony_mount_plate'


def mesh_volume(mesh):
    """Double-precision signed volume about a local origin.

    FreeCAD Mesh.Volume loses precision for small supports near world XY200.
    Topology vertices and fsum avoid cancellation of large world coordinates.
    """
    import math
    points,faces=mesh.Topology
    b=mesh.BoundBox;origin=((b.XMin+b.XMax)/2,(b.YMin+b.YMax)/2,(b.ZMin+b.ZMax)/2)
    local=[(p.x-origin[0],p.y-origin[1],p.z-origin[2]) for p in points]
    def term(face):
        a,b,c=[local[i] for i in face]
        return (a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
    return abs(math.fsum(term(face) for face in faces))
