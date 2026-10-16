// =====================================================================
// child_harness.scad - child-unit internal wiring harnesses (keep-out bodies)
//
// Not a printed part: models every board-to-board JST-XH cable, the battery
// XT30 link and the LED / external-sensor pigtails as 3D volumes in WORLD
// coordinates of assemblies/child_interior (X=width, Y=stack, +Y=LCD side,
// Z=tube axis; deck underside y=-10, deck top y=-6). Used to (a) render the
// as-built harness routing for review and (b) run the same clearance check
// (scad/lib/check_asm_contacts.py) used for real parts, so cable routing is
// verified against every neighbouring part before the boards are populated.
//
// Each harness = a polyline of waypoints -> cylinder per segment + sphere at
// every interior joint (both faceted, $fn=24 - acceptable for cabling, see
// the .md). XH plug housings are cubes sized from pin count and pitch, seated
// on top of the header (the board STL already includes the 7.0mm header) and
// centred on the connector's pin row; the wire leaves from the centre of the
// plug's outward face.
//
// One variant per harness, selected by the `variant` string (see variants.txt).
// =====================================================================

$fn = 24;

/* [Variant] */
variant = "xh9_pwr"; // [xh9_pwr,xh6_rx,xh7_lcd,xh3_teth,xh4_temp,xh2_leak,xh4_prs,bat,led]

/* [XH plug geometry] */
xh_header_h = 7.0;   // header height already modelled in the board STL
xh_plug_h   = 7.4;   // mated plug height above the header top
xh_plug_w   = 5.75;  // plug width across the row
xh_pitch    = 2.5;   // XH pin pitch
xh_end_margin = 2.4; // plug overhang beyond the outer pins, along the row

// ---- connector table -------------------------------------------------
// c = [pin1=[x,y,z], n_pins, row_axis("x"/"z"), row_sign(+-1), board_normal_sign(+-1)]
J_PWR1  = [[12,    4.6,  25.5], 9, "x",  1,  1];  // CHILD_MAIN
J_RX1   = [[-8,    4.6,  80  ], 6, "z",  1,  1];  // CHILD_MAIN
J_LCD1  = [[-21,   4.6,  80  ], 7, "z",  1,  1];  // CHILD_MAIN
J_TEMP1 = [[-8,    4.6,  99  ], 4, "z",  1,  1];  // CHILD_MAIN
J_LEAK1 = [[-8,    4.6,  113 ], 2, "z",  1,  1];  // CHILD_MAIN
J_TETH1 = [[-18,   4.6,  107 ], 3, "z",  1,  1];  // CHILD_MAIN
J_PRS1  = [[40,    4.6,  105 ], 4, "z",  1,  1];  // CHILD_MAIN
J_MAIN  = [[15,    5.6,  131 ], 9, "x", -1,  1];  // CHILD_PWR
RX_J2   = [[-31.1,-17.6, 154 ], 6, "z",  1, -1];  // RX (housing on -Y side)

// J_BAT / J_LED: unpopulated XT30PW-M footprint / LED pads on CHILD_PWR - no
// header, pigtail soldered directly to the pads. Centre points only.
J_BAT_C = [21.4, 5.6, 145];    // midpoint of the two solder pads (147.5/142.5)
J_LED_C = [-21.4, 5.6, 146];

function conn_pin1(c)  = c[0];
function conn_n(c)     = c[1];
function conn_axis(c)  = c[2];
function conn_rsign(c) = c[3];
function conn_nsign(c) = c[4];

function xh_center(pin1, n, axis, rsign) =
    axis == "x" ? [pin1[0] + rsign*(n-1)*xh_pitch/2, pin1[1], pin1[2]]
                : [pin1[0], pin1[1], pin1[2] + rsign*(n-1)*xh_pitch/2];

function conn_center(c) = xh_center(conn_pin1(c), conn_n(c), conn_axis(c), conn_rsign(c));

// point where the wire leaves the plug (centre of the face away from the board)
function conn_wire(c) =
    let(ctr = conn_center(c), ns = conn_nsign(c))
    [ctr[0], ctr[1] + ns*(xh_header_h + xh_plug_h), ctr[2]];

// short (2.5mm) stub straight out from the board before the first bend
function conn_stub(c, len=2.5) =
    let(w = conn_wire(c), ns = conn_nsign(c))
    [w[0], w[1] + ns*len, w[2]];

module xh_plug(c) {
    ctr   = conn_center(c);
    n     = conn_n(c);
    axis  = conn_axis(c);
    ns    = conn_nsign(c);
    len_row = xh_pitch*n + xh_end_margin;
    lx = (axis == "x") ? len_row : xh_plug_w;
    lz = (axis == "z") ? len_row : xh_plug_w;
    y0 = ctr[1] + ns*xh_header_h;
    ylo = (ns > 0) ? y0 : y0 - xh_plug_h;
    translate([ctr[0]-lx/2, ylo, ctr[2]-lz/2])
        cube([lx, xh_plug_h, lz]);
}

