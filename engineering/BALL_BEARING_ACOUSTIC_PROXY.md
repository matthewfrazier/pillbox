# Ball-bearing acoustic proxy

## Standardized contents

- Eight 5 mm Grade 25 AISI 52100 chrome-steel balls
- Manufacturer-specified mass: 0.513 g each
- Total moving mass: 4.104 g

This is a conservative hard-content proxy. It is repeatable and dimensionally precise, but it will overstate contact hardness relative to many tablets.

The initial PETG-only design uses three shorter compartments, integral rounded microtexture on the drawer floors and sleeve ceiling, and exterior roof/floor stiffening beads. A compliant liner remains a future option if the PETG-only prototype is still too loud.

## Deterministic drop benchmark

For a drop height `h`, incident energy is `N m g h`. Rebound energy is `e^2` times incident energy, where `e` is the measured coefficient of restitution for the bearing/surface pair. The supplied script uses explicit preliminary hypotheses of 0.45 for smooth PETG, 0.30 for textured PETG, and 0.12 for a 90A TPU liner.

At a 10 mm drop height, eight bearings carry 0.402 mJ incident energy. With the preliminary coefficients, predicted rebound heights are 2.03 mm, 0.90 mm, and 0.14 mm respectively. These values rank repeated-rattle potential, not emitted sound pressure: energy not returned to rebound can become heat, local deformation, or sound depending on each surface's loss factor and the shell modes.

## Calibration test

1. Print 50 x 50 mm coupons using the actual PETG profile: smooth, textured, and TPU-lined.
2. Drop one clean 5 mm bearing from 10.0 mm through a short vertical guide tube.
3. Record at 240 fps or faster with a scale in frame.
4. Measure first rebound height and calculate `e = sqrt(rebound/drop)`.
5. Repeat 20 times per surface and use the median `e` in `bearing_drop_proxy.py`.
6. Shake eight bearings in the complete pillbox at a controlled acceleration while recording A-weighted SPL and peak SPL at a fixed microphone distance.

The final shake test is necessary because coefficient of restitution predicts repeated bouncing, while audible noise also depends on PETG panel vibration, pill-to-pill collisions, contact duration, and microphone weighting.
