# PETG Fit and Detent Engineering Check

## Geometry decision

- Sleeve internal opening: 50.6 x 15.8 mm
- Drawer body: 50.2 x 15.4 mm
- Centered running clearance: 0.20 mm per side, top, and bottom
- Bilateral detent interference during engagement: 0.05 mm per wall
- Rear-bottom detent interference during engagement: 0.05 mm into a shallow sleeve-floor receiver
- Receiver pockets are recessed into the sleeve inner walls and do not break the exterior skin

The running surfaces remain clearance fits. Retention comes from three localized detents—two side locks and one rear-bottom lock—avoiding the high and inconsistent friction that would result from making the entire PETG drawer an interference fit.

## Solver model

- Solver: CalculiX 2.23 installed with FreeCAD 1.1.1
- Analysis: geometrically nonlinear static solid-element submodel
- Mesh: 9,471 nodes and 7,680 reduced-integration hexahedral elements
- Sleeve wall: 20 x 1.5 x 16 mm local wall strip
- Detent contact footprint: 8 x 2.6 mm
- Boundary condition: wall continuity fixed at the sleeve roof and floor edges
- Loading: imposed outward displacement over the detent footprint
- Material: bilinear printed PETG baseline, E = 1939 MPa, nu = 0.38, yield = 46.2 MPa

The imposed-patch model is conservative: it prevents contact pressure from redistributing around the rounded detent. It is useful for sizing and comparing detent interference, but extraction force still depends on ramp angle, surface finish, lubrication, and the printed coefficient of friction.

## Results per sleeve wall

| Interference | Normal reaction | Peak von Mises stress | Result |
|---:|---:|---:|---|
| 0.05 mm | 24.4 N | 6.1 MPa | Selected |
| 0.10 mm | 48.8 N | 12.2 MPa | Excessively stiff |
| 0.15 mm | 73.3 N | 18.1 MPa | Excessively stiff |
| 0.30 mm | 147.9 N | 35.7 MPa | Rejected |

No plastic strain was predicted in the tested cases, but avoiding yield alone is not an acceptable usability criterion. The 0.05 mm case provides the lowest force and a large stress margin. Because typical FDM dimensional variation can exceed 0.05 mm, print a receiver/detent coupon at 0.00, 0.05, and 0.10 mm nominal interference before committing to production geometry.

## Limitations

- UltiMaker printed-PETG data is used as a baseline, not a universal PETG definition.
- Poisson's ratio is assumed because it is not supplied in the cited tensile data.
- Creep, cyclic fatigue, moisture, temperature, layer adhesion defects, and printer dimensional error are not represented.
- A production release should use the chosen filament's stress-strain data and measured coupon dimensions.
