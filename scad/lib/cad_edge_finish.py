"""Identify geometric corners, excluding periodic seams and tangent joins."""
import math

def sharp_edges(shape):
    result=[]
    adjacency={}
    for face in shape.Faces:
        for edge in face.Edges:adjacency.setdefault(edge.hashCode(),[]).append(face)
    for edge in shape.Edges:
        adjacent=adjacency.get(edge.hashCode(),[])
        if len(adjacent)!=2: continue
        point=edge.valueAt((edge.FirstParameter+edge.LastParameter)/2)
        normals=[]
        for face in adjacent:
            u,v=face.Surface.parameter(point)
            normals.append(face.normalAt(u,v))
        if normals[0].getAngle(normals[1]) > math.radians(1): result.append(edge)
    return result
