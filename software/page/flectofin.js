/* The Flectofin module's geometry and its deformation, in one place.

   The fin is not ours. It is the Flectofin, by ITKE at the University of Stuttgart,
   patented as EP2320015. What follows is a physically informed approximation of its
   kinematics for a browser, not a structural or mechanical result, and nothing it
   produces is a validated engineering figure.

   The mechanism it approximates, in the order the parts move:

     1. A narrow backbone spans the bay and is held at both ends by conceptual clamps.
     2. Actuation shortens the chord between those clamps, so the backbone bows.
     3. Bowing tilts the local frame carried along the backbone, and that tilt is what
        drives the two thin lamellae attached along it sideways. Nothing rotates a
        lamella directly.
     4. Each lamella is treated as an inextensible strip: it bends without stretching,
        so every point keeps its arc distance from the backbone. Its shape at any
        actuation is the integral of a turning angle along that arc, which is why the
        surface curves through every intermediate position instead of staying flat and
        tilting. Nothing here scales a lamella down or fades it out.
     5. The turning angle is held at zero through the stiffer root next to the
        backbone and rises smoothly to its greatest value at the free outer edge.

   Two properties fall out of the inextensible construction and are asserted in the
   tests, because the roof depends on them:

     - The plan width of a lamella never exceeds its flat width, so a module can never
       reach into its neighbour's bay or through a supporting rail.
     - The root sits exactly on the backbone at every actuation, so a lamella can
       never detach from the member that carries it.

   Everything here is a pure function of the actuation value. Reversing actuation runs
   the same functions backwards, so the closing movement is the opening one in reverse.

   The renderer rebuilds one deformed mesh per distinct actuation value each frame, so
   this file is the only description of the shape. It is written to be replaced: swap
   `lamellaProfile` for precomputed morph targets exported from a nonlinear
   finite-element run and everything else, including the opening fraction the overlay
   reports, follows from the new shape without further change.
*/

