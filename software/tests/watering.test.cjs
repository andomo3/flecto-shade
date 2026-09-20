const {test} = require("node:test");
const assert = require("node:assert/strict");
const {footprints, simulate, fromCAD} = require("../page/watering-model.js");
const model = require("../page/model.json");
const mapping = require("../page/controller-map.json");

const flap = (id, x, radius = 0.51) => ({id, x_m: x, y_m: 0.5, radius_m: radius});
const roof = (...flaps) => ({width_m: 3, length_m: 1, cols: 3, rows: 1, flaps, source: "test fixture"});
const input = (selected, target_mm = 5, rain_mm = 5) => ({selected, target_mm, rain_mm});
const close = (a, b) => assert.ok(Math.abs(a - b) < 1e-9, `${a} != ${b}`);
function conserve(r) {
  close(r.admitted_litres + r.excluded_litres, r.rain_litres);
  close(r.selected_litres + r.outside_litres, r.admitted_litres);
  close(r.initial_soil_litres + r.admitted_litres, r.final_soil_litres + r.overflow_litres);
  assert.deepEqual(r.final_open_flaps, []);
}
test("simultaneous apertures use a union, never double rainfall on overlap", () => {
  const r = simulate(roof(flap("A", 1), flap("B", 2)), input([0, 1, 2], 4, 4));
  assert.deepEqual(r.cells.map(c => c.delivered_mm), [4, 4, 4]);
  close(r.admitted_litres, 12); conserve(r);
});
test("replan to the narrow flap when one selected neighbor reaches its target", () => {
  const r = simulate(roof(flap("A", 1), flap("B", 1.5, 0.4)), input([0, 1], [2, 5, 0]));
  assert.deepEqual(r.phases.map(p => [p.open_flaps, p.depth_mm]), [[["A"], 2], [["B"], 3]]);
  close(r.admitted_litres, 7); conserve(r);
});
test("protected completed neighbors block further watering and report the shortfall", () => {
  const r = simulate(roof(flap("A", 1)), input([0, 1], [2, 5, 0]));
  assert.equal(r.cells[1].reason, "policy_blocked");
  close(r.cells[1].remaining_mm, 3); conserve(r);
});
test("unselected cells stay dry; allowing spill reports delivery and overflow", () => {
  const layout = roof(flap("A", 1));
  const i = {...input([0]), capacity_mm: 10, soil_mm: [0, 9, 0]};
  const strict = simulate(layout, i);
  close(strict.admitted_litres, 0); conserve(strict);
  const r = simulate(layout, {...i, spill_allowed: true});
  close(r.outside_litres, 5); close(r.overflow_litres, 4); close(r.stored_litres, 6); conserve(r);
});
test("uncovered demand does not stop reachable cells from taking remaining rain", () => {
  const r = simulate(roof(flap("A", 0.5, 0.4)), input([0, 2], [10, 0, 1]));
  assert.equal(r.cells[0].reason, "rain_exhausted");
  assert.equal(r.cells[2].reason, "uncovered");
  close(r.cells[0].delivered_mm, 5); conserve(r);
});
test("blocked and rain-exhausted reasons remain distinct at event end", () => {
  const r = simulate(roof(flap("A", 1), flap("B", 2.5, 0.4)), input([0, 2], 10));
  assert.equal(r.cells[0].reason, "policy_blocked");
  assert.equal(r.cells[2].reason, "rain_exhausted"); conserve(r);
});
test("flap ID breaks ties independent of input order and selection order", () => {
  const a = flap("A", 1), b = flap("B", 1);
  const r = simulate(roof(b, a), input([0, 1]));
  assert.deepEqual(r.phases[0].open_flaps, ["A"]);
  assert.deepEqual(r, simulate(roof(a, b), input([1, 0])));
});
test("one millimetre over one square metre equals one litre; rectangular cells", () => {
  const layout = {width_m: 1, length_m: 1, cols: 2, rows: 4, flaps: [flap("A", 0.5, 1)]};
  const r = simulate(layout, input([0, 1, 2, 3, 4, 5, 6, 7], 3, 3));
  close(r.admitted_litres, 3); conserve(r);
});
test("circle boundary is included and overhanging circles are clipped to the grid", () => {
  assert.deepEqual(footprints(roof(flap("A", 1, 0.5))).get("A"), [0, 1]);
  assert.deepEqual(footprints(roof(flap("A", 0, 0.5))).get("A"), [0]);
});
test("zero rain, empty selection, no apertures and met targets finish with shut flaps", () => {
  for (const r of [
    simulate(roof(flap("A", 1)), input([0, 1], 5, 0)),
    simulate(roof(flap("A", 1)), input([])),
    simulate(roof(), input([0, 1])),
    simulate(roof(flap("A", 1)), {...input([0, 1]), soil_mm: 6}),
    simulate(roof(flap("A", 1)), {...input([0, 1]), soil_mm: 5 - 1e-12}),
  ]) { assert.deepEqual(r.phases, []); conserve(r); }
});
test("empty raster footprints are diagnosed", () => {
  const r = simulate(roof(flap("A", 1, 0.1)), input([0]));
  assert.deepEqual(r.empty_flaps, ["A"]); assert.equal(r.cells[0].reason, "uncovered");
});
test("invalid dimensions, water values, IDs and types fail explicitly", () => {
  for (const patch of [{width_m: NaN}, {length_m: 0}, {cols: 1.5}, {rows: Infinity},
    {flaps: [flap("A", 1), flap("A", 2)]}, {flaps: [flap("", 1)]},
    {flaps: [flap("A", NaN)]}, {flaps: [flap("A", 1, -1)]}]) {
    assert.throws(() => simulate({...roof(), ...patch}, input([0])));
  }
  for (const patch of [{rain_mm: NaN}, {rain_mm: -1}, {capacity_mm: Infinity},
    {soil_mm: NaN}, {soil_mm: -1}, {soil_mm: 61}, {target_mm: 61},
    {target_mm: [1, 2]}, {selected: [0.5]}, {selected: [true]},
    {selected: [3]}, {spill_allowed: "false"}]) {
    assert.throws(() => simulate(roof(), {...input([0]), ...patch}));
  }
});
test("conservation and strict protection hold across reproducible varied selections", () => {
  const layout = roof(flap("A", 0.5, 0.4), flap("B", 1), flap("C", 2), flap("D", 2.5, 0.4));
  for (let selection = 0; selection < 8; selection++) {
    for (const spill_allowed of [true, false]) {
      const i = {...input([0, 1, 2].filter(id => selection & (1 << id)), [6.7, 5.3, 9.1], 7.47),
        soil_mm: [2.31, 5.2, 1.7], spill_allowed};
      const r = simulate(layout, i);
      conserve(r);
      assert.deepEqual(r, simulate(layout, i));
      if (!spill_allowed) {
        close(r.outside_litres, 0); close(r.overflow_litres, 0);
        for (const cell of r.cells) if (cell.selected) assert.ok(cell.soil_mm <= cell.target_mm + 1e-9);
      }
    }
  }
});

