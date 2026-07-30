# Pillbox Design Specification

## Overview
3D-printable pill organizer with two-part design: sleeve container and internal drawer. Credit-card sized with ultra-thin profile for pocket carry.

## Assembly
- Exactly two manufactured solid pieces: one monolithic sleeve + one monolithic drawer
- No separate panels, trim, pull-tab, divider, or fastener parts
- Drawer travels along the 86 mm axis and exits through the smallest outer face: the 54 x 19 mm end face
- Three-point friction-lock mechanism: symmetric locks on both drawer side edges plus one rear-bottom lock
- Closed bottom, open front for drawer insertion/removal

## Sleeve (Container)
- Outer dimensions: 86 x 54 x 19 mm (standard credit card + height: 0.75 inches)
- Nominal broad roof/floor thickness: 1.1 mm between stiffening beads; locally thickened to approximately 2.1 mm at the beads; nominal side-wall thickness: 1.7 mm
- Closed perimeter shell with one open 54 x 19 mm end face
- Manufactured as one continuous solid body; the shell must not read as an assembly of separate curved-edge panels
- External curvature is restrained and nearly planar, with a target outer edge radius of approximately 1.5 mm
- Interior opening and transitions are filleted where manufacturing clearances permit
- The exterior roof and underside include shallow integral longitudinal stiffening beads while remaining within the 19 mm overall height envelope
- The interior ceiling includes an integral field of low rounded PETG microtexture bumps positioned above the compartment lanes
- Both inner side walls include shallow, rounded detent receivers aligned with the drawer locks in the fully closed position
- The sleeve floor includes a shallow receiver aligned with the drawer's rear-bottom detent in the fully closed position
- Detent receivers must retain the sleeve's continuous exterior surface and must not break through the outer walls
- Surface: smooth finish
- Future: may add slide-lock mechanism (not priority)

## Drawer (Insertable Tray)
- Body dimensions: approximately 82 x 50.2 x 15.0 mm
- Running clearance: 0.20 mm at each side and below the drawer; approximately 0.60 mm to the plain ceiling and 0.30 mm to the ceiling microtexture crowns
- Manufactured as one continuous solid body, including its floor, walls, dividers, and pull
- Internal division: 3 compartments arranged along the 82 mm travel direction to reduce contents' free travel distance
- Tray perimeter walls: approximately 1.5 mm thick; two divider walls: approximately 1.2 mm thick
- Each compartment floor includes integral rounded PETG microtexture bumps approximately 0.3 mm high, with broad crowns and approximately 6 mm nominal spacing
- External edge radius: approximately 1.2 mm, retaining softened edges without a heavily curved appearance
- Surface: smooth finish

## Drawer Features
- Pull grip: integral full-width grip across the complete drawer body width (approximately 50 mm)
- Grip is located on the drawer's front 54 mm end and forms part of the single drawer solid
- Grip provides opposed top and bottom contact surfaces with enough projection/relief for a deliberate thumb-and-finger pinch, not a fingertip-only hook
- All grip edges are comfortably rounded while retaining a positive pinch surface
- The top of the pull includes shallow, rounded grip ridges for traction
- The tops of the grip ridges align flush with the top edge of the drawer; no part of the pull projects above the drawer body
- Friction engagement: matching integral bumps on both drawer side edges
- Each friction bump engages a shallow receiver recessed into the corresponding sleeve inner wall
- A third integral bump on the rear underside of the drawer engages a shallow receiver recessed into the sleeve floor
- Detents must provide tactile retention without requiring excessive pull force or scraping the sleeve exterior wall
- Nominal detent interference: 0.05 mm at each side and bottom lock, based on the PETG nonlinear wall-deflection submodel

## Material & Finish
- Intended production material: FDM PETG, printed flat with the 86 x 54 mm face parallel to the build plate
- Baseline analysis properties: printed-XY Young's modulus 1939 MPa, Poisson's ratio 0.38 (assumed), and tensile yield stress 46.2 MPa
- Final detent sizing must be validated with the selected filament, printer profile, and a small tolerance coupon because printed PETG is anisotropic and process-dependent
- Slightly rounded edges for comfort and aesthetics
- Smooth interior surfaces for ease of use
- No sharp edges
- All noise-control texture is nonporous, broadly rounded, and integral to the PETG bodies for cleanability

## Assembly Notes
- Friction-lock: two edge bumps and one rear-bottom bump seat into matching shallow sleeve receivers when fully closed
- Drawer slides in/out smoothly
- Compartments sized for pill storage
- Fit: drawer should slide with slight resistance

## Future Enhancements
- Slide-lock mechanism option
- Custom compartment sizing
- Different material finishes
