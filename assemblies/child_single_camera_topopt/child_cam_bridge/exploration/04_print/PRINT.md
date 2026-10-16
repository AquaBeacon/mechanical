# Print this: `study.stl`

> ## This is optimiser output, not a finished part.
>
> The shape is quantised to the 3.0 mm voxel grid it was solved on, so **every mating dimension in it is wrong by up to one voxel**. On a real run a 3.50 mm slot came out at 3.21 mm and the assembly would not go together. Bolt holes, slots, bearing seats and mating faces must be rebuilt in CAD from the source model, and the result checked with `topopt compare`.

> ## The analysis verdict is FAIL.
>
> Printing this is fine for looking at, fitting, and checking the layout. It is not signed off to carry load. See section 3.

## 1. Files

| file | what it is |
|---|---|
| `study.stl` | **the mesh to slice** |
| `../../../_work/images/child_cam_bridge/exploration/04_print/preview_shape.png` | what the optimiser produced, in section |
| `../../../_work/images/child_cam_bridge/exploration/04_print/preview_design_space.png` | what it was allowed to fill — compare against the shape |
| `../../../_work/images/child_cam_bridge/exploration/04_print/preview_print.png` | **what the mesh above actually looks like** — three shaded views of the surface you are about to slice, flat-shaded so faceting shows |
| `../../../_work/images/child_cam_bridge/exploration/04_print/preview_orientation.png` | how it sits on the plate, and what overhangs |

Threshold **0.50** of the density field.

_Why this one: no candidate passes every check; this is the strongest of the connected ones and is NOT a pass. Outstanding: mesh resolution (2.0 (thin 6.00 mm) / 2.0 (typical 6.00 mm), required >= 3 elements across the thinnest section)_

## 2. How to print it

| | |
|---|---|
| orientation the analysis assumed | model **Y** axis up |
| fits the build volume | yes |
| size as modelled | 120.0 × 69.0 × 150.0 mm |
| lowest-support orientation | +Z up |
| support volume in this orientation | 340605 mm³ |

**Do not reorient it to save support.** The material is anisotropic and the analysis was run with the axis above pointing up; laying the part on its side moves the layer planes and the safety factors no longer apply to it. If another orientation is wanted, change `build_axis` in the study and re-run.

**Support on mating faces.** support rests on 42 preserve voxel(s) (378.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly.

## 3. What is still wrong with it

These failed the stop conditions (spec 18). They are listed in full, with the fix, in `../03_optimization/report.md`.

- **The density field converged (not merely out of iterations)** — termination: max_iterations
- **Mesh convergence confirmed** — TOO COARSE (voxel FEA only: 2.0 (thin 6.00 mm) / 2.0 (typical 6.00 mm) vs required >= 3 elements across the thinnest section). A three-mesh convergence study still has not been run.
- **No support lands on a mating (preserve) face** — support rests on 42 preserve voxel(s) (378.0 mm2). Those faces come off the printer rough and out of tolerance. Reorient the part, or accept the finish and say so explicitly.
- _not checked:_ Load/reaction balance within 1 %
- _not checked:_ Final shape is watertight
- _not checked:_ Minimum wall thickness is met

_This list covers the stop conditions the report checks. **How much support the part needs is not one of them** -- that is judged by `topopt print <stl>`, which applies a 15 % overhang-area limit and is worth running before you slice._

## 4. Where the rest of it is

| | |
|---|---|
| what was assumed (loads, material, machine, what was fixed) | `../01_assumptions/assumptions.md` |
| the design space and its validation | `../02_setup/` |
| the full analysis and every number | `../03_optimization/report.md` |

