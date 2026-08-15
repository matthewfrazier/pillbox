#!/usr/bin/env python3
"""v8.8 — the same bolt again, marked on the blade's back face, with the date back on it.

Not one dimension of the part moves. v8.5's geometry, v8.6's and v8.7's mark practice, the
same font at the same cap to the same measured stroke floor. What changes is WHERE the
recess is cut and, because of that, WHAT it can say: "v8.8 15ag26" instead of "v8.7". It is
cut HERE, in the design source, rather than onto the exported STL afterwards, because the
project builds print/{version}_pillbox_plate.stl from the tagged script: a mark applied
downstream is gone at the next refresh. The guard block below proves the rest of the bolt
did not move — same bounding box to 1e-4, volume down by the mark's own cut and nothing else.

WHAT CHANGED FROM v8.7, AND WHY — the rule we were using was the wrong shape
  v8.7 confined the mark to the thumb pad's land and then wrote the datecode off as
  something that "belongs on a part with room for it". Both of those followed from one
  sentence in the placement rules — never mark a sliding or bearing face — applied to the
  blade's +X side as a whole. The operator looked at the printed bolt and said the obvious
  thing: that face is 30.5 x 7.0mm of flat material, nearly all of it touching nothing, and
  a recess out on the tip end of it cannot interfere with anything the bolt does.
  He is right, and the rule as written is too coarse. A FACE is not the unit. The unit is a
  BAND. Read off this script's own constants: the drawer's detent fin carries exactly one
  sphere, BUMP_R = 1.1 centred at x = FIN_X0 + BUMP_R - BUMP_PROUD = 10.05, y = BUMP_Y = 17.10,
  z = ZC = 9.375, standing 0.25 proud into the blade's face. Everything else that comes near
  that face stands off it, and the source says by how much: the drawer's channel wall at
  CH_X1 = 9.50 clears the face by CLR = 0.30; the sleeve's bolt hole at HOLE_X1 = 9.70 clears
  it by HOLE_CLR_X_FREE = 0.50 — the asymmetric hole's LOOSE side is this one, by design,
  precisely because this is the face that never bears; the counterbore is 0.40 looser still;
  the fin's own relief is behind the fin, outside the channel entirely. Nothing else in the
  assembly reaches x = 9.20 anywhere in the stroke.
  So exactly ONE thing ever touches the marked face, and it touches a band 2.2mm tall
  centred on mid-height and 8.10mm long between the dimples: 17.8mm2 of the face's 301mm2,
  under 6%. v8.7 gave away the other 94% for a rule of thumb, and the date with it.

WHAT THE HAZARD ACTUALLY IS — a false detent, not wear
  The reason to stay off the bump's path is not that a letter would wear. It is that a
  recess ON that path is somewhere for the bump to DROP INTO: the bolt would click where it
  should not, and a lock that clicks in the wrong place is worse than one that does not
  click at all. The same reasoning forbids breaking either dimple's rim, since a broken rim
  turns a clean detent into a ragged one.
  The free region is therefore DERIVED here, from the fin and dimple parameters, and
  asserted at build time — not eyeballed off a render:
    the swept band, in the bolt's own frame (the bolt is modelled at LOCKED)
      Y  DIMPLE_LOCK_Y - BUMP_R .. DIMPLE_OPEN_Y + OVERTRAVEL_OPEN + BUMP_R = 16.00 .. 24.10
      Z  ZC -/+ BUMP_R                                                      =  8.275 .. 10.475
    OVERTRAVEL_OPEN is not a fudge factor: it is (TIP_OPEN - BOLT_L) - CH_Y0 = 0.50, the
    distance the bolt can still be pushed AFTER the OPEN detent before its tail bottoms out
    on the bore's closed end. The LOCKED end needs no such term — the pad bears on the
    sleeve wall there, which is a hard stop, not a detent.
    The band is drawn with BUMP_R rather than the bump's true contact circle. The sphere is
    only 0.25 proud of the face, so what can actually touch is a disc of radius
    sqrt(BUMP_R^2 - (BUMP_R - 0.25)^2) = 0.698mm. Using 1.1 makes the band 0.402mm wider on
    every side than the contact patch can ever be. That conservatism is free, so it is kept.
    Both dimple rims sit INSIDE that band — 1.025mm for the 0.7-deep LOCKED dimple, 0.887mm
    for the 0.45-deep OPEN one, against the band's 1.1 — so guarding the band guards the
    rims as well. The build asserts that relationship rather than assuming it.
  MARK_BAND_CLR = 1.0mm on top of the band. Sized for the two things that could put material
  where the arithmetic says there is none: a recess perimeter that bulges outward by an
  extrusion width (0.42) or starts its seam there, and the position error between a blade
  printed now and the fin printed back at v8.4. 1.0mm is ~2.4 extrusion widths, and it sits
  on top of the 0.402mm already built into the band, so the real gap from the nearest stroke
  to the furthest the bump's contact patch can ever reach is over 1.5mm. Larger was tried
  and rejected: 2.0mm forces the cap under the stroke floor, which trades a real legibility
  floor for an imaginary safety one.

WHICH FACE, AND WHAT RIDES ON IT
  +X — the blade's BACK face, the one carrying the two detent dimples. It is NOT the loaded
  face. The load path is the other side: the sleeve's hole is deliberately asymmetric in X
  (HOLE_CLR_X_LOAD 0.25 at HOLE_X0 = 3.95, HOLE_CLR_X_FREE 0.50 at HOLE_X1 = 9.70), and
  pulling the drawer drives the blade against the hole's -X wall, so the blade's -X face is
  what bears. That face has 1.25 x 10.0mm of flat material anyway and could not hold this
  mark even if it were free. +X carries no load at all — the +X direction is dead-stopped by
  the drawer's own rear face against the cavity, which is why its clearance could be opened
  to 0.50 in the first place — and its only contact is the detent bump above.
  Measured on the real flat material at each face plane, not the bounding box, which lies on
  a stepped part: +X 30.50 x 7.00, -Z 6.97 x 18.00, +Z 5.16 x 18.00, -X 1.25 x 10.00, the
  two ends 4.13 x 6.75. +X is the only face on this part that can hold a version AND a date.
  That 30.50 is ALREADY the free rectangle, not the whole face: engrave() measures the
  largest rectangle of material really at the face plane, and the dimples push that
  measurement's -Y edge out to y = 23.40, past the OPEN dimple's rim. The mark centres in it
  at y = 38.65, which puts its near end at y = 25.22 — 1.12mm clear of the swept band's
  24.10 and 1.83mm clear of the OPEN dimple's rim. Those are the numbers the new guard
  checks, and it computes them from the fin, not from this paragraph.

THE MARK ITSELF — same font, same floor, more string
  DejaVu Sans Mono Bold, and the cap derived the way v8.7 derived it: start at 3.00mm and
  step up 0.1 at a time until the MEASURED stroke on the meshed glyph clears watermark's
  MIN_STROKE_DEBOSS_MM. In this face 3.00mm already draws 0.522mm, so the cap is 3.00 — the
  same cap and the same ink as v8.7, which is the point. The letters do not change; only the
  string does. "v8.8 15ag26" at that cap measures 26.87 x 3.91mm, unrotated: the face's long
  axis IS the bolt axis, so unlike the pad this needs no 90deg rotation to read along the
  part.
  Headroom, stated so the next version knows what this face has left: 27.10mm of string
  before the band guard fires, and 28.50mm before engrave's own 1.0mm margin check does. The
  band binds first, and it binds at a 3.03mm cap — 0.03 above the one we ship. That is thin,
  and it is the honest state of this face: big enough for a version and a date at a legible
  stroke, and not much bigger.
  REJECTED: growing the cap to fill the flat rectangle. A 3.18mm cap fits it (28.48 of
  28.50) but leaves the mark's near end 0.31mm from the swept band, and even 3.10mm leaves
  only 0.67 — both well inside MARK_BAND_CLR, and 3.10 is one of the perturbations the guard
  was proved red against. The legibility floor sets the cap and the band sets the limit;
  nothing on this face is sized by eye.

DEPTH: 0.5mm, NOT v8.7's 0.6 — because this face is VERTICAL in the print pose
  The bolt is never rotated by pose(), so -Z was the plate and +X is a side wall. v8.7 went
  to 0.6mm for one specific reason that does not apply here: the marked land was the FIRST
  LAYER, and first-layer squish partly fills a shallow recess, so it wanted three layers of
  depth rather than two. On a vertical wall there is no squish and no elephant foot, and the
  recess is not layers of floor at all — it is a notch the outer perimeter detours into,
  once per layer, all the way up each glyph. What governs it is EXTRUSION WIDTH, not layer
  height. 0.5mm makes the groove roughly square in section against its own 0.522mm stroke: a
  0.42mm nozzle can enter a 0.52mm groove, and at 1:1 it can trace both flanks without the
  two passes colliding and over-filling the letter shut. Deeper buys no more shadow on a
  vertical face and starts to make a slot the nozzle smears rather than traces; it also
  removes more of a 5.0mm blade. 0.5 is watermark's own DEFAULT_DEPTH_MM and well over its
  MIN_DEPTH_MM of 0.4, and the build asserts the latter.
  Cost, re-measured on this build rather than assumed: printcheck reads 66.19mm2 of overhang
  on the unmarked v8.5 bolt, 86.25 on v8.6, 82.17 on v8.7 and 90.75 here. This mark costs
  24.56mm2 where v8.7's cost 15.98 — not because it is deeper, it is shallower, but because
  it is 11 glyphs instead of 4. On a vertical face the recess's entire overhang is the
  MARK_DEPTH ledge along the top of each glyph, and 0.5mm of unsupported horizontal per
  letter is not a bridge in any meaningful sense. The verdict stays warn, as it has since
  v8.6, and the part is still 0 non-manifold edges.
  Reported rather than papered over: the EXACT boolean leaves one sliver triangle of under
  1e-6 mm2 in 8826 (v8.6's four-glyph mark left four, and shipped). The mesh is closed, every
  slicer drops zero-area faces, and a cleanup pass to remove it would be a mesh edit this
  version has no licence to make — the frozen-mesh guard exists precisely to stop those.

The product, not a coupon. Sleeve + drawer + bolt, back at the SPEC's thin credit-card
geometry, carrying the lock the v7.1 -> v7.4 coupons converged on.

Everything is modelled in ONE assembly frame so the fit arithmetic is provable, then each
part is rotated/translated into its print pose. Assembly frame:

    X  0..86   travel axis. Sleeve open face at X=0, closed rear at X=86. Drawer exits -X.
    Y  0..54   width. The bolt travels along +Y to lock.
    Z  0..19   height.

CARRIED OVER FROM v7.4 UNCHANGED (validated by hand, not redesigned)
  - Blade bolt cross-section 5.0 (X) x 10.0 (Z). Sliding clearance was 0.25mm/face on the
    coupons; v8.5 opens it to 0.30 because the printed v8.0 was still tight in the hand.
  - Detent in the HOUSING (v7.3): a 1.0 x 15mm cantilever fin in the drawer's front block,
    into two dimples in the bolt's back face — LOCKED 0.7, OPEN 0.45. Fin deflection at
    the crossover is 0.25mm, the low-strain number v7.3's FEA sized, and v8.5 holds it
    there by growing the bump 0.75 -> 0.85 proud to span the wider clearance.
  - The fin prints as a plain vertical wall off the bed, its relief slot open through the
    underside of the front block. Never a horizontal cantilever over air.
  - Thumb PAD, not a thumbnail tab: FULL bolt height, 2.5mm proud, all as vertical ribs so
    the bolt slices bridge-free. v8.5 lengthens it 14 -> 18mm along Y with 5 ridges.
  - Bolt tip FLUSH at LOCKED — in v8.5, flush with the sleeve's plain 54.0 outer face.
    Flush reads as locked by fingertip, the empty counterbored recess reads as open,
    nothing protrudes to be knocked back.

THE BRIDGE-DROOP FIX (operator photo of the v7.4 coupon: sagged strands inside the slide
channel — bridge droop, not stringing). Three changes, all reported with spans below:
  1. The blade's long edges are chamfered 2.0 (front pair) and 2.5 (back top) at 45deg.
     That is what BUYS the housing its chamfers: the channel roof's inside corners can
     only be filled to within one clearance (0.30) of the blade.
  2. The channel's upper inside corners are chamfered 2.15 (front) and 2.65 (back), so the
     flat span narrows from 5.6mm to 0.80mm before it ever bridges.
  3. The fin relief and the thumb-pad slot no longer overlap in Y. Overlapped (the naive
     layout) they strip the channel roof of support from BOTH sides and it spans 9.45mm.
     Separated, the worst span in the drawer is 4.45mm. Separation costs bolt length: the
     bump must stay under the blade at both positions. That cost is a benefit — see the
     guide-length note below; the blade is 45.0mm.
  4. v8.5 GABLES the bore roof. Chamfering the two upper corners and leaving a flat crown
     between them was not enough: the camera caught that crown drooping loops into the pad
     slot mid-print, the same cruft the operator hand-trimmed off v8.0. So the two 45deg
     planes are no longer truncated — they run on until they meet at a ridge, and the flat
     crown ceases to exist. Because they are the SAME planes, blade clearance is untouched
     at 0.318. The fin relief is roofed by the back plane carried down to the block's rear
     wall rather than by a flat cap, which also deletes the cap's own 2.5mm bridge; the
     cost is a shorter fin (see report()). The one region that CANNOT be gabled is the run
     over the pad slot, and report() shows the arithmetic for why.

THE TWO OPERATOR REQUESTS
  1. "Less curve if it lets the mechanism operate more cleanly" -> SPEC's ~1.5mm outer
     radius becomes a 0.5mm chamfer (EDGE_BREAK). No curvature eating engagement depth
     around the hole or the boss.
  2. "Slightly bevel peg edges to ease fit" -> the blade's 0.5mm all-edge chamfer is
     applied to the plain box BEFORE the pad/dimple booleans (bevelling after boolean cuts
     is the order that breaks), the corner wedges add 2.0-2.5mm of lead-in on the tip, and
     the sleeve hole gets a 0.6mm-deep, 0.8mm-oversize entry counterbore on the face the
     bolt enters. Capture range for this blind, by-feel mate is ~2mm of misalignment. It
     doubles as string tolerance: a channel that prints imperfect still lets the bolt seat.

DELIBERATE DEVIATIONS FROM SPEC.md — all of them
  - Sleeve roof/floor 1.4mm (SPEC 1.1), side walls 1.8mm (SPEC 1.7). ~3 and ~4 perimeters
    at 0.42mm width, so the walls are solid perimeter. 1.1mm is 2.6 perimeters, ragged.
  - 0.5mm chamfer instead of a 1.5mm (sleeve) / 1.2mm (drawer) radius. Request 1 above.
  - Drawer BODY 81.80 x 48.90 x 15.55 (SPEC "approximately 82 x 50.2 x 15.0"). DERIVED
    from the cavity and the tightened clearances (0.15 each side, 0.20 below, 0.45 to the
    ceiling); the length falls out of the front-block depth the mechanism needs, and the
    width is 1.2 narrower than SPEC because the lock wall is 3.0 rather than 1.7. The
    printed part measures 17.40 tall because the grip knob rises into the roof notch.
  - The +Y wall is 3.0mm where SPEC says 1.7. It has to be: it is the wall the bolt
    engages, and 3.0 is the engagement depth the coupons validated. v8.3 got there with a
    pad bolted to the outside, which stood 1.2 proud and was the operator's last
    complaint; v8.5 takes the 1.2 out of the cavity instead so the outer face is dead
    flat. The box's widest point is therefore exactly 54.0, asserted on the mesh.
  - Sleeve bolt hole is ASYMMETRIC in X — 0.25/face on the loaded side, 0.50 on the side
    the rear stop covers — and 0.30/face in Z. See report()'s free-play table.
  - The sleeve roof is interrupted at the mouth by the 21mm grip notch, leaving two 16.5mm
    strips of roof either side of it. The side walls carry the mouth, not the roof.
  - Thumb pad crowns sit 1.2mm behind the sleeve rim rather than flush. That distance is
    the retention ligament between the bolt hole and the open face — at flush it would be
    gone and the hole's print-ceiling chamfer would eat what remained.
  - v8.4: ALL fits were signed off by hand on the v8.3 prints. Its only change was
    deleting the proud boss; every clearance, the detent, the stroke, the dock and the
    gable carried over untouched, re-anchored to the new wall.
  - v8.5 IS A BOLT-ONLY REPRINT. The v8.4 drawer and sleeve are printed and immutable, so
    ONLY bolt parameters differ and a guard block asserts every housing dimension is
    untouched. v8.4's missing LOCKED stop was confirmed in the hand: the soft click did
    not arrest the thumb, the push ran on until the pad met the sleeve wall 3.70 past
    design-LOCKED, and the tip stood well proud. v8.5 stops fighting that and adopts it —
    LOCKED is now DEFINED as the pad bearing on the wall, the blade is re-cut so the tip
    lands 0.40 proud there (a bump you can feel, too small to snag), and the LOCKED dimple
    moves to that same position so click and hard stop finally agree. Stroke falls out at
    5.40. The one thing surrendered is v8.3's inboard stroke: the pad now finishes ON the
    wall, which is precisely what makes LOCKED unmistakable.
    Bonus that fell out of keeping the blade at 44.0: at OPEN the tail is 0.50 off the
    bore's closed end, so THAT end is hard-stopped too. The bolt is now positively
    arrested in both directions for the first time since v8.2.

DELIBERATELY OMITTED — noted, not silently dropped
  - SPEC's exterior stiffening beads, the ceiling microtexture field, and the
    compartment-floor microtexture.
  - SPEC's three friction detents and their sleeve receivers. The bolt is v8.5's
    retention; the friction detents are what it replaces. Re-adding them is its own pass.

WHAT CHANGED FROM v8.0 (operator printed it, trimmed and sanded it, and hand-tested it)
  1. THE FRONT PULL FAILED. v8.0 tried a pull on the drawer's front face — first opposed
     perimeter ledges, then one centred tab flush with the sleeve rim. In the hand neither
     works: the drawer seats so deep in the mouth that a face-mounted pull has nothing
     standing out to catch, no matter how far forward it reaches. The pull moves to the
     TOP, and the front face returns to flat except the pad slot.
     A U-shaped notch is cut through the sleeve roof at the open end and the drawer grows
     a knob that rides in it; push the knob toward the mouth and the drawer follows. The
     knob is 2.0mm tall — exactly the 0.60 ceiling gap plus the 1.4 roof — so its top is
     FLUSH with the sleeve's outer roof and nothing stands proud of the closed box. Its
     traction ridges are formed by cutting grooves, so their crowns are flush too.
     The notch is a true U (straight slot ending in a semicircle), because the roof is only
     1.4mm thick and a square inside corner there is a stress raiser. The knob's arc shares
     the notch's centre, so clearance is a uniform 0.30 all the way round, and withdrawing
     moves the two arc centres apart — clearance only ever grows. Legibility comes free:
     knob against the round end of the notch means shut.
  2. THE BOLT WAS STILL TIGHT. Every sliding clearance goes 0.25 -> 0.30 per face: the
     bore, the pad slot, and the sleeve hole (whose X clearance keeps its extra tolerance
     allowance, 0.40 -> 0.45). The detent is preserved by growing the fin bump 0.75 ->
     0.85 proud — 0.10, not 0.05, because widening CLR moves the channel's back wall AND
     the fin's standoff behind it, two 0.05 steps. Interference stays 0.25, fin deflection
     stays 0.25, and report() computes both rather than asserting them.
  v8.5 (hand test of the printed v8.1, carrying v8.2's gable forward):
  A. THE STROKE MOVES INBOARD. The pad used to finish flush against the drawer's +Y edge,
     which put the thumb hard against the sleeve wall at the end of every lock. It now
     ends 3.50 short of that edge and starts just left of face centre. Raising
     PAD_TIP_GAP walks the pad along the blade; the fin FLIPS its anchored edge so the
     bump can follow the pad -Y without the LOCKED dimple running off the blade's tail.
     The cost is stated in report(): the sleeve wall no longer backstops LOCKED at 0.40,
     it is 3.70 away, so LOCKED is detent-held. The slot's +Y mouth is the only way the
     pad can be installed, so the slot itself cannot supply that stop.
  B. INSET 3.20 -> 2.40 AND A ZERO-SLACK DOCK. The whole bolt/pad column shifts 0.80
     toward the mouth rather than the front wall thickening, which keeps the pad's
     prominence and keeps the un-gableable bore-roof span at 4.45 instead of widening it.
     The knob's arc centre nudges 0.20 forward so it nests 0.10 from the notch's round
     end while its flanks stay at 0.30. Fully-closed is still defined by the rear face
     bottoming out; the dock backs it up 0.10 behind, and report() argues why that way
     round.
  C. LOCKED WIGGLE. Side 0.20 -> 0.15, ceiling 0.60 -> 0.45, and the sleeve hole's X
     clearance goes ASYMMETRIC — 0.25 on the face that actually bears when you pull the
     drawer, 0.50 on the face the rear stop already covers. Free play per axis is
     tabulated in report(). The bore's own 0.30 is untouched.
  3. THE THUMB PAD IS LONGER: 14 -> 18mm along Y with 5 ridges instead of 4, still full
     bolt height and 2.5 proud. The pad slot grew with it, which pushed the fin relief
     -Y to keep relief and slot from overlapping — that separation is what keeps the bore
     roof supported — and the blade grew 44 -> 45mm to keep the detent dimples off its
     tail. Travel is still 5.00 and every clearance above is unchanged by this.

BORE, PAD SLOT AND ASSEMBLY (musket load)
  The bore is CLOSED all round the shaft — a rectangular hole through the drawer's front
  block, stopped at Y=4.5 and opening only through the drawer's +Y side wall where the
  bolt must exit into the sleeve. The one deliberate opening is the PAD SLOT: the thumb
  pad rides on the bolt and has to protrude through the drawer's front face and slide with
  it, so the front wall carries a Y-running slot over the pad's whole travel. That slot is
  closed at its -Y end (the OPEN hard stop) and open at its +Y mouth, which is also the
  insertion path: the bolt is musket-loaded tail-first through the side-wall bore with the
  pad entering the mouth, once, at assembly.
  The bolt is NOT permanently captured and is not meant to be. The detent fin holds it in
  whichever dimple it is sitting in, the pad slot stops it at OPEN, and the sleeve's +Y
  inner wall stops it 0.4mm past LOCKED once the drawer is in the sleeve. Pull the drawer
  right out and the bolt can be deliberately slid back out the way it went in — that is
  the cleaning and replacement path, not a defect.
  Closing the bore is what buys the guide length: 40.8mm of shaft stays inside the drawer
  at LOCKED against a 5.0mm shaft thickness, an 8.2:1 guide ratio. That, not clearance, is
  what kills the residual wiggle the operator could still feel on the coupons.

Print: all three are posed supportless, but v8.8's DEFAULT PLATE IS THE BOLT ALONE — it is
the only part that changes, and the housing in the operator's hand is the same v8.4 drawer
and sleeve this script would re-emit byte for byte, so "slice v8.8" reprints exactly what is
new and nothing else. All three parts are still built (the housing carries the fit arithmetic
and the mesh envelope assert) and any one of them is still exportable with --only.
Poses, unchanged: sleeve stands on its closed rear end (86mm tall, open face up) as
print/prepare_supportless_plate.py posed v1 — laid flat it would bridge the whole roof.
Drawer bottom-down. Bolt standing, pad as a vertical rib; the marked face is a
vertical side wall on this plate, not the first layer. PETG,
supports=off, orient=off, brim on (the bolt's footprint is ~175mm2).

Usage:  blender -b --factory-startup --python design_v8_8_pillbox.py [-- --only Bolt]
Writes: print/v8_8_pillbox_plate.stl — the marked bolt (or print/v8_8_pillbox_<part>.stl
        with --only, which still builds and exports the drawer or the sleeve on demand)
Needs:  the printfarm watermark helper, found via PRINTFARM_SRC (default ~/code/printfarm/src)
"""
import os
import sys
from math import radians

