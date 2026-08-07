#!/usr/bin/env python3
"""v7 slide-lock mechanism — working prototype coupon (run inside Blender).

Goal (from the v7 revision brief): a sliding, locking thumb lock, slightly inset,
operable one-handed, physically legible (detent "click" at LOCKED and OPEN), and
unlikely to walk loose in a bag. This coupon prototypes ONLY the mechanism so the
feel can be validated in hand before it is integrated into the credit-card box.

Three separate printed parts (no print-in-place — parts assemble by hand):

  FRAME   — the stand-in for the sleeve front: a slider channel with side capture
            grooves (the slider's wings ride under them), two detent dimples in the
            channel floor (LOCKED / OPEN positions), a wall the bolt tongue passes
            through, and a perpendicular bay where the drawer stub slides.
  SLIDER  — thumb piece: body with bottom wings (captured by the frame grooves),
            an in-plane cantilever flexure carrying a detent bump (the "click"),
            a bolt tongue, and transverse thumb ribs that stay INSET below the
            frame's top surface (bag-rub protection).
  STUB    — a mock drawer edge sliding in the bay; the locked tongue enters its
            notch and blocks it. Slide the slider back and the stub runs free.

Assembly: drop the slider's wings into the insertion window at the right end of
the channel, slide left past the OPEN detent. (Proto note: there is no capture rib
yet — over-sliding right removes the slider, battery-door style. Final rev adds a
capture feature.)

Print: everything lies flat, supportless (the only downward feature is the 0.4 mm
detent bump — below any support threshold). PETG, supports=off, orient=off.

Usage:  blender -b --factory-startup --python design_v7_slide_lock_proto.py
Writes: print/v7_slide_lock_proto_plate.stl
"""
import os

import bpy

# --- parameters (mm) -------------------------------------------------------------
CLR = 0.25          # sliding clearance per face
FRAME_X0, FRAME_X1 = 0.0, 46.0
FRAME_Y0, FRAME_Y1 = 0.0, 24.0
FRAME_Z = 4.0      # deep enough that the seated slider's thumb ribs stay 0.2 mm INSET
POCKET_X0, POCKET_X1 = 4.0, 34.0     # slider channel
POCKET_Y0, POCKET_Y1 = 6.0, 18.0
POCKET_FLOOR = 1.4                    # channel depth = FRAME_Z - POCKET_FLOOR
GROOVE_W, GROOVE_H = 1.25, 1.0        # wing capture grooves in the channel walls
GROOVE_X1 = 30.0                      # grooves run POCKET_X0..GROOVE_X1
WINDOW_X0 = 26.0                      # insertion window: full-width, full-depth
WALL_X = POCKET_X0                    # bolt wall is the material x 0..4
TONGUE_W, TONGUE_L = 6.0, 8.0
SLIDER_L, SLIDER_W, SLIDER_T = 14.0, POCKET_Y1 - POCKET_Y0 - 2 * CLR, 1.6
WING_W, WING_T = 1.0, 0.8
LOCK_X = POCKET_X0 + CLR              # slider body x0 at LOCKED
OPEN_X = LOCK_X + 7.0                 # 7 mm travel
BUMP_R, BUMP_PROUD = 1.0, 0.4         # detent bump under the flexure finger
DIMPLE_R, DIMPLE_DEPTH = 1.2, 0.5
APRON_X0 = -12.0                      # drawer bay
RAIL_W, RAIL_H, APRON_FLOOR = 1.5, 3.0, 1.0
STUB_T = 1.8
YC = (FRAME_Y0 + FRAME_Y1) / 2


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

# --- FRAME -----------------------------------------------------------------------
frame = box("Frame_V7", FRAME_X0, FRAME_X1, FRAME_Y0, FRAME_Y1, 0, FRAME_Z)
# slider channel pocket
frame = combine(frame, box("pocket", POCKET_X0, POCKET_X1, POCKET_Y0, POCKET_Y1,
                           POCKET_FLOOR, FRAME_Z + 0.1), "DIFFERENCE")
# wing capture grooves (1.25 mm bridges print fine flat)
for y0, y1 in ((POCKET_Y0 - GROOVE_W, POCKET_Y0), (POCKET_Y1, POCKET_Y1 + GROOVE_W)):
    frame = combine(frame, box("groove", POCKET_X0, GROOVE_X1, y0, y1,
                               POCKET_FLOOR, POCKET_FLOOR + GROOVE_H), "DIFFERENCE")
# insertion window: full width incl. groove span, full depth, at the far end
frame = combine(frame, box("window", WINDOW_X0, POCKET_X1,
                           POCKET_Y0 - GROOVE_W, POCKET_Y1 + GROOVE_W,
                           POCKET_FLOOR, FRAME_Z + 0.1), "DIFFERENCE")
# bolt tongue notch through the wall (open to the top for supportless printing)
frame = combine(frame, box("wallnotch", FRAME_X0 - 0.1, WALL_X + 0.1,
                           YC - TONGUE_W / 2 - CLR, YC + TONGUE_W / 2 + CLR,
                           POCKET_FLOOR, FRAME_Z + 0.1), "DIFFERENCE")
