"""Build preview imagery for the pocket-safe edge-roller cam lock.

Run inside Blender:

    exec(compile(open(
        "/Users/mf/code/pillbox/design_edge_roller_cam_preview.py"
    ).read(), "design_edge_roller_cam_preview.py", "exec"))

This is intentionally concept/presentation geometry.  It does not overwrite the
production STLs.
"""

from math import cos, pi, radians, sin
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path("/Users/mf/code/pillbox")
BLEND_PATH = ROOT / "pillbox_v6_edge_roller_cam_preview.blend"
OVERVIEW_PATH = ROOT / "pillbox_v6_edge_roller_overview.png"
MECHANISM_PATH = ROOT / "pillbox_v6_edge_roller_mechanism.png"
INVENTORY_PATH = ROOT / "pillbox_v6_edge_roller_inventory_top.png"

SCENE_COLLECTION = "Pillbox_V6_EdgeRoller"
OVERVIEW_COLLECTION = "V6_Overview"
MECHANISM_COLLECTION = "V6_Mechanism"
INVENTORY_COLLECTION = "V6_Inventory"
STAGE_COLLECTION = "V6_Stage"


def activate(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def remove_collection_tree(collection):
    for child in list(collection.children):
        remove_collection_tree(child)
    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(collection)


def remove_prior_preview():
    root = bpy.data.collections.get(SCENE_COLLECTION)
    if root:
        remove_collection_tree(root)
    # Clean up empty child collections left by preview-builder versions that
    # predated recursive collection removal.
    for base_name in (
        OVERVIEW_COLLECTION,
        MECHANISM_COLLECTION,
        INVENTORY_COLLECTION,
        STAGE_COLLECTION,
    ):
        for collection in list(bpy.data.collections):
            if (
                collection.name == base_name
                or collection.name.startswith(base_name + ".")
            ):
                remove_collection_tree(collection)


def create_collection(name, parent):
    collection = bpy.data.collections.new(name)
    parent.children.link(collection)
    return collection


def relink(obj, collection):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def material(name, color, metallic=0.0, roughness=0.42):
    existing = bpy.data.materials.get(name)
    if existing:
        bpy.data.materials.remove(existing)
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def rounded_box(collection, name, location, dimensions, mat, radius=0.45):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = relink(bpy.context.object, collection)
    obj.name = name
    obj.dimensions = dimensions
    activate(obj)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if radius:
        bevel = obj.modifiers.new("Pocket-soft edge", "BEVEL")
        bevel.width = radius
        bevel.segments = 3
        bevel.limit_method = "ANGLE"
        activate(obj)
        bpy.ops.object.modifier_apply(modifier=bevel.name)
    obj.data.materials.append(mat)
    return obj


def cylinder_x(collection, name, location, radius, depth, mat, vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=(0, pi / 2, 0),
    )
    obj = relink(bpy.context.object, collection)
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def torus_x(collection, name, location, major_radius, minor_radius, mat):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=64,
        minor_segments=12,
        location=location,
        rotation=(0, pi / 2, 0),
    )
    obj = relink(bpy.context.object, collection)
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def sphere(collection, name, location, radius, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32, ring_count=16, radius=radius, location=location
    )
    obj = relink(bpy.context.object, collection)
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def boolean_difference(target, cutter):
    modifier = target.modifiers.new(f"Cut {cutter.name}", "BOOLEAN")
    modifier.operation = "DIFFERENCE"
    modifier.solver = "EXACT"
    modifier.object = cutter
    activate(target)
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def label(collection, name, body, location, size, mat):
    bpy.ops.object.text_add(location=location)
    obj = relink(bpy.context.object, collection)
    obj.name = name
    obj.data.body = body
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.10
    obj.data.bevel_depth = 0.025
    obj.data.materials.append(mat)
    if hasattr(obj, "visible_shadow"):
        obj.visible_shadow = False
    return obj


