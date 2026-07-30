#!/usr/bin/env bash
# Slice a prepared plate for a requested material without changing orientation.
set -euo pipefail

input="${1:?usage: slice_for_material_p2s.sh INPUT.stl OUTPUT.3mf MATERIAL [PROFILE]}"
output="${2:?usage: slice_for_material_p2s.sh INPUT.stl OUTPUT.3mf MATERIAL [PROFILE]}"
material="${3:?material is required, for example PETG}"
profile="${4:-Generic $material @BBL P2S.json}"
image="${PRINTFARM_ORCA_IMAGE:-printfarm-orca:latest}"
profiles=/opt/orca/squashfs-root/resources/profiles/BBL
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

cp "$input" "$work/pillbox_supportless_plate.stl"
docker run --rm --entrypoint bash "$image" \
  -c "cat '$profiles/process/0.20mm Standard @BBL P2S.json'" > "$work/process.json"
docker run --rm -v "$work":/work --entrypoint sh "$image" \
  -c "cp -a '$profiles/filament' /work/filament && chmod -R a+rwX /work/filament"
python3 - "$work/filament" "$profile" "$work/filament-resolved.json" <<'PY'
import json, os, sys
root, requested, output = sys.argv[1:]
by_name = {}
for name in os.listdir(root):
    if not name.endswith('.json'):
        continue
    try:
        data = json.load(open(os.path.join(root, name)))
        by_name[data.get('name')] = data
    except Exception:
        pass
def resolve(data, seen=()):
    parent = data.get('inherits')
    if not parent:
        return dict(data)
    if parent in seen or parent not in by_name:
        raise SystemExit(f'cannot resolve filament parent: {parent}')
    merged = resolve(by_name[parent], seen + (parent,))
    merged.update(data)
    return merged
resolved = resolve(json.load(open(os.path.join(root, requested))))
resolved.update({'inherits': '', 'from': 'User', 'instantiation': 'true'})
json.dump(resolved, open(output, 'w'))
PY

python3 - "$work/process.json" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as stream:
    process = json.load(stream)
process.update({
    "from": "User",
    "name": "pillbox-supportless-material",
    "enable_support": "0",
    "support_type": "normal(auto)",
})
with open(path, "w", encoding="utf-8") as stream:
    json.dump(process, stream)
PY

docker run --rm -v "$work":/work -e XDG_RUNTIME_DIR=/tmp -e HOME=/tmp \
  --entrypoint /opt/orca/squashfs-root/AppRun "$image" \
  --curr-bed-type "Textured PEI Plate" \
  --load-settings "$profiles/machine/Bambu Lab P2S 0.4 nozzle.json;/work/process.json" \
  --load-filaments "/work/filament-resolved.json" \
  --scale 1 --arrange 1 --slice 0 \
  --export-3mf pillbox_supportless_petg.3mf --outputdir /work \
  /work/pillbox_supportless_plate.stl

test -s "$work/pillbox_supportless_petg.3mf"
cp "$work/pillbox_supportless_petg.3mf" "$output"
echo "sliced supportless $material job with '$profile' -> $output"
