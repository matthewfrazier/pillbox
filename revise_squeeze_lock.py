import bpy
from mathutils import Vector
from pathlib import Path

ROOT = Path('/Users/mf/code/pillbox')


def activate(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def rounded_box(name, center, size, radius=0.4, segments=3):
    bpy.ops.mesh.primitive_cube_add(location=center)
    obj = bpy.context.object
    obj.name = name
    obj.scale = tuple(v / 2 for v in size)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel = obj.modifiers.new('Printable edge radius', 'BEVEL')
    bevel.width = radius
    bevel.segments = segments
    bevel.limit_method = 'ANGLE'
    activate(obj)
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    return obj


def ellipsoid(name, center, scale):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=center)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def boolean(target, tool, operation):
    mod = target.modifiers.new(f'{operation}_{tool.name}', 'BOOLEAN')
    mod.operation = operation
    mod.solver = 'EXACT'
    mod.object = tool
    activate(target)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(tool, do_unlink=True)


def union_many(target, objects):
    for obj in objects:
        boolean(target, obj, 'UNION')


def export_stl(obj, path):
    activate(obj)
    bpy.ops.wm.stl_export(filepath=str(path), export_selected_objects=True,
                          apply_modifiers=True, ascii_format=False)


sleeve_old = bpy.data.objects['Sleeve_Monolithic']
drawer_old = bpy.data.objects['Drawer_Monolithic']
sleeve = sleeve_old.copy()
sleeve.data = sleeve_old.data.copy()
bpy.context.collection.objects.link(sleeve)
sleeve.name = 'Sleeve_SqueezeLock_V2'
drawer = drawer_old.copy()
drawer.data = drawer_old.data.copy()
bpy.context.collection.objects.link(drawer)
drawer.name = 'Drawer_SqueezeLock_V2'

# Display geometry is arranged with the drawer pulled out. The closed position is
# drawer X - 86 mm: the original grip then protrudes 2 mm. The new fascia/pads end
# at X=109, leaving a deliberate 5 mm graspable projection in the closed position.
fascia = rounded_box('Extended_full_width_grip', (107.35, 0, 9.1), (3.3, 45.0, 8.4), 0.8, 5)

# Cut the side wall away around each flexure, leaving a genuine free cantilever.
# Each arm is anchored at its rear end (X=95.2..97.2), with an 11.8 mm free length.
for sign in (-1, 1):
    cutter = rounded_box(f'Flexure_relief_{sign:+d}', (102.7, sign * 24.65, 9.0),
                          (11.4, 3.0, 8.4), 0.45, 3)
    boolean(drawer, cutter, 'DIFFERENCE')

arms = []
for sign in (-1, 1):
    arm = rounded_box(f'Squeeze_arm_{sign:+d}', (101.9, sign * 24.72, 9.0),
                      (13.4, 1.25, 6.2), 0.55, 5)
    pad = rounded_box(f'Squeeze_pad_{sign:+d}', (107.2, sign * 24.72, 9.0),
                      (3.4, 1.9, 8.0), 0.75, 5)
    # Rounded peg, elongated along travel so it cams smoothly into the receiver.
    peg = ellipsoid(f'Lock_peg_{sign:+d}', (101.6, sign * 25.55, 9.0), (1.45, 0.72, 1.35))
    arms.extend((arm, pad, peg))

union_many(drawer, [fascia] + arms)

# Positive-overlap anchor blocks make the cantilevers a single printable body;
# the relief cuts begin at X=97.0, so each anchor retains 0.5 mm of overlap.
anchors = []
for sign in (-1, 1):
    anchors.append(rounded_box(f'Flexure_anchor_{sign:+d}', (96.2, sign * 24.72, 9.0),
                               (3.0, 1.25, 6.2), 0.5, 4))
union_many(drawer, anchors)

# Matching blind receptacles in both sleeve walls. They stop >1 mm before the
# exterior surface and are elongated in X to tolerate normal FDM shrink/fit error.
for sign in (-1, 1):
    pocket = ellipsoid(f'Peg_receiver_{sign:+d}', (15.6, sign * 25.38, 9.0), (1.65, 0.78, 1.52))
    boolean(sleeve, pocket, 'DIFFERENCE')

# Boolean cuts against the legacy triangulated source can leave intersection
# topology. A sub-layer voxel remesh produces one closed component per part.
for obj in (sleeve, drawer):
    activate(obj)
    remesh = obj.modifiers.new('Manifold print mesh', 'REMESH')
    remesh.mode = 'VOXEL'
    remesh.voxel_size = 0.08
    remesh.use_smooth_shade = False
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    decimate = obj.modifiers.new('Print mesh simplification', 'DECIMATE')
    decimate.decimate_type = 'COLLAPSE'
    decimate.ratio = 0.14
    decimate.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=decimate.name)

for obj in (sleeve_old, drawer_old):
    obj.hide_viewport = True
    obj.hide_render = True

# Engineering metadata retained in the source file.
drawer['closed_shift_x_mm'] = -86.0
drawer['closed_grip_projection_mm'] = 5.0
drawer['lock_type'] = 'bilateral squeeze-release cantilever pegs'
drawer['flexure_free_length_mm'] = 11.8
drawer['flexure_thickness_mm'] = 1.25
drawer['peg_outward_projection_mm'] = 0.72
sleeve['receiver_type'] = 'blind bilateral rounded pockets'
sleeve['receiver_outer_wall_remaining_mm_min'] = 0.84

export_stl(sleeve, ROOT / 'pillbox_sleeve_v2_squeeze_lock.stl')
export_stl(drawer, ROOT / 'pillbox_drawer_v2_squeeze_lock.stl')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'pillbox_model_v2_squeeze_lock.blend'))
print('V2 complete', sleeve.dimensions[:], drawer.dimensions[:])