def look_at(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat(
        "-Z", "Y"
    ).to_euler()


def billboard_text(obj, camera):
    obj.rotation_euler = (camera.location - obj.location).to_track_quat(
        "Z", "Y"
    ).to_euler()


def create_edge_texture(
    collection, prefix, wheel_x, wheel_y, wheel_z, radius, mat
):
    """Add rounded radial ribs to the roller without sharp pocket-facing teeth."""
    ribs = []
    for index in range(24):
        angle = index * 2 * pi / 24
        y = wheel_y + radius * sin(angle)
        z = wheel_z + radius * cos(angle)
        rib = rounded_box(
            collection,
            f"{prefix}_GripRib_{index:02d}",
            (wheel_x, y, z),
            (0.34, 0.62, 1.00),
            mat,
            0.20,
        )
        rib.rotation_euler.x = -angle
        ribs.append(rib)
    return ribs


def cut_roller_opening(front, center, radius):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64,
        radius=radius,
        depth=4.0,
        location=center,
        rotation=(0, pi / 2, 0),
    )
    boolean_difference(front, bpy.context.object)


def build_sleeve(collection, prefix, center_x, mat, cutaway=False):
    width = 54.0
    length = 86.0 if not cutaway else 70.0
    bottom = rounded_box(
        collection,
        f"{prefix}_SleeveBottom",
        (center_x, 0, 1.0),
        (length, width, 2.0),
        mat,
        0.65,
    )
    rounded_box(
        collection,
        f"{prefix}_SleeveFarWall",
        (center_x, 26.0, 9.5),
        (length, 2.0, 17.0),
        mat,
        0.65,
    )
    if not cutaway:
        rounded_box(
            collection,
            f"{prefix}_SleeveNearWall",
            (center_x, -26.0, 9.5),
            (length, 2.0, 17.0),
            mat,
            0.65,
        )
        rounded_box(
            collection,
            f"{prefix}_SleeveRoof",
            (center_x, 0, 18.0),
            (length, width, 2.0),
            mat,
            0.65,
        )
    else:
        rounded_box(
            collection,
            f"{prefix}_SleeveRoofCutaway",
            (center_x - 2.0, 13.5, 18.0),
            (length - 4.0, 27.0, 2.0),
            mat,
            0.65,
        )
        rounded_box(
            collection,
            f"{prefix}_KeeperRoofBridge",
            (center_x + 28.5, 2.5, 18.0),
            (8.0, 22.0, 2.0),
            mat,
            0.45,
        )
    rounded_box(
        collection,
        f"{prefix}_SleeveBack",
        (center_x - length / 2 + 1.0, 7.0 if cutaway else 0, 9.5),
        (2.0, 38.0 if cutaway else 52.0, 17.0),
        mat,
        0.65,
    )
    return bottom


def build_drawer_tray(
    collection,
    prefix,
    center_x,
    mat,
    front_x,
    cutaway=False,
):
    length = 88.0 if not cutaway else 68.0
    rounded_box(
        collection,
        f"{prefix}_DrawerBase",
        (center_x, 0, 2.1),
        (length, 50.0 if not cutaway else 49.0, 2.0),
        mat,
        0.55,
    )
    rounded_box(
        collection,
        f"{prefix}_DrawerFarWall",
        (center_x, 24.2 if not cutaway else 23.7, 8.0),
        (length, 1.6, 12.0),
        mat,
        0.45,
    )
    if not cutaway:
        rounded_box(
            collection,
            f"{prefix}_DrawerNearWall",
            (center_x, -24.2, 8.0),
            (length, 1.6, 12.0),
            mat,
            0.45,
        )
    rounded_box(
        collection,
        f"{prefix}_DrawerBack",
        (center_x - length / 2 + 1.0, 6.0 if cutaway else 0, 8.0),
        (2.0, 36.0 if cutaway else 48.0, 12.0),
        mat,
        0.45,
    )
    for index, offset in enumerate((-9.0, 19.0) if not cutaway else (-7.0, 14.0)):
        rounded_box(
            collection,
            f"{prefix}_Divider_{index}",
            (center_x + offset, 6.0 if cutaway else 0, 8.0),
            (1.4, 36.0 if cutaway else 48.0, 12.0),
            mat,
            0.35,
        )
    front = rounded_box(
        collection,
        f"{prefix}_DrawerPull",
        (front_x - 1.4, 0, 8.0),
        (2.8, 50.0, 14.0),
        mat,
        0.55,
    )
    return front


