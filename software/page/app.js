/* Boot: load the simulated day, stand the model up, and wire the console to it.

   The page is usable with no server at all. day.json is a static file written by
   package H2 from package H1's output, and everything the demonstration shows is
   derived from it. The API is asked for stored configuration once, after the screen is
   already drawn, and the console shows an explicit offline state if it is not there.
*/

(function (root) {
  "use strict";

  var Fin = root.Flectofin;
  var $ = function (id) { return document.getElementById(id); };
  var SITE = "boston-demo";

  var scene = null, panel = null, day = null;

  /* ------------------------------------------------------------ loading state */

  function skeleton() {
    $("zone-grid").innerHTML = new Array(3).join(",").split(",").map(function () {
      return '<article class="zone-card is-loading" aria-hidden="true">' +
        '<span class="skeleton line wide"></span><span class="skeleton line"></span>' +
        '<span class="skeleton block"></span><span class="skeleton line"></span></article>';
    }).join("");
    $("inspector-body").innerHTML =
      '<span class="skeleton line wide"></span><span class="skeleton block"></span>';
  }

  function failed(message) {
    $("stage-fallback").hidden = false;
    $("stage-fallback").innerHTML = '<p>' + message + '</p>';
    $("stage-place").textContent = "The simulated day could not be loaded.";
    $("run-state").setAttribute("data-state", "offline");
    $("run-state").querySelector("span").textContent = "Simulated day unavailable";
    $("zone-grid").innerHTML = '<p class="empty">No simulated result is available, so no zone ' +
      'decision, roof position, or modelled crop condition can be shown.</p>';
    $("inspector-body").innerHTML = '<p class="empty">Nothing to inspect until the simulated ' +
      'day loads.</p>';
    $("announce").textContent = message;
  }

  /* ------------------------------------------------------------ rain over the model */

  /* The rain is drawn inside the scene, not over it, so the modelled roof can stop it.
     This only hands the hour's modelled rate across and marks the stage state. */
  function syncRain(hour) {
    var raining = hour.rain_mm > 0;
    $("stage-frame").classList.toggle("is-raining", raining);
    scene.setRain(document.hidden ? 0 : hour.rain_mm);
  }

  /* ------------------------------------------------------------ the technical overlay */

  var OVERLAY_POINTS = [
    { key: "crown", label: "Backbone", note: "Bows under actuation" },
    { key: "rootLeft", label: "Stiffer root", note: "Stays on the backbone" },
    { key: "freeEdgeLeft", label: "Left lamella, free edge", note: "Bends most" },
    { key: "freeEdgeRight", label: "Right lamella, free edge", note: "Nested, never overlapping" },
    { key: "supports", label: "Support points", note: "Conceptual clamps, on the rail" }
  ];

  function paintOverlay() {
    var anchors = $("anchors"), lines = $("overlay-lines");
    if (!scene || !scene.overlayOn()) {
      anchors.innerHTML = "";
      lines.innerHTML = "";
      var inspecting = scene && scene.mode() !== "operate";
      $("module-legend").hidden = !inspecting;
      $("module-parts").hidden = false;
      if (inspecting) {
        var showing = scene.focusBay(panel ? panel.state.selected : null);
        if (showing) {
          $("module-open-value").textContent =
            Math.round(Fin.openingFraction(showing.actuation) * 100) + "%";
          $("module-actuation").textContent = showing.actuation.toFixed(2);
        }
      }
      return;
    }
    var bay = scene.focusBay(panel ? panel.state.selected : null);
    if (!bay) { return; }
    var marks = Fin.annotations(bay.actuation);

    function place(point) {
      return scene.project([
        bay.origin[0] + point[0], bay.origin[1] + point[1], bay.origin[2] + point[2]
      ]);
    }

    var items = [];
    OVERLAY_POINTS.forEach(function (item) {
      var source = marks[item.key];
      var point = Array.isArray(source[0]) ? source[Math.floor(source.length / 2)] : source;
      var screen = place(point);
      if (screen) { items.push({ label: item.label, note: item.note, at: screen }); }
    });

    var arrow = place(marks.crown);
    var base = place(marks.supports[0]);
    lines.innerHTML = items.map(function (item, index) {
      var toY = 42 + index * 64;
      return '<line x1="' + item.at[0].toFixed(1) + '" y1="' + item.at[1].toFixed(1) +
        '" x2="24" y2="' + toY + '" />' +
        '<circle cx="' + item.at[0].toFixed(1) + '" cy="' + item.at[1].toFixed(1) + '" r="3.5" />';
    }).join("") + (arrow && base
      ? '<line class="actuation" x1="' + base[0].toFixed(1) + '" y1="' + base[1].toFixed(1) +
        '" x2="' + arrow[0].toFixed(1) + '" y2="' + arrow[1].toFixed(1) + '" />'
      : "");

    anchors.innerHTML = items.map(function (item, index) {
      return '<span class="anchor" style="top:' + (42 + index * 64 - 18) + 'px">' +
        '<strong>' + item.label + '</strong><em>' + item.note + '</em></span>';
    }).join("");

    /* The anchors already name every part, so the parts list stands down while the
       overlay is on and the numbers stay. */
    $("module-legend").hidden = false;
    $("module-parts").hidden = true;
    $("module-open-value").textContent = Math.round(marks.openingFraction * 100) + "%";
    $("module-actuation").textContent = bay.actuation.toFixed(2);
  }

  /* The A to D identifiers, anchored to the zone they name rather than floating. */
  function paintZoneTags(frame) {
    var host = $("zone-tags");
    if (!panel || frame.mode !== "operate") { host.innerHTML = ""; return; }
    var selected = panel.state.selected;
    host.innerHTML = Object.keys(frame.zoneCentre).map(function (letter) {
      var at = scene.project(frame.zoneCentre[letter]);
      if (!at) { return ""; }
      var zone = panel.state.zones.filter(function (item) { return item.letter === letter; })[0];
      return '<span class="zone-tag' + (selected === letter ? " is-selected" : "") +
        '" style="left:' + at[0].toFixed(1) + 'px;top:' + at[1].toFixed(1) + 'px">' +
        '<b>' + letter + '</b>' + (zone ? "<i>" + zone.name + "</i>" : "") + '</span>';
    }).join("");
    keepTagsInside(host);
  }

  /* A tag is centred on its zone, so a zone near the edge pushes half its tag out of
     the frame. Only a tag that close to an edge has its width read, and is pulled back in. */
  function keepTagsInside(host) {
    var width = host.clientWidth, margin = 8, near = 140;
    Array.prototype.forEach.call(host.children, function (tag) {
      var x = parseFloat(tag.style.left);
      if (x > near && x < width - near) { return; }
      var half = tag.offsetWidth / 2 + margin;
      tag.style.left = Math.min(Math.max(x, half), Math.max(half, width - half)).toFixed(1) + "px";
    });
  }

  function buildModuleParts() {
    $("module-parts").innerHTML = Fin.PART_LABELS.map(function (part) {
      return "<div><dt>" + part.label + "</dt><dd>" + part.note + "</dd></div>";
    }).join("");
  }

  /* ------------------------------------------------------------ stage controls */

  function bindStage() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-preset]"), function (button) {
      button.addEventListener("click", function () {
        Array.prototype.forEach.call(document.querySelectorAll("[data-preset]"), function (other) {
          other.setAttribute("aria-pressed", other === button ? "true" : "false");
        });
        scene.preset(button.getAttribute("data-preset"));
      });
    });

    $("reset-view").addEventListener("click", function () {
      scene.resetView();
      $("inspect-toggle").setAttribute("aria-pressed", "false");
      $("explode-toggle").setAttribute("aria-pressed", "false");
      $("explode-toggle").disabled = true;
      $("stage-frame").classList.remove("is-inspecting");
      scene.setMode("operate");
      panel.announce("Model view reset to the overview.");
    });

    $("inspect-toggle").addEventListener("click", function () {
      var on = this.getAttribute("aria-pressed") !== "true";
      this.setAttribute("aria-pressed", on ? "true" : "false");
      $("explode-toggle").disabled = !on;
      if (!on) { $("explode-toggle").setAttribute("aria-pressed", "false"); }
      $("stage-frame").classList.toggle("is-inspecting", on);
      scene.setMode(on ? "inspect" : "operate", panel.state.selected);
      panel.announce(on
        ? "Inspecting one Flectofin module, isolated from the roof."
        : "Back to the whole modelled shade house.");
    });

    $("explode-toggle").addEventListener("click", function () {
      var on = this.getAttribute("aria-pressed") !== "true";
      this.setAttribute("aria-pressed", on ? "true" : "false");
      scene.setMode(on ? "exploded" : "inspect", panel.state.selected);
      panel.announce(on
        ? "Exploded view: the lamellae, the backbone, and the conceptual clamps are parted."
        : "Module reassembled.");
    });

    $("overlay-toggle").addEventListener("click", function () {
      var on = this.getAttribute("aria-pressed") !== "true";
      this.setAttribute("aria-pressed", on ? "true" : "false");
      $("stage-frame").classList.toggle("is-overlay", on);
      scene.setOverlay(on);
      paintOverlay();
      panel.announce(on ? "Technical overlay shown." : "Technical overlay hidden.");
    });
  }

  /* ------------------------------------------------------------ stored configuration */

  function loadStored() {
    if (typeof fetch !== "function") { panel.offlineStore(); return; }
    root.Api.health()
      .then(function () { return Promise.all([root.Api.zones(SITE), root.Api.metricDefinitions()]); })
      .then(function (both) {
        panel.setMetricRegistry(both[1].metrics);
        panel.adoptStored(both[0]);
      })
      .catch(function () {
        panel.offlineStore(
          "Offline. The historical demonstration runs from the static simulated day; " +
          "configuration changes are held in this session only.");
      });
  }

  /* ------------------------------------------------------------ boot */

  function start(payload) {
    day = payload;

    $("stage-place").textContent = day.place;
    $("clock-date").textContent = day.date_local;
    $("foot-sources").textContent = "Sun: " + day.sources.sun + ". Rain: " + day.sources.rain + ".";
    $("foot-credit").textContent = day.credit;
    $("foot-region").textContent = "In " + day.region.year + " the named gauge recorded " +
      day.region.rain_mm.toLocaleString() + " mm across " +
      day.region.rain_hours.toLocaleString() + " rain hours, " +
      day.region.daylight_rain_hours + " of them during daylight. " + day.region.source;

    document.addEventListener("visibilitychange", function () {
      syncRain(day.hours[panel.hour()]);
    });

    scene = root.ShadeHouse.create({
      host: $("stage-viewport"),
      onZonePick: function (letter) { panel.select(letter, false); },
      onFrame: function (frame) { paintZoneTags(frame); paintOverlay(); }
    });

    if (!scene.mount()) {
      $("stage-fallback").hidden = false;
      $("stage-fallback").innerHTML = "<p>This browser cannot draw the modelled roof. " +
        "Every zone decision, roof position, and reason stays available in words below.</p>";
    }

    panel = root.Console.create({
      scene: scene,
      onRender: function (state) {
        syncRain(day.hours[state.hour]);
        paintOverlay();
      }
    });

    buildModuleParts();
    bindStage();
    panel.boot(day);
    loadStored();
  }

  /* ------------------------------------------------------------ the lede's one action */

  /* "See the roof decide" is a one-way handoff. The introductory section leaves the
     document flow, so scrolling up returns to the roof rather than the landing copy.
     The canvas carries tabindex 0 once the model mounts; if the browser cannot draw
     it, the stage heading takes the focus instead and the words below still read. */
  function handOverToTheRoof() {
    var button = $("to-roof");
    if (!button) { return; }
    button.addEventListener("click", function () {
      var frame = $("stage-frame");
      var target = frame.querySelector(".stage-canvas") || $("stage-title");
      var lede = document.querySelector(".lede");
      if (lede) { lede.hidden = true; }
      if (frame.scrollIntoView) {
        frame.scrollIntoView({ behavior: "auto", block: "start" });
      }
      if (target && target.focus) { target.focus({ preventScroll: true }); }
    });
  }

  handOverToTheRoof();

  skeleton();
  fetch("day.json")
    .then(function (response) {
      if (!response.ok) { throw new Error(String(response.status)); }
      return response.json();
    })
    .then(start)
    .catch(function () {
      failed("The simulated day file is missing. Run python software/page/build_day.py, " +
             "then reload this page.");
    });
}(typeof self !== "undefined" ? self : this));
