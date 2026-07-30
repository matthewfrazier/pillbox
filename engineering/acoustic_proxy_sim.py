"""Blender/Bullet comparative rattle test using standardized 5 mm steel balls.

Run with:
  blender -b --python acoustic_proxy_sim.py

This is a comparative impact-energy model, not an absolute sound-pressure
prediction. SI units are used so Bullet receives physically scaled geometry.
"""

import bpy
import csv
import json
import math
from pathlib import Path
from mathutils import Vector

OUT = Path(__file__).resolve().parent
ORIGINAL_SCENE = bpy.context.scene
FPS = 240
FRAMES = 720
LENGTH_SCALE = 1000.0  # Blender units per meter; use millimetres for Bullet stability
BALL_D = 5.0
BALL_MASS = 0.000513

VARIANTS = {
    "smooth_petg": {"restitution": 0.45, "friction": 0.25},
    "textured_petg": {"restitution": 0.30, "friction": 0.45},
    "tpu_90a_liner": {"restitution": 0.12, "friction": 0.65},
}


def cube(name, location, dimensions):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def add_rigid(obj, kind, mass=0.0, restitution=0.0, friction=0.5):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = kind
    obj.rigid_body.collision_shape = "BOX" if kind == "PASSIVE" else "SPHERE"
    obj.rigid_body.mass = mass
    obj.rigid_body.restitution = restitution
    obj.rigid_body.friction = friction
    obj.rigid_body.linear_damping = 0.04
    obj.rigid_body.angular_damping = 0.08
    obj.rigid_body.use_margin = True
    obj.rigid_body.collision_margin = 0.1
    obj.select_set(False)


def shake_location(frame):
    t = frame / FPS
    return Vector((
        6.0 * math.sin(2 * math.pi * 4.0 * t) + 2.0 * math.sin(2 * math.pi * 11.0 * t),
        3.0 * math.sin(2 * math.pi * 7.0 * t + 0.4),
        1.5 * math.sin(2 * math.pi * 5.0 * t),
    ))


def run_variant(name, surface):
    scene = bpy.data.scenes.new(f"TEMP_acoustic_{name}")
    bpy.context.window.scene = scene
    scene.render.fps = FPS
    scene.frame_start = 1
    scene.frame_end = FRAMES
    scene.gravity = (0, 0, -9810.0)
    bpy.ops.rigidbody.world_add()
    world = scene.rigidbody_world
    world.substeps_per_frame = 8
    world.solver_iterations = 30
    world.time_scale = 1.0

    # One current pillbox compartment: 38.9 x 47.2 x 13.9 mm usable volume.
    inner_x, inner_y, inner_z = 38.9, 47.2, 13.9
    wall_t = 1.5
    parts = [
        cube("floor", (0, 0, -wall_t / 2), (inner_x, inner_y, wall_t)),
        cube("ceiling", (0, 0, inner_z + wall_t / 2), (inner_x, inner_y, wall_t)),
        cube("wall_xn", (-inner_x / 2 - wall_t / 2, 0, inner_z / 2), (wall_t, inner_y, inner_z)),
        cube("wall_xp", (inner_x / 2 + wall_t / 2, 0, inner_z / 2), (wall_t, inner_y, inner_z)),
        cube("wall_yn", (0, -inner_y / 2 - wall_t / 2, inner_z / 2), (inner_x, wall_t, inner_z)),
        cube("wall_yp", (0, inner_y / 2 + wall_t / 2, inner_z / 2), (inner_x, wall_t, inner_z)),
    ]
    for part in parts:
        add_rigid(part, "PASSIVE", restitution=surface["restitution"], friction=surface["friction"])
        part.rigid_body.kinematic = True
        for frame in range(1, FRAMES + 1, 4):
            part.location = shake_location(frame)
            part.keyframe_insert("location", frame=frame)

    balls = []
    starts = [(-12, -14), (-4, -14), (4, -14), (12, -14),
              (-12, 0), (-4, 0), (4, 0), (12, 0)]
    for i, (x, y) in enumerate(starts):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=BALL_D / 2,
                                             location=(x, y, BALL_D / 2 + 0.2))
        ball = bpy.context.object
        ball.name = f"steel_ball_{i+1}"
        add_rigid(ball, "ACTIVE", BALL_MASS, restitution=0.70, friction=0.20)
        balls.append(ball)

    rows = []
    prior = None
    cumulative_delta_ke = 0.0
    peak_ke = 0.0
    for frame in range(1, FRAMES + 1):
        scene.frame_set(frame)
        positions = [b.matrix_world.translation.copy() for b in balls]
        if prior is not None:
            velocities = [(p - q) * (FPS / LENGTH_SCALE) for p, q in zip(positions, prior)]
            total_ke = sum(0.5 * BALL_MASS * v.length_squared for v in velocities)
            if frame > 12:  # discard Bullet contact initialization transient
                peak_ke = max(peak_ke, total_ke)
            if rows and frame > 12:
                # Positive downward jumps in resolved kinetic energy are an
                # impact/dissipation proxy. It includes ball-ball collisions.
                cumulative_delta_ke += max(0.0, rows[-1][2] - total_ke)
            rows.append((frame, frame / FPS, total_ke))
        else:
            rows.append((frame, frame / FPS, 0.0))
        prior = positions

    tail = [r[2] for r in rows[-FPS:]]
    result = {
        "variant": name,
        "surface_restitution": surface["restitution"],
        "surface_friction": surface["friction"],
        "balls": len(balls),
        "ball_diameter_mm": BALL_D,
        "ball_mass_g": BALL_MASS * 1000,
        "peak_total_kinetic_energy_mJ": peak_ke * 1000,
        "cumulative_energy_drop_proxy_mJ": cumulative_delta_ke * 1000,
        "last_second_rms_kinetic_energy_mJ": (sum(v*v for v in tail) / len(tail)) ** 0.5 * 1000,
    }
    with (OUT / f"acoustic_proxy_{name}.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("frame", "time_s", "total_kinetic_energy_J"))
        writer.writerows(rows)
    # Restore the product scene and remove every temporary simulation object.
    bpy.context.window.scene = ORIGINAL_SCENE
    for obj in list(scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.scenes.remove(scene)
    return result


results = [run_variant(name, surface) for name, surface in VARIANTS.items()]
(OUT / "acoustic_proxy_results.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
