"""Build K1's modelled display fin using only the Python standard library."""

import argparse
from collections import Counter, defaultdict
from math import isclose, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
# ASSUMED design and fabrication values, documented in README.md.
RIB_LENGTH_MM = 150.0
RIB_THICKNESS_MM = 1.5
RIB_HEIGHT_MM = 5.0
SHEET_CLEAR_WIDTH_MM = 40.0
SHEET_THICKNESS_MM = 0.4
LAYER_HEIGHT_MM = 0.2
NOZZLE_DIAMETER_MM = 0.4


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def geometry():
    """Extrude a single L section; no intersecting or internal mesh faces."""
    width = RIB_THICKNESS_MM + SHEET_CLEAR_WIDTH_MM
    section = [(0, 0), (width, 0), (width, SHEET_THICKNESS_MM),
               (RIB_THICKNESS_MM, SHEET_THICKNESS_MM),
               (RIB_THICKNESS_MM, RIB_HEIGHT_MM), (0, RIB_HEIGHT_MM)]
    vertices = [(x, y, z) for x in (0, RIB_LENGTH_MM) for y, z in section]
    caps = [(0, 1, 2), (0, 2, 3), (0, 3, 5), (3, 4, 5)]
    triangles = [tuple(reversed(f)) for f in caps]
    triangles += [tuple(i + 6 for i in f) for f in caps]
    surfaces = [list(reversed(range(6))), list(range(6, 12))]
    for i in range(6):
        j = (i + 1) % 6
        triangles += [(i, j, j+6), (i, j+6, i+6)]
        surfaces.append([i, j, j+6, i+6])
    return vertices, triangles, surfaces


def stl_text(vertices, triangles):
    lines = ['solid K1_modelled_display_fin_units_mm']
    for face in triangles:
        a, b, c = [vertices[i] for i in face]
        n = cross(sub(b, a), sub(c, a))
        length = sqrt(dot(n, n))
        lines.append('  facet normal ' + ' '.join(f'{v/length:.9g}' for v in n))
        lines.append('    outer loop')
        for p in (a, b, c):
            lines.append('      vertex ' + ' '.join(f'{v:.9g}' for v in p))
        lines += ['    endloop', '  endfacet']
    return '\n'.join(lines + ['endsolid K1_modelled_display_fin_units_mm', ''])


def scad_text():
    return f'''// K1: modelled display adaptation of ITKE's Flectofin, EP2320015.
// All dimensions are millimetres and ASSUMED; see README.md.
// Edit these dimensions, press F6 in OpenSCAD, then export STL.
// Geometry only: no deformation or structural simulation is performed.
rib_length_mm = {RIB_LENGTH_MM:g};
rib_thickness_mm = {RIB_THICKNESS_MM:g};
rib_height_mm = {RIB_HEIGHT_MM:g};
sheet_clear_width_mm = {SHEET_CLEAR_WIDTH_MM:g};
sheet_thickness_mm = {SHEET_THICKNESS_MM:g};

assert(rib_length_mm > 0 && rib_thickness_mm > 0);
assert(sheet_clear_width_mm > 0 && sheet_thickness_mm > 0);
assert(rib_height_mm > sheet_thickness_mm);
union() {{
    cube([rib_length_mm, rib_thickness_mm, rib_height_mm]);
    // The sheet extends under the rib, making a continuous solid union.
    cube([rib_length_mm, rib_thickness_mm + sheet_clear_width_mm,
          sheet_thickness_mm]);
}}
'''


def render_svg(vertices, surfaces):
    def project(p):
        x, y, z = p
        return (160 + 5*x + 2.1*y, 305 + 0.85*x - 2.2*y - 6*z)

    def points(face):
        return ' '.join(f'{x:.2f},{y:.2f}' for x, y in (project(vertices[i]) for i in face))

    camera = (12.6, -30, 12.785)
    visible = []
    for index, face in enumerate(surfaces):
        a, b, c = [vertices[i] for i in face[:3]]
        if dot(cross(sub(b, a), sub(c, a)), camera) > 0:
            depth = sum(dot(vertices[i], camera) for i in face) / len(face)
            color = '#76bca5' if index == 4 else '#263f3d'
            if index == 6:
                color = '#dda86d'
            visible.append((depth, f'<polygon points="{points(face)}" fill="{color}" stroke="#294a43" stroke-width="1.2"/>'))
    polygons = '\n'.join(item[1] for item in sorted(visible))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800">