def build_edge_roller(
    collection,
    prefix,
    front_x,
    center_z,
    rotor_mat,
    recess_mat,
    drawer_mat,
    locked=False,
    axial_takeup=0.0,
    include_internal=False,
    keeper_mat=None,
    detent_mat=None,
):
    """Build one shrouded roller and, optionally, its internal mechanism."""
    wheel_center_x = front_x - 0.45 + axial_takeup
    wheel_radius = 7.55

    torus_x(
        collection,
        f"{prefix}_ShroudLip",
        (front_x - 0.55, 0, center_z),
        7.95,
        0.34,
        recess_mat,
    )
    cylinder_x(
        collection,
        f"{prefix}_Roller",
        (wheel_center_x, 0, center_z),
        wheel_radius,
        1.55,
        rotor_mat,
    )
    create_edge_texture(
        collection,
        prefix,
        front_x + 0.23 + axial_takeup,
        0,
        center_z,
        wheel_radius,
        recess_mat,
    )

    # A broad face dimple offers a second access method without adding a wing.
    indicator = rounded_box(
        collection,
        f"{prefix}_DirectionBar",
        (front_x + 0.34 + axial_takeup, 0, center_z),
        (0.18, 7.0 if not locked else 1.25, 1.25 if not locked else 7.0),
        recess_mat,
        0.28,
    )
    indicator["rotation_state"] = "locked" if locked else "unlocked"

    if not include_internal:
        return

    # One-piece keyed rotor: face roller, shaft, and dog rotate as one assembly.
    shaft_center = (front_x - 5.25 + axial_takeup, 0, center_z)
    cylinder_x(
        collection,
        f"{prefix}_RotorShaft",
        shaft_center,
        1.65,
        8.8,
        rotor_mat,
    )

    collar_x = front_x - 9.15 + axial_takeup
    cylinder_x(
        collection,
        f"{prefix}_DetentCollar",
        (collar_x, 0, center_z),
        3.8,
        2.0,
        rotor_mat,
    )

    # A visible two-level face cam substitutes for a wear-prone printed thread.
    cylinder_x(
        collection,
        f"{prefix}_DrawerThrustRing",
        (front_x - 7.75, 0, center_z),
        4.45,
        0.70,
        drawer_mat,
    )
    ramp = rounded_box(
        collection,
        f"{prefix}_QuarterTurnRamp",
        (front_x - 8.28 + axial_takeup / 2, -2.8, center_z + 2.2),
        (0.95, 3.4, 1.4),
        rotor_mat,
        0.30,
    )
    ramp.rotation_euler.x = radians(-22 if locked else 22)

    dog_x = front_x - 12.95 + axial_takeup
    dog = rounded_box(
        collection,
        f"{prefix}_CamDog",
        (dog_x, 0, center_z),
        (2.6, 12.5, 2.8),
        rotor_mat,
        0.45,
    )
    if locked:
        dog.rotation_euler.x = pi / 2

    # The sleeve keeper has a ramped entry face and a square retaining face.
    rounded_box(
        collection,
        f"{prefix}_SleeveKeeper",
        (front_x - 10.15, 0, 15.55),
        (3.2, 14.0, 2.9),
        keeper_mat,
        0.38,
    )
    keeper_entry = rounded_box(
        collection,
        f"{prefix}_KeeperEntryRamp",
        (front_x - 8.95, -4.7, 14.55),
        (1.1, 2.0, 2.0),
        keeper_mat,
        0.30,
    )
    keeper_entry.rotation_euler.x = radians(28)

    # Integral PETG leaf spring: shallow unlocked pocket, deeper locked pocket.
    spring_z = 12.75 if locked else 12.50
    spring = rounded_box(
        collection,
        f"{prefix}_DetentLeaf",
        (front_x - 9.55, -4.5, spring_z),
        (8.2, 1.15, 0.82),
        detent_mat,
        0.30,
    )
    spring.rotation_euler.y = radians(-3.0 if locked else 1.5)
    sphere(
        collection,
        f"{prefix}_DetentNose",
        (collar_x, -4.5, spring_z - 0.48),
        0.68 if locked else 0.58,
        detent_mat,
    )
    # Dark marker represents the asymmetric endpoint pocket in the rotor collar.
    rounded_box(
        collection,
        f"{prefix}_DetentPocket",
        (collar_x - 1.03, -3.55, center_z + 3.55),
        (0.30, 1.35, 1.0 if locked else 0.72),
        recess_mat,
        0.20,
    )


