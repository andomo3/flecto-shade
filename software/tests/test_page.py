"""C8: the page is one file, it is honest in words, and it needs no network."""

from __future__ import annotations

import re

from canopy.app import STATIC

PAGE = (STATIC / "index.html").read_text(encoding="utf-8")


def test_the_page_is_one_file_with_nothing_fetched_from_the_internet():
    assert not re.search(r"https?://", PAGE), "no CDN, no web font, no network"
    assert "<script" in PAGE and 'src="' not in PAGE.split("<script")[1].split(">")[0]


def test_the_page_says_what_is_measured_and_what_is_modelled():
    assert "Measured today on this table" in PAGE
    assert "Simulation: no hardware is connected" in PAGE
    assert "Replay mode" in PAGE
    assert "PVGIS typical year, Houston" in PAGE


def test_an_unfitted_sensor_reads_not_fitted_and_never_zero():
    assert "not fitted" in PAGE


def test_the_board_going_quiet_is_a_sentence_a_human_can_act_on():
    assert "The board stopped sending readings" in PAGE
    assert "Check the USB cable" in PAGE


def test_the_judge_has_one_button_and_the_rest_is_a_drawer():
    assert PAGE.count('class="play"') == 1
    assert 'id="drawer"' in PAGE
    for control in ("led", "sun-angle", "replay", "reset"):
        assert f'id="{control}"' in PAGE


def test_nothing_on_the_page_is_smaller_than_eighteen_pixels():
    sizes = [int(size) for size in re.findall(r"font-size:\s*(\d+)px", PAGE)]
    assert sizes and min(sizes) >= 18


def test_the_scene_has_a_sun_three_leaves_a_bench_and_a_figure():
    assert 'id="sun-disc"' in PAGE
    assert all(f'id="leaf-{n}"' in PAGE for n in (1, 2, 3))
    assert 'id="figure"' in PAGE
    assert 'id="bench-fill"' in PAGE and 'id="sun-fill"' in PAGE
