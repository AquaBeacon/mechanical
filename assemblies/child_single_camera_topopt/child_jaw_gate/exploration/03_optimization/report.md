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
  p99.5 0.40 vs required 3.00 (worst element 0.17)
- **Mesh convergence confirmed**  
  TOO COARSE (voxel FEA only: 2.0 (thin 6.00 mm) / 2.0 (typical 6.00 mm) vs required >= 3 elements across the thinnest section). A three-mesh convergence study still has not been run.
- **Self-supporting along the build axis (no voxel without material in the 45 degree cone below it)**  
  4 voxel(s), 36 mm2 of material with nothing under it within 45 degrees (build axis +Z, at [[-56.0, 37.1, 48.0], [-47.0, 46.1, 54.0]]); it would print on support or not at all. Enable design.overhang, or move the build axis
- **No support lands on a mating (preserve) face**  
  support rests on 578 preserve voxel(s) (5202.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly.

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
- Setup validation passed (preserve/obstacle, loads on preserve) (0 error(s), 31 warning(s))
- All preserve regions are connected (4 component(s); 1161 mm3 of floating islands were dropped)
- The optimiser's stress constraint held on the final density field (not requested (design.stress off); strength is judged by the final FEA only)
- The final shape was re-analysed (5 load case(s) re-solved on the thresholded solid)
- No support inside a sealed cavity (all support is reachable from outside)

</details>

## 4. Which shape this is

The optimiser produces a density field, not a shape. A threshold turns it into one, and different thresholds give different parts.

| threshold | volume (mm³) | safety factor (p99.5) | thinnest member (mm) |
|---|---|---|---|
| 0.50 **← chosen** | 151632 | 0.40 | 6.00 — grid-limited |

**Why this one:** no candidate passes every check; this is the strongest of the connected ones and is NOT a pass. Outstanding: mesh resolution (2.0 (thin 6.00 mm) / 2.0 (typical 6.00 mm), required >= 3 elements across the thinnest section); strength (0.30 (worst element) / 0.67 (p99.5), required safety factor >= 3.00); stiffness (27.740 mm, required max deflection <= 1.000 mm)

> A thinnest member marked *grid-limited* is exactly two voxels across, which is the finest the grid can represent. That number describes the mesh, not the structure.

## 5. How it was solved

| | |
|---|---|
| iterations | 80 of 80 requested |
| converged | **False** |
| why it stopped | `max_iterations` |
| volume fraction (of free cells) | 0.052 |
| filter radius | 9.0 mm |
| build axis | Z |
| material model | `orthotropic_equivalent_solid` |
| optimiser | oc |
| stress constraint | none (volume and stiffness only) |
| wall-clock | 1062 s |

> The material card is provisional — none of its values were measured on this printer. Use these results to compare options (build direction, layout, load case), not as an absolute strength.

## 6. Structural results

| load case | class | required | safety factor (p99.5) | safety factor (worst element) | max displacement (mm) |
|---|---|---|---|---|---|
| L1 hoist 3g: single camera + smaller adapter, 20N total on HP4/HP5 plus gate self-weight | normal | 3.00 | 28.55 | 15.57 | 0.376 |
| L2f transport frontal 300 N (-Y) through the cam bridge into HP4/HP5, the container reacts on the three bands | normal | 3.00 | 0.67 | 0.30 | 27.740 |
| L2s transport side 300 N (-X on the latch edge), the container reacts on the three bands | normal | 3.00 | 1.84 | 0.64 | 4.806 |
| L3 clamp preload: the two M5 knob bolts pull the latch bosses -Y (300 N each) and the hinge pin pulls the knuckles -Y, the tube + EVA react on the three bands | normal | 3.00 | 1.16 | 0.41 | 6.808 |
| L4 frontal collision 300 N on the top of the bridge column (z 195): statics on the HP4/HP5 bolt pair (z 170 / 100) gives -400 N on HP4 and +100 N pull-out on HP5, the container reacts on the three bands | normal | 3.00 | 0.40 | 0.17 | 33.486 |

Required: safety factor ≥ 3.00 on every normal case; abnormal cases (drop, one foot caught) are judged at their own `required` column (spec 15.1).

> The p99.5 value decides pass/fail; the worst element decides whether a person has to go and look, because a single stair-stepped voxel at a load point is an artefact of the grid rather than of the part.

## 7. Can it be made

| | |
|---|---|
| machine | Bambu Lab X1-Carbon |
| usable build volume | 250 × 250 × 250 mm |
| design space | 153 × 72 × 237 mm |
| fits with Z up | **yes** |

| | |
|---|---|
| build axis | Z |
| flat overhang area | 8586.0 mm² |
| support volume | 443610.0 mm³ |
| support on mating faces | support rests on 578 preserve voxel(s) (5202.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly. |
| enclosed support | all support is reachable from outside |

> measured on the voxel grid, so overhang angles are only 0 or 90 degrees. A 60-degree face that would self-support is not counted here; `topopt overhang` reads real angles off the STL.

## 8. What the slicer says

**UNKNOWN** -- no `slice.json` in this run. Print time, real filament use and real support quantity come from a slicer and from nothing else; they are not estimated here.

    topopt slice PART.stl --out DIR

## 9. How much of the shape was optimised

| | |
|---|---|
| share of the domain free to decide | 37 % |
| share of the expected part that is preserve | 72 % |

Positions fixed by the CAD model, not chosen by the optimiser:

| | region | position (mm) |
|---|---|---|
| support | `knuckles` | [-71.7, 9.8, 100.4] |
| support | `latch_lo` | [63.2, 22.2, 40.5] |
| support | `latch_hi` | [63.2, 22.2, 169.5] |
| load | `hp4` | [-0.5, 69.5, 169.5] |
| load | `hp5` | [-0.3, 68.8, 100.5] |
| support | `pocket_bot` | [1.6, 41.5, -10.2] |
| support | `band_mid` | [1.9, 39.6, 100.5] |
| support | `pocket_top` | [1.9, 39.8, 209.6] |
| load | `latch_lo` | [63.2, 22.2, 40.5] |
| load | `latch_hi` | [63.2, 22.2, 169.5] |
| load | `knuckles` | [-71.7, 9.8, 100.4] |

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
| run at | 2026-09-10T06:58:38Z (- s) |

**External tools on this machine:**

- calculix: `This is Version 2.23`
- freecad: `FreeCAD 1.0.0 Revision: 39109 (Git)`
- gmsh: `4.15.2`
- openscad: `OpenSCAD version 2021.01`
- slicer: `None`
> A stage that needs a tool this machine does not have was not run. Its conditions are reported as not checked above, never as passing.