def add_stage(stage_collection):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = 0.30
    scene.world.color = (0.015, 0.019, 0.026)
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.012, 0.016, 0.024, 1.0)
    background.inputs["Strength"].default_value = 0.10

    bpy.ops.mesh.primitive_plane_add(size=520, location=(0, 0, -2.05))
    ground = relink(bpy.context.object, stage_collection)
    ground.name = "V6_Ground"
    ground.data.materials.append(MATS["ground"])

    bpy.ops.object.camera_add(location=(135, -170, 112))
    camera = relink(bpy.context.object, stage_collection)
    camera.name = "V6_Camera"
    camera.data.type = "ORTHO"
    scene.camera = camera

    def area(name, location, energy, size, color):
        bpy.ops.object.light_add(type="AREA", location=location)
        light = relink(bpy.context.object, stage_collection)
        light.name = name
        light.data.energy = energy
        light.data.shape = "DISK"
        light.data.size = size
        light.data.color = color
        look_at(light, (0, 0, 8))

    area("V6_Key", (15, -70, 130), 4800, 75, (1.0, 0.89, 0.78))
    area("V6_Fill", (-100, 70, 75), 3400, 65, (0.66, 0.82, 1.0))
    area("V6_Rim", (90, 80, 110), 4300, 55, (0.62, 0.90, 1.0))

    # Sun lights keep the concept legible even when Blender interprets the
    # millimetre-scale geometry as metre-scale for inverse-square area lighting.
    bpy.ops.object.light_add(type="SUN", location=(150, -170, 170))
    sun_key = relink(bpy.context.object, stage_collection)
    sun_key.name = "V6_SunKey"
    sun_key.data.energy = 1.45
    sun_key.data.color = (1.0, 0.90, 0.78)
    look_at(sun_key, (0, 0, 7))

    bpy.ops.object.light_add(type="SUN", location=(-140, -80, 105))
    sun_fill = relink(bpy.context.object, stage_collection)
    sun_fill.name = "V6_SunFill"
    sun_fill.data.energy = 0.90
    sun_fill.data.color = (0.64, 0.80, 1.0)
    look_at(sun_fill, (0, 0, 7))

    bpy.ops.object.light_add(type="SUN", location=(20, 170, 150))
    sun_rim = relink(bpy.context.object, stage_collection)
    sun_rim.name = "V6_SunRim"
    sun_rim.data.energy = 0.75
    sun_rim.data.color = (0.68, 0.88, 1.0)
    look_at(sun_rim, (0, 0, 7))
    return camera


def render(scene, camera, path, resolution, ortho_scale, camera_location, target):
    camera.location = camera_location
    camera.data.ortho_scale = ortho_scale
    look_at(camera, target)
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


# Start a clean, isolated V6 presentation without deleting prior design work.
remove_prior_preview()
root_collection = create_collection(SCENE_COLLECTION, bpy.context.scene.collection)
overview_collection = create_collection(OVERVIEW_COLLECTION, root_collection)
mechanism_collection = create_collection(MECHANISM_COLLECTION, root_collection)
inventory_collection = create_collection(INVENTORY_COLLECTION, root_collection)
stage_collection = create_collection(STAGE_COLLECTION, root_collection)

for obj in bpy.context.scene.objects:
    obj.hide_render = True

