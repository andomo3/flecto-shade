"""Turn the shade house CAD into `model.json`, the mesh the console renders.

Input is a STEP assembly exported from SolidWorks: one base plate carrying 22 flaps in
11 rows of 2. Every flap is hinged at its own local origin and extends 50 mm along
local -Y, so swinging a flap is a rotation about its local X axis.

The 11 rows are banded across the three crop zones, so one roof shows three zones
behaving differently, which is the whole claim about resolution.

This is an asset step, not part of the build. It needs `cascadio` and `trimesh`, which
are deliberately NOT in software/requirements.txt: the page ships the committed JSON and
the project gains no dependency. Rerun it only when the CAD changes:

    python -m venv /tmp/cadvenv && /tmp/cadvenv/bin/pip install cascadio trimesh
    /tmp/cadvenv/bin/python software/page/build_model.py --step /path/to/third.STEP
"""

import argparse
import json
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parent / "model.json"

# Geometry is written as integers in tenths of a millimetre, which is finer than the
# tessellation tolerance and keeps the file small.
SCALE = 10.0

# The flaps sit in 11 rows. Banded across the three zones, low Y first.
ZONE_BANDS = [("A", 0, 4), ("B", 4, 8), ("C", 8, 11)]


def load_scene(step_path, glb_path):
    import cascadio
    import trimesh

    cascadio.step_to_glb(str(step_path), str(glb_path), tol_linear=0.02, tol_angular=0.1)
    return trimesh.load(str(glb_path))


def build(step_path, out_path=OUT_PATH, glb_path=None):
    import numpy as np

    glb_path = glb_path or out_path.parent / "_model.glb"
    scene = load_scene(step_path, glb_path)

    meshes, mesh_index = [], {}
    instances = []

    for node in scene.graph.nodes_geometry:
        transform, geom_name = scene.graph[node]
        geom = scene.geometry[geom_name]

        # The exporter names every instance separately, so dedupe on the geometry
        # itself. The 22 flaps are two shapes repeated, and storing them once is the
        # difference between a 465 KB file and a 60 KB one.
        positions = np.round(np.asarray(geom.vertices, dtype=float) * 1000.0 * SCALE).astype(int)
        indices = np.asarray(geom.faces, dtype=int)
        key = (positions.tobytes(), indices.tobytes())
        if key not in mesh_index:
            mesh_index[key] = len(meshes)
            meshes.append({
                "name": geom_name,
                "positions": positions.ravel().tolist(),
                "indices": indices.ravel().tolist(),
            })

        origin = np.asarray(transform, dtype=float)[:3, 3] * 1000.0
        instances.append({
            "mesh": mesh_index[key],
            "node": node,
            "origin": [round(value * SCALE) for value in origin],
            "kind": "base" if "Part 1" in geom_name else "flap",
        })

    base = next(i for i in instances if i["kind"] == "base")
    flaps = [i for i in instances if i["kind"] == "flap"]

    # Rows, low Y first. Each row holds the two flaps that share a Y.
    rows = {}
    for flap in flaps:
        rows.setdefault(flap["origin"][1], []).append(flap)
    ordered = [rows[key] for key in sorted(rows)]

    for zone, start, stop in ZONE_BANDS:
        for row in ordered[start:stop]:
            for flap in row:
                flap["zone"] = zone
    for flap in flaps:
        flap.setdefault("zone", ZONE_BANDS[-1][0])

    all_xyz = []
    for inst in instances:
        mesh = meshes[inst["mesh"]]
        pos = np.asarray(mesh["positions"], dtype=float).reshape(-1, 3)
        all_xyz.append(pos + np.asarray(inst["origin"], dtype=float))
    stacked = np.vstack(all_xyz)
    low, high = stacked.min(axis=0), stacked.max(axis=0)
    centre = ((low + high) / 2).tolist()

    payload = {
        "source": Path(step_path).name,
        "note": "Modelled. Geometry is the team's CAD, tessellated once and committed.",
        "units": "tenths of a millimetre",
        "scale": SCALE,
        "centre": [round(value) for value in centre],
        "extent": [round(value) for value in (high - low).tolist()],
        "hinge": {
            "axis": "x",
            "comment": "Each flap is hinged at its local origin and runs 50 mm along -Y.",
        },
        "rows": len(ordered),
        "zone_bands": [{"zone": z, "first_row": a, "last_row": b - 1} for z, a, b in ZONE_BANDS],
        "meshes": meshes,
        "instances": instances,
    }

    out_path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
    Path(glb_path).unlink(missing_ok=True)
    return out_path, payload


def main():
    parser = argparse.ArgumentParser(description="Tessellate the shade house CAD.")
    parser.add_argument("--step", required=True, help="path to the STEP assembly")
    parser.add_argument("--out", default=str(OUT_PATH))
    args = parser.parse_args()

    path, payload = build(Path(args.step), Path(args.out))
    size = path.stat().st_size
    print(f"wrote {path} ({size / 1024:.1f} KB)")
    print(f"  {len(payload['meshes'])} unique meshes, {len(payload['instances'])} instances")
    print(f"  extent {payload['extent']} tenths of a mm, {payload['rows']} flap rows")
    for band in payload["zone_bands"]:
        count = sum(1 for i in payload["instances"] if i.get("zone") == band["zone"])
        print(f"  zone {band['zone']}: rows {band['first_row']} to {band['last_row']}, {count} flaps")


if __name__ == "__main__":
    main()
