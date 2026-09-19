"""C9: keep the run.

The recorder writes every line the source produced, byte for byte, with the
header in front of it. Nothing is reformatted, rounded, or filled in, so a
recorded file is evidence: it replays through the same parser and the same
page as the board did, and the numbers on the result card cannot drift.

That is also the fallback. If the board dies at 02:00, this morning's recorded
run still plays the demo, and the page says in words where its numbers came
from.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from canopy import contract
from canopy.sources import Source

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class Recorder:
    """Write the raw stream to a file, and say how much of it there was."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.lines = 0
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("w", encoding="utf-8", newline="\n")
        self._write(contract.HEADER_LINE)

    def _write(self, line: str) -> None:
        self._handle.write(line + "\n")

    def record(self, line: str) -> None:
        """One line in, one line out, unchanged."""
        text = line.rstrip("\r\n")
        if not text:
            return
        self._write(text)
        self.lines += 1
        self._handle.flush()

    def attach(self, source: Source) -> Recorder:
        """Record everything a source sees from now on."""
        source.observe(self.record)
        return self

    def close(self) -> None:
        if not self._handle.closed:
            self._handle.close()

    def __enter__(self) -> Recorder:
        return self

    def __exit__(self, *_exception: object) -> None:
        self.close()


def run_path(name: str | None = None, *, now: datetime | None = None) -> Path:
    """``fixtures/run-YYYYmmdd-HHMM.csv``, named after when it was taken."""
    stamp = (now or datetime.now()).strftime("%Y%m%d-%H%M")
    return FIXTURES / f"run-{stamp}{'-' + name if name else ''}.csv"
