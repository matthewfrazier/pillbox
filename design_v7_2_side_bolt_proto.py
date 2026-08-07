#!/usr/bin/env python3
"""v7.2 side-bolt lock — working prototype coupon (run inside Blender).

Operator direction after v7.1: engage the SLEEVE SIDE WALL, not the top — side
walls are loaded in-plane by bag pressure (they don't bow off the bolt), so
twisting/jostling puts the bolt purely in shear. Single bar chosen over a
top+bottom hasp on investigation: a 3x4.5mm PETG bolt tip in shear carries
~190-380N against a 20-50N bag-snag load (SF 4-10x), so a second engagement
point adds nothing structural, while a hasp's two simultaneous pin/hole fits
lose to FDM tolerance stack (~±0.2mm XY): either a pin binds or clearances
grow past the crisp flush-feel. One interface, direct thumb drive, wins.

Detent flexure corrected from v7.1 (whose 3mm prongs hit ~5.6% strain — over
PETG's ~2% limit): v7.2 prongs are 1.2mm thick x 9mm long, ~1.0% strain at
full click. Lock dimple deeper than open (0.5 vs 0.35) so the lock holds.

Parts:
  PULL   — drawer-front stand-in: HORIZONTAL bolt channel behind the face,
           thumb ridges through a front slot (0.3mm inset), thumb slides
           sideways 3.25mm. Bar tip exits the pull's side face.
  BAR    — the bolt: 3x4.5mm section, 20mm long; tail split into two in-plane
           prongs with fore/aft detent bumps clicking into channel-wall dimples.
  SLEEVE — a real sleeve section (open tube) that the pull slides into. One
           side wall is 3.0mm thick and carries the bolt hole. LOCKED: bar tip
           fills it flush with the outer face (fingertip reads FLAT) and blocks
           the tube from sliding. OPEN: fingertip reads a 3mm empty hole.

Assembly: slide the bar into the pull channel from the side face (tab rides
the slot, open at that end); slide the sleeve section over the pull.

Print: pull and sleeve upright as modeled, bar on its back — all supportless.
PETG, supports=off, orient=off. Sliding clearances 0.25mm/face.

Usage:  blender -b --factory-startup --python design_v7_2_side_bolt_proto.py
Writes: print/v7_2_side_bolt_proto_plate.stl
"""
import os

import bpy
from mathutils import Vector

# --- parameters (mm) -------------------------------------------------------------
CLR = 0.25
PULL_Y, PULL_X, PULL_Z = 32.0, 8.0, 14.0     # width, depth, height (front face at x=0)
WALL_F = 1.6
BAR_T, BAR_H, BAR_L = 3.0, 4.5, 20.0          # bolt: thick(X) x tall(Z) x long(Y)
TRAVEL = 3.25                                 # = engagement = sleeve side wall thickness + gap
CH_X0, CH_X1 = WALL_F, WALL_F + BAR_T + 2 * CLR
CH_Z0, CH_Z1 = 5.0, 5.0 + BAR_H + 2 * CLR     # 5.0..9.75+
CH_YEND = 21.0                                # closed end stop (bar tail at OPEN = 20)
TAB_W, TAB_D = 6.0, 0.8                       # thumb tab through the front slot
RIDGE_W, RIDGE_P = 0.9, 0.5                   # vertical ridges on the tab; crest 0.3 inset
TAB_Y0, TAB_Y1 = 7.0, 13.0                    # tab span on the bar (local y, tip at 0)
PRONG_SLIT, PRONG_L = 0.6, 9.0                # tail split -> two 1.2mm prongs, ~1.0% strain
BUMP_R, BUMP_P = 0.9, 0.35
BUMP_Y = 18.5                                 # bump position on the bar (local)
DIMPLE_R = 0.9
DIMPLE_LOCK_D, DIMPLE_OPEN_D = 0.5, 0.35
LOCK_Y0, OPEN_Y0 = -TRAVEL, 0.0               # bar tip world-y at LOCKED / OPEN
SLEEVE_SIDE, SLEEVE_WALL, SLEEVE_LEN = 3.0, 1.6, 12.0
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

# --- PULL (printed upright; the horizontal channel roof is a short 3.5mm bridge) --
pull = box("Pull_V72", 0, PULL_X, 0, PULL_Y, 0, PULL_Z)
# horizontal bolt channel: open through the side face (y=0), closed stop at CH_YEND
pull = combine(pull, box("channel", CH_X0, CH_X1, -0.1, CH_YEND, CH_Z0, CH_Z1), "DIFFERENCE")
# front slot: horizontal, open at the side edge so the bar's tab slides in with it
pull = combine(pull, box("slot", -0.1, WALL_F + 0.1, -0.1, TAB_Y1 + OPEN_Y0 + 1.0,
                         ZC - TAB_W / 2 - CLR, ZC + TAB_W / 2 + CLR), "DIFFERENCE")
