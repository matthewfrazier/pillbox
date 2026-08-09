#!/usr/bin/env python3
"""v8.1 — the full credit-card pillbox with the validated v7.4 side-bolt lock.

The product, not a coupon. Sleeve + drawer + bolt, back at the SPEC's thin credit-card
geometry, carrying the lock the v7.1 -> v7.4 coupons converged on.

Everything is modelled in ONE assembly frame so the fit arithmetic is provable, then each
part is rotated/translated into its print pose. Assembly frame:

    X  0..86   travel axis. Sleeve open face at X=0, closed rear at X=86. Drawer exits -X.
    Y  0..54   width. The bolt travels along +Y to lock.
    Z  0..19   height.

CARRIED OVER FROM v7.4 UNCHANGED (validated by hand, not redesigned)
  - Blade bolt cross-section 5.0 (X) x 10.0 (Z). Sliding clearance was 0.25mm/face on the
    coupons; v8.1 opens it to 0.30 because the printed v8.0 was still tight in the hand.
  - Detent in the HOUSING (v7.3): a 1.0 x 15mm cantilever fin in the drawer's front block,
    into two dimples in the bolt's back face — LOCKED 0.7, OPEN 0.45. Fin deflection at
    the crossover is 0.25mm, the low-strain number v7.3's FEA sized, and v8.1 holds it
    there by growing the bump 0.75 -> 0.85 proud to span the wider clearance.
  - The fin prints as a plain vertical wall off the bed, its relief slot open through the
    underside of the front block. Never a horizontal cantilever over air.
  - Thumb PAD, not a thumbnail tab: FULL bolt height, 2.5mm proud, all as vertical ribs so
    the bolt slices bridge-free. v8.1 lengthens it 14 -> 18mm along Y with 5 ridges.
  - Bolt tip FLUSH with the lock boss at LOCKED. Flush reads as locked by fingertip, the
    empty counterbored recess reads as open, nothing protrudes to be knocked back.

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
  4. The fin relief is capped at Z=14.30 instead of running through the top, so the roof
     slab over the channel stays tied to the block's rear wall along its whole length.
     The fin top sits 1.3mm below that cap so a sagging bridge cannot weld it shut.

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
  - Drawer BODY 81.00 x 50.00 x 15.40 (SPEC "approximately 82 x 50.2 x 15.0"). DERIVED
    from the cavity and SPEC's clearances (0.20 each side, 0.20 below, 0.60 to the
    ceiling); the length falls out of the front-block depth the mechanism needs. The
    printed part measures 17.40 tall because the grip knob rises into the roof notch.
  - The LOCK BOSS stands 1.2mm proud, so the widest point is 55.2mm not 54.0mm. Operator
    sanctioned ("that side may need to be thicker or extend slightly"). Its perimeter is
    chamfered 1.4mm, which both keeps it out of bag seams and makes it print supportless.
  - The boss pad is 22 x 14 but CANNOT be centred on the hole: the hole centre is only
    5.5mm from the open face, so the pad runs from the open rim (X=0..22) instead.
  - Sleeve bolt hole is 0.45mm/face clear in X, 0.30mm/face in Z. X accumulates the
    drawer-length tolerance (closed position is set by the drawer's rear face bottoming
    out on the cavity, 81mm away); Z accumulates nothing.
  - The sleeve roof is interrupted at the mouth by the 21mm grip notch, leaving two 16.5mm
    strips of roof either side of it. The side walls carry the mouth, not the roof.
  - Thumb pad crowns sit 2.0mm behind the sleeve rim rather than flush. That distance is
    the retention ligament between the bolt hole and the open face — at flush it was
    2.4mm and the hole's print-ceiling chamfer would have eaten most of it.

DELIBERATELY OMITTED — noted, not silently dropped
  - SPEC's exterior stiffening beads, the ceiling microtexture field, and the
    compartment-floor microtexture.
  - SPEC's three friction detents and their sleeve receivers. The bolt is v8.1's
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

Print: all three as posed, supportless. Sleeve stands on its closed rear end (86mm tall,
open face up) as print/prepare_supportless_plate.py posed v1 — laid flat it would bridge
the whole roof. Drawer bottom-down. Bolt standing, pad as a vertical rib. PETG,
supports=off, orient=off, brim on (the bolt's footprint is ~175mm2).

Usage:  blender -b --factory-startup --python design_v8_1_pillbox.py [-- --only Bolt]
Writes: print/v8_1_pillbox_plate.stl  (or print/v8_1_pillbox_<part>.stl with --only)
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
EDGE_BREAK = 0.5
CAV_X1 = BOX_X - WALL_REAR                             # 84.20
CAV_Y0, CAV_Y1 = WALL_SIDE, BOX_Y - WALL_SIDE          # 1.80 .. 52.20
CAV_Z0, CAV_Z1 = WALL_FACE, BOX_Z - WALL_FACE          # 1.40 .. 17.60

# --- drawer, DERIVED from the cavity + SPEC clearances -----------------------------
CLR_SIDE, CLR_BELOW, CLR_ABOVE = 0.20, 0.20, 0.60
DR_Y0, DR_Y1 = CAV_Y0 + CLR_SIDE, CAV_Y1 - CLR_SIDE    # 2.00 .. 52.00
DR_Z0, DR_Z1 = CAV_Z0 + CLR_BELOW, CAV_Z1 - CLR_ABOVE  # 1.60 .. 17.00
DR_WALL, DR_DIV, DR_FLOOR = 1.5, 1.2, 1.2
N_COMPARTMENTS = 3

# --- bolt + channel, X chain from the thumb ridges backwards -----------------------
CLR = 0.30                                             # v8.1: 0.25 -> 0.30, still tight
BOLT_T, BOLT_H = 5.0, 10.0
TRAVEL = 5.0
PAD_PROUD, PAD_L = 2.5, 18.0                           # v8.1: 14 -> 18 along Y
RIDGE_P, RIDGE_W, RIDGE_N = 0.5, 1.2, 5                # v8.1: 4 -> 5 ridges
PAD_TIP_GAP = 3.4
RIDGE_X0 = 2.0                                         # crowns sit 2.0 behind the rim
PAD_X0 = RIDGE_X0 + RIDGE_P                            # 2.50
BOLT_X0 = PAD_X0 + PAD_PROUD                           # 5.00
BOLT_X1 = BOLT_X0 + BOLT_T                             # 10.00
CH_X0, CH_X1 = BOLT_X0 - CLR, BOLT_X1 + CLR            # 4.75 .. 10.25
DR_X0 = CH_X0 - DR_WALL                                # 3.25  drawer front face
DR_X1 = CAV_X1                                         # 84.20 rear face = closed stop
DR_L = DR_X1 - DR_X0                                   # 80.95

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

# --- Y chain -----------------------------------------------------------------------
BOSS_T = 3.0
BOSS_Y1 = CAV_Y1 + BOSS_T                              # 55.20 boss outer face
TIP_LOCKED = BOSS_Y1                                   # flush
TIP_OPEN = TIP_LOCKED - TRAVEL                         # 50.20 vs drawer inner wall 50.50
BOLT_L = 45.0                                          # guide length, not travel: see report
TAIL_LOCKED = TIP_LOCKED - BOLT_L                      # 10.20
CH_Y0 = 4.5                                            # closed bore end, 1.0 of -Y wall left
CH_Y1 = DR_Y1 + 0.1                                    # bores through the +Y side wall

PAD_Y1_LOCKED = TIP_LOCKED - PAD_TIP_GAP               # 51.80
PAD_Y0_LOCKED = PAD_Y1_LOCKED - PAD_L                  # 37.80
SLOT_Y0 = PAD_Y0_LOCKED - TRAVEL - 0.2                 # 32.60  closed: the OPEN stop
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
KNOB_R = NOTCH_R - KNOB_CLR                            # 10.20, arc SHARES the notch centre
KNOB_X1 = NOTCH_CX + KNOB_R                            # 12.70, i.e. KNOB_CLR shy of NOTCH_D
KNOB_Z1 = BOX_Z                                        # 19.00 flush with the outer roof
KNOB_CHAMFER = 0.4
GROOVE_R, GROOVE_D, GROOVE_N = 0.6, 0.5, 4             # crowns stay flush at KNOB_Z1

# The pad slot grew with the longer pad, so the fin relief slides -Y to keep the two from
# overlapping — that separation is what keeps the bore roof supported (see BRIDGES).
RELIEF_Y0, RELIEF_Y1 = 9.6, 26.6
RELIEF_Z1 = 14.30                                      # capped: keeps the roof slab tied
FIN_Y1 = RELIEF_Y1                                     # anchored edge
FIN_Y0 = FIN_Y1 - FIN_LEN                              # 11.60 free edge
FIN_Z1 = 13.00                                         # 1.3 below the relief cap
# BUMP_PROUD grows 0.10, not 0.05: widening CLR moves the channel wall AND the fin's
# standoff behind it, so the bump has two 0.05 steps to make up. Interference is then
# unchanged at 0.25 — see report(), which computes it rather than asserting it.
BUMP_Y, BUMP_R, BUMP_PROUD = 14.6, 1.1, 0.85
DIMPLE_R = 1.1
DIMPLE_LOCK_D, DIMPLE_OPEN_D = 0.7, 0.45
DIMPLE_LOCK_Y = BUMP_Y                                 # bolt is modelled at LOCKED
DIMPLE_OPEN_Y = BUMP_Y + TRAVEL

# --- lock boss + hole --------------------------------------------------------------
BOSS_X0, BOSS_X1 = 0.0, 22.0
BOSS_Z0, BOSS_Z1 = ZC - 7.0, ZC + 7.0                  # 2.30 .. 16.30
BOSS_CHAMFER = 1.4
HOLE_CLR_X, HOLE_CLR_Z = 0.45, 0.30                    # v8.1: both +0.05 with CLR
HOLE_X0, HOLE_X1 = BOLT_X0 - HOLE_CLR_X, BOLT_X1 + HOLE_CLR_X   # 4.55 .. 10.45
HOLE_Z0, HOLE_Z1 = BOLT_Z0 - HOLE_CLR_Z, BOLT_Z1 + HOLE_CLR_Z   # 4.00 .. 14.60
HOLE_CH = 2.30                                         # print-ceiling corners of the hole
CBORE_D, CBORE_OVER, CBORE_CH = 0.6, 0.4, 2.6

PLATE_LIMIT, PART_GAP = 115.0, 12.0


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
sleeve = bevel(box("Sleeve_V81", 0, BOX_X, 0, BOX_Y, 0, BOX_Z), EDGE_BREAK)
sleeve = combine(sleeve, bevel(box("boss", BOSS_X0, BOSS_X1, CAV_Y1 - 1.2, BOSS_Y1,
                                   BOSS_Z0, BOSS_Z1), BOSS_CHAMFER, segments=2), "UNION")
sleeve = combine(sleeve, box("cavity", -1.0, CAV_X1, CAV_Y0, CAV_Y1, CAV_Z0, CAV_Z1),
                 "DIFFERENCE")

# Bolt hole. Standing on its rear end the sleeve prints with Z' = 86 - X, so the hole's
# LOW-X face is its ceiling and the span that would bridge is the hole's full Z extent.
# Chamfer both corners of that face 45deg: 10.50 -> 6.10mm.
hole = box("hole", HOLE_X0, HOLE_X1, CAV_Y1 - 0.2, BOSS_Y1 + 0.1, HOLE_Z0, HOLE_Z1)
hole = combine(hole, wedge("hw_t", HOLE_X0, HOLE_Z1, -1, +1, HOLE_CH,
                           CAV_Y1 - 0.4, BOSS_Y1 + 0.3), "DIFFERENCE")
hole = combine(hole, wedge("hw_b", HOLE_X0, HOLE_Z0, -1, -1, HOLE_CH,
                           CAV_Y1 - 0.4, BOSS_Y1 + 0.3), "DIFFERENCE")
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

# U notch through the roof at the open end. Stood on its rear end the sleeve prints with
# this notch at the very TOP, and the void only ever widens going up, so the surrounding
# roof is a subset of the layer below it: nothing bridges and nothing overhangs.
notch = box("notch", -1.0, NOTCH_CX, NOTCH_Y0, NOTCH_Y1, CAV_Z1 - 0.1, BOX_Z + 0.5)
notch = combine(notch, cylinder_z("notcharc", NOTCH_CX, NOTCH_YC, CAV_Z1 - 0.1,
                                  BOX_Z + 0.5, NOTCH_R), "UNION")
sleeve = combine(sleeve, notch, "DIFFERENCE")

# --- DRAWER ------------------------------------------------------------------------
drawer = bevel(box("Drawer_V81", DR_X0, DR_X1, DR_Y0, DR_Y1, DR_Z0, DR_Z1), EDGE_BREAK)
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
chan = box("channel", CH_X0, CH_X1, CH_Y0, CH_Y1, CH_Z0, CH_Z1)
chan = combine(chan, wedge("cf", CH_X0, CH_Z1, -1, +1, CHAN_CF, CH_Y0 - 0.2, SLOT_Y0),
               "DIFFERENCE")
chan = combine(chan, wedge("cb1", CH_X1, CH_Z1, +1, +1, CHAN_CB, CH_Y0 - 0.2, RELIEF_Y0),
               "DIFFERENCE")
chan = combine(chan, wedge("cb2", CH_X1, CH_Z1, +1, +1, CHAN_CB, RELIEF_Y1, CH_Y1 + 0.2),
               "DIFFERENCE")
drawer = combine(drawer, chan, "DIFFERENCE")

# Pad slot: the one opening in the bore. Closed at -Y (the OPEN hard stop), open at its
# +Y mouth, which is the musket-load insertion path.
drawer = combine(drawer, box("slot", SLOT_X0, SLOT_X1, SLOT_Y0, SLOT_Y1, CH_Z0, CH_Z1),
                 "DIFFERENCE")
# Fin relief: open through the UNDERSIDE so the fin prints as a plain vertical wall off
# the bed, but CAPPED at RELIEF_Z1 so the roof slab over the bore stays tied to the block's
# rear wall along its whole length. The fin stops 1.3mm below that cap so a sagging bridge
# cannot weld it shut.
drawer = combine(drawer, box("relief", CH_X1, RELIEF_X1, RELIEF_Y0, RELIEF_Y1,
                             DR_Z0 - 0.5, RELIEF_Z1), "DIFFERENCE")
drawer = combine(drawer, box("fin", FIN_X0, FIN_X1, FIN_Y0, FIN_Y1 + 0.5, DR_Z0, FIN_Z1),
                 "UNION")
drawer = combine(drawer, sphere("bump", FIN_X0 + BUMP_R - BUMP_PROUD, BUMP_Y, ZC, BUMP_R),
                 "UNION")

# Grip knob on the drawer's TOP, sharing the notch's arc centre so clearance is a uniform
# KNOB_CLR all the way round. Clipped at the drawer's front face: any part hanging past it
# would print over air. Everything here faces up — knob, cone cap, grooves — so the drawer
# stays bridge-free in its bottom-down orientation.
knob = cylinder_z("knob", NOTCH_CX, NOTCH_YC, DR_Z1 - 0.75, KNOB_Z1 - KNOB_CHAMFER,
                  KNOB_R)
knob = combine(knob, cone_z("knobcap", NOTCH_CX, NOTCH_YC, KNOB_Z1 - KNOB_CHAMFER,
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
bolt = bevel(box("Bolt_V81", BOLT_X0, BOLT_X1, TAIL_LOCKED, TIP_LOCKED, BOLT_Z0, BOLT_Z1),
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


# --- build report: every number below is derived, none is asserted by hand -----------
DR_INNER_Y = DR_Y1 - DR_WALL
BRIDGES = [
    ("drawer", "bore roof, plain run", (CH_X1 - CHAN_CB) - (CH_X0 + CHAN_CF),
     f"y {CH_Y0:.1f}-{RELIEF_Y0:.1f} and {RELIEF_Y1:.1f}-{SLOT_Y0:.1f}; both roof corners"
     " chamfered"),
    ("drawer", "bore roof over fin relief", CH_X1 - (CH_X0 + CHAN_CF),
     f"y {RELIEF_Y0:.1f}-{RELIEF_Y1:.1f}; back chamfer omitted, its wall is the relief"),
    ("drawer", "bore roof over pad slot", (CH_X1 - CHAN_CB) - DR_X0,
     f"y {SLOT_Y0:.1f}-{CH_Y1:.1f}; front chamfer omitted, the slot IS the front wall"),
    ("drawer", "fin relief cap", RELIEF_X1 - CH_X1,
     f"z {RELIEF_Z1:.2f}, y {RELIEF_Y0:.1f}-{RELIEF_Y1:.1f}; ties the roof slab to the"
     " rear wall"),
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
]


def report():
    print("\nv8.1 Y-STACK (mm, along the bolt axis)")
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
        ("sleeve nominal outer", BOX_Y, f"nominal wall {WALL_SIDE}"),
        ("boss outer face", BOSS_Y1,
         f"boss wall {BOSS_T}, stands {BOSS_Y1 - BOX_Y:.2f} proud of the 54mm face"),
    ]:
        print(f"   y={y:7.2f}  {label:<24} {note}")
    print(f"   blade {BOLT_T}x{BOLT_H} x {BOLT_L} long   travel {TRAVEL:.2f}")
    print(f"   LOCKED tip y={TIP_LOCKED:.2f} vs boss face y={BOSS_Y1:.2f}"
          f" -> flush by {BOSS_Y1 - TIP_LOCKED:+.2f};"
          f" engagement in the sleeve wall {TIP_LOCKED - CAV_Y1:.2f}")
    print(f"   OPEN   tip y={TIP_OPEN:.2f} vs drawer inner wall y={DR_INNER_Y:.2f}"
          f" -> clear by {DR_INNER_Y - TIP_OPEN:.2f};"
          f" clear of the sleeve wall by {CAV_Y1 - TIP_OPEN:.2f}")
    print(f"   travel needed to clear the drawer's own wall = {TIP_LOCKED - DR_INNER_Y:.2f}"
          f"; to merely clear the sleeve = {TIP_LOCKED - CAV_Y1:.2f}; using {TRAVEL:.2f}")
    print(f"   GUIDE engaged inside the drawer: LOCKED {DR_Y1 - TAIL_LOCKED:.2f}"
          f" ({(DR_Y1 - TAIL_LOCKED) / BOLT_T:.1f}:1 on a {BOLT_T}mm shaft),"
          f" OPEN {BOLT_L:.2f} ({BOLT_L / BOLT_T:.1f}:1)")
    print(f"   pad @LOCKED ends y={PAD_Y1_LOCKED:.2f}; sleeve wall at y={CAV_Y1:.2f}"
          f" -> max over-travel {CAV_Y1 - PAD_Y1_LOCKED:.2f}")
    print(f"   pad @OPEN starts y={PAD_Y0_LOCKED - TRAVEL:.2f}; slot closed at"
          f" y={SLOT_Y0:.2f} -> OPEN hard stop, slack {PAD_Y0_LOCKED - TRAVEL - SLOT_Y0:.2f}")

    print("\nv8.1 DRAWER vs CAVITY")
    print(f"   Y  drawer {DR_Y0:.2f}..{DR_Y1:.2f} in cavity {CAV_Y0:.2f}..{CAV_Y1:.2f}"
          f"  -> {DR_Y0 - CAV_Y0:.2f} / {CAV_Y1 - DR_Y1:.2f} per side")
    print(f"   Z  drawer {DR_Z0:.2f}..{DR_Z1:.2f} in cavity {CAV_Z0:.2f}..{CAV_Z1:.2f}"
          f"  -> {DR_Z0 - CAV_Z0:.2f} below / {CAV_Z1 - DR_Z1:.2f} above")
    print(f"   X  drawer {DR_X0:.2f}..{DR_X1:.2f}, cavity ends {CAV_X1:.2f}"
          f"  -> the rear face IS the closed stop; front face {DR_X0:.2f} behind the rim")
    print(f"   drawer body {DR_L:.2f} x {DR_Y1 - DR_Y0:.2f} x {DR_Z1 - DR_Z0:.2f}"
          f"; front block {FB_X1 - DR_X0:.2f} deep")
    _kx0 = DR_X0
    _khw = (KNOB_R ** 2 - (_kx0 - NOTCH_CX) ** 2) ** 0.5
    _nhw = (NOTCH_R ** 2 - (_kx0 - NOTCH_CX) ** 2) ** 0.5
    print(f"\nv8.1 TOP GRIP")
    print(f"   sleeve roof notch: U, {NOTCH_W:.1f} wide x {NOTCH_D:.1f} deep in X,"
          f" semicircular end r={NOTCH_R:.2f} at x={NOTCH_CX:.2f}, y"
          f" {NOTCH_Y0:.2f}-{NOTCH_Y1:.2f}; cut through the roof z"
          f" {CAV_Z1:.2f}-{BOX_Z:.2f}, open at the mouth")
    print(f"   drawer knob: arc r={KNOB_R:.2f} on the SAME centre -> uniform"
          f" {KNOB_CLR:.2f} clearance; x {DR_X0:.2f}-{KNOB_X1:.2f}"
          f" ({KNOB_X1 - DR_X0:.2f} long), width {2 * _khw:.2f} at its front vs notch"
          f" {2 * _nhw:.2f} there")
    print(f"   knob z {DR_Z1:.2f}-{KNOB_Z1:.2f} = {KNOB_Z1 - DR_Z1:.2f} tall"
          f" ({CAV_Z1 - DR_Z1:.2f} ceiling gap + {BOX_Z - CAV_Z1:.2f} roof), top FLUSH"
          f" with the sleeve outer roof; {GROOVE_N} grooves {GROOVE_D} deep, crowns flush")
    print(f"   closed: knob's +X end at {KNOB_X1:.2f} vs notch end {NOTCH_D:.2f}"
          f" -> {NOTCH_D - KNOB_X1:.2f} gap, and that contact reads as SHUT")
    print(f"   withdrawing moves the knob -X; its arc centre leaves the notch's, so"
          f" clearance only grows. Knob max width {2 * KNOB_R:.2f} in a"
          f" {NOTCH_W:.2f} slot -> {KNOB_CLR:.2f}/side all the way out")
    print(f"   compartments {N_COMPARTMENTS} x {COMP_LEN:.2f} long,"
          f" {DR_Y1 - DR_Y0 - 2 * DR_WALL:.2f} wide, {DR_Z1 - DR_Z0 - DR_FLOOR:.2f} deep;"
          f" dividers {DR_DIV}")

    print("\nv8.1 DETENT")
    _fin_l = FIN_Y1 - FIN_Y0
    _defl = BOLT_X1 - (FIN_X0 - BUMP_PROUD)
    _strain = 3 * FIN_T * _defl / (2 * _fin_l ** 2)
    print(f"   fin {FIN_T} x {_fin_l:.1f} long x {FIN_Z1 - DR_Z0:.2f} tall,"
          f" anchored at y={FIN_Y1:.1f}, free at y={FIN_Y0:.1f}, {FIN_FREE} behind it")
    print(f"   bump crown x={FIN_X0 - BUMP_PROUD:.2f} vs blade back face x={BOLT_X1:.2f}"
          f"  -> deflection at the crossover {_defl:.2f} (UNCHANGED from v8.0)")
    print(f"   fin strain 3*t*d/(2*L^2) = {_strain * 100:.3f}% vs PETG yield ~2%")
    print(f"   bump sinks {BUMP_PROUD - (FIN_X0 - BOLT_X1):.2f} below the blade face when"
          f" relaxed; both dimples are deeper than that, so it never bottoms out")
    print(f"   dimples LOCKED {DIMPLE_LOCK_D} deep, OPEN {DIMPLE_OPEN_D} deep;"
          f" bolt-local y {DIMPLE_LOCK_Y - TAIL_LOCKED:.2f} and"
          f" {DIMPLE_OPEN_Y - TAIL_LOCKED:.2f} of {BOLT_L:.1f}")

    print("\nv8.1 BRIDGED FACES (flat span that must bridge, mm)")
    for part, what, span, why in BRIDGES:
        print(f"   {part:<7} {what:<26} {span:5.2f}  {why}")


report()

# --- print poses -------------------------------------------------------------------
# Sleeve: +90deg about Y maps world +X to world -Z, so the closed rear end (x=BOX_X) is
# the first layer and the open face points up. 86mm tall, every wall vertical.
pose(sleeve, 90.0)
place(drawer, 0.0, -45.0)
place(sleeve, -40.0, 20.0)
place(bolt, 20.0, 20.0)

# --- export ------------------------------------------------------------------------
if ONLY:
    for o in [o for o in bpy.data.objects if ONLY.lower() not in o.name.lower()]:
        bpy.data.objects.remove(o, do_unlink=True)
    if not bpy.data.objects:
        raise SystemExit(f"v8.1: no part matches --only {ONLY!r}")
    place(bpy.data.objects[0], 0.0, 0.0)

print("\nv8.1 PLATE")
for o in bpy.data.objects:
    (x0, x1), (y0, y1), (z0, z1) = extents(o)
    print(f"   {o.name:<12} {x1 - x0:6.2f} x {y1 - y0:6.2f} x {z1 - z0:6.2f}"
          f"   x[{x0:7.2f},{x1:7.2f}] y[{y0:7.2f},{y1:7.2f}] z[{z0:5.2f},{z1:6.2f}]")
    if max(abs(x0), abs(x1), abs(y0), abs(y1)) > PLATE_LIMIT:
        raise SystemExit(f"v8.1: {o.name} leaves the +/-{PLATE_LIMIT}mm plate window")

_parts = list(bpy.data.objects)
for _a in range(len(_parts)):
    for _b in range(_a + 1, len(_parts)):
        (ax0, ax1), (ay0, ay1), _ = extents(_parts[_a])
        (bx0, bx1), (by0, by1), _ = extents(_parts[_b])
        gap = max(bx0 - ax1, ax0 - bx1, by0 - ay1, ay0 - by1)
        if gap < PART_GAP:
            raise SystemExit(f"v8.1: {_parts[_a].name}/{_parts[_b].name} gap {gap:.2f}"
                             f" < {PART_GAP}mm")

name = f"v8_1_pillbox_{ONLY.lower()}.stl" if ONLY else "v8_1_pillbox_plate.stl"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "print", name)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.wm.stl_export(filepath=out, export_selected_objects=True, global_scale=1.0)
print(f"v8.1: wrote {out}")