import bpy

_argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ONLY = _argv[_argv.index("--only") + 1] if "--only" in _argv else None

SQ2 = 2 ** -0.5

# --- sleeve shell (mm) -------------------------------------------------------------
BOX_X, BOX_Y, BOX_Z = 86.0, 54.0, 19.0
WALL_SIDE, WALL_FACE, WALL_REAR = 1.8, 1.4, 1.8
# v8.5: the +Y wall carries the lock, so it is a uniform 3.0mm for its whole area. v8.3
# got that 3.0 by bolting a pad onto a 1.8 wall, which stood 1.2 proud of the box and was
# the operator's last complaint. Now the 1.2 comes out of the CAVITY instead: the outer
# face stays dead flat at exactly BOX_Y and nothing protrudes anywhere.
WALL_LOCK = 3.0
EDGE_BREAK = 0.5
CAV_X1 = BOX_X - WALL_REAR                             # 84.20
CAV_Y0, CAV_Y1 = WALL_SIDE, BOX_Y - WALL_LOCK          # 1.80 .. 51.00
CAV_Z0, CAV_Z1 = WALL_FACE, BOX_Z - WALL_FACE          # 1.40 .. 17.60

# --- drawer, DERIVED from the cavity + SPEC clearances -----------------------------
# v8.5 anti-wiggle: side 0.20 -> 0.15, ceiling 0.60 -> 0.45. The floor stays 0.20 — the
# drawer rides on it, and that is the one face where a tight fit costs stiction rather
# than buying rigidity.
CLR_SIDE, CLR_BELOW, CLR_ABOVE = 0.15, 0.20, 0.45
DR_Y0, DR_Y1 = CAV_Y0 + CLR_SIDE, CAV_Y1 - CLR_SIDE    # 2.00 .. 52.00
DR_Z0, DR_Z1 = CAV_Z0 + CLR_BELOW, CAV_Z1 - CLR_ABOVE  # 1.60 .. 17.00
DR_WALL, DR_DIV, DR_FLOOR = 1.5, 1.2, 1.2
N_COMPARTMENTS = 3

