"""What the page shows, derived from the stream and nothing else.

The two percentages, averaged separately while the leaves are bent and while
they are resting, the leaf state, which sensors are fitted, the cycle count,
the temperature difference, and whether the day has finished.

A sensor that is not fitted is absent here too, so the page can say "not
fitted" and never a zero.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from canopy import config
from canopy.contract import Reading

RESTING = "resting"
BENDING = "bending"
BENT = "bent"


@dataclass
class Series:
    """A running mean and spread, so the card can show both."""

    count: int = 0
    mean: float = 0.0
    _m2: float = 0.0
    low: float | None = None
    high: float | None = None

    def add(self, value: float) -> None:
        self.count += 1
        delta = value - self.mean
        self.mean += delta / self.count
        self._m2 += delta * (value - self.mean)
        self.low = value if self.low is None else min(self.low, value)
        self.high = value if self.high is None else max(self.high, value)

    @property
    def spread(self) -> float | None:
        """The sample standard deviation, once there are two readings."""
        if self.count < 2:
            return None
        return math.sqrt(self._m2 / (self.count - 1))

    def as_dict(self) -> dict[str, float | int | None]:
        return {
            "count": self.count,
            "mean": round(self.mean, 1) if self.count else None,
            "spread": round(self.spread, 1) if self.spread is not None else None,
            "low": round(self.low, 1) if self.low is not None else None,
            "high": round(self.high, 1) if self.high is not None else None,
        }


@dataclass
class State:
    """Fold the stream into the handful of things the screen needs."""

    reading: Reading | None = None
    leaves: str = RESTING
    cycles: int = 0
    day_finished: bool = False
    replay_mode: bool = False
    bent: Series = field(default_factory=Series)
    resting: Series = field(default_factory=Series)
    fixed: Series = field(default_factory=Series)
    _previous_angle: int | None = None
    _armed: bool = False

    def reset(self) -> None:
        """Between judges: forget the run, keep nothing but the source."""
        self.reading = None
        self.leaves = RESTING
        self.cycles = 0
        self.day_finished = False
        self.bent = Series()
        self.resting = Series()
        self.fixed = Series()
        self._previous_angle = None
        self._armed = False

    def update(self, reading: Reading) -> None:
        self.reading = reading
        self.leaves = self._leaf_state(reading)

        bench_percent = percent(reading.bench, reading.light)
        if bench_percent is not None:
            if self.leaves == BENT:
                self.bent.add(bench_percent)
            elif self.leaves == RESTING:
                self.resting.add(bench_percent)

        fixed_percent = percent(reading.fixed, reading.light)
        if fixed_percent is not None:
            self.fixed.add(fixed_percent)

        self._count_cycles(reading)
        self._previous_angle = reading.angle

    def _leaf_state(self, reading: Reading) -> str:
        if reading.angle >= config.ANGLE_BENT_ENOUGH:
            return BENT
        if reading.angle <= config.ANGLE_RESTING:
            return RESTING
        return BENDING

    def _count_cycles(self, reading: Reading) -> None:
        """One cycle: the light crosses the threshold, the leaves reach bent,
        and later they return."""
        if reading.light >= config.BEND_LIGHT and reading.angle >= config.ANGLE_BENT:
            self._armed = True
        elif self._armed and reading.angle <= config.ANGLE_RESTING:
            self.cycles += 1
            self._armed = False

    @property
    def temperature_difference(self) -> float | None:
        """Degrees, open minus canopy, only while both sensors are present."""
        reading = self.reading
        if reading is None or reading.temp_open is None or reading.temp_canopy is None:
            return None
        return round((reading.temp_open - reading.temp_canopy) / 10, 1)

    @property
    def fitted(self) -> dict[str, bool]:
        reading = self.reading
        present = reading.fitted if reading is not None else frozenset()
        return {
            "bench": "bench" in present,
            "fixed": "fixed" in present,
            "flex": "flex" in present,
            "temperature": {"temp_canopy", "temp_open"} <= set(present),
            "sun": "sun" in present,
        }

    def snapshot(self) -> dict:
        """One JSON safe object, the whole of what the page renders from."""
        reading = self.reading
        return {
            "waiting": reading is None,
            "t_ms": reading.t_ms if reading else None,
            "light": reading.light if reading else None,
            "bench": reading.bench if reading else None,
            "fixed": reading.fixed if reading else None,
            "flex": reading.flex if reading else None,
            "angle": reading.angle if reading else None,
            "sun": reading.sun if reading else None,
            "led": reading.led if reading else None,
            "override": reading.override if reading else None,
            "bench_percent": percent(reading.bench, reading.light) if reading else None,
            "fixed_percent": percent(reading.fixed, reading.light) if reading else None,
            "leaves": self.leaves,
            "cycles": self.cycles,
            "temperature_difference": self.temperature_difference,
            "fitted": self.fitted,
            "day_finished": self.day_finished,
            "replay_mode": self.replay_mode,
            "averages": {
                "bent": self.bent.as_dict(),
                "resting": self.resting.as_dict(),
                "fixed": self.fixed.as_dict(),
            },
        }


def percent(part: int | None, whole: int | None) -> float | None:
    """``part / whole * 100``, or nothing when either is missing or dark."""
    if part is None or not whole:
        return None
    return round(part / whole * 100, 1)
