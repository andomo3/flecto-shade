/* The operating console: overview, inspector, timeline, and the configuration workspace.

   Every figure it shows is simulated or modelled. The three committed zones carry
   package H1's own hours out of day.json unchanged; a zone a grower adds, and any hour
   a manual override touches, is run through the same deterministic rules in rules.js.
   Which of the two a row is reading is stated on the row, never left to be guessed.

   Colour is never the only carrier of a state. Every status has a word, a glyph, and a
   border treatment as well.
*/

(function (root) {
  "use strict";

  var Rules = root.Rules;
  var SITE = "apopka-demo";
  var MAX_ZONES = 4;
  var LETTERS = ["A", "B", "C", "D"];

  /* The registry the console falls back to when the API is unavailable. It is the same
     list the API serves, and a metric outside it is never rendered. */
  var METRICS = [
    { id: "roof_position", label: "Roof position", removable: false },
    { id: "control_state", label: "Control state", removable: false },
    { id: "decision_reason", label: "Decision reason", removable: false },
    { id: "rain_outcome", label: "Rain admitted or excluded", removable: true },
    { id: "daily_light", label: "Daily light against target", removable: true },
    { id: "soil_water", label: "Modelled soil water", removable: true },
    { id: "last_decision", label: "Last decision", removable: true },
    { id: "next_action", label: "Next expected action", removable: true },
    { id: "data_timestamp", label: "Data timestamp", removable: true },
    { id: "irrigation", label: "Modelled irrigation added", removable: true }
  ];
  var DEFAULT_PROFILE = METRICS.filter(function (metric) {
    return metric.id !== "irrigation";
  }).map(function (metric) { return metric.id; });

  var STATUS = {
    auto:     { word: "Automatic", glyph: "M3 8.5l3.2 3.2L13 5" },
    warning:  { word: "Attention", glyph: "M8 2.5L14.5 13.5h-13zM8 6.6v3.2M8 11.4v.1" },
    conflict: { word: "Conflict",  glyph: "M8 1.8L14.8 13.8H1.2zM8 6v3.6M8 11.2v.2" },
    manual:   { word: "Manual hold", glyph: "M3 5h10M3 11h10M6 3v4M10 9v4" },
    stale:    { word: "Stale data", glyph: "M8 3v5l3 2M8 14A6 6 0 108 2a6 6 0 000 12z" },
    offline:  { word: "Not stored", glyph: "M2.5 13.5l11-11M4 8a6 6 0 019-5M12 8a6 6 0 01-9 5" }
  };

  function create(options) {
    var scene = options.scene;
    var day = null, constants = null, hours = [];
    var state = {
      hour: 0,
      playing: false,
      timer: null,
      selected: null,
      zones: [],
      metrics: METRICS.slice(),
      store: { online: false, checked: false, message: "Session only, nothing stored" },
      lastRunId: null,
      draft: null,
      metricDraft: null,
      announced: -1
    };

    var $ = function (id) { return document.getElementById(id); };
    var clamp = function (value, low, high) { return Math.max(low, Math.min(high, value)); };
    var hourText = function (value) { return String(value).padStart(2, "0") + ":00"; };
    var escape = function (text) {
      return String(text).replace(/[&<>"']/g, function (character) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[character];
      });
    };

    function glyph(path, extra) {
      return '<svg class="glyph ' + (extra || "") + '" viewBox="0 0 16 16" aria-hidden="true">' +
        '<path d="' + path + '"/></svg>';
    }

    /* ------------------------------------------------------------ zone model */

    function zoneFrom(source, letter) {
      return {
        letter: letter,
        id: null,
        persisted: false,
        revision: 1,
        resultsRevision: 1,
        name: source.crop,
        crop_name: source.crop,
        botanical: source.botanical || "",
        light_rule: source.light_rule,
        light_target: source.light_target,
        soil_request_below_mm: constants.SOIL_DRY_BELOW,
        rain_ok: !!source.rain_ok,
        kc: source.kc,
        soil_start: source.soil_start,
        note: source.note || "",
        archived: false,
        origin: "committed",
        review_profile: DEFAULT_PROFILE.slice(),
        overrides: [],
        baseline: source.hours.map(function (item) {
          return {
            local_hour: item.local_hour === undefined ? 0 : item.local_hour,
            open: item.open_fraction,
            state: item.state,
            reason: item.reason,
            conflict: false,
            manual: false,
            light: item.light_mol_so_far,
            soil: item.soil_mm,
            rainIn: item.rain_in_mm,
            irrigation: item.irrigation_mm
          };
        }),
        results: null
      };
    }

    function configuredLikeBaseline(zone) {
      var source = day.zones.filter(function (item) { return item.zone === zone.letter; })[0];
      if (!source) { return false; }
      return zone.light_rule === source.light_rule &&
        zone.light_target === source.light_target &&
        zone.rain_ok === !!source.rain_ok &&
        zone.kc === source.kc &&
        zone.soil_request_below_mm === constants.SOIL_DRY_BELOW;
    }

    function recompute() {
      state.zones.forEach(function (zone) {
        if (zone.archived) { zone.results = null; return; }
        var untouched = zone.origin === "committed" &&
          !zone.overrides.length && configuredLikeBaseline(zone);
        zone.results = untouched
          ? zone.baseline.map(function (item) { return Object.assign({}, item); })
          : Rules.runZone(constants, zone, hours, zone.overrides);
        zone.source = untouched ? "committed" : "modelled";
        zone.resultsRevision = zone.revision;
      });
    }

    function activeZones() {
      return state.zones.filter(function (zone) { return !zone.archived; });
    }

    function zoneOf(letter) {
      return state.zones.filter(function (zone) { return zone.letter === letter; })[0] || null;
    }

    function resultAt(zone, hour) {
      if (!zone.results) { return null; }
      return zone.results[clamp(hour, 0, zone.results.length - 1)];
    }

    /* ------------------------------------------------------------ zone status */

    /* The control state of a zone, which is about the roof and not about the store.
       Whether the configuration is stored is a property of the service, reported on
       the store chip and on the card's footer, so an offline service never makes a
       working zone look broken. */
    function statusOf(zone) {
      var result = resultAt(zone, state.hour);
      if (!result) { return "offline"; }
      if (result.conflict) { return "conflict"; }
      if (result.manual) { return "manual"; }
      if (zone.revision !== zone.resultsRevision) { return "stale"; }
      if (result.state === "HEAT_SHADE") { return "warning"; }
      if (result.soil < zone.soil_request_below_mm && !zone.rain_ok) { return "warning"; }
      return "auto";
    }

    function statusNote(zone, status) {
      var result = resultAt(zone, state.hour);
      if (status === "conflict") {
        return "A safety rule refused the manual command for this hour.";
      }
      if (status === "manual") {
        var held = zone.overrides[zone.overrides.length - 1];
        return "Held " + held.command + " until " + hourText(held.until_hour % 24) +
          (held.until_hour >= 24 ? ", the end of the simulated day" : "");
      }
      if (status === "offline") {
        return "No modelled result for this hour, so no roof position can be shown.";
      }
      if (status === "stale") { return "Configuration revision " + zone.revision +
        " has not been run yet."; }
      if (status === "warning" && result && result.state === "HEAT_SHADE") {
        return "The modelled heat shade rule is holding the roof part folded.";
      }
      if (status === "warning") {
        return "Modelled soil is below the request threshold and this crop excludes rain.";
      }
      return "Running on the deterministic zone rules.";
    }

    function positionText(result) {
      if (!result) { return "Unavailable"; }
      if (result.open > 0.08 && result.open < 0.92) {
        return "Part folded, " + Math.round(result.open * 100) + "%";
      }
      return Rules.STATE_LABEL[result.state] || "Closed";
    }

    function rainOutcome(zone, result) {
      if (!hours[state.hour] || hours[state.hour].rain_mm <= 0) { return "No modelled rain this hour"; }
      return result && result.rainIn > 0
        ? "Admitting gauge-recorded rain"
        : "Rain excluded from this zone";
    }

    function transitions(zone) {
      var out = [];
      if (!zone.results) { return out; }
      for (var index = 1; index < zone.results.length; index++) {
        var now = zone.results[index], before = zone.results[index - 1];
        if (now.state !== before.state || now.open !== before.open || now.reason !== before.reason) {
          out.push({ hour: index, result: now });
        }
      }
      return out;
    }

    function lastDecision(zone) {
      var found = null;
      transitions(zone).forEach(function (item) {
        if (item.hour <= state.hour) { found = item; }
      });
      if (!found) { return hourText(0) + ", " + positionText(resultAt(zone, 0)).toLowerCase(); }
      return hourText(found.hour) + ", " + positionText(found.result).toLowerCase();
    }

    function nextAction(zone) {
      var found = null;
      transitions(zone).forEach(function (item) {
        if (found === null && item.hour > state.hour) { found = item; }
      });
      if (!found) { return "No further modelled change today"; }
      return hourText(found.hour) + ", " + positionText(found.result).toLowerCase();
    }

    /* ------------------------------------------------------------ metric cells */

    function metricCell(zone, id) {
      var result = resultAt(zone, state.hour);
      var target = zone.light_rule === "dli"
        ? zone.light_target.toFixed(1) + " mol m⁻² d⁻¹"
        : "shade rule, " + Math.round(zone.light_target * 100) + "%";

      switch (id) {
        case "roof_position":
          return { label: "Roof position", value: positionText(result) };
        case "control_state":
          return { label: "Control state", value: STATUS[statusOf(zone)].word };
        case "decision_reason":
          return { label: "Decision reason",
                   value: result ? Rules.reasonText(zone, result) : "No modelled result yet",
                   wide: true };
        case "rain_outcome":
          return { label: "Rain", value: rainOutcome(zone, result) };
        case "daily_light":
          return {
            label: "Daily light, modelled",
            value: result ? result.light.toFixed(1) + " of " + target : "-",
            bar: result && zone.light_rule === "dli"
              ? clamp(result.light / Math.max(zone.light_target, 0.1), 0, 1) : null,
            tone: "light"
          };
        case "soil_water":
          return {
            label: "Soil water, modelled",
            value: result
              ? result.soil.toFixed(1) + " mm, requests rain below " +
                zone.soil_request_below_mm.toFixed(0) + " mm"
              : "-",
            bar: result ? clamp(result.soil / constants.SOIL_CAPACITY, 0, 1) : null,
            mark: zone.soil_request_below_mm / constants.SOIL_CAPACITY,
            tone: "soil"
          };
        case "last_decision":
          return { label: "Last decision", value: lastDecision(zone) };
        case "next_action":
          return { label: "Next expected action", value: nextAction(zone) };
        case "data_timestamp":
          return { label: "Data timestamp",
                   value: day.date_local + " " + hourText(state.hour) + " local, historical input" };
        case "irrigation":
          return { label: "Irrigation added, modelled",
                   value: result ? result.irrigation.toFixed(1) + " mm this hour" : "-" };
        default:
          return null;
      }
    }

    function cellMarkup(cell, id) {
      if (!cell) { return ""; }
      var bar = "";
      if (cell.bar !== null && cell.bar !== undefined) {
        var mark = cell.mark === undefined ? null : cell.mark;
        bar = '<span class="bar ' + (cell.tone || "") + '">' +
          '<span class="bar-fill" style="transform:scaleX(' + cell.bar.toFixed(4) + ')"></span>' +
          (mark === null ? "" : '<span class="bar-mark" style="left:' +
            (mark * 100).toFixed(2) + '%"></span>') + '</span>';
      }
      return '<div class="cell' + (cell.wide ? " wide" : "") + '" data-metric="' + id + '">' +
        '<span class="cell-label">' + escape(cell.label) + '</span>' +
        '<span class="cell-value">' + escape(cell.value) + '</span>' + bar + '</div>';
    }

    /* ------------------------------------------------------------ the overview */

    function renderOverview() {
      var grid = $("zone-grid");
      var zones = activeZones();
      if (!zones.length) {
        grid.innerHTML = '<p class="empty">No zone is configured. Add one in the configuration workspace below.</p>';
        return;
      }
      grid.innerHTML = zones.map(function (zone) {
        var status = statusOf(zone);
        var badge = STATUS[status];
        var cells = zone.review_profile.map(function (id) {
          return cellMarkup(metricCell(zone, id), id);
        }).join("");
        return '<article class="zone-card" role="listitem" data-zone="' + zone.letter +
            '" data-status="' + status + '"' +
            (state.selected === zone.letter ? ' data-selected="true"' : "") + '>' +
          '<button type="button" class="zone-head" data-select="' + zone.letter + '">' +
            '<span class="zone-letter">' + zone.letter + '</span>' +
            '<span class="zone-titles">' +
              '<strong>' + escape(zone.name) + '</strong>' +
              (zone.crop_name === zone.name ? ""
                : '<span class="zone-crop">' + escape(zone.crop_name) + '</span>') +
            '</span>' +
            '<span class="status">' + glyph(badge.glyph) + escape(badge.word) + '</span>' +
          '</button>' +
          '<p class="status-note">' + escape(statusNote(zone, status)) + '</p>' +
          '<div class="cells">' + cells + '</div>' +
          '<p class="origin">' + (zone.source === "committed"
            ? "Simulated hours carried from the committed run"
            : "Simulated in this browser from the same rules and weather") +
            (zone.persisted ? "" : ". Configuration is held in this session only") + '</p>' +
        '</article>';
      }).join("");

      Array.prototype.forEach.call(grid.querySelectorAll("[data-select]"), function (button) {
        button.addEventListener("click", function () {
          select(button.getAttribute("data-select"), true);
        });
      });
    }

    /* ------------------------------------------------------------ the inspector */

    function renderInspector() {
      var body = $("inspector-body");
      var zone = zoneOf(state.selected);
      $("inspector-focus").disabled = !zone;
      if (!zone) {
        $("inspector-sub").textContent = "Choose a zone on the roof or in the overview.";
        body.innerHTML = '<p class="empty">Nothing is selected. Select a roof zone or an overview card, or press 1 to ' +
          activeZones().length + ' with the model focused.</p>';
        return;
      }
      var result = resultAt(zone, state.hour);
      var status = statusOf(zone);
      $("inspector-sub").textContent = "Zone " + zone.letter + ", " + zone.name +
        ", at " + hourText(state.hour) + " simulated local time.";

      var held = zone.overrides[zone.overrides.length - 1] || null;
      var history = transitions(zone).filter(function (item) { return item.hour <= state.hour; })
        .slice(-5).reverse();

      body.innerHTML = '' +
        '<div class="why" data-status="' + status + '">' +
          '<h3>Why this decision?</h3>' +
          '<p class="why-lead">' + escape(result ? Rules.reasonText(zone, result) : "No modelled result yet.") + '</p>' +
          (result && result.conflict
            ? '<p class="blocked">' + glyph(STATUS.conflict.glyph) +
              'The manual command was refused for this hour. ' +
              escape(Rules.reasonText(zone, result)) +
              ' A safety rule outranks a manual command, so the modelled roof stayed closed.</p>'
            : "") +
        '</div>' +
        '<dl class="facts">' +
          fact("Automatic rain policy", zone.rain_ok
            ? "May admit rain when modelled soil is below the request threshold"
            : "Never admits rain") +
          fact(zone.light_rule === "dli" ? "Daily light target" : "Heat shade rule",
            zone.light_rule === "dli"
              ? zone.light_target.toFixed(1) + " mol m⁻² d⁻¹, modelled"
              : "Part folds to " + Math.round(constants.HEAT_SHADE_OPEN * 100) +
                "% above " + constants.HEAT_SHADE_C + " °C, modelled") +
          fact("Soil rain request threshold",
            zone.soil_request_below_mm.toFixed(0) + " mm modelled, of " +
            constants.SOIL_CAPACITY.toFixed(0) + " mm capacity") +
          fact("Current roof command", positionText(result) +
            (result ? ", actuation " + result.open.toFixed(2) : "")) +
          fact("Configuration revision", String(zone.revision) +
            (zone.persisted ? ", stored" : ", this session only")) +
        '</dl>' +
        '<div class="history">' +
          '<h3>Decision history</h3>' +
          (history.length
            ? '<ol>' + history.map(function (item) {
                return '<li><span>' + hourText(item.hour) + '</span> ' +
                  escape(positionText(item.result)) + '. ' +
                  escape(Rules.reasonText(zone, item.result)) + '</li>';
              }).join("") + '</ol>'
            : '<p class="empty">No modelled roof change before this hour.</p>') +
        '</div>' +
        '<div class="manual" data-open="' + (held ? "true" : "false") + '">' +
          '<h3>Manual override</h3>' +
          (held
            ? '<p class="held">' + glyph(STATUS.manual.glyph) + 'Held ' + escape(held.command) +
              ' from ' + hourText(held.from_hour) + ' until ' +
              (held.until_hour >= 24 ? "the end of the simulated day" : hourText(held.until_hour)) +
              '.</p><button type="button" class="btn accent" id="return-auto">Return to automatic</button>'
            : '<div class="override-form">' +
                '<p class="field"><label for="override-command">Roof command</label>' +
                  '<select id="override-command">' +
                    '<option value="open">Hold the roof open</option>' +
                    '<option value="closed">Hold the roof closed</option>' +
                  '</select></p>' +
                '<p class="field"><label for="override-duration">Override duration</label>' +
                  '<select id="override-duration">' +
                    '<option value="one_hour">One simulated hour</option>' +
                    '<option value="end_of_day">Until the simulated day ends</option>' +
                  '</select></p>' +
                '<div class="review" id="override-review" hidden></div>' +
                '<div class="form-actions">' +
                  '<button type="button" class="btn" id="override-review-btn">Review the override</button>' +
                  '<button type="button" class="btn accent" id="override-apply" hidden>Apply the override</button>' +
                '</div>' +
              '</div>') +
        '</div>';

      if (held) {
        $("return-auto").addEventListener("click", function () { returnToAutomatic(zone); });
      } else {
        $("override-review-btn").addEventListener("click", function () { reviewOverride(zone); });
        $("override-apply").addEventListener("click", function () { applyOverride(zone); });
      }
    }

    function fact(term, value) {
      return '<div><dt>' + escape(term) + '</dt><dd>' + escape(value) + '</dd></div>';
    }

    /* ------------------------------------------------------------ overrides */

    function overridePlan(zone) {
      var command = $("override-command").value;
      var duration = $("override-duration").value;
      var until = duration === "one_hour" ? Math.min(24, state.hour + 1) : 24;
      var trial = Rules.runZone(constants, zone, hours,
        [{ command: command, from_hour: state.hour, until_hour: until }]);
      return { command: command, duration: duration, until: until, trial: trial };
    }

    function reviewOverride(zone) {
      stopPlayback();
      var plan = overridePlan(zone);
      var atHour = plan.trial[state.hour];
      var blocked = atHour.conflict;
      $("override-review").hidden = false;
      $("override-review").innerHTML = '<h4>Review before applying</h4>' +
        '<ul>' +
          '<li>Zone ' + zone.letter + ' is held <strong>' + escape(plan.command) +
            '</strong> from ' + hourText(state.hour) + '.</li>' +
          '<li>It expires at ' + (plan.until >= 24
            ? "the end of the simulated day" : hourText(plan.until)) +
            ' and returns to automatic control by itself.</li>' +
          '<li>Simulated hours before ' + hourText(state.hour) +
            ' and every earlier simulation run stay unchanged.</li>' +
          (blocked
            ? '<li class="blocked-line">' + glyph(STATUS.conflict.glyph) +
              'A safety rule refuses this command at ' + hourText(state.hour) + '. ' +
              escape(Rules.reasonText(zone, atHour)) +
              ' The override can still be recorded, and the modelled roof will stay closed.</li>'
            : "") +
        '</ul>';
      $("override-apply").hidden = false;
      announce("Override for zone " + zone.letter + " ready to review.");
    }

    function applyOverride(zone) {
      var plan = overridePlan(zone);
      zone.overrides = [{
        command: plan.command, from_hour: state.hour, until_hour: plan.until
      }];
      recompute();
      render();
      announce("Zone " + zone.letter + " held " + plan.command + " from " + hourText(state.hour) +
        ", expiring at " + (plan.until >= 24 ? "the end of the day" : hourText(plan.until)) + ".");
      if (state.store.online && zone.id) {
        root.Api.override(zone.id, {
          command: plan.command, duration: plan.duration, from_hour: state.hour,
          acknowledged_review: true
        }, zone.letter + "-" + state.hour + "-" + plan.command)
          .catch(function (error) { storeProblem(error); });
      }
    }

    function returnToAutomatic(zone) {
      zone.overrides = [];
      recompute();
      render();
      announce("Zone " + zone.letter + " returned to automatic control at " + hourText(state.hour) + ".");
      if (state.store.online && zone.id) {
        root.Api.returnToAutomatic(zone.id, state.hour)
          .catch(function (error) { storeProblem(error); });
      }
    }

    /* ------------------------------------------------------------ the workspace */

    function renderWorkspace() {
      var admin = $("zone-admin");
      admin.innerHTML = state.zones.map(function (zone) {
        return '<div class="admin-row' + (zone.archived ? " archived" : "") + '">' +
          '<span class="zone-letter small">' + zone.letter + '</span>' +
          '<span class="admin-title"><strong>' + escape(zone.name) + '</strong>' +
            '<span>' + escape(zone.crop_name) + ', ' +
            (zone.light_rule === "dli"
              ? "daily light " + zone.light_target.toFixed(1)
              : "heat shade " + Math.round(zone.light_target * 100) + "%") +
            ', rain ' + (zone.rain_ok ? "allowed" : "excluded") +
            ', revision ' + zone.revision + '</span></span>' +
          '<span class="admin-actions">' +
            (zone.archived
              ? '<button type="button" class="btn-quiet" data-restore="' + zone.letter + '">Restore</button>'
              : '<button type="button" class="btn-quiet" data-edit="' + zone.letter + '">Edit</button>' +
                '<button type="button" class="btn-quiet" data-archive="' + zone.letter + '">Archive</button>') +
          '</span>' +
        '</div>';
      }).join("");

      Array.prototype.forEach.call(admin.querySelectorAll("[data-edit]"), function (button) {
        button.addEventListener("click", function () { openZoneForm(button.getAttribute("data-edit")); });
      });
      Array.prototype.forEach.call(admin.querySelectorAll("[data-archive]"), function (button) {
        button.addEventListener("click", function () { archiveZone(button.getAttribute("data-archive")); });
      });
      Array.prototype.forEach.call(admin.querySelectorAll("[data-restore]"), function (button) {
        button.addEventListener("click", function () { restoreZone(button.getAttribute("data-restore")); });
      });

      var full = activeZones().length >= MAX_ZONES;
      $("add-zone").disabled = full;
      $("add-zone-note").textContent = full
        ? "The modelled roof carries " + MAX_ZONES + " zones. Archive one to add another. " +
          "Archiving keeps every earlier simulation run readable."
        : activeZones().length + " of " + MAX_ZONES + " zones are active.";
      $("add-zone-note").classList.toggle("is-limit", full);
    }

    function renderMetrics() {
      var zone = zoneOf(state.selected) || activeZones()[0];
      var list = $("metric-list");
      if (!zone) {
        list.innerHTML = '<li class="empty">Add a zone before choosing what to review.</li>';
        return;
      }
      $("metrics-lead").textContent = "Choose what the overview reviews for zone " +
        zone.letter + ", " + zone.name + ", and put it in the order you read it. " +
        "The list is a fixed registry, not a formula.";
      var chosen = state.metricDraft || zone.review_profile.slice();
      state.metricDraft = chosen;
      var ordered = chosen.concat(state.metrics.filter(function (metric) {
        return chosen.indexOf(metric.id) < 0;
      }).map(function (metric) { return metric.id; }));

      list.innerHTML = ordered.map(function (id, index) {
        var metric = state.metrics.filter(function (item) { return item.id === id; })[0];
        if (!metric) { return ""; }
        var on = chosen.indexOf(id) >= 0;
        var position = chosen.indexOf(id);
        return '<li class="metric-row' + (on ? " on" : "") + '">' +
          '<label><input type="checkbox" data-metric="' + id + '"' + (on ? " checked" : "") +
            (metric.removable === false ? " disabled" : "") + '>' +
            escape(metric.label) +
            (metric.removable === false ? ' <span class="pill">always shown</span>' : "") +
          '</label>' +
          '<span class="order">' +
            '<button type="button" data-up="' + id + '" aria-label="Move ' + escape(metric.label) +
              ' earlier"' + (!on || position <= 0 ? " disabled" : "") + '>Up</button>' +
            '<button type="button" data-down="' + id + '" aria-label="Move ' + escape(metric.label) +
              ' later"' + (!on || position < 0 || position >= chosen.length - 1 ? " disabled" : "") +
              '>Down</button>' +
          '</span>' +
        '</li>';
      }).join("");

      Array.prototype.forEach.call(list.querySelectorAll("[data-metric]"), function (box) {
        box.addEventListener("change", function () {
          var id = box.getAttribute("data-metric");
          var at = state.metricDraft.indexOf(id);
          if (box.checked && at < 0) { state.metricDraft.push(id); }
          if (!box.checked && at >= 0) { state.metricDraft.splice(at, 1); }
          renderMetrics();
        });
      });
      Array.prototype.forEach.call(list.querySelectorAll("[data-up]"), function (button) {
        button.addEventListener("click", function () { moveMetric(button.getAttribute("data-up"), -1); });
      });
      Array.prototype.forEach.call(list.querySelectorAll("[data-down]"), function (button) {
        button.addEventListener("click", function () { moveMetric(button.getAttribute("data-down"), 1); });
      });
    }

    function moveMetric(id, delta) {
      var at = state.metricDraft.indexOf(id);
      var to = at + delta;
      if (at < 0 || to < 0 || to >= state.metricDraft.length) { return; }
      state.metricDraft.splice(to, 0, state.metricDraft.splice(at, 1)[0]);
      renderMetrics();
      announce("Moved " + id.replace(/_/g, " ") + " to position " + (to + 1) + ".");
    }

    function applyMetrics() {
      var zone = zoneOf(state.selected) || activeZones()[0];
      if (!zone) { return; }
      var required = state.metrics.filter(function (metric) { return metric.removable === false; })
        .map(function (metric) { return metric.id; });
      var missing = required.filter(function (id) { return state.metricDraft.indexOf(id) < 0; });
      if (missing.length) {
        showError("metric-error",
          "The overview must keep the roof position, the control state, and the decision reason.");
        return;
      }
      hideError("metric-error");
      zone.review_profile = state.metricDraft.slice();
      render();
      announce("Zone " + zone.letter + " overview now reviews " +
        zone.review_profile.length + " metrics.");
      if (state.store.online && zone.id) {
        root.Api.reviewProfile(zone.id, zone.review_profile)
          .catch(function (error) { storeProblem(error); });
      }
    }

    /* ------------------------------------------------------------ the zone form */

    function openZoneForm(letter) {
      stopPlayback();
      var zone = letter ? zoneOf(letter) : null;
      state.draft = {
        letter: letter,
        creating: !zone,
        before: zone ? Object.assign({}, zone) : null
      };
      $("zone-form").hidden = false;
      $("zone-form-title").textContent = zone
        ? "Zone " + zone.letter + " settings, simulated"
        : "New zone, simulated";
      $("zone-form-lead").textContent = zone
        ? "Applying writes revision " + (zone.revision + 1) +
          ". Earlier revisions and earlier simulation runs are not rewritten."
        : "A new zone is modelled in this browser from the same rules and the same historical weather.";
      $("field-name").value = zone ? zone.name : "";
      $("field-crop").value = zone ? zone.crop_name : "";
      $("field-rule").value = zone ? zone.light_rule : "dli";
      $("field-target").value = zone ? zone.light_target : 10;
      $("field-soil").value = zone ? zone.soil_request_below_mm : constants.SOIL_DRY_BELOW;
      $("field-rain").checked = zone ? zone.rain_ok : true;
      syncRuleLabel();
      $("zone-review").hidden = true;
      $("zone-apply").hidden = true;
      hideError("zone-form-error");
      $("field-name").focus();
    }

    function syncRuleLabel() {
      var dli = $("field-rule").value === "dli";
      $("field-target-label").textContent = dli
        ? "Daily light target, mol m⁻² d⁻¹ modelled"
        : "Shade share when the heat rule applies, 0 to 1";
      $("field-target").max = dli ? 80 : 1;
      $("field-target").step = dli ? 0.5 : 0.05;
    }

    function readZoneForm() {
      var name = $("field-name").value.trim();
      var crop = $("field-crop").value.trim() || name;
      var rule = $("field-rule").value;
      var target = Number($("field-target").value);
      var soil = Number($("field-soil").value);
      var problems = [];
      if (!name) { problems.push("Give the zone a name."); }
      if (name.length > 60) { problems.push("Keep the zone name under 60 characters."); }
      if (!isFinite(target) || target < 0) { problems.push("The light target must be zero or more."); }
      if (rule === "dli" && target > 80) { problems.push("The daily light target must be 80 or less."); }
      if (rule === "shade_pct" && target > 1) { problems.push("The shade share must be 1 or less."); }
      if (!isFinite(soil) || soil < 0 || soil > constants.SOIL_CAPACITY) {
        problems.push("The soil threshold must be between 0 and " +
          constants.SOIL_CAPACITY.toFixed(0) + " mm.");
      }
      return {
        name: name, crop_name: crop, light_rule: rule, light_target: target,
        soil_request_below_mm: soil, rain_ok: $("field-rain").checked, problems: problems
      };
    }

    function reviewZoneForm() {
      var wanted = readZoneForm();
      if (wanted.problems.length) {
        showError("zone-form-error", wanted.problems.join(" "));
        $("zone-apply").hidden = true;
        $("zone-review").hidden = true;
        return;
      }
      hideError("zone-form-error");
      var zone = state.draft.letter ? zoneOf(state.draft.letter) : null;
      var lines = [];
      if (zone) {
        [["name", "Name"], ["crop_name", "Crop"], ["light_rule", "Light rule"],
         ["light_target", "Light target"], ["soil_request_below_mm", "Soil threshold"],
         ["rain_ok", "Rain policy"]].forEach(function (pair) {
          if (String(zone[pair[0]]) !== String(wanted[pair[0]])) {
            lines.push(pair[1] + ": " + String(zone[pair[0]]) + " becomes " + String(wanted[pair[0]]));
          }
        });
        if (!lines.length) { lines.push("Nothing changes."); }
        lines.push("This writes revision " + (zone.revision + 1) + ".");
      } else {
        lines.push("A new zone " + nextLetter() + ", " + wanted.name + ", is added.");
        lines.push("It starts at the modelled soil capacity and is simulated in this browser.");
      }

      var preview = previewZone(wanted, zone);
      lines.push("At " + hourText(state.hour) + " the modelled roof would read " +
        positionText(preview[state.hour]).toLowerCase() + ".");
      lines.push("Earlier simulation runs keep the revision they were run with.");

      $("zone-review-list").innerHTML = lines.map(function (line) {
        return "<li>" + escape(line) + "</li>";
      }).join("");
      $("zone-review").hidden = false;
      $("zone-apply").hidden = false;
    }

    function previewZone(wanted, zone) {
      return Rules.runZone(constants, {
        light_rule: wanted.light_rule,
        light_target: wanted.light_target,
        soil_request_below_mm: wanted.soil_request_below_mm,
        rain_ok: wanted.rain_ok,
        kc: zone ? zone.kc : 1.0,
        soil_start: zone ? zone.soil_start : constants.SOIL_START
      }, hours, zone ? zone.overrides : []);
    }

    function nextLetter() {
      var taken = activeZones().map(function (zone) { return zone.letter; });
      for (var index = 0; index < LETTERS.length; index++) {
        if (taken.indexOf(LETTERS[index]) < 0) { return LETTERS[index]; }
      }
      return null;
    }

    function applyZoneForm() {
      var wanted = readZoneForm();
      if (wanted.problems.length) {
        showError("zone-form-error", wanted.problems.join(" "));
        return;
      }
      var zone = state.draft.letter ? zoneOf(state.draft.letter) : null;

      if (zone) {
        Object.assign(zone, {
          name: wanted.name, crop_name: wanted.crop_name, light_rule: wanted.light_rule,
          light_target: wanted.light_target,
          soil_request_below_mm: wanted.soil_request_below_mm, rain_ok: wanted.rain_ok,
          revision: zone.revision + 1
        });
        recompute();
        closeZoneForm();
        render();
        announce("Zone " + zone.letter + " saved as revision " + zone.revision + ".");
        if (state.store.online && zone.id) {
          root.Api.patchZone(zone.id, {
            expected_revision: zone.revision - 1,
            name: wanted.name, crop_name: wanted.crop_name, light_rule: wanted.light_rule,
            light_target: wanted.light_target,
            soil_request_below_mm: wanted.soil_request_below_mm, rain_ok: wanted.rain_ok
          }).then(function (payload) {
            zone.revision = payload.zone.revision;
            zone.resultsRevision = zone.revision;
            zone.persisted = true;
            render();
          }).catch(function (error) { storeProblem(error, zone); });
        }
        return;
      }

      var letter = nextLetter();
      if (!letter) {
        showError("zone-form-error",
          "The modelled roof carries " + MAX_ZONES + " zones. Archive one to add another.");
        return;
      }
      var added = {
        letter: letter, id: null, persisted: false, revision: 1, resultsRevision: 1,
        name: wanted.name, crop_name: wanted.crop_name, botanical: "",
        light_rule: wanted.light_rule, light_target: wanted.light_target,
        soil_request_below_mm: wanted.soil_request_below_mm, rain_ok: wanted.rain_ok,
        kc: 1.0, soil_start: constants.SOIL_START, note: "", archived: false,
        origin: "grower", review_profile: DEFAULT_PROFILE.slice(), overrides: [],
        baseline: null, results: null
      };
      state.zones.push(added);
      state.zones.sort(function (a, b) { return a.letter < b.letter ? -1 : 1; });
      recompute();
      closeZoneForm();
      select(letter, false);
      render();
      announce("Zone " + letter + ", " + added.name + ", added and simulated.");
      if (state.store.online) {
        root.Api.addZone(SITE, {
          name: wanted.name, crop_name: wanted.crop_name, light_rule: wanted.light_rule,
          light_target: wanted.light_target,
          soil_request_below_mm: wanted.soil_request_below_mm, rain_ok: wanted.rain_ok, kc: 1.0
        }).then(function (payload) {
          added.id = payload.zone.id;
          added.persisted = true;
          added.revision = payload.zone.revision;
          added.resultsRevision = added.revision;
          render();
        }).catch(function (error) { storeProblem(error, added); });
      }
    }

    function closeZoneForm() {
      $("zone-form").hidden = true;
      state.draft = null;
    }

    function archiveZone(letter) {
      var zone = zoneOf(letter);
      if (!zone) { return; }
      zone.archived = true;
      zone.overrides = [];
      if (state.selected === letter) { select(activeZones().length ? activeZones()[0].letter : null, false); }
      recompute();
      render();
      announce("Zone " + letter + " archived. Earlier simulation runs keep it.");
      if (state.store.online && zone.id) {
        root.Api.archiveZone(zone.id).catch(function (error) { storeProblem(error, zone); });
      }
    }

    function restoreZone(letter) {
      var zone = zoneOf(letter);
      if (!zone) { return; }
      if (activeZones().length >= MAX_ZONES) {
        announce("The modelled roof already carries " + MAX_ZONES + " zones. Archive one to restore this.");
        $("add-zone-note").textContent =
          "The modelled roof carries " + MAX_ZONES + " zones. Archive one before restoring zone " +
          letter + ".";
        $("add-zone-note").classList.add("is-limit");
        return;
      }
      zone.archived = false;
      recompute();
      render();
      announce("Zone " + letter + " restored.");
      if (state.store.online && zone.id) {
        root.Api.restoreZone(zone.id).catch(function (error) { storeProblem(error, zone); });
      }
    }

    /* ------------------------------------------------------------ errors */

    function showError(id, message) {
      var node = document.getElementById(id);
      node.textContent = message;
      node.hidden = false;
    }

    function hideError(id) {
      var node = document.getElementById(id);
      node.hidden = true;
      node.textContent = "";
    }

    function storeProblem(error, zone) {
      state.store.online = false;
      state.store.message = error && error.code === "offline"
        ? "Offline. Changes are held in this session only."
        : "The service refused the change: " + ((error && error.message) || "unknown reason");
      if (zone) { zone.persisted = false; }
      if (error && error.code === "revision_conflict" && zone) {
        showError("zone-form-error",
          "This zone changed elsewhere. Reload the stored configuration and review the change again.");
      }
      renderStoreState();
      render();
    }

    function renderStoreState() {
      var chip = $("store-state");
      var online = state.store.online;
      chip.setAttribute("data-state", !state.store.checked ? "loading" : online ? "ok" : "offline");
      chip.querySelector("span").textContent = !state.store.checked
        ? "Checking stored configuration"
        : online ? "Configuration stored" : state.store.message;
    }

    /* ------------------------------------------------------------ the timeline */

    function renderTimeline() {
      var weather = hours[state.hour];
      $("time-control").value = String(state.hour);
      $("clock").textContent = hourText(weather.local_hour);
      $("sky-readout").textContent = "Modelled sun " + weather.ghi.toFixed(0) +
        " W m⁻², rain " + weather.rain_mm.toFixed(1) + " mm, air " +
        weather.t2m.toFixed(1) + " °C";
      $("timeline-readout").textContent = "Historical input " + day.date_local + " " +
        hourText(weather.local_hour) + " local. Modelled sun " + weather.ghi.toFixed(0) +
        " W m⁻², rain " + weather.rain_mm.toFixed(1) + " mm, air " +
        weather.t2m.toFixed(1) + " °C.";

      var chip = $("run-state");
      var worst = activeZones().reduce(function (carry, zone) {
        var status = statusOf(zone);
        var rank = { conflict: 5, offline: 4, stale: 3, manual: 2, warning: 1, auto: 0 };
        return rank[status] > rank[carry] ? status : carry;
      }, "auto");
      if (!activeZones().length) {
        chip.setAttribute("data-state", "empty");
        chip.querySelector("span").textContent = "No simulated result yet, no zone is configured";
      } else if (state.playing) {
        chip.setAttribute("data-state", "running");
        chip.querySelector("span").textContent = "Simulated day running";
      } else {
        chip.setAttribute("data-state", worst);
        chip.querySelector("span").textContent = worst === "auto"
          ? "Every zone on automatic control"
          : STATUS[worst].word + " in at least one zone";
      }
    }

    function buildMarks() {
      var storm = hours.map(function (hour, index) { return hour.rain_mm > 0 ? index : -1; })
        .filter(function (index) { return index >= 0; });
      var marks = [{ at: 0, text: "00" }, { at: 6, text: "06" }, { at: 12, text: "12" },
                   { at: 18, text: "18" }, { at: 23, text: "23" }];
      if (storm.length) {
        marks.push({ at: storm[0], text: hourText(storm[0]) + " storm", strong: true });
      }
      $("timeline-marks").innerHTML = marks.map(function (mark) {
        return '<span' + (mark.strong ? ' class="strong"' : "") + ' style="left:' +
          (mark.at / 23 * 100).toFixed(2) + '%">' + escape(mark.text) + "</span>";
      }).join("");
      if (storm.length) {
        $("jump-storm").textContent = "Go to the storm at " + hourText(storm[0]);
        $("jump-storm").disabled = false;
        $("jump-storm").addEventListener("click", function () {
          stopPlayback();
          setHour(storm[0]);
          announce("Moved to the modelled storm at " + hourText(storm[0]) + ".");
        });
      }
    }

    /* ------------------------------------------------------------ playback */

    function setHour(value) {
      state.hour = clamp(value, 0, hours.length - 1);
      render();
    }

    function step() {
      if (state.hour >= hours.length - 1) {
        stopPlayback();
        announce("The simulated day is complete.");
        return;
      }
      setHour(state.hour + 1);
      state.timer = setTimeout(step, hours[state.hour].play_seconds * 1000);
    }

    function stopPlayback() {
      state.playing = false;
      if (state.timer !== null) { clearTimeout(state.timer); }
      state.timer = null;
      $("play-label").textContent = state.hour >= hours.length - 1
        ? "Run the simulated day again" : "Run the simulated day";
      renderTimeline();
    }

    function play() {
      if (state.playing) {
        stopPlayback();
        announce("Simulated day paused at " + hourText(state.hour) + ".");
        return;
      }
      if (state.hour >= hours.length - 1) { setHour(0); }
      state.playing = true;
      $("play-label").textContent = "Pause";
      announce("Simulated day running from " + hourText(state.hour) + ".");
      renderTimeline();
      state.timer = setTimeout(step, hours[state.hour].play_seconds * 1000);
    }

    function restoreBaseline() {
      stopPlayback();
      state.zones.forEach(function (zone) { zone.overrides = []; });
      recompute();
      setHour(0);
      announce("Baseline restored. Every zone is on automatic control at 00:00.");
    }

    /* ------------------------------------------------------------ selection */

    function select(letter, focusRoof, quiet) {
      state.selected = letter;
      scene.setSelected(letter);
      if (letter && focusRoof) { scene.focusZone(letter); }
      render();
      /* Start-up selects a zone too, and that must never scroll the page off its top. */
      if (letter && !quiet) {
        var card = document.querySelector('.zone-card[data-zone="' + letter + '"]');
        if (card && card.scrollIntoView) { card.scrollIntoView({ block: "nearest" }); }
      }
    }

    function announce(message) {
      $("announce").textContent = message;
    }

    /* ------------------------------------------------------------ rendering */

    function sceneZones() {
      return activeZones().map(function (zone) {
        var result = resultAt(zone, state.hour);
        var status = statusOf(zone);
        return {
          letter: zone.letter,
          actuation: result ? result.open : 0,
          admittingRain: !!(result && result.rainIn > 0),
          manual: status === "manual",
          conflict: status === "conflict",
          stale: status === "stale",
          offline: status === "offline"
        };
      });
    }

    var lastRoofSignature = "";

    function render() {
      renderOverview();
      renderInspector();
      renderTimeline();
      renderWorkspace();
      renderMetrics();
      renderStoreState();
      $("restore").hidden = !state.zones.some(function (zone) { return zone.overrides.length; });

      var signature = activeZones().map(function (zone) { return zone.letter; }).join("");
      if (signature !== lastRoofSignature) {
        scene.setZones(sceneZones());
        lastRoofSignature = signature;
      } else {
        scene.updateZones(sceneZones());
      }
      options.onRender(state);

      if (hours[state.hour].rain_mm > 0 && state.announced !== state.hour) {
        var words = activeZones().map(function (zone) {
          var result = resultAt(zone, state.hour);
          return "zone " + zone.letter + " " +
            (result && result.rainIn > 0 ? "admits the rain" : "excludes it");
        }).join(", ");
        announce("Modelled storm hour " + hourText(state.hour) + ". " + words + ".");
      }
      state.announced = state.hour;
    }

    /* ------------------------------------------------------------ wiring */

    function bind() {
      $("play").addEventListener("click", play);
      $("restore").addEventListener("click", restoreBaseline);
      $("time-control").addEventListener("input", function (event) {
        /* Read the wanted hour before stopping: stopping re-renders the timeline and
           would rewrite this control from the hour we are leaving. */
        var wanted = Number(event.target.value);
        stopPlayback();
        setHour(wanted);
      });
      $("inspector-focus").addEventListener("click", function () {
        if (state.selected) { scene.focusZone(state.selected); }
      });
      $("add-zone").addEventListener("click", function () { openZoneForm(null); });
      $("zone-cancel").addEventListener("click", function () {
        closeZoneForm();
        announce("Zone changes discarded.");
      });
      $("zone-review-btn").addEventListener("click", reviewZoneForm);
      $("zone-apply").addEventListener("click", applyZoneForm);
      $("field-rule").addEventListener("change", syncRuleLabel);
      $("metrics-apply").addEventListener("click", applyMetrics);
      $("metrics-reset").addEventListener("click", function () {
        state.metricDraft = DEFAULT_PROFILE.slice();
        renderMetrics();
        announce("Metric order restored to the default.");
      });

      ["zones", "metrics"].forEach(function (name) {
        $("tab-" + name).addEventListener("click", function () {
          ["zones", "metrics"].forEach(function (other) {
            var selected = other === name;
            $("tab-" + other).setAttribute("aria-selected", selected ? "true" : "false");
            $("pane-" + other).hidden = !selected;
          });
        });
      });

      document.addEventListener("keydown", function (event) {
        /* The model handles its own arrow keys and calls preventDefault, so a key it
           has already used must not also scrub the timeline. */
        if (event.defaultPrevented) { return; }
        var tag = document.activeElement && document.activeElement.tagName;
        if (tag === "INPUT" || tag === "SELECT" || tag === "TEXTAREA") { return; }
        if (event.key === " " && tag !== "BUTTON") { play(); event.preventDefault(); }
        else if (event.key.toLowerCase() === "r" && !event.metaKey && !event.ctrlKey) {
          restoreBaseline();
        } else if (event.key === "ArrowLeft" && tag !== "BUTTON") {
          stopPlayback(); setHour(state.hour - 1); event.preventDefault();
        } else if (event.key === "ArrowRight" && tag !== "BUTTON") {
          stopPlayback(); setHour(state.hour + 1); event.preventDefault();
        }
      });
    }

    /* ------------------------------------------------------------ boot */

    function boot(payload) {
      day = payload;
      constants = day.constants;
      hours = day.hours;
      state.zones = day.zones.map(function (source) { return zoneFrom(source, source.zone); });
      recompute();
      buildMarks();
      bind();
      $("play").disabled = false;
      setHour(0);
      /* No zone is chosen at start-up, so every card opens at the same size. */
      select(null, false, true);
    }

    function adoptStored(payload) {
      state.store.online = true;
      state.store.checked = true;
      state.store.message = "Configuration stored";
      payload.zones.forEach(function (stored) {
        var zone = zoneOf(stored.letter);
        if (!zone) { return; }
        zone.id = stored.id;
        zone.persisted = true;
        zone.revision = stored.revision;
        zone.resultsRevision = stored.revision;
        zone.name = stored.config.name;
        zone.crop_name = stored.config.crop_name;
        zone.light_rule = stored.config.light_rule;
        zone.light_target = stored.config.light_target;
        zone.soil_request_below_mm = stored.config.soil_request_below_mm;
        zone.rain_ok = stored.config.rain_ok;
        zone.kc = stored.config.kc;
        zone.archived = stored.archived;
        zone.review_profile = stored.review_profile.slice();
      });
      state.metricDraft = null;
      recompute();
      render();
    }

    function offlineStore(message) {
      state.store.online = false;
      state.store.checked = true;
      state.store.message = message ||
        "Offline. The historical demonstration runs; configuration is session only.";
      renderStoreState();
      render();
    }

    return {
      boot: boot,
      adoptStored: adoptStored,
      offlineStore: offlineStore,
      setMetricRegistry: function (list) {
        state.metrics = list.map(function (item) {
          return { id: item.id, label: item.label, removable: item.removable };
        });
        renderMetrics();
      },
      state: state,
      select: select,
      hour: function () { return state.hour; },
      hoursData: function () { return hours; },
      announce: announce,
      render: render
    };
  }

  root.Console = { create: create, METRICS: METRICS, DEFAULT_PROFILE: DEFAULT_PROFILE };
}(typeof self !== "undefined" ? self : this));
