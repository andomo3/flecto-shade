"""The modelled shade house stands up.

scene.js keeps the structure as plain data, so what carries what can be checked instead
of taken on trust. These tests run the page's own file under node and assert the
acceptance criterion the picture rests on: nothing floats. Every member is carried by
one below it, every module clamps to the two rails bounding its bay, every rail meets a
primary beam, every beam meets a column, and every column reaches the slab.

They also assert the layout: square bays on one roof plane, three zones by default and
four supported, and a roof that shuts without a gap beside a rail.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PAGE = REPO_ROOT / "software" / "page"
NODE = shutil.which("node")
TOUCH = 1e-6


def plan(zone_count):
    if not NODE:
        pytest.skip("node is not installed, so the browser geometry cannot be executed")
    script = (
        "global.self = global;\n"
        "require(" + json.dumps(str(PAGE / "flectofin.js")) + ");\n"
        "var House = require(" + json.dumps(str(PAGE / "scene.js")) + ");\n"
        "process.stdout.write(JSON.stringify(House.planStructure(" + str(zone_count) + ")));\n"
    )
    finished = subprocess.run([NODE, "-e", script], capture_output=True, text=True,
                              timeout=60, cwd=str(REPO_ROOT))
    assert finished.returncode == 0, finished.stderr
    return json.loads(finished.stdout)


@pytest.fixture(scope="module")
def house():
    return plan(3)


def box(member):
    return {
        "x0": member["x"] - member["width"] / 2, "x1": member["x"] + member["width"] / 2,
        "y0": member["y"] - member["depth"] / 2, "y1": member["y"] + member["depth"] / 2,
        "z0": member["z"] - member["height"] / 2, "z1": member["z"] + member["height"] / 2,
    }


def overlaps_in_plan(a, b, slack=0.0):
    return (min(a["x1"], b["x1"]) - max(a["x0"], b["x0"]) > -slack and
            min(a["y1"], b["y1"]) - max(a["y0"], b["y0"]) > -slack)


def of_kind(house, *kinds):
    return [member for member in house["members"] if member["kind"] in kinds]


# ------------------------------------------------------------------ nothing floats

def test_every_member_is_carried_by_something_below_it(house):
    """The acceptance criterion: no roof part floats or disconnects from the frame."""
    boxes = [(member, box(member)) for member in house["members"]]
    floating = []
    for member, shape in boxes:
        if member["kind"] == "ground":
            continue
        carried = any(
            other is not member
            and other_shape["z1"] >= shape["z0"] - TOUCH
            and other_shape["z0"] <= shape["z0"] + TOUCH
            and overlaps_in_plan(shape, other_shape)
            for other, other_shape in boxes
        )
        if not carried:
            floating.append(f'{member["kind"]} at ({member["x"]:.2f}, {member["y"]:.2f}, '
                            f'{member["z"]:.2f})')
    assert not floating, "these members rest on nothing: " + "; ".join(sorted(set(floating)))


def test_the_load_path_runs_module_to_rail_to_beam_to_column_to_slab(house):
    rails = [box(member) for member in of_kind(house, "rail")]
    beams = [box(member) for member in of_kind(house, "primary-beam")]
    columns = [box(member) for member in of_kind(house, "column")]
    slab = box(of_kind(house, "slab")[0])

    for clamp in of_kind(house, "clamp"):
        shape = box(clamp)
        assert any(overlaps_in_plan(shape, rail) and rail["z1"] >= shape["z0"] - TOUCH
                   for rail in rails), "a clamp holds a module to no rail"

    for rail in rails:
        assert any(overlaps_in_plan(rail, beam) and beam["z1"] >= rail["z0"] - TOUCH
                   for beam in beams), "a secondary rail meets no primary beam"

    for beam in beams:
        assert any(overlaps_in_plan(beam, column) and column["z1"] >= beam["z0"] - TOUCH
                   for column in columns), "a primary beam meets no column"

    for column in columns:
        assert column["z0"] <= slab["z1"] + TOUCH, "a column does not reach the slab"


def test_every_module_clamps_to_the_two_rails_that_bound_its_bay(house):
    """Two clamps per module, one on each of the rails at the ends of its backbone."""
    clamps = of_kind(house, "clamp")
    assert len(clamps) == 2 * len(house["bays"])
    row_rails = [member for member in of_kind(house, "rail") if member["depth"] < 0.1]
    rail_lines = sorted(member["y"] for member in row_rails)

    for bay in house["bays"]:
        # inside half a bay, so the neighbouring bay's clamps are not counted
        near = [clamp for clamp in clamps
                if abs(clamp["x"] - bay["x"]) < 1e-9
                and abs(clamp["y"] - bay["y"]) < house["cell"] / 2]
        assert len(near) == 2, f'bay at {bay["x"]:.2f} is not held at both ends'
        for clamp in near:
            assert any(abs(clamp["y"] - line) < house["railHalfY"] + 0.05 for line in rail_lines), \
                "a clamp sits away from any rail"


# ---------------------------------------------------------------------- the layout

def test_the_closed_roof_cells_are_square_and_on_one_plane(house):
    cell = house["cell"]
    xs = sorted({round(bay["x"], 6) for bay in house["bays"]})
    ys = sorted({round(bay["y"], 6) for bay in house["bays"]})
    for index in range(1, len(xs)):
        assert xs[index] - xs[index - 1] == pytest.approx(cell, abs=1e-9)
    for index in range(1, len(ys)):
        assert ys[index] - ys[index - 1] == pytest.approx(cell, abs=1e-9)
    assert len(xs) * cell == pytest.approx(house["width"], abs=1e-9)
    assert len(ys) * cell == pytest.approx(house["depth"], abs=1e-9)
    assert house["levels"]["ROOF_Z"] > house["levels"]["RAIL_Z"] > house["levels"]["BEAM_Z"]


def test_three_zones_by_default_and_a_fourth_is_supported():
    three, four = plan(3), plan(4)
    assert sorted({bay["zone"] for bay in three["bays"]}) == ["A", "B", "C"]
    assert sorted({bay["zone"] for bay in four["bays"]}) == ["A", "B", "C", "D"]
    assert len(four["bays"]) == len(three["bays"]) + three["bayColumnsPerZone"] * three["bayRows"]
    assert four["width"] > three["width"]
    assert len(four["beds"]) == 4
    per_zone = {}
    for bay in four["bays"]:
        per_zone[bay["zone"]] = per_zone.get(bay["zone"], 0) + 1
    assert set(per_zone.values()) == {three["bayColumnsPerZone"] * three["bayRows"]}


def test_the_zones_are_marked_out_without_relying_on_colour(house):
    dividers = of_kind(house, "zone-divider")
    boundaries = sorted(member["x"] for member in dividers if member["depth"] > member["width"])
    expected = [house["left"] + index * house["bayColumnsPerZone"] * house["cell"]
                for index in range(4)]
    assert boundaries == pytest.approx(expected, abs=1e-9)
    for member in dividers:
        assert member["z"] > house["levels"]["RAIL_Z"], "a zone outline must read above the rails"


def test_the_beds_leave_a_circulation_gap(house):
    beds = house["beds"]
    zone_width = house["bayColumnsPerZone"] * house["cell"]
    for bed in beds:
        assert bed["width"] < zone_width, "a bed fills its zone with no path beside it"
        assert bed["depth"] < house["depth"]
    for index in range(1, len(beds)):
        gap = (beds[index]["x"] - beds[index]["width"] / 2) - \
              (beds[index - 1]["x"] + beds[index - 1]["width"] / 2)
        assert gap > 0.1, "two beds meet with no circulation gap between them"


def test_the_structure_is_deterministic():
    assert plan(3) == plan(3)
    source = (PAGE / "scene.js").read_text(encoding="utf-8")
    assert "Math.random" not in source, "the model must draw the same way every time"
    assert "seededRandom" in source, "the illustrative planting is seeded, not random"
