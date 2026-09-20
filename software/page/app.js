/* Grower's console.
   Reads day.json, replays the day, and re-runs the zone rules whenever the grower
   changes the sky or takes a zone off rain. Nothing here fetches the network beyond
   the one relative file beside it. */

(function () {
  "use strict";

  var D = null, C = null;
  var hour = 0, cloud = 0, playing = false, timer = null;
  var overrides = {};
  var sim = {};
  var ROOF_ZONES = ["A", "B", "C", "D"];
  var MANUAL_RAIN_DEFAULT = true;

  var $ = function (id) { return document.getElementById(id); };

  /* ---------- the rules, the same nine, run client side ---------- */

  function et0(ghi, t2m) {
    var slope = 4098 * (0.6108 * Math.exp(17.27 * t2m / (t2m + 237.3))) / Math.pow(t2m + 237.3, 2);
    return C.MAKKINK_C * slope / (slope + C.GAMMA) * (ghi * 3600 / 1e6) / C.LATENT_HEAT;
  }

  function lightFor(ghi, open) {
    return ghi * C.K * 3600 / 1e6 * C.T_STRUCT * (open + (1 - open) * C.T_CLOSED);
  }

  function sky(i) {
    var h = D.hours[i];
    return { ghi: h.ghi * (1 - cloud / 100), rain: h.rain_mm, t2m: h.t2m };
  }

  function decide(z, i, lightSoFar, wantRain) {
    var s = sky(i);
    var rainOk = overrides[z.zone];

    if (s.ghi <= 0) return { open: 0, state: "NIGHT", reason: "" };

    if (s.rain > 0) {
      if (!rainOk) return { open: 0, state: "RAIN_SHUT", reason: "opted_out" };
      if (!wantRain) return { open: 0, state: "RAIN_SHUT", reason: "wet_enough" };
      var later = i + C.DRYING_HOURS;
      if (later >= D.hours.length || sky(later).ghi <= 0)
        return { open: 0, state: "RAIN_SHUT", reason: "no_drying_time" };
      if (s.rain >= C.HARD_RAIN_MM) return { open: 0, state: "RAIN_SHUT", reason: "hard_rain" };
      return { open: 1, state: "RAIN_OPEN", reason: "" };
    }

    if (z.light_rule === "dli") {
      if (lightSoFar < z.light_target) return { open: 1, state: "LIGHT_OPEN", reason: "" };
      return { open: 0, state: "SHADE", reason: "" };
    }

    if (s.t2m >= C.HEAT_SHADE_C) return { open: C.HEAT_SHADE_OPEN, state: "HEAT_SHADE", reason: "" };
    return { open: 1, state: "LIGHT_OPEN", reason: "" };
  }

  function runZone(z) {
    var soil = z.soil_start, light = 0, out = [];
    var wantRain = soil < C.SOIL_DRY_BELOW;

    for (var i = 0; i < D.hours.length; i++) {
      if (soil < C.SOIL_DRY_BELOW) wantRain = true;
      else if (soil >= C.SOIL_FULL_AT) wantRain = false;

      var d = decide(z, i, light, wantRain);
      var s = sky(i);
      light += lightFor(s.ghi, d.open);

      var before = soil;
      soil = Math.min(C.SOIL_CAPACITY, soil + s.rain * d.open);
      var rainIn = soil - before;
      soil = Math.max(0, soil - z.kc * et0(s.ghi, s.t2m) * d.open * C.T_STRUCT);

      var irr = 0;
      if (soil < C.SOIL_IRRIGATE_BELOW) { irr = C.SOIL_FULL_AT - soil; soil = C.SOIL_FULL_AT; }

      out.push({ open: d.open, state: d.state, reason: d.reason,
                 light: light, soil: soil, rainIn: rainIn, irrigation: irr });
    }
    return out;
  }

  function runAll() {
    D.zones.forEach(function (z) { sim[z.zone] = runZone(z); });
  }

  /* ---------- words ---------- */

  var STATE = {
    NIGHT:      { text: "Night",              cls: "night" },
    LIGHT_OPEN: { text: "Open for light",     cls: "open"  },
    SHADE:      { text: "Shaded, target met", cls: "shut"  },
    HEAT_SHADE: { text: "Shaded, heat",       cls: "heat"  },
    RAIN_OPEN:  { text: "Open for rain",      cls: "rain"  },
    RAIN_SHUT:  { text: "Shut against rain",  cls: "shut"  }
  };
  var REASON = {
    opted_out: "this crop opts out of rain",
    wet_enough: "its soil is wet enough",
    no_drying_time: "no drying time left today",
    hard_rain: "the rain is too hard"
  };

  function isTouched() {
    if (overrides.D !== MANUAL_RAIN_DEFAULT) return true;
    return D.zones.some(function (z) { return overrides[z.zone] !== !!z.rain_ok; });
  }

  /* ---------- the roof, the team's CAD, drawn in WebGL with no library ----------

     model.json carries three tessellated meshes and 23 instances: one base plate and
     22 flaps in 11 rows, banded across four roof regions here. Every flap is hinged at its own
     local origin and runs 50 mm along local -Y, so a flap opens by rotating about its
     local X axis. Shading is flat, taken from screen-space derivatives, so the file
     needs no normals. */

  var MODEL = null, gl = null, prog = null, loc = {}, gpu = [], canvas = null;
  var MAX_FLAP_DEG = 72;
  var watering = document.body.dataset.mode === "watering";
  var waterLayout = null, waterState = {open: [], selected: [], delivered: [], raining: false};
  var overlayVAO = null, overlayBuffer = null;
  var camera = { azimuth: watering ? -.2 : Math.PI, polar: watering ? 1.05 : 0.18, distance: 4.4 };
  var rainCanvas = null, rainCtx = null, rainRaf = null, rainIntensity = 0;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  // Flaps ease toward the hour's open fraction rather than snapping to it. The day
  // plays 24 hours in 38 seconds, so an untweened roof reads as broken rather than fast.
  var shown = {}, raf = null;

  var VERT = [
    "#version 300 es",
    "in vec3 aPos;",
    "uniform mat4 uProj; uniform mat4 uView; uniform mat4 uModel;",
    "out vec3 vWorld;",
    "void main() {",
    "  vec4 w = uModel * vec4(aPos, 1.0);",
    "  vWorld = w.xyz;",
    "  gl_Position = uProj * uView * w;",
    "}"
  ].join("\n");

  var FRAG = [
    "#version 300 es",
    "precision highp float;",
    "in vec3 vWorld;",
    "uniform vec3 uColor; uniform vec3 uLight; uniform bool uFlat;",
    "out vec4 frag;",
    "void main() {",
    "  if (uFlat) { frag = vec4(uColor, 1.0); return; }",
    "  vec3 n = normalize(cross(dFdx(vWorld), dFdy(vWorld)));",
    "  float key = max(dot(n, normalize(uLight)), 0.0);",
    "  float rim = max(dot(n, normalize(vec3(-0.4, 0.3, 0.6))), 0.0);",
    "  vec3 c = uColor * (0.42 + 0.62 * key + 0.10 * rim);",
    "  frag = vec4(pow(c, vec3(0.4545)), 1.0);",
    "}"
  ].join("\n");

  function mat4() {
    return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
  }

  function multiply(a, b) {
    var out = new Float32Array(16);
    for (var c = 0; c < 4; c++) {
      for (var r = 0; r < 4; r++) {
        out[c * 4 + r] = a[r] * b[c * 4] + a[4 + r] * b[c * 4 + 1] +
                         a[8 + r] * b[c * 4 + 2] + a[12 + r] * b[c * 4 + 3];
      }
    }
    return out;
  }

  function translation(x, y, z) {
    var m = mat4(); m[12] = x; m[13] = y; m[14] = z; return m;
  }

  function rotationX(rad) {
    var m = mat4(), c = Math.cos(rad), s = Math.sin(rad);
    m[5] = c; m[6] = s; m[9] = -s; m[10] = c;
    return m;
  }

  function perspective(fovy, aspect, near, far) {
    var f = 1 / Math.tan(fovy / 2), m = new Float32Array(16);
    m[0] = f / aspect; m[5] = f; m[11] = -1;
    m[10] = (far + near) / (near - far);
    m[14] = (2 * far * near) / (near - far);
    return m;
  }

  function lookAt(eye, at, up) {
    var z = norm(sub(eye, at)), x = norm(cross(up, z)), y = cross(z, x);
    return new Float32Array([
      x[0], y[0], z[0], 0,
      x[1], y[1], z[1], 0,
      x[2], y[2], z[2], 0,
      -dot(x, eye), -dot(y, eye), -dot(z, eye), 1
    ]);
  }

  function sub(a, b) { return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]; }
  function dot(a, b) { return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]; }
  function cross(a, b) {
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
  }
  function norm(v) {
    var l = Math.hypot(v[0], v[1], v[2]) || 1;
    return [v[0]/l, v[1]/l, v[2]/l];
  }

  function compile(type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      throw new Error(gl.getShaderInfoLog(sh));
    }
    return sh;
  }

  function prepareRoof() {
    var half = MODEL.extent[1] / 2 || 1, centre = MODEL.centre;
    var rows = MODEL.instances
      .filter(function (inst) { return inst.kind === "flap"; })
      .map(function (inst) { return inst.origin[1]; })
      .filter(function (value, index, list) { return list.indexOf(value) === index; })
      .sort(function (a, b) { return a - b; });
    MODEL.instances.forEach(function (inst) {
      inst.offset = [
        (inst.origin[0] - centre[0]) / half,
        (inst.origin[1] - centre[1]) / half,
        (inst.origin[2] - centre[2]) / half
      ];
      if (inst.kind === "flap") {
        var row = rows.indexOf(inst.origin[1]);
        inst.renderZone = row < 3 ? "A" : row < 6 ? "B" : row < 9 ? "C" : "D";
      }
    });
  }

  function buildRoof() {
    var host = $("roof");
    host.innerHTML = "";

    if (!MODEL) {
      host.innerHTML = '<p class="model-missing">The roof model is missing. ' +
        'Run python software/page/build_model.py, then reload.</p>';
      return;
    }

    prepareRoof();
    canvas = document.createElement("canvas");
    canvas.className = "roof-canvas";
    canvas.setAttribute("role", "img");
    canvas.setAttribute("tabindex", "0");
    canvas.setAttribute("aria-label",
      watering ? "Team CAD with independently commanded flaps and simulated soil below" :
        "Interactive bird's-eye view of four independently controlled roof regions, drawn from the team's CAD");
    host.appendChild(canvas);

    gl = canvas.getContext("webgl2", { antialias: true, alpha: true });
    if (!gl) {
      host.innerHTML = '<p class="model-missing">This browser has no WebGL2, ' +
        'so the roof model cannot be drawn.</p>';
      return;
    }

    prog = gl.createProgram();
    gl.attachShader(prog, compile(gl.VERTEX_SHADER, VERT));
    gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, FRAG));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      throw new Error(gl.getProgramInfoLog(prog));
    }
    gl.useProgram(prog);
    ["uProj", "uView", "uModel", "uColor", "uLight", "uFlat"].forEach(function (name) {
      loc[name] = gl.getUniformLocation(prog, name);
    });
    var aPos = gl.getAttribLocation(prog, "aPos");
    overlayVAO = gl.createVertexArray();
    gl.bindVertexArray(overlayVAO);
    overlayBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, overlayBuffer);
    gl.enableVertexAttribArray(aPos);
    gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, 0, 0);
    gl.bindVertexArray(null);

    // Normalise so the roof's long axis spans about two units about the origin.
    var half = MODEL.extent[1] / 2 || 1;

    gpu = MODEL.meshes.map(function (mesh) {
      var vao = gl.createVertexArray();
      gl.bindVertexArray(vao);

      var positions = new Float32Array(mesh.positions.length);
      for (var i = 0; i < mesh.positions.length; i += 3) {
        positions[i]     = (mesh.positions[i])     / half;
        positions[i + 1] = (mesh.positions[i + 1]) / half;
        positions[i + 2] = (mesh.positions[i + 2]) / half;
      }
      var vbo = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
      gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
      gl.enableVertexAttribArray(aPos);
      gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, 0, 0);

      var ibo = gl.createBuffer();
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(mesh.indices), gl.STATIC_DRAW);

      gl.bindVertexArray(null);
      return { vao: vao, count: mesh.indices.length };
    });

    gl.enable(gl.DEPTH_TEST);
    bindCamera();
    window.addEventListener("resize", paintRoof);
  }

  function resetCamera() {
    camera.azimuth = Math.PI;
    camera.polar = 0.18;
    camera.distance = 4.4;
    drawRoof();
  }

  function bindCamera() {
    var dragging = false, lastX = 0, lastY = 0;

    canvas.addEventListener("pointerdown", function (e) {
      dragging = true;
      lastX = e.clientX;
      lastY = e.clientY;
      canvas.setPointerCapture(e.pointerId);
      $("model-frame").classList.add("dragging");
    });
    canvas.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      camera.azimuth -= (e.clientX - lastX) * 0.008;
      camera.polar = Math.max(0.13, Math.min(1.25, camera.polar + (e.clientY - lastY) * 0.006));
      lastX = e.clientX;
      lastY = e.clientY;
      drawRoof();
    });
    var endDrag = function (e) {
      dragging = false;
      $("model-frame").classList.remove("dragging");
      if (e && canvas.hasPointerCapture(e.pointerId)) canvas.releasePointerCapture(e.pointerId);
    };
    canvas.addEventListener("pointerup", endDrag);
    canvas.addEventListener("pointercancel", endDrag);
    canvas.addEventListener("wheel", function (e) {
      camera.distance = Math.max(2.3, Math.min(6.5, camera.distance * Math.exp(e.deltaY * 0.0012)));
      drawRoof();
      e.preventDefault();
    }, { passive: false });
    canvas.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") camera.azimuth += 0.08;
      else if (e.key === "ArrowRight") camera.azimuth -= 0.08;
      else if (e.key === "ArrowUp") camera.polar = Math.max(0.13, camera.polar - 0.06);
      else if (e.key === "ArrowDown") camera.polar = Math.min(1.25, camera.polar + 0.06);
      else if (e.key === "+" || e.key === "=") camera.distance = Math.max(2.3, camera.distance * 0.9);
      else if (e.key === "-") camera.distance = Math.min(6.5, camera.distance * 1.1);
      else if (e.key === "Home") resetCamera();
      else return;
      drawRoof();
      e.preventDefault();
    });
  }

  function paintRoof() {
    if (!gl || !MODEL) return;
    if (raf === null) raf = requestAnimationFrame(tickRoof);
  }

  function tickRoof() {
    raf = null;
    var moving = false;
    var keys = watering ? waterLayout.flaps.map(function (f) { return f.id; }) :
      ROOF_ZONES;
    keys.forEach(function (key) {
      var target = watering ? (waterState.open.includes(key) ? 1 : 0) :
        roofTarget(key);
      var from = shown[key] === undefined ? 0 : shown[key];
      var next = reduceMotion.matches ? target : from + (target - from) * 0.18;
      if (Math.abs(target - next) < 0.002) next = target;
      else moving = true;
      shown[key] = next;
    });
    drawRoof();
    if (moving || (waterState.raining && !reduceMotion.matches)) raf = requestAnimationFrame(tickRoof);
  }

  function overlay(vertices, colour, mode) {
    if (!vertices.length) return;
    gl.bindVertexArray(overlayVAO);
    gl.bindBuffer(gl.ARRAY_BUFFER, overlayBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.DYNAMIC_DRAW);
    gl.uniformMatrix4fv(loc.uModel, false, mat4());
    gl.uniform3fv(loc.uColor, colour);
    gl.drawArrays(mode, 0, vertices.length / 3);
  }

  function drawWater() {
    var layout = waterLayout, half = MODEL.extent[1] / 2;
    var cellX = layout.width_m / layout.cols, cellY = layout.length_m / layout.rows;
    var floor = -0.55, roof = 0.15;
    var groups = [[], [], [], []], lines = [], rain = [];
    function point(x, y, z) {
      return [((layout.origin_m[0] + x) * 10000 - MODEL.centre[0]) / half,
        ((layout.origin_m[1] + y) * 10000 - MODEL.centre[1]) / half, z];
    }
    for (var id = 0; id < layout.cols * layout.rows; id++) {
      var x = (id % layout.cols) * cellX, y = Math.floor(id / layout.cols) * cellY;
      var picked = waterState.selected.includes(id), wet = waterState.delivered[id] > 0;
      var vertices = groups[wet ? (picked ? 2 : 3) : (picked ? 1 : 0)];
      var a = point(x + cellX * .025, y + cellY * .025, floor);
      var b = point(x + cellX * .975, y + cellY * .025, floor);
      var c = point(x + cellX * .975, y + cellY * .975, floor);
      var d = point(x + cellX * .025, y + cellY * .975, floor);
      vertices.push(...a, ...b, ...c, ...a, ...c, ...d);
      if (waterState.raining && id % 3 === 0) {
        var receives = waterState.wet.includes(id);
        var bottom = receives ? floor : roof;
        var z = .7 - ((performance.now() / 750 + id * .618) % 1) * (.7 - bottom);
        rain.push(...point(x + cellX / 2, y + cellY / 2, z),
          ...point(x + cellX / 2, y + cellY / 2, Math.max(bottom, z - .08)));
      }
    }
    var colours = [[.83,.79,.71], [.36,.60,.36], [.30,.61,.76], [.90,.69,.41]];
    gl.uniform1i(loc.uFlat, 1);
    groups.forEach(function (v, i) { overlay(v, colours[i], gl.TRIANGLES); });
    layout.flaps.filter(function (f) { return waterState.open.includes(f.id); }).forEach(function (f) {
      for (var j = 0; j < 32; j++) {
        var angle = j * Math.PI / 16, next = (j + 1) * Math.PI / 16;
        var x = f.x_m + f.radius_m * Math.cos(angle), y = f.y_m + f.radius_m * Math.sin(angle);
        lines.push(...point(x, y, floor + .002),
          ...point(f.x_m + f.radius_m * Math.cos(next), f.y_m + f.radius_m * Math.sin(next), floor + .002));
        if (j % 8 === 0) lines.push(...point(x, y, floor), ...point(x, y, roof));
      }
    });
    overlay(lines, [.22,.50,.62], gl.LINES);
    overlay(rain, [.14,.43,.64], gl.LINES);
    gl.uniform1i(loc.uFlat, 0);
  }

  function waterCamera(aspect) {
    var at = [0, 0, -.05], direction = [
      Math.sin(camera.polar) * Math.cos(camera.azimuth),
      Math.sin(camera.polar) * Math.sin(camera.azimuth),
      Math.cos(camera.polar)
    ];
    var right = norm(cross([0, 0, 1], direction)), up = cross(direction, right);
    var distance = 0, tangent = Math.tan(.52 / 2);
    [-.5, .5].forEach(function (x) {
      [-1.1, 1.1].forEach(function (y) {
        [-.6, .75].forEach(function (z) {
          var p = sub([x, y, z], at);
          distance = Math.max(distance, dot(direction, p) +
            Math.max(Math.abs(dot(right, p)) / (tangent * aspect), Math.abs(dot(up, p)) / tangent));
        });
      });
    });
    return lookAt(direction.map(function (v, i) {
      return at[i] + v * distance * 1.08 * camera.distance / 4.4;
    }), at, [0, 0, 1]);
  }

  function roofTarget(zone) {
    if (zone === "D") return sky(hour).rain > 0 && overrides.D ? 1 : 0;
    return sim[zone] ? sim[zone][hour].open : 0;
  }

  function drawRoof() {
    if (!gl || !MODEL) return;

    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.max(1, Math.round(canvas.clientWidth * dpr));
    var h = Math.max(1, Math.round(canvas.clientHeight * dpr));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w; canvas.height = h;
    }
    gl.viewport(0, 0, w, h);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Start almost directly above the roof. Azimuth PI puts its long Y axis across the
    // wide screen; pointer drag moves away from plan view without losing the model.
    var proj = perspective(watering ? 0.52 : 0.46, w / h, 0.1, 40);
    var sinPolar = Math.sin(camera.polar);
    var eye = [
      camera.distance * sinPolar * Math.cos(camera.azimuth),
      camera.distance * sinPolar * Math.sin(camera.azimuth),
      camera.distance * Math.cos(camera.polar)
    ];
    var view = watering ? waterCamera(w / h) : lookAt(eye, [0, 0, -0.04], [0, 0, 1]);
    gl.useProgram(prog);
    gl.uniformMatrix4fv(loc.uProj, false, proj);
    gl.uniformMatrix4fv(loc.uView, false, view);
    if (watering) drawWater();

    // The key light follows the hour, so the roof is lit from where the sun is.
    var frac = (hour + 0.5) / 24;
    var elev = Math.sin(Math.max(0, (frac - 0.25) / 0.5) * Math.PI);
    gl.uniform3f(loc.uLight, Math.cos(frac * Math.PI * 2) * 0.8, -0.35, 0.35 + elev * 0.9);
    if (watering) gl.uniform3f(loc.uLight, .6, -.35, 1.1);

    var BASE = [0.47, 0.52, 0.49];
    var ZONE_COLOURS = {
      A: [0.045, 0.25, 0.13],
      B: [0.09, 0.36, 0.19],
      C: [0.20, 0.47, 0.25],
      D: [0.39, 0.59, 0.32]
    };
    var WATER_OPEN = [0.12, 0.39, 0.55];

    MODEL.instances.forEach(function (inst) {
      var model = translation(inst.offset[0], inst.offset[1], inst.offset[2]);
      var colour = BASE;

      if (inst.kind === "flap") {
        var zone = inst.renderZone;
        var open = shown[watering ? inst.node : zone] || 0;
        // Negative, so the free end at local -Y lifts away from the bed.
        model = multiply(model, rotationX(-open * MAX_FLAP_DEG * Math.PI / 180));
        colour = (watering ? waterState.raining : sky(hour).rain > 0) && open > 0.5 ?
          WATER_OPEN : ZONE_COLOURS[zone];
      }

      gl.uniformMatrix4fv(loc.uModel, false, model);
      gl.uniform3f(loc.uColor, colour[0], colour[1], colour[2]);
      var mesh = gpu[inst.mesh];
      gl.bindVertexArray(mesh.vao);
      gl.drawElements(gl.TRIANGLES, mesh.count, gl.UNSIGNED_SHORT, 0);
    });
    gl.bindVertexArray(null);
  }

  /* ---------- rain over the roof ---------- */

  function fraction(value) { return value - Math.floor(value); }

  function clearRain() {
    if (!rainCtx || !rainCanvas) return;
    rainCtx.clearRect(0, 0, rainCanvas.width, rainCanvas.height);
  }

  function drawRain(now) {
    rainRaf = null;
    if (!rainCtx || rainIntensity <= 0 || document.hidden || reduceMotion.matches) {
      clearRain();
      return;
    }

    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var width = Math.max(1, Math.round(rainCanvas.clientWidth * dpr));
    var height = Math.max(1, Math.round(rainCanvas.clientHeight * dpr));
    if (rainCanvas.width !== width || rainCanvas.height !== height) {
      rainCanvas.width = width;
      rainCanvas.height = height;
    }

    var w = width / dpr, h = height / dpr;
    rainCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    rainCtx.clearRect(0, 0, w, h);
    rainCtx.lineCap = "round";
    rainCtx.lineWidth = 1.5;
    rainCtx.strokeStyle = "rgba(174, 224, 244, .72)";
    rainCtx.beginPath();

    var strength = Math.min(1, rainIntensity / 24);
    var count = Math.round(28 + strength * 105);
    for (var i = 0; i < count; i++) {
      var x = fraction(Math.sin((i + 3) * 12.9898) * 43758.5453) * (w + 80) - 40;
      var start = fraction(Math.sin((i + 17) * 78.233) * 19341.719) * h;
      var speed = 190 + fraction(Math.sin((i + 11) * 5.331) * 9901.13) * 250;
      var y = (start + now / 1000 * speed) % (h + 100) - 50;
      var length = 16 + strength * 22;
      rainCtx.moveTo(x, y);
      rainCtx.lineTo(x - length * 0.22, y + length);
    }
    rainCtx.stroke();
    rainRaf = requestAnimationFrame(drawRain);
  }

  function updateRain() {
    rainIntensity = watering ? (waterState.raining ? 10 : 0) : D.hours[hour].rain_mm;
    $("model-frame").classList.toggle("raining", rainIntensity > 0);
    $("rain-status").textContent = watering ? (waterState.raining ? "Simulated rain event" : "Ready for rain") : rainIntensity > 0
      ? "Rain now · " + rainIntensity.toFixed(1) + " mm"
      : "No rain this hour";

    if (rainIntensity > 0 && !reduceMotion.matches && !document.hidden) {
      if (rainRaf === null) rainRaf = requestAnimationFrame(drawRain);
    } else {
      if (rainRaf !== null) cancelAnimationFrame(rainRaf);
      rainRaf = null;
      clearRain();
    }
  }

  function buildRain() {
    rainCanvas = $("rain-canvas");
    rainCtx = rainCanvas.getContext("2d");
    reduceMotion.addEventListener("change", updateRain);
    document.addEventListener("visibilitychange", updateRain);
  }

  /* ---------- zone rows ---------- */

  function regionName(zone) {
    if (zone === "D") return "Manual bay";
    var found = D.zones.find(function (z) { return z.zone === zone; });
    return found ? found.crop : "Region " + zone;
  }

  function buildRegionControls() {
    $("region-controls").innerHTML = ROOF_ZONES.map(function (zone) {
      return '' +
        '<label class="region-switch">' +
          '<span class="region-letter" data-zone="' + zone + '">' + zone + '</span>' +
          '<input type="checkbox" id="rain-' + zone + '"' + (overrides[zone] ? " checked" : "") + '>' +
          '<span class="region-copy">' +
            '<span class="region-name">' + regionName(zone) + '</span>' +
            '<span class="region-choice" id="choice-' + zone + '"></span>' +
          '</span>' +
          '<span class="toggle-ui" aria-hidden="true"></span>' +
        '</label>';
    }).join("");

    ROOF_ZONES.forEach(function (zone) {
      $("rain-" + zone).addEventListener("change", function (e) {
        overrides[zone] = e.target.checked;
        if (zone !== "D") runAll();
        paint();
      });
    });
  }

  function buildZones() {
    var cropZones = D.zones.map(function (z) {
      var target = z.light_rule === "dli"
        ? z.light_target + " mol target"
        : Math.round(z.light_target * 100) + "% shade wanted";
      return '' +
      '<div class="zone" id="row-' + z.zone + '">' +
        '<div class="z-id">' +
          '<span class="region-letter" data-zone="' + z.zone + '">' + z.zone + '</span>' +
          '<span class="z-name">' + z.crop + '</span>' +
          '<span class="z-bot">' + z.botanical + '</span>' +
        '</div>' +
        '<div class="meter">' +
          '<div class="meter-top"><span class="meter-label">Light today</span>' +
            '<span class="meter-val" id="lv-' + z.zone + '">-</span></div>' +
          '<div class="track"><div class="fill light" id="lf-' + z.zone + '"></div>' +
            (z.light_rule === "dli" ? '<div class="target" id="lt-' + z.zone + '"></div>' : '') +
          '</div>' +
          '<span class="meter-label">' + target + '</span>' +
        '</div>' +
        '<div class="meter">' +
          '<div class="meter-top"><span class="meter-label">Soil water</span>' +
            '<span class="meter-val" id="sv-' + z.zone + '">-</span></div>' +
          '<div class="track soil-track"><div class="fill soil" id="sf-' + z.zone + '"></div></div>' +
          '<span class="meter-label">dry below ' + C.SOIL_DRY_BELOW + ' mm</span>' +
        '</div>' +
        '<div class="z-state">' +
          '<span class="badge" id="bg-' + z.zone + '"><i></i><span id="bt-' + z.zone + '">-</span></span>' +
          '<span class="z-reason" id="br-' + z.zone + '"></span>' +
        '</div>' +
      '</div>';
    }).join("");

    var manualZone = '' +
      '<div class="zone manual-zone" id="row-D">' +
        '<div class="z-id">' +
          '<span class="region-letter" data-zone="D">D</span>' +
          '<span class="z-name">Manual bay</span>' +
          '<span class="z-bot">No crop model attached</span>' +
        '</div>' +
        '<p class="manual-copy">A fourth physical roof region for a grower-selected bed. It has no invented crop or soil figures.</p>' +
        '<div class="z-state">' +
          '<span class="badge" id="bg-D"><i></i><span id="bt-D">-</span></span>' +
          '<span class="z-reason" id="br-D"></span>' +
        '</div>' +
      '</div>';

    $("zones").innerHTML = cropZones + manualZone;

    D.zones.forEach(function (z) {
      if (z.light_rule === "dli") {
        var scale = Math.max(z.light_target * 1.7, 20);
        $("lt-" + z.zone).style.left = (z.light_target / scale * 100) + "%";
      }
    });
  }

  /* ---------- painting ---------- */

  function paint() {
    var h = D.hours[hour], s = sky(hour);
    var hh = String(h.local_hour).padStart(2, "0") + ":00";

    $("clock").textContent = hh;
    $("time-control").value = String(hour);
    $("weather-readout").textContent =
      "Sun " + h.ghi.toFixed(0) + " W/m² · Rain " + h.rain_mm.toFixed(1) +
      " mm · Air " + h.t2m.toFixed(1) + " °C";

    var touched = isTouched();
    $("reset").hidden = !touched;

    ROOF_ZONES.forEach(function (zone) {
      $("choice-" + zone).textContent = overrides[zone] ? "Rain enabled" : "Keep dry";
    });

    D.zones.forEach(function (z) {
      var r = sim[z.zone][hour];
      var scale = z.light_rule === "dli" ? Math.max(z.light_target * 1.7, 20) : 36;
      $("lv-" + z.zone).textContent = r.light.toFixed(1) + " mol";
      $("lf-" + z.zone).style.transform = "scaleX(" + Math.min(1, r.light / scale).toFixed(4) + ")";
      $("sv-" + z.zone).textContent = r.soil.toFixed(1) + " mm";
      $("sf-" + z.zone).style.transform = "scaleX(" + (r.soil / C.SOIL_CAPACITY).toFixed(4) + ")";

      var st = STATE[r.state];
      var badge = $("bg-" + z.zone);
      badge.className = "badge " + st.cls;
      $("bt-" + z.zone).textContent = st.text;
      $("br-" + z.zone).textContent = r.reason ? "Because " + REASON[r.reason] + "." : "";
      $("row-" + z.zone).classList.toggle("live", r.state === "RAIN_OPEN");
    });

    var manualOpen = s.rain > 0 && overrides.D;
    var manualBadge = $("bg-D");
    manualBadge.className = "badge " + (manualOpen ? "rain" : "shut");
    $("bt-D").textContent = s.rain > 0
      ? (manualOpen ? "Open for rain" : "Shut against rain")
      : (overrides.D ? "Ready for rain" : "Set to stay dry");
    $("br-D").textContent = s.rain > 0
      ? (manualOpen ? "The grower enabled rain for this region." : "The grower kept this region dry.")
      : "The fins will respond when the gauge records rain.";
    $("row-D").classList.toggle("live", manualOpen);

    updateRain();
    paintRoof();
  }

  /* ---------- playback ---------- */

  function setHour(i) {
    hour = Math.max(0, Math.min(D.hours.length - 1, i));
    paint();
  }

  function step() {
    if (hour >= D.hours.length - 1) { stop(); return; }
    setHour(hour + 1);
    timer = setTimeout(step, D.hours[hour].play_seconds * 1000);
  }

  function stop() {
    playing = false;
    clearTimeout(timer);
    $("play-label").textContent = hour >= D.hours.length - 1 ? "Play again" : "Play the day";
  }

  function play() {
    if (playing) { stop(); return; }
    if (hour >= D.hours.length - 1) setHour(0);
    playing = true;
    $("play-label").textContent = "Pause";
    timer = setTimeout(step, D.hours[hour].play_seconds * 1000);
  }

  /* ---------- timeline ---------- */

  function bindTimeline() {
    $("time-control").addEventListener("input", function (e) {
      stop();
      setHour(Number(e.target.value));
    });
  }

  /* ---------- static furniture ---------- */

  function buildRegion() {
    var r = D.region;
    $("foot-region").textContent =
      "That year the gauge caught " + r.rain_mm.toLocaleString() + " mm of rain over " +
      r.rain_hours.toLocaleString() + " hours, " + r.vs_normal_pct +
      " percent above the 1991 to 2020 normal of " + r.normal_mm.toLocaleString() +
      " mm, so 2023 was an ordinary year here. " + r.daylight_rain_hours +
      " of those hours fell in daylight, carrying " + r.daylight_rain_mm.toLocaleString() +
      " mm, and that is the rain this roof can do anything about. " + r.source;
  }

  /* ---------- boot ---------- */

  function boot(data) {
    D = data; C = D.constants;
    D.zones.forEach(function (z) { overrides[z.zone] = !!z.rain_ok; });
    overrides.D = MANUAL_RAIN_DEFAULT;

    $("place").textContent = D.place;
    $("date").textContent = new Date(D.date_local + "T12:00:00").toLocaleDateString(undefined,
      { weekday: "long", day: "numeric", month: "long", year: "numeric" });
    $("sources").textContent = "Sun: " + D.sources.sun + ". Rain: " + D.sources.rain + ".";
    $("credit").textContent = D.credit;

    buildRegion(); buildRain(); buildRoof(); buildRegionControls(); buildZones(); bindTimeline();
    runAll(); setHour(0);

    $("play").disabled = false;
    $("play").addEventListener("click", play);
    $("reset-view").addEventListener("click", resetCamera);
    $("reset").addEventListener("click", function () {
      cloud = 0;
      D.zones.forEach(function (z) {
        overrides[z.zone] = !!z.rain_ok;
        $("rain-" + z.zone).checked = !!z.rain_ok;
      });
      overrides.D = MANUAL_RAIN_DEFAULT;
      $("rain-D").checked = MANUAL_RAIN_DEFAULT;
      runAll(); paint();
    });
  }

  if (watering) {
    window.CadRoof = {
      mount: function (model, layout) {
        MODEL = model; waterLayout = layout;
        buildRain(); buildRoof(); paintRoof();
        $("reset-view").addEventListener("click", resetCamera);
      },
      update: function (state) { waterState = state; updateRain(); paintRoof(); }
    };
    return;
  }

  Promise.all([
    fetch("day.json").then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }),
    fetch("model.json").then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
  ])
    .then(function (both) { MODEL = both[1]; boot(both[0]); })
    .catch(function () {
      $("place").textContent =
        "The day's file is missing. Run python software/page/build_day.py, then reload.";
    });
})();
