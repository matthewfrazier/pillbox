#!/usr/bin/env python3
"""Prepare the pillbox sleeve and drawer as a supportless binary-STL plate.

The sleeve is stood on its closed -X face. The drawer remains on its broad
bottom face. Both parts are translated to Z=0 and separated on the plate.
"""

import math
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_binary_stl(path):
    data = path.read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + 50 * count:
        raise ValueError(f"expected binary STL: {path}")
    triangles = []
    for index in range(count):
        values = struct.unpack_from("<12fH", data, 84 + 50 * index)
        triangles.append([values[3:6], values[6:9], values[9:12]])
    return triangles


def normal(a, b, c):
    ux, uy, uz = (b[i] - a[i] for i in range(3))
    vx, vy, vz = (c[i] - a[i] for i in range(3))
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    length = math.sqrt(nx * nx + ny * ny + nz * nz)
    return (0.0, 0.0, 0.0) if length == 0 else (nx / length, ny / length, nz / length)


def write_binary_stl(path, name, triangles):
    header = name.encode("ascii")[:80].ljust(80, b" ")
    with path.open("wb") as stream:
        stream.write(header)
        stream.write(struct.pack("<I", len(triangles)))
        for tri in triangles:
            stream.write(struct.pack("<12fH", *(normal(*tri) + tuple(tri[0]) + tuple(tri[1]) + tuple(tri[2]) + (0,))))


def transform(triangles, fn):
    return [[fn(*vertex) for vertex in tri] for tri in triangles]


def bounds(triangles):
    points = [vertex for tri in triangles for vertex in tri]
    low = tuple(min(point[i] for point in points) for i in range(3))
    high = tuple(max(point[i] for point in points) for i in range(3))
    return low, high


def shift_to_bed(triangles, center_x):
    low, high = bounds(triangles)
    mid_x = (low[0] + high[0]) / 2
    mid_y = (low[1] + high[1]) / 2
    return transform(triangles, lambda x, y, z: (x - mid_x + center_x, y - mid_y, z - low[2]))


def main():
    sleeve = read_binary_stl(ROOT / "pillbox_sleeve_print.stl")
    drawer = read_binary_stl(ROOT / "pillbox_drawer_print.stl")

    # New Z is old X, so the sleeve's closed old -X end is the first layer.
    sleeve = transform(sleeve, lambda x, y, z: (y, z, x))
    sleeve = shift_to_bed(sleeve, -42.0)
    drawer = shift_to_bed(drawer, 42.0)

    write_binary_stl(ROOT / "pillbox_sleeve_closed_face_down.stl", "pillbox sleeve closed face down", sleeve)
    write_binary_stl(ROOT / "pillbox_drawer_bottom_down.stl", "pillbox drawer bottom down", drawer)
    write_binary_stl(ROOT / "pillbox_supportless_plate.stl", "pillbox supportless two-part plate", sleeve + drawer)

    for label, triangles in (("sleeve", sleeve), ("drawer", drawer), ("plate", sleeve + drawer)):
        low, high = bounds(triangles)
        dims = tuple(high[i] - low[i] for i in range(3))
        print(label, "bounds", tuple(round(v, 3) for v in low), tuple(round(v, 3) for v in high),
              "dimensions", tuple(round(v, 3) for v in dims), "triangles", len(triangles))


if __name__ == "__main__":
    main()
