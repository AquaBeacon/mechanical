# Assumptions (前提条件) — child_core_frame_v5_study

_Everything on this page is an **input**. A topology-optimisation result is a picture of its assumptions: change any line below and a different shape is equally optimal. The shape is not the result — the shape together with this page is._

child_core_frame v5: lightweight the aft core frame of the AquaBeacon child unit by topology optimisation, keeping every functional interface of v4 (650 cm3).

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

**L1** — hoist 3g: lugs fixed, container + guard + gate weights down

**L2s** — transport side hit 300 N (+X on back wall and lugs), container reacts

**L2h** — transport landing on the hinge side (300 N +X through the knuckles), container reacts

**L2r** — transport rear hit 300 N on the back wall (+Y), container reacts

**L3** — clamp preload: knob bolts pull the latch bosses and the gate pulls the knuckles (+Y), tube reacts on the bands

**L5** — landing 600 N up through the guard bosses, container reacts

Cases that must be present for the study to be considered complete: `L1`, `L2s`, `L2h`, `L2r`, `L3`, `L5`.

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

**Does it fit?** The design space measures 153 × 129 × 234 mm; the machine takes 250 × 250 × 250 mm. With Z up: **fits**.

## 5. How much of the shape was decided in advance

| | |
|---|---|
| Design-space bounding box | 153 × 129 × 234 mm |
| Voxel size | 3.0 mm, grid 66×63×86 |
| Volume fraction target | 0.1 of the free region |
| Filter radius | 6.0 mm |
| Symmetry imposed | none |
| Preserve (always kept) | 186138.0 mm³ |
| Obstacle (never filled) | 3105594.0 mm³ |
| Free for the optimiser | 2456460.0 mm³ |
| Share of the domain the optimiser may decide | **61 %** |
| Share of the expected final part that is preserve | **43 %** |


**Fixed by the CAD model, not by the optimisation.** These act on preserve, so their positions are inputs:

| | Region | Position (mm) | Volume mm³ |
|---|---|---|---|
| support | `lug_boss_R` | (65.3, -10.9, 210.8) | 3402.0 |
| support | `lug_boss_L` | (-65.1, -10.8, 210.8) | 3348.0 |
| load | `pocket_bot` | (0.6, -37.8, -9.1) | 17658.0 |
| load | `guard_boss_R` | (56.6, -32.4, -2.3) | 5589.0 |
| load | `guard_boss_L` | (-56.4, -32.5, -2.3) | 5535.0 |
| load | `latch_lo` | (64.6, -9, 40) | 6480.0 |
| load | `latch_hi` | (64.6, -9, 169) | 6480.0 |
| support | `pocket_bot` | (0.6, -37.8, -9.1) | 17658.0 |
| support | `pocket_top` | (0.7, -38.7, 207.7) | 19710.0 |
| load | `back_wall` | (-3.6, -93.8, 64) | 12960.0 |
| load | `lug_boss_R` | (65.3, -10.9, 210.8) | 3402.0 |
| load | `lug_boss_L` | (-65.1, -10.8, 210.8) | 3348.0 |
| load | `knuckles` | (-72.2, 10.4, 100) | 29808.0 |
| load | `grip_bar` | (0.1, -95.4, 157) | 12096.0 |
| support | `band_mid` | (0.6, -41.7, 100) | 23976.0 |

Geometry read from:

- **preserve** `interfaces` → `02_setup/child_core_frame_v5_preserve.stl`
- **design_space** → `02_setup/child_core_frame_v5_design_space.stl`
- **obstacle** `keep_out` → `02_setup/child_core_frame_v5_obstacle.stl`

## 6. What this study does *not* establish

- **The material card is not measured.** Every stiffness and strength in section 3 is a literature/handbook value for PETG, not a coupon test of this filament on this machine at these settings. Use the results to compare options (build direction, layout, load case), not as absolute strength.
- **The safety factor used (3.0) is below the 4.0 this material card calls for** while it is unmeasured. Results are reported against 3.0; read them with that in mind.
- **43 % of the expected final part is preserve** -- drawn in CAD, not chosen by the optimiser.
- **Where the part is held is an input, not a result.** The 5 support footprint(s) sit on preserve at positions the CAD model chose; the optimiser decided how to reach them, not where they go.
- The free region is only 2.0 voxels thick at its thinnest, so in that region the topology follows the outline rather than the optimisation.
- Nothing here has been tested physically. No printed specimen, no static load test, no comparison of a measured stiffness against the predicted one.
