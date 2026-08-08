#!/usr/bin/env python3
"""v7.4 side-bolt lock — blade bolt + full-thumb pad (run inside Blender).

Driven by the hand test of the printed coupon. Operator findings and the response:

  "bolt wiggles a bit"            -> cross-section 3x4.5 -> 5x10mm. Angular slop at the
                                    same 0.25mm/face clearance falls 6.3deg -> 2.9deg,
                                    and shear area goes 13.5 -> 50mm2 (~700N, vs a
                                    20-50N bag snag). A blade that BEARS on the hole,
                                    not a pin that pivots in it.
  "shaft extends well past wall,
   invites accidental disengage"  -> travel 3.25 -> 3.4mm into a 3.5mm wall, so the tip
                                    lands FLUSH (0.1mm shy) instead of proud. Nothing
                                    stands out to be knocked back.
  "requires sneaking a thumbnail
   into the slide"                -> the tab becomes a PAD: 14mm long x 8mm tall,
                                    standing 2.5mm proud of the pull face with 4 ridges.
                                    A whole thumb pushes it in shear, which is also what
                                    makes the detent perceptible — you can't feel a click
                                    through a fingernail fighting channel friction.
  "can't feel the dimple"         -> detent stays on the pull's fin (v7.3) but the locked
                                    dimple deepens 0.5 -> 0.7mm, and the fin lengthens
                                    12 -> 15mm so it deflects with less force per mm.
  "cruft on one edge, may need
   filing down"                   -> NOT bridging: the v7.3 bar sliced with zero bridge or
                                    overhang features. It is brim tear-off — 5mm of brim at
                                    a 0.1mm object gap welds itself to a small part. This
                                    bar's footprint nearly doubles (86 -> 165mm2) so it
                                    needs far less help: print with brim=3, and slice.sh
                                    now uses brim_object_gap 0.2 so brim snaps off clean.

Hollow-vs-solid: modelled solid. At 5x10 the slicer's own sparse infill leaves it hollow
between two perimeters, which is the strength/weight point of a hollow bolt without the
geometry (or the print risk of thin internal walls).

Sizing note: the bolt's 10mm height is the vertical axis of the real box, whose drawer
front is ~15mm tall — hence PULL_Z = 15 with 2.25mm walls above and below the channel.
This coupon is dimensionally honest about that constraint.

Parts: PULL (channel + fin detent + thumb slot), BAR (blade bolt + thumb pad), SHEATH
(sleeve section with the 3.5mm lock wall). Assembly: bar slides in from the pull's side
face, sheath slides over. No print-in-place.

Print: as modelled, supportless. PETG, supports=off, orient=off, brim=3.

Usage:  blender -b --factory-startup --python design_v7_4_blade_bolt.py [-- --only Bar]
Writes: print/v7_4_blade_bolt_plate.stl  (or ..._<part>.stl with --only)
"""
import os
import sys

import bpy

_argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ONLY = _argv[_argv.index("--only") + 1] if "--only" in _argv else None

# --- parameters (mm) -------------------------------------------------------------
CLR = 0.25                                    # validated by hand: snug, keep it
BAR_T, BAR_H, BAR_L = 5.0, 10.0, 22.0         # blade bolt: was 3.0 x 4.5 x 20
PULL_Y, PULL_X, PULL_Z = 32.0, 12.0, 15.0     # PULL_Z = real drawer-front height
WALL_F = 1.6
CH_X0 = WALL_F
CH_X1 = CH_X0 + BAR_T + 2 * CLR               # 7.1
CH_Z0 = (PULL_Z - (BAR_H + 2 * CLR)) / 2      # centred: 2.25
CH_Z1 = CH_Z0 + BAR_H + 2 * CLR               # 12.75
CH_YEND = 23.0
TRAVEL = 3.4                                  # into a 3.5mm wall -> tip sits flush
# thumb pad: whole thumb, not a nail. FULL bar height on purpose — a centred pad
# overhangs its own underside (v7.4's first slice grew bridges the v7.3 bar never had),
# and full height is more thumb contact anyway.
PAD_L, PAD_H, PAD_PROUD = 14.0, 10.0, 2.5
PAD_Y0 = 6.0
RIDGE_W, RIDGE_P, RIDGE_N = 1.2, 0.6, 4
FIN_T, FIN_Y0, FIN_Y1 = 1.0, 5.0, 20.0        # 15mm long: softer, more perceptible click
FIN_X0 = CH_X1 + CLR
BUMP_R, BUMP_PROUD = 1.1, 0.85
BUMP_Y = 7.0
DIMPLE_R = 1.1
DIMPLE_LOCK_D, DIMPLE_OPEN_D = 0.7, 0.45      # locked holds harder than open
OPEN_DIMPLE_Y = BUMP_Y
LOCK_DIMPLE_Y = BUMP_Y + TRAVEL
SLEEVE_SIDE, SLEEVE_WALL, SLEEVE_LEN = 3.5, 1.6, 12.0
ZC = (CH_Z0 + CH_Z1) / 2


def box(name, x0, x1, y0, y1, z0, z1):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object
    o.name = name
    o.dimensions = (x1 - x0, y1 - y0, z1 - z0)
    o.location = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def sphere(name, x, y, z, r):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, y, z), segments=24, ring_count=12)
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


