# Assumptions (前提条件) — child_jaw_gate_v1_study

_Everything on this page is an **input**. A topology-optimisation result is a picture of its assumptions: change any line below and a different shape is equally optimal. The shape is not the result — the shape together with this page is._

child_jaw_gate v1: lightweight the movable jaw of the AquaBeacon child unit by topology optimisation, keeping every functional interface of the current part (308.3 cm3).

**Units.** mm / N / MPa (lengths mm, forces N, stresses MPa)

## 1. What it has to survive

Every load case is a use case someone chose. They are not measured service loads unless a case says so.

| Case | Held at | Loaded at | Force (N) | \|F\| N |
|---|---|---|---|---|
| **L1** | knuckles (xyz), latch_lo (xyz), latch_hi (xyz) | hp4 | (0, 0, -18) | 18.00 |
|  |  | hp5 | (0, 0, -17) | 17.00 |
| **L2f** | pocket_bot (xyz), band_mid (xyz), pocket_top (xyz) | hp4 | (0, -150, 0) | 150.00 |
|  |  | hp5 | (0, -150, 0) | 150.00 |
| **L2s** | pocket_bot (xyz), band_mid (xyz), pocket_top (xyz) | latch_lo | (-150, 0, 0) | 150.00 |
|  |  | latch_hi | (-150, 0, 0) | 150.00 |
| **L3** | pocket_bot (xyz), band_mid (xyz), pocket_top (xyz) | latch_lo | (0, -300, 0) | 300.00 |
|  |  | latch_hi | (0, -300, 0) | 300.00 |
|  |  | knuckles | (0, -300, 0) | 300.00 |
| **L4** | pocket_bot (xyz), band_mid (xyz), pocket_top (xyz) | hp4 | (0, -400, 0) | 400.00 |
|  |  | hp5 | (0, 100, 0) | 100.00 |

**L1** — hoist 3g: the gate hangs on the hinge pin and the two knob bolts; bridge + cameras (1.2 kg x 3 g = 35 N) pull down on HP4/HP5

**L2f** — transport frontal 300 N (-Y) through the cam bridge into HP4/HP5, the container reacts on the three bands

**L2s** — transport side 300 N (-X on the latch edge), the container reacts on the three bands

**L3** — clamp preload: the two M5 knob bolts pull the latch bosses -Y (300 N each) and the hinge pin pulls the knuckles -Y, the tube + EVA react on the three bands

**L4** — frontal collision 300 N on the top of the bridge column (z 195): statics on the HP4/HP5 bolt pair (z 170 / 100) gives -400 N on HP4 and +100 N pull-out on HP5, the container reacts on the three bands

Cases that must be present for the study to be considered complete: `L1`, `L2f`, `L2s`, `L3`, `L4`.

## 2. What counts as a pass

| Requirement | Value |
|---|---|
| Safety factor (p99.5 of elements) | ≥ 3.0 |
| Maximum deflection | ≤ 1.0 mm |
| Safety factor this material card calls for | ≥ 4.0 |


## 3. What it is made of

| | |
|---|---|
| Material | PETG |
| Model | `orthotropic_equivalent_solid` |
| Card | `petg_generic_fff_orthotropic_v1_x0.75E_x0.75S` (conservative_literature_based_default) |
| Measured on this printer | **no** |
| Source | docs/FFF_PLA_PETG_orthotropic_material_reference.md section 6 |
| Walls / infill used for derating | 4 / 0.25 |
| Max service temperature | 70 °C |

Stiffness (MPa): Ex 1575, Ey 1312.5, Ez 862.5, Gxy 525, Gyz 315, Gzx 315

Strength (MPa): Xt 31.5, Xc 37.5, Yt 24.75, Yc 31.5, Zt 18.75, Zc 26.25, Sxy 15, Syz 10.5, Szx 10.5

> Tough, good layer adhesion, low warp, water resistant. The default for AquaBeacon wet-side parts. Softer than PLA, so deflection governs more often than strength.

## 4. What has to make it

| | |
|---|---|
| Machine | Bambu Lab X1-Carbon |
| Usable build volume | 250 × 250 × 250 mm |
| Nozzle / smallest wall | 0.4 mm / 0.8 mm |
| Printer chosen or assumed | built-in |
| Build axis (up on the plate) | **Z** |
| Raster axis (in-plane) | X |

**Does it fit?** The design space measures 153 × 75 × 234 mm; the machine takes 250 × 250 × 250 mm. With Z up: **fits**.

## 5. How much of the shape was decided in advance

| | |
|---|---|
| Design-space bounding box | 153 × 75 × 234 mm |
| Voxel size | 3.0 mm, grid 57×33×85 |
| Volume fraction target | 0.052 of the free region |
| Filter radius | 6.0 mm |
| Symmetry imposed | none |
| Preserve (always kept) | 133029.0 mm³ |
| Obstacle (never filled) | 1747629.0 mm³ |
| Free for the optimiser | 1234467.0 mm³ |
| Share of the domain the optimiser may decide | **46 %** |
| Share of the expected final part that is preserve | **67 %** |


**Fixed by the CAD model, not by the optimisation.** These act on preserve, so their positions are inputs:

| | Region | Position (mm) | Volume mm³ |
|---|---|---|---|
| support | `knuckles` | (-71.6, 9.8, 100.4) | 19197.0 |
| support | `latch_lo` | (65.5, 7.5, 40) | 5400.0 |
| support | `latch_hi` | (65.5, 7.5, 169) | 5400.0 |
| load | `hp4` | (-0.5, 71.1, 170.5) | 18360.0 |
| load | `hp5` | (-0.9, 70.1, 100) | 19818.0 |
| support | `pocket_bot` | (-0.9, 40.4, -9.2) | 13743.0 |
| support | `band_mid` | (-1, 39.2, 100) | 20412.0 |
| support | `pocket_top` | (-1.3, 39.3, 207) | 16389.0 |
| load | `latch_lo` | (65.5, 7.5, 40) | 5400.0 |
| load | `latch_hi` | (65.5, 7.5, 169) | 5400.0 |
| load | `knuckles` | (-71.6, 9.8, 100.4) | 19197.0 |

Geometry read from:

- **preserve** `interfaces` → `02_setup/child_jaw_gate_v1_preserve.stl`
- **design_space** → `02_setup/child_jaw_gate_v1_design_space.stl`
- **obstacle** `keep_out` → `02_setup/child_jaw_gate_v1_obstacle.stl`

## 6. What this study does *not* establish

- **The material card is not measured.** Every stiffness and strength in section 3 is a literature/handbook value for PETG, not a coupon test of this filament on this machine at these settings. Use the results to compare options (build direction, layout, load case), not as absolute strength.
- **The safety factor used (3.0) is below the 4.0 this material card calls for** while it is unmeasured. Results are reported against 3.0; read them with that in mind.
- **67 % of the expected final part is preserve** -- drawn in CAD, not chosen by the optimiser.
- **Where the part is held is an input, not a result.** The 6 support footprint(s) sit on preserve at positions the CAD model chose; the optimiser decided how to reach them, not where they go.
- The free region is only 2.0 voxels thick at its thinnest, so in that region the topology follows the outline rather than the optimisation.
- Nothing here has been tested physically. No printed specimen, no static load test, no comparison of a measured stiffness against the predicted one.
