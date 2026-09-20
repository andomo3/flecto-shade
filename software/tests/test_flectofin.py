"""The Flectofin deformation, checked where it has to hold.

The geometry lives in JavaScript because the browser draws it, so these tests run the
same file the page loads, under node, and assert the properties the roof depends on.
Where node is not installed the file is still read and its structure checked, so the
suite reports rather than silently skipping everything.

Nothing here claims the approximation is mechanically valid. What it claims is that the
approximation behaves like a thin shell bending about a bowing backbone rather than
like a panel being rotated, scaled, or faded out, and that the roof it makes is
physically consistent: nothing detaches, nothing interpenetrates, and a shut roof is
shut.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PAGE = REPO_ROOT / "software" / "page"
FIN = PAGE / "flectofin.js"
NODE = shutil.which("node")

# Geometry scene.js places the modules on. Kept here so a change to either file that
# would let the rain leak through a shut roof fails a test rather than a demonstration.
CELL = 0.64
RAIL_HALF_X = 0.045
RAIL_HALF_Y = 0.035


def run_js(body):
    """Evaluate a snippet against the page's own flectofin.js and return its JSON."""
    if not NODE:
        pytest.skip("node is not installed, so the browser geometry cannot be executed")
    script = (
        "var Fin = require(" + json.dumps(str(FIN)) + ");\n"
        "var out = (function () {\n" + body + "\n})();\n"
        "process.stdout.write(JSON.stringify(out));\n"
    )
    finished = subprocess.run([NODE, "-e", script], capture_output=True, text=True,
                              timeout=60, cwd=str(REPO_ROOT))
    assert finished.returncode == 0, finished.stderr
    return json.loads(finished.stdout)


@pytest.fixture(scope="module")
def source():
    return FIN.read_text(encoding="utf-8")


# ------------------------------------------------------------------ the mechanism

def test_the_backbone_bows_and_carries_the_lamellae():
    """Actuation bends the backbone, and the lamellae follow the frame it carries."""
    result = run_js("""
      var out = { rise: [], rootOffset: [] };
      [0, 0.25, 0.5, 0.75, 1].forEach(function (a) {
        out.rise.push(Fin.backboneAt(0.5, a).point[2]);
        // the root sits on the backbone at every actuation, to within the member's own
        // half thickness, so a lamella can never come away from what carries it
        var root = Fin.lamellaPoint(1, 0, 0.5, a);
        var spine = Fin.backboneAt(0.5, a).point;
        out.rootOffset.push(Math.hypot(root[0] - spine[0], root[1] - spine[1],
                                       root[2] - spine[2]));
      });
      out.clampedEnds = [Fin.backboneAt(0, 1).point[2], Fin.backboneAt(1, 1).point[2]];
      return out;
    """)
    assert result["rise"] == sorted(result["rise"]), "the backbone bow must grow with actuation"
    assert result["rise"][0] == 0, "a closed module has a straight backbone"
    assert result["rise"][-1] > 0.05, "a fully actuated backbone has to visibly bow"
    assert max(abs(end) for end in result["clampedEnds"]) < 1e-12, \
        "both clamps hold the backbone in the roof plane"
    tolerance = run_js("return Fin.PARAMS.backboneHalf;") + 0.006
    assert max(result["rootOffset"]) <= tolerance, "the root left the backbone"


def test_the_lamella_bends_without_stretching():
    """An inextensible strip: its arc length is its flat width at every actuation."""
    result = run_js("""
      var flat = Fin.PARAMS.halfWidth, worst = 0;
      for (var step = 0; step <= 20; step++) {
        for (var row = 0; row <= 10; row++) {
          var profile = Fin.lamellaProfile(step / 20, row / 10);
          var length = 0;
          for (var index = 1; index < profile.length; index++) {
            length += Math.hypot(profile[index][0] - profile[index - 1][0],
                                 profile[index][1] - profile[index - 1][1]);
          }
          worst = Math.max(worst, Math.abs(length - flat) / flat);
        }
      }
      return worst;
    """)
    assert result < 0.02, f"the lamella stretched or shrank by {result:.1%}"


