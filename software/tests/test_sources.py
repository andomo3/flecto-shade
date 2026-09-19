"""C2 and C3: the fixture source replays a file, and the fake board behaves."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from canopy import config, contract
from canopy.contract import Reading
from canopy.sources import FakeSource, FixtureSource, open_source

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic-day.csv"


class Clock:
    """A sleep that records what it was asked to wait for and never waits."""

    def __init__(self) -> None:
        self.waits: list[float] = []

    async def __call__(self, seconds: float) -> None:
        self.waits.append(seconds)


async def take(source, count: int) -> list[Reading]:
    out = []
    async for reading in source.readings():
        out.append(reading)
        if len(out) == count:
            break
    return out


def test_the_fixture_file_parses_line_by_line():
    lines = FIXTURE.read_text(encoding="utf-8").splitlines()
    parsed = [contract.parse_line(line) for line in lines]
    assert all(item is not None for item in parsed)
    readings = [item for item in parsed if isinstance(item, Reading)]
    headers = [item for item in parsed if isinstance(item, contract.Header)]
    assert len(readings) == 600
    assert headers and all(header.version == contract.VERSION for header in headers)


def test_the_fixture_source_yields_the_files_readings_in_order():
    clock = Clock()
    source = FixtureSource(FIXTURE, sleep=clock)
    readings = asyncio.run(take(source, 600))
    assert [reading.t_ms for reading in readings] == list(range(0, 60_000, 100))


def test_the_fixture_source_is_paced_by_t_ms():
    clock = Clock()
    source = FixtureSource(FIXTURE, sleep=clock)
    asyncio.run(take(source, 5))
    assert clock.waits == pytest.approx([0.1, 0.1, 0.1, 0.1])


def test_speed_shortens_the_wait_without_changing_the_readings():
    clock = Clock()
    source = FixtureSource(FIXTURE, sleep=clock, speed=10.0)
    asyncio.run(take(source, 3))
    assert clock.waits == pytest.approx([0.01, 0.01])


def test_the_fixture_source_loops():
    clock = Clock()
    source = FixtureSource(FIXTURE, sleep=clock)
    readings = asyncio.run(take(source, 602))
    assert readings[600].t_ms == 0
    assert readings[601].t_ms == 100


def test_a_fixture_source_that_does_not_loop_stops():
    clock = Clock()
    source = FixtureSource(FIXTURE, sleep=clock, loop=False)
    readings = asyncio.run(take(source, 10_000))
    assert len(readings) == 600


def test_the_fixture_day_bends_the_leaves_at_noon_and_rests_at_night():
    clock = Clock()
    source = FixtureSource(FIXTURE, sleep=clock, loop=False)
    readings = asyncio.run(take(source, 10_000))
    assert readings[0].angle == config.ANGLE_RESTING
    assert readings[300].angle == config.ANGLE_BENT
    assert readings[-1].angle == config.ANGLE_RESTING


def test_the_fixture_keeps_unfitted_sensors_empty():
    clock = Clock()
    source = FixtureSource(FIXTURE, sleep=clock)
    reading = asyncio.run(take(source, 1))[0]
    assert reading.temp_canopy is None
    assert reading.temp_open is None
    assert reading.fixed is None
    assert reading.bench is not None


def test_a_file_cannot_act_on_a_command_but_keeps_it():
    source = FixtureSource(FIXTURE, sleep=Clock())
    source.send(contract.led(120))
    assert source.commands == ["L 120\n"]


def test_the_fake_board_follows_the_led_it_is_given():
    board = FakeSource()
    board.send(contract.led(255))
    reading = board.tick()
    assert reading.light == 1000
    assert reading.led == 255


def test_the_fake_board_bends_over_about_four_seconds():
    board = FakeSource()
    board.send(contract.led(255))
    ticks = 0
    while board.tick().angle < config.ANGLE_BENT:
        ticks += 1
        assert ticks < 200
    seconds = ticks * config.TICK_MS / 1000
    assert seconds == pytest.approx(config.BEND_SECONDS, abs=0.5)


def test_the_fake_board_rests_when_the_light_goes():
    board = FakeSource()
    board.send(contract.led(255))
    for _ in range(60):
        board.tick()
    board.send(contract.led(0))
    for _ in range(60):
        reading = board.tick()
    assert reading.angle == config.ANGLE_RESTING
    assert reading.bench == 0


def test_the_hysteresis_holds_the_leaves_between_the_thresholds():
    board = FakeSource()
    board.send(contract.led(round(config.REST_LIGHT * 0.255) + 10))
    for _ in range(60):
        reading = board.tick()
    assert reading.angle == config.ANGLE_RESTING

    board.send(contract.led(255))
    for _ in range(60):
        board.tick()
    board.send(contract.led(round(config.BEND_LIGHT * 0.255) - 10))
    for _ in range(60):
        reading = board.tick()
    assert reading.angle == config.ANGLE_BENT


def test_replay_mode_takes_the_leaves_and_o_zero_gives_them_back():
    board = FakeSource()
    board.send(contract.leaf_angle(90))
    for _ in range(60):
        reading = board.tick()
    assert reading.angle == 90
    assert reading.override == 1

    board.send(contract.override(False))
    reading = board.tick()
    assert reading.override == 0


def test_garbage_and_out_of_range_commands_are_ignored():
    board = FakeSource()
    board.send(contract.led(200))
    before = board.tick()
    for junk in ["", "Z 9\n", "L 900\n", "A 999\n", "L\n", "L abc\n"]:
        board.send(junk)
    after = board.tick()
    assert after.led == before.led
    assert after.sun is None


def test_an_unfitted_sensor_is_empty_and_never_zero():
    board = FakeSource(has_bench=False, has_flex=False)
    board.send(contract.led(255))
    reading = board.tick()
    assert reading.bench is None
    assert reading.flex is None
    assert reading.light > 0


def test_open_source_builds_by_name():
    assert isinstance(open_source("fixture", fixture=FIXTURE), FixtureSource)
    assert isinstance(open_source("fake"), FakeSource)
    with pytest.raises(ValueError):
        open_source("nonsense")
