/* The modelled shade house: structure, modules, camera, and the technical overlay.

   The structure is drawn as a real one stands up, and the tests depend on it:
   a column carries a primary beam, a primary beam carries a secondary rail, and every
   Flectofin module clamps to the two rails that bound its bay. Nothing is placed in
   the air. When a mounting detail is not established by a source it is drawn as a
   conceptual clamp and labelled as one, rather than shown as engineered hardware.

   The module's shape comes from flectofin.js and from nowhere else. Every module in a
   zone shares that zone's actuation, so one deformed mesh is built per zone per frame
   and drawn once per bay.

   This is a browser approximation for explaining an operating decision. It is not a
   structural or mechanical result and carries no validated figure.
*/

(function (root) {
  "use strict";

  var Fin = root.Flectofin;

  /* --- the house, in metres of modelled geometry ------------------------- */

  var CELL = 0.64;                 /* one square roof bay, on one roof plane */
  var BAY_COLUMNS_PER_ZONE = 3;
  var BAY_ROWS = 4;
  var COLUMN_TOP = 1.80;
  var BEAM_Z = 1.87;               /* primary beams sit on the columns */
  var RAIL_Z = 1.955;              /* secondary rails sit on the primary beams */
  var ROOF_Z = 2.02;               /* the module plane, carried by the rails */
  var BED_Z = 0.19;
  var PATH = 0.26;                 /* circulation gap between the ground beds */
  var MOVE_MS = 1500;
  var LETTERS = ["A", "B", "C", "D"];
  var RAIL_HALF_X = 0.045;         /* half width of a rail between two bay columns */
  var RAIL_HALF_Y = 0.035;         /* half width of a rail between two bay rows */

  /* Rain, drawn in the scene rather than over it, so the roof can stop it.

     The drop count and the fall speed come from the hour's modelled rain rate. The
     speed range is the ordinary terminal velocity band for raindrops, wider drops
     falling faster at heavier rates; the drop count is an illustrative density, not a
     count of anything real, and no figure here is read off the screen. What the
     rain is strict about is where it goes: a drop is tested against the same plan
     geometry the deformation produces, so it is stopped by a shut module, stopped by a
     rail, and passes only through an opening the rules actually made. A zone the
     console reports as excluding rain therefore cannot show a drop reaching its bed. */
  var RAIN = {
    DROPS_PER_MM: 24,     /* illustrative density per mm of modelled hourly rain */
    MAX_DROPS: 900,
    SLOW_FALL: 4.5,       /* metres per second at a light rate */
    FAST_FALL: 8.0,       /* metres per second at a heavy rate */
    HEAVY_MM: 25.0,       /* the rate at which the fall speed tops out */
    EXPOSURE: 0.026,      /* seconds of fall drawn as one streak */
    SHEAR: 0.17,          /* lateral slant of a streak */
    TOP: 2.4,             /* how far above the roof plane drops enter */
    SPLASH: 0.055         /* half length of an impact tick */
  };

  /* One palette, shared with style.css.

     These are the same hex values the stylesheet declares as custom properties, so the
     modelled roof and the page around it cannot drift apart. The shader works in linear
     light and gamma encodes on the way out, so every hex is converted once here rather
     than eyeballed as a triple. Change a colour in :root, change it here, and the whole
     console moves together. */
  var PALETTE = {
    loam:       "#22221b",   /* the ground under the house */
    slab:       "#2f2f27",
    soil:       "#4a3a2a",   /* a raised bed */
    soilRim:    "#6b5c48",
    timber:     "#b7ae9f",   /* columns and rails, raw timber */
    timberDeep: "#8c8374",   /* beams, in shadow */
    timberPale: "#ded8cf",
    clamp:      "#a89a86",
    divider:    "#e6dccd",   /* sand, marking a zone boundary */
    backbone:   "#9a9384",
    root:       "#6f6a5d",
    stem:       "#4a5c41",
    leaf:       "#5d7052",   /* moss */
    leafLight:  "#7d9070",
    rain:       "#8fb6c2",   /* river stone */
    shadow:     "#161610"
  };

  /* sRGB hex to the linear triple the shader multiplies its lighting into. */
  function tone(hex) {
    var value = parseInt(hex.slice(1), 16);
    return [16, 8, 0].map(function (shift) {
      var channel = ((value >> shift) & 255) / 255;
      return channel <= 0.04045
        ? channel / 12.92
        : Math.pow((channel + 0.055) / 1.055, 2.4);
    });
  }

  var TONE = {
    ground:     tone(PALETTE.loam),
    slab:       tone(PALETTE.slab),
    bed:        tone(PALETTE.soil),
    bedRim:     tone(PALETTE.soilRim),
    column:     tone(PALETTE.timber),
    beam:       tone(PALETTE.timberDeep),
    rail:       tone(PALETTE.timberPale),
    rain:       tone(PALETTE.rain),
    clamp:      tone(PALETTE.clamp),
    divider:    tone(PALETTE.divider),
    backbone:   tone(PALETTE.backbone),
    root:       tone(PALETTE.root),
    stem:       tone(PALETTE.stem),
    leaf:       tone(PALETTE.leaf),
    leafLight:  tone(PALETTE.leafLight),
    shadow:     tone(PALETTE.shadow)
  };

  /* The membrane carries the zone's state, in the same family the console's chips use:
     moss is automatic, river stone is admitted rain, clay is a manual hold, burnt
     sienna is a conflict, and dried grass is unavailable. */
  var MEMBRANE = {
    normal:   tone("#5d7052"),
    rain:     tone("#4f6b75"),
    manual:   tone("#c18c5d"),
    conflict: tone("#a85448"),
    idle:     tone("#78786c")
  };


  var VERT = [
    "#version 300 es",
    "in vec3 aPos;",
    "in float aTint;",
    "uniform mat4 uProj; uniform mat4 uView; uniform mat4 uModel;",
    "out vec3 vWorld; out float vTint;",
    "void main() {",
    "  vec4 world = uModel * vec4(aPos, 1.0);",
    "  vWorld = world.xyz; vTint = aTint;",
    "  gl_Position = uProj * uView * world;",
    "}"
  ].join("\n");

  var FRAG = [
    "#version 300 es",
    "precision highp float;",
    "in vec3 vWorld; in float vTint;",
    "uniform vec3 uColor; uniform vec3 uTintColor; uniform vec3 uLight;",
    "uniform float uAlpha; uniform float uFlat;",
    "out vec4 frag;",
    "void main() {",
    "  vec3 base = mix(uColor, uTintColor, clamp(vTint, 0.0, 1.0));",
    "  if (uFlat > 0.5) { frag = vec4(pow(base, vec3(0.4545)), uAlpha); return; }",
    "  vec3 n = normalize(cross(dFdx(vWorld), dFdy(vWorld)));",
    "  vec3 key = normalize(uLight);",
    "  float lambert = abs(dot(n, key));",
    "  float sky = 0.5 + 0.5 * abs(n.z);",
    "  float rim = pow(1.0 - abs(n.z), 3.0) * 0.10;",
    "  vec3 colour = base * (0.20 + 0.56 * lambert + 0.15 * sky) + rim;",
    "  frag = vec4(pow(colour, vec3(0.4545)), uAlpha);",
    "}"
  ].join("\n");

  /* --- small matrix helpers ---------------------------------------------- */

  function identity() {
    return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
  }

  function multiply(a, b) {
    var out = new Float32Array(16);
    for (var column = 0; column < 4; column++) {
      for (var row = 0; row < 4; row++) {
        out[column * 4 + row] =
          a[row] * b[column * 4] + a[4 + row] * b[column * 4 + 1] +
          a[8 + row] * b[column * 4 + 2] + a[12 + row] * b[column * 4 + 3];
      }
    }
    return out;
  }

  function translation(x, y, z) {
    var m = identity();
    m[12] = x; m[13] = y; m[14] = z;
    return m;
  }

  function scaling(x, y, z) {
    var m = identity();
    m[0] = x; m[5] = y; m[10] = z;
    return m;
  }

  function boxModel(x, y, z, width, depth, height) {
    return multiply(translation(x, y, z), scaling(width, depth, height));
  }

  function perspective(fovy, aspect, near, far) {
    var f = 1 / Math.tan(fovy / 2), m = new Float32Array(16);
    m[0] = f / aspect; m[5] = f; m[11] = -1;
    m[10] = (far + near) / (near - far);
    m[14] = (2 * far * near) / (near - far);
    return m;
  }

  function subtract(a, b) { return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]; }
  function dot(a, b) { return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]; }
  function cross(a, b) {
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
  }
  function unit(v) {
    var length = Math.hypot(v[0], v[1], v[2]) || 1;
    return [v[0]/length, v[1]/length, v[2]/length];
  }

  function lookAt(eye, target, up) {
    var z = unit(subtract(eye, target));
    var x = unit(cross(up, z));
    var y = cross(z, x);
    return new Float32Array([
      x[0], y[0], z[0], 0,
      x[1], y[1], z[1], 0,
      x[2], y[2], z[2], 0,
      -dot(x, eye), -dot(y, eye), -dot(z, eye), 1
    ]);
  }

  function project(matrix, point) {
    var x = point[0], y = point[1], z = point[2];
    return [
      matrix[0]*x + matrix[4]*y + matrix[8]*z + matrix[12],
      matrix[1]*x + matrix[5]*y + matrix[9]*z + matrix[13],
      matrix[2]*x + matrix[6]*y + matrix[10]*z + matrix[14],
      matrix[3]*x + matrix[7]*y + matrix[11]*z + matrix[15]
    ];
  }

  /* Flattens geometry onto the bed plane along the key light, for a contact shadow. */
  function shadowMatrix(light, planeZ) {
    var m = identity();
    m[8] = -light[0] / light[2];
    m[9] = -light[1] / light[2];
    m[10] = 0;
    m[12] = planeZ * light[0] / light[2];
    m[13] = planeZ * light[1] / light[2];
    m[14] = planeZ;
    return m;
  }

  /* --- static meshes ------------------------------------------------------ */

  function boxMesh() {
    return {
      positions: [
        -.5,-.5,-.5, .5,-.5,-.5, .5,.5,-.5, -.5,.5,-.5,
        -.5,-.5,.5, .5,-.5,.5, .5,.5,.5, -.5,.5,.5
      ],
      tints: [0,0,0,0,0,0,0,0],
      indices: [
        0,2,1, 0,3,2, 4,5,6, 4,6,7, 0,1,5, 0,5,4,
        1,2,6, 1,6,5, 2,3,7, 2,7,6, 3,0,4, 3,4,7
      ]
    };
  }

  function leafMesh() {
    return {
      positions: [0,.55,.06, .30,.05,.01, 0,-.5,.03, -.30,.05,.01, 0,.05,.12],
      tints: [1, 0, .4, 0, .6],
      indices: [0,1,4, 1,2,4, 2,3,4, 3,0,4, 3,2,1, 3,1,0]
    };
  }

  function seededRandom(seed) {
    var value = seed >>> 0;
    return function () {
      value += 0x6D2B79F5;
      var t = value;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  /* --- the structure, as plain data --------------------------------------- */

  var MEMBER_TONE = {
    ground: "ground", slab: "slab", bed: "bed", "bed-rim": "bedRim",
    column: "column", "base-plate": "beam", "column-head": "beam",
    "primary-beam": "beam", "eave-beam": "beam", rail: "rail",
    "zone-divider": "divider", clamp: "clamp"
  };

  /* Every member of the shade house, with no WebGL in sight, so that what carries
     what can be read and checked rather than taken on trust. The order is the order a
     house goes up: ground, beds, columns, primary beams, eave beams, secondary rails,
     zone outlines, then the clamps that hold each module to the two rails bounding its
     bay. Nothing is placed that is not carried by something below it. */
  function planStructure(zoneCount) {
    var members = [], bays = [], beds = [];
    var columns = Math.max(1, zoneCount) * BAY_COLUMNS_PER_ZONE;
    var width = columns * CELL;
    var depth = BAY_ROWS * CELL;
    var left = -width / 2;
    var overhang = 0.16;

    function put(kind, x, y, z, w, d, h) {
      members.push({ kind: kind, x: x, y: y, z: z, width: w, depth: d, height: h });
    }

    put("ground", 0, 0, -0.06, width + 1.5, depth + 1.5, 0.12);
    put("slab", 0, 0, 0.015, width + 0.9, depth + 0.9, 0.03);

    for (var zoneIndex = 0; zoneIndex < zoneCount; zoneIndex++) {
      var start = left + zoneIndex * BAY_COLUMNS_PER_ZONE * CELL;
      var centre = start + BAY_COLUMNS_PER_ZONE * CELL / 2;
      var bedWidth = BAY_COLUMNS_PER_ZONE * CELL - PATH;
      var bedDepth = depth - PATH - 0.10;
      put("bed", centre, 0, BED_Z / 2 + 0.03, bedWidth, bedDepth, BED_Z);
      put("bed-rim", centre, 0, BED_Z + 0.025, bedWidth + 0.05, bedDepth + 0.05, 0.05);
      beds.push({ x: centre, width: bedWidth, depth: bedDepth });
    }

    var columnLines = [];
    for (var line = 0; line <= zoneCount; line++) {
      columnLines.push(left + line * BAY_COLUMNS_PER_ZONE * CELL);
    }
    var rowLines = [-depth / 2, 0, depth / 2];

    columnLines.forEach(function (x) {
      rowLines.forEach(function (y) {
        put("column", x, y, COLUMN_TOP / 2, 0.11, 0.11, COLUMN_TOP);
        put("base-plate", x, y, 0.06, 0.24, 0.24, 0.12);
        put("column-head", x, y, COLUMN_TOP - 0.16, 0.20, 0.20, 0.06);
      });
      put("primary-beam", x, 0, BEAM_Z, 0.13, depth + overhang * 2, 0.16);
    });
    rowLines.forEach(function (y) {
      put("primary-beam", 0, y, BEAM_Z, width + overhang * 2, 0.13, 0.16);
    });

    /* The perimeter tie runs on the outer column lines, not outside them, so each
       eave beam is carried by the column heads it joins rather than cantilevered off
       nothing. */
    [-depth / 2, depth / 2].forEach(function (y) {
      put("eave-beam", 0, y, COLUMN_TOP - 0.05, width + overhang * 2, 0.10, 0.12);
    });
    [left, left + width].forEach(function (x) {
      put("eave-beam", x, 0, COLUMN_TOP - 0.05, 0.10, depth + overhang * 2, 0.12);
    });

    /* Secondary rails. Every module clamps to the two that bound its bay, and the one
       running between bay columns is wide enough to close the gap between two modules
       in plan, so a shut roof sheds the whole bay. */
    for (var row = 0; row <= BAY_ROWS; row++) {
      put("rail", 0, -depth / 2 + row * CELL, RAIL_Z, width + overhang, RAIL_HALF_Y * 2, 0.09);
    }
    for (var column = 0; column <= columns; column++) {
      put("rail", left + column * CELL, 0, RAIL_Z - 0.012, RAIL_HALF_X * 2,
          depth + overhang, 0.065);
    }

    for (var boundary = 0; boundary <= zoneCount; boundary++) {
      put("zone-divider", left + boundary * BAY_COLUMNS_PER_ZONE * CELL, 0, RAIL_Z + 0.045,
          0.075, depth + overhang, 0.10);
    }
    [-depth / 2, depth / 2].forEach(function (edge) {
      put("zone-divider", 0, edge, RAIL_Z + 0.045, width + overhang, 0.075, 0.10);
    });

    for (var index = 0; index < zoneCount; index++) {
      for (var bayColumn = 0; bayColumn < BAY_COLUMNS_PER_ZONE; bayColumn++) {
        for (var bayRow = 0; bayRow < BAY_ROWS; bayRow++) {
          var bx = left + (index * BAY_COLUMNS_PER_ZONE + bayColumn + 0.5) * CELL;
          var by = -depth / 2 + (bayRow + 0.5) * CELL;
          bays.push({ zone: LETTERS[index] || String(index + 1), x: bx, y: by });
          [-1, 1].forEach(function (end) {
            put("clamp", bx, by + end * (Fin.PARAMS.span / 2 + 0.018), ROOF_Z - 0.028,
                0.085, 0.055, 0.075);
          });
        }
      }
    }

    return {
      members: members, bays: bays, beds: beds,
      columns: columns, width: width, depth: depth, left: left,
      levels: { BED_Z: BED_Z, COLUMN_TOP: COLUMN_TOP, BEAM_Z: BEAM_Z,
                RAIL_Z: RAIL_Z, ROOF_Z: ROOF_Z },
      cell: CELL, bayRows: BAY_ROWS, bayColumnsPerZone: BAY_COLUMNS_PER_ZONE,
      railHalfX: RAIL_HALF_X, railHalfY: RAIL_HALF_Y
    };
  }

  /* --- the scene ---------------------------------------------------------- */

  function create(options) {
    var host = options.host;
    var onZonePick = options.onZonePick || function () {};
    var onFrame = options.onFrame || function () {};

    var gl = null, program = null, uniform = {}, attribute = {}, canvas = null;
    var buffers = {}, structure = [], plants = [], bays = [], zones = [];
    var topology = Fin.moduleTopology();
    var spine = Fin.backboneTopology();
    var lamellaPositions = new Float32Array(topology.vertexCount * 3);
    var spinePositions = new Float32Array(spine.vertexCount * 3);
    var motion = {}, mode = "operate", overlay = false, selected = null;
    var rainRate = 0, rainSeeds = [], rainData = null, rainCount = 0;
    var inspectZone = null, explode = 0, explodeTarget = 0;
    var raf = null, lastMatrix = null, viewSize = [1, 1];
    var reduceMotion = root.matchMedia
      ? root.matchMedia("(prefers-reduced-motion: reduce)")
      : { matches: false };

    var LIGHT = unit([-0.46, -0.30, 0.83]);
    var camera = {
      azimuth: -Math.PI / 2 - 0.34, polar: 0.62, distance: 9.4,
      target: [0, 0, 0.95], pan: [0, 0]
    };

    /* narrowFit reads the canvas rectangle, which is zero until the first sized draw,
       so the chosen preset is applied again as soon as the frame has a real shape. */
    var lastPreset = "overview", framed = false;

    var PRESETS = {
      overview: { azimuth: -Math.PI / 2 - 0.34, polar: 0.64, distance: 8.3, target: [0, 0, 1.00] },
      plan:     { azimuth: -Math.PI / 2, polar: 0.06, distance: 8.6, target: [0, 0, 1.4] },
      eave:     { azimuth: -Math.PI / 2 - 0.10, polar: 1.16, distance: 8.0, target: [0, 0, 1.05] },
      bay:      { azimuth: -Math.PI / 2 - 0.52, polar: 0.80, distance: 3.6, target: [0, 0, 1.70] }
    };

    /* ----------------------------------------------------- layout */

    function houseWidth(count) { return count * BAY_COLUMNS_PER_ZONE * CELL; }

    function bayColumnCount() { return zones.length * BAY_COLUMNS_PER_ZONE; }

    function leftEdge() { return -houseWidth(zones.length) / 2; }

    function roofDepth() { return BAY_ROWS * CELL; }

    function zoneCentreX(index) {
      return leftEdge() + (index + 0.5) * BAY_COLUMNS_PER_ZONE * CELL;
    }

    function zoneSpanX(index) {
      var start = leftEdge() + index * BAY_COLUMNS_PER_ZONE * CELL;
      return [start, start + BAY_COLUMNS_PER_ZONE * CELL];
    }

    function addBox(list, x, y, z, width, depth, height, colour, kind) {
      list.push({ mesh: "box", model: boxModel(x, y, z, width, depth, height),
                  colour: colour, kind: kind || "structure" });
    }

    function buildStructure() {
      var plan = planStructure(zones.length);
      structure = plan.members.map(function (member) {
        return {
          mesh: "box",
          kind: member.kind,
          model: boxModel(member.x, member.y, member.z,
                          member.width, member.depth, member.height),
          colour: TONE[MEMBER_TONE[member.kind]] || TONE.beam
        };
      });
      bays = plan.bays.map(function (bay) {
        return { zone: bay.zone, x: bay.x, y: bay.y, model: translation(bay.x, bay.y, ROOF_Z) };
      });
      plants = [];
      plan.beds.forEach(function (bed, index) {
        addPlants(index, bed.x, bed.width, bed.depth);
      });
    }

    function addPlants(zoneIndex, centreX, bedWidth, bedDepth) {
      var random = seededRandom((0xF1EC70 ^ Math.imul(zoneIndex + 1, 0x9E3779B9)) >>> 0);
      var rows = 4, perRow = 7;
      for (var row = 0; row < rows; row++) {
        for (var index = 0; index < perRow; index++) {
          var jitterX = (random() - 0.5) * 0.09;
          var jitterY = (random() - 0.5) * 0.09;
          var x = centreX + (index / (perRow - 1) - 0.5) * (bedWidth - 0.34) + jitterX;
          var y = (row / (rows - 1) - 0.5) * (bedDepth - 0.34) + jitterY;
          var height = 0.17 + random() * 0.11;
          var size = 0.17 + random() * 0.07;
          var angle = random() * Math.PI;
          plants.push({ mesh: "box", colour: TONE.stem,
                        model: boxModel(x, y, BED_Z + height / 2, 0.028, 0.028, height) });
          for (var blade = 0; blade < 3; blade++) {
            var turn = angle + blade * 2.09;
            plants.push({
              mesh: "leaf",
              colour: blade % 2 ? TONE.leafLight : TONE.leaf,
              model: multiply(
                translation(x, y, BED_Z + height * (0.72 + blade * 0.12)),
                multiply(rotationZ(turn), scaling(size, size, size * 0.8)))
            });
          }
        }
      }
    }

    function rotationZ(angle) {
      var m = identity(), c = Math.cos(angle), s = Math.sin(angle);
      m[0] = c; m[1] = s; m[4] = -s; m[5] = c;
      return m;
    }

    /* ----------------------------------------------------- rain */

    /* Deterministic drop seeds, rebuilt only when the house changes size. */
    function seedRain() {
      var random = seededRandom(0x5A1D07);
      rainSeeds = [];
      for (var index = 0; index < RAIN.MAX_DROPS; index++) {
        rainSeeds.push({ x: random(), y: random(), phase: random(), length: 0.7 + random() * 0.6 });
      }
      rainData = new Float32Array(RAIN.MAX_DROPS * 6);
    }

    /* Does a drop falling at (x, y) get past the roof? The lamella reach comes from
       flectofin.js, so this answer and the reported opening cannot disagree. */
    function passesRoof(x, y) {
      var columns = bayColumnCount(), depth = roofDepth(), left = leftEdge();
      var across = (x - left) / CELL, along = (y + depth / 2) / CELL;
      if (across < 0 || across > columns || along < 0 || along > BAY_ROWS) { return true; }

      var column = Math.min(columns - 1, Math.floor(across));
      var row = Math.min(BAY_ROWS - 1, Math.floor(along));
      var bx = left + (column + 0.5) * CELL;
      var by = -depth / 2 + (row + 0.5) * CELL;

      if (Math.abs(x - bx) >= CELL / 2 - RAIL_HALF_X) { return false; }   /* on a rail */
      if (Math.abs(y - by) >= CELL / 2 - RAIL_HALF_Y) { return false; }   /* on a rail */

      var zone = zones[Math.floor(column / BAY_COLUMNS_PER_ZONE)];
      if (!zone) { return true; }
      var actuation = motion[zone.letter] ? motion[zone.letter].value : 0;
      var v = (y - by) / Fin.PARAMS.span + 0.5;
      if (v < 0 || v > 1) { return false; }                               /* over a clamp */
      var side = x >= bx ? 1 : -1;
      return Math.abs(x - bx) > Fin.planHalfWidth(side, v, actuation);
    }

    function writeRain(now) {
      rainCount = 0;
      if (rainRate <= 0 || !rainData || !zones.length) { return; }

      var columns = bayColumnCount();
      var width = columns * CELL, depth = roofDepth(), left = leftEdge();
      var spanX = width + 1.2, spanY = depth + 1.2;
      var heavy = Math.min(1, rainRate / RAIN.HEAVY_MM);
      var fall = RAIN.SLOW_FALL + (RAIN.FAST_FALL - RAIN.SLOW_FALL) * heavy;
      var streak = fall * RAIN.EXPOSURE;
      var top = ROOF_Z + RAIN.TOP;
      var height = top - BED_Z;
      var drops = Math.min(RAIN.MAX_DROPS, Math.round(rainRate * RAIN.DROPS_PER_MM));
      var seconds = reduceMotion.matches ? 0 : now / 1000;
      var cursor = 0;

      for (var index = 0; index < drops; index++) {
        var seed = rainSeeds[index];
        var phase = (seed.phase + seconds * fall / height) % 1;
        var z = top - phase * height;
        var x = left - 0.6 + seed.x * spanX;
        var y = -depth / 2 - 0.6 + seed.y * spanY;
        var length = streak * seed.length;
        var through = passesRoof(x, y);
        var bottom = z - length;

        if (!through && bottom < ROOF_Z) {
          if (z <= ROOF_Z) {
            /* the drop is on the shut roof: a brief tick where it landed */
            if (z > ROOF_Z - RAIN.SPLASH * 3) {
              cursor = pushSegment(cursor, x - RAIN.SPLASH, y, ROOF_Z + 0.012,
                                   x + RAIN.SPLASH, y, ROOF_Z + 0.012);
            }
            continue;
          }
          bottom = ROOF_Z;                                    /* stopped by the roof */
        }
        if (bottom < BED_Z) {
          if (z <= BED_Z + 0.01) {
            cursor = pushSegment(cursor, x - RAIN.SPLASH, y, BED_Z + 0.03,
                                 x + RAIN.SPLASH, y, BED_Z + 0.03);
            continue;
          }
          bottom = BED_Z;                                     /* reached the bed */
        }
        cursor = pushSegment(cursor, x, y, z, x - (z - bottom) * RAIN.SHEAR, y, bottom);
      }
      rainCount = cursor / 3;
    }

    function pushSegment(cursor, x1, y1, z1, x2, y2, z2) {
      rainData[cursor] = x1; rainData[cursor + 1] = y1; rainData[cursor + 2] = z1;
      rainData[cursor + 3] = x2; rainData[cursor + 4] = y2; rainData[cursor + 5] = z2;
      return cursor + 6;
    }

    function drawRain() {
      if (!rainCount) { return; }
      gl.bindBuffer(gl.ARRAY_BUFFER, buffers.rain.positions);
      gl.bufferSubData(gl.ARRAY_BUFFER, 0, rainData.subarray(0, rainCount * 3));
      setColour(TONE.rain, null, 0.82, true);
      gl.uniformMatrix4fv(uniform.uModel, false, identity());
      gl.depthMask(false);
      gl.bindVertexArray(buffers.rain.vao);
      gl.drawArrays(gl.LINES, 0, rainCount);
      gl.depthMask(true);
    }

    /* ----------------------------------------------------- gl plumbing */

    function compile(type, source) {
      var shader = gl.createShader(type);
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        throw new Error(gl.getShaderInfoLog(shader));
      }
      return shader;
    }

    function uploadStatic(name, mesh) {
      var vao = gl.createVertexArray();
      gl.bindVertexArray(vao);
      bindArray(mesh.positions, attribute.position, 3);
      bindArray(mesh.tints, attribute.tint, 1);
      var indexBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(mesh.indices), gl.STATIC_DRAW);
      gl.bindVertexArray(null);
      buffers[name] = { vao: vao, count: mesh.indices.length };
    }

    function bindArray(data, location, size) {
      var buffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);
      gl.enableVertexAttribArray(location);
      gl.vertexAttribPointer(location, size, gl.FLOAT, false, 0, 0);
      return buffer;
    }

    function uploadDynamic(name, vertexCount, tints, indices) {
      var vao = gl.createVertexArray();
      gl.bindVertexArray(vao);
      var positionBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, vertexCount * 3 * 4, gl.DYNAMIC_DRAW);
      gl.enableVertexAttribArray(attribute.position);
      gl.vertexAttribPointer(attribute.position, 3, gl.FLOAT, false, 0, 0);
      bindArray(tints, attribute.tint, 1);
      var indexBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(indices), gl.STATIC_DRAW);
      gl.bindVertexArray(null);
      buffers[name] = { vao: vao, count: indices.length, positions: positionBuffer };
    }

    /* A dynamic position-only buffer, drawn with gl.LINES. */
    function uploadPoints(name, vertexCount) {
      var vao = gl.createVertexArray();
      gl.bindVertexArray(vao);
      var positionBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, vertexCount * 3 * 4, gl.DYNAMIC_DRAW);
      gl.enableVertexAttribArray(attribute.position);
      gl.vertexAttribPointer(attribute.position, 3, gl.FLOAT, false, 0, 0);
      bindArray(new Array(vertexCount).fill(0), attribute.tint, 1);
      gl.bindVertexArray(null);
      buffers[name] = { vao: vao, positions: positionBuffer };
    }

    function writeDynamic(name, data) {
      gl.bindBuffer(gl.ARRAY_BUFFER, buffers[name].positions);
      gl.bufferSubData(gl.ARRAY_BUFFER, 0, data);
    }

    function mount() {
      canvas = document.createElement("canvas");
      canvas.className = "stage-canvas";
      canvas.setAttribute("tabindex", "0");
      canvas.setAttribute("role", "application");
      canvas.setAttribute("aria-label",
        "Modelled shade house. Drag to orbit, shift-drag to pan, scroll to zoom, " +
        "arrow keys to turn, number keys to select a zone.");
      host.appendChild(canvas);

      gl = canvas.getContext("webgl2", { antialias: true, alpha: true });
      if (!gl) { return false; }

      program = gl.createProgram();
      gl.attachShader(program, compile(gl.VERTEX_SHADER, VERT));
      gl.attachShader(program, compile(gl.FRAGMENT_SHADER, FRAG));
      gl.linkProgram(program);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        throw new Error(gl.getProgramInfoLog(program));
      }
      gl.useProgram(program);

      attribute.position = gl.getAttribLocation(program, "aPos");
      attribute.tint = gl.getAttribLocation(program, "aTint");
      ["uProj", "uView", "uModel", "uColor", "uTintColor", "uLight", "uAlpha", "uFlat"]
        .forEach(function (name) { uniform[name] = gl.getUniformLocation(program, name); });

      uploadStatic("box", boxMesh());
      uploadStatic("leaf", leafMesh());
      uploadDynamic("lamellae", topology.vertexCount, topology.tints, topology.indices);
      uploadDynamic("spine", spine.vertexCount,
                    new Array(spine.vertexCount).fill(0), spine.indices);
      uploadPoints("rain", RAIN.MAX_DROPS * 2);
      seedRain();

      gl.enable(gl.DEPTH_TEST);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
      bindInput();
      root.addEventListener("resize", request);
      return true;
    }

    /* ----------------------------------------------------- camera input */

    function clamp(value, low, high) { return Math.max(low, Math.min(high, value)); }

    function eyePoint() {
      var sinPolar = Math.sin(camera.polar);
      var right = [Math.sin(camera.azimuth), -Math.cos(camera.azimuth), 0];
      var target = [
        camera.target[0] + right[0] * camera.pan[0],
        camera.target[1] + right[1] * camera.pan[0],
        camera.target[2] + camera.pan[1]
      ];
      return {
        eye: [
          target[0] + camera.distance * sinPolar * Math.cos(camera.azimuth),
          target[1] + camera.distance * sinPolar * Math.sin(camera.azimuth),
          target[2] + camera.distance * Math.cos(camera.polar)
        ],
        target: target
      };
    }

    function bindInput() {
      var dragging = false, panning = false, lastX = 0, lastY = 0;

      canvas.addEventListener("pointerdown", function (event) {
        dragging = true;
        panning = event.shiftKey || event.button === 1;
        lastX = event.clientX; lastY = event.clientY;
        canvas.setPointerCapture(event.pointerId);
        host.classList.add("is-dragging");
      });

      canvas.addEventListener("pointermove", function (event) {
        if (!dragging) { return; }
        var dx = event.clientX - lastX, dy = event.clientY - lastY;
        if (panning) {
          camera.pan[0] -= dx * camera.distance * 0.00042;
          camera.pan[1] += dy * camera.distance * 0.00042;
        } else {
          camera.azimuth -= dx * 0.0068;
          camera.polar = clamp(camera.polar + dy * 0.0050, 0.05, 1.34);
        }
        lastX = event.clientX; lastY = event.clientY;
        request();
      });

      function endDrag(event) {
        if (dragging && !panning && event && Math.abs(event.movementX || 0) < 2) { pick(event); }
        dragging = false; panning = false;
        host.classList.remove("is-dragging");
        if (event && event.pointerId !== undefined && canvas.hasPointerCapture(event.pointerId)) {
          canvas.releasePointerCapture(event.pointerId);
        }
      }
      canvas.addEventListener("pointerup", endDrag);
      canvas.addEventListener("pointercancel", function () {
        dragging = false; panning = false;
        host.classList.remove("is-dragging");
      });

      canvas.addEventListener("wheel", function (event) {
        camera.distance = clamp(camera.distance * Math.exp(event.deltaY * 0.0011), 2.4, 19.0);
        request();
        event.preventDefault();
      }, { passive: false });

      canvas.addEventListener("keydown", function (event) {
        var step = event.shiftKey ? 0.22 : 0.08;
        var handled = true;
        switch (event.key) {
          case "ArrowLeft": camera.azimuth += step; break;
          case "ArrowRight": camera.azimuth -= step; break;
          case "ArrowUp": camera.polar = clamp(camera.polar - step * 0.7, 0.05, 1.34); break;
          case "ArrowDown": camera.polar = clamp(camera.polar + step * 0.7, 0.05, 1.34); break;
          case "+": case "=": camera.distance = clamp(camera.distance * 0.9, 2.4, 19.0); break;
          case "-": case "_": camera.distance = clamp(camera.distance * 1.1, 2.4, 19.0); break;
          case "0": case "Home": resetView(); break;
          case "1": case "2": case "3": case "4":
            var index = Number(event.key) - 1;
            if (zones[index]) { onZonePick(zones[index].letter); }
            break;
          default: handled = false;
        }
        if (handled) { request(); event.preventDefault(); }
      });
    }

    /* A click lands on the roof plane, and the roof plane says which zone it was. */
    function pick(event) {
      if (!lastMatrix) { return; }
      var rect = canvas.getBoundingClientRect();
      var ndcX = (event.clientX - rect.left) / rect.width * 2 - 1;
      var ndcY = 1 - (event.clientY - rect.top) / rect.height * 2;
      var view = eyePoint();
      var forward = unit(subtract(view.target, view.eye));
      var right = unit(cross(forward, [0, 0, 1]));
      var up = cross(right, forward);
      var aspect = rect.width / Math.max(1, rect.height);
      var tan = Math.tan(0.56 / 2);
      var ray = unit([
        forward[0] + right[0] * ndcX * tan * aspect + up[0] * ndcY * tan,
        forward[1] + right[1] * ndcX * tan * aspect + up[1] * ndcY * tan,
        forward[2] + right[2] * ndcX * tan * aspect + up[2] * ndcY * tan
      ]);
      if (Math.abs(ray[2]) < 1e-5) { return; }
      var t = (ROOF_Z - view.eye[2]) / ray[2];
      if (t <= 0) { return; }
      var hitX = view.eye[0] + ray[0] * t;
      var hitY = view.eye[1] + ray[1] * t;
      if (Math.abs(hitY) > roofDepth() / 2 + 0.2) { return; }
      for (var index = 0; index < zones.length; index++) {
        var span = zoneSpanX(index);
        if (hitX >= span[0] && hitX <= span[1]) {
          onZonePick(zones[index].letter);
          return;
        }
      }
    }

    /* ----------------------------------------------------- animation */

    function ease(t) { return t * t * (3 - 2 * t); }

    function sample(item, now) {
      var progress = clamp((now - item.startedAt) / MOVE_MS, 0, 1);
      return item.from + (item.target - item.from) * ease(progress);
    }

    function advance(now) {
      var moving = false;
      zones.forEach(function (zone) {
        var item = motion[zone.letter];
        if (!item) {
          item = motion[zone.letter] = { value: 0, from: 0, target: 0, startedAt: now };
        }
        if (zone.actuation !== item.target) {
          item.from = sample(item, now);
          item.target = zone.actuation;
          item.startedAt = reduceMotion.matches ? now - MOVE_MS : now;
        }
        item.value = sample(item, now);
        if (Math.abs(item.value - item.target) > 0.0015) { moving = true; }
        else { item.value = item.target; }
      });
      if (rainRate > 0 && !reduceMotion.matches) { moving = true; }
      if (Math.abs(explode - explodeTarget) > 0.002) {
        explode += (explodeTarget - explode) * (reduceMotion.matches ? 1 : 0.14);
        moving = true;
      } else { explode = explodeTarget; }
      return moving;
    }

    function request() {
      if (raf === null) { raf = requestAnimationFrame(tick); }
    }

    function tick(now) {
      raf = null;
      var moving = advance(now);
      writeRain(now);
      draw();
      if (moving) { raf = requestAnimationFrame(tick); }
    }

    /* ----------------------------------------------------- drawing */

    function setColour(colour, tintColour, alpha, flat) {
      gl.uniform3f(uniform.uColor, colour[0], colour[1], colour[2]);
      var tint = tintColour || colour;
      gl.uniform3f(uniform.uTintColor, tint[0], tint[1], tint[2]);
      gl.uniform1f(uniform.uAlpha, alpha === undefined ? 1 : alpha);
      gl.uniform1f(uniform.uFlat, flat ? 1 : 0);
    }

    function drawMesh(name, model) {
      var mesh = buffers[name];
      gl.uniformMatrix4fv(uniform.uModel, false, model);
      gl.bindVertexArray(mesh.vao);
      gl.drawElements(gl.TRIANGLES, mesh.count, gl.UNSIGNED_SHORT, 0);
    }

    function membraneColour(zone) {
      if (zone.conflict) { return MEMBRANE.conflict; }
      if (zone.manual) { return MEMBRANE.manual; }
      if (zone.offline || zone.stale) { return MEMBRANE.idle; }
      if (zone.admittingRain) { return MEMBRANE.rain; }
      return MEMBRANE.normal;
    }

    function zoneOf(letter) {
      for (var index = 0; index < zones.length; index++) {
        if (zones[index].letter === letter) { return zones[index]; }
      }
      return null;
    }

    function visibleBays() {
      if (mode === "operate") { return bays; }
      var zone = inspectZone || (zones[0] && zones[0].letter);
      var candidates = bays.filter(function (bay) { return bay.zone === zone; });
      return candidates.length ? [candidates[Math.floor(candidates.length / 2)]] : [];
    }

    function explodedOffset(part) {
      var reach = explode;
      if (part === "left") { return [0.26 * reach, 0, 0.10 * reach]; }
      if (part === "right") { return [-0.26 * reach, 0, 0.10 * reach]; }
      if (part === "spine") { return [0, 0, 0.30 * reach]; }
      return [0, 0, 0];
    }

    function draw() {
      if (!gl) { return; }
      var dpr = Math.min(root.devicePixelRatio || 1, 2);
      var width = Math.max(1, Math.round(canvas.clientWidth * dpr));
      var height = Math.max(1, Math.round(canvas.clientHeight * dpr));
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width; canvas.height = height;
      }
      viewSize = [canvas.clientWidth, canvas.clientHeight];
      if (!framed && canvas.clientHeight > 1) {
        framed = true;
        applyPreset(lastPreset);
      }
      gl.viewport(0, 0, width, height);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

      var view = eyePoint();
      var projection = perspective(0.56, width / height, 0.08, 60);
      var viewMatrix = lookAt(view.eye, view.target, [0, 0, 1]);
      lastMatrix = multiply(projection, viewMatrix);

      gl.useProgram(program);
      gl.uniformMatrix4fv(uniform.uProj, false, projection);
      gl.uniformMatrix4fv(uniform.uView, false, viewMatrix);
      gl.uniform3f(uniform.uLight, LIGHT[0], LIGHT[1], LIGHT[2]);

      var inspecting = mode !== "operate";
      var shadow = shadowMatrix(LIGHT, BED_Z + 0.06);

      if (!inspecting) {
        structure.forEach(function (item) {
          setColour(item.colour, null, 1, false);
          drawMesh(item.mesh, item.model);
        });
        plants.forEach(function (item) {
          setColour(item.colour, TONE.leafLight, 1, false);
          drawMesh(item.mesh, item.model);
        });
      } else {
        drawInspectionRails();
      }

      /* contact shadows, flattened onto the bed plane, drawn without depth writes */
      if (!inspecting) {
        gl.depthMask(false);
        setColour(TONE.shadow, null, 0.30, true);
        structure.forEach(function (item) {
          if (item.model[14] > BED_Z) { drawMesh(item.mesh, multiply(shadow, item.model)); }
        });
        gl.depthMask(true);
      }

      var list = visibleBays();
      var drawnByZone = {};
      zones.forEach(function (zone) {
        var actuation = motion[zone.letter] ? motion[zone.letter].value : 0;
        var zoneBays = list.filter(function (bay) { return bay.zone === zone.letter; });
        if (!zoneBays.length) { return; }
        drawnByZone[zone.letter] = actuation;

        Fin.writeLamellae(actuation, lamellaPositions);
        writeDynamic("lamellae", lamellaPositions);
        Fin.writeBackbone(actuation, spinePositions);
        writeDynamic("spine", spinePositions);

        var colour = membraneColour(zone);
        var dim = selected && selected !== zone.letter && !inspecting;
        var alpha = dim ? 0.62 : 1;
        var left = explodedOffset("left"), right = explodedOffset("right");
        var spineShift = explodedOffset("spine");

        zoneBays.forEach(function (bay) {
          if (!inspecting) {
            gl.depthMask(false);
            setColour(TONE.shadow, null, 0.26, true);
            drawLamella("left", multiply(shadow, bay.model));
            drawLamella("right", multiply(shadow, bay.model));
            gl.depthMask(true);
          }
          setColour(colour, mixToward(colour, TONE.root, 0.55), alpha, false);
          drawLamella("left", shift(bay.model, left));
          drawLamella("right", shift(bay.model, right));
          setColour(TONE.backbone, TONE.root, alpha, false);
          drawMesh("spine", shift(bay.model, spineShift));
        });
      });

      if (!inspecting) { drawRain(); }
      gl.bindVertexArray(null);
      onFrame({
        matrix: lastMatrix,
        size: viewSize,
        actuation: drawnByZone,
        roofZ: ROOF_Z,
        zoneCentre: zoneAnchors(),
        mode: mode,
        overlay: overlay
      });
    }

    /* The two lamellae are one mesh in two index ranges, so each can be drawn with its
       own model matrix. That is what lets the exploded view part them without
       rebuilding anything, and what lets the overlay name one of them. */
    function drawLamella(side, model) {
      var mesh = buffers.lamellae;
      var half = mesh.count / 2;
      gl.uniformMatrix4fv(uniform.uModel, false, model);
      gl.bindVertexArray(mesh.vao);
      gl.drawElements(gl.TRIANGLES, half, gl.UNSIGNED_SHORT,
                      side === "left" ? 0 : half * 2);
    }

    function shift(model, offset) {
      if (!offset || (!offset[0] && !offset[1] && !offset[2])) { return model; }
      return multiply(model, translation(offset[0], offset[1], offset[2]));
    }

    function mixToward(colour, other, amount) {
      return [
        colour[0] + (other[0] - colour[0]) * amount,
        colour[1] + (other[1] - colour[1]) * amount,
        colour[2] + (other[2] - colour[2]) * amount
      ];
    }

    function drawInspectionRails() {
      var bay = visibleBays()[0];
      if (!bay) { return; }
      var half = Fin.PARAMS.span / 2 + 0.018;
      setColour(TONE.rail, null, 1, false);
      [-1, 1].forEach(function (end) {
        drawMesh("box", boxModel(bay.x, bay.y + end * half, ROOF_Z - 0.075, 1.5, 0.07, 0.09));
      });
      setColour(TONE.clamp, null, 1, false);
      [-1, 1].forEach(function (end) {
        drawMesh("box", boxModel(bay.x, bay.y + end * half,
                                 ROOF_Z - 0.028 + explodedOffset("spine")[2] * 0.4,
                                 0.085, 0.055, 0.075));
      });
    }

    function zoneAnchors() {
      var out = {};
      zones.forEach(function (zone, index) {
        out[zone.letter] = [zoneCentreX(index), 0, ROOF_Z + 0.34];
      });
      return out;
    }

    /* ----------------------------------------------------- public surface */

    function resetView() {
      applyPreset("overview");
    }

    /* Presets are written for a three zone roof, so they widen with the house. */
    function spread() {
      return Math.max(1, zones.length || 3) / 3;
    }

    /* The presets were framed for a frame about one and a half times as wide as it is
       tall. In a narrower frame the camera steps back, so the whole roof stays in view
       and no zone is cut off at the sides. */
    function narrowFit(name) {
      if (name === "bay" || !canvas) { return 1; }
      var rect = canvas.getBoundingClientRect();
      if (!rect.width || !rect.height) { return 1; }
      return clamp(1.5 / (rect.width / rect.height), 1, 1.7);
    }

    function applyPreset(name) {
      var preset = PRESETS[name] || PRESETS.overview;
      var wide = name === "bay" ? 1 : spread();
      lastPreset = name;
      camera.azimuth = preset.azimuth;
      camera.polar = preset.polar;
      camera.distance = clamp(preset.distance * wide * narrowFit(name), 2.4, 17.0);
      camera.target = preset.target.slice();
      camera.pan = [0, 0];
      request();
    }

    function centreOnZone(letter) {
      var index = zones.findIndex(function (zone) { return zone.letter === letter; });
      if (index < 0) { return; }
      camera.pan[0] = 0;
      camera.target = [zoneCentreX(index), 0, 1.25];
      camera.distance = Math.min(camera.distance, 6.6);
      request();
    }

    return {
      mount: mount,
      isReady: function () { return !!gl; },
      canvas: function () { return canvas; },
      setZones: function (next) {
        var before = zones.length;
        var changed = next.length !== before ||
          next.some(function (zone, index) { return !zones[index] || zones[index].letter !== zone.letter; });
        zones = next.map(function (zone) { return Object.assign({}, zone); });
        if (!changed) { request(); return; }
        buildStructure();
        seedRain();
        /* The roof just changed width, so pull the camera back in proportion rather
           than leaving half the house outside the frame. */
        if (before && next.length !== before) {
          camera.distance = clamp(camera.distance * (next.length / before), 2.4, 19.0);
        } else if (!before) {
          applyPreset("overview");
        }
        request();
      },
      updateZones: function (next) {
        next.forEach(function (zone) {
          var existing = zoneOf(zone.letter);
          if (existing) { Object.assign(existing, zone); }
        });
        request();
      },
      setSelected: function (letter) { selected = letter; request(); },
      /* The module the technical overlay annotates: the isolated one when inspecting,
         otherwise the middle bay of the zone in hand. */
      focusBay: function (letter) {
        var wanted = mode === "operate" ? (letter || selected || (zones[0] && zones[0].letter))
                                        : (inspectZone || (zones[0] && zones[0].letter));
        var candidates = bays.filter(function (bay) { return bay.zone === wanted; });
        if (!candidates.length) { return null; }
        var bay = candidates[Math.floor(candidates.length / 2)];
        return {
          zone: bay.zone,
          origin: [bay.x, bay.y, ROOF_Z],
          actuation: motion[bay.zone] ? motion[bay.zone].value : 0
        };
      },
      focusZone: centreOnZone,
      setMode: function (next, letter) {
        mode = next;
        inspectZone = letter || inspectZone;
        explodeTarget = next === "exploded" ? 1 : 0;
        if (next === "operate") { applyPreset("overview"); }
        else { applyPreset("bay"); centreOnBay(); }
        request();
      },
      mode: function () { return mode; },
      setOverlay: function (value) { overlay = value; request(); },
      /* The hour's modelled rain, in millimetres. Nothing else drives the rain. */
      setRain: function (millimetres) {
        rainRate = Math.max(0, millimetres || 0);
        if (!rainRate) { rainCount = 0; }
        request();
      },
      rainRate: function () { return rainRate; },
      overlayOn: function () { return overlay; },
      resetView: resetView,
      preset: applyPreset,
      request: request,
      project: function (point) {
        if (!lastMatrix) { return null; }
        var clip = project(lastMatrix, point);
        if (clip[3] <= 0) { return null; }
        return [
          (clip[0] / clip[3] * 0.5 + 0.5) * viewSize[0],
          (-clip[1] / clip[3] * 0.5 + 0.5) * viewSize[1]
        ];
      },
      geometry: {
        CELL: CELL, ROOF_Z: ROOF_Z, RAIL_Z: RAIL_Z, BEAM_Z: BEAM_Z,
        COLUMN_TOP: COLUMN_TOP, BAY_ROWS: BAY_ROWS,
        BAY_COLUMNS_PER_ZONE: BAY_COLUMNS_PER_ZONE
      }
    };

    function centreOnBay() {
      var bay = visibleBays()[0];
      if (!bay) { return; }
      camera.target = [bay.x, bay.y, ROOF_Z + 0.06];
      camera.distance = 2.7;
      camera.pan = [0, 0];
    }
  }

  root.ShadeHouse = { create: create, planStructure: planStructure, tone: tone,
                      PALETTE: PALETTE, TONE: TONE, MEMBRANE: MEMBRANE,
                      MEMBER_TONE: MEMBER_TONE };
  if (typeof module === "object" && module.exports) { module.exports = root.ShadeHouse; }
}(typeof self !== "undefined" ? self : this));