MATS = {
    "sleeve": material("V6 Sleeve", (0.015, 0.44, 0.54), 0.08, 0.34),
    "drawer": material("V6 Drawer", (0.78, 0.30, 0.018), 0.02, 0.37),
    "rotor": material("V6 Rotor", (0.96, 0.63, 0.06), 0.32, 0.28),
    "keeper": material("V6 Keeper", (0.10, 0.78, 0.84), 0.18, 0.30),
    "detent": material("V6 Detent", (0.87, 0.22, 0.46), 0.06, 0.33),
    "recess": material("V6 Recess", (0.012, 0.014, 0.018), 0.05, 0.24),
    "text": material("V6 Text", (0.78, 0.81, 0.86), 0.0, 0.42),
    "ground": material("V6 Ground", (0.022, 0.028, 0.037), 0.0, 0.72),
}

camera = add_stage(stage_collection)
for obj in root_collection.all_objects:
    obj.hide_render = False
inventory_collection.hide_render = True

# Overview: the roller is accessible from its face and exposed top/bottom arcs,
# but remains between the sleeve's broad top and bottom planes.
build_sleeve(overview_collection, "Overview", -58.0, MATS["sleeve"])
overview_front = build_drawer_tray(
    overview_collection,
    "Overview",
    33.0,
    MATS["drawer"],
    78.4,
)
cut_roller_opening(overview_front, (78.0, 0, 8.4), 8.05)
build_edge_roller(
    overview_collection,
    "Overview",
    78.4,
    8.4,
    MATS["rotor"],
    MATS["recess"],
    MATS["drawer"],
)
overview_title = label(
    overview_collection,
    "Overview_Title",
    "SHROUDED EDGE ROLLER  /  FACE + TOP + BOTTOM THUMB ACCESS",
    (-4, 0, 28),
    4.2,
    MATS["text"],
)

mechanism_collection.hide_render = True
billboard_text(overview_title, camera)
render(
    bpy.context.scene,
    camera,
    OVERVIEW_PATH,
    (1500, 950),
    224,
    (138, -175, 112),
    (-3, 0, 8),
)

# Mechanism storyboard: same one-piece rotor, shown before and after the
# quarter-turn ramp provides 0.6 mm axial take-up and the deep endpoint click.
overview_collection.hide_render = True
mechanism_collection.hide_render = False

for cx, prefix, locked, takeup in (
    (-50.0, "Unlocked", False, 0.0),
    (50.0, "Locked", True, 0.6),
):
    build_sleeve(
        mechanism_collection,
        prefix,
        cx,
        MATS["sleeve"],
        cutaway=True,
    )
    front_x = cx + 35.0
    front = build_drawer_tray(
        mechanism_collection,
        prefix,
        cx,
        MATS["drawer"],
        front_x,
        cutaway=True,
    )
    cut_roller_opening(front, (front_x - 0.4, 0, 8.4), 8.05)
    build_edge_roller(
        mechanism_collection,
        prefix,
        front_x,
        8.4,
        MATS["rotor"],
        MATS["recess"],
        MATS["drawer"],
        locked=locked,
        axial_takeup=takeup,
        include_internal=True,
        keeper_mat=MATS["keeper"],
        detent_mat=MATS["detent"],
    )

unlocked_label = label(
    mechanism_collection,
    "Unlocked_Label",
    "UNLOCKED  /  SHALLOW CLICK  /  CAM CLEARS",
    (-50, 0, 29),
    3.6,
    MATS["text"],
)
locked_label = label(
    mechanism_collection,
    "Locked_Label",
    "LOCKED  /  0.6 mm TAKE-UP  /  DEEP CLICK",
    (50, 0, 29),
    3.6,
    MATS["text"],
)

camera.location = (82, -224, 108)
camera.data.ortho_scale = 194
look_at(camera, (2, 0, 8))
for obj in (unlocked_label, locked_label):
    billboard_text(obj, camera)

render(
    bpy.context.scene,
    camera,
    MECHANISM_PATH,
    (1500, 950),
    194,
    (82, -224, 108),
    (2, 0, 8),
)

# High three-quarter inventory view.  The rotor is shown unlocked so its entire
# horizontal cam dog reads from above; the inventory explicitly distinguishes
# a separate rigid moving part from an integral compliant feature.
mechanism_collection.hide_render = True
inventory_collection.hide_render = False

