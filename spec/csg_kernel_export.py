"""Evaluate elementary CSG directly in OCC, avoiding importCSG boolean failures.
Run in FreeCAD Python. Input comes from OpenSCAD, never evaluates arbitrary Python.
Only the eight primitive/boolean operations actually used by these parts supported.
"""
import os,re,ast,json,math
from pathlib import Path
import FreeCAD as A,Part,Mesh,MeshPart
src=Path(os.environ['CSG_IN']);dest=Path(os.environ['STEP_OUT']);ref=Path(os.environ['STL_REF'])
text=src.read_text();pos=0
def space():
 global pos
 while pos<len(text) and text[pos].isspace():pos+=1
def parse():
 global pos
 space();m=re.match(r'(\w+)\s*\(',text[pos:]);assert m,text[pos:pos+80]
 name=m[1];pos+=m.end();start=pos;depth=1
 while depth:
  ch=text[pos];pos+=1
  if ch=='(':depth+=1
  elif ch==')':depth-=1
 args=text[start:pos-1];space();children=[]
 if text[pos]==';':pos+=1
 else:
  assert text[pos]=='{';pos+=1;space()
  while text[pos]!='}':children.append(parse());space()
  pos+=1
 return name,args,children
def value(s):return ast.literal_eval(s.replace('true','True').replace('false','False').replace('undef','None'))
def kwargs(s):
 result={};start=0;depth=0;pieces=[]
 for i,ch in enumerate(s):
  if ch in '[(':depth+=1
  elif ch in '])':depth-=1
  elif ch==',' and depth==0:pieces.append(s[start:i]);start=i+1
 pieces.append(s[start:])
 for p in pieces:
  if not p.strip():continue
  k,v=p.split('=',1);result[k.strip()]=value(v.strip())
 return result
def fuse(shapes):
 shapes=[s for s in shapes if s is not None and not s.isNull()]
 if not shapes:return None
 s=shapes[0]
 for t in shapes[1:]:s=s.fuse(t)
 return s
cache={}
def cutters(node):
 if node[0] in ['group','union']:
  for c in node[2]:yield from cutters(c)
 else:yield node
def evaluate(node):
 name,args,children=node;key=repr(node)
 if key in cache:return cache[key].copy() if cache[key] is not None else None
 if name=='cube':
  k=kwargs(args);sz=k['size'];s=Part.makeBox(*sz)
  if k.get('center'):s.translate(A.Vector(*[-v/2 for v in sz]))
 elif name=='cylinder':
  k=kwargs(args);h=k['h'];r1=k['r1'];r2=k['r2'];fn=k.get('$fn',0)
  if fn and fn<16 and abs(r1-r2)<1e-9:
   pts=[A.Vector(r1*math.cos(2*math.pi*i/fn),r1*math.sin(2*math.pi*i/fn),0) for i in range(int(fn))]
   pts.append(pts[0]);s=Part.Face(Part.makePolygon(pts)).extrude(A.Vector(0,0,h))
  else:s=Part.makeCylinder(r1,h) if abs(r1-r2)<1e-9 else Part.makeCone(r1,r2,h)
  if k.get('center'):s.translate(A.Vector(0,0,-h/2))
 elif name=='sphere':s=Part.makeSphere(kwargs(args)['r'])
 elif name=='multmatrix':
  s=fuse([evaluate(c) for c in children])
  if s is not None:
   rows=value(args);s.transformShape(A.Matrix(*[v for row in rows for v in row]),True)
 elif name in ['group','union']:s=fuse([evaluate(c) for c in children])
 elif name=='difference':
  s=evaluate(children[0]) if children else None
  if s is not None:
   for c in [leaf for child in children[1:] for leaf in cutters(child)]:
    t=evaluate(c)
    if t is not None and not t.isNull():
     before=s.Volume
     if os.environ.get('CSG_TRACE') and t.Volume>1.5e6 and before>2e6:print('BORE DEBUG',s.isValid(),s.isInside(A.Vector(0,10,100),1e-6,True),t.isInside(A.Vector(0,10,100),1e-6,True),s.common(t).Volume,s.BoundBox,t.BoundBox,flush=True)
     s=s.cut(t)
     if os.environ.get('CSG_TRACE') and before>1e6:print('CUT',before,t.Volume,t.isValid(),s.Volume,repr(c)[:180],flush=True)
 elif name=='intersection':
  s=evaluate(children[0]) if children else None
  for c in children[1:]:
   t=evaluate(c)
   if s is None or t is None:s=None;break
   s=s.common(t)
   if s.isNull():s=None;break
 else:raise ValueError('Unsupported CSG: '+name)
 cache[key]=s.copy() if s is not None else None
 return s
nodes=[];space()
while pos<len(text):nodes.append(parse());space()
shape=fuse([evaluate(n) for n in nodes]).removeSplitter()
m=Mesh.Mesh(str(ref));b=shape.BoundBox;bm=m.BoundBox
db=max(abs(x-y) for x,y in zip([b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],[bm.XMin,bm.YMin,bm.ZMin,bm.XMax,bm.YMax,bm.ZMax]))
dv=abs(shape.Volume-m.Volume)/abs(m.Volume)
report={'valid':shape.isValid(),'solids':len(shape.Solids),'volume_mm3':shape.Volume,'stl_volume_mm3':m.Volume,'relative_volume_difference':dv,'bbox_difference_mm':db}
print(json.dumps(report),flush=True)
dest.with_suffix('.check.json').write_text(json.dumps(report,indent=2))
if not report['valid'] or len(shape.Solids)!=1 or db>.5 or dv>.02:raise RuntimeError('Refusing an unverified STEP')
shape.exportStep(str(dest))
mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.12,AngularDeflection=.15,Relative=False)
mesh.write(str(dest.with_name(dest.stem+'_occ.stl')))
