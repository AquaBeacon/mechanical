from pathlib import Path
import trimesh,json
r=Path.cwd();out=r/'print_jobs/parent_spar_bolted'
for name,path,flip in [
 ('parent_deck','parts/parent/exterior/printed/parent_deck/parent_deck.stl',True),
 ('dji_osmo_action6_mount','parts/child/exterior/printed/dji_osmo_action6_mount/dji_osmo_action6_mount.stl',False)]:
 m=trimesh.load(r/path,force='mesh')
 if flip:m.apply_transform(trimesh.transformations.rotation_matrix(3.141592653589793,[1,0,0]))
 m.apply_translation([0,0,-m.bounds[0,2]])
 m.export(out/(name+'.stl'))
 print(name,m.extents,m.is_watertight)