<rect width="1200" height="800" fill="#f5f3ec"/>
<g font-family="Helvetica,Arial,sans-serif" fill="#203832">
<text x="60" y="52" font-size="15" letter-spacing="3">K1 / DISPLAY FIN / MODELLED GEOMETRY</text>
<text x="60" y="105" font-size="42" font-weight="700">One rib. One thin sheet.</text>
<text x="60" y="141" font-size="19">ITKE's Flectofin principle · EP2320015 · Display adaptation</text>
{polygons}
<path d="M 275,318 L 235,198 L 95,198" fill="none" stroke="#52665d" stroke-width="1.5"/>
<text x="60" y="187" font-size="18">Rib: {RIB_THICKNESS_MM:g} × {RIB_HEIGHT_MM:g} mm</text>
<path d="M 742,332 L 908,238 L 1130,238" fill="none" stroke="#52665d" stroke-width="1.5"/>
<text x="897" y="210" font-size="18">Sheet: {SHEET_THICKNESS_MM:g} mm thick</text>
<text x="897" y="231" font-size="16">{SHEET_CLEAR_WIDTH_MM:g} mm clear width</text>
<path d="M 157,352 L 907,479 M 154,341 L 160,363 M 904,468 L 910,490" fill="none" stroke="#52665d" stroke-width="1.4"/>
<text x="470" y="461" font-size="19">{RIB_LENGTH_MM:g} mm modelled length</text>
<line x1="60" y1="527" x2="1140" y2="527" stroke="#c6cfc4"/>
<text x="60" y="563" font-size="15" letter-spacing="2">END SECTION</text>
<path d="M 65,675 L 65,600 L 87.5,600 L 87.5,669 L 687.5,669 L 687.5,675 Z" fill="#76bca5" stroke="#294a43" stroke-width="1.5"/>
<path d="M 65,695 L 687.5,695 M 65,688 L 65,702 M 687.5,688 L 687.5,702" fill="none" stroke="#52665d"/>
<text x="264" y="724" font-size="18">{RIB_THICKNESS_MM + SHEET_CLEAR_WIDTH_MM:g} mm total width</text>
<text x="775" y="588" font-size="21" font-weight="700">Print flat, sheet down</text>
<text x="775" y="622" font-size="18">PLA · {LAYER_HEIGHT_MM:g} mm layers</text>
<text x="775" y="650" font-size="18">Two layers through the sheet</text>
<text x="775" y="687" font-size="16">Bending behaviour awaits a physical check.</text>
<text x="60" y="772" font-size="15">All dimensions are modelled design assumptions. Geometry render only; no structural solver has run.</text>
</g></svg>
'''


def check_stl(path):
    """Read the exported mesh independently and check its solid topology."""
    raw = path.read_text()
    coords = [tuple(map(float, line.split()[1:])) for line in raw.splitlines()
              if line.strip().startswith('vertex ')]
    assert len(coords) % 3 == 0 and coords, 'Incomplete STL triangles'
    faces = [coords[i:i+3] for i in range(0, len(coords), 3)]
    edges = Counter()
    directed = Counter()
    neighbours = defaultdict(set)
    volume = 0.0
    for a, b, c in faces:
        normal = cross(sub(b, a), sub(c, a))
        assert dot(normal, normal) > 1e-12, 'Degenerate triangle'
        volume += dot(a, cross(b, c)) / 6
        for u, v in ((a, b), (b, c), (c, a)):
            edges[tuple(sorted((u, v)))] += 1
            directed[(u, v)] += 1
            neighbours[u].add(v)
            neighbours[v].add(u)
    assert all(n == 2 for n in edges.values()), 'Open or non-manifold edge'
    assert all(directed[(v, u)] == n for (u, v), n in directed.items()), 'Inconsistent face orientation'
    seen = set()
    pending = [coords[0]]
    while pending:
        p = pending.pop()
        if p not in seen:
            seen.add(p)
            pending.extend(neighbours[p] - seen)
    assert seen == set(coords), 'Disconnected mesh'
    assert len(seen) - len(edges) + len(faces) == 2, 'Unexpected solid topology'
    expected_bounds = (RIB_LENGTH_MM, RIB_THICKNESS_MM + SHEET_CLEAR_WIDTH_MM, RIB_HEIGHT_MM)
    for axis, expected in enumerate(expected_bounds):
        assert min(p[axis] for p in coords) == 0
        assert isclose(max(p[axis] for p in coords), expected, abs_tol=1e-8)
    expected_volume = RIB_LENGTH_MM * (RIB_THICKNESS_MM * RIB_HEIGHT_MM + SHEET_CLEAR_WIDTH_MM * SHEET_THICKNESS_MM)
    assert isclose(volume, expected_volume, rel_tol=1e-9), 'Wrong volume or inward orientation'
    assert path.stat().st_size < 5_000_000
    print(f'PASS: one closed solid, {len(faces)} triangles, outward orientation, bounds {expected_bounds} mm, modelled volume {volume:g} mm^3')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='check existing outputs without rewriting them')
    args = parser.parse_args()
    vertices, triangles, surfaces = geometry()
    outputs = {'display-fin.stl': stl_text(vertices, triangles),
               'display-fin.scad': scad_text(),
               'display-fin.svg': render_svg(vertices, surfaces)}
    for name, content in outputs.items():
        path = HERE / name
        if args.check:
            assert path.read_text() == content, f'{name} differs from the design parameters'
        else:
            path.write_text(content)
    check_stl(HERE / 'display-fin.stl')
    print('PASS: STL, editable OpenSCAD source, and geometry render match the same dimensions')


if __name__ == '__main__':
    main()