// ---- generic bare-pad "connector" (XT30 pads / LED pads: no housing) --
module pad_stub(p, dir=[0,1,0], len=2.5) { /* geometry only from the route itself */ }

// ---- polyline renderer --------------------------------------------
// eps: each cylinder is extended slightly past both its endpoints so it
// truly overlaps the joint sphere / the next collinear cylinder instead of
// merely touching it (coincident faces at an exact tangent produce a
// non-manifold STL - "watertight: N open edges" - even though the union is
// a valid solid). Joint spheres are enlarged by the same margin and placed
// at every vertex (not only interior joints) for the same reason; this is a
// mesh-quality fix, not a change to the modelled route (see the .md).
module seg(p0, p1, d, eps=0.03) {
    v = p1 - p0;
    ln = norm(v);
    if (ln > 1e-6) {
        dirn = v / ln;
        p0e = p0 - dirn * eps;
        ax = (abs(v[0]) < 1e-9 && abs(v[1]) < 1e-9) ? [1,0,0] : cross([0,0,1], v);
        ang = acos(v[2]/ln);
        translate(p0e) rotate(a=ang, v=ax) cylinder(d=d, h=ln + 2*eps, $fn=24);
    }
}

module polyline(pts, d) {
    n = len(pts);
    for (i = [0:n-2]) seg(pts[i], pts[i+1], d);
    for (i = [0:n-1]) translate(pts[i]) sphere(d=d*1.02, $fn=24);
}

function seg_len(p0, p1) = norm(p1-p0);
function polyline_len(pts, i=0, acc=0) =
    (i >= len(pts)-1) ? acc : polyline_len(pts, i+1, acc + seg_len(pts[i], pts[i+1]));

// ---- harness definitions -------------------------------------------
// Diameters per the spec's bundle table.
D_XH9 = 5.5; D_XH7 = 5.0; D_XH6 = 4.5; D_XH4 = 3.5; D_XH3 = 3.0; D_XH2 = 2.5;
D_PWR = 5.0; // 2-wire power leads (battery / LED / pigtail)

// 1. xh9_pwr: CHILD_MAIN J_PWR1 <-> CHILD_PWR J_MAIN
XH9_PWR_PTS = [
    conn_wire(J_PWR1),
    [22, 19, 25.5],
    [10, 19, 32],
    [10, 23, 40],     // shifted x8->10 / y23 to clear the MAIN high zone (y<=21.1, x 8..42) and stay under the LCD arch underside (y~23-32)
    [10, 23, 118],
    [7, 22, 125],
    [7, 20, 129],
    conn_wire(J_MAIN),
];
module h_xh9_pwr() {
    xh_plug(J_PWR1);
    xh_plug(J_MAIN);
    polyline(XH9_PWR_PTS, D_XH9);
}

// 2. xh6_rx: CHILD_MAIN J_RX1 <-> RX J2
// NOTE (assembly-order exception): x=-36, y=-15.5 sits inside the -X cable
// rail's trough (child_vtray_cable_rail, base_t slab y -10..-12.4 full width,
// walls y -12.4..-18.9 at the two 4mm side strips). The trough's floor is
// flush with the deck underside (both at y=-10, zero clearance) so a static
// straight-line route from above the deck into the trough necessarily
// crosses the floor. The intended assembly is: lay the harness into the open
// (bottom-facing) trough first, THEN bolt the rail up onto the deck from
// below - the same "assembly order" rationale as --ignore-threads for screw
// pilots. Treated here like the harness<->board-header exception; see
// child_harness.md "要確認" - this is a call the brief's exception list did
// not make explicitly and should be confirmed.
CABLE_RAIL_SIGNAL_X = -36; // rail centreline (channel is open x -40..-32)
XH6_RX_PTS = [
    conn_wire(J_RX1),
    [-8, 19, 86],
    [-24, 17, 92],
    [CABLE_RAIL_SIGNAL_X, 10, 96],
    [CABLE_RAIL_SIGNAL_X, -8, 96],     // through the -X deck slit (x 29..43 mirrored, z 83..109)
    [CABLE_RAIL_SIGNAL_X, -15.5, 100],
    [CABLE_RAIL_SIGNAL_X, -15.5, 123],
    [CABLE_RAIL_SIGNAL_X, -25.5, 131], // below paired clamp and M3 head reserve
    [CABLE_RAIL_SIGNAL_X, -25.5, 148],
    [-33, -28, 156],
    [-31.1, -33, 160],
    conn_wire(RX_J2),
];
module h_xh6_rx() {
    xh_plug(J_RX1);
    xh_plug(RX_J2);
    polyline(XH6_RX_PTS, D_XH6);
}

