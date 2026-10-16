# Assumptions (前提条件) — study

_Everything on this page is an **input**. A topology-optimisation result is a picture of its assumptions: change any line below and a different shape is equally optimal. The shape is not the result — the shape together with this page is._

child_core_frame: current interface setup review, not a finished part

**Units.** mm / N / MPa (lengths mm, forces N, stresses MPa)

## 1. What it has to survive

Every load case is a use case someone chose. They are not measured service loads unless a case says so.

| Case | Held at | Loaded at | Force (N) | \|F\| N |
|---|---|---|---|---|
| **L1** | lug_boss_R (xyz), lug_boss_L (xyz) | pocket_bot | (0, 0, -77) | 77.00 |
|  |  | guard_boss_R | (0, 0, -37) | 37.00 |
|  |  | guard_boss_L | (0, 0, -37) | 37.00 |
|  |  | latch_lo | (0, 0, -18) | 18.00 |
|  |  | latch_hi | (0, 0, -18) | 18.00 |
|  |  | td04a_hp1 | (0, 0, -9.4) | 9.40 |
| **L2s** | pocket_bot (xyz), pocket_top (xyz) | back_wall | (200, 0, 0) | 200.00 |
|  |  | lug_boss_R | (50, 0, 0) | 50.00 |
|  |  | lug_boss_L | (50, 0, 0) | 50.00 |
| **L2h** | pocket_bot (xyz), pocket_top (xyz) | knuckles | (300, 0, 0) | 300.00 |
| **L2r** | pocket_bot (xyz), pocket_top (xyz) | back_wall | (0, 200, 0) | 200.00 |
|  |  | grip_bar | (0, 100, 0) | 100.00 |
| **L3** | pocket_bot (xyz), band_mid (xyz), pocket_top (xyz) | latch_lo | (0, 300, 0) | 300.00 |
|  |  | latch_hi | (0, 300, 0) | 300.00 |
|  |  | knuckles | (0, 300, 0) | 300.00 |
| **L5** | pocket_bot (xyz), pocket_top (xyz) | guard_boss_R | (0, 0, 300) | 300.00 |
|  |  | guard_boss_L | (0, 0, 300) | 300.00 |
| **L6** | pocket_bot (xyz), pocket_top (xyz) | grip_underside | (0, 0, 200) | 200.00 |
| **L7** | pocket_bot (xyz), pocket_top (xyz) | light_hp | (0, 0, -9) | 9.00 |
|  |  | light_hp_upper | (8.1, 0, 0) | 8.10 |
|  |  | light_hp_lower | (-8.1, 0, 0) | 8.10 |

**L1** — hoist 3g: lugs fixed, container + guard + gate weights down

**L2s** — transport side hit 300 N (+X on back wall and lugs), container reacts

**L2h** — transport landing on the hinge side (300 N +X through the knuckles), container reacts

**L2r** — transport rear hit 300 N on the back wall (+Y), container reacts

**L3** — clamp preload: knob bolts pull the latch bosses and the gate pulls the knuckles (+Y), tube reacts on the bands

**L5** — landing 600 N up through the guard bosses, container reacts

**L6** — grip lift +200 N: equivalent handling test with vessel restrained; provisional 6kg x 3g rounded up

**L7** — vertical light 3g: provisional 0.3kg, 9N weight plus 324Nmm offset moment

Cases that must be present for the study to be considered complete: `L1`, `L2s`, `L2h`, `L2r`, `L3`, `L5`, `L6`, `L7`.

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

**Does it fit?** The design space measures 153 × 129 × 237 mm; the machine takes 250 × 250 × 250 mm. With Z up: **fits**.

## 5. How much of the shape was decided in advance

| | |
|---|---|
| Design-space bounding box | 153 × 129 × 237 mm |
| Voxel size | 3.0 mm, grid 69×76×108 |
| Volume fraction target | 0.1 of the free region |
| Filter radius | 9.0 mm |
| Symmetry imposed | none |
| Preserve (always kept) | 194130.0 mm³ |
| Obstacle (never filled) | 3847041.0 mm³ |
| Free for the optimiser | 2171529.0 mm³ |
| Share of the domain the optimiser may decide | **53 %** |
| Share of the expected final part that is preserve | **47 %** |


**Fixed by the CAD model, not by the optimisation.** These act on preserve, so their positions are inputs:

| | Region | Position (mm) | Volume mm³ |
|---|---|---|---|
| support | `lug_boss_R` | (65.1, -10.9, 211.5) | 4374.0 |
| support | `lug_boss_L` | (-65, -10.8, 211.5) | 4293.0 |
| load | `pocket_bot` | (0.6, -37.7, -10.1) | 17307.0 |
| load | `guard_boss_R` | (56.6, -32.5, -3.3) | 5535.0 |
| load | `guard_boss_L` | (-56.4, -32.5, -3.3) | 5508.0 |
| load | `latch_lo` | (64.6, -9, 39) | 6480.0 |
| load | `latch_hi` | (64.6, -9, 171) | 6480.0 |
| load | `td04a_hp1` | (0.5, -85.3, 216) | 17199.0 |
| support | `pocket_bot` | (0.6, -37.7, -10.1) | 17307.0 |
| support | `pocket_top` | (0.6, -39, 210.3) | 20763.0 |
| load | `back_wall` | (-3.7, -93.9, 65.2) | 12339.0 |
| load | `lug_boss_R` | (65.1, -10.9, 211.5) | 4374.0 |
| load | `lug_boss_L` | (-65, -10.8, 211.5) | 4293.0 |
| load | `knuckles` | (-72.2, 10.4, 100.5) | 29808.0 |
| load | `grip_bar` | (0.1, -95.4, 157.5) | 13608.0 |
| support | `band_mid` | (0.6, -41.7, 100.5) | 19980.0 |
| load | `grip_underside` | (0.1, -95.4, 147) | 3024.0 |
| load | `light_hp` | (42.1, -75, 100.5) | 14688.0 |
| load | `light_hp_upper` | (42.1, -75, 120) | 3456.0 |
| load | `light_hp_lower` | (42.1, -75, 81) | 3456.0 |

Geometry read from:

- **preserve** `interfaces` → `{'stl': 'inputs/preserve.stl', 'attach': ['join_free_space']}`
- **design_space** → `inputs/design_space.stl`
- **obstacle** `keep_out` → `inputs/obstacle.stl`
- **obstacle** `pressure_vessel` → `../scene/pressure_vessel.stl`
- **obstacle** `light_vertical` → `../scene/light_vertical.stl`
- **obstacle** `hand_clearance` → `../scene/hand_clearance.stl`
- **obstacle** `cables` → `../scene/cables.stl`

## 6. What this study does *not* establish

- **The material card is not measured.** Every stiffness and strength in section 3 is a literature/handbook value for PETG, not a coupon test of this filament on this machine at these settings. Use the results to compare options (build direction, layout, load case), not as absolute strength.
- **The safety factor used (3.0) is below the 4.0 this material card calls for** while it is unmeasured. Results are reported against 3.0; read them with that in mind.
- **47 % of the expected final part is preserve** -- drawn in CAD, not chosen by the optimiser.
- **Where the part is held is an input, not a result.** The 5 support footprint(s) sit on preserve at positions the CAD model chose; the optimiser decided how to reach them, not where they go.
- The free region is only 2.0 voxels thick at its thinnest, so in that region the topology follows the outline rather than the optimisation.
- Nothing here has been tested physically. No printed specimen, no static load test, no comparison of a measured stiffness against the predicted one.
