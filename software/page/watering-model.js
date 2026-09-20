/* Deterministic rain-event model. Cell-centre masks approximate circular apertures. */
(function (root) {
  "use strict";
  const EPS = 1e-9;

  function finite(value, name, minimum = 0) {
    if (typeof value !== "number" || !Number.isFinite(value) || value < minimum) {
      throw new Error(name + " must be a finite number >= " + minimum);
    }
    return value;
  }

  function footprints(layout) {
    finite(layout.width_m, "width_m", Number.EPSILON);
    finite(layout.length_m, "length_m", Number.EPSILON);
    for (const key of ["cols", "rows"]) {
      if (!Number.isInteger(layout[key]) || layout[key] < 1) {
        throw new Error(key + " must be a positive integer");
      }
    }
    if (layout.cols * layout.rows > 20000) throw new Error("Grid exceeds 20000 cells");
    if (!Array.isArray(layout.flaps)) throw new Error("flaps must be an array");
    const masks = new Map();
    for (const flap of [...layout.flaps].sort((a, b) => a.id < b.id ? -1 : a.id > b.id ? 1 : 0)) {
      if (typeof flap.id !== "string" || !flap.id.trim() || masks.has(flap.id)) {
        throw new Error("Flap IDs must be unique nonempty strings");
      }
      finite(flap.x_m, "x_m", -Number.MAX_VALUE);
      finite(flap.y_m, "y_m", -Number.MAX_VALUE);
      finite(flap.radius_m, "radius_m", Number.EPSILON);
      const cells = [];
      for (let i = 0; i < layout.cols * layout.rows; i++) {
        const x = (i % layout.cols + 0.5) * layout.width_m / layout.cols;
        const y = (Math.floor(i / layout.cols) + 0.5) * layout.length_m / layout.rows;
        if (Math.hypot(x - flap.x_m, y - flap.y_m) <= flap.radius_m) cells.push(i);
      }
      masks.set(flap.id, cells);
    }
    return masks;
  }

  function fromCAD(model, mapping) {
    if (mapping.units !== "m" || !mapping.all_occurrence_rotations_identity ||
        model.units !== "tenths of a millimetre" || model.scale !== 10) {
      throw new Error("Unsupported CAD units or occurrence rotations");
    }
    const instances = model.instances.filter(instance => instance.kind === "flap");
    if (instances.length !== mapping.flaps.length) throw new Error("CAD mapping count mismatch");
    const layout = {
      width_m: mapping.controller_bounding_rectangle_size_m[0],
      length_m: mapping.controller_bounding_rectangle_size_m[1],
      origin_m: mapping.controller_domain_origin_xy_m,
      cols: 13, rows: 30,
      source: "third.STEP — independent circular apertures; cross-layer occlusion excluded",
      source_sha256: mapping.source.sha256,
      flaps: mapping.flaps.map(flap => {
        const instance = instances.find(item => item.node === flap.id);
        if (!instance || instance.origin.some((v, i) => Math.abs(v / 10000 - flap.origin_m[i]) > 0.0001)) {
          throw new Error("CAD mapping is stale for " + flap.id);
        }
        return {id: flap.id, x_m: flap.assumed_center_xy_from_domain_origin_m[0],
          y_m: flap.assumed_center_xy_from_domain_origin_m[1], radius_m: flap.radius_m};
      }),
    };
    footprints(layout);
    return layout;
  }

  function simulate(layout, input) {
    const masks = footprints(layout), count = layout.cols * layout.rows;
    const rain = finite(input.rain_mm, "rain_mm");
    const capacity = finite(input.capacity_mm ?? 60, "capacity_mm", Number.EPSILON);
    const spill = input.spill_allowed ?? false;
    if (typeof spill !== "boolean") throw new Error("spill_allowed must be boolean");
    if (!Array.isArray(input.selected)) throw new Error("selected must be an array");
    const selected = new Set(input.selected);
    for (const id of selected) {
      if (!Number.isInteger(id) || id < 0 || id >= count) throw new Error("Invalid cell ID");
    }
    function values(value, name) {
      if (Array.isArray(value) && value.length !== count) throw new Error(name + " length mismatch");
      return Array.from({length: count}, (_, id) => {
        const v = finite(Array.isArray(value) ? value[id] : value, name);
        if (v > capacity) throw new Error(name + " exceeds soil capacity");
        return v;
      });
    }
    const soil = values(input.soil_mm ?? 0, "soil_mm");
    const target = values(input.target_mm, "target_mm");
    const initial = [...soil], delivered = Array(count).fill(0), overflow = Array(count).fill(0);
    const need = id => Math.max(0, target[id] - soil[id]);
    const eligible = cells => cells.some(id => selected.has(id) && need(id) > EPS) &&
      (spill || cells.every(id => selected.has(id) && need(id) > EPS));
    const phases = [];
    let remaining = rain;
    while (remaining > EPS) {
      const candidates = [...masks].filter(([, cells]) => eligible(cells));
      const wanted = new Set([...selected].filter(id => need(id) > EPS));
      const open = [], wet = new Set();
      while (wanted.size) {
        let best = null, gain = 0;
        for (const entry of candidates) {
          const n = entry[1].filter(id => wanted.has(id)).length;
          if (n > gain) { best = entry; gain = n; }
        }
        if (!best) break;
        open.push(best[0]);
        for (const id of best[1]) { wet.add(id); wanted.delete(id); }
      }
      if (!open.length) break;
      const depth = Math.min(remaining,
        ...[...wet].filter(id => selected.has(id) && need(id) > EPS).map(need));
      const from = rain - remaining;
      for (const id of wet) {
        const stored = Math.min(depth, capacity - soil[id]);
        soil[id] += stored;
        delivered[id] += depth;
        overflow[id] += depth - stored;
      }
      remaining = Math.max(0, remaining - depth);
      phases.push({open_flaps: open.sort(), wet_cells: [...wet].sort((a, b) => a - b),
        depth_mm: depth, from_rain_mm: from, to_rain_mm: rain - remaining});
    }
    const area = layout.width_m * layout.length_m / count;
    const sum = xs => xs.reduce((a, b) => a + b, 0) * area;
    const cells = soil.map((value, id) => {
      let reason = selected.has(id) ? "target_met" : "not_selected";
      if (selected.has(id) && need(id) > EPS) {
        const above = [...masks.values()].filter(mask => mask.includes(id));
        reason = !above.length ? "uncovered" :
          !above.some(eligible) ? "policy_blocked" : "rain_exhausted";
      }
      return {id, selected: selected.has(id), soil_mm: value, target_mm: target[id],
        delivered_mm: delivered[id], remaining_mm: need(id), overflow_mm: overflow[id], reason};
    });
    return {
      simulated: true, layout_source: layout.source, rain_mm: rain,
      spill_allowed: spill, phases, final_open_flaps: [], unused_rain_mm: remaining, cells,
      empty_flaps: [...masks].filter(([, mask]) => !mask.length).map(([id]) => id),
      cell_area_m2: area, rain_litres: rain * layout.width_m * layout.length_m,
      admitted_litres: sum(delivered), excluded_litres: rain * layout.width_m * layout.length_m - sum(delivered),
      selected_litres: sum(delivered.map((v, id) => selected.has(id) ? v : 0)),
      outside_litres: sum(delivered.map((v, id) => selected.has(id) ? 0 : v)),
      stored_litres: sum(delivered) - sum(overflow), overflow_litres: sum(overflow),
      initial_soil_litres: sum(initial), final_soil_litres: sum(soil),
    };
  }

  const api = {footprints, simulate, fromCAD};
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.Watering = api;
})(globalThis);
