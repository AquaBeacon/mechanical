# topopt report -- study

## Verdict: **FAIL**

**FAIL** — 5 stop condition(s) failed. This part is not signed off.

| | conditions |
|---|---|
| failed | **5** |
| not checked | 3 |
| passed | 8 |

_The inputs this rests on — loads, material, machine, and what was fixed before the optimiser ran — are in `assumptions.md`. This page reports only what was measured._

## 1. What failed

These are errors, not warnings (spec 18). Each one names the fix.

- **The density field converged (not merely out of iterations)**  
  termination: max_iterations
- **Safety factor meets the requirement on every case**  
  p99.5 2.27 vs required 3.00 (worst element 1.12)
- **Mesh convergence confirmed**  
  TOO COARSE (voxel FEA only: 2.0 (thin 6.00 mm) / 2.0 (typical 6.00 mm) vs required >= 3 elements across the thinnest section). A three-mesh convergence study still has not been run.
- **Self-supporting along the build axis (no voxel without material in the 45 degree cone below it)**  
  1 voxel(s), 9 mm2 of material with nothing under it within 45 degrees (build axis +Z, at [[30.1, -78.0, 39.0], [33.1, -75.0, 42.0]]); it would print on support or not at all. Enable design.overhang, or move the build axis
- **No support lands on a mating (preserve) face**  
  support rests on 443 preserve voxel(s) (3987.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly.

## 2. What was not checked

3 condition(s) have no answer in this run. Not checked is not the same as fine: an analysis that was never run is not evidence the part is sound, so these count against it and not for it.

- Load/reaction balance within 1 % — _not checked in this run_
- Final shape is watertight — _not checked in this run_
- Minimum wall thickness is met — _not checked in this run_

## 3. What passed

<details><summary>8 condition(s) passed</summary>

- Units are declared and are mm / N / MPa (mm / N / MPa)
- Material properties have no unresolved nulls (orthotropic_equivalent_solid, provisional card (no values measured on this printer))
- Material coordinate system (build_axis) is defined (build axis Z)
- Setup validation passed (preserve/obstacle, loads on preserve) (0 error(s), 38 warning(s))
- All preserve regions are connected (18 component(s); 4941 mm3 of floating islands were dropped)
- The optimiser's stress constraint held on the final density field (not requested (design.stress off); strength is judged by the final FEA only)
- The final shape was re-analysed (8 load case(s) re-solved on the thresholded solid)
- No support inside a sealed cavity (all support is reachable from outside)

</details>

## 4. Which shape this is

The optimiser produces a density field, not a shape. A threshold turns it into one, and different thresholds give different parts.

| threshold | volume (mm³) | safety factor (p99.5) | thinnest member (mm) |
|---|---|---|---|
| 0.50 **← chosen** | 360207 | 2.27 | 6.00 — grid-limited |

**Why this one:** no candidate passes every check; this is the strongest of the connected ones and is NOT a pass. Outstanding: stiffness (2.205 mm, required max deflection <= 1.000 mm); mesh resolution (2.0 (thin 6.00 mm) / 2.0 (typical 6.00 mm), required >= 3 elements across the thinnest section); strength (1.12 (worst element) / 2.27 (p99.5), required safety factor >= 3.00)

> A thinnest member marked *grid-limited* is exactly two voxels across, which is the finest the grid can represent. That number describes the mesh, not the structure.

## 5. How it was solved

| | |
|---|---|
| iterations | 80 of 80 requested |
| converged | **False** |
| why it stopped | `max_iterations` |
| volume fraction (of free cells) | 0.1 |
| filter radius | 9.0 mm |
| build axis | Z |
| material model | `orthotropic_equivalent_solid` |
| optimiser | oc |
| stress constraint | none (volume and stiffness only) |
| wall-clock | 1637 s |

> The material card is provisional — none of its values were measured on this printer. Use these results to compare options (build direction, layout, load case), not as an absolute strength.

## 6. Structural results

| load case | class | required | safety factor (p99.5) | safety factor (worst element) | max displacement (mm) |
|---|---|---|---|---|---|
| L1 hoist 3g: lugs fixed, container + guard + gate weights down | normal | 3.00 | 7.72 | 2.74 | 2.205 |
| L2s transport side hit 300 N (+X on back wall and lugs), container reacts | normal | 3.00 | 11.37 | 3.09 | 0.662 |
| L2h transport landing on the hinge side (300 N +X through the knuckles), container reacts | normal | 3.00 | 2.27 | 1.12 | 3.934 |
| L2r transport rear hit 300 N on the back wall (+Y), container reacts | normal | 3.00 | 6.12 | 2.05 | 1.444 |
| L3 clamp preload: knob bolts pull the latch bosses and the gate pulls the knuckles (+Y), tube reacts on the bands | normal | 3.00 | 5.43 | 2.23 | 0.406 |
| L5 landing 600 N up through the guard bosses, container reacts | normal | 3.00 | 57.00 | 24.80 | 0.006 |
| L6 grip lift +200 N: equivalent handling test with vessel restrained; provisional 6kg x 3g rounded up | normal | 3.00 | 11.70 | 4.37 | 0.395 |
| L7 vertical light 3g: provisional 0.3kg, 9N weight plus 324Nmm offset moment | normal | 3.00 | 137.19 | 62.23 | 0.044 |

Required: safety factor ≥ 3.00 on every normal case; abnormal cases (drop, one foot caught) are judged at their own `required` column (spec 15.1).

> The p99.5 value decides pass/fail; the worst element decides whether a person has to go and look, because a single stair-stepped voxel at a load point is an artefact of the grid rather than of the part.

## 7. Can it be made

| | |
|---|---|
| machine | Bambu Lab X1-Carbon |
| usable build volume | 250 × 250 × 250 mm |
| design space | 153 × 129 × 237 mm |
| fits with Z up | **yes** |

| | |
|---|---|
| build axis | Z |
| flat overhang area | 18396.0 mm² |
| support volume | 1543995.0 mm³ |
| support on mating faces | support rests on 443 preserve voxel(s) (3987.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly. |
| enclosed support | all support is reachable from outside |

> measured on the voxel grid, so overhang angles are only 0 or 90 degrees. A 60-degree face that would self-support is not counted here; `topopt overhang` reads real angles off the STL.

## 8. What the slicer says

**UNKNOWN** -- no `slice.json` in this run. Print time, real filament use and real support quantity come from a slicer and from nothing else; they are not estimated here.

    topopt slice PART.stl --out DIR

## 9. How much of the shape was optimised

| | |
|---|---|
| share of the domain free to decide | 53 % |
| share of the expected part that is preserve | 47 % |

Positions fixed by the CAD model, not chosen by the optimiser:

| | region | position (mm) |
|---|---|---|
| support | `lug_boss_R` | [65.1, -10.9, 211.5] |
| support | `lug_boss_L` | [-65.0, -10.8, 211.5] |
| load | `pocket_bot` | [0.6, -37.7, -10.1] |
| load | `guard_boss_R` | [56.6, -32.5, -3.3] |
| load | `guard_boss_L` | [-56.4, -32.5, -3.3] |
| load | `latch_lo` | [64.6, -9.0, 39.0] |
| load | `latch_hi` | [64.6, -9.0, 171.0] |
| load | `td04a_hp1` | [0.5, -85.3, 216.0] |
| support | `pocket_bot` | [0.6, -37.7, -10.1] |
| support | `pocket_top` | [0.6, -39.0, 210.3] |
| load | `back_wall` | [-3.7, -93.9, 65.2] |
| load | `lug_boss_R` | [65.1, -10.9, 211.5] |
| load | `lug_boss_L` | [-65.0, -10.8, 211.5] |
| load | `knuckles` | [-72.2, 10.4, 100.5] |
| load | `grip_bar` | [0.1, -95.4, 157.5] |
| support | `band_mid` | [0.6, -41.7, 100.5] |
| load | `grip_underside` | [0.1, -95.4, 147.0] |
| load | `light_hp` | [42.1, -75.0, 100.5] |
| load | `light_hp_upper` | [42.1, -75.0, 120.0] |
| load | `light_hp_lower` | [42.1, -75.0, 81.0] |

> Loads and supports may only act on preserve, so where the part is held is an input to this study. The optimiser decided how to reach those points, not where they are.

## 10. Independent re-analysis (CalculiX)

**Not run.** The voxel solver has not been checked against a second solver on a second mesh, so its results carry only its own assumptions.

## 11. Reproducibility

| | |
|---|---|
| commit | `not recorded` |
| tool version | 1.0.0 |
| python | 3.13.5 on Windows-11-10.0.26200-SP0 |
| numpy / scipy | 2.4.2 / 1.18.0 |
| run at | 2026-09-10T07:16:51Z (- s) |

**External tools on this machine:**

- calculix: `This is Version 2.23`
- freecad: `FreeCAD 1.0.0 Revision: 39109 (Git)`
- gmsh: `4.15.2`
- openscad: `OpenSCAD version 2021.01`
- slicer: `None`
> A stage that needs a tool this machine does not have was not run. Its conditions are reported as not checked above, never as passing.

