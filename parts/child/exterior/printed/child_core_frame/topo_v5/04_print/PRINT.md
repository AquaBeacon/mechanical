# Print this: `child_core_frame_v5.stl`

> ## Half of this is a finished part. Know which half.
>
> The **interface** was re-cut from the source CAD on a 0.50 mm grid, so a feature width is good to within **0.50 mm** instead of 3.0 mm. Not exact — quote that tolerance, do not quote the drawing. The **optimised body** is still the analysis grid: resampling it added no detail it never had, and no mating dimension may be taken off it.
>
> The analysis did **not** see this shape. The FEA ran on the 3.0 mm interface, so stresses in and around it are resolved no better than that grid allows.

> ## The analysis verdict is FAIL.
>
> Printing this is fine for looking at, fitting, and checking the layout. It is not signed off to carry load. See section 3.

## 1. Files

| file | what it is |
|---|---|
| `child_core_frame_v5.stl` | **the mesh to slice** — optimiser body with the interface re-cut from CAD on a 0.50 mm grid |
| `child_core_frame_v5_raw.stl` | what the optimiser produced, on the analysis grid |
| `child_core_frame_v5_smooth.stl` | the same shape, Taubin-smoothed — nicer surface, slightly different dimensions |
| `child_core_frame_v5.step` | solid model for CAD, if you are rebuilding the interfaces (you are) |
| `../../_work/images/topo_v5/04_print/preview_shape.png` | what the optimiser produced, in section |
| `../../_work/images/topo_v5/04_print/preview_design_space.png` | what it was allowed to fill — compare against the shape |
| `../../_work/images/topo_v5/04_print/preview_orientation.png` | how it sits on the plate, and what overhangs |

Threshold **0.50** of the density field.

_Why this one: no candidate could be analysed; this is a placeholder, not a choice_

## 2. How to print it

| | |
|---|---|
| orientation the analysis assumed | model **Z** axis up |
| fits the build volume | yes |
| size as modelled | 153.0 × 129.0 × 234.0 mm |
| lowest-support orientation | -Z up |
| support volume in this orientation | 1201230 mm³ |

**Do not reorient it to save support.** The material is anisotropic and the analysis was run with the axis above pointing up; laying the part on its side moves the layer planes and the safety factors no longer apply to it. If another orientation is wanted, change `build_axis` in the study and re-run.

**Support on mating faces.** support rests on 354 preserve voxel(s) (3186.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly.

## 3. What is still wrong with it

These failed the stop conditions (spec 18). They are listed in full, with the fix, in `../03_optimization/report.md`.

- **The density field converged (not merely out of iterations)** — termination: max_iterations
- **Self-supporting along the build axis (no voxel without material in the 45 degree cone below it)** — 15 voxel(s), 135 mm2 of material with nothing under it within 45 degrees (build axis +Z, at [[-38.9, -84.0, 94.0], [24.1, -60.0, 196.0]]); it would print on support or not at all. Enable design.overhang, or move the build axis
- **No support lands on a mating (preserve) face** — support rests on 354 preserve voxel(s) (3186.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly.
- _not checked:_ Safety factor meets the requirement on every case
- _not checked:_ Load/reaction balance within 1 %
- _not checked:_ Mesh convergence confirmed
- _not checked:_ Final shape is watertight
- _not checked:_ Minimum wall thickness is met

_This list covers the stop conditions the report checks. **How much support the part needs is not one of them** -- that is judged by `topopt print <stl>`, which applies a 15 % overhang-area limit and is worth running before you slice._

## 4. Where the rest of it is

| | |
|---|---|
| what was assumed (loads, material, machine, what was fixed) | `../01_assumptions/assumptions.md` |
| the design space and its validation | `../02_setup/` |
| the full analysis and every number | `../03_optimization/report.md` |

