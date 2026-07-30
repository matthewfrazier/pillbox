"""Render the proposed support-free P2S plate layout for pillbox V6.

This is a planning illustration built from dimensional proxies.  It deliberately
does not export or slice STLs because the V6 lock is still concept geometry.

Run inside Blender:

    exec(compile(open(
        "/Users/mf/code/pillbox/design_edge_roller_print_layout.py"
    ).read(), "design_edge_roller_print_layout.py", "exec"))
"""

from math import pi
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path("/Users/mf/code/pillbox")
OUTPUT = ROOT / "pillbox_v6_print_layout_plan.png"
BLEND = ROOT / "pillbox_v6_print_layout_plan.blend"
COLLECTION = "Pillbox_V6_PrintPlan"


def remove_tree(collection):
    for child in list(collection.children):
        remove_tree(child)
    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(collection)


old = bpy.data.collections.get(COLLECTION)
if old:
    remove_tree(old)

for obj in bpy.context.scene.objects:
    obj.hide_render = True

plan = bpy.data.collections.new(COLLECTION)
bpy.context.scene.collection.children.link(plan)


def relink(obj):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    plan.objects.link(obj)
    obj.hide_render = False
    return obj


def mat(name, color, metallic=0.0, roughness=0.42, emission=0.0):
    old_mat = bpy.data.materials.get(name)
    if old_mat:
        bpy.data.materials.remove(old_mat)
    result = bpy.data.materials.new(name)
    result.use_nodes = True
    bsdf = result.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        emission_color = bsdf.inputs.get("Emission Color")
        emission_strength = bsdf.inputs.get("Emission Strength")
        if emission_color:
            emission_color.default_value = (*color, 1.0)
        if emission_strength:
            emission_strength.default_value = emission
    return result


M = {
    "bed": mat("Plan Bed", (0.055, 0.065, 0.078), 0.12, 0.58),
    "grid": mat("Plan Grid", (0.14, 0.17, 0.20), 0.05, 0.48),
    "sleeve": mat("Plan Sleeve", (0.015, 0.44, 0.54), 0.08, 0.34),
    "drawer": mat("Plan Drawer", (0.78, 0.30, 0.018), 0.02, 0.37),
    "rotor": mat("Plan Rotor", (0.96, 0.63, 0.06), 0.32, 0.28),
    "coupon": mat("Plan Coupon", (0.87, 0.22, 0.46), 0.06, 0.33),
    "brim": mat("Plan Brim", (0.10, 0.24, 0.31), 0.12, 0.44),
    "text": mat("Plan Text", (0.84, 0.87, 0.91), 0.0, 0.40),
    "text_ui": mat("Plan Text UI", (0.84, 0.87, 0.91), emission=2.0),
    "sleeve_ui": mat("Plan Sleeve UI", (0.08, 0.77, 0.88), emission=1.6),
    "drawer_ui": mat("Plan Drawer UI", (1.0, 0.47, 0.04), emission=1.6),
    "rotor_ui": mat("Plan Rotor UI", (1.0, 0.72, 0.10), emission=1.6),
    "coupon_ui": mat("Plan Coupon UI", (1.0, 0.32, 0.62), emission=1.6),
}


