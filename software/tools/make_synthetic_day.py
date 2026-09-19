"""Write ``fixtures/synthetic-day.csv``: one fast forward day, no board needed.

Sixty seconds of ten hertz lines, a sun that rises and sets, and leaves that
bend and rest under the same control law the fake board runs. The bench and
flex sensors are fitted from the start, the temperatures are not, so the page
has both a fitted and a "not fitted" field to render before any hardware
exists.

Run: ``python tools/make_synthetic_day.py``
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from canopy import config, contract  # noqa: E402
from canopy.sources import FakeSource  # noqa: E402

ROWS = 600
OUT = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic-day.csv"


def led_for(step: int) -> int:
    """A day: dark, a climb to noon, and dark again."""
    day = math.sin(math.pi * step / ROWS)
    return max(0, round(255 * (day**1.6)))


def main() -> None:
    board = FakeSource(has_bench=True, has_flex=True, has_temperature=False)
    lines = [contract.HEADER_LINE]
    for step in range(ROWS):
        board.send(contract.led(led_for(step)))
        reading = board.tick()
        if step and reading.t_ms % 10_000 == 0:
            lines.append(contract.HEADER_LINE)
        lines.append(
            ",".join(
                "" if getattr(reading, name) is None else str(getattr(reading, name))
                for name in contract.FIELD_NAMES
            )
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"{OUT}: {len(lines)} lines, {config.TICK_MS} ms apart")


if __name__ == "__main__":
    main()