# detent dimples in the channel's front (x=CH_X0) and back (x=CH_X1) walls at the
# bump y-positions for LOCKED and OPEN
for xwall, sgn in ((CH_X0, -1), (CH_X1, 1)):
    for y0, depth in ((LOCK_Y0 + BUMP_Y, DIMPLE_LOCK_D), (OPEN_Y0 + BUMP_Y, DIMPLE_OPEN_D)):
        pull = combine(pull, sphere("dimple", xwall + sgn * (DIMPLE_R - depth), y0, ZC,
                                    DIMPLE_R), "DIFFERENCE")

# --- BAR (modeled in place standing; laid on its back for the plate) --------------
bar = box("Bar_V72", 0, BAR_T, 0, BAR_L, 0, BAR_H)
# thumb tab + vertical ridges (front = -x)
bar = combine(bar, box("tab", -TAB_D, 0.1, TAB_Y0, TAB_Y1,
                       BAR_H / 2 - TAB_W / 2 + 0.75, BAR_H / 2 + TAB_W / 2 - 0.75), "UNION")
for ry in (7.8, 9.55, 11.3):
    bar = combine(bar, box("ridge", -TAB_D - RIDGE_P, -TAB_D + 0.1, ry, ry + RIDGE_W,
                           BAR_H / 2 - TAB_W / 2 + 1.25, BAR_H / 2 + TAB_W / 2 - 1.25), "UNION")
# tail slit -> two in-plane prongs (1.2mm thick, bending in x)
bar = combine(bar, box("slit", BAR_T / 2 - PRONG_SLIT / 2, BAR_T / 2 + PRONG_SLIT / 2,
                       BAR_L - PRONG_L, BAR_L + 0.1, -0.1, BAR_H + 0.1), "DIFFERENCE")
# fore/aft detent bumps at the prong tails (only BUMP_P protrudes past each face)
for x, sgn in ((0, -1), (BAR_T, 1)):
    bar = combine(bar, sphere("bump", x + sgn * (BUMP_P - BUMP_R), BUMP_Y, BAR_H / 2,
                              BUMP_R), "UNION")
# lay on its back (tab up) for printing: rotate +90 about Y maps -x -> +z
bar.rotation_euler = (0, 1.5707963, 0)
bpy.context.view_layer.objects.active = bar
bpy.ops.object.transform_apply(rotation=True)
mn = min((bar.matrix_world @ Vector(v.co)).z for v in bar.data.vertices)
bar.location = (16.0, 40.0, -mn)
bpy.ops.object.transform_apply(location=True)

# --- SLEEVE section (modeled standing in print orientation) -----------------------
# print axes: X = assembly Z (pull height), Y = assembly Y, Z = assembly X (slide axis)
IN_X, IN_Y = PULL_Z + 0.5, PULL_Y + 0.5
OUT_X = IN_X + 2 * SLEEVE_WALL
OUT_Y = IN_Y + SLEEVE_SIDE + SLEEVE_WALL
sleeve = box("Sleeve_V72", 0, OUT_X, 0, OUT_Y, 0, SLEEVE_LEN)
sleeve = combine(sleeve, box("cavity", SLEEVE_WALL, SLEEVE_WALL + IN_X,
                             SLEEVE_SIDE, SLEEVE_SIDE + IN_Y, -0.1, SLEEVE_LEN + 0.1),
                 "DIFFERENCE")
# bolt hole through the thick side wall. Mapping: pull z0 sits at print-x
# SLEEVE_WALL+0.25; pull front face (assembly x=0) at print-z 0.5.
px = SLEEVE_WALL + 0.25
hole_x0, hole_x1 = px + CH_Z0 - 0.3, px + CH_Z1 + 0.3
hole_z0, hole_z1 = 0.5 + CH_X0 - 0.3 + CLR, 0.5 + CH_X1 + 0.3 - CLR
sleeve = combine(sleeve, box("hole", hole_x0, hole_x1, -0.1, SLEEVE_SIDE + 0.1,
                             hole_z0, hole_z1), "DIFFERENCE")
sleeve.location = (32.0, 0, 0)
bpy.context.view_layer.objects.active = sleeve
bpy.ops.object.transform_apply(location=True)

# --- export ----------------------------------------------------------------------
for o in bpy.data.objects:
    print(f"v7.2-proto: {o.name} dims={[round(d, 2) for d in o.dimensions]}")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "print", "v7_2_side_bolt_proto_plate.stl")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.wm.stl_export(filepath=out, export_selected_objects=True, global_scale=1.0)
print(f"v7.2-proto: wrote {out}")