(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) { module.exports = api; }
  root.Flectofin = api;
}(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var PARAMS = {
    span: 0.60,            /* backbone length, clamp to clamp */
    halfWidth: 0.262,      /* flat width of one lamella, backbone to free edge */
    backboneHalf: 0.016,   /* half thickness of the backbone member */
    thetaMax: 1.85,        /* greatest turning angle past the hinge band, radians */
    rootFraction: 0.20,    /* the stiffer root, as a share of the lamella width */
    hingeBand: 0.30,       /* the compliant band the bend concentrates in */
    bow: 0.125,            /* how far the backbone bows at mid span at full actuation */
    nestGap: 0.020,        /* the clearance that keeps the folded pair out of one volume */
    nestBias: 1.07,        /* one lamella turns slightly further, so the pair reads nested */
    spanFloor: 0.62,       /* the turn still felt at the clamped ends */
    across: 14,            /* mesh samples from root to free edge */
    along: 10              /* mesh samples from clamp to clamp */
  };

  function smoothstep(edge0, edge1, x) {
    var t = Math.min(1, Math.max(0, (x - edge0) / (edge1 - edge0)));
    return t * t * (3 - 2 * t);
  }

  function normalise(v) {
    var length = Math.hypot(v[0], v[1], v[2]) || 1;
    return [v[0] / length, v[1] / length, v[2] / length];
  }

  /* --- the backbone ------------------------------------------------------ */

  /* Station v runs 0 at one clamp to 1 at the other. The bow is a half cosine, so the
     deflection is zero at both clamps and greatest at mid span, which is the shape a
     strut held at its ends takes when its chord is shortened. */
  function backboneAt(v, a) {
    var s = v - 0.5;
    var y = s * PARAMS.span;
    var z = PARAMS.bow * a * Math.cos(Math.PI * s);
    var slope = -PARAMS.bow * a * Math.PI * Math.sin(Math.PI * s) / PARAMS.span;
    var tangent = normalise([0, 1, slope]);
    var lateral = [1, 0, 0];
    var up = normalise([
      lateral[1] * tangent[2] - lateral[2] * tangent[1],
      lateral[2] * tangent[0] - lateral[0] * tangent[2],
      lateral[0] * tangent[1] - lateral[1] * tangent[0]
    ]);
    return { point: [0, y, z], tangent: tangent, lateral: lateral, up: up };
  }

  /* --- the lamella ------------------------------------------------------- */

  /* How much of the turn has been taken up by arc position t, which is 0 at the
     backbone and 1 at the free edge. Zero through the stiffer root, then smooth
     through a narrow compliant band, then held: the bend concentrates where the shell
     is thinnest, and the outer part of the lamella carries it as a near rigid rotation
     of an already curved surface. */
  function rootWeight(t) {
    return smoothstep(PARAMS.rootFraction, PARAMS.rootFraction + PARAMS.hingeBand, t);
  }

  /* The turn is greatest where the backbone bows most, and never quite zero at the
     clamps, because the free edge is still free there. */
  function spanWeight(v) {
    var floor = PARAMS.spanFloor;
    return floor + (1 - floor) * Math.cos(Math.PI * (v - 0.5));
  }

  /* The cross section at station v, as an inextensible arc walked outward from the
     backbone in equal arc steps. Returns [alongLateral, alongUp] per sample, in
     lamella units, with sample 0 exactly on the backbone. */
  function lamellaProfile(a, v, samples) {
    samples = samples || PARAMS.across;
    var turn = PARAMS.thetaMax * a * spanWeight(v);
    var step = PARAMS.halfWidth / samples;
    var out = new Array(samples + 1);
    var across = 0, up = 0;
    out[0] = [0, 0];
    for (var index = 1; index <= samples; index++) {
      var angleHere = turn * rootWeight(index / samples);
      var anglePrev = turn * rootWeight((index - 1) / samples);
      /* trapezoid over the arc step keeps the strip's length exactly halfWidth */
      across += step * (Math.cos(angleHere) + Math.cos(anglePrev)) / 2;
      up += step * (Math.sin(angleHere) + Math.sin(anglePrev)) / 2;
      out[index] = [across, up];
    }
    return out;
  }

  /* One lamella point in module space. `side` is +1 or -1. */
  function lamellaPoint(side, u, v, a) {
    var profile = lamellaProfile(a * (side < 0 ? PARAMS.nestBias : 1), v);
    var index = Math.round(u * PARAMS.across);
    return placeLamella(side, profile[index], index / PARAMS.across, v, a);
  }

  /* `t` is the arc position, 0 at the backbone and 1 at the free edge. The nest gap
     is taken up along that arc rather than applied to the whole lamella, so the root
     stays on the backbone at every actuation and only the outer part of the pair moves
     apart. It is a separation for drawing, a fraction of a lamella width, and it is
     deliberately kept out of `lamellaProfile`, which is the shape model. */
  function placeLamella(side, sample, t, v, a) {
    var frame = backboneAt(v, a);
    var across = side * (sample[0] + PARAMS.nestGap * a * t + PARAMS.backboneHalf);
    var up = sample[1];
    return [
      frame.point[0] + frame.lateral[0] * across + frame.up[0] * up,
      frame.point[1] + frame.lateral[1] * across + frame.up[1] * up,
      frame.point[2] + frame.lateral[2] * across + frame.up[2] * up
    ];
  }

  /* How far one lamella reaches across the bay, seen from above, at station v. This
     is what decides whether a falling drop meets the shell or the gap, so the rain and
     the reported opening are read off the same curve. */
  function planHalfWidth(side, v, a) {
    var bias = side < 0 ? PARAMS.nestBias : 1;
    var profile = lamellaProfile(a * bias, v);
    return profile[PARAMS.across][0] + PARAMS.nestGap * a + PARAMS.backboneHalf;
  }

  /* --- what the deformation opens --------------------------------------- */

  /* The share of the bay the lamellae no longer cover, seen from above. It is read
     off the same arc the renderer draws, so the overlay and the picture agree. */
  function openingFraction(a) {
    var stations = 12, covered = 0;
    for (var index = 0; index <= stations; index++) {
      var v = index / stations;
      var weight = (index === 0 || index === stations) ? 0.5 : 1;
      var profile = lamellaProfile(a, v);
      var mirror = lamellaProfile(a * PARAMS.nestBias, v);
      var plan = profile[PARAMS.across][0] + mirror[PARAMS.across][0];
      covered += weight * plan;
    }
    covered /= stations;
    var flat = 2 * PARAMS.halfWidth;
    return Math.min(1, Math.max(0, 1 - covered / flat));
  }

  /* --- meshes ------------------------------------------------------------ */

  /* Index buffers never change, so they are built once and reused for every
     actuation value. Tints mark the stiffer root, for the fragment shader. */
  function lamellaIndices(across, along, offset) {
    var indices = [];
    for (var row = 0; row < along; row++) {
      for (var column = 0; column < across; column++) {
        var a = offset + row * (across + 1) + column;
        var b = a + 1;
        var c = offset + (row + 1) * (across + 1) + column;
        var d = c + 1;
        indices.push(a, b, d, a, d, c);
        indices.push(a, d, b, a, c, d);   /* the strip is thin, so it is drawn both ways */
      }
    }
    return indices;
  }

  function moduleTopology() {
    var across = PARAMS.across, along = PARAMS.along;
    var perLamella = (across + 1) * (along + 1);
    var indices = lamellaIndices(across, along, 0)
      .concat(lamellaIndices(across, along, perLamella));
    var tints = [];
    for (var side = 0; side < 2; side++) {
      for (var row = 0; row <= along; row++) {
        for (var column = 0; column <= across; column++) {
          var t = column / across;
          /* 1 in the stiffer root, falling to 0 past the hinge band */
          tints.push(1 - smoothstep(PARAMS.rootFraction * 0.5,
                                    PARAMS.rootFraction + PARAMS.hingeBand, t));
        }
      }
    }
    return {
      vertexCount: perLamella * 2,
      indices: indices,
      tints: tints,
      perLamella: perLamella
    };
  }

  /* Positions for both lamellae at one actuation value, written into `out`. */
  function writeLamellae(a, out) {
    var across = PARAMS.across, along = PARAMS.along, cursor = 0;
    for (var side = 0; side < 2; side++) {
      var sign = side === 0 ? 1 : -1;
      var bias = sign < 0 ? PARAMS.nestBias : 1;
      for (var row = 0; row <= along; row++) {
        var v = row / along;
        var profile = lamellaProfile(a * bias, v);
        for (var column = 0; column <= across; column++) {
          var point = placeLamella(sign, profile[column], column / across, v, a);
          out[cursor++] = point[0];
          out[cursor++] = point[1];
          out[cursor++] = point[2];
        }
      }
    }
    return out;
  }

  /* The backbone drawn as a slender four sided prism swept along its own curve, so
     that the bend is visible rather than implied. */
  function backboneTopology() {
    var along = PARAMS.along, indices = [];
    for (var row = 0; row < along; row++) {
      for (var corner = 0; corner < 4; corner++) {
        var next = (corner + 1) % 4;
        var a = row * 4 + corner, b = row * 4 + next;
        var c = (row + 1) * 4 + corner, d = (row + 1) * 4 + next;
        indices.push(a, b, d, a, d, c);
      }
    }
    var cap = along * 4;
    indices.push(0, 1, 2, 0, 2, 3, cap, cap + 2, cap + 1, cap, cap + 3, cap + 2);
    return { vertexCount: (along + 1) * 4, indices: indices };
  }

  function writeBackbone(a, out) {
    var along = PARAMS.along, half = PARAMS.backboneHalf, cursor = 0;
    var corners = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
    for (var row = 0; row <= along; row++) {
      var frame = backboneAt(row / along, a);
      for (var corner = 0; corner < 4; corner++) {
        var lateral = corners[corner][0] * half;
        var up = corners[corner][1] * half * 1.9;
        out[cursor++] = frame.point[0] + frame.lateral[0] * lateral + frame.up[0] * up;
        out[cursor++] = frame.point[1] + frame.lateral[1] * lateral + frame.up[1] * up;
        out[cursor++] = frame.point[2] + frame.lateral[2] * lateral + frame.up[2] * up;
      }
    }
    return out;
  }

  /* --- what the technical overlay points at ------------------------------ */

  function annotations(a) {
    var backbone = [], edgeLeft = [], edgeRight = [];
    for (var index = 0; index <= PARAMS.along; index++) {
      var v = index / PARAMS.along;
      backbone.push(backboneAt(v, a).point);
      edgeLeft.push(lamellaPoint(1, 1, v, a));
      edgeRight.push(lamellaPoint(-1, 1, v, a));
    }
    return {
      backbone: backbone,
      freeEdgeLeft: edgeLeft,
      freeEdgeRight: edgeRight,
      supports: [backboneAt(0, a).point, backboneAt(1, a).point],
      rootLeft: lamellaPoint(1, PARAMS.rootFraction, 0.5, a),
      rootRight: lamellaPoint(-1, PARAMS.rootFraction, 0.5, a),
      crown: backboneAt(0.5, a).point,
      openingFraction: openingFraction(a)
    };
  }

  var PART_LABELS = [
    { id: "backbone", label: "Backbone", note: "Carries the bay and takes the actuation." },
    { id: "root", label: "Stiffer root", note: "Holds the lamella to the backbone." },
    { id: "lamella-left", label: "Left lamella", note: "Thin shell, bends without stretching." },
    { id: "lamella-right", label: "Right lamella", note: "Its mirror, nested when folded." },
    { id: "free-edge", label: "Free edge", note: "Deforms most, and sets the opening." },
    { id: "clamp", label: "Conceptual clamp", note: "Where the backbone meets the rail." },
    { id: "actuation", label: "Actuation", note: "Shortens the chord, so the backbone bows." }
  ];

  return {
    PARAMS: PARAMS,
    PART_LABELS: PART_LABELS,
    smoothstep: smoothstep,
    backboneAt: backboneAt,
    rootWeight: rootWeight,
    spanWeight: spanWeight,
    lamellaProfile: lamellaProfile,
    lamellaPoint: lamellaPoint,
    planHalfWidth: planHalfWidth,
    openingFraction: openingFraction,
    moduleTopology: moduleTopology,
    writeLamellae: writeLamellae,
    backboneTopology: backboneTopology,
    writeBackbone: writeBackbone,
    annotations: annotations
  };
}));
