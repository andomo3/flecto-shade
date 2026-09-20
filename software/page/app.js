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
    if (cloud !== 0) return true;
    return D.zones.some(function (z) { return overrides[z.zone] !== !!z.rain_ok; });
  }

  /* ---------- the roof figure ---------- */

  function buildRoof() {
    var W = 1000, H = 420, padX = 30, gap = 40, topPad = 56;
    var n = D.zones.length;
    var bedW = (W - padX * 2 - gap * (n - 1)) / n;
    var bedH = H - topPad - 24;
    var svg = ['<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="xMidYMid meet"' +
               ' role="img" aria-label="Three shade house zones seen from above, each under its own roof of fins">'];

    D.zones.forEach(function (z, zi) {
      var x = padX + zi * (bedW + gap);
      svg.push('<text class="bed-label" x="' + x + '" y="24">Zone ' + z.zone + '</text>');
      svg.push('<text class="bed-crop" x="' + x + '" y="44">' + z.crop + '</text>');
      svg.push('<rect x="' + x + '" y="' + topPad + '" width="' + bedW + '" height="' + bedH +
               '" rx="8" fill="#ffffff" stroke="#ded7c9"/>');

      // A louvre turning edge-on narrows to a line, so a fin's drawn depth is its open
      // fraction. Shut, the slats touch and roof the bed.
      var slats = 12, inset = 14;
      var span = bedH - inset * 2;
      var pitch = span / (slats - 1);
      for (var i = 0; i < slats; i++) {
        var fy = topPad + inset + pitch * i;
        var h = pitch - 2;
        svg.push('<rect class="fin" id="fin-' + z.zone + '-' + i + '" x="' + (x + 10) +
                 '" y="' + (fy - h / 2) + '" width="' + (bedW - 20) + '" height="' + h.toFixed(1) +
                 '" rx="2" fill="#1e6b3a"/>');
      }
    });

    svg.push('</svg>');
    $("roof").innerHTML = svg.join("");
  }

  function paintRoof() {
    D.zones.forEach(function (z) {
      var open = sim[z.zone][hour].open;
      var scale = (1 - open * 0.88).toFixed(3);       // 1 shut, 0.12 fully open
      var op = (0.6 + (1 - open) * 0.4).toFixed(2);   // solid when it roofs the bed
      for (var i = 0; i < 12; i++) {
        var el = document.getElementById("fin-" + z.zone + "-" + i);
        if (el) {
          el.style.transform = "scaleY(" + scale + ")";
          el.setAttribute("fill-opacity", op);
        }
      }
    });
  }

  /* ---------- zone rows ---------- */

  function buildZones() {
    $("zones").innerHTML = D.zones.map(function (z) {
      var target = z.light_rule === "dli"
        ? z.light_target + " mol target"
        : Math.round(z.light_target * 100) + "% shade wanted";
      return '' +
      '<div class="zone" id="row-' + z.zone + '">' +
        '<div class="z-id">' +
          '<span class="z-name">Zone ' + z.zone + ' &middot; ' + z.crop + '</span>' +
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
        '<label class="switch">' +
          '<input type="checkbox" id="sw-' + z.zone + '"' + (z.rain_ok ? " checked" : "") + '>' +
          '<span class="switch-ui"></span>' +
          '<span class="switch-text">Take rain</span>' +
        '</label>' +
      '</div>';
    }).join("");

    D.zones.forEach(function (z) {
      $("sw-" + z.zone).addEventListener("change", function (e) {
        overrides[z.zone] = e.target.checked;
        runAll(); paint();
      });
      if (z.light_rule === "dli") {
        var scale = Math.max(z.light_target * 1.7, 20);
        $("lt-" + z.zone).style.left = (z.light_target / scale * 100) + "%";
      }
    });
  }

  /* ---------- painting ---------- */

  function skyColour(ghi) {
    var t = Math.min(1, Math.max(0, ghi) / 900);
    // night end of the ramp, then the lit end
    var topA = [20, 29, 46],  topB = [26, 88, 148];
    var botA = [36, 50, 74],  botB = [138, 188, 226];
    var mix = function (a, b) { return Math.round(a + (b - a) * t); };
    var rgb = function (a, b) {
      return "rgb(" + mix(a[0], b[0]) + "," + mix(a[1], b[1]) + "," + mix(a[2], b[2]) + ")";
    };
    return "linear-gradient(180deg," + rgb(topA, topB) + "," + rgb(botA, botB) + ")";
  }

  function paint() {
    var h = D.hours[hour], s = sky(hour);
    var hh = String(h.local_hour).padStart(2, "0") + ":00";

    $("clock").textContent = hh;
    $("rec-ghi").textContent = h.ghi.toFixed(0) + " W/m²";
    $("rec-rain").textContent = h.rain_mm.toFixed(1) + " mm";
    $("rec-t2m").textContent = h.t2m.toFixed(1) + " °C";

    $("sky-fill").style.background = skyColour(s.ghi);
    $("sky-cloud").style.opacity = cloud / 100;
    $("sun").style.left = ((hour + 0.5) / 24 * 100) + "%";
    $("sun").classList.toggle("night", h.ghi <= 0);
    $("sun").setAttribute("aria-valuenow", String(h.local_hour));
    $("sun").setAttribute("aria-valuetext", hh);

    var touched = isTouched();
    $("mode-pill").hidden = !touched;
    $("reset").hidden = !touched;
    $("cloud-out").textContent = cloud === 0 ? "as recorded" : cloud + "% added";

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

  /* ---------- scrubbing ---------- */

  function scrubTo(clientX) {
    var box = $("sky").getBoundingClientRect();
    var frac = (clientX - box.left) / box.width;
    setHour(Math.round(frac * 24 - 0.5));
  }

  function bindScrub() {
    var band = $("sky"), dragging = false;
    var down = function (e) {
      dragging = true; stop();
      scrubTo(e.touches ? e.touches[0].clientX : e.clientX);
      e.preventDefault();
    };
    var move = function (e) {
      if (!dragging) return;
      scrubTo(e.touches ? e.touches[0].clientX : e.clientX);
    };
    var up = function () { dragging = false; };

    band.addEventListener("mousedown", down);
    band.addEventListener("touchstart", down, { passive: false });
    window.addEventListener("mousemove", move);
    window.addEventListener("touchmove", move, { passive: false });
    window.addEventListener("mouseup", up);
    window.addEventListener("touchend", up);

    $("sun").addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { stop(); setHour(hour + 1); e.preventDefault(); }
      if (e.key === "ArrowLeft")  { stop(); setHour(hour - 1); e.preventDefault(); }
      if (e.key === "Home")       { stop(); setHour(0); e.preventDefault(); }
      if (e.key === "End")        { stop(); setHour(23); e.preventDefault(); }
    });
  }

  /* ---------- static furniture ---------- */

  function buildTicks() {
    var out = [];
    for (var i = 0; i <= 24; i += 3) {
      out.push('<span class="' + (i % 6 === 0 ? "major" : "") + '" style="left:' + (i / 24 * 100) + '%"></span>');
      if (i < 24) out.push('<b style="left:' + ((i + 0.5) / 24 * 100) + '%">' + String(i).padStart(2, "0") + '</b>');
    }
    $("sky-ticks").innerHTML = out.join("");
  }

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

    $("place").textContent = D.place + " · " + D.date_local;
    $("date").textContent = new Date(D.date_local + "T12:00:00").toLocaleDateString(undefined,
      { weekday: "long", day: "numeric", month: "long", year: "numeric" });
    $("sources").textContent = "Sun: " + D.sources.sun + ". Rain: " + D.sources.rain + ".";
    $("credit").textContent = D.credit;

    buildTicks(); buildRegion(); buildRoof(); buildZones(); bindScrub();
    runAll(); setHour(0);

    $("play").disabled = false;
    $("play").addEventListener("click", play);
    $("cloud").addEventListener("input", function (e) {
      cloud = Number(e.target.value); runAll(); paint();
    });
    $("reset").addEventListener("click", function () {
      cloud = 0; $("cloud").value = 0;
      D.zones.forEach(function (z) {
        overrides[z.zone] = !!z.rain_ok;
        $("sw-" + z.zone).checked = !!z.rain_ok;
      });
      runAll(); paint();
    });
  }

  fetch("day.json")
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(boot)
    .catch(function () {
      $("place").textContent =
        "The day's file is missing. Run python software/page/build_day.py, then reload.";
    });
})();
