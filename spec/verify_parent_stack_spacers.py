"""Verify runner membership, unmodified columns and eight severable necks."""
import FreeCAD as A, Part, Mesh
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';P=R/'parts/common/interior/printed/stack_spacers'
import sys
sys.path.insert(0,str(R/'scad/lib'));import parent_gnss as G
d=json.loads((O/'placement.json').read_text(encoding='utf-8'));members=json.loads((P/'set_members.json').read_text(encoding='utf-8'))['members']
actual={it['label']:(it['part'],it['file']) for it in d['items'] if it.get('print_set')=='parent_stack_spacer_set'}
assert actual=={it['label']:(it['part'],it['file']) for it in members}
assert len(members)==12 and all(it['print'] is False for it in d['items'] if it['label'] in actual)
cfg=json.loads((O/'print_config.json').read_text(encoding='utf-8'));assert sum(it['quantity'] for it in cfg['extra_parts'] if it['file']=='parent_stack_spacer_set')==1
s=Part.read(str(P/'parent_stack_spacer_set.step'));severed=s.copy();rows=[]
for it in members:
 src=R/it['part']/(it['file']+'.step');assert hashlib.sha256(src.read_bytes()).hexdigest()==it['source_step_sha256']
 piece=Part.read(str(src))
 for axis,angle in zip([A.Vector(1,0,0),A.Vector(0,1,0),A.Vector(0,0,1)],it.get('rotations_deg',[0,0,0])):piece.rotate(A.Vector(),axis,angle)
 piece.translate(A.Vector(*it['translation_mm']))
 missing=piece.cut(s).Volume
 x,y=it['neck_xy_mm'];width=it['neck_width_mm']-.1
 neck=Part.makeBox(width,.3,.3,A.Vector(x-width/2,y-.15,.05));overlap=s.common(neck).Volume
 # Across the entire neck, away from both part and runner, create a real gap.
 severed=severed.cut(Part.makeBox(2,.4,1.2,A.Vector(x-1,y-.2,-.1)))
 rows.append(dict(label=it['label'],missing_member_mm3=missing,neck_probe_mm3=overlap,pass_=missing<.001 and abs(overlap-width*.09)<.0001))
assert severed.isValid() and len(severed.Solids)==13,('Twelve spacers + discarded runner',len(severed.Solids))
for it in members:
 p=Part.read(str(R/it['part']/(it['file']+'.step')))
 for axis,angle in zip([A.Vector(1,0,0),A.Vector(0,1,0),A.Vector(0,0,1)],it.get('rotations_deg',[0,0,0])):p.rotate(A.Vector(),axis,angle)
 p.translate(A.Vector(*it['translation_mm']))
 assert any(p.cut(q).Volume<.001 for q in severed.Solids)
floor=Part.read(str(R/'parts/parent/interior/printed/parent_hand_service/floor_plate.step'))
boss_top=json.loads((R/'parts/parent/exterior/cots/bcas212310g/dimensions.json').read_text(encoding='utf-8'))['boss_top_z_mm']
for i,(x,y) in enumerate(sum([G.UNIVERSAL_FRAME_FOOT_XY,G.RACK_FOOT_XY,G.MAIN_CARRIER_FOOT_XY,G.SONY_CARRIER_FOOT_XY],[])):
 z=G.FLOOR_GRID_BOTTOM_Z+.2;h=16-z
 annulus=Part.makeCylinder(2.4,h,A.Vector(x,y,z)).cut(Part.makeCylinder(1.9,h,A.Vector(x,y,z)))
 missing=annulus.cut(floor).Volume
 # A necessary case-boss socket can trim the bottom corner of a tab. Require
 # three continuous paths to the grid underside and all four above the bosses;
 # a tab supported only by a raised shelf cannot pass these checks.
 paths=[Part.makeCylinder(.1,h,A.Vector(x+dx,y+dy,z)) for dx,dy in [(2.1,0),(-2.1,0),(0,2.1),(0,-2.1)]]
 gaps=[q.cut(floor).Volume for q in paths]
 upper=[Part.makeCylinder(.1,16-boss_top,A.Vector(x+dx,y+dy,boss_top)).cut(floor).Volume for dx,dy in [(2.1,0),(-2.1,0),(0,2.1),(0,-2.1)]]
 rows.append(dict(label='floor_nut_continuous_support_'+str(i),outer_ring_case_relief_mm3=missing,missing_vertical_path_mm3=gaps,missing_above_boss_mm3=upper,pass_=sum(q<.001 for q in gaps)>=3 and max(upper)<.001))
out=dict(status='PASS' if all(q['pass_'] for q in rows) else 'FAIL',checks=rows,connected_before=len(s.Solids),separate_after=len(severed.Solids),notes=['1.2 x 0.4 mm side necks, nominal two 0.2 mm layers; actual printed break force unmeasured.','Cut flush at the side; no sacrificial connection on bearing/key/bore faces.','MAIN/PWR/TX/battery/antenna integral spacers are already printable supports; no purchased hex spacer used.'])
(O/'stack_spacer_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(out['status']);assert out['status']=='PASS'
