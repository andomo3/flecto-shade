"""Tests for the grower's console.

The page derives no physics. Every baseline number in day.json came out of package H1,
so these tests check that it carried them across without changing them, and that the
page's own files are self-contained and fetch nothing.

The values asserted here were computed by a planner from the real 2023 data before any
page code existed. They are not adjusted to match an implementation.

The model's geometry is covered in test_shade_house.py, the Flectofin deformation in
test_flectofin.py, and the persistent backend in test_api.py.
"""

import importlib.util
import json
import re
import socket
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PAGE = REPO_ROOT / "software" / "page"
BUILD = PAGE / "build_day.py"

SCRIPTS = ["flectofin.js", "rules.js", "scene.js", "api.js", "console.js", "app.js"]
SERVED = ["console.html", "style.css"] + SCRIPTS


def load():
    spec = importlib.util.spec_from_file_location("build_day", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def builder():
    return load()


@pytest.fixture(scope="module")
def day(builder, tmp_path_factory):
    out = tmp_path_factory.mktemp("page") / "day.json"
    _, payload = builder.build(date="2023-06-03", out_path=out)
    return payload


@pytest.fixture(scope="module")
def html():
    return (PAGE / "console.html").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def script():
    return "\n".join((PAGE / name).read_text(encoding="utf-8") for name in SCRIPTS)


def zone(day, letter):
    return next(z for z in day["zones"] if z["zone"] == letter)


# --------------------------------------------------------------- H1's own numbers

def test_builds_with_the_network_off(builder, tmp_path, monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("build_day opened a socket, and it must run with the network off")

    monkeypatch.setattr(socket, "socket", refuse)
    path, _ = builder.build(date="2023-06-03", out_path=tmp_path / "day.json")
    assert path.exists()


def test_the_day_is_whole(day):
    assert day["date_local"] == "2023-06-03"
    assert len(day["hours"]) == 24
    assert len(day["zones"]) == 3
    assert all(len(z["hours"]) == 24 for z in day["zones"])
    assert day["from_package"] == "H1"


def test_playback_matches_the_spoken_demo(day):
    """H2's three asserted values, computed by a planner from S1's year."""
    assert day["day"]["lit_hours"] == 14
    assert day["day"]["play_seconds"] == pytest.approx(38.6, abs=0.1)
    seconds = [h["play_seconds"] for h in day["hours"]]
    assert sum(seconds[:11]) == pytest.approx(15.0, abs=0.1), "the fern's fins shut"
    assert sum(seconds[:15]) == pytest.approx(24.6, abs=0.1), "the storm starts"


def test_it_carried_h1s_numbers_without_changing_them(day):
    assert day["day"]["rain_mm"] == pytest.approx(42.4, abs=0.05)
    a, b, c = zone(day, "A"), zone(day, "B"), zone(day, "C")
    assert a["soil_start"] == pytest.approx(53.26, abs=0.02)
    assert b["soil_start"] == pytest.approx(26.71, abs=0.02)
    assert c["soil_start"] == pytest.approx(34.11, abs=0.02)
    assert b["hours"][11]["light_mol_so_far"] == pytest.approx(12.72, abs=0.02)
    assert b["hours"][19]["light_mol_so_far"] == pytest.approx(18.68, abs=0.02)
    assert sum(h["rain_in_mm"] for h in b["hours"]) == pytest.approx(34.9, abs=0.1)


def test_three_zones_three_answers_with_their_reasons_in_words(day):
    a, b, c = zone(day, "A"), zone(day, "B"), zone(day, "C")
    for hour in (15, 16):
        assert a["hours"][hour]["open_fraction"] == 0
        assert a["hours"][hour]["state"] == "RAIN_SHUT"
        assert a["hours"][hour]["reason"] == "opted_out"
        assert a["hours"][hour]["because"] == "this crop opts out of rain"
        assert a["hours"][hour]["rain_in_mm"] == 0
        assert b["hours"][hour]["open_fraction"] == 1
        assert b["hours"][hour]["state"] == "RAIN_OPEN"
        assert b["hours"][hour]["reason"] == ""
        assert b["hours"][hour]["rain_in_mm"] > 0
        assert c["hours"][hour]["open_fraction"] == 0
        assert c["hours"][hour]["state"] == "RAIN_SHUT"
        assert c["hours"][hour]["reason"] == "wet_enough"
        assert c["hours"][hour]["because"] == "its soil is wet enough"
        assert c["hours"][hour]["rain_in_mm"] == 0


def test_the_constants_come_from_h1(day):
    spec = importlib.util.spec_from_file_location(
        "h1_build", REPO_ROOT / "software" / "h1" / "build.py")
    h1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h1)
    assert day["constants"]["K"] == pytest.approx(h1.K, abs=0.0001)
    assert day["constants"]["SOIL_DRY_BELOW"] == h1.SOIL_DRY_BELOW
    assert day["constants"]["HEAT_SHADE_C"] == h1.HEAT_SHADE_C


def test_the_region_panel(day):
    region = day["region"]
    assert region["rain_mm"] == pytest.approx(1338.6, abs=0.05)
    assert region["rain_hours"] == 373
    assert region["daylight_rain_hours"] == 242
    assert region["daylight_rain_mm"] == pytest.approx(924.2, abs=0.05)
    assert region["lit_hours"] == 4568
    assert len(region["monthly_rain_mm"]) == 12
    assert region["source"].startswith("NOAA")


def test_two_runs_give_identical_bytes(builder, tmp_path):
    first = builder.build(date="2023-06-03", out_path=tmp_path / "a.json")[0].read_bytes()
    second = builder.build(date="2023-06-03", out_path=tmp_path / "b.json")[0].read_bytes()
    assert first == second


def test_a_missing_input_says_what_to_run(builder, monkeypatch, tmp_path):
    monkeypatch.setattr(builder, "PROCESSED", tmp_path)
    with pytest.raises(FileNotFoundError, match="package H1"):
        builder.build(date="2023-06-03", out_path=tmp_path / "day.json")


# ------------------------------------------------------- the page fetches nothing

def test_the_page_fetches_nothing(day):
    """Gate F3's territory, checked here too because it is what breaks a demo."""
    for name in SERVED:
        text = (PAGE / name).read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(("*", "/*", "//")):
                continue
            assert "http://" not in stripped and "https://" not in stripped, f"{name}: {stripped[:90]}"


def test_every_served_script_is_loaded_by_the_page(html):
    for name in SCRIPTS:
        assert f'src="{name}"' in html, f"{name} is served but never loaded"
    assert "cdn" not in html.lower()
    assert "<link rel=\"stylesheet\" href=\"style.css\">" in html


def test_there_is_no_decorative_top_bar(html):
    assert '<header class="bar">' not in html
    assert "<header" not in html


# --------------------------------------------------------- the browser rules are H1's

def test_the_browser_rules_reproduce_h1_for_every_committed_zone(day):
    """A zone a grower adds is run in the browser, so those rules must be H1's.

    Compared against day.json, which is rounded to two decimals, so the tolerance is
    the rounding and nothing more.
    """
    import shutil
    import subprocess

    node = shutil.which("node")
    if not node:
        pytest.skip("node is not installed, so the browser rules cannot be executed")

    payload = json.dumps(day)
    program = """
      var Rules = require(%s);
      var day = JSON.parse(process.argv[1]);
      var out = {};
      day.zones.forEach(function (zone) {
        var mine = Rules.runZone(day.constants, {
          light_rule: zone.light_rule, light_target: zone.light_target,
          kc: zone.kc, rain_ok: zone.rain_ok, soil_start: zone.soil_start
        }, day.hours, []);
        var worstSoil = 0, worstLight = 0, mismatches = [];
        mine.forEach(function (hour, index) {
          var theirs = zone.hours[index];
          worstSoil = Math.max(worstSoil, Math.abs(hour.soil - theirs.soil_mm));
          worstLight = Math.max(worstLight, Math.abs(hour.light - theirs.light_mol_so_far));
          if (hour.state !== theirs.state || hour.reason !== theirs.reason ||
              hour.open !== theirs.open_fraction) { mismatches.push(index); }
        });
        out[zone.zone] = { soil: worstSoil, light: worstLight, mismatches: mismatches };
      });
      process.stdout.write(JSON.stringify(out));
    """ % json.dumps(str(PAGE / "rules.js"))

    finished = subprocess.run([node, "-e", program, payload],
                              capture_output=True, text=True, timeout=60)
    assert finished.returncode == 0, finished.stderr
    result = json.loads(finished.stdout)
    for letter, report in result.items():
        assert report["mismatches"] == [], f"zone {letter} decided differently at {report['mismatches']}"
        assert report["soil"] < 0.01, f"zone {letter} soil drifted by {report['soil']}"
        assert report["light"] < 0.01, f"zone {letter} light drifted by {report['light']}"


# ------------------------------------------------------------------- the interface

def test_the_screen_is_the_five_regions_the_console_needs(html):
    for marker in ('<section class="stage"', 'id="overview"', 'id="inspector"',
                   'class="panel timeline"', 'class="panel workspace"'):
        assert marker in html, f"the console is missing {marker}"
    assert html.index('id="overview"') < html.index('id="inspector"')


def test_the_overview_can_show_every_metric_the_registry_holds(script):
    for metric in ("roof_position", "control_state", "decision_reason", "rain_outcome",
                   "daily_light", "soil_water", "last_decision", "next_action",
                   "data_timestamp", "irrigation"):
        assert f'"{metric}"' in script, f"the overview cannot render {metric}"
    assert "metricCell" in script and "review_profile" in script


def test_the_reviewed_metrics_are_a_registry_and_not_a_formula(script):
    assert "METRICS" in script
    assert "removable: false" in script
    assert "eval(" not in script and "new Function" not in script


def test_every_required_state_has_a_word_a_glyph_and_a_treatment(script):
    css = (PAGE / "style.css").read_text(encoding="utf-8")
    for state, word in (("auto", "Automatic"), ("warning", "Attention"),
                        ("conflict", "Conflict"), ("manual", "Manual hold"),
                        ("stale", "Stale data"), ("offline", "Not stored")):
        assert f'word: "{word}"' in script, f"state {state} has no word"
        assert f'glyph:' in script
        assert f'[data-status="{state}"]' in css or f'[data-state="{state}"]' in css, \
            f"state {state} has no border or colour treatment"
    assert "skeleton" in css and "is-loading" in script, "there is no loading state"
    assert "No simulated result yet" in script, "there is no empty result state"
    assert "form-error" in css, "there is no invalid configuration state"


def test_the_four_zone_limit_is_explained_and_not_only_disabled(script):
    assert "MAX_ZONES = 4" in script
    assert 'LETTERS = ["A", "B", "C", "D"]' in script
    assert "Archive one to add another" in script
    assert 'classList.toggle("is-limit"' in script


def test_selecting_a_zone_joins_the_roof_and_the_console(script):
    assert "onZonePick" in script, "the roof cannot select a console row"
    assert "scene.setSelected(letter)" in script
    assert "scene.focusZone(letter)" in script
    assert "focusZone: centreOnZone" in script


def test_an_override_is_reviewed_carries_an_expiry_and_can_be_released(script):
    assert "Review the override" in script
    assert "Review before applying" in script
    assert "returns to automatic control by itself" in script
    assert "Return to automatic" in script
    assert "acknowledged_review: true" in script
    assert "until_hour" in script
    assert "A safety rule refuses this command" in script


def test_a_configuration_change_is_previewed_and_keeps_earlier_runs(html, script):
    assert "Preview the change" in html, "a change can be applied without being previewed"
    assert "Earlier simulation runs keep the revision they were run with." in script
    assert "expected_revision" in script
    assert "This writes revision " in script
    assert "Archiving keeps every earlier simulation run readable." in script


def test_the_console_is_operable_from_the_keyboard(html, script):
    assert 'class="skip"' in html, "there is no skip link"
    assert 'setAttribute("tabindex", "0")' in script, "the model cannot take focus"
    assert 'case "ArrowLeft"' in script and 'case "ArrowRight"' in script
    assert 'case "0": case "Home"' in script, "the view cannot be reset from the keyboard"
    assert 'case "1": case "2": case "3": case "4"' in script, "zones cannot be picked by key"
    assert 'event.key === "ArrowLeft"' in script, "the timeline cannot be stepped by key"
    assert 'aria-live="polite"' in html
    assert 'role="tablist"' in html and 'role="tabpanel"' in html


def test_an_unavailable_service_still_leaves_the_demonstration_running(script):
    assert "offlineStore" in script
    assert "The historical demonstration runs from the static simulated day" in script
    assert "held in this session only" in script
    assert "The simulated day file is missing." in script, "no message when day.json is gone"
    assert "This browser cannot draw the modelled roof" in script


def test_the_plants_are_decoration_and_say_so(html, script):
    assert "not a simulated crop response" in html
    assert "seededRandom" in script
    assert "Math.random" not in script


def test_the_page_credits_the_mechanism_it_did_not_invent(day):
    assert "ITKE" in day["credit"]
    assert "University of Stuttgart" in day["credit"]
    assert "EP2320015" in day["credit"]
    for name in SERVED:
        text = (PAGE / name).read_text(encoding="utf-8")
        assert "Flexofin" not in text, f"{name} misspells the Flectofin"


def test_the_model_never_claims_to_be_validated(html, script):
    assert "no value on it is a validated engineering result" in html
    assert "conceptual clamp" in html.lower()
    assert "physically informed approximation" in script.lower()
    for text in (html, script):
        assert "finite-element" not in text.lower() or "replaced" in text.lower() or \
            "exported" in text.lower()


def test_no_figure_for_cost_yield_energy_or_water_saved(html, script):
    for text in (html, script):
        lowered = text.lower()
        for phrase in ("water saved", "energy saved", "cost saving", "yield increase",
                       "per cent more", "roi", "payback"):
            assert phrase not in lowered, f'the page writes "{phrase}"'


def test_console_type_never_drops_below_eighteen_pixels():
    style = (PAGE / "style.css").read_text(encoding="utf-8")
    sizes = [int(value) for value in re.findall(r"font-size:\s*(\d+)px", style)]
    sizes += [int(value) for value in re.findall(r"font:\s*[^;]*?(\d+)px", style)]
    assert sizes
    assert min(sizes) >= 18


def test_touch_targets_stay_at_least_forty_eight_pixels():
    style = (PAGE / "style.css").read_text(encoding="utf-8")
    heights = [int(value) for value in re.findall(r"min-height:\s*(\d+)px", style)]
    assert heights
    assert min(heights) >= 40, "a control is smaller than a finger"
    assert "min-height: 1.5em" in style, "a text line should not be sized as a control"
    assert heights.count(48) >= 5, "the console's controls should share one 48 px target"
