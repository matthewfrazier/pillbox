#!/usr/bin/env python3
"""Generate a CalculiX nonlinear sleeve-wall submodel for the pillbox detent.

Units: mm, N, MPa.  The model represents one of the two symmetric sleeve
walls.  The inner contact patch is displaced outward by the nominal detent
interference.  Top and bottom edges are fixed to represent continuity into
the sleeve roof and floor.  Results are intentionally conservative because
the imposed patch displacement prevents local contact redistribution.
"""

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--interference", type=float, default=0.30)
args = parser.parse_args()
OUT = Path(__file__).resolve().parent
tag = f"{args.interference:.2f}".replace(".", "p")
INP = OUT / f"petg_detent_wall_{tag}.inp"

# Geometry and mesh divisions.
length, thickness, height = 20.0, 1.5, 16.0
nx, ny, nz = 40, 6, 32
interference = args.interference


def node_id(i, j, k):
    return 1 + i + (nx + 1) * (j + (ny + 1) * k)


lines = [
    "*HEADING",
    "PETG pillbox sleeve wall - nonlinear detent interference submodel",
    "*NODE",
]

contact_nodes = []
fixed_nodes = []
for k in range(nz + 1):
    z = height * k / nz
    for j in range(ny + 1):
        y = thickness * j / ny
        for i in range(nx + 1):
            x = -length / 2 + length * i / nx
            nid = node_id(i, j, k)
            lines.append(f"{nid},{x:.6f},{y:.6f},{z:.6f}")
            if k in (0, nz):
                fixed_nodes.append(nid)
            # Actual 8 x 2.6 mm detent footprint on the inner sleeve face.
            if j == 0 and abs(x) <= 4.0001 and abs(z - height / 2) <= 1.3001:
                contact_nodes.append(nid)

lines.append("*ELEMENT,TYPE=C3D8R,ELSET=WALL")
eid = 1
for k in range(nz):
    for j in range(ny):
        for i in range(nx):
            n1 = node_id(i, j, k)
            n2 = node_id(i + 1, j, k)
            n3 = node_id(i + 1, j + 1, k)
            n4 = node_id(i, j + 1, k)
            n5 = node_id(i, j, k + 1)
            n6 = node_id(i + 1, j, k + 1)
            n7 = node_id(i + 1, j + 1, k + 1)
            n8 = node_id(i, j + 1, k + 1)
            lines.append(f"{eid},{n1},{n2},{n3},{n4},{n5},{n6},{n7},{n8}")
            eid += 1

def write_set(name, values):
    lines.append(f"*NSET,NSET={name}")
    for p in range(0, len(values), 16):
        lines.append(",".join(str(v) for v in values[p:p + 16]))


write_set("FIXED_EDGES", fixed_nodes)
write_set("DETENT_PATCH", contact_nodes)
lines += [
    "*MATERIAL,NAME=PETG_PRINTED_XY",
    "*ELASTIC",
    "1939.,0.38",
    "*PLASTIC",
    "46.2,0.0",
    "50.0,0.020",
    "*SOLID SECTION,ELSET=WALL,MATERIAL=PETG_PRINTED_XY",
    "*STEP,NLGEOM",
    "*STATIC",
    "0.05,1.0,1.E-05,0.10",
    "*BOUNDARY",
    "FIXED_EDGES,1,3,0.0",
    f"DETENT_PATCH,2,2,{interference:.6f}",
    "*NODE FILE",
    "U,RF",
    "*EL FILE",
    "S,PEEQ",
    "*NODE PRINT,NSET=DETENT_PATCH,TOTALS=YES",
    "RF",
    "*EL PRINT,ELSET=WALL",
    "S,PEEQ",
    "*END STEP",
]

INP.write_text("\n".join(lines) + "\n")
print(INP)
print(f"nodes={(nx+1)*(ny+1)*(nz+1)} elements={nx*ny*nz} contact_nodes={len(contact_nodes)}")
