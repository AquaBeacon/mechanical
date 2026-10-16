"""Remove empty CSG groups while preserving boolean empty-set semantics.
FreeCAD's importer can fail on OpenSCAD's group(); output from echo/empty modules.
This does not change any primitive dimensions. STEP is still checked against STL.
"""
import re,sys
from pathlib import Path

def clean(text):
    pos=0
    def space():
        nonlocal pos
        while pos<len(text) and text[pos].isspace():pos+=1
    def node():
        nonlocal pos
        space();m=re.match(r'([\w$]+)\s*\(',text[pos:])
        if not m:raise ValueError(text[pos:pos+60])
        name=m[1];start=pos;pos+=m.end();depth=1;quoted=False;escape=False
        while depth:
            ch=text[pos];pos+=1
            if quoted:
                if escape:escape=False
                elif ch=='\\':escape=True
                elif ch=='"':quoted=False
            elif ch=='"':quoted=True
            elif ch=='(':depth+=1
            elif ch==')':depth-=1
        header=text[start:pos];space()
        if text[pos]==';':
            pos+=1
            return None if name in ['group','union','difference','intersection'] else header+';'
        assert text[pos]=='{';pos+=1;children=[];space()
        while text[pos]!='}':children.append(node());space()
        pos+=1
        if name=='difference' and (not children or children[0] is None):return None
        if name=='intersection' and any(c is None for c in children):return None
        children=[c for c in children if c is not None]
        if not children:return None
        if len(children)==1 and name in ['group','union','difference','intersection']:return children[0]
        return header+'{\n'+'\n'.join(children)+'\n}'
    nodes=[];space()
    while pos<len(text):
        n=node()
        if n:nodes.append(n)
        space()
    return '\n'.join(nodes)+'\n'

if __name__=='__main__':
    p=Path(sys.argv[1]);dest=Path(sys.argv[2]);dest.write_text(clean(p.read_text()),encoding='utf-8')