# --- bolt + channel, X chain from the thumb ridges backwards -----------------------
CLR = 0.30                                             # v8.5: 0.25 -> 0.30, still tight
BOLT_T, BOLT_H = 5.0, 10.0
# v8.5 BOLT-ONLY REPRINT. The drawer and sleeve are printed and FIXED as v8.4 built them;
# every housing number below is frozen and re-asserted at the bottom of this block.
# v8.4 shipped with no hard stop at LOCKED — the soft detent click did not arrest the
# thumb, so the push carried on until the pad fetched up against the sleeve wall 3.70
# past design-LOCKED and the tip stood well proud. Rather than fight that, v8.5 ADOPTS it:
# the pad on the wall IS locked. The blade is re-cut around that stop and the detent is
# moved to agree with it, so the click and the wall now say the same thing.
TRAVEL = 5.40                                          # falls out of the new stop, see below
PAD_PROUD, PAD_L = 2.5, 18.0                           # v8.5: 14 -> 18 along Y
RIDGE_P, RIDGE_W, RIDGE_N = 0.5, 1.2, 5                # v8.5: 4 -> 5 ridges
# PAD_TIP_GAP is the pad's +Y end to the blade tip. With LOCKED redefined as "pad against
# the sleeve wall at CAV_Y1", this distance alone sets where the tip ends up, so it is
# simply wall-to-tip: CAV_Y1 + PAD_TIP_GAP = BOX_Y + TIP_PROUD. v8.4's inboard stroke is
# deliberately surrendered here — the pad now finishes ON the wall, which is exactly what
# makes LOCKED unmistakable to the thumb.
TIP_PROUD = 0.40                                       # tactile "locked" bump, too small to snag
PAD_TIP_GAP = (BOX_Y + TIP_PROUD) - (BOX_Y - WALL_LOCK)  # 3.40
RIDGE_X0 = 1.2                                         # v8.5: 2.0 -> 1.2, see DR_X0 below
PAD_X0 = RIDGE_X0 + RIDGE_P                            # 2.50
BOLT_X0 = PAD_X0 + PAD_PROUD                           # 5.00
BOLT_X1 = BOLT_X0 + BOLT_T                             # 10.00
CH_X0, CH_X1 = BOLT_X0 - CLR, BOLT_X1 + CLR            # 4.75 .. 10.25
# v8.5 shallower inset: the whole bolt/pad column moved 0.80 toward the mouth via
# RIDGE_X0, walking the drawer's front face from 3.20 to 2.40 — a 25% shallower curtain
# wall — WITHOUT thickening the front wall. Thickening it instead would have pushed DR_X0
# forward while leaving the pad where it was, cutting the pad's prominence above the face
# from 1.20 to 0.40 (unpushable) and widening the un-gableable bore-roof span by the same
# 0.80. Moving the column keeps both, and brings the thumb ridges 0.80 nearer the rim.
DR_X0 = CH_X0 - DR_WALL                                # 2.40  drawer front face
DR_X1 = CAV_X1                                         # 84.20 rear face = closed stop
DR_L = DR_X1 - DR_X0                                   # 81.80

FIN_T, FIN_FREE, FIN_LEN = 1.0, 1.2, 15.0
FIN_X0 = CH_X1 + CLR                                   # 10.50
FIN_X1 = FIN_X0 + FIN_T                                # 11.50
RELIEF_X1 = FIN_X1 + FIN_FREE                          # 12.70
FB_X1 = RELIEF_X1 + DR_WALL                            # 14.20 front block rear face

BOLT_Z0 = DR_Z0 + (DR_Z1 - DR_Z0 - BOLT_H) / 2         # 4.30
BOLT_Z1 = BOLT_Z0 + BOLT_H                             # 14.30
CH_Z0, CH_Z1 = BOLT_Z0 - CLR, BOLT_Z1 + CLR            # 4.05 .. 14.55
ZC = (BOLT_Z0 + BOLT_Z1) / 2                           # 9.30

# 45deg corner chamfers. The blade's set the ceiling for the housing's: parallel 45deg
# planes must stay >= CLR apart, i.e. housing_leg <= blade_leg + (housing corner offset).
BLADE_FT, BLADE_FB, BLADE_BT = 2.0, 2.0, 2.5           # front-top, front-bottom, back-top
CHAN_CF, CHAN_CB = 2.15, 2.65                          # channel roof: front, back corners
# v8.5 GABLE. v8.1 chamfered the bore roof's two upper corners and left a flat crown
# between them; on the printer that crown drooped loops into the pad slot. The fix is to
# stop truncating: run those SAME two 45deg planes on until they meet, and the flat crown
# becomes a ridge. Same planes means the blade clearance is untouched — still 0.318, above
# the 0.30 minimum — and the ridge lands well under the drawer's top surface.
GABLE_F = CH_Z1 - CHAN_CF - CH_X0                      # 7.75  front plane: z - x = this
GABLE_B = CH_X1 + CH_Z1 - CHAN_CB                      # 22.25 back plane:  x + z = this
RIDGE_Z = (GABLE_F + GABLE_B) / 2                      # 15.00
RIDGE_X = RIDGE_Z - GABLE_F                            # 7.25
GABLE_LEG_F = RIDGE_Z - CH_X0 - GABLE_F                # 2.55 leg from the corner at RIDGE_Z
GABLE_LEG_B = CH_X1 + RIDGE_Z - GABLE_B                # 3.05

# --- Y chain -----------------------------------------------------------------------
TIP_LOCKED = BOX_Y + TIP_PROUD                         # 54.40, 0.40 proud by design
TIP_OPEN = TIP_LOCKED - TRAVEL                         # 50.20 vs drawer inner wall 50.50
# v8.5: 45.0 -> 44.0. The +Y side of the whole stack moved 1.20 inboard with the cavity,
# but the -Y side did not, so a 45mm blade would push its tail past the bore's closed end
# and into the drawer's -Y wall. One millimetre off the blade restores the margin.
BOLT_L = 44.0                                          # guide length, not travel: see report
TAIL_LOCKED = TIP_LOCKED - BOLT_L                      # 10.20
CH_Y0 = 4.5                                            # closed bore end, 1.0 of -Y wall left
CH_Y1 = DR_Y1 + 0.1                                    # bores through the +Y side wall

PAD_Y1_LOCKED = TIP_LOCKED - PAD_TIP_GAP               # 51.80
PAD_Y0_LOCKED = PAD_Y1_LOCKED - PAD_L                  # 37.80
# FROZEN: the slot is cut in the printed drawer. In v8.4 it derived from the pad position
# and travel; both of those move in v8.5, so it is pinned to what v8.4 actually built.
SLOT_Y0 = 24.10
SLOT_Y1 = CH_Y1
SLOT_X0, SLOT_X1 = DR_X0 - 0.1, CH_X0 + 0.05

# --- TOP grip: U notch in the sleeve roof + knob on the drawer's top ----------------
# v8.0 put the pull on the drawer's front face. In the hand it failed outright: the drawer
# seats so deep in the mouth that even a tab flush with the rim leaves nothing to grab.
# The pull moves to the TOP, where there is real estate no recess can swallow. A U-shaped
# notch is cut through the sleeve roof at the open end, and the drawer grows a knob that
# rides in it. Push the knob toward the mouth and the drawer comes with it.
# Height budget: the knob starts at the drawer's top plane and rises to the sleeve's OUTER
# roof plane — the 0.60 ceiling gap plus the 1.4 roof = exactly 2.0mm — so it is flush
# with the closed box and nothing stands proud.
# The notch is a true U: a straight slot from the mouth ending in a semicircle, so the
# 1.4mm roof has no re-entrant corner anywhere to raise stress.
# Legibility comes free: knob against the notch's round end = shut.
NOTCH_W = 21.0
NOTCH_R = NOTCH_W / 2                                  # 10.50 semicircular end
NOTCH_D = 13.0                                         # depth in X from the mouth
NOTCH_CX = NOTCH_D - NOTCH_R                           # 2.50 arc centre
NOTCH_YC = (DR_Y0 + DR_Y1) / 2                         # 27.00 centred on the drawer
NOTCH_Y0, NOTCH_Y1 = NOTCH_YC - NOTCH_R, NOTCH_YC + NOTCH_R
KNOB_CLR = 0.30
KNOB_R = NOTCH_R - KNOB_CLR                            # 10.20
# v8.5 ZERO-SLACK DOCK. v8.2 shared the notch's arc centre, so the knob sat 0.30 shy of
# the notch's round end and the closed drawer showed a visible gap behind it. Nudging the
# knob's arc centre 0.20 FORWARD closes the dock to 0.10 while the flanks stay at 0.30:
# at the knob's widest the notch measures sqrt(NOTCH_R^2 - e^2) = 10.498 against the knob's
# 10.20. Same radius, same notch, one offset — the dock tightens and the slide does not.
KNOB_E = 0.20                                          # arc-centre offset toward +X
KNOB_CX = NOTCH_CX + KNOB_E                            # 2.70
KNOB_X1 = KNOB_CX + KNOB_R                             # 12.90, i.e. 0.10 shy of NOTCH_D
KNOB_Z1 = BOX_Z                                        # 19.00 flush with the outer roof
KNOB_CHAMFER = 0.4
GROOVE_R, GROOVE_D, GROOVE_N = 0.6, 0.5, 4             # crowns stay flush at KNOB_Z1