bpy.ops.wm.read_factory_settings(use_empty=True)

# --- PULL -------------------------------------------------------------------------
pull = box("Pull_V74", 0, PULL_X, 0, PULL_Y, 0, PULL_Z)
# blade channel, open through the side face (y=0), closed stop at CH_YEND
pull = combine(pull, box("channel", CH_X0, CH_X1, -0.1, CH_YEND, CH_Z0, CH_Z1), "DIFFERENCE")
# thumb slot: the pad must travel its own length PLUS the lock travel, and is open at the
# side edge so the pad enters with the bar
pull = combine(pull, box("slot", -0.1, WALL_F + 0.1, -0.1, PAD_Y0 + PAD_L + TRAVEL + 1.0,
                         CH_Z0 - CLR, CH_Z1 + CLR), "DIFFERENCE")
# relief for the detent fin: open through the BACK face and the TOP so the fin prints as
# a plain vertical wall off the bed — nothing bridges
pull = combine(pull, box("relief", CH_X1, PULL_X + 0.1, FIN_Y0 - 2.0, FIN_Y1,
                         -0.1, PULL_Z + 0.1), "DIFFERENCE")
pull = combine(pull, box("fin", FIN_X0, FIN_X0 + FIN_T, FIN_Y0, FIN_Y1, 0, PULL_Z), "UNION")
pull = combine(pull, sphere("bump", FIN_X0 + BUMP_R - BUMP_PROUD, BUMP_Y, ZC, BUMP_R), "UNION")

# --- BAR: blade bolt + thumb pad (modelled in print orientation — standing) --------
bar = box("Bar_V74", 0, BAR_T, 0, BAR_L, 0, BAR_H)
# thumb pad, proud of the bar's front face; spans PAD_H of the bar's 10mm height
pad_z0, pad_z1 = (BAR_H - PAD_H) / 2, (BAR_H + PAD_H) / 2
bar = combine(bar, box("pad", -PAD_PROUD, 0.1, PAD_Y0, PAD_Y0 + PAD_L, pad_z0, pad_z1), "UNION")
# ridges across the pad, so thumb shear has something to bite
for i in range(RIDGE_N):
    ry = PAD_Y0 + 2.0 + i * (PAD_L - 4.0) / (RIDGE_N - 1)
    bar = combine(bar, box("ridge", -PAD_PROUD - RIDGE_P, -PAD_PROUD + 0.1,
                           ry, ry + RIDGE_W, pad_z0 + 0.8, pad_z1 - 0.8), "UNION")
# detent dimples in the back face, where the pull's fin bump rides
for dy, depth in ((OPEN_DIMPLE_Y, DIMPLE_OPEN_D), (LOCK_DIMPLE_Y, DIMPLE_LOCK_D)):
    bar = combine(bar, sphere("dimple", BAR_T + DIMPLE_R - depth, dy, BAR_H / 2,
                              DIMPLE_R), "DIFFERENCE")
bar.location = (18.0, 40.0, 0)
bpy.context.view_layer.objects.active = bar
bpy.ops.object.transform_apply(location=True)

# --- SHEATH (modelled upside down: top plate on the bed) --------------------------
IN_X, IN_Y = PULL_Z + 0.5, PULL_Y + 0.5
OUT_X = IN_X + 2 * SLEEVE_WALL
OUT_Y = IN_Y + SLEEVE_SIDE + SLEEVE_WALL
sheath = box("Sheath_V74", 0, OUT_X, 0, OUT_Y, 0, SLEEVE_LEN)
sheath = combine(sheath, box("cavity", SLEEVE_WALL, SLEEVE_WALL + IN_X,
                             SLEEVE_SIDE, SLEEVE_SIDE + IN_Y, -0.1, SLEEVE_LEN + 0.1),
                 "DIFFERENCE")
# bolt hole: matches the blade + clearance, so the blade BEARS on it rather than pivoting
px = SLEEVE_WALL + 0.25
sheath = combine(sheath, box("hole", px + CH_Z0 - 0.3, px + CH_Z1 + 0.3,
                             -0.1, SLEEVE_SIDE + 0.1,
                             0.5 + CH_X0 - 0.3 + CLR, 0.5 + CH_X1 + 0.3 - CLR),
                 "DIFFERENCE")
sheath.location = (40.0, 0, 0)
bpy.context.view_layer.objects.active = sheath
bpy.ops.object.transform_apply(location=True)

# --- export ----------------------------------------------------------------------
if ONLY:
    for o in [o for o in bpy.data.objects if ONLY.lower() not in o.name.lower()]:
        bpy.data.objects.remove(o, do_unlink=True)
    if not bpy.data.objects:
        raise SystemExit(f"v7.4: no part matches --only {ONLY!r}")
    obj = bpy.data.objects[0]
    obj.location = (-obj.dimensions.x / 2, -obj.dimensions.y / 2, obj.location.z)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True)

for o in bpy.data.objects:
    print(f"v7.4: {o.name} dims={[round(d, 2) for d in o.dimensions]}")
name = f"v7_4_blade_bolt_{ONLY.lower()}.stl" if ONLY else "v7_4_blade_bolt_plate.stl"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "print", name)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.wm.stl_export(filepath=out, export_selected_objects=True, global_scale=1.0)
print(f"v7.4: wrote {out}")
