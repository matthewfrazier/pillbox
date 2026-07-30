#!/usr/bin/env python3
"""Auditable impact/rebound proxy using commercial 5 mm 52100 balls."""

import json
from pathlib import Path

MASS_KG = 0.000513
BALLS = 8
G = 9.80665
DROP_HEIGHTS_M = (0.005, 0.010)

# These coefficients are explicit hypotheses for ranking prototypes. Replace
# them with e=sqrt(rebound_height/drop_height) from a high-speed-video test.
SURFACES = {
    "smooth_petg": 0.45,
    "textured_petg": 0.30,
    "tpu_90a_liner": 0.12,
}

results = []
for height in DROP_HEIGHTS_M:
    incident = BALLS * MASS_KG * G * height
    for surface, e in SURFACES.items():
        rebound = incident * e * e
        dissipated = incident - rebound
        results.append({
            "surface": surface,
            "balls": BALLS,
            "ball_mass_g": MASS_KG * 1000,
            "drop_height_mm": height * 1000,
            "assumed_coefficient_of_restitution": e,
            "incident_energy_mJ": incident * 1000,
            "rebound_energy_mJ": rebound * 1000,
            "energy_not_returned_to_rebound_mJ": dissipated * 1000,
            "rebound_height_mm": height * e * e * 1000,
        })

out = Path(__file__).with_name("bearing_drop_proxy_results.json")
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