test("the STEP mapping addresses every rendered flap in metres, within mesh quantization", () => {
  const layout = fromCAD(model, mapping), masks = footprints(layout);
  assert.equal(masks.size, 22);
  assert.equal(layout.cols * layout.rows, 390);
  assert.ok(layout.width_m > 0.129 && layout.width_m < 0.130);
  assert.ok(layout.length_m > 0.303 && layout.length_m < 0.305);
  assert.ok([...masks.values()].every(cells => cells.length > 0));
  const stale = structuredClone(mapping);
  stale.flaps[0].origin_m[0] += 0.1;
  assert.throws(() => fromCAD(model, stale), /stale/);
  assert.throws(() => fromCAD({...model, units: "mm"}, mapping), /units/);
  assert.throws(() => fromCAD(model, {...mapping, flaps: []}), /count/);
});

test("the two-footprint CAD demo meets selected targets with no outside delivery", () => {
  const layout = fromCAD(model, mapping), masks = footprints(layout);
  const selected = [...new Set([...masks.get(layout.flaps[0].id), ...masks.get(layout.flaps.at(-1).id)])];
  const r = simulate(layout, {selected, soil_mm: 20, target_mm: 25, rain_mm: 10});
  assert.ok(selected.length > 20);
  assert.ok(r.cells.filter(c => c.selected).every(c => c.reason === "target_met"));
  assert.equal(r.phases.length, 1);
  assert.equal(r.phases[0].open_flaps.length, 2);
  close(r.unused_rain_mm, 5); close(r.outside_litres, 0);
  conserve(r);
});

test("the full CAD rectangle reports coverage gaps honestly while watering reachable cells", () => {
  const layout = fromCAD(model, mapping);
  const selected = Array.from({length: layout.cols * layout.rows}, (_, i) => i);
  const r = simulate(layout, {selected, soil_mm: 20, target_mm: 25, rain_mm: 10});
  assert.ok(r.cells.some(c => c.reason === "uncovered"));
  assert.ok(r.cells.some(c => c.reason === "target_met"));
  assert.ok(r.cells.every(c => c.reason === "uncovered" || c.reason === "target_met"));
  conserve(r);
});
