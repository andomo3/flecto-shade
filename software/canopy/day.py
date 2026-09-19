"""C7: play the real Houston day into whatever source is connected.

The day is a file of 600 steps. Ten times a second the player sends one ``L``
for the lamp and one ``A`` for the sun arm, so twenty four hours pass in about
sixty seconds. The board, the fake board, and the simulator all take the same
two commands, so the player never knows which one it is driving.

The player only ever sends light. What the leaves do about that light is the
board's decision, not the laptop's, which is the whole point of the demo.
"""

from __future__ import annotations

import asyncio
import csv
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path

from canopy import config, contract
from canopy.sources import Source

PROCESSED = Path(__file__).resolve().parents[2] / "data" / "processed"
DEFAULT_DAY = PROCESSED / "day-houston.csv"

Sleeper = Callable[[float], Awaitable[None]]


@dataclass(frozen=True)
class Step:
    """One step of the day, as the file has it."""

    step: int
    local_time: str
    ghi: float
    elevation: float
    azimuth: float
    t2m: float
    led: int
    sun_angle: int


@dataclass(frozen=True)
class Day:
    """A day the player can play, and the facts the page says out loud."""

    city: str
    date: str
    steps: list[Step]

    @property
    def peak_ghi(self) -> float:
        return max(step.ghi for step in self.steps)

    @property
    def peak_t2m(self) -> float:
        return max(step.t2m for step in self.steps)

    def at(self, index: int) -> Step:
        return self.steps[index % len(self.steps)]


def load_day(path: str | Path = DEFAULT_DAY) -> Day:
    """Read a ``data/processed/day-<city>.csv`` written by ``tools/build_day.py``."""
    path = Path(path)
    steps = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            steps.append(
                Step(
                    step=int(row["step"]),
                    local_time=row["local_time"],
                    ghi=float(row["ghi"]),
                    elevation=float(row["elevation"]),
                    azimuth=float(row["azimuth"]),
                    t2m=float(row["t2m"]),
                    led=int(row["led"]),
                    sun_angle=int(row["sun_angle"]),
                )
            )
    if not steps:
        raise ValueError(f"{path}: no steps")
    city = path.stem.removeprefix("day-")
    return Day(city=city, date=steps[0].local_time[:10], steps=steps)


class DayPlayer:
    """Sends the day to a source, one step every ``TICK_MS``."""

    def __init__(
        self,
        source: Source,
        day: Day | None = None,
        *,
        loop: bool = True,
        replay_mode: bool = False,
        sleep: Sleeper = asyncio.sleep,
    ) -> None:
        self.source = source
        self.day = day or load_day()
        self.loop = loop
        self.replay_mode = replay_mode
        self._sleep = sleep
        self.index = 0

    @property
    def now(self) -> Step:
        return self.day.at(self.index)

    def send_step(self, step: Step) -> None:
        """One step: the lamp, the sun arm, and in replay mode the leaves too."""
        self.source.send(contract.led(step.led))
        self.source.send(contract.sun_angle(step.sun_angle))
        if self.replay_mode:
            bent = step.led >= round(config.BEND_LIGHT / 1000 * 255)
            angle = config.ANGLE_BENT if bent else config.ANGLE_RESTING
            self.source.send(contract.leaf_angle(angle))

    async def play(self, steps: int | None = None) -> None:
        """Play ``steps`` steps, or the whole day, or forever when looping."""
        remaining = steps if steps is not None else len(self.day.steps)
        played = 0
        while played < remaining:
            self.send_step(self.day.at(self.index))
            self.index += 1
            played += 1
            if not self.loop and self.index >= len(self.day.steps):
                break
            await self._sleep(config.TICK_MS / 1000)
