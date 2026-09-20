/* The deterministic zone rules, in the browser.

   These are package H1's nine rules and nothing else: night, then rain with its four
   refusals, then the daily light rule or the heat shade rule. The constants arrive in
   day.json, taken from H1 itself, so this file cannot drift from the simulation even
   if someone edits a number here.

   The page needs them for two reasons the served files cannot get from H1 directly: a
   zone a grower adds has no committed baseline, and a timed manual override has to be
   answered at the hour a grower sets it. Every baseline figure the console shows for
   the three committed zones still comes from day.json, unchanged.

   No language model and no learned model is in this loop.
*/

(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) { module.exports = api; }
  root.Rules = api;
}(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var STATE_LABEL = {
    NIGHT: "Closed",
    LIGHT_OPEN: "Open",
    SHADE: "Closed",
    HEAT_SHADE: "Part folded",
    RAIN_OPEN: "Open",
    RAIN_SHUT: "Closed",
    MANUAL_OPEN: "Open",
    MANUAL_SHUT: "Closed"
  };

  var REASON_TEXT = {
    opted_out: "This crop's rain policy excludes rain, so the roof stayed closed.",
    wet_enough: "Modelled soil water is above the rain request threshold, so rain was excluded.",
    no_drying_time: "Too little modelled daylight is left for the leaves to dry, so rain was excluded.",
    hard_rain: "The hard rain safety rule applies at this modelled intensity.",
    manual_override: "A timed manual override is holding this zone."
  };

  function referenceEvaporation(constants, ghi, t2m) {
    var slope = 4098 * (0.6108 * Math.exp(17.27 * t2m / (t2m + 237.3))) /
      Math.pow(t2m + 237.3, 2);
    return constants.MAKKINK_C * slope / (slope + constants.GAMMA) *
      (ghi * 3600 / 1e6) / constants.LATENT_HEAT;
  }

  function lightForHour(constants, ghi, open) {
    return ghi * constants.K * 3600 / 1e6 * constants.T_STRUCT *
      (open + (1 - open) * constants.T_CLOSED);
  }

  /* The nine rules, in H1's order. Returns the automatic answer only. */
  function decide(constants, zone, hours, index, lightSoFar, wantRain) {
    var hour = hours[index];
    if (hour.ghi <= 0) { return { open: 0, state: "NIGHT", reason: "" }; }

    if (hour.rain_mm > 0) {
      if (!zone.rain_ok) { return { open: 0, state: "RAIN_SHUT", reason: "opted_out" }; }
      if (!wantRain) { return { open: 0, state: "RAIN_SHUT", reason: "wet_enough" }; }
      var later = index + constants.DRYING_HOURS;
      if (later >= hours.length || hours[later].ghi <= 0) {
        return { open: 0, state: "RAIN_SHUT", reason: "no_drying_time" };
      }
      if (hour.rain_mm >= constants.HARD_RAIN_MM) {
        return { open: 0, state: "RAIN_SHUT", reason: "hard_rain" };
      }
      return { open: 1, state: "RAIN_OPEN", reason: "" };
    }

    if (zone.light_rule === "dli") {
      return lightSoFar < zone.light_target
        ? { open: 1, state: "LIGHT_OPEN", reason: "" }
        : { open: 0, state: "SHADE", reason: "" };
    }

    if (hour.t2m >= constants.HEAT_SHADE_C) {
      return { open: constants.HEAT_SHADE_OPEN, state: "HEAT_SHADE", reason: "" };
    }
    return { open: 1, state: "LIGHT_OPEN", reason: "" };
  }

  function overrideAt(overrides, hour) {
    for (var index = 0; index < (overrides || []).length; index++) {
      var item = overrides[index];
      if (hour >= item.from_hour && hour < item.until_hour) { return item; }
    }
    return null;
  }

  /* One local day for one zone. The same inputs always give the same 24 hours. */
  function runZone(constants, zone, hours, overrides) {
    var soil = zone.soil_start === undefined ? constants.SOIL_START : zone.soil_start;
    var requestBelow = zone.soil_request_below_mm === undefined
      ? constants.SOIL_DRY_BELOW : zone.soil_request_below_mm;
    var light = 0;
    var wantRain = soil < requestBelow;
    var out = [];

    for (var index = 0; index < hours.length; index++) {
      var hour = hours[index];
      if (hour.local_hour === 0) { light = 0; }
      if (soil < requestBelow) { wantRain = true; }
      else if (soil >= constants.SOIL_FULL_AT) { wantRain = false; }

      var answer = decide(constants, zone, hours, index, light, wantRain);
      var conflict = false, manual = overrideAt(overrides, hour.local_hour);

      if (manual) {
        var wantsOpen = manual.command === "open";
        if (wantsOpen && hour.rain_mm >= constants.HARD_RAIN_MM) {
          answer = { open: 0, state: "RAIN_SHUT", reason: "hard_rain" };
          conflict = true;
        } else if (wantsOpen && hour.ghi <= 0) {
          answer = { open: 0, state: "NIGHT", reason: "" };
          conflict = true;
        } else {
          answer = {
            open: wantsOpen ? 1 : 0,
            state: wantsOpen ? "MANUAL_OPEN" : "MANUAL_SHUT",
            reason: "manual_override"
          };
        }
      }

      light += lightForHour(constants, hour.ghi, answer.open);
      var before = soil;
      soil = Math.min(constants.SOIL_CAPACITY, soil + hour.rain_mm * answer.open);
      var rainIn = soil - before;
      soil = Math.max(0, soil - zone.kc *
        referenceEvaporation(constants, hour.ghi, hour.t2m) * answer.open * constants.T_STRUCT);

      var irrigation = 0;
      if (soil < constants.SOIL_IRRIGATE_BELOW) {
        irrigation = constants.SOIL_FULL_AT - soil;
        soil = constants.SOIL_FULL_AT;
      }

      out.push({
        local_hour: hour.local_hour,
        open: answer.open,
        state: answer.state,
        reason: answer.reason,
        conflict: conflict,
        manual: !!manual && !conflict,
        light: light,
        soil: soil,
        rainIn: rainIn,
        irrigation: irrigation
      });
    }
    return out;
  }

  function reasonText(zone, result) {
    if (result.reason) { return REASON_TEXT[result.reason] || result.reason; }
    if (result.state === "NIGHT") { return "No modelled daylight, so the roof is closed."; }
    if (result.state === "LIGHT_OPEN") {
      return zone.light_rule === "dli"
        ? "The modelled daily light target has not been reached, so the roof is open."
        : "The crop's shade rule allows full light at this modelled temperature.";
    }
    if (result.state === "SHADE") {
      return "The modelled daily light target has been reached, so the roof closed.";
    }
    if (result.state === "HEAT_SHADE") {
      return "Modelled air temperature reached the heat shade rule, so the roof part folded.";
    }
    if (result.state === "RAIN_OPEN") {
      return "Rain is allowed here and modelled soil water requested it, so the roof opened.";
    }
    return "The deterministic zone rules set this position.";
  }

  return {
    STATE_LABEL: STATE_LABEL,
    REASON_TEXT: REASON_TEXT,
    decide: decide,
    runZone: runZone,
    overrideAt: overrideAt,
    reasonText: reasonText,
    lightForHour: lightForHour,
    referenceEvaporation: referenceEvaporation
  };
}));
