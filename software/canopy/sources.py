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
Listener = Callable[[str], None]


class Source(ABC):
    """One interface: iterate readings, and send commands back.

    A source also hands out the raw line behind each reading, so the recorder
    can keep the stream exactly as it arrived rather than a re-rendering of it.
    """

    name: str = "source"
    _line_listeners: list[Listener] | None = None

    def observe(self, listener: Listener) -> None:
        """Call ``listener`` with every raw line this source sees."""
        if self._line_listeners is None:
            self._line_listeners = []
        self._line_listeners.append(listener)

    def _emit(self, line: str) -> None:
        for listener in self._line_listeners or ():
            listener(line)

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

    def _parsed(self) -> list[tuple[str, Reading]]:
        readings = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            parsed = contract.parse_line(line)
            if isinstance(parsed, Reading):
                readings.append((line, parsed))
        return readings

    async def readings(self) -> AsyncIterator[Reading]:
        readings = self._parsed()
        if not readings:
            return
        while True:
            previous_t_ms: int | None = None
            for line, reading in readings:
                if previous_t_ms is not None and self.speed > 0:
                    gap = (reading.t_ms - previous_t_ms) / 1000 / self.speed
                    if gap > 0:
                        await self._sleep(gap)
                previous_t_ms = reading.t_ms
                self._emit(line)
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

    @property
    def commanded_angle(self) -> int | None:
        """The angle held by replay mode, or ``None`` when the light decides."""
        return self._commanded_angle

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
            reading = self.tick()
            self._emit(contract.to_line(reading))
            yield reading
            await self._sleep(config.TICK_MS / 1000)


class SerialSource(Source):
    """The board on a USB cable.

    Reading the port blocks, so it happens on a worker thread and the loop
    stays free for the page. A line that does not parse is dropped, which is
    what lets the app connect in the middle of a stream.
    """

    name = "serial"

    def __init__(self, port: str, *, baud: int = 115200, timeout: float = 1.0) -> None:
        import serial  # Imported here so the demo runs on a laptop with no pyserial.

        self.port = port
        self._serial = serial.Serial(port, baud, timeout=timeout)

    def send(self, command: str) -> None:
        self._serial.write(command.encode("ascii"))

    async def close(self) -> None:
        self._serial.close()

    async def readings(self) -> AsyncIterator[Reading]:
        while self._serial.is_open:
            raw = await asyncio.to_thread(self._serial.readline)
            if not raw:
                continue
            line = raw.decode("ascii", errors="replace").rstrip("\r\n")
            self._emit(line)
            parsed = contract.parse_line(line)
            if isinstance(parsed, Reading):
                yield parsed


def open_source(name: str, *, fixture: str | Path | None = None, **kwargs) -> Source:
    """Build a source by the name the command line uses."""
    if name == "fixture":
        if fixture is None:
            raise ValueError("the fixture source needs a file")
        return FixtureSource(fixture, **kwargs)
    if name == "fake":
        return FakeSource(**kwargs)
    if name == "serial":
        return SerialSource(**kwargs)
    raise ValueError(f"unknown source {name!r}")
