/* The client for the persistent zone backend.

   The console never depends on it. The historical demonstration is driven entirely by
   day.json, which is a static file, so the page runs with no server, no network, and
   no API. What the backend adds is persistence: zones, revisions, review profiles,
   overrides, and run records that outlive a reload.

   When the API cannot be reached the client says so once and the console shows an
   explicit offline state. It never retries in a loop and never blocks a render.
*/

(function (root) {
  "use strict";

  var BASE = "/api";
  var TIMEOUT_MS = 2500;

  function request(method, path, body, headers) {
    var controller = typeof AbortController === "function" ? new AbortController() : null;
    var timer = controller ? setTimeout(function () { controller.abort(); }, TIMEOUT_MS) : null;
    var options = {
      method: method,
      headers: Object.assign({ "Content-Type": "application/json" }, headers || {}),
      signal: controller ? controller.signal : undefined
    };
    if (body !== undefined && body !== null) { options.body = JSON.stringify(body); }

    return fetch(BASE + path, options).then(function (response) {
      if (timer) { clearTimeout(timer); }
      return response.text().then(function (text) {
        var parsed = null;
        try { parsed = text ? JSON.parse(text) : null; } catch (error) { parsed = null; }
        if (!response.ok) {
          var problem = (parsed && parsed.error) || {
            code: "unreachable", message: "The service returned " + response.status + "."
          };
          problem.status = response.status;
          throw problem;
        }
        return parsed;
      });
    }, function (error) {
      if (timer) { clearTimeout(timer); }
      throw {
        code: "offline",
        message: "The configuration service could not be reached.",
        cause: error && error.name
      };
    });
  }

  root.Api = {
    health: function () { return request("GET", "/health"); },
    metricDefinitions: function () { return request("GET", "/metric-definitions"); },
    zones: function (site) { return request("GET", "/sites/" + site + "/zones"); },
    addZone: function (site, body) { return request("POST", "/sites/" + site + "/zones", body); },
    patchZone: function (id, body) { return request("PATCH", "/zones/" + id, body); },
    archiveZone: function (id) { return request("POST", "/zones/" + id + "/archive", {}); },
    restoreZone: function (id) { return request("POST", "/zones/" + id + "/restore", {}); },
    reviewProfile: function (id, metrics) {
      return request("PUT", "/zones/" + id + "/review-profile", { metrics: metrics });
    },
    override: function (id, body, key) {
      return request("POST", "/zones/" + id + "/overrides", body,
                     key ? { "Idempotency-Key": key } : null);
    },
    returnToAutomatic: function (id, hour) {
      return request("POST", "/zones/" + id + "/return-to-automatic", { at_hour: hour });
    },
    controlEvents: function (id) { return request("GET", "/zones/" + id + "/control-events"); },
    createRun: function (note) { return request("POST", "/simulation-runs", { note: note || "" }); },
    run: function (id) { return request("GET", "/simulation-runs/" + id); }
  };
}(typeof self !== "undefined" ? self : this));
