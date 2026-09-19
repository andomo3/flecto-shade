"""C4: hand written readings, and the values the page draws from them."""

from __future__ import annotations

from canopy import config
from canopy.contract import Reading, parse_line
from canopy.state import BENDING, BENT, RESTING, State, percent


def reading(**over) -> Reading:
    fields = dict(
        t_ms=1000,
        light=800,
        bench=160,
        fixed=None,
        flex=650,
        temp_canopy=None,
        temp_open=None,
        angle=config.ANGLE_BENT,
        sun=None,
        led=255,
        override=0,
    )
    fields.update(over)
    return Reading(**fields)


def test_percent_is_the_number():
    assert percent(160, 800) == 20.0
    assert percent(None, 800) is None
    assert percent(160, 0) is None
    assert percent(160, None) is None


def test_the_leaf_state_comes_from_the_angle():
    state = State()
    state.update(reading(angle=0))
    assert state.leaves == RESTING
    state.update(reading(angle=60))
    assert state.leaves == BENDING
    state.update(reading(angle=config.ANGLE_BENT))
    assert state.leaves == BENT


def test_the_two_averages_are_kept_apart():
    state = State()
    state.update(reading(angle=0, light=200, bench=164))  # resting, 82 percent
    state.update(reading(angle=0, light=300, bench=240))  # resting, 80 percent
    state.update(reading(angle=config.ANGLE_BENT, light=800, bench=160))  # bent, 20
    state.update(reading(angle=config.ANGLE_BENT, light=900, bench=162))  # bent, 18

    assert state.resting.count == 2
    assert state.resting.mean == 81.0
    assert state.bent.count == 2
    assert state.bent.mean == 19.0
    assert round(state.bent.spread, 3) == 1.414
    assert state.bent.low == 18.0
    assert state.bent.high == 20.0


def test_a_moving_leaf_counts_towards_neither_average():
    state = State()
    state.update(reading(angle=60))
    assert state.bent.count == 0
    assert state.resting.count == 0


def test_an_unfitted_bench_sensor_is_absent_and_never_zero():
    state = State()
    state.update(reading(bench=None, flex=None))
    snapshot = state.snapshot()
    assert snapshot["bench"] is None
    assert snapshot["bench_percent"] is None
    assert snapshot["fitted"] == {
        "bench": False,
        "fixed": False,
        "flex": False,
        "temperature": False,
        "sun": False,
    }


def test_the_early_line_from_the_contract_shows_only_the_incident_sensor():
    state = State()
    state.update(parse_line("1200,212,,,,,,0,,40,0"))
    snapshot = state.snapshot()
    assert snapshot["light"] == 212
    assert snapshot["bench"] is None
    assert snapshot["leaves"] == RESTING
    assert all(value is False for value in snapshot["fitted"].values())


def test_the_full_line_from_the_contract_fits_every_sensor():
    state = State()
    state.update(parse_line("61200,791,187,610,661,253,268,125,90,255,1"))
    snapshot = state.snapshot()
    assert snapshot["bench_percent"] == 23.6
    assert snapshot["fixed_percent"] == 77.1
    assert snapshot["temperature_difference"] == 1.5
    assert snapshot["fitted"]["temperature"] is True
    assert snapshot["fitted"]["sun"] is True


def test_the_temperature_difference_needs_both_sensors():
    state = State()
    state.update(reading(temp_canopy=253, temp_open=None))
    assert state.temperature_difference is None
    state.update(reading(temp_canopy=253, temp_open=268))
    assert state.temperature_difference == 1.5


def test_a_cycle_is_bent_and_back():
    state = State()
    for angle in (0, 60, config.ANGLE_BENT, config.ANGLE_BENT, 60, 0):
        state.update(reading(angle=angle, light=800))
    assert state.cycles == 1

    for angle in (60, config.ANGLE_BENT, 60, 0):
        state.update(reading(angle=angle, light=800))
    assert state.cycles == 2


def test_a_bend_that_never_returns_is_not_a_cycle():
    state = State()
    for angle in (0, 60, config.ANGLE_BENT, config.ANGLE_BENT):
        state.update(reading(angle=angle, light=800))
    assert state.cycles == 0


def test_reset_forgets_the_run():
    state = State()
    state.update(reading())
    state.day_finished = True
    state.reset()
    snapshot = state.snapshot()
    assert snapshot["waiting"] is True
    assert snapshot["cycles"] == 0
    assert snapshot["day_finished"] is False
    assert snapshot["averages"]["bent"]["count"] == 0
