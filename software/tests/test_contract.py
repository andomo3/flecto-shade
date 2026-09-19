"""C1: the parser is checked against the contract file itself.

The sample lines are read out of ``planning/firmware/SERIAL_FORMAT.md`` rather
than copied here, so a change to the contract breaks this test the moment it
lands.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from canopy import contract

CONTRACT_FILE = (
    Path(__file__).resolve().parents[2] / "planning" / "firmware" / "SERIAL_FORMAT.md"
)


def _sample_lines() -> list[str]:
    """Every line of the fenced block that holds the parser's samples."""
    text = CONTRACT_FILE.read_text(encoding="utf-8")
    blocks = re.findall(r"```\n(.*?)```", text, flags=re.DOTALL)
    for block in blocks:
        lines = [line for line in block.splitlines() if line.strip()]
        if lines and lines[0] == contract.HEADER_LINE and len(lines) > 1:
            return lines
    raise AssertionError("no sample block found in the contract file")


SAMPLES = _sample_lines()


def test_contract_file_is_present():
    assert CONTRACT_FILE.exists()
    assert len(SAMPLES) >= 5


def test_every_sample_line_parses():
    for line in SAMPLES:
        assert contract.parse_line(line) is not None, line


def test_the_header_gives_the_version():
    header = contract.parse_line(SAMPLES[0])
    assert isinstance(header, contract.Header)
    assert header.version == contract.VERSION


def test_an_early_line_shows_only_the_incident_sensor():
    reading = contract.parse_line(SAMPLES[1])
    assert isinstance(reading, contract.Reading)
    assert reading.t_ms == 1200
    assert reading.light == 212
    assert reading.bench is None
    assert reading.temp_open is None
    assert reading.angle == 0
    assert reading.led == 40
    assert reading.override == 0
    assert reading.fitted == frozenset()


def test_a_full_line_carries_every_sensor():
    reading = contract.parse_line(SAMPLES[-1])
    assert isinstance(reading, contract.Reading)
    assert reading.light == 791
    assert reading.bench == 187
    assert reading.fixed == 610
    assert reading.flex == 661
    assert reading.temp_canopy == 253
    assert reading.temp_open == 268
    assert reading.angle == 125
    assert reading.sun == 90
    assert reading.led == 255
    assert reading.override == 1
    assert reading.fitted == frozenset(
        {"bench", "fixed", "flex", "temp_canopy", "temp_open", "sun"}
    )


def test_an_empty_optional_field_is_none_and_never_zero():
    reading = contract.parse_line("61000,790,,,655,,,124,,255,0")
    assert isinstance(reading, contract.Reading)
    assert reading.bench is None
    assert reading.flex == 655
    assert reading.fitted == frozenset({"flex"})


def test_negative_temperatures_parse():
    reading = contract.parse_line("900,5,,,,-21,-18,0,,0,0")
    assert isinstance(reading, contract.Reading)
    assert reading.temp_canopy == -21
    assert reading.temp_open == -18


GARBAGE = [
    "",
    "   ",
    "hello",
    "# canopy",
    "# canopy v",
    "# canopy vX",
    "# something else v2",
    "1200,212,,,,,,0,,40",  # ten fields
    "1200,212,,,,,,0,,40,0,0",  # twelve fields
    "1200,212,,,,,,0,,40,2",  # override out of range
    "1200,1212,,,,,,0,,40,0",  # light out of range
    "1200,212,,,,,,0,,400,0",  # led out of range
    "1200,212,,,,,,181,,40,0",  # angle out of range
    "1200,,,,,,,0,,40,0",  # light is not optional
    ",212,,,,,,0,,40,0",  # t_ms is not optional
    "1200,21.2,,,,,,0,,40,0",  # not an integer
    "1200,0x2,,,,,,0,,40,0",
    "1200,212,,,,,,0,,40,0\r\nextra,line",
]


@pytest.mark.parametrize("line", GARBAGE)
def test_garbage_returns_nothing(line):
    assert contract.parse_line(line) is None


def test_the_commands_are_the_bytes_the_board_reads():
    assert contract.led(0) == "L 0\n"
    assert contract.led(255) == "L 255\n"
    assert contract.sun_angle(90) == "A 90\n"
    assert contract.leaf_angle(124) == "S 124\n"
    assert contract.override(True) == "O 1\n"
    assert contract.override(False) == "O 0\n"
    assert contract.ping() == "P\n"


@pytest.mark.parametrize(
    "call",
    [
        lambda: contract.led(256),
        lambda: contract.led(-1),
        lambda: contract.sun_angle(181),
        lambda: contract.leaf_angle(-5),
    ],
)
def test_an_out_of_range_command_is_refused(call):
    with pytest.raises(ValueError):
        call()
