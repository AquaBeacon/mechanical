import FreeCAD,Part
s=Part.read('C:/Program Files/KiCad/10.0/share/kicad/3dmodels/Module.3dshapes/RaspberryPi_Pico_H.step')
for sol in s.Solids:
 b=sol.BoundBox
 if sol.Volume>45: print(round(sol.Volume,1),b)
