# topopt report -- child_core_frame_v5_study

## Verdict: **FAIL**

**FAIL** — 3 stop condition(s) failed. This part is not signed off.

| | conditions |
|---|---|
| failed | **3** |
| not checked | 5 |
| passed | 7 |

_The inputs this rests on — loads, material, machine, and what was fixed before the optimiser ran — are in `assumptions.md`. This page reports only what was measured._

## 1. What failed

These are errors, not warnings (spec 18). Each one names the fix.

- **The density field converged (not merely out of iterations)**  
  termination: max_iterations
- **Self-supporting along the build axis (no voxel without material in the 45 degree cone below it)**  
  15 voxel(s), 135 mm2 of material with nothing under it within 45 degrees (build axis +Z, at [[-38.9, -84.0, 94.0], [24.1, -60.0, 196.0]]); it would print on support or not at all. Enable design.overhang, or move the build axis
- **No support lands on a mating (preserve) face**  
  support rests on 354 preserve voxel(s) (3186.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly.

## 2. What was not checked

5 condition(s) have no answer in this run. Not checked is not the same as fine: an analysis that was never run is not evidence the part is sound, so these count against it and not for it.

- Safety factor meets the requirement on every case — _not checked in this run_
- Load/reaction balance within 1 % — _not checked in this run_
- Mesh convergence confirmed — _not checked in this run_
- Final shape is watertight — _not checked in this run_
- Minimum wall thickness is met — _not checked in this run_

## 3. What passed

<details><summary>7 condition(s) passed</summary>

- Units are declared and are mm / N / MPa (mm / N / MPa)
- Material properties have no unresolved nulls (orthotropic_equivalent_solid, provisional card (no values measured on this printer))
- Material coordinate system (build_axis) is defined (build axis Z)
- Setup validation passed (preserve/obstacle, loads on preserve) (0 error(s), 31 warning(s))
- All preserve regions are connected (42 component(s); 5616 mm3 of floating islands were dropped)
- The final shape was re-analysed (1 load case(s) re-solved on the thresholded solid)
- No support inside a sealed cavity (all support is reachable from outside)

</details>

## 4. Which shape this is

The optimiser produces a density field, not a shape. A threshold turns it into one, and different thresholds give different parts.

| threshold | volume (mm³) | safety factor (p99.5) | thinnest member (mm) |
|---|---|---|---|
| 0.40 | 404865 | - | 6.00 — grid-limited |
| 0.50 **← chosen** | 400707 | - | 6.00 — grid-limited |
| 0.60 | 396144 | - | 6.00 — grid-limited |

**Why this one:** no candidate could be analysed; this is a placeholder, not a choice

> A thinnest member marked *grid-limited* is exactly two voxels across, which is the finest the grid can represent. That number describes the mesh, not the structure.

## 5. How it was solved

| | |
|---|---|
| iterations | 80 of 80 requested |
| converged | **False** |
| why it stopped | `max_iterations` |
| volume fraction (of free cells) | 0.1 |
| filter radius | 6.0 mm |
| build axis | Z |
| material model | `orthotropic_equivalent_solid` |
| wall-clock | 24912 s |

> The material card is provisional — none of its values were measured on this printer. Use these results to compare options (build direction, layout, load case), not as an absolute strength.

## 6. Structural results

| load case | safety factor (p99.5) | safety factor (worst element) | max displacement (mm) |
|---|---|---|---|
| ? | 0.00 | 0.00 | 0.000 |

Required: safety factor ≥ 3.00 on every case.

> The p99.5 value decides pass/fail; the worst element decides whether a person has to go and look, because a single stair-stepped voxel at a load point is an artefact of the grid rather than of the part.

## 7. Can it be made

| | |
|---|---|
| machine | Bambu Lab X1-Carbon |
| usable build volume | 250 × 250 × 250 mm |
| design space | 153 × 129 × 234 mm |
| fits with Z up | **yes** |

| | |
|---|---|
| build axis | Z |
| flat overhang area | 22293.0 mm² |
| support volume | 1201230.0 mm³ |
| support on mating faces | support rests on 354 preserve voxel(s) (3186.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly. |
| enclosed support | all support is reachable from outside |

> measured on the voxel grid, so overhang angles are only 0 or 90 degrees. A 60-degree face that would self-support is not counted here; `topopt overhang` reads real angles off the STL.

## 8. How much of the shape was optimised

| | |
|---|---|
| share of the domain free to decide | 61 % |
| share of the expected part that is preserve | 43 % |

Positions fixed by the CAD model, not chosen by the optimiser:

| | region | position (mm) |
|---|---|---|
| support | `lug_boss_R` | [65.3, -10.9, 210.8] |
| support | `lug_boss_L` | [-65.1, -10.8, 210.8] |
| load | `pocket_bot` | [0.6, -37.8, -9.1] |
| load | `guard_boss_R` | [56.6, -32.4, -2.3] |
| load | `guard_boss_L` | [-56.4, -32.5, -2.3] |
| load | `latch_lo` | [64.6, -9.0, 40.0] |
| load | `latch_hi` | [64.6, -9.0, 169.0] |
| support | `pocket_bot` | [0.6, -37.8, -9.1] |
| support | `pocket_top` | [0.7, -38.7, 207.7] |
| load | `back_wall` | [-3.6, -93.8, 64.0] |
| load | `lug_boss_R` | [65.3, -10.9, 210.8] |
| load | `lug_boss_L` | [-65.1, -10.8, 210.8] |
| load | `knuckles` | [-72.2, 10.4, 100.0] |
| load | `grip_bar` | [0.1, -95.4, 157.0] |
| support | `band_mid` | [0.6, -41.7, 100.0] |

> Loads and supports may only act on preserve, so where the part is held is an input to this study. The optimiser decided how to reach those points, not where they are.

## 9. Independent re-analysis (CalculiX)

**Not run.** The voxel solver has not been checked against a second solver on a second mesh, so its results carry only its own assumptions.

## 10. Reproducibility

| | |
|---|---|
| commit | `1ffa0c88feb867a77f4af8b1ab36e8b11eb7f5ef` **(working tree dirty)** |
| tool version | 1.0.0 |
| python | 3.13.5 on Windows-11-10.0.26200-SP0 |
| numpy / scipy | 2.4.2 / 1.18.0 |
| run at | 2026-09-05T10:26:17Z (- s) |

> The working tree had uncommitted changes when this ran, so the commit above does not fully describe the code that produced these numbers.

**External tools on this machine:**

- calculix: **not installed**
- freecad: **not installed**
- gmsh: **not installed**
- openscad: `OpenSCAD version 2021.01`
- slicer: **not installed**
> A stage that needs a tool this machine does not have was not run. Its conditions are reported as not checked above, never as passing.