# detent dimples in the channel floor at LOCKED / OPEN bump positions
for bx in (LOCK_X + SLIDER_L / 2, OPEN_X + SLIDER_L / 2):
    frame = combine(frame, sphere("dimple", bx, YC,
                                  POCKET_FLOOR + DIMPLE_R - DIMPLE_DEPTH, DIMPLE_R), "DIFFERENCE")
# drawer bay: apron floor + two y-running rails, with a rail gap for the tongue
frame = combine(frame, box("apron", APRON_X0, FRAME_X0 + 0.1, FRAME_Y0, FRAME_Y1,
                           0, APRON_FLOOR), "UNION")
for x0, x1 in ((APRON_X0, APRON_X0 + RAIL_W), (FRAME_X0 - RAIL_W, FRAME_X0)):
    frame = combine(frame, box("rail", x0, x1, FRAME_Y0, FRAME_Y1, 0, RAIL_H), "UNION")
frame = combine(frame, box("railgap", FRAME_X0 - RAIL_W - 0.1, FRAME_X0 + 0.1,
                           YC - TONGUE_W / 2 - CLR, YC + TONGUE_W / 2 + CLR,
                           POCKET_FLOOR, RAIL_H + 0.1), "DIFFERENCE")

# --- SLIDER (built at origin, then placed on the plate) --------------------------
sl = box("Slider_V7", 0, SLIDER_L, 0, SLIDER_W, 0, SLIDER_T)
# bottom wings
for y0, y1 in ((-WING_W, 0), (SLIDER_W, SLIDER_W + WING_W)):
    sl = combine(sl, box("wing", 0, SLIDER_L, y0, y1, 0, WING_T), "UNION")
# bolt tongue off the leading (-x) edge, centered
sl = combine(sl, box("tongue", -TONGUE_L, 0.1, SLIDER_W / 2 - TONGUE_W / 2,
                     SLIDER_W / 2 + TONGUE_W / 2, 0, SLIDER_T), "UNION")
# thumb ribs — inset: rib tops at SLIDER_T+0.8 = 2.4 vs frame top 3.2 when seated
for rx in (6.0, 8.5, 11.0):
    sl = combine(sl, box("rib", rx, rx + 1.2, 1.0, SLIDER_W - 1.0,
                         SLIDER_T, SLIDER_T + 0.8), "UNION")
# cantilever flexure finger (3 mm wide, ~7 mm long, rooted at the +x end) via U-slot
FIN_Y0, FIN_Y1 = SLIDER_W / 2 - 1.5, SLIDER_W / 2 + 1.5
sl = combine(sl, box("slotA", 3.0, 11.0, FIN_Y0 - 1.2, FIN_Y0, -0.1, SLIDER_T + 0.1), "DIFFERENCE")
sl = combine(sl, box("slotB", 3.0, 11.0, FIN_Y1, FIN_Y1 + 1.2, -0.1, SLIDER_T + 0.1), "DIFFERENCE")
sl = combine(sl, box("slotC", 3.0, 4.0, FIN_Y0, FIN_Y1, -0.1, SLIDER_T + 0.1), "DIFFERENCE")
# detent bump under the free end of the finger (matches dimple x = body center)
sl = combine(sl, sphere("bump", SLIDER_L / 2, SLIDER_W / 2,
                        BUMP_R - BUMP_PROUD, BUMP_R), "UNION")
sl.location = (0, 34.0, 0)   # plate position, clear of the frame
bpy.context.view_layer.objects.active = sl
bpy.ops.object.transform_apply(location=True)

# --- DRAWER STUB -----------------------------------------------------------------
BAY_GAP_X0, BAY_GAP_X1 = APRON_X0 + RAIL_W + CLR, FRAME_X0 - RAIL_W - CLR
STUB_W = BAY_GAP_X1 - BAY_GAP_X0            # ~8.5 wide, slides along y in the bay
stub = box("Stub_V7", 0, STUB_W, 0, 26.0, 0, STUB_T)
# notch on the +x edge, mid-length: the locked tongue lands here
stub = combine(stub, box("notch", STUB_W - 2.2, STUB_W + 0.1, 13.0 - TONGUE_W / 2 - CLR,
                         13.0 + TONGUE_W / 2 + CLR, 0.3, STUB_T + 0.1), "DIFFERENCE")
# grip tab on the far end
stub = combine(stub, box("tab", -1.5, STUB_W + 1.5, 24.5, 26.0, 0, STUB_T + 1.2), "UNION")
stub.location = (24.0, 34.0, 0)
bpy.context.view_layer.objects.active = stub
bpy.ops.object.transform_apply(location=True)

# --- export ----------------------------------------------------------------------
for o in bpy.data.objects:
    print(f"v7-proto: {o.name} dims={[round(d, 2) for d in o.dimensions]}")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "print", "v7_slide_lock_proto_plate.stl")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.wm.stl_export(filepath=out, export_selected_objects=True, global_scale=1.0)
print(f"v7-proto: wrote {out}")
