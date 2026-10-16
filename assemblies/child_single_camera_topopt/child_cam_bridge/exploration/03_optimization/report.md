# topopt report -- study

## Verdict: **FAIL**

**FAIL** — 3 stop condition(s) failed. This part is not signed off.

| | conditions |
|---|---|
| failed | **3** |
| not checked | 3 |
| passed | 10 |

_The inputs this rests on — loads, material, machine, and what was fixed before the optimiser ran — are in `assumptions.md`. This page reports only what was measured._

## 1. What failed

These are errors, not warnings (spec 18). Each one names the fix.

- **The density field converged (not merely out of iterations)**  
  termination: max_iterations
- **Mesh convergence confirmed**  
  TOO COARSE (voxel FEA only: 2.0 (thin 6.00 mm) / 2.0 (typical 6.00 mm) vs required >= 3 elements across the thinnest section). A three-mesh convergence study still has not been run.
- **No support lands on a mating (preserve) face**  
  support rests on 42 preserve voxel(s) (378.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly.

## 2. What was not checked

3 condition(s) have no answer in this run. Not checked is not the same as fine: an analysis that was never run is not evidence the part is sound, so these count against it and not for it.

- Load/reaction balance within 1 % — _not checked in this run_
- Final shape is watertight — _not checked in this run_
- Minimum wall thickness is met — _not checked in this run_

## 3. What passed

<details><summary>10 condition(s) passed</summary>

- Units are declared and are mm / N / MPa (mm / N / MPa)
- Material properties have no unresolved nulls (orthotropic_equivalent_solid, provisional card (no values measured on this printer))
- Material coordinate system (build_axis) is defined (build axis Y)
- Setup validation passed (preserve/obstacle, loads on preserve) (0 error(s), 2 warning(s))
- All preserve regions are connected (37 component(s); 10800 mm3 of floating islands were dropped)
- The optimiser's stress constraint held on the final density field (not requested (design.stress off); strength is judged by the final FEA only)
- The final shape was re-analysed (4 load case(s) re-solved on the thresholded solid)
- Safety factor meets the requirement on every case (p99.5 8.04 vs required 3.00 (worst element 2.82))
- Self-supporting along the build axis (no voxel without material in the 45 degree cone below it) (every optimised voxel has material in the 45 degree cone below it (build axis +Y); 11 voxel(s) / 99 mm2 hang off a preserve body -- that is the interface's own underside, chamfer or roof it in CAD)
- No support inside a sealed cavity (all support is reachable from outside)

</details>

## 4. Which shape this is

The optimiser produces a density field, not a shape. A threshold turns it into one, and different thresholds give different parts.

| threshold | volume (mm³) | safety factor (p99.5) | thinnest member (mm) |
|---|---|---|---|
| 0.50 **← chosen** | 180576 | 8.04 | 6.00 — grid-limited |

**Why this one:** no candidate passes every check; this is the strongest of the connected ones and is NOT a pass. Outstanding: mesh resolution (2.0 (thin 6.00 mm) / 2.0 (typical 6.00 mm), required >= 3 elements across the thinnest section)

> A thinnest member marked *grid-limited* is exactly two voxels across, which is the finest the grid can represent. That number describes the mesh, not the structure.

## 5. How it was solved

| | |
|---|---|
| iterations | 80 of 80 requested |
| converged | **False** |
| why it stopped | `max_iterations` |
| volume fraction (of free cells) | 0.2 |
| filter radius | 9.0 mm |
| build axis | Y |
| material model | `orthotropic_equivalent_solid` |
| optimiser | oc |
| stress constraint | none (volume and stiffness only) |
| wall-clock | 96 s |

> The material card is provisional — none of its values were measured on this printer. Use these results to compare options (build direction, layout, load case), not as an absolute strength.

## 6. Structural results

| load case | class | required | safety factor (p99.5) | safety factor (worst element) | max displacement (mm) |
|---|---|---|---|---|---|
| L1 single 0.35kg camera at 3g, adapter self-weight at 3g | normal | 3.00 | 89.74 | 14.62 | 0.789 |
| L4 frontal impact 150 N (-Y) on one front-edge bumper, HP4/HP5 react | normal | 3.00 | 8.04 | 2.82 | 0.575 |
| L2s side impact 150 N (-X) on the starboard end plate through the side bumper, HP4/HP5 react | normal | 3.00 | 13.78 | 6.61 | 0.278 |
| L6 unit handled by central camera, 100N +Z on single mounting seat | normal | 3.00 | 17.41 | 7.65 | 0.247 |

Required: safety factor ≥ 3.00 on every normal case; abnormal cases (drop, one foot caught) are judged at their own `required` column (spec 15.1).

> The p99.5 value decides pass/fail; the worst element decides whether a person has to go and look, because a single stair-stepped voxel at a load point is an artefact of the grid rather than of the part.

## 7. Can it be made

| | |
|---|---|
| machine | Bambu Lab X1-Carbon |
| usable build volume | 250 × 250 × 250 mm |
| design space | 120 × 69 × 150 mm |
| fits with Y up | **yes** |

| | |
|---|---|
| build axis | Y |
| flat overhang area | 14679.0 mm² |
| support volume | 340605.0 mm³ |
| support on mating faces | support rests on 42 preserve voxel(s) (378.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly. |
| enclosed support | all support is reachable from outside |

> measured on the voxel grid, so overhang angles are only 0 or 90 degrees. A 60-degree face that would self-support is not counted here; `topopt overhang` reads real angles off the STL.

## 8. What the slicer says

**UNKNOWN** -- no `slice.json` in this run. Print time, real filament use and real support quantity come from a slicer and from nothing else; they are not estimated here.

    topopt slice PART.stl --out DIR

## 9. How much of the shape was optimised

| | |
|---|---|
| share of the domain free to decide | 53 % |
| share of the expected part that is preserve | 40 % |

Positions fixed by the CAD model, not chosen by the optimiser:

| | region | position (mm) |
|---|---|---|
| support | `hp4_seat` | [0.0, 76.0, 169.4] |
| support | `hp5_seat` | [0.0, 76.0, 100.5] |
| load | `mount_C` | [0.0, 106.0, 49.5] |
| load | `fbump_R` | [45.0, 133.0, 63.0] |
| load | `endp_R` | [57.0, 101.5, 63.0] |

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
| run at | 2026-09-10T06:56:37Z (- s) |

**External tools on this machine:**

- calculix: `This is Version 2.23`
- freecad: `FreeCAD 1.0.0 Revision: 39109 (Git)`
- gmsh: `4.15.2`
- openscad: `OpenSCAD version 2021.01`
- slicer: `None`
> A stage that needs a tool this machine does not have was not run. Its conditions are reported as not checked above, never as passing.

