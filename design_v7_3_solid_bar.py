#!/usr/bin/env python3
"""v7.3 side-bolt lock — solid bar, spring in the housing (run inside Blender).

Operator review of the v7.2 print drove two changes, both validated by the parts:

1. PRINT THE BAR STANDING, not laid on its back. v7.2's bar was rotated flat, which
   put its prong slit HORIZONTAL: the slicer bridged it (7 bridge/overhang features)
   so the slit roof sagged, and — worse — the prongs then flexed ACROSS layer lines,
   the delamination direction. Standing, the slit/fin geometry is vertical: no
   bridging, flex within layers. Footprint 86 vs 90 mm2, same height: nothing lost.

2. SOLID BAR, spring moved into the pull. A flexure on the moving part is the
   fatigue path; the housing can host a far longer, lower-strain one:
       v7.1 prong  3.0mm x 6mm,  0.45mm  ->  5.6% strain   (over PETG's ~2% yield)
       v7.2 prong  1.2mm x 9mm,  0.45mm  ->  1.0%
       v7.3 fin    1.0mm x 12mm, 0.25mm  ->  0.26%
   The bar now carries only two dimples; the pull's fin carries the bump. This is how
   slide switches are built — spring in the housing, not the slider.

Also kept from the v7.2 print, which validated it: 0.25mm/face sliding clearance
("fits cleanly into the groove"), and side-wall engagement so bag pressure on the
flush bolt pushes it TOWARD locked, never out.

Parts:
  PULL   — 10mm deep. Horizontal bolt channel behind the face; thumb ridges through a
           front slot; behind the channel a full-height cantilever FIN (1mm thick,
           12mm long, anchored at one vertical edge) whose bump rides the bar and
           snaps into its dimples. Prints upright: the fin is a vertical wall off the
           bed, its relief slot open at the back and top, so nothing bridges but the
           channel roof (3.5mm — proven fine).
  BAR    — SOLID 3 x 4.5 x 20mm bolt, thumb tab + ridges as full-height ribs, and two
           dimples on its back face (LOCKED deeper than OPEN: bag pressure is harmless
           here, but the lock should still hold harder). Prints STANDING as modelled.
  SHEATH — sleeve section with the 3mm-thick lock wall and bolt hole. Unchanged.

Print: everything as modelled, supportless, brim 5mm (v7.2's 79mm2 bar detached).
PETG, supports=off, orient=off, brim=5.

Usage:  blender -b --factory-startup --python design_v7_3_solid_bar.py [-- --only Bar]
Writes: print/v7_3_solid_bar_plate.stl  (or ..._<part>.stl with --only)
"""
import os
import sys

import bpy

_argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ONLY = _argv[_argv.index("--only") + 1] if "--only" in _argv else None

# --- parameters (mm) -------------------------------------------------------------
CLR = 0.25                                    # validated on the v7.2 print
PULL_Y, PULL_X, PULL_Z = 32.0, 10.0, 14.0     # deeper than v7.2 to host the fin
WALL_F = 1.6
BAR_T, BAR_H, BAR_L = 3.0, 4.5, 20.0
TRAVEL = 3.25                                 # = engagement into the sheath wall
CH_X0 = WALL_F
CH_X1 = CH_X0 + BAR_T + 2 * CLR               # 5.1
CH_Z0 = 5.0
CH_Z1 = CH_Z0 + BAR_H + 2 * CLR               # 10.0
CH_YEND = 21.0
TAB_W, TAB_D = 6.0, 0.8
RIDGE_W, RIDGE_P = 0.9, 0.5
TAB_Y0, TAB_Y1 = 7.0, 13.0
FIN_T, FIN_Y0, FIN_Y1 = 1.0, 6.0, 18.0        # 1mm thick, 12mm long, anchored at Y1
FIN_X0 = CH_X1 + CLR                          # 5.35
BUMP_R, BUMP_PROUD = 0.9, 0.75                # protrudes past the fin face
BUMP_Y = 8.0                                  # near the fin's free end
DIMPLE_R = 0.9
DIMPLE_LOCK_D, DIMPLE_OPEN_D = 0.5, 0.35
OPEN_DIMPLE_Y = BUMP_Y                        # bar-local y aligned with the bump at OPEN
LOCK_DIMPLE_Y = BUMP_Y + TRAVEL               # ... and at LOCKED (bar has slid out)
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

