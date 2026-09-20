(function () {
  "use strict";
  const $ = id => document.getElementById(id);
  const selected = new Set(), buttons = [], circles = new Map();
  const reasons = {uncovered: "No aperture above this cell", policy_blocked: "Protected neighbours block the opening",
    rain_exhausted: "Rain ended before the target", target_met: "Target met", not_selected: "Not selected"};
  let layout, masks, mapping, result = null, input = null, frame = null, started = 0;
  let painting = null, lastPainted = -1, focusId = 0, running = false, phaseIndex = -1;
  const volume = litres => litres < 1 ? (litres * 1000).toFixed(1) + " mL" : litres.toFixed(2) + " L";
  const count = () => layout.cols * layout.rows;

  function message(text, error = false) {
    $("status").textContent = text;
    $("status").classList.toggle("error", error);
  }

  function scene(open = [], delivered = [], wet = [], raining = false) {
    window.CadRoof.update({open, selected: [...selected], delivered, wet, raining});
    for (const [id, circle] of circles) circle.classList.toggle("open", open.includes(id));
  }

  function stop() {
    if (frame !== null) cancelAnimationFrame(frame);
    frame = null; running = false; phaseIndex = -1;
    $("finish").hidden = true;
    $("simulate").textContent = "Simulate rain";
  }

  function invalidate() {
    stop(); result = null; input = null;
    $("export").disabled = true;
    $("event-progress").value = 0;
    for (const id of ["met", "delivered", "outside", "overflow"]) $(id).textContent = "—";
    $("shortfalls").textContent = "Choose areas and simulate rain to see the result.";
    $("accounting").textContent = "";
    $("phases").replaceChildren();
    $("phase-status").textContent = "All flaps closed. Ready for a rain event.";
    message("Ready. Inputs and all water delivery are simulated.");
    paintMap(); scene(); describe(focusId);
  }

  function paintMap(delivered = null, finished = false) {
    for (let id = 0; id < count(); id++) {
      const cell = buttons[id], picked = selected.has(id);
      cell.setAttribute("aria-selected", String(picked));
      const depth = delivered ? delivered[id] : 0;
      cell.classList.toggle("wet", picked && depth > 1e-9);
      cell.classList.toggle("spilled", !picked && depth > 1e-9);
      cell.classList.toggle("short", finished && picked && result.cells[id].remaining_mm > 1e-9);
      cell.setAttribute("aria-label", `Cell ${id + 1}, ${picked ? "selected" : "not selected"}` +
        (finished ? `, ${result.cells[id].delivered_mm.toFixed(1)} mm delivered, ${reasons[result.cells[id].reason]}` : ""));
    }
    $("selection-count").textContent = `${selected.size} of ${count()} cells selected · ` +
      `${(selected.size * layout.width_m * layout.length_m / count() * 10000).toFixed(1)} cm² at CAD scale`;
  }

  function describe(id) {
    const cell = result && !running ? result.cells[id] : null;
    $("cell-detail").textContent = `Cell ${id + 1}: ${selected.has(id) ? "selected" : "not selected"}. ` +
      (cell ? `${cell.delivered_mm.toFixed(1)} mm delivered; soil ${cell.soil_mm.toFixed(1)} mm. ${reasons[cell.reason]}.` :
        `${[...masks.values()].filter(mask => mask.includes(id)).length} assumed apertures above.`);
  }

  function selectCell(id, picked) {
    if (id === lastPainted) return;
    lastPainted = id;
    if (picked) selected.add(id); else selected.delete(id);
    invalidate(); describe(id);
  }

  function setFocus(id) {
    buttons[focusId].tabIndex = -1;
    focusId = id; buttons[id].tabIndex = 0; buttons[id].focus();
    describe(id);
  }

  function buildMap() {
    const map = $("soil-map");
    map.style.gridTemplateColumns = `repeat(${layout.rows}, 1fr)`;
    map.setAttribute("aria-rowcount", layout.cols);
    map.setAttribute("aria-colcount", layout.rows);
    for (let x = 0; x < layout.cols; x++) {
      for (let y = 0; y < layout.rows; y++) {
        const id = y * layout.cols + x, button = document.createElement("button");
        button.type = "button"; button.className = "soil-cell"; button.dataset.cell = id;
        button.setAttribute("role", "gridcell");
        button.setAttribute("aria-rowindex", x + 1); button.setAttribute("aria-colindex", y + 1);
        button.tabIndex = id === 0 ? 0 : -1;
        button.addEventListener("pointerdown", event => {
          if (event.button !== 0) return;
          event.preventDefault();
          painting = !selected.has(id); lastPainted = -1; setFocus(id); selectCell(id, painting);
        });
        button.addEventListener("focus", () => describe(id));
        button.addEventListener("click", event => {
          if (event.detail === 0) { lastPainted = -1; selectCell(id, !selected.has(id)); }
        });
        button.addEventListener("keydown", event => {
          const dx = {ArrowDown: 1, ArrowUp: -1}[event.key] || 0;
          const dy = {ArrowRight: 1, ArrowLeft: -1}[event.key] || 0;
          if (dx || dy) {
            event.preventDefault();
            setFocus(Math.min(layout.rows - 1, Math.max(0, y + dy)) * layout.cols +
              Math.min(layout.cols - 1, Math.max(0, x + dx)));
          }
        });
        buttons[id] = button; map.appendChild(button);
      }
    }
    document.addEventListener("pointermove", event => {
      if (painting === null) return;
      const element = document.elementFromPoint(event.clientX, event.clientY);
      if (element && element.classList.contains("soil-cell")) selectCell(Number(element.dataset.cell), painting);
    });
    const end = () => { painting = null; lastPainted = -1; };
    document.addEventListener("pointerup", end);
    document.addEventListener("pointercancel", end);
    window.addEventListener("blur", end);
    const svg = $("footprint-rings");
    svg.setAttribute("viewBox", `0 0 ${layout.length_m * 1000} ${layout.width_m * 1000}`);
    svg.setAttribute("preserveAspectRatio", "none");
    for (const flap of layout.flaps) {
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", flap.y_m * 1000); circle.setAttribute("cy", flap.x_m * 1000);
      circle.setAttribute("r", flap.radius_m * 1000);
      svg.appendChild(circle); circles.set(flap.id, circle);
    }
  }

  function finish() {
    stop();
    const delivery = result.cells.map(cell => cell.delivered_mm);
    scene([], delivery); paintMap(delivery, true);
    $("event-progress").value = 1;
    $("phase-status").textContent = "Rain event complete. All flaps closed.";
    const requested = result.cells.filter(cell => cell.selected);
    const met = requested.filter(cell => cell.reason === "target_met").length;
    $("met").textContent = `${met} / ${requested.length}`;
    $("delivered").textContent = volume(result.selected_litres);
    $("outside").textContent = volume(result.outside_litres);
    $("overflow").textContent = volume(result.overflow_litres);
    const counts = ["uncovered", "policy_blocked", "rain_exhausted"].map(reason => {
      const n = requested.filter(cell => cell.reason === reason).length;
      return n ? `${n}: ${reasons[reason].toLowerCase()}` : "";
    }).filter(Boolean);
    $("shortfalls").textContent = !requested.length ? "No areas selected; all rain excluded." :
      counts.length ? counts.join(". ") + "." : "Every selected cell reached its target.";
    $("accounting").textContent = `Event over the map: ${volume(result.rain_litres)} = ` +
      `${volume(result.admitted_litres)} admitted + ${volume(result.excluded_litres)} excluded. ` +
      `${result.unused_rain_mm.toFixed(1)} mm of the event remained after the last opening. ` +
      `Retained from this event: ${volume(result.stored_litres)}.`;
    $("export").disabled = false; describe(focusId);
    message(counts.length ? "Simulation complete with unmet targets. Inspect the result for reasons." :
      "Simulation complete. Results describe this idealized rain model.");
  }

  function animate(now) {
    const fraction = Math.min(1, (now - started) / 8000), depth = result.rain_mm * fraction;
    if (fraction >= 1) { finish(); return; }
    const delivered = Array(count()).fill(0);
    let open = [], wet = [], active = -1;
    result.phases.forEach((phase, index) => {
      const applied = Math.max(0, Math.min(phase.depth_mm, depth - phase.from_rain_mm));
      for (const id of phase.wet_cells) delivered[id] += applied;
      if (depth >= phase.from_rain_mm && depth < phase.to_rain_mm) {
        open = phase.open_flaps; wet = phase.wet_cells; active = index;
      }
    });
    if (active !== phaseIndex) {
      phaseIndex = active;
      $("phase-status").textContent = open.length ? `Open: ${open.join(", ")}. Rain reaches the highlighted footprints.` :
        "All flaps closed. The remaining rain is excluded.";
    }
    $("event-progress").value = fraction;
    paintMap(delivered); scene(open, delivered, wet, true);
    frame = requestAnimationFrame(animate);
  }

  function run(event) {
    event.preventDefault();
    if (!$("rain-form").reportValidity()) return;
    invalidate();
    try {
      input = {selected: [...selected].sort((a, b) => a - b), rain_mm: Number($("rain").value),
        soil_mm: Number($("soil").value), target_mm: Number($("target").value),
        capacity_mm: 60, spill_allowed: $("spill").checked};
      result = window.Watering.simulate(layout, input);
      for (const phase of result.phases) {
        const item = document.createElement("li");
        item.textContent = `${phase.from_rain_mm.toFixed(2)}–${phase.to_rain_mm.toFixed(2)} mm of event: ` +
          `${phase.open_flaps.join(", ")}; ${phase.wet_cells.length} receiving cells.`;
        $("phases").appendChild(item);
      }
      if (!result.phases.length) {
        const item = document.createElement("li"); item.textContent = "No opening is needed or permitted.";
        $("phases").appendChild(item);
      }
      if (!input.rain_mm || window.matchMedia("(prefers-reduced-motion: reduce)").matches) { finish(); return; }
      running = true; started = performance.now();
      $("finish").hidden = false; $("simulate").textContent = "Restart rain";
      $("phase-status").textContent = "All flaps closed. Rain is excluded.";
      message("Simulating the rain event. Changing an input cancels this run.");
      frame = requestAnimationFrame(animate);
    } catch (error) { message(error.message, true); }
  }

  async function load(name) {
    const response = await fetch(name);
    if (!response.ok) throw new Error(`${name} could not be loaded (${response.status})`);
    return response.json();
  }

  Promise.all([load("model.json"), load("controller-map.json")]).then(([model, map]) => {
    mapping = map; layout = window.Watering.fromCAD(model, mapping);
    masks = window.Watering.footprints(layout);
    buildMap();
    try { window.CadRoof.mount(model, layout); }
    catch (error) {
      window.CadRoof.update = () => {};
      $("roof").textContent = `CAD rendering unavailable: ${error.message}. The soil map still works.`;
    }
    $("layout-source").textContent = `${(layout.width_m * 1000).toFixed(1)} × ${(layout.length_m * 1000).toFixed(1)} mm ` +
      `assembly bounding rectangle. ${layout.cols} × ${layout.rows} cells, approximately 10 mm each. ${layout.source}.`;
    for (const id of ["simulate", "reset", "example", "all", "clear"]) $(id).disabled = false;
    $("rain-form").addEventListener("submit", run);
    for (const id of ["rain", "soil", "target", "spill"]) $(id).addEventListener("input", invalidate);
    $("reset").addEventListener("click", () => {
      selected.clear(); $("rain-form").reset(); invalidate(); describe(focusId);
    });
    $("clear").addEventListener("click", () => { selected.clear(); invalidate(); describe(focusId); });
    $("all").addEventListener("click", () => {
      for (let id = 0; id < count(); id++) selected.add(id);
      invalidate(); describe(focusId);
    });
    $("example").addEventListener("click", () => {
      selected.clear();
      for (const id of [layout.flaps[0].id, layout.flaps[layout.flaps.length - 1].id]) {
        for (const cell of masks.get(id)) selected.add(cell);
      }
      invalidate(); describe(focusId);
    });
    $("finish").addEventListener("click", finish);
    $("export").addEventListener("click", () => {
      const body = {schema: "shadehouse-watering-result-1", layout, assumptions: mapping.assumptions, input, result};
      const url = URL.createObjectURL(new Blob([JSON.stringify(body, null, 2)], {type: "application/json"}));
      const link = document.createElement("a"); link.href = url; link.download = "shade-house-watering.json";
      link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
    invalidate();
  }).catch(error => message(`Demo could not load: ${error.message}. Serve the complete software/page directory and reload.`, true));
})();
