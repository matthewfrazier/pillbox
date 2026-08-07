#!/usr/bin/env python3
"""v7.1 bolt-in-pull lock — working prototype coupon (run inside Blender).

Revision of the v7 slide-lock after operator review: the v7.0 coupon dedicated a
whole frame face to the slider. v7.1 hides the mechanism INSIDE the drawer pull
instead, and the sleeve ("sheath") only needs a hole:

  PULL   — stand-in for the drawer front: a vertical channel inside the pull holds
           the bolt bar; a slot in the front face exposes the bar's thumb ridges
           (recessed 0.3 mm below the face — bag rub touches the face, not the bar).
           Thumb slides UP to lock, DOWN to open. 3.25 mm travel.
  BAR    — the solid bolt: top end exits through the pull's top into the sheath
           hole. Lower half is split into two prongs with outward detent bumps —
           a pen-clip-style clicker giving a positive click at both LOCKED and
           OPEN. The LOCKED dimple is deeper/steeper than OPEN because bag
           pressure on the flush bolt pushes toward unlock.
  SHEATH — stand-in for the sleeve top: a U-bracket that slides over the pull.
           Its top plate has the bolt hole. LOCKED: bar fills the hole flush with
           the outer surface (thumb reads FLAT). OPEN: the hole is an empty
           3 mm recess (thumb reads HOLE). Locked bar blocks the sheath from
           sliding off — the actual lock function.

Assembly: drop the bar into the pull channel from the top (tab rides the slot,
which is open at the top). Slide the sheath over the pull. No print-in-place.

Print: all three parts flat/upright as laid out, supportless. PETG,
supports=off, orient=off. Clearances 0.25 mm per sliding face.

Usage:  blender -b --factory-startup --python design_v7_1_bolt_in_pull_proto.py
Writes: print/v7_1_bolt_in_pull_proto_plate.stl
"""
import os

import bpy

# --- parameters (mm) -------------------------------------------------------------
CLR = 0.25
# pull block (drawer-front stand-in), origin at its front-left-bottom corner
PULL_Y, PULL_X, PULL_Z = 32.0, 8.0, 14.0     # width, depth, height
WALL_F = 1.6                                  # front face wall the slot pierces
BAR_W, BAR_T, BAR_L = 8.0, 3.0, 13.0          # bolt bar: width(Y) x thick(X) x long(Z)
TRAVEL = 3.25
CH_Y0 = (PULL_Y - BAR_W) / 2 - CLR            # channel: bar + clearance
CH_Y1 = CH_Y0 + BAR_W + 2 * CLR
CH_X0, CH_X1 = WALL_F, WALL_F + BAR_T + 2 * CLR
CH_FLOOR = 1.0                                # bar rests here at OPEN; top flush with pull
TAB_W, TAB_D = 6.0, 0.8                       # thumb tab through the front slot
RIDGE_H, RIDGE_P = 0.9, 0.5                   # ridge height(z) and proudness(x); crest 0.3 inset
TAB_Z0, TAB_Z1 = 3.0, 9.0                     # tab span on the bar (local z)
PRONG_SLIT = 2.0                              # split the bar's lower half into two prongs
BUMP_R, BUMP_P = 0.9, 0.35                    # prong detent bumps (outward, +-Y)
BUMP_Z = 2.0                                  # bump center height on the bar (local)
DIMPLE_R = 0.9
DIMPLE_LOCK_D, DIMPLE_OPEN_D = 0.5, 0.3       # locked detent holds harder than open
# sheath U-bracket
SH_TOP, SH_WALL, SH_DROP = 3.0, 2.0, 10.0
YC = PULL_Y / 2


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

# --- PULL (printed upright as modeled: channel and slot are vertical, supportless)
pull = box("Pull_V71", 0, PULL_X, 0, PULL_Y, 0, PULL_Z)
# vertical bolt channel, open through the top
pull = combine(pull, box("channel", CH_X0, CH_X1, CH_Y0, CH_Y1,
                         CH_FLOOR, PULL_Z + 0.1), "DIFFERENCE")
# front slot exposing the thumb tab, open at the top for bar insertion
pull = combine(pull, box("slot", -0.1, WALL_F + 0.1, YC - TAB_W / 2 - CLR,
                         YC + TAB_W / 2 + CLR, TAB_Z0 + CH_FLOOR, PULL_Z + 0.1), "DIFFERENCE")