# --- PULL -------------------------------------------------------------------------
pull = box("Pull_V73", 0, PULL_X, 0, PULL_Y, 0, PULL_Z)
# bolt channel: open through the side face (y=0), closed stop at CH_YEND
pull = combine(pull, box("channel", CH_X0, CH_X1, -0.1, CH_YEND, CH_Z0, CH_Z1), "DIFFERENCE")
# thumb slot in the front face, open at the side edge so the bar's ribs enter with it
pull = combine(pull, box("slot", -0.1, WALL_F + 0.1, -0.1, TAB_Y1 + 1.0,
                         ZC - TAB_W / 2 - CLR, ZC + TAB_W / 2 + CLR), "DIFFERENCE")
# relief slot for the fin: open through the BACK face and the TOP, so the fin prints
# as a plain vertical wall off the bed and nothing bridges
pull = combine(pull, box("relief", CH_X1, PULL_X + 0.1, FIN_Y0 - 2.0, FIN_Y1,
                         -0.1, PULL_Z + 0.1), "DIFFERENCE")
# the fin itself: full height, anchored to the body at FIN_Y1, free at FIN_Y0
pull = combine(pull, box("fin", FIN_X0, FIN_X0 + FIN_T, FIN_Y0, FIN_Y1,
                         0, PULL_Z), "UNION")
# detent bump on the fin's channel-facing side
pull = combine(pull, sphere("bump", FIN_X0 + BUMP_R - BUMP_PROUD, BUMP_Y, ZC, BUMP_R), "UNION")

# --- BAR (solid; modelled in print orientation — standing) ------------------------
bar = box("Bar_V73", 0, BAR_T, 0, BAR_L, 0, BAR_H)
bar = combine(bar, box("tab", -TAB_D, 0.1, TAB_Y0, TAB_Y1, 0, BAR_H), "UNION")
for ry in (7.8, 9.55, 11.3):
    bar = combine(bar, box("ridge", -TAB_D - RIDGE_P, -TAB_D + 0.1, ry, ry + RIDGE_W,
                           0, BAR_H), "UNION")
# detent dimples in the BACK face (the fin bump rides here). LOCKED holds harder.
for dy, depth in ((OPEN_DIMPLE_Y, DIMPLE_OPEN_D), (LOCK_DIMPLE_Y, DIMPLE_LOCK_D)):
    bar = combine(bar, sphere("dimple", BAR_T + DIMPLE_R - depth, dy, BAR_H / 2,
                              DIMPLE_R), "DIFFERENCE")
bar.location = (16.0, 40.0, 0)
bpy.context.view_layer.objects.active = bar
bpy.ops.object.transform_apply(location=True)

# --- SHEATH (modelled upside down: top plate on the bed) --------------------------
IN_X, IN_Y = PULL_Z + 0.5, PULL_Y + 0.5
OUT_X = IN_X + 2 * SLEEVE_WALL
OUT_Y = IN_Y + SLEEVE_SIDE + SLEEVE_WALL
sheath = box("Sheath_V73", 0, OUT_X, 0, OUT_Y, 0, SLEEVE_LEN)
sheath = combine(sheath, box("cavity", SLEEVE_WALL, SLEEVE_WALL + IN_X,
                             SLEEVE_SIDE, SLEEVE_SIDE + IN_Y, -0.1, SLEEVE_LEN + 0.1),
                 "DIFFERENCE")
px = SLEEVE_WALL + 0.25
sheath = combine(sheath, box("hole", px + CH_Z0 - 0.3, px + CH_Z1 + 0.3,
                             -0.1, SLEEVE_SIDE + 0.1,
                             0.5 + CH_X0 - 0.3 + CLR, 0.5 + CH_X1 + 0.3 - CLR),
                 "DIFFERENCE")
sheath.location = (34.0, 0, 0)
bpy.context.view_layer.objects.active = sheath
bpy.ops.object.transform_apply(location=True)

# --- export ----------------------------------------------------------------------
if ONLY:
    for o in [o for o in bpy.data.objects if ONLY.lower() not in o.name.lower()]:
        bpy.data.objects.remove(o, do_unlink=True)
    if not bpy.data.objects:
        raise SystemExit(f"v7.3: no part matches --only {ONLY!r}")
    obj = bpy.data.objects[0]
    obj.location = (-obj.dimensions.x / 2, -obj.dimensions.y / 2, obj.location.z)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True)

for o in bpy.data.objects:
    print(f"v7.3: {o.name} dims={[round(d, 2) for d in o.dimensions]}")
name = f"v7_3_solid_bar_{ONLY.lower()}.stl" if ONLY else "v7_3_solid_bar_plate.stl"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "print", name)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.wm.stl_export(filepath=out, export_selected_objects=True, global_scale=1.0)
print(f"v7.3: wrote {out}")