# v8.5: moving the stroke inboard drags the pad slot's -Y end down to 25.30, so the fin
# relief follows it -Y to preserve the no-overlap separation the gable depends on. The fin
# also FLIPS: it is now anchored at its -Y edge and free at its +Y edge, putting the bump
# at 18.30 instead of down near 14.60. Without the flip the bump would sit so close to the
# blade's tail that the LOCKED dimple would break out of the end of the blade.
RELIEF_Y0 = 5.1                                        # v8.5: follows the slot 1.2 inboard
# v8.5: the relief's flat cap is gone. Its ceiling is now the bore's own back gable plane
# carried on down to the block's rear wall, so the relief and the bore share one unbroken
# 45deg surface that grows out of solid material instead of bridging across it.
RELIEF_Z1 = GABLE_B - RELIEF_X1                        # 9.55 where that plane lands
FIN_Y0 = RELIEF_Y0                                     # 6.30  anchored edge (flipped)
FIN_Y1 = FIN_Y0 + FIN_LEN                              # 21.30 free edge
RELIEF_Y1 = FIN_Y1 + 2.0                               # 23.30 relief runs past the free end
FIN_Z1 = GABLE_B - FIN_X1 - 0.35                       # 10.40, under the gable at its back
# BUMP_PROUD grows 0.10, not 0.05: widening CLR moves the channel wall AND the fin's
# standoff behind it, so the bump has two 0.05 steps to make up. Interference is then
# unchanged at 0.25 — see report(), which computes it rather than asserting it.
BUMP_Y, BUMP_R, BUMP_PROUD = FIN_Y1 - 3.0, 1.1, 0.85   # 18.30, near the flipped free end
DIMPLE_R = 1.1
DIMPLE_LOCK_D, DIMPLE_OPEN_D = 0.7, 0.45
DIMPLE_LOCK_Y = BUMP_Y                                 # bolt is modelled at LOCKED
DIMPLE_OPEN_Y = BUMP_Y + TRAVEL

# --- lock boss + hole --------------------------------------------------------------
# v8.5: no boss. There is nothing to add to the outside of the +Y wall any more — the wall
# IS 3.0 thick everywhere — so BOSS_X/Z/CHAMFER are gone along with their 45deg blend ramp.
# v8.5 ASYMMETRIC hole in X. Only ONE of the hole's two X faces is ever loaded: pull the
# drawer and the blade bears on the -X face. The +X direction is stopped dead by the rear
# wall, so clearance on that side costs nothing and buys mating tolerance. So the load
# face tightens to 0.25 while the free face opens to 0.50 — total width is barely changed,
# so the blade still enters as easily, but the felt rattle halves on the side you feel it.
HOLE_CLR_X_LOAD, HOLE_CLR_X_FREE = 0.25, 0.50
HOLE_CLR_Z = 0.30
HOLE_X0 = BOLT_X0 - HOLE_CLR_X_LOAD                    # 3.95  the face that bears
HOLE_X1 = BOLT_X1 + HOLE_CLR_X_FREE                    # 9.70
HOLE_Z0, HOLE_Z1 = BOLT_Z0 - HOLE_CLR_Z, BOLT_Z1 + HOLE_CLR_Z
HOLE_CH = 2.10                                         # print-ceiling corners of the hole
CBORE_D, CBORE_OVER, CBORE_CH = 0.6, 0.4, 2.6

PLATE_LIMIT, PART_GAP = 115.0, 12.0

# --- v8.8 guards -------------------------------------------------------------------
# FROZEN HOUSING. The drawer and sleeve are already printed. Every number here is what
# v8.4 actually built; if a bolt edit ever perturbs one of them, this stops the build
# rather than quietly producing a bolt for a box that does not exist.
for _name, _got, _want in [
    ("BOX_Y", BOX_Y, 54.00), ("CAV_Y1", CAV_Y1, 51.00),
    ("DR_Y1", DR_Y1, 50.85), ("drawer wall inner", DR_Y1 - DR_WALL, 49.35),
    ("CH_Y0", CH_Y0, 4.50), ("CH_Y1", CH_Y1, 50.95), ("SLOT_Y0", SLOT_Y0, 24.10),
    ("BUMP_Y", BUMP_Y, 17.10), ("BUMP_PROUD", BUMP_PROUD, 0.85),
    ("FIN_X0", FIN_X0, 9.80), ("DR_X0", DR_X0, 2.40),
    ("BOLT_X0", BOLT_X0, 4.20), ("BOLT_X1", BOLT_X1, 9.20),
    ("BOLT_Z0", BOLT_Z0, 4.375), ("BOLT_Z1", BOLT_Z1, 14.375),
    ("CH_X0", CH_X0, 3.90), ("CH_X1", CH_X1, 9.50),
    ("CH_Z0", CH_Z0, 4.075), ("CH_Z1", CH_Z1, 14.675),
    ("PAD_X0", PAD_X0, 1.70), ("PAD_L", PAD_L, 18.0), ("CLR", CLR, 0.30),
]:
    if abs(_got - _want) > 1e-6:
        raise SystemExit(f"v8.8: FROZEN housing value {_name} is {_got}, must stay {_want}")

# BOLT sanity, the three the directive named plus the margins they depend on.
_TAIL_OPEN = TIP_OPEN - BOLT_L
_PAD_Y0_OPEN = PAD_Y0_LOCKED - TRAVEL
if abs(TIP_LOCKED - 54.40) > 0.05:
    raise SystemExit(f"v8.8: tip at LOCKED {TIP_LOCKED:.3f}, must be 54.40 +/-0.05")
if TIP_OPEN > 49.05:
    raise SystemExit(f"v8.8: tip at OPEN {TIP_OPEN:.3f}, must be <= 49.05")
if abs((DIMPLE_OPEN_Y - DIMPLE_LOCK_Y) - TRAVEL) > 1e-9:
    raise SystemExit("v8.8: dimple spacing must equal the stroke")
if abs(PAD_Y1_LOCKED - CAV_Y1) > 1e-6:
    raise SystemExit(f"v8.8: pad at LOCKED ends {PAD_Y1_LOCKED:.3f}, must bear on"
                     f" the sleeve wall at {CAV_Y1:.3f}")
if _TAIL_OPEN < CH_Y0 + 0.5:
    raise SystemExit(f"v8.8: tail at OPEN {_TAIL_OPEN:.3f} is under 0.5 clear of the"
                     f" bore end {CH_Y0:.2f}")
if _PAD_Y0_OPEN < SLOT_Y0 or PAD_Y1_LOCKED - TRAVEL > SLOT_Y1:
    raise SystemExit("v8.8: pad leaves its slot somewhere in the stroke")
if DIMPLE_LOCK_Y - _TAIL_OPEN < 2.5:
    raise SystemExit("v8.8: LOCKED dimple too near the blade tail")


def box(name, x0, x1, y0, y1, z0, z1):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object
    o.name = name
    o.dimensions = (x1 - x0, y1 - y0, z1 - z0)
    o.location = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def sphere(name, x, y, z, r):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, y, z), segments=32,
                                         ring_count=16)
    o = bpy.context.object
    o.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def _solo(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o


def wedge(name, cx, cz, sx, sz, leg, y0, y1, size=180.0):
    """A 45deg corner-trimming solid for the X-Z plane, running along Y.

    Trims the corner at (cx, cz) with legs of `leg`; (sx, sz) are each +-1 and point out
    of the material that survives. Used on plain boxes only, never after a boolean.
    """
    px, pz = cx - sx * leg / 2, cz - sz * leg / 2
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object
    o.name = name
    o.dimensions = (size, y1 - y0, size)
    bpy.ops.object.transform_apply(scale=True)
    o.rotation_euler = (0.0, radians(-45.0), 0.0)
    o.location = (px + sx * SQ2 * size / 2, (y0 + y1) / 2, pz + sz * SQ2 * size / 2)
    _solo(o)
    bpy.ops.object.transform_apply(location=True, rotation=True)
    return o


def cylinder_y(name, x, z, r, y0, y1):
    """A Y-axis cylinder — used to cut rounded grooves, so the ridges between them are
    rounded crowns flush with the surface rather than raised bars."""
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=y1 - y0, vertices=32,
                                        location=(x, (y0 + y1) / 2, z),
                                        rotation=(radians(90.0), 0.0, 0.0))
    o = bpy.context.object
    o.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def cylinder_z(name, x, y, z0, z1, r):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=z1 - z0, vertices=64,
                                        location=(x, y, (z0 + z1) / 2))
    o = bpy.context.object
    o.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def cone_z(name, x, y, z0, z1, r0, r1):
    """Truncated cone — the knob's top edge break. Built as geometry rather than a bevel
    modifier because the knob is already a boolean result by then."""
    bpy.ops.mesh.primitive_cone_add(radius1=r0, radius2=r1, depth=z1 - z0, vertices=64,
                                    location=(x, y, (z0 + z1) / 2))
    o = bpy.context.object
    o.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def combine(target, tool, op):
    m = target.modifiers.new(op.lower(), "BOOLEAN")
    m.operation = op
    m.object = tool
    m.solver = "EXACT"
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(tool, do_unlink=True)
    return target


def bevel(o, width, segments=1):
    """Chamfer every hard edge. Always called on a plain box, BEFORE any boolean."""
    m = o.modifiers.new("bevel", "BEVEL")
    m.width = width
    m.segments = segments
    m.limit_method = "ANGLE"
    m.angle_limit = radians(30.0)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def extents(o):
    c = o.bound_box
    return [(min(v[i] for v in c), max(v[i] for v in c)) for i in range(3)]


def pose(o, rot_y):
    o.rotation_euler = (0.0, radians(rot_y), 0.0)
    _solo(o)
    bpy.ops.object.transform_apply(rotation=True)
    return o


def place(o, cx, cy):
    (x0, x1), (y0, y1), (z0, _) = extents(o)
    o.location = (cx - (x0 + x1) / 2, cy - (y0 + y1) / 2, -z0)
    _solo(o)
    bpy.ops.object.transform_apply(location=True)
    return o


bpy.ops.wm.read_factory_settings(use_empty=True)

# --- SLEEVE ------------------------------------------------------------------------
# The boss is unioned BEFORE the cavity is cut, so its box may run into the cavity and
# have its inner-side chamfer trimmed off harmlessly by that cut.
sleeve = bevel(box("Sleeve_V88", 0, BOX_X, 0, BOX_Y, 0, BOX_Z), EDGE_BREAK)
sleeve = combine(sleeve, box("cavity", -1.0, CAV_X1, CAV_Y0, CAV_Y1, CAV_Z0, CAV_Z1),
                 "DIFFERENCE")

# Bolt hole. Standing on its rear end the sleeve prints with Z' = 86 - X, so the hole's
# LOW-X face is its ceiling and the span that would bridge is the hole's full Z extent.
# Chamfer both corners of that face 45deg: 10.50 -> 6.10mm.
hole = box("hole", HOLE_X0, HOLE_X1, CAV_Y1 - 0.2, BOX_Y + 0.1, HOLE_Z0, HOLE_Z1)
hole = combine(hole, wedge("hw_t", HOLE_X0, HOLE_Z1, -1, +1, HOLE_CH,
                           CAV_Y1 - 0.4, BOX_Y + 0.3), "DIFFERENCE")
hole = combine(hole, wedge("hw_b", HOLE_X0, HOLE_Z0, -1, -1, HOLE_CH,
                           CAV_Y1 - 0.4, BOX_Y + 0.3), "DIFFERENCE")
sleeve = combine(sleeve, hole, "DIFFERENCE")

# Entry counterbore on the face the bolt enters (cavity side) — blind-mate lead-in and
# tolerance for any droop left on the hole's ceiling.
cb = box("cbore", HOLE_X0 - CBORE_OVER, HOLE_X1 + CBORE_OVER, CAV_Y1 - 0.1,
         CAV_Y1 + CBORE_D, HOLE_Z0 - CBORE_OVER, HOLE_Z1 + CBORE_OVER)
cb = combine(cb, wedge("cw_t", HOLE_X0 - CBORE_OVER, HOLE_Z1 + CBORE_OVER, -1, +1,
                       CBORE_CH, CAV_Y1 - 0.3, CAV_Y1 + CBORE_D + 0.2), "DIFFERENCE")
cb = combine(cb, wedge("cw_b", HOLE_X0 - CBORE_OVER, HOLE_Z0 - CBORE_OVER, -1, -1,
                       CBORE_CH, CAV_Y1 - 0.3, CAV_Y1 + CBORE_D + 0.2), "DIFFERENCE")
sleeve = combine(sleeve, cb, "DIFFERENCE")

