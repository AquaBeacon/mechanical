# Assumptions (前提条件) — child_cam_bridge_v1_study

_Everything on this page is an **input**. A topology-optimisation result is a picture of its assumptions: change any line below and a different shape is equally optimal. The shape is not the result — the shape together with this page is._

child_cam_bridge v1: lightweight the camera bridge of the AquaBeacon child unit by topology optimisation, keeping every functional interface of the current part (328.1 cm3 / PETG ~407 g).

**Units.** mm / N / MPa (lengths mm, forces N, stresses MPa)

## 1. What it has to survive

Every load case is a use case someone chose. They are not measured service loads unless a case says so.

| Case | Held at | Loaded at | Force (N) | \|F\| N |
|---|---|---|---|---|
| **L1** | hp4_seat (xyz), hp5_seat (xyz) | mount_R | (0, 0, -10.3) | 10.30 |
|  |  | mount_L | (0, 0, -10.3) | 10.30 |
| **L4** | hp4_seat (xyz), hp5_seat (xyz) | fbump_R | (0, -150, 0) | 150.00 |
| **L2s** | hp4_seat (xyz), hp5_seat (xyz) | endp_R | (-150, 0, 0) | 150.00 |
| **L6** | hp4_seat (xyz), hp5_seat (xyz) | mount_R | (0, 0, 100) | 100.00 |

**L1** — operational hoist 3g: HP4/HP5 fixed, camera + case (0.35 kg each) hang off the mount seats, bridge self-weight at 3 g

**L4** — frontal impact 150 N (-Y) on one front-edge bumper, HP4/HP5 react

**L2s** — side impact 150 N (-X) on the starboard end plate through the side bumper, HP4/HP5 react

**L6** — handling: the unit is picked up by one camera, 100 N (+Z) on the starboard cam_mount seat, HP4/HP5 react

Cases that must be present for the study to be considered complete: `L1`, `L4`, `L2s`, `L6`.

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
| Build axis (up on the plate) | **Y** |
| Raster axis (in-plane) | X |

**Does it fit?** The design space measures 240 × 60 × 150 mm; the machine takes 250 × 250 × 250 mm. With Y up: **fits**.

## 5. How much of the shape was decided in advance

| | |
|---|---|
| Design-space bounding box | 240 × 60 × 150 mm |
| Voxel size | 3.0 mm, grid 86×27×55 |
| Volume fraction target | 0.06 of the free region |
| Filter radius | 6.0 mm |
| Symmetry imposed | X |
| Preserve (always kept) | 123984.0 mm³ |
| Obstacle (never filled) | 996516.0 mm³ |
| Free for the optimiser | 1108836.0 mm³ |
| Share of the domain the optimiser may decide | **51 %** |
| Share of the expected final part that is preserve | **65 %** |


**Fixed by the CAD model, not by the optimisation.** These act on preserve, so their positions are inputs:

| | Region | Position (mm) | Volume mm³ |
|---|---|---|---|
| support | `hp4_seat` | (0, 76, 169.4) | 14688.0 |
| support | `hp5_seat` | (0, 76, 100.5) | 14688.0 |
| load | `mount_R` | (75, 97, 49.5) | 13608.0 |
| load | `mount_L` | (-75, 97, 49.5) | 13608.0 |
| load | `fbump_R` | (75, 124, 63) | 19440.0 |
| load | `endp_R` | (117, 97, 63) | 12960.0 |

Geometry read from:

- **preserve** `interfaces` → `02_setup/child_cam_bridge_v1_preserve.stl`
- **design_space** → `02_setup/child_cam_bridge_v1_design_space.stl`
- **obstacle** `keep_out` → `02_setup/child_cam_bridge_v1_obstacle.stl`

## 6. What this study does *not* establish

- **The material card is not measured.** Every stiffness and strength in section 3 is a literature/handbook value for PETG, not a coupon test of this filament on this machine at these settings. Use the results to compare options (build direction, layout, load case), not as absolute strength.
- **The safety factor used (3.0) is below the 4.0 this material card calls for** while it is unmeasured. Results are reported against 3.0; read them with that in mind.
- **65 % of the expected final part is preserve** -- drawn in CAD, not chosen by the optimiser.
- **Where the part is held is an input, not a result.** The 2 support footprint(s) sit on preserve at positions the CAD model chose; the optimiser decided how to reach them, not where they go.
- The free region is only 2.0 voxels thick at its thinnest, so in that region the topology follows the outline rather than the optimisation.
- Nothing here has been tested physically. No printed specimen, no static load test, no comparison of a measured stiffness against the predicted one.
