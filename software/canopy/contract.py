"""Serial contract, version 2.

One line in, a header, a reading, or nothing.
Commands out, as the bytes the board reads.
Standard library only, so every other module can depend on this one.

The field list, the ranges, and the samples come from
``planning/firmware/SERIAL_FORMAT.md``, which is the contract itself.
"""

from __future__ import annotations

from dataclasses import dataclass

VERSION = 2

HEADER_LINE = f"# canopy v{VERSION}"

FIELD_NAMES = (
    "t_ms",
    "light",
    "bench",
    "fixed",
    "flex",
    "temp_canopy",
    "temp_open",
    "angle",
    "sun",
    "led",
    "override",
)

OPTIONAL_FIELDS = frozenset(
    {"bench", "fixed", "flex", "temp_canopy", "temp_open", "sun"}
)

# Inclusive bounds. A field with no bound is only checked for being an integer,
# and the temperatures are tenths of a degree and may be negative.
FIELD_RANGES: dict[str, tuple[int, int]] = {
    "t_ms": (0, 2**32 - 1),
    "light": (0, 1000),
    "bench": (0, 1000),
    "fixed": (0, 1000),
    "flex": (0, 1000),
    "angle": (0, 180),
    "sun": (0, 180),
    "led": (0, 255),
    "override": (0, 1),
}


@dataclass(frozen=True)
class Header:
    """The line the board prints at boot and every ten seconds."""

    version: int


@dataclass(frozen=True)
class Reading:
    """One data line: eleven fields, six of which may be absent."""

    t_ms: int
    light: int
    bench: int | None
    fixed: int | None
    flex: int | None
    temp_canopy: int | None
    temp_open: int | None
    angle: int
    sun: int | None
    led: int
    override: int

    @property
    def fitted(self) -> frozenset[str]:
        """The optional sensors that sent a value on this line."""
        return frozenset(
            name for name in OPTIONAL_FIELDS if getattr(self, name) is not None
        )


def to_line(reading: Reading) -> str:
    """The line a board would have printed for this reading.

    An absent sensor is an empty field, never a zero, because a zero is a
    measurement and an empty field is the truth.
    """
    return ",".join(
        "" if getattr(reading, name) is None else str(getattr(reading, name))
        for name in FIELD_NAMES
    )


def parse_line(line: str) -> Header | Reading | None:
    """Parse one line of the stream, or return None if it is not one.

    Every line is told apart by its first character, so a reader that
    connects mid stream can throw away whatever it does not recognise.
    """
    text = line.strip()
    if not text:
        return None
    if text.startswith("#"):
        return _parse_header(text)
    return _parse_reading(text)


def _parse_header(text: str) -> Header | None:
    parts = text.split()
    if len(parts) != 3 or parts[1] != "canopy":
        return None
    version = parts[2]
    if not version.startswith("v") or not version[1:].isdigit():
        return None
    return Header(version=int(version[1:]))


def _parse_reading(text: str) -> Reading | None:
    fields = text.split(",")
    if len(fields) != len(FIELD_NAMES):
        return None

    values: dict[str, int | None] = {}
    for name, raw in zip(FIELD_NAMES, fields):
        raw = raw.strip()
        if raw == "":
            if name not in OPTIONAL_FIELDS:
                return None
            values[name] = None
            continue
        value = _as_int(raw)
        if value is None:
            return None
        bounds = FIELD_RANGES.get(name)
        if bounds is not None and not bounds[0] <= value <= bounds[1]:
            return None
        values[name] = value

    return Reading(**values)  # type: ignore[arg-type]


def _as_int(raw: str) -> int | None:
    body = raw[1:] if raw[0] == "-" else raw
    if not body.isdigit():
        return None
    return int(raw)


def override(on: bool) -> str:
    """``O 1`` and ``O 0``: take the leaves off the photoresistor, or hand them back."""
    return f"O {1 if on else 0}\n"


def led(duty: int) -> str:
    """``L 0`` to ``L 255``: the LED sun brightness, the PWM duty."""
    return f"L {_checked('led', duty)}\n"


def sun_angle(degrees: int) -> str:
    """``A 0`` to ``A 180``: the sun mount servo angle."""
    return f"A {_checked('sun', degrees)}\n"


def leaf_angle(degrees: int) -> str:
    """``S 0`` to ``S 180``: replay mode, the leaf servo angle set directly.

    The normal demo never sends this, because only the light moves the leaves.
    """
    return f"S {_checked('angle', degrees)}\n"


def ping() -> str:
    """``P``: the board answers with the header line."""
    return "P\n"


def _checked(field: str, value: int) -> int:
    low, high = FIELD_RANGES[field]
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{field} must be an int, got {value!r}")
    if not low <= value <= high:
        raise ValueError(f"{field} must be {low} to {high}, got {value}")
    return value
