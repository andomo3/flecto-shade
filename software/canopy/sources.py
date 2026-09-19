"""Sources: readings out, commands in.

Every source speaks the same contract, so the state, the page, the recorder,
and the day player cannot tell a board from a file from a simulator.

``FixtureSource`` replays a recorded stream at its original pace.
``FakeSource`` stands in for the board and runs the same control law.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Awaitable, Callable
from pathlib import Path

from canopy import config, contract
from canopy.contract import Reading

Sleeper = Callable[[float], Awaitable[None]]


class Source(ABC):
    """One interface: iterate readings, and send commands back."""

    name: str = "source"

    @abstractmethod
    def readings(self) -> AsyncIterator[Reading]:
        """Yield readings until the source runs out, which a live one never does."""

    def send(self, command: str) -> None:
        """Accept a command line built by :mod:`canopy.contract`.

        A source that cannot act on a command ignores it, exactly as the board
        ignores one it does not know.
        """

    async def close(self) -> None:
        """Release whatever the source holds."""


class FixtureSource(Source):
    """Replay a file of v2 lines, paced by ``t_ms``, and loop when it ends."""

    name = "fixture"

    def __init__(
        self,
        path: str | Path,
        *,
        loop: bool = True,
        speed: float = 1.0,
        sleep: Sleeper = asyncio.sleep,
    ) -> None:
        self.path = Path(path)
        self.loop = loop
        self.speed = speed
        self._sleep = sleep
        self._commands: list[str] = []

    @property
    def commands(self) -> list[str]:
        """Every command sent to this source, which a file cannot act on."""
        return list(self._commands)

    def send(self, command: str) -> None:
        self._commands.append(command)

    def _parsed(self) -> list[Reading]:
        readings = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            parsed = contract.parse_line(line)
            if isinstance(parsed, Reading):
                readings.append(parsed)
        return readings

    async def readings(self) -> AsyncIterator[Reading]:
        readings = self._parsed()
        if not readings:
            return
        while True:
            previous_t_ms: int | None = None
            for reading in readings:
                if previous_t_ms is not None and self.speed > 0:
                    gap = (reading.t_ms - previous_t_ms) / 1000 / self.speed
                    if gap > 0:
                        await self._sleep(gap)
                previous_t_ms = reading.t_ms
                yield reading
            if not self.loop:
                return


class FakeSource(Source):
    """A board that is not there.

    It holds the LED duty, the sun angle, and the override the way the sketch
    does, runs the threshold with hysteresis and the rate limited servo step,
    and prints a reading every tick. The light it reports is the LED it was
    told to light, so the day player drives it exactly as it drives the board.
    """

    name = "fake"

    def __init__(
        self,
        *,
        sleep: Sleeper = asyncio.sleep,
        has_bench: bool = True,
        has_fixed: bool = False,
        has_flex: bool = True,
        has_temperature: bool = False,
    ) -> None:
        self._sleep = sleep
        self.has_bench = has_bench
        self.has_fixed = has_fixed
        self.has_flex = has_flex
        self.has_temperature = has_temperature

        self._t_ms = 0
        self._led = 0
        self._sun: int | None = None
        self._angle = float(config.ANGLE_RESTING)
        self._override = False
        self._commanded_angle: int | None = None
        self._running = True

    def send(self, command: str) -> None:
        text = command.strip()
        if not text:
            return
        letter, _, argument = text.partition(" ")
        value = int(argument) if argument.strip().lstrip("-").isdigit() else None

        if letter == "L" and value is not None and 0 <= value <= 255:
            self._led = value
        elif letter == "A" and value is not None and 0 <= value <= 180:
            self._sun = value
        elif letter == "S" and value is not None and 0 <= value <= 180:
            self._commanded_angle = value
            self._override = True
        elif letter == "O" and value in (0, 1):
            self._override = value == 1
            if not self._override:
                self._commanded_angle = None
        # Unknown commands and out of range arguments are ignored.

    async def close(self) -> None:
        self._running = False

    def _light(self) -> int:
        return round(self._led / 255 * 1000)

    def _step_angle(self, light: int) -> None:
        if self._override and self._commanded_angle is not None:
            target = float(self._commanded_angle)
        elif light >= config.BEND_LIGHT:
            target = float(config.ANGLE_BENT)
        elif light <= config.REST_LIGHT:
            target = float(config.ANGLE_RESTING)
        else:
            target = self._angle

        step = config.ANGLE_STEP_PER_TICK
        if target > self._angle:
            self._angle = min(target, self._angle + step)
        else:
            self._angle = max(target, self._angle - step)

    def _bench(self, light: int) -> int:
        travel = (self._angle - config.ANGLE_RESTING) / (
            config.ANGLE_BENT - config.ANGLE_RESTING
        )
        fraction = config.BENCH_FRACTION_RESTING + travel * (
            config.BENCH_FRACTION_BENT - config.BENCH_FRACTION_RESTING
        )
        return round(light * fraction)

    def tick(self) -> Reading:
        """Advance one tick and return the line the board would have printed."""
        light = self._light()
        self._step_angle(light)
        angle = round(self._angle)
        reading = Reading(
            t_ms=self._t_ms,
            light=light,
            bench=self._bench(light) if self.has_bench else None,
            fixed=round(light * config.BENCH_FRACTION_FIXED) if self.has_fixed else None,
            flex=round(angle / config.ANGLE_BENT * 700) if self.has_flex else None,
            temp_canopy=253 if self.has_temperature else None,
            temp_open=253 + round(angle / config.ANGLE_BENT * 40)
            if self.has_temperature
            else None,
            angle=angle,
            sun=self._sun,
            led=self._led,
            override=1 if self._override else 0,
        )
        self._t_ms += config.TICK_MS
        return reading

    async def readings(self) -> AsyncIterator[Reading]:
        while self._running:
            yield self.tick()
            await self._sleep(config.TICK_MS / 1000)


def open_source(name: str, *, fixture: str | Path | None = None, **kwargs) -> Source:
    """Build a source by the name the command line uses."""
    if name == "fixture":
        if fixture is None:
            raise ValueError("the fixture source needs a file")
        return FixtureSource(fixture, **kwargs)
    if name == "fake":
        return FakeSource(**kwargs)
    raise ValueError(f"unknown source {name!r}")