// 3. xh7_lcd: CHILD_MAIN J_LCD1 -> LCD carrier board (position TBD, stub end)
XH7_LCD_PTS = [
    conn_wire(J_LCD1),
    [-21, 19, 87],
    [-27, 21, 80],
    [-30, 28, 82],
    [-26, 33, 87],
];
module h_xh7_lcd() {
    xh_plug(J_LCD1);
    polyline(XH7_LCD_PTS, D_XH7);
}

// 4. xh3_teth: CHILD_MAIN J_TETH1 -> bottom-cap penetrator (external cable)
// Bottom rib (child_vtray_rib_bot, z 0..6) duct is the real keep-through:
// x -20..20, y -36..-14 (child_vtray_rib.scad duct_w=40/duct_y0=-36/duct_y1=-14).
// Crossing points below are spread across |x|<=16 so a >=1.0mm margin to the
// duct edge holds for every bundle diameter used here (largest Ø5.0/led).
XH3_TETH_PTS = [
    conn_wire(J_TETH1),
    [-18, 19, 109.5],
    [-30, 15, 100],
    [CABLE_RAIL_SIGNAL_X, 10, 96],
    [CABLE_RAIL_SIGNAL_X, -8, 96],
    [CABLE_RAIL_SIGNAL_X, -15.5, 90],
    [CABLE_RAIL_SIGNAL_X, -15.5, 20],
    [-20, -20, 12],
    [-16, -25, 4],
    [-13, -25, -2],
];
module h_xh3_teth() {
    xh_plug(J_TETH1);
    polyline(XH3_TETH_PTS, D_XH3);
}

// 5a. xh4_temp: CHILD_MAIN J_TEMP1, same corridor as teth
XH4_TEMP_PTS = [
    conn_wire(J_TEMP1),
    [-8, 19, 102.75],
    [-20, 16, 99],
    [-30, 12, 96],
    [CABLE_RAIL_SIGNAL_X, 9, 96],
    [CABLE_RAIL_SIGNAL_X, -8, 96],
    [CABLE_RAIL_SIGNAL_X, -15.5, 100], // through existing rail window, world Z90..104
    [CABLE_RAIL_SIGNAL_X, -15.5, 20],
    [-26, -20, 12],
    [-9, -25, 4],
    [-6, -25, -2],
];
module h_xh4_temp() {
    xh_plug(J_TEMP1);
    polyline(XH4_TEMP_PTS, D_XH4);
}

// 5b. xh2_leak: CHILD_MAIN J_LEAK1, same corridor
XH2_LEAK_PTS = [
    conn_wire(J_LEAK1),
    [-8, 19, 114.25],
    [-22, 17, 108],
    [-31, 12, 98],
    [CABLE_RAIL_SIGNAL_X, 9, 96],
    [CABLE_RAIL_SIGNAL_X, -8, 96],
    [CABLE_RAIL_SIGNAL_X, -15.5, 92],
    [CABLE_RAIL_SIGNAL_X, -15.5, 20],
    [-20, -20, 12],
    [-3, -25, 4],
    [0, -25, -2],
];
module h_xh2_leak() {
    xh_plug(J_LEAK1);
    polyline(XH2_LEAK_PTS, D_XH2);
}

// 6. xh4_prs: CHILD_MAIN J_PRS1 -> penetrator (external cable, +X rail channel)
CABLE_RAIL_POWER_X = 36; // rail centreline (channel is open x 32..40)
XH4_PRS_PTS = [
    conn_wire(J_PRS1),
    [40, 19, 108.75],
    [38, 10, 100],
    [CABLE_RAIL_POWER_X, -8, 96],
    [CABLE_RAIL_POWER_X, -15.5, 90],
    [CABLE_RAIL_POWER_X, -15.5, 20],
    [22, -20, 12],
    [10, -25, 4],
    [7, -25, -2],
];
module h_xh4_prs() {
    xh_plug(J_PRS1);
    polyline(XH4_PRS_PTS, D_XH4);
}