def activate(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def box(name, location, dimensions, material, bevel=0.45):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = relink(bpy.context.object)
    obj.name = name
    obj.dimensions = dimensions
    activate(obj)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        modifier = obj.modifiers.new("Printable edge", "BEVEL")
        modifier.width = bevel
        modifier.segments = 3
        modifier.limit_method = "ANGLE"
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    obj.data.materials.append(material)
    return obj


def cylinder(name, location, radius, depth, material, vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth, location=location
    )
    obj = relink(bpy.context.object)
    obj.name = name
    obj.data.materials.append(material)
    return obj


def text(name, body, size, material):
    bpy.ops.object.text_add()
    obj = relink(bpy.context.object)
    obj.name = name
    obj.data.body = body
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.10
    obj.data.bevel_depth = 0.02
    obj.data.materials.append(material)
    if hasattr(obj, "visible_shadow"):
        obj.visible_shadow = False
    return obj


def look_at(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat(
        "-Z", "Y"
    ).to_euler()


def build_arrow(name, x, y, start_z, end_z, material):
    cylinder(
        name + "_Shaft",
        (x, y, (start_z + end_z) / 2),
        0.65,
        end_z - start_z,
        material,
        24,
    )
    bpy.ops.mesh.primitive_cone_add(
        vertices=32,
        radius1=2.3,
        radius2=0.0,
        depth=5.0,
        location=(x, y, end_z + 2.5),
    )
    cone = relink(bpy.context.object)
    cone.name = name + "_Head"
    cone.data.materials.append(material)


# 256 x 256 mm P2S plate and a 32 mm planning grid.
box("P2S_256mm_Plate", (0, 0, -0.55), (256, 256, 1.1), M["bed"], 3.0)
for coordinate in range(-96, 97, 32):
    box(
        f"Grid_X_{coordinate}",
        (coordinate, 0, 0.05),
        (0.35, 248, 0.10),
        M["grid"],
        0,
    )
    box(
        f"Grid_Y_{coordinate}",
        (0, coordinate, 0.05),
        (248, 0.35, 0.10),
        M["grid"],
        0,
    )

# 1. Sleeve: original closed 54 x 19 mm end on the bed; open mouth upward.
sx, sy = -61.0, 42.0
box("Sleeve_8mm_Brim", (sx, sy, 0.16), (70, 35, 0.32), M["brim"], 3.0)
box("Sleeve_ClosedEnd", (sx, sy, 1.0), (54, 19, 2.0), M["sleeve"], 0.8)
box("Sleeve_Wall_L", (sx - 26, sy, 43), (2, 19, 86), M["sleeve"], 0.7)
box("Sleeve_Wall_R", (sx + 26, sy, 43), (2, 19, 86), M["sleeve"], 0.7)
box("Sleeve_Wall_F", (sx, sy - 8.5, 43), (50, 2, 86), M["sleeve"], 0.7)
box("Sleeve_Wall_B", (sx, sy + 8.5, 43), (50, 2, 86), M["sleeve"], 0.7)
build_arrow("Sleeve_BuildDirection", sx, sy, 88, 105, M["text"])

# 2. Drawer: broad closed bottom on the bed, compartments open upward.
dx, dy = 29.0, 39.0
box("Drawer_Base", (dx, dy, 1.0), (88, 50, 2.0), M["drawer"], 0.7)
box("Drawer_Left", (dx, dy - 24.2, 7.0), (88, 1.6, 12), M["drawer"], 0.5)
box("Drawer_Right", (dx, dy + 24.2, 7.0), (88, 1.6, 12), M["drawer"], 0.5)
box("Drawer_Back", (dx - 43, dy, 7.0), (2, 48, 12), M["drawer"], 0.5)
box("Drawer_Pull", (dx + 43, dy, 7.5), (2.8, 50, 13), M["drawer"], 0.6)
box("Drawer_Divider_1", (dx - 9, dy, 7.0), (1.4, 48, 12), M["drawer"], 0.4)
box("Drawer_Divider_2", (dx + 19, dy, 7.0), (1.4, 48, 12), M["drawer"], 0.4)
build_arrow("Drawer_BuildDirection", dx, dy, 16, 31, M["text"])

# 3. One-piece rotor concept: flat annular face on bed, keyed shaft vertical,
# and a 45-degree production underside on the cam dog.  A 5 mm brim is shown.
rx, ry = 75.0, -49.0
cylinder("Rotor_5mm_Brim", (rx, ry, 0.16), 13.0, 0.32, M["brim"])
cylinder("Rotor_FlatFace", (rx, ry, 0.95), 7.55, 1.6, M["rotor"])
cylinder("Rotor_Shaft", (rx, ry, 6.0), 1.65, 8.6, M["rotor"], 48)
cylinder("Rotor_RampCollar", (rx, ry, 8.5), 3.8, 2.0, M["rotor"], 48)
box("Rotor_CamDog", (rx, ry, 11.0), (12.5, 2.8, 2.6), M["rotor"], 0.45)
build_arrow("Rotor_BuildDirection", rx, ry, 14, 29, M["text"])

# 0. A small lock-fit coupon is part of the first validation plate, not the
# production assembly.  It checks bearing clearance, ramp take-up, and click.
cx, cy = -20.0, -51.0
box("Coupon_Base", (cx, cy, 1.5), (42, 20, 3), M["coupon"], 0.8)
cylinder("Coupon_Bearing", (cx - 10, cy, 4.0), 4.5, 2.0, M["drawer"], 48)
box("Coupon_Keeper", (cx + 9, cy, 4.0), (7, 14, 5), M["sleeve"], 0.6)
box("Coupon_DetentLeaf", (cx, cy - 6, 4.0), (18, 1.2, 1.0), M["coupon"], 0.35)
build_arrow("Coupon_BuildDirection", cx, cy, 7, 19, M["text"])

# Stage lighting and high isometric camera.
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.render.resolution_x = 1800
scene.render.resolution_y = 1200
scene.render.resolution_percentage = 100
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = 0.15
scene.world.use_nodes = True
background = scene.world.node_tree.nodes.get("Background")
background.inputs["Color"].default_value = (0.012, 0.016, 0.024, 1)
background.inputs["Strength"].default_value = 0.10

bpy.ops.object.camera_add(location=(255, -295, 295))
camera = relink(bpy.context.object)
camera.name = "PrintPlan_Camera"
camera.data.type = "ORTHO"
camera.data.ortho_scale = 340
look_at(camera, (0, 0, 25))
scene.camera = camera

for name, location, energy, color in (
    ("Plan_SunKey", (190, -180, 260), 1.5, (1.0, 0.90, 0.78)),
    ("Plan_SunFill", (-160, -100, 160), 0.9, (0.65, 0.82, 1.0)),
    ("Plan_SunRim", (0, 180, 220), 0.7, (0.68, 0.88, 1.0)),
):
    bpy.ops.object.light_add(type="SUN", location=location)
    light = relink(bpy.context.object)
    light.name = name
    light.data.energy = energy
    light.data.color = color
    look_at(light, (0, 0, 20))

# Screen-aligned title and part/orientation inventory.
overlays = (
    (
        text(
            "Plan_Title",
            "PILLBOX V6  /  SUPPORT-FREE PRINT + PLATE PLAN",
            6.5,
            M["text_ui"],
        ),
        (0, 100, -120),
    ),
    (
        text(
            "Plan_Subtitle",
            "P2S 256 x 256  |  TEXTURED PEI  |  PETG A4 INTENT  |  SUPPORTS OFF",
            4.1,
            M["text_ui"],
        ),
        (0, 89, -120),
    ),
    (
        text(
            "Plan_SleeveLabel",
            "1  SLEEVE\nCLOSED END DOWN\n8 mm BRIM / Z 86 mm",
            3.7,
            M["sleeve_ui"],
        ),
        (-150, -83, -120),
    ),
    (
        text(
            "Plan_DrawerLabel",
            "2  DRAWER\nBOTTOM DOWN\nNO SUPPORT",
            3.7,
            M["drawer_ui"],
        ),
        (-48, -83, -120),
    ),
    (
        text(
            "Plan_RotorLabel",
            "3  ROTOR\nFLAT FACE DOWN\n5 mm BRIM",
            3.7,
            M["rotor_ui"],
        ),
        (48, -83, -120),
    ),
    (
        text(
            "Plan_CouponLabel",
            "0  LOCK COUPON\nPRINT FIRST, THEN REMOVE\nCLEARANCE / CLICK / TAKE-UP",
            3.0,
            M["coupon_ui"],
        ),
        (142, -83, -120),
    ),
    (
        text(
            "Plan_Gate",
            "CONCEPT LAYOUT ONLY — EXPORT MANIFOLD STLs, VERIFY A4=PETG, THEN SLICE + PREVIEW",
            3.6,
            M["text_ui"],
        ),
        (0, -104, -120),
    ),
)
for obj, position in overlays:
    obj.parent = camera
    obj.location = position
    obj.rotation_euler = (0, 0, 0)

scene.render.filepath = str(OUTPUT)
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
print(f"Print layout plan: {OUTPUT}")
print(f"Blender source: {BLEND}")
