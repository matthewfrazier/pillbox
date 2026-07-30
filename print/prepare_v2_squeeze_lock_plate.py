#!/usr/bin/env python3
"""Prepare the V2 squeeze-lock pillbox for review slicing only."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_supportless_plate import read_binary_stl, write_binary_stl, transform, shift_to_bed, bounds

ROOT = Path(__file__).resolve().parent
MODEL = ROOT.parent


def main():
    sleeve = read_binary_stl(MODEL / 'pillbox_sleeve_v2_squeeze_lock.stl')
    drawer = read_binary_stl(MODEL / 'pillbox_drawer_v2_squeeze_lock.stl')

    # Closed end down for the sleeve; broad flat bottom down for the drawer.
    sleeve = transform(sleeve, lambda x, y, z: (y, z, x))
    sleeve = shift_to_bed(sleeve, -42.0)
    drawer = shift_to_bed(drawer, 42.0)

    outputs = (
        ('pillbox_sleeve_v2_closed_end_down.stl', sleeve),
        ('pillbox_drawer_v2_bottom_down.stl', drawer),
        ('pillbox_v2_squeeze_lock_review_plate.stl', sleeve + drawer),
    )
    for name, triangles in outputs:
        write_binary_stl(ROOT / name, name.removesuffix('.stl'), triangles)
        low, high = bounds(triangles)
        print(name, 'bounds', tuple(round(v, 3) for v in low),
              tuple(round(v, 3) for v in high), 'triangles', len(triangles))


if __name__ == '__main__':
    main()