# v8.5 envelope assert: nothing may stand proud of the credit-card outline. Checked on the
# real mesh, not on the parameters, so a stray union anywhere would trip it.
_sy0, _sy1 = extents(sleeve)[1]
if abs(_sy0) > 1e-4 or abs(_sy1 - BOX_Y) > 1e-4:
    raise SystemExit(f"v8.8: sleeve spans Y {_sy0:.4f}..{_sy1:.4f}, must be 0..{BOX_Y}")

# U notch through the roof at the open end. Stood on its rear end the sleeve prints with
# this notch at the very TOP, and the void only ever widens going up, so the surrounding
# roof is a subset of the layer below it: nothing bridges and nothing overhangs.
notch = box("notch", -1.0, NOTCH_CX, NOTCH_Y0, NOTCH_Y1, CAV_Z1 - 0.1, BOX_Z + 0.5)
notch = combine(notch, cylinder_z("notcharc", NOTCH_CX, NOTCH_YC, CAV_Z1 - 0.1,
                                  BOX_Z + 0.5, NOTCH_R), "UNION")
sleeve = combine(sleeve, notch, "DIFFERENCE")

# --- DRAWER ------------------------------------------------------------------------
drawer = bevel(box("Drawer_V88", DR_X0, DR_X1, DR_Y0, DR_Y1, DR_Z0, DR_Z1), EDGE_BREAK)
COMP_SPAN = (DR_X1 - DR_WALL) - FB_X1
COMP_LEN = (COMP_SPAN - (N_COMPARTMENTS - 1) * DR_DIV) / N_COMPARTMENTS
_cx = FB_X1
for _i in range(N_COMPARTMENTS):
    drawer = combine(drawer, box(f"comp{_i}", _cx, _cx + COMP_LEN,
                                 DR_Y0 + DR_WALL, DR_Y1 - DR_WALL,
                                 DR_Z0 + DR_FLOOR, DR_Z1 + 0.5), "DIFFERENCE")
    _cx += COMP_LEN + DR_DIV

# Closed bore for the shaft. Its roof is chamfered at both upper inside corners, but each
# chamfer is only carried where the wall BELOW it survives to support the 45deg ramp:
# the front chamfer stops where the pad slot starts, the back chamfer skips the fin
# relief. A 45deg ramp starting in mid-air is worse than the bridge it replaces.
# GABLED section, y = CH_Y0..SLOT_Y0. Both 45deg planes run to the ridge, so there is no
# flat crown at all: the void narrows to a point and every layer of roof above it is a
# subset of the layer below. The front plane is carried by the front wall and the back
# plane by the block behind the bore — over the fin relief that support is the relief's
# own gabled ceiling, which is the same plane (see below).
chan = box("channel", CH_X0, CH_X1, CH_Y0, SLOT_Y0, CH_Z0, RIDGE_Z)
chan = combine(chan, wedge("cf", CH_X0, RIDGE_Z, -1, +1, GABLE_LEG_F,
                           CH_Y0 - 0.2, SLOT_Y0 + 0.2), "DIFFERENCE")
chan = combine(chan, wedge("cb", CH_X1, RIDGE_Z, +1, +1, GABLE_LEG_B,
                           CH_Y0 - 0.2, SLOT_Y0 + 0.2), "DIFFERENCE")
drawer = combine(drawer, chan, "DIFFERENCE")
# FLAT-CROWN section, y = SLOT_Y0..CH_Y1. This one cannot be gabled: see report(). Its
# ceiling stays at CH_Z1 and only the back corner is chamfered, on the same plane as the
# gable so the two sections meet without a step on that side.
chan2 = box("channel2", CH_X0, CH_X1, SLOT_Y0, CH_Y1, CH_Z0, CH_Z1)
chan2 = combine(chan2, wedge("cb2", CH_X1, CH_Z1, +1, +1, CHAN_CB,
                             SLOT_Y0 - 0.2, CH_Y1 + 0.2), "DIFFERENCE")
drawer = combine(drawer, chan2, "DIFFERENCE")

# Pad slot: the one opening in the bore. Closed at -Y (the OPEN hard stop), open at its
# +Y mouth, which is the musket-load insertion path.
drawer = combine(drawer, box("slot", SLOT_X0, SLOT_X1, SLOT_Y0, SLOT_Y1, CH_Z0, CH_Z1),
                 "DIFFERENCE")
# Fin relief: still open through the UNDERSIDE so the fin prints as a plain vertical wall
# off the bed. v8.1 closed its top with a flat cap, which was itself a 2.5mm bridge; v8.5
# roofs it with the bore's own back gable plane instead, carried down to the block's rear
# wall. That plane grows out of the rear wall at 45deg, so it needs nothing bridged, and it
# leaves the fin's top edge clear by 0.35 at its back corner.
relief = box("relief", CH_X1, RELIEF_X1, RELIEF_Y0, RELIEF_Y1, DR_Z0 - 0.5, RIDGE_Z)
relief = combine(relief, wedge("rb", CH_X1, RIDGE_Z, +1, +1, GABLE_LEG_B,
                               RELIEF_Y0 - 0.2, RELIEF_Y1 + 0.2), "DIFFERENCE")
drawer = combine(drawer, relief, "DIFFERENCE")
drawer = combine(drawer, box("fin", FIN_X0, FIN_X1, FIN_Y0 - 0.5, FIN_Y1, DR_Z0, FIN_Z1),
                 "UNION")
drawer = combine(drawer, sphere("bump", FIN_X0 + BUMP_R - BUMP_PROUD, BUMP_Y, ZC, BUMP_R),
                 "UNION")

# Grip knob on the drawer's TOP, sharing the notch's arc centre so clearance is a uniform
# KNOB_CLR all the way round. Clipped at the drawer's front face: any part hanging past it
# would print over air. Everything here faces up — knob, cone cap, grooves — so the drawer
# stays bridge-free in its bottom-down orientation.
knob = cylinder_z("knob", KNOB_CX, NOTCH_YC, DR_Z1 - 0.75, KNOB_Z1 - KNOB_CHAMFER,
                  KNOB_R)
knob = combine(knob, cone_z("knobcap", KNOB_CX, NOTCH_YC, KNOB_Z1 - KNOB_CHAMFER,
                            KNOB_Z1, KNOB_R, KNOB_R - KNOB_CHAMFER), "UNION")
knob = combine(knob, box("knobclip", DR_X0, KNOB_X1 + 1.0, DR_Y0, DR_Y1,
                         DR_Z1 - 1.0, KNOB_Z1 + 0.5), "INTERSECT")
drawer = combine(drawer, knob, "UNION")
# break the knob's front-top edge — the one square corner the clip leaves behind
drawer = combine(drawer, wedge("knobfront", DR_X0, KNOB_Z1, -1, +1, KNOB_CHAMFER,
                               DR_Y0 - 1.0, DR_Y1 + 1.0), "DIFFERENCE")
for _i in range(GROOVE_N):
    _gx = DR_X0 + 1.6 + _i * (KNOB_X1 - DR_X0 - 3.2) / (GROOVE_N - 1)
    drawer = combine(drawer, cylinder_y("groove", _gx, KNOB_Z1 + GROOVE_R - GROOVE_D,
                                        GROOVE_R, NOTCH_Y0 - 1.0, NOTCH_Y1 + 1.0),
                     "DIFFERENCE")

# --- BOLT (modelled at LOCKED, in the assembly frame) ------------------------------
# 0.5mm all-edge chamfer on the PLAIN box first — that is the tip lead-in, and bevelling
# after the pad and dimple booleans is the order that breaks. Then the three long-edge
# wedges: they are the lead-in proper AND what lets the housing chamfer its roofs.
bolt = bevel(box("Bolt_V88", BOLT_X0, BOLT_X1, TAIL_LOCKED, TIP_LOCKED, BOLT_Z0, BOLT_Z1),
             EDGE_BREAK)
_by0, _by1 = TAIL_LOCKED - 1.0, TIP_LOCKED + 1.0
bolt = combine(bolt, wedge("bft", BOLT_X0, BOLT_Z1, -1, +1, BLADE_FT, _by0, _by1),
               "DIFFERENCE")
bolt = combine(bolt, wedge("bfb", BOLT_X0, BOLT_Z0, -1, -1, BLADE_FB, _by0, _by1),
               "DIFFERENCE")
bolt = combine(bolt, wedge("bbt", BOLT_X1, BOLT_Z1, +1, +1, BLADE_BT, _by0, _by1),
               "DIFFERENCE")
# Thumb pad: FULL bolt height, so it prints as a vertical rib and never overhangs itself.
# It reaches PAST the blade's front face to BOLT_X0 + BLADE_FT, refilling the two front
# corner chamfers over its own Y span. Left hollow, the taper between the pad's back and
# the receding chamfer closes into a 1.9mm bridge on the bolt's underside — the one bridge
# the first slice found on this part. Refilling costs nothing: the pad's span never enters
# the sleeve wall, so those chamfers are not doing lead-in work there, and the channel's
# own front chamfer is already omitted over the slot.
bolt = combine(bolt, box("pad", PAD_X0, BOLT_X0 + max(BLADE_FT, BLADE_FB) + 0.05,
                         PAD_Y0_LOCKED, PAD_Y1_LOCKED, BOLT_Z0, BOLT_Z1), "UNION")
for _i in range(RIDGE_N):
    _ry = PAD_Y0_LOCKED + 2.0 + _i * (PAD_L - 4.0) / (RIDGE_N - 1)
    bolt = combine(bolt, box("ridge", RIDGE_X0, PAD_X0 + 0.05, _ry, _ry + RIDGE_W,
                             BOLT_Z0, BOLT_Z1), "UNION")
for _dy, _depth in ((DIMPLE_LOCK_Y, DIMPLE_LOCK_D), (DIMPLE_OPEN_Y, DIMPLE_OPEN_D)):
    bolt = combine(bolt, sphere("dimple", BOLT_X1 + DIMPLE_R - _depth, _dy, ZC, DIMPLE_R),
                   "DIFFERENCE")

# --- v8.8 MARK: the version AND the date, on the blade's back face ------------------
# The mark is cut HERE, in the design source, and not onto the exported STL afterwards: the
# project builds print/{version}_pillbox_plate.stl from the tagged script, so a mark applied
# downstream is gone on the next refresh. The helper is bootstrapped off PRINTFARM_SRC —
# the documented path — so the API host reproduces this build from the tag alone.
# The bolt is never rotated by pose(), so its +X here IS a vertical side wall on the plate.
# The privates come from the same module for the same reason render_part.py borrows
# _largest_rect: the guards below must measure the part the way engrave() measures it, or
# the two can disagree about a mark that is fine — and the band guard in particular needs
# the face rectangle's CENTRE, which is what engrave() places the mark on.
sys.path.insert(0, os.environ.get("PRINTFARM_SRC", os.path.expanduser("~/code/printfarm/src")))
from watermark import (MIN_DEPTH_MM, MIN_STROKE_DEBOSS_MM, MIN_STROKE_EMBOSS_MM,  # noqa: E402
                       _flat_region, _frame, _mesh_volume, _world_mesh_bbox, engrave,
                       stroke_mm)

MARK_TEXT = "v8.8 15ag26"                              # version AND date: see the docstring
MARK_FACE, MARK_ROT = "+X", 0.0                        # the blade's back face; its long axis
MARK_MARGIN = 1.0                                      # IS the bolt axis, so no rotation
# DEPTH. v8.7 used 0.6 because its face was the part's FIRST LAYER and squish fills a
# shallow recess. This face is a vertical wall: no squish, no elephant foot, and the recess
# is a notch the outer perimeter detours into rather than layers of floor. Extrusion width
# governs, not layer height, so the depth is set ~1:1 against the stroke (0.522mm) — a
# 0.42mm nozzle enters a 0.52mm groove and at that aspect can trace both flanks without the
# passes colliding and filling the letter shut. See the docstring.
MARK_DEPTH = 0.5
MARK_FONT = "DejaVu Sans Mono:style=Bold"
# CAP IS DERIVED, NOT PICKED — v8.7's rule verbatim, so the letters carry the same ink. The
# loop measures what stroke the target actually draws in THIS font and steps up until it
# clears the deboss floor; the fit against the free region is checked separately below,
# because a cap that fits but cannot be read is not a smaller mark, it is no mark.
MARK_CAP_TARGET, MARK_CAP_STEP = 3.0, 0.1
MARK_CAP = MARK_CAP_TARGET
while stroke_mm(MARK_CAP, MARK_FONT) < MIN_STROKE_DEBOSS_MM:
    MARK_CAP = round(MARK_CAP + MARK_CAP_STEP, 3)
    if MARK_CAP > 4.0:                                 # v8.6's cap: at that point stop
        raise SystemExit(f"v8.8: {MARK_FONT} needs a cap over 4.0mm to reach the"
                         f" {MIN_STROKE_DEBOSS_MM}mm deboss floor — this is not a smaller mark")