inventory_center_x = -34.0
inventory_front_x = -8.0
rounded_box(
    inventory_collection,
    "Inventory_DrawerBase",
    (inventory_center_x, 0, 2.1),
    (52.0, 42.0, 2.0),
    MATS["drawer"],
    0.55,
)
inventory_front = rounded_box(
    inventory_collection,
    "Inventory_DrawerPull",
    (inventory_front_x - 1.4, 0, 8.0),
    (2.8, 42.0, 14.0),
    MATS["drawer"],
    0.55,
)
cut_roller_opening(
    inventory_front,
    (inventory_front_x - 0.4, 0, 8.4),
    8.05,
)

# Only the local roof bridge is retained so the keeper remains structurally
# contextual without hiding the rotor and compliant detent from the top view.
rounded_box(
    inventory_collection,
    "Inventory_KeeperRoofBridge",
    (inventory_front_x - 10.1, 7.0, 18.0),
    (8.0, 18.0, 2.0),
    MATS["sleeve"],
    0.45,
)
build_edge_roller(
    inventory_collection,
    "Inventory",
    inventory_front_x,
    8.4,
    MATS["rotor"],
    MATS["recess"],
    MATS["drawer"],
    locked=False,
    axial_takeup=0.0,
    include_internal=True,
    keeper_mat=MATS["keeper"],
    detent_mat=MATS["detent"],
)

inventory_labels = [
    label(
        inventory_collection,
        "Inventory_Title",
        "TOP MECHANISM VIEW\nMOVING-PART INVENTORY",
        (34, 25, 26),
        3.6,
        MATS["text"],
    ),
    label(
        inventory_collection,
        "Inventory_Count",
        "1 SEPARATE ROTOR\n+ 1 INTEGRAL FLEXURE",
        (34, 12, 25),
        3.0,
        MATS["text"],
    ),
    label(
        inventory_collection,
        "Inventory_Rotor_Label",
        "1  GOLD: ROTOR ASSEMBLY\nROLLER / SHAFT / RAMP / CAM DOG",
        (34, -1, 24),
        2.65,
        MATS["rotor"],
    ),
    label(
        inventory_collection,
        "Inventory_Detent_Label",
        "2  MAGENTA: PETG DETENT LEAF + NOSE",
        (34, -14, 23),
        2.55,
        MATS["detent"],
    ),
    label(
        inventory_collection,
        "Inventory_Detent_Note",
        "FLEXES IN PLACE; NOT A SEPARATE COMPONENT",
        (34, -21, 22),
        2.15,
        MATS["text"],
    ),
    label(
        inventory_collection,
        "Inventory_Keeper_Label",
        "CYAN: FIXED SLEEVE KEEPER",
        (34, -29, 21),
        2.35,
        MATS["keeper"],
    ),
    label(
        inventory_collection,
        "Inventory_Drawer_Label",
        "ORANGE: FIXED DRAWER BEARING + THRUST FACE",
        (34, -36, 20),
        2.15,
        MATS["drawer"],
    ),
]

camera.location = (26, -42, 245)
camera.data.ortho_scale = 146
look_at(camera, (0, 0, 8))

# Parent inventory copy to the camera so the legend is a true screen-aligned
# plate rather than perspective-skewed world text.
inventory_screen_positions = (
    (42, 45, -100),
    (42, 29, -100),
    (42, 11, -100),
    (42, -7, -100),
    (42, -18, -100),
    (42, -31, -100),
    (42, -42, -100),
)
for obj, screen_position in zip(inventory_labels, inventory_screen_positions):
    obj.parent = camera
    obj.location = screen_position
    obj.rotation_euler = (0, 0, 0)

render(
    bpy.context.scene,
    camera,
    INVENTORY_PATH,
    (1600, 1000),
    146,
    (26, -42, 245),
    (0, 0, 8),
)

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
print(f"V6 edge-roller preview saved to {BLEND_PATH}")
print(f"Overview: {OVERVIEW_PATH}")
print(f"Mechanism: {MECHANISM_PATH}")
print(f"Top inventory: {INVENTORY_PATH}")
