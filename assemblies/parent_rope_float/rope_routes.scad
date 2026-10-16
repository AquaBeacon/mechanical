// Flexible rope ROUTE ENVELOPE, not a rigid member or printable part.
$fn=20; rope_d=4;
module segment(a,b){v=b-a;L=norm(v);translate(a)rotate(a=acos(v[2]/L),v=[-v[1],v[0],0])cylinder(d=rope_d,h=L);}
module route(p){for(i=[0:len(p)-2])segment(p[i],p[i+1]);for(q=p)translate(q)sphere(d=rope_d);}
route([[-90, 108, -35], [-118, 108, -35], [-150, 170, -20], [-178, 165, 0], [-178, 150, 0], [-178, -150, 0], [-178, -165, 0], [-150, -170, -20], [-118, -108, -35], [-90, -108, -35]]);
route([[90, 108, -35], [118, 108, -35], [150, 170, -20], [178, 165, 0], [178, 150, 0], [178, -150, 0], [178, -165, 0], [150, -170, -20], [118, -108, -35], [90, -108, -35]]);