if MARK_DEPTH < MIN_DEPTH_MM:
    raise SystemExit(f"v8.8: mark depth {MARK_DEPTH}mm is under the module's"
                     f" {MIN_DEPTH_MM}mm floor — a groove that shallow does not print")

# --- THE SWEPT BAND, derived from the fin and the dimples --------------------------
# The one hazard on this face is a FALSE DETENT: a recess anywhere the fin's bump can reach
# gives the bump somewhere to drop into, and the bolt clicks where it should not. Every
# number below comes from the fin/dimple parameters above, so moving a dimple, retuning the
# stroke or regrowing the bump re-derives the band and the guard either still passes or
# stops the build. None of it is copied from a measurement.
OVERTRAVEL_OPEN = (TIP_OPEN - BOLT_L) - CH_Y0          # 0.50 further before the tail bottoms
BUMP_PEN = BOLT_X1 - (FIN_X0 - BUMP_PROUD)             # 0.25 proud of the blade face
BUMP_CONTACT_R = (BUMP_R ** 2 - (BUMP_R - BUMP_PEN) ** 2) ** 0.5   # 0.698, the real patch
SWEPT_Y0 = DIMPLE_LOCK_Y - BUMP_R                      # LOCKED is a hard stop: no over-travel
SWEPT_Y1 = DIMPLE_OPEN_Y + OVERTRAVEL_OPEN + BUMP_R    # OPEN is not: add the over-travel
SWEPT_Z0, SWEPT_Z1 = ZC - BUMP_R, ZC + BUMP_R
# BUMP_R, not BUMP_CONTACT_R: the band is deliberately drawn wider than the patch can be.
MARK_BAND_CLR = 1.0                                    # ~2.4 extrusion widths; see docstring
# Guarding the band only guards the dimple RIMS if the rims are inside it. Prove that here
# rather than assuming it — a deeper dimple has a wider rim and could grow past the band.
for _name, _dy, _d in (("LOCKED", DIMPLE_LOCK_Y, DIMPLE_LOCK_D),
                       ("OPEN", DIMPLE_OPEN_Y, DIMPLE_OPEN_D)):
    _rim = (2 * DIMPLE_R * _d - _d * _d) ** 0.5
    if _rim > BUMP_R or _dy - _rim < SWEPT_Y0 - 1e-9 or _dy + _rim > SWEPT_Y1 + 1e-9:
        raise SystemExit(f"v8.8: the {_name} dimple's rim (r={_rim:.3f} at y={_dy:.2f}) is not"
                         f" inside the swept band y {SWEPT_Y0:.2f}..{SWEPT_Y1:.2f},"
                         f" r<={BUMP_R} — the band guard would stop protecting the rim")

# Measure the face the way engrave() will, BEFORE the boolean: engrave() centres the mark on
# the largest rectangle of material really at the face plane, so this centre is where the
# mark lands and the band guard needs it to compute the footprint.
_axis, _sign, _n, _right, _up, _ri, _ui = _frame(MARK_FACE)
MARK_CR, MARK_CU, MARK_FACE_W, MARK_FACE_H = _flat_region(bolt, _axis, _sign, _ri, _ui)

# FROZEN BOLT. v8.8 changes no geometry, so these are what v8.5 actually built
# (print/v8_5_pillbox_bolt.stl, Blender 4.5.12). MARK_CUT_MM3 is the NEW mark's own cut,
# measured on the first v8.8 build — this mark is far longer than v8.7's, so v8.7's 5.514 is
# not carried forward. They are asserted below, before and after the mark.
BOLT_V85_DIMS = (8.0, 44.0, 10.0)
BOLT_V85_VOL = 2426.77695
MARK_CUT_MM3 = 15.35790

_pre_box = _world_mesh_bbox(bolt)
_pre_dims = tuple(_pre_box[1][_a] - _pre_box[0][_a] for _a in (0, 1, 2))
_pre_vol = _mesh_volume(bolt.data)
MARK = engrave(bolt, MARK_TEXT, face=MARK_FACE, depth=MARK_DEPTH, cap_mm=MARK_CAP,
               mode="deboss", margin_mm=MARK_MARGIN, rotate_deg=MARK_ROT, font=MARK_FONT)
_post_box = _world_mesh_bbox(bolt)
_post_dims = tuple(_post_box[1][_a] - _post_box[0][_a] for _a in (0, 1, 2))
_mark_cut = _pre_vol - _mesh_volume(bolt.data)

# --- v8.8 mark guard ---------------------------------------------------------------
# FROZEN BOLT. The v8.5 bolt is printed and its fits were signed off in the hand, so the
# ONLY legal difference between this mesh and that one is the recess itself. The housing
# guard above cannot see this: it checks parameters, and a mark is pure mesh. So check the
# mesh — the bounding box must be v8.5's to 1e-4 (a mark that moved a face would show up
# here as a tenth of a millimetre nobody would otherwise notice), and the volume must move
# DOWN by exactly the mark's own cut. Anything else means the boolean ate the part.
for _name, _got, _want, _tol in [
    ("bolt X before the mark", _pre_dims[0], BOLT_V85_DIMS[0], 1e-4),
    ("bolt Y before the mark", _pre_dims[1], BOLT_V85_DIMS[1], 1e-4),
    ("bolt Z before the mark", _pre_dims[2], BOLT_V85_DIMS[2], 1e-4),
    ("bolt volume before the mark", _pre_vol, BOLT_V85_VOL, 1e-3),
    ("bolt X after the mark", _post_dims[0], BOLT_V85_DIMS[0], 1e-4),
    ("bolt Y after the mark", _post_dims[1], BOLT_V85_DIMS[1], 1e-4),
    ("bolt Z after the mark", _post_dims[2], BOLT_V85_DIMS[2], 1e-4),
    ("the mark's cut", _mark_cut, MARK_CUT_MM3, MARK_CUT_MM3 * 0.02),
]:
    if abs(_got - _want) > _tol:
        raise SystemExit(f"v8.8: {_name} is {_got:.5f}, must be {_want:.5f}"
                         f" +/-{_tol:g} — v8.8 may not change the bolt, only mark it")
# The floor this mark has to clear is the DEBOSS floor, asserted against the module's own
# constant rather than a number copied into this file.
if MARK["stroke_mm"] < MIN_STROKE_DEBOSS_MM:
    raise SystemExit(f"v8.8: stroke {MARK['stroke_mm']:.3f}mm is under the module's"
                     f" {MIN_STROKE_DEBOSS_MM}mm deboss floor at cap {MARK_CAP:.2f}mm")
# legibility() is then checked in full. A warning means the mark is below a floor for the mode
# actually requested, so any warning stops the build — there is nothing here to accept by name.
if MARK["warnings"]:
    raise SystemExit(f"v8.8: the mark is below a legibility floor: {MARK['warnings']}")

# --- v8.8 FALSE-DETENT GUARD, new in this version ----------------------------------
# The guard the placement rule should have been all along. engrave() chose the face we named
# and centred the mark on the rectangle measured above; check that it did, then check that
# the resulting footprint is clear of the swept band by MARK_BAND_CLR on at least one axis.
# It is written against SWEPT_*, which are derived from the fin and the dimples, so a later
# edit that moves a dimple, lengthens the stroke or fattens the bump fails the BUILD instead
# of quietly cutting a place for the detent to land.
if MARK["face"] != MARK_FACE:
    raise SystemExit(f"v8.8: engrave() marked face {MARK['face']}, not {MARK_FACE} — the band"
                     f" guard's coordinates are only valid for {MARK_FACE}")
if (abs(MARK["face_size_mm"][0] - MARK_FACE_W) > 1e-3
        or abs(MARK["face_size_mm"][1] - MARK_FACE_H) > 1e-3):
    raise SystemExit(f"v8.8: engrave() measured the face as {MARK['face_size_mm']}, this file"
                     f" measured {MARK_FACE_W:.3f} x {MARK_FACE_H:.3f} — the band guard cannot"
                     f" trust its own footprint")
MARK_Y0 = MARK_CR - MARK["text_size_mm"][0] / 2
MARK_Y1 = MARK_CR + MARK["text_size_mm"][0] / 2
MARK_Z0 = MARK_CU - MARK["text_size_mm"][1] / 2
MARK_Z1 = MARK_CU + MARK["text_size_mm"][1] / 2
BAND_GAPS = {
    "+Y, out past the OPEN dimple": MARK_Y0 - SWEPT_Y1,
    "-Y, back behind the LOCKED dimple": SWEPT_Y0 - MARK_Y1,
    "+Z, above the band": MARK_Z0 - SWEPT_Z1,
    "-Z, below the band": SWEPT_Z0 - MARK_Z1,
}
MARK_BAND_SIDE = max(BAND_GAPS, key=BAND_GAPS.get)
MARK_BAND_GAP = BAND_GAPS[MARK_BAND_SIDE]
if MARK_BAND_GAP < MARK_BAND_CLR:
    raise SystemExit(
        f"v8.8: the mark's footprint y {MARK_Y0:.2f}..{MARK_Y1:.2f} z {MARK_Z0:.2f}.."
        f"{MARK_Z1:.2f} is only {MARK_BAND_GAP:.3f}mm clear of the bump's swept band"
        f" (y {SWEPT_Y0:.2f}..{SWEPT_Y1:.2f}, z {SWEPT_Z0:.3f}..{SWEPT_Z1:.3f}), best side"
        f" {MARK_BAND_SIDE}; {MARK_BAND_CLR}mm is the minimum. A recess on that path is a"
        f" FALSE DETENT — the bolt would click where it should not.")


# --- build report: every number below is derived, none is asserted by hand -----------
DR_INNER_Y = DR_Y1 - DR_WALL
BRIDGES = [
    ("drawer", "bore roof, gabled run", 0.0,
     f"y {CH_Y0:.1f}-{SLOT_Y0:.1f}; two 45deg planes meet at a ridge, z={RIDGE_Z:.2f},"
     f" x={RIDGE_X:.2f} — no flat crown to bridge"),
    ("drawer", "bore roof over fin relief", 0.0,
     f"y {RELIEF_Y0:.1f}-{RELIEF_Y1:.1f}; the relief shares the same gable, so the back"
     " plane now has support the whole way"),
    ("drawer", "bore roof over pad slot", (CH_X1 - CHAN_CB) - DR_X0,
     f"y {SLOT_Y0:.1f}-{CH_Y1:.1f}; CANNOT be gabled — see report(), the only span left"),
    ("drawer", "fin relief cap", 0.0,
     f"GONE — the flat cap is replaced by the gable plane landing on the rear wall at"
     f" z={RELIEF_Z1:.2f}"),
    ("drawer", "top grip knob", 0.0,
     "knob, cone cap and grooves all face up off a solid roof slab"),
    ("sleeve", "roof U notch", 0.0,
     "prints at the top of the standing sleeve; the void only widens going up"),
    ("sleeve", "bolt hole ceiling", (HOLE_Z1 - HOLE_CH) - (HOLE_Z0 + HOLE_CH),
     "low-X face is the ceiling when stood on the rear end; both corners chamfered"),
    ("sleeve", "counterbore ceiling",
     (HOLE_Z1 + CBORE_OVER - CBORE_CH) - (HOLE_Z0 - CBORE_OVER + CBORE_CH),
     f"only {CBORE_D}mm deep; droop here lands in the lead-in recess"),
    ("bolt", "none", 0.0, "sliced with zero Bridge and zero Overhang wall: pad and ridges"
     " are full-height vertical ribs, corner chamfers are 45deg self-supporting, the pad"
     " refills the front chamfers over its own span, dimples are 1.1mm pockets"),
    ("bolt", "v8.8 mark recess", 0.0,
     f"{MARK_DEPTH}mm deep in a VERTICAL wall — perimeters detour into a notch every layer."
     f" Its only overhang is the {MARK_DEPTH}mm ledge at each glyph's top, not a span"),
]


