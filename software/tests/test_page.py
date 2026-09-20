"""Tests for H2, the grower's console.

The page derives no physics. Every baseline number in day.json came out of package H1,
so these tests check that it carried them across without changing them, and that the
page's own files are self-contained and fetch nothing.
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


def zone(day, letter):
    return next(z for z in day["zones"] if z["zone"] == letter)


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
        assert a["hours"][hour]["state"] == "RAIN_SHUT"
        assert a["hours"][hour]["because"] == "this crop opts out of rain"
        assert b["hours"][hour]["state"] == "RAIN_OPEN"
        assert c["hours"][hour]["state"] == "RAIN_SHUT"
        assert c["hours"][hour]["because"] == "its soil is wet enough"


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


def test_the_page_fetches_nothing(day):
    """Gate F3's territory, checked here too because it is what breaks a demo."""
    for name in ("index.html", "style.css", "app.js"):
        text = (PAGE / name).read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(("*", "/*", "//")):
                continue
            assert "http://" not in stripped and "https://" not in stripped, f"{name}: {stripped[:90]}"


def test_two_runs_give_identical_bytes(builder, tmp_path):
    first = builder.build(date="2023-06-03", out_path=tmp_path / "a.json")[0].read_bytes()
    second = builder.build(date="2023-06-03", out_path=tmp_path / "b.json")[0].read_bytes()
    assert first == second


def test_a_missing_input_says_what_to_run(builder, monkeypatch, tmp_path):
    monkeypatch.setattr(builder, "PROCESSED", tmp_path)
    with pytest.raises(FileNotFoundError, match="package H1"):
        builder.build(date="2023-06-03", out_path=tmp_path / "day.json")
