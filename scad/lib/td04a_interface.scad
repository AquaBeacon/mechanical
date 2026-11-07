// TD04A mechanical interface. User confirmation 2026-10-25, not image scaling.
td04a_mount_pitch=12; // user approximate value; verify physical pitch before printing
td04a_cable_clearance=60; // from M4 hole baseline towards exterior, not from cable boot
td04a_mount_nominal=4;
td04a_mount_clearance=4.5;
// Unmeasured ear thickness is NOT an OEM specification.
td04a_ear_t_provisional=3;

// User correction 2026-10-25: baseline X lies parallel to broad plane XY;
// fixing plane XZ is perpendicular to broad plane XY. Screw axis is Y.
td04a_hole_baseline=[1,0,0];
td04a_fixing_plane_normal=[0,1,0];
td04a_broad_plane_normal=[0,0,1];

// Broad PLANE normal above is unsigned; requested face direction is -Z for parent, +Z for child.