def test_the_surface_curves_rather_than_tilting_as_a_rigid_panel():
    """A rotated flat panel has one turning angle. A bending shell has many."""
    result = run_js("""
      var profile = Fin.lamellaProfile(0.6, 0.5), angles = [];
      for (var index = 1; index < profile.length; index++) {
        angles.push(Math.atan2(profile[index][1] - profile[index - 1][1],
                               profile[index][0] - profile[index - 1][0]));
      }
      return { spread: Math.max.apply(null, angles) - Math.min.apply(null, angles),
               rootAngle: angles[0], edgeAngle: angles[angles.length - 1] };
    """)
    assert result["spread"] > 0.5, "the cross section is flat, so this is a rigid rotation"
    assert abs(result["rootAngle"]) < 0.02, "the stiffer root should barely turn"
    assert result["edgeAngle"] > result["rootAngle"], "the free edge must turn most"


def test_the_root_is_stiffer_than_the_free_edge():
    weights = run_js("""
      return [0, 0.1, 0.2, 0.35, 0.6, 0.85, 1].map(function (t) { return Fin.rootWeight(t); });
    """)
    assert weights[0] == 0 and weights[1] == 0, "nothing turns inside the root"
    assert weights == sorted(weights), "stiffness must fall smoothly outward"
    assert weights[-1] == 1, "the free edge carries the whole turn"


def test_actuation_opens_the_roof_smoothly_and_reverses():
    result = run_js("""
      var forward = [], back = [];
      for (var step = 0; step <= 40; step++) { forward.push(Fin.openingFraction(step / 40)); }
      for (var step = 40; step >= 0; step--) { back.push(Fin.openingFraction(step / 40)); }
      back.reverse();
      var worstJump = 0;
      for (var index = 1; index < forward.length; index++) {
        worstJump = Math.max(worstJump, forward[index] - forward[index - 1]);
      }
      return { forward: forward, same: JSON.stringify(forward) === JSON.stringify(back),
               worstJump: worstJump };
    """)
    opening = result["forward"]
    assert opening[0] == 0, "a shut module opens nothing"
    assert opening[-1] > 0.5, "a fully actuated module has to open most of its bay"
    assert opening == sorted(opening), "the opening must grow with actuation, never dip"
    assert result["worstJump"] < 0.06, "the movement must be continuous, with no step"
    assert result["same"], "closing is opening run backwards"


def test_the_paired_lamellae_never_share_a_volume():
    """They fold toward one another and nest. They must not pass through each other."""
    result = run_js("""
      var worst = Infinity;
      for (var step = 0; step <= 20; step++) {
        var a = step / 20;
        for (var row = 0; row <= 10; row++) {
          var v = row / 10;
          var left = Fin.lamellaPoint(1, 1, v, a), right = Fin.lamellaPoint(-1, 1, v, a);
          worst = Math.min(worst, left[0] - right[0]);
        }
      }
      return worst;
    """)
    assert result > 0.02, f"the free edges came within {result:.4f} of each other"


def test_a_shut_roof_is_shut_and_an_open_one_is_open():
    """The rain is tested against this reach, so a shut zone cannot leak onto its bed."""
    reach = CELL / 2 - RAIL_HALF_X
    result = run_js(f"""
      var reach = {reach};
      var shutWorst = Infinity, openBest = 0;
      for (var row = 0; row <= 40; row++) {{
        var v = row / 40;
        [1, -1].forEach(function (side) {{
          shutWorst = Math.min(shutWorst, Fin.planHalfWidth(side, v, 0) - reach);
          openBest = Math.max(openBest, reach - Fin.planHalfWidth(side, v, 1));
        }});
      }}
      return {{ shutWorst: shutWorst, openBest: openBest, span: Fin.PARAMS.span }};
    """)
    assert result["shutWorst"] >= 0, (
        "a shut module leaves a gap beside the rail, so rain would reach a zone the "
        "console reports as excluding it")
    assert result["openBest"] > 0.1, "an actuated module must leave a real opening"
    assert CELL - result["span"] <= RAIL_HALF_Y * 2, (
        "the gap between bay rows is wider than the rail that covers it")