def report():
    print("\nv8.8 Y-STACK (mm, along the bolt axis)")
    for label, y, note in [
        ("bore closed end", CH_Y0, "musket-load stop; 1.0mm of -Y side wall left solid"),
        ("bolt tail @ OPEN", TIP_OPEN - BOLT_L, "fully inside the bore"),
        ("bolt tail @ LOCKED", TAIL_LOCKED, f"guide still engaged {DR_Y1 - TAIL_LOCKED:.2f}"),
        ("drawer wall, inner", DR_INNER_Y,
         f"bore {CH_X1 - CH_X0:.2f}x{CH_Z1 - CH_Z0:.2f} = {CLR}/face on the blade"),
        ("drawer wall, outer", DR_Y1, f"wall {DR_WALL}"),
        ("sleeve wall, inner", CAV_Y1, f"running gap {CAV_Y1 - DR_Y1:.2f}"),
        ("counterbore floor", CAV_Y1 + CBORE_D,
         f"{CBORE_D} deep, {2 * CBORE_OVER} oversize, on the face the bolt enters"),
        ("sleeve OUTER face", BOX_Y,
         f"uniform {WALL_LOCK} lock wall, dead flat; only the bolt tip breaks it"),
        ("bolt tip @ LOCKED", TIP_LOCKED,
         f"{TIP_PROUD:.2f} proud — the tactile 'locked' bump"),
    ]:
        print(f"   y={y:7.2f}  {label:<24} {note}")
    print(f"   blade {BOLT_T}x{BOLT_H} x {BOLT_L} long   travel {TRAVEL:.2f}")
    print(f"   LOCKED tip y={TIP_LOCKED:.2f} vs the plain outer face y={BOX_Y:.2f}"
          f" -> {TIP_LOCKED - BOX_Y:.2f} PROUD by design;"
          f" engagement in the sleeve wall {TIP_LOCKED - CAV_Y1:.2f}")
    print(f"   OPEN   tip y={TIP_OPEN:.2f} vs drawer inner wall y={DR_INNER_Y:.2f}"
          f" -> clear by {DR_INNER_Y - TIP_OPEN:.2f};"
          f" clear of the sleeve wall by {CAV_Y1 - TIP_OPEN:.2f}")
    print(f"   travel needed to clear the drawer's own wall = {TIP_LOCKED - DR_INNER_Y:.2f}"
          f"; to merely clear the sleeve = {TIP_LOCKED - CAV_Y1:.2f}; using {TRAVEL:.2f}")
    print(f"   GUIDE engaged inside the drawer: LOCKED {DR_Y1 - TAIL_LOCKED:.2f}"
          f" ({(DR_Y1 - TAIL_LOCKED) / BOLT_T:.1f}:1 on a {BOLT_T}mm shaft),"
          f" OPEN {BOLT_L:.2f} ({BOLT_L / BOLT_T:.1f}:1)")
    print(f"\n   STOPS (v8.5 — this is the fix)")
    print(f"   LOCKED = HARD: the pad's +Y face bears on the sleeve wall at"
          f" y={CAV_Y1:.2f}. Bearing land is x {PAD_X0 - RIDGE_P:.2f}..{HOLE_X0 - CBORE_OVER:.2f}"
          f" (the counterbore takes the rest), about"
          f" {((HOLE_X0 - CBORE_OVER) - (PAD_X0 - RIDGE_P)) * BOLT_H:.0f} mm2 of PETG"
          f" on PETG. The thumb cannot push past it.")
    print(f"   the LOCKED dimple sits at y={DIMPLE_LOCK_Y:.2f} = the fin bump, so the"
          f" click lands exactly as the pad touches the wall — click and stop agree")
    print(f"   OPEN = HARD too, and free: the blade's tail reaches the bore's closed end"
          f" at y={CH_Y0:.2f} only {(TIP_OPEN - BOLT_L) - CH_Y0:.2f} past OPEN, so"
          f" over-travel that way is arrested as well")
    print(f"   pad @OPEN spans y={PAD_Y0_LOCKED - TRAVEL:.2f}..{PAD_Y1_LOCKED - TRAVEL:.2f}"
          f" inside a slot running {SLOT_Y0:.2f}..{SLOT_Y1:.2f} -> fully captive, with"
          f" {(PAD_Y0_LOCKED - TRAVEL) - SLOT_Y0:.2f} to spare at the -Y end")

    print("\nv8.8 DRAWER vs CAVITY")
    print(f"   Y  drawer {DR_Y0:.2f}..{DR_Y1:.2f} in cavity {CAV_Y0:.2f}..{CAV_Y1:.2f}"
          f"  -> {DR_Y0 - CAV_Y0:.2f} / {CAV_Y1 - DR_Y1:.2f} per side")
    print(f"   Z  drawer {DR_Z0:.2f}..{DR_Z1:.2f} in cavity {CAV_Z0:.2f}..{CAV_Z1:.2f}"
          f"  -> {DR_Z0 - CAV_Z0:.2f} below / {CAV_Z1 - DR_Z1:.2f} above")
    print(f"   X  drawer {DR_X0:.2f}..{DR_X1:.2f}, cavity ends {CAV_X1:.2f}"
          f"  -> the rear face IS the closed stop; front face {DR_X0:.2f} behind the rim")
    print(f"   drawer body {DR_L:.2f} x {DR_Y1 - DR_Y0:.2f} x {DR_Z1 - DR_Z0:.2f}"
          f"; front block {FB_X1 - DR_X0:.2f} deep")
    _kx0 = DR_X0
    _khw = (KNOB_R ** 2 - max(_kx0 - KNOB_CX, 0.0) ** 2) ** 0.5
    _nhw = (NOTCH_R ** 2 - max(_kx0 - NOTCH_CX, 0.0) ** 2) ** 0.5
    print(f"\nv8.8 TOP GRIP")
    print(f"   sleeve roof notch: U, {NOTCH_W:.1f} wide x {NOTCH_D:.1f} deep in X,"
          f" semicircular end r={NOTCH_R:.2f} at x={NOTCH_CX:.2f}, y"
          f" {NOTCH_Y0:.2f}-{NOTCH_Y1:.2f}; cut through the roof z"
          f" {CAV_Z1:.2f}-{BOX_Z:.2f}, open at the mouth")
    print(f"   drawer knob: arc r={KNOB_R:.2f} centred {KNOB_E:.2f} forward of the"
          f" notch's; x {DR_X0:.2f}-{KNOB_X1:.2f} ({KNOB_X1 - DR_X0:.2f} long), width"
          f" {2 * _khw:.2f} at its front vs notch {2 * _nhw:.2f} there")
    print(f"   knob z {DR_Z1:.2f}-{KNOB_Z1:.2f} = {KNOB_Z1 - DR_Z1:.2f} tall"
          f" ({CAV_Z1 - DR_Z1:.2f} ceiling gap + {BOX_Z - CAV_Z1:.2f} roof), top FLUSH"
          f" with the sleeve outer roof; {GROOVE_N} grooves {GROOVE_D} deep, crowns flush")
    _flank = (NOTCH_R ** 2 - KNOB_E ** 2) ** 0.5 - KNOB_R
    print(f"   DOCK: knob's +X end {KNOB_X1:.2f} vs notch end {NOTCH_D:.2f} ->"
          f" {NOTCH_D - KNOB_X1:.2f} gap; flanks still {_flank:.3f} (arc centre offset"
          f" {KNOB_E:.2f}) so only the dock tightened")
    print(f"   FULLY-CLOSED IS DEFINED BY: the drawer's rear face bottoming out on the"
          f" cavity at x={CAV_X1:.2f}. The dock backs it up {NOTCH_D - KNOB_X1:.2f} behind.")
    print(f"   why: the rear face is a {DR_Y1 - DR_Y0:.0f}x{DR_Z1 - DR_Z0:.1f} flat-on-flat"
          f" contact that cannot cam or wear, and it is the datum the bolt-hole X"
          f" alignment was validated against. An arc-on-arc dock would wear into slop and"
          f" fight the rear face for control. Because the two stops sit within"
          f" {NOTCH_D - KNOB_X1:.2f} of each other, whichever wins bounds the closed"
          f" position to that — which is what lets the hole's load face tighten.")
    print(f"   withdrawing moves the knob -X, its arc centre leaves the notch's, so"
          f" clearance only grows: max width {2 * KNOB_R:.2f} in a {NOTCH_W:.2f} slot")
    print(f"   compartments {N_COMPARTMENTS} x {COMP_LEN:.2f} long,"
          f" {DR_Y1 - DR_Y0 - 2 * DR_WALL:.2f} wide, {DR_Z1 - DR_Z0 - DR_FLOOR:.2f} deep;"
          f" dividers {DR_DIV}")

    print("\nv8.8 LOCKED FREE PLAY (mm of drawer movement, v8.2 -> v8.5)")
    print(f"   X  bore {CLR:.2f} + hole load face {HOLE_CLR_X_LOAD:.2f} ="
          f" {CLR + HOLE_CLR_X_LOAD:.2f}   was 0.30 + 0.45 = 0.75"
          f"   (+X is dead-stopped by the rear face, so this is the whole range)")
    print(f"   Y  2 x {CLR_SIDE:.2f} = {2 * CLR_SIDE:.2f}   was 0.40")
    print(f"   Z  {CLR_BELOW:.2f} below + {CLR_ABOVE:.2f} above ="
          f" {CLR_BELOW + CLR_ABOVE:.2f}   was 0.80")
    print(f"   the bore's own {CLR:.2f} is now the single largest term in X and is left"
          f" alone: it is the validated sliding fit the operator signed off.")
    print(f"   visible slack behind the knob at closed: {NOTCH_D - KNOB_X1:.2f}, was 0.30")

    print("\nv8.8 DETENT")
    _fin_l = FIN_Y1 - FIN_Y0
    _defl = BOLT_X1 - (FIN_X0 - BUMP_PROUD)
    _strain = 3 * FIN_T * _defl / (2 * _fin_l ** 2)
    print(f"   fin {FIN_T} x {_fin_l:.1f} long x {FIN_Z1 - DR_Z0:.2f} tall,"
          f" anchored at y={FIN_Y0:.1f}, free at y={FIN_Y1:.1f} (flipped in v8.5),"
          f" {FIN_FREE} behind it")
    print(f"   bump crown x={FIN_X0 - BUMP_PROUD:.2f} vs blade back face x={BOLT_X1:.2f}"
          f"  -> deflection at the crossover {_defl:.2f} (UNCHANGED from v8.0)")
    print(f"   fin strain 3*t*d/(2*L^2) = {_strain * 100:.3f}% vs PETG yield ~2%")
    print(f"   bump sinks {BUMP_PROUD - (FIN_X0 - BOLT_X1):.2f} below the blade face when"
          f" relaxed; both dimples are deeper than that, so it never bottoms out")
    print(f"   dimples LOCKED {DIMPLE_LOCK_D} deep, OPEN {DIMPLE_OPEN_D} deep;"
          f" bolt-local y {DIMPLE_LOCK_Y - TAIL_LOCKED:.2f} and"
          f" {DIMPLE_OPEN_Y - TAIL_LOCKED:.2f} of {BOLT_L:.1f}")

    _blade_f = BOLT_Z1 - BLADE_FT - BOLT_X0
    _blade_b = BOLT_X1 + BOLT_Z1 - BLADE_BT
    _need = BOLT_Z1 + CLR
    _pin_x1 = _blade_b - BOLT_Z1                       # where the blade's back chamfer starts
    print("\nv8.8 GABLE")
    print(f"   front plane z-x={GABLE_F:.2f}, back plane x+z={GABLE_B:.2f} — the SAME two"
          f" planes v8.1 chamfered with, simply run on until they meet")
    print(f"   ridge x={RIDGE_X:.2f} z={RIDGE_Z:.2f}; roof above it"
          f" {DR_Z1 - RIDGE_Z:.2f}, knob base at {DR_Z1 - 0.75:.2f} clears by"
          f" {DR_Z1 - 0.75 - RIDGE_Z:.2f} -> no break-through, angle stays 45deg")
    print(f"   blade clearance unchanged: front |{GABLE_F:.2f}-{_blade_f:.2f}|/sqrt2 ="
          f" {abs(GABLE_F - _blade_f) * SQ2:.3f}, back"
          f" {abs(GABLE_B - _blade_b) * SQ2:.3f} (>= {CLR})")
    print(f"   relief ceiling is that back plane landing on the rear wall at"
          f" x={RELIEF_X1:.2f} z={RELIEF_Z1:.2f}; fin top {FIN_Z1:.2f} clears the plane"
          f" above its back edge by {GABLE_B - FIN_X1 - FIN_Z1:.2f}")
    print(f"   NOT gabled, y {SLOT_Y0:.1f}-{CH_Y1:.1f}: the pad forces the ceiling to"
          f" >= {_need:.2f} from x={DR_X0:.2f} to {_pin_x1:.2f}, and only"
          f" {DR_Z1 - _need:.2f} of headroom exists above it.")
    _c_ridge = ((_need - DR_X0) + GABLE_B) / 2
    print(f"   a 45deg plane springing from the front face would ridge at"
          f" z={_c_ridge:.2f}, leaving {DR_Z1 - _c_ridge:.2f} of roof and fouling the"
          f" knob base at {DR_Z1 - 0.75:.2f}.")
    print(f"   steeper than 45deg raises the ridge, not lowers it, and the slot is a"
          f" through-window so nothing exists below z={_need:.2f} to spring a plane from.")
    print(f"   -> irreducible without moving a frozen constraint (drawer top, pad top,"
          f" or the slot's +Y insertion mouth).")

    print("\nv8.8 BRIDGED FACES (flat span that must bridge, mm)")
    for part, what, span, why in BRIDGES:
        print(f"   {part:<7} {what:<26} {span:5.2f}  {why}")

    print("\nv8.8 MARK")
    print(f"   \"{MARK['text']}\" debossed on face {MARK['face']} — the blade's BACK face,"
          f" the one the dimples are in — unrotated, because that face's long axis is the"
          f" bolt axis: {MARK['text_size_mm'][0]:.2f} x {MARK['text_size_mm'][1]:.2f}mm on"
          f" {MARK['face_size_mm'][0]:.2f} x {MARK['face_size_mm'][1]:.2f}mm of flat"
          f" material ({MARK_MARGIN:.1f}mm margin all round)")
    print(f"   font {MARK['font']}")
    print(f"   cap {MARK_CAP:.2f}mm (target {MARK_CAP_TARGET:.2f}, stepped"
          f" {MARK_CAP_STEP:.1f} until the stroke cleared the floor) -> stroke"
          f" {MARK['stroke_mm']:.3f}mm MEASURED on the meshed glyph, vs the"
          f" {MIN_STROKE_DEBOSS_MM}mm deboss floor and the {MIN_STROKE_EMBOSS_MM}mm emboss"
          f" floor this mark is deliberately under (it is a groove, not a bead)")
    print(f"   same font, same cap and same {MARK['stroke_mm']:.3f}mm stroke as v8.7 — only"
          f" the string changed, 4 chars -> {len(MARK_TEXT)}, and with it the footprint:"
          f" 9.44 x 3.11 -> {MARK['text_size_mm'][0]:.2f} x {MARK['text_size_mm'][1]:.2f}mm."
          f" The version alone would be 9.49 x 3.11 here.")
    print(f"   warnings: {MARK['warnings'] or 'none'}")
    print(f"   depth {MARK_DEPTH:.2f}mm on a VERTICAL wall, so it prints as perimeters"
          f" detouring into a notch, not as first-layer floor: ~1:1 against its own"
          f" {MARK['stroke_mm']:.3f}mm stroke, over the module's {MIN_DEPTH_MM}mm floor."
          f" v8.7's 0.6 was for elephant-foot squish on a plate-contact face; there is none"
          f" here")

    print("\nv8.8 FALSE-DETENT CLEARANCE (the guard, in full)")
    print(f"   what touches this face across the whole stroke: the fin bump, and nothing"
          f" else. channel wall x={CH_X1:.2f} stands off by {CH_X1 - BOLT_X1:.2f}; sleeve"
          f" hole x={HOLE_X1:.2f} by {HOLE_X1 - BOLT_X1:.2f} (the asymmetric hole's LOOSE"
          f" side, because this face never bears); counterbore {CBORE_OVER:.2f} looser;"
          f" the fin relief is behind the fin, outside the bore")
    print(f"   the LOADED face is -X: pull the drawer and the blade bears on the hole's"
          f" -X wall at x={HOLE_X0:.2f}, {HOLE_CLR_X_LOAD:.2f} off the blade. That face"
          f" carries 1.25 x 10.00mm of flat material and could not hold this mark anyway.")
    print(f"   bump r={BUMP_R:.2f} at x={FIN_X0 + BUMP_R - BUMP_PROUD:.2f},"
          f" {BUMP_PEN:.2f} proud of the face -> the disc that can actually touch is"
          f" r={BUMP_CONTACT_R:.3f}; the band is drawn at {BUMP_R:.2f} anyway,"
          f" {BUMP_R - BUMP_CONTACT_R:.3f}mm conservative on every side")
    print(f"   swept band  Y {SWEPT_Y0:6.2f} .. {SWEPT_Y1:6.2f}  = DIMPLE_LOCK_Y-r ..")
    print(f"                                         DIMPLE_OPEN_Y + over-travel"
          f" {OVERTRAVEL_OPEN:.2f} + r")
    print(f"               Z {SWEPT_Z0:6.3f} .. {SWEPT_Z1:6.3f}  = ZC -/+ r")
    print(f"   dimple rims r={(2 * DIMPLE_R * DIMPLE_LOCK_D - DIMPLE_LOCK_D ** 2) ** 0.5:.3f}"
          f" (LOCKED) and {(2 * DIMPLE_R * DIMPLE_OPEN_D - DIMPLE_OPEN_D ** 2) ** 0.5:.3f}"
          f" (OPEN), both < {BUMP_R:.2f} and both inside the band -> guarding the band"
          f" guards the rims")
    print(f"   band area {(SWEPT_Y1 - SWEPT_Y0) * (SWEPT_Z1 - SWEPT_Z0):.1f}mm2 of the"
          f" face's {(TIP_LOCKED - TAIL_LOCKED - 2 * EDGE_BREAK) * (BOLT_H - BLADE_BT - EDGE_BREAK):.1f}mm2"
          f" = {(SWEPT_Y1 - SWEPT_Y0) * (SWEPT_Z1 - SWEPT_Z0) / ((TIP_LOCKED - TAIL_LOCKED - 2 * EDGE_BREAK) * (BOLT_H - BLADE_BT - EDGE_BREAK)) * 100:.1f}%"
          f" — the rest of the face contacts nothing, which is what let the date back on")
    print(f"   free rectangle engrave() found: y {MARK_CR - MARK_FACE_W / 2:.2f}.."
          f"{MARK_CR + MARK_FACE_W / 2:.2f} z {MARK_CU - MARK_FACE_H / 2:.3f}.."
          f"{MARK_CU + MARK_FACE_H / 2:.3f}; its -Y edge IS the OPEN dimple's rim, and the"
          f" mark centres on it at y={MARK_CR:.2f}")
    print(f"   mark footprint  y {MARK_Y0:.2f}..{MARK_Y1:.2f}  z {MARK_Z0:.3f}..{MARK_Z1:.3f}")
    print(f"   clear of the band on {MARK_BAND_SIDE} by {MARK_BAND_GAP:.3f}mm, against the"
          f" {MARK_BAND_CLR:.1f}mm guard; add the band's own"
          f" {BUMP_R - BUMP_CONTACT_R:.3f} of conservatism and the true gap to the contact"
          f" patch is {MARK_BAND_GAP + BUMP_R - BUMP_CONTACT_R:.3f}mm")
    print(f"   headroom: the string may grow to"
          f" {2 * (MARK_CR - SWEPT_Y1 - MARK_BAND_CLR):.2f}mm before the band guard fires"
          f" (cap {MARK_CAP * 2 * (MARK_CR - SWEPT_Y1 - MARK_BAND_CLR) / MARK['text_size_mm'][0]:.2f}mm)"
          f" and {MARK_FACE_W - 2 * MARK_MARGIN:.2f}mm before engrave's margin check does."
          f" The BAND binds first — which is the point of the guard.")
    print(f"   cut {_mark_cut:.3f}mm3 of {_pre_vol:.3f}mm3 (v8.7's mark cut 5.514); bounding"
          f" box unchanged at {_post_dims[0]:.3f} x {_post_dims[1]:.3f} x {_post_dims[2]:.3f}"
          f" — no functional surface moved")