// 7. bat: battery lead -> XT30 mated pair -> pigtail to J_BAT, plus charge lead
// Lead stub tips measured from lipo_35x26x110_leads.stl via the placement
// transform (translate[-17.5,-14,131] + rotate[0,90,-90]): power lead tip
// world (13,-27,13), charge lead tip world (-13,-27,13) - NOT (±13,-27,20)
// as the brief's proposal assumed (that point sits inside the modelled 8mm
// lead stub itself).
BAT_LEAD_PTS = [
    [13, -27, 13],
    [13, -27, 17],
    [22, -24, 16],
    [33, -21.5, 16],   // stay below the rail's -Z end (z 20) and its wall bottoms (y -18.9)
    [36, -19.5, 20],   // enter the trough through its open -Z end, not through the wall
    [36, -17.4, 25],
];
XT30_PAIR_X0 = 32.5; XT30_PAIR_X1 = 39.5;
XT30_PAIR_Y0 = -22.4; XT30_PAIR_Y1 = -12.4;
XT30_PAIR_Z0 = 25; XT30_PAIR_Z1 = 55;
BAT_PIGTAIL_PTS = [
    [36, -17.4, 55],
    [36, -15.5, 60],
    [36, -15.5, 123],
    [36, -25.5, 131],
    [36, -25.5, 146],
    [36, -15.5, 151],
    [36, -8, 157],
    [30, 9, 152],
    [24, 9, 146],
    J_BAT_C,
];
CHG_XH4_CTR = [-26, -19, 11.5]; // charge-lead XH4 plug block, z 8..15
CHG_LEAD_PTS = [
    [-13, -27, 13],
    [-13, -27, 17],
    [-24, -22, 15],
    [-26, -19, 10],
    CHG_XH4_CTR,
];
module h_bat() {
    polyline(BAT_LEAD_PTS, D_PWR);
    // XT30 mated pair: 7mm across an 8mm channel (0.5mm/side) - a deliberately
    // snug connector fit, not a routing error; cannot reach 1.0mm to the rail
    // walls without leaving the channel entirely. See child_harness.md.
    translate([XT30_PAIR_X0, XT30_PAIR_Y0, XT30_PAIR_Z0])
        cube([XT30_PAIR_X1-XT30_PAIR_X0, XT30_PAIR_Y1-XT30_PAIR_Y0, XT30_PAIR_Z1-XT30_PAIR_Z0]);
    polyline(BAT_PIGTAIL_PTS, D_PWR);
    polyline(CHG_LEAD_PTS, D_XH4);
    translate([CHG_XH4_CTR[0]-6.2, CHG_XH4_CTR[1]-2.875, 8])
        cube([12.4, 5.75, 7]);
}

// 8. led: CHILD_PWR J_LED pads -> penetrator (external cable, -X channel)
LED_PTS = [
    J_LED_C,
    [-26, 9, 150],
    [-36, 9, 157],
    [CABLE_RAIL_SIGNAL_X, -8, 157],
    [CABLE_RAIL_SIGNAL_X, -15.5, 150],
    [CABLE_RAIL_SIGNAL_X, -25.5, 146],
    [CABLE_RAIL_SIGNAL_X, -25.5, 131],
    [CABLE_RAIL_SIGNAL_X, -15.5, 123],
    [CABLE_RAIL_SIGNAL_X, -15.5, 24],
    [CABLE_RAIL_SIGNAL_X, -20, 18],   // leave the trough through its open -Z end (below the wall bottoms y -18.9)
    [-14, -22, 12],
    [3, -25, 4],
    [6, -25, -2],
];
module h_led() {
    polyline(LED_PTS, D_PWR);
}

// ---- dispatch ---------------------------------------------------------
module render_variant() {
    if (variant == "xh9_pwr") h_xh9_pwr();
    else if (variant == "xh6_rx") h_xh6_rx();
    else if (variant == "xh7_lcd") h_xh7_lcd();
    else if (variant == "xh3_teth") h_xh3_teth();
    else if (variant == "xh4_temp") h_xh4_temp();
    else if (variant == "xh2_leak") h_xh2_leak();
    else if (variant == "xh4_prs") h_xh4_prs();
    else if (variant == "bat") h_bat();
    else if (variant == "led") h_led();
    else assert(false, str("unknown child_harness variant: ", variant));
}

render_variant();

// Lengths (mm) echoed for the .md recommended-cut-length table.
echo(str("child_harness[", variant, "] xh9_pwr_len=", polyline_len(XH9_PWR_PTS)));
echo(str("child_harness[", variant, "] xh6_rx_len=", polyline_len(XH6_RX_PTS)));
echo(str("child_harness[", variant, "] xh7_lcd_len=", polyline_len(XH7_LCD_PTS)));
echo(str("child_harness[", variant, "] xh3_teth_len=", polyline_len(XH3_TETH_PTS)));
echo(str("child_harness[", variant, "] xh4_temp_len=", polyline_len(XH4_TEMP_PTS)));
echo(str("child_harness[", variant, "] xh2_leak_len=", polyline_len(XH2_LEAK_PTS)));
echo(str("child_harness[", variant, "] xh4_prs_len=", polyline_len(XH4_PRS_PTS)));
echo(str("child_harness[", variant, "] bat_lead_len=", polyline_len(BAT_LEAD_PTS)));
echo(str("child_harness[", variant, "] bat_pigtail_len=", polyline_len(BAT_PIGTAIL_PTS)));
echo(str("child_harness[", variant, "] chg_lead_len=", polyline_len(CHG_LEAD_PTS)));
echo(str("child_harness[", variant, "] led_len=", polyline_len(LED_PTS)));