def test_the_plan_reach_never_grows_past_the_bay():
    """A module has to stay inside its own square bay at every actuation.

    The arc itself can only contract in plan, and the nest gap adds at most its own
    width, so the reach is bounded well inside half a bay and a module can never meet
    its neighbour or cross a supporting rail.
    """
    result = run_js("""
      var shut = Fin.planHalfWidth(1, 0.5, 0), worst = 0;
      for (var step = 0; step <= 20; step++) {
        for (var row = 0; row <= 10; row++) {
          [1, -1].forEach(function (side) {
            worst = Math.max(worst, Fin.planHalfWidth(side, row / 10, step / 20));
          });
        }
      }
      return { worst: worst, shut: shut, nestGap: Fin.PARAMS.nestGap };
    """)
    assert result["worst"] < CELL / 2, "a module reached outside its own bay"
    assert result["worst"] <= result["shut"] + result["nestGap"] + 1e-9, (
        "the reach grew by more than the nest gap, so the arc is stretching")


def test_the_mesh_is_whole_and_indexed():
    result = run_js("""
      var topology = Fin.moduleTopology();
      var positions = new Float32Array(topology.vertexCount * 3);
      Fin.writeLamellae(0.5, positions);
      var finite = Array.prototype.every.call(positions, function (value) {
        return Number.isFinite(value);
      });
      var highest = Math.max.apply(null, topology.indices);
      var spine = Fin.backboneTopology();
      var spinePositions = new Float32Array(spine.vertexCount * 3);
      Fin.writeBackbone(1, spinePositions);
      return {
        finite: finite, highest: highest, vertexCount: topology.vertexCount,
        tints: topology.tints.length,
        spineFinite: Array.prototype.every.call(spinePositions, Number.isFinite),
        spineHighest: Math.max.apply(null, spine.indices),
        spineVertices: spine.vertexCount
      };
    """)
    assert result["finite"] and result["spineFinite"], "the mesh holds a value that is not a number"
    assert result["highest"] < result["vertexCount"], "an index points past the mesh"
    assert result["spineHighest"] < result["spineVertices"]
    assert result["tints"] == result["vertexCount"], "every vertex needs its root tint"


def test_the_annotations_name_every_part_the_overlay_shows():
    result = run_js("""
      var marks = Fin.annotations(0.7);
      return { keys: Object.keys(marks).sort(),
               supports: marks.supports.length,
               opening: marks.openingFraction,
               parts: Fin.PART_LABELS.map(function (part) { return part.id; }) };
    """)
    for key in ("backbone", "freeEdgeLeft", "freeEdgeRight", "rootLeft", "rootRight",
                "supports", "openingFraction"):
        assert key in result["keys"], f"the overlay cannot point at {key}"
    assert result["supports"] == 2, "a module is held at both ends"
    assert 0 < result["opening"] < 1
    for part in ("backbone", "root", "lamella-left", "lamella-right", "free-edge",
                 "clamp", "actuation"):
        assert part in result["parts"]


# ------------------------------------------------------ what the file must not do

def test_the_module_is_deformed_and_not_rotated_scaled_or_hidden(source):
    """The defect this replaced: a panel scaled toward zero and slid out of the way."""
    assert "p.x *= residual" not in source
    assert "rotationX" not in source and "rotationY" not in source
    assert "opacity" not in source
    assert "lamellaProfile" in source and "backboneAt" in source


def test_the_geometry_is_deterministic_and_fetches_nothing(source):
    assert "Math.random" not in source, "the module geometry must be reproducible"
    assert "fetch(" not in source
    for address in ("http://", "https://"):
        assert address not in source


def test_the_file_says_what_the_approximation_is_not(source):
    lowered = source.lower()
    assert "not a structural" in lowered or "not for structural" in lowered or \
challenge_text(lowered), "the file must say it is not a validated engineering result"
    assert "flectofin" in lowered and "itke" in lowered and "ep2320015" in lowered.replace(" ", "")
    assert "finite-element" in lowered or "finite element" in lowered, \
        "the file must name what would replace the approximation"


def challenge_text(lowered):
    return "not a structural or mechanical result" in lowered or \
        "physically informed approximation" in lowered