report()

# --- print poses -------------------------------------------------------------------
# Sleeve: +90deg about Y maps world +X to world -Z, so the closed rear end (x=BOX_X) is
# the first layer and the open face points up. 86mm tall, every wall vertical.
pose(sleeve, 90.0)
place(drawer, 0.0, -45.0)
place(sleeve, -40.0, 20.0)
place(bolt, 20.0, 20.0)

# --- export ------------------------------------------------------------------------
# v8.8's DEFAULT PLATE IS THE BOLT ALONE. The project slices print/v8_8_pillbox_plate.stl,
# with no --only, straight from the dashboard, so whatever that file holds is what gets
# printed by "slice v8.8" — and the only thing v8.8 changes is the bolt. The drawer and
# sleeve are the printed, immutable v8.4 parts (the guard block above exists to keep them
# that way); putting them on the plate would spend 4 hours and ~40g reprinting two parts
# byte-for-byte identical to the ones already in the operator's hand. All three are still
# BUILT — the housing carries the fit arithmetic and the mesh envelope assert — and any of
# them can still be exported on its own with --only, which is how a housing reprint would
# be done if it were ever wanted.
PLATE_PART = ONLY.lower() if ONLY else "bolt"
for o in [o for o in bpy.data.objects if PLATE_PART not in o.name.lower()]:
    bpy.data.objects.remove(o, do_unlink=True)
if not bpy.data.objects:
    raise SystemExit(f"v8.8: no part matches --only {ONLY!r}")
place(bpy.data.objects[0], 0.0, 0.0)

print("\nv8.8 PLATE")
for o in bpy.data.objects:
    (x0, x1), (y0, y1), (z0, z1) = extents(o)
    print(f"   {o.name:<12} {x1 - x0:6.2f} x {y1 - y0:6.2f} x {z1 - z0:6.2f}"
          f"   x[{x0:7.2f},{x1:7.2f}] y[{y0:7.2f},{y1:7.2f}] z[{z0:5.2f},{z1:6.2f}]")
    if max(abs(x0), abs(x1), abs(y0), abs(y1)) > PLATE_LIMIT:
        raise SystemExit(f"v8.8: {o.name} leaves the +/-{PLATE_LIMIT}mm plate window")

_parts = list(bpy.data.objects)
for _a in range(len(_parts)):
    for _b in range(_a + 1, len(_parts)):
        (ax0, ax1), (ay0, ay1), _ = extents(_parts[_a])
        (bx0, bx1), (by0, by1), _ = extents(_parts[_b])
        gap = max(bx0 - ax1, ax0 - bx1, by0 - ay1, ay0 - by1)
        if gap < PART_GAP:
            raise SystemExit(f"v8.8: {_parts[_a].name}/{_parts[_b].name} gap {gap:.2f}"
                             f" < {PART_GAP}mm")

name = f"v8_8_pillbox_{ONLY.lower()}.stl" if ONLY else "v8_8_pillbox_plate.stl"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "print", name)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.wm.stl_export(filepath=out, export_selected_objects=True, global_scale=1.0)
print(f"v8.8: wrote {out}")
