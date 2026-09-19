"""C7: the day drives the light, and the leaves follow the light, not the clock."""

from __future__ import annotations

import asyncio

from canopy import config
from canopy.day import DEFAULT_DAY, DayPlayer, load_day
from canopy.sources import FakeSource


async def nap(_seconds: float) -> None:
    """No waiting in tests: the pacing is asserted, not lived through."""


def test_the_houston_day_loads_with_its_real_date():
    day = load_day(DEFAULT_DAY)
    assert day.city == "houston"
    assert len(day.steps) == 600
    assert day.date == day.steps[0].local_time[:10]
    assert day.peak_ghi > 900
    assert day.steps[0].led == 0


def test_a_step_sends_one_lamp_and_one_sun_command():
    source = FakeSource()
    commands: list[str] = []
    source.send = commands.append  # type: ignore[method-assign]
    player = DayPlayer(source, load_day(DEFAULT_DAY), sleep=nap)

    player.send_step(player.day.steps[300])
    assert len(commands) == 2
    assert commands[0].startswith("L ")
    assert commands[1].startswith("A ")


def test_replay_mode_also_commands_the_leaves():
    source = FakeSource()
    commands: list[str] = []
    source.send = commands.append  # type: ignore[method-assign]
    player = DayPlayer(source, load_day(DEFAULT_DAY), replay_mode=True, sleep=nap)

    noon = max(player.day.steps, key=lambda step: step.led)
    player.send_step(noon)
    assert commands[-1].strip() == f"S {config.ANGLE_BENT}"

    player.send_step(player.day.steps[0])
    assert commands[-1].strip() == f"S {config.ANGLE_RESTING}"


def test_the_player_walks_the_day_ten_steps_a_second():
    naps: list[float] = []

    async def counted(seconds: float) -> None:
        naps.append(seconds)

    player = DayPlayer(FakeSource(), load_day(DEFAULT_DAY), sleep=counted)
    asyncio.run(player.play(steps=10))
    assert player.index == 10
    assert naps == [config.TICK_MS / 1000] * 10


def test_against_the_fake_board_the_leaves_flare_by_day_and_rest_by_night():
    source = FakeSource(has_bench=True)
    player = DayPlayer(source, load_day(DEFAULT_DAY), sleep=nap)

    angles = []
    for step in player.day.steps:
        player.send_step(step)
        angles.append(source.tick().angle)

    dawn = angles[:120]  # before 05:00 local
    noon = angles[280:320]
    night = angles[-60:]
    assert max(dawn) == config.ANGLE_RESTING
    assert min(noon) >= config.ANGLE_BENT_ENOUGH
    assert max(night) == config.ANGLE_RESTING


def test_the_day_loops_so_the_demo_never_runs_dry():
    day = load_day(DEFAULT_DAY)
    player = DayPlayer(FakeSource(), day, sleep=nap)
    player.index = len(day.steps) + 5
    assert player.now.step == 5
