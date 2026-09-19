"""C9: a recorded run is evidence, so every line survives unchanged."""

from __future__ import annotations

import asyncio
from datetime import datetime

from canopy import contract
from canopy.recorder import Recorder, run_path
from canopy.sources import FakeSource, FixtureSource

LINES = [
    "# canopy v2",
    "1200,845,152,,690,,,125,90,255,0",
    "1300,845,151,,691,,,125,90,255,0",
    "1400,0,0,,0,,,0,90,0,0",
]


async def nap(_seconds: float) -> None:
    pass


def fixture_file(tmp_path):
    path = tmp_path / "run.csv"
    path.write_text("\n".join(LINES) + "\n", encoding="utf-8", newline="\n")
    return path


def test_every_source_line_is_written_back_byte_for_byte(tmp_path):
    source = FixtureSource(fixture_file(tmp_path), loop=False, sleep=nap)
    out = tmp_path / "recorded.csv"

    async def run():
        with Recorder(out).attach(source):
            async for _reading in source.readings():
                pass

    asyncio.run(run())

    written = out.read_text(encoding="utf-8").splitlines()
    assert written[0] == contract.HEADER_LINE
    assert written[1:] == [line for line in LINES if not line.startswith("#")]


def test_a_recording_replays_through_the_same_parser(tmp_path):
    source = FakeSource(has_bench=True)
    out = tmp_path / "recorded.csv"
    recorder = Recorder(out).attach(source)

    async def run():
        source.send(contract.led(255))
        count = 0
        async for _reading in source.readings():
            count += 1
            if count == 40:
                await source.close()
        recorder.close()

    asyncio.run(run())

    replayed = FixtureSource(out, loop=False, sleep=nap)

    async def collect():
        return [reading async for reading in replayed.readings()]

    readings = asyncio.run(collect())
    assert len(readings) == recorder.lines == 40
    assert max(reading.angle for reading in readings) > 0


def test_an_absent_sensor_stays_absent_through_a_recording(tmp_path):
    source = FakeSource(has_bench=False, has_flex=False, has_temperature=False)
    out = tmp_path / "recorded.csv"
    recorder = Recorder(out).attach(source)

    async def run():
        count = 0
        async for _reading in source.readings():
            count += 1
            if count == 3:
                await source.close()
        recorder.close()

    asyncio.run(run())

    for line in out.read_text(encoding="utf-8").splitlines()[1:]:
        reading = contract.parse_line(line)
        assert reading is not None
        assert reading.bench is None and reading.flex is None
        assert ",," in line  # empty fields, never zeroes


def test_blank_lines_are_not_recorded(tmp_path):
    out = tmp_path / "recorded.csv"
    with Recorder(out) as recorder:
        recorder.record("")
        recorder.record("1200,845,152,,690,,,125,90,255,0\r\n")
    assert recorder.lines == 1
    assert out.read_text(encoding="utf-8").splitlines() == [
        contract.HEADER_LINE,
        "1200,845,152,,690,,,125,90,255,0",
    ]


def test_a_run_is_named_after_when_it_was_taken():
    path = run_path("serial", now=datetime(2026, 9, 20, 2, 5))
    assert path.name == "run-20260920-0205-serial.csv"
    assert path.parent.name == "fixtures"