# detent dimples in BOTH channel side walls at OPEN (bar on floor) and LOCKED (raised) heights
for ywall, sgn in ((CH_Y0, -1), (CH_Y1, 1)):
    for z, depth in ((CH_FLOOR + BUMP_Z, DIMPLE_OPEN_D),
                     (CH_FLOOR + BUMP_Z + TRAVEL, DIMPLE_LOCK_D)):
        pull = combine(pull, sphere("dimple", (CH_X0 + CH_X1) / 2,
                                    ywall + sgn * (DIMPLE_R - depth), z, DIMPLE_R), "DIFFERENCE")

# --- BAR (printed lying on its back: tab + ridges up, prong bumps sideways) ------
# modeled in PLACE first (standing in the channel), then laid down for the plate
bar = box("Bar_V71", 0, BAR_T, 0, BAR_W, 0, BAR_L)
# thumb tab + ridges on the front (-x becomes front when in the pull; model tab at x<0)
bar = combine(bar, box("tab", -TAB_D, 0.1, BAR_W / 2 - TAB_W / 2,
                       BAR_W / 2 + TAB_W / 2, TAB_Z0, TAB_Z1), "UNION")
for rz in (3.8, 5.6, 7.4):
    bar = combine(bar, box("ridge", -TAB_D - RIDGE_P, -TAB_D + 0.1,
                           BAR_W / 2 - TAB_W / 2 + 0.5, BAR_W / 2 + TAB_W / 2 - 0.5,
                           rz, rz + RIDGE_H), "UNION")
# split the lower half into two prongs (the clicker spring)
bar = combine(bar, box("slit", -0.1, BAR_T + 0.1, BAR_W / 2 - PRONG_SLIT / 2,
                       BAR_W / 2 + PRONG_SLIT / 2, -0.1, 6.0), "DIFFERENCE")
# outward detent bumps at the prong tips: center sits inside the prong so only
# BUMP_P of the sphere protrudes past the bar's side face
for y, sgn in ((0, -1), (BAR_W, 1)):
    bar = combine(bar, sphere("bump", BAR_T / 2, y + sgn * (BUMP_P - BUMP_R),
                              BUMP_Z, BUMP_R), "UNION")
# lay the bar on its back for printing: rotate -90deg about Y? simplest: rotate about
# the y-axis so -x (tab side) faces +z. Rotate +90 deg about Y maps -x -> +z.
bar.rotation_euler = (0, 1.5707963, 0)
bpy.context.view_layer.objects.active = bar
bpy.ops.object.transform_apply(rotation=True)
# after rotation the bar lies in negative z; lift to the bed and move beside the pull
from mathutils import Vector  # noqa: E402
mn = min((bar.matrix_world @ Vector(v.co)).z for v in bar.data.vertices)
bar.location = (14.0, 40.0, -mn)
bpy.ops.object.transform_apply(location=True)

# --- SHEATH (printed top-plate-down as modeled upside down) ----------------------
# modeled upside down directly: top plate on the bed, walls rising
SH_W = PULL_Y + 2 * (SH_WALL + CLR)
sheath = box("Sheath_V71", 0, PULL_X, 0, SH_W, 0, SH_TOP)          # top plate (on bed)
for y0 in (0.0, SH_W - SH_WALL):
    sheath = combine(sheath, box("wall", 0, PULL_X, y0, y0 + SH_WALL,
                                 SH_TOP, SH_TOP + SH_DROP), "UNION")
# bolt hole through the top plate, positioned over the channel (mirrored in y is
# symmetric, so plain coordinates work)
hy0 = SH_WALL + CLR + CH_Y0 - 0.1
hy1 = SH_WALL + CLR + CH_Y1 + 0.1
sheath = combine(sheath, box("hole", CH_X0 - 0.1, CH_X1 + 0.1, hy0, hy1,
                             -0.1, SH_TOP + 0.1), "DIFFERENCE")
sheath.location = (30.0, 0, 0)
bpy.context.view_layer.objects.active = sheath
bpy.ops.object.transform_apply(location=True)

# --- export ----------------------------------------------------------------------
for o in bpy.data.objects:
    print(f"v7.1-proto: {o.name} dims={[round(d, 2) for d in o.dimensions]}")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "print", "v7_1_bolt_in_pull_proto_plate.stl")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.wm.stl_export(filepath=out, export_selected_objects=True, global_scale=1.0)
print(f"v7.1-proto: wrote {out}")
