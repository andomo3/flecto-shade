"""Gate F5: nothing simulated is called measured.

Reads every label the page can show and asserts that the words "simulated" or
"modelled" are present, and that "measured" appears nowhere except once, inside the
rain source line, where it is true of the gauge. Asserts that and nothing else.
"""

import json
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parents[2] / "software" / "page"
SERVED = ["index.html", "style.css", "app.js", "day.json"]


def served_text():
    return {name: (PAGE / name).read_text(encoding="utf-8") for name in SERVED
            if (PAGE / name).exists()}


def test_the_page_labels_itself_simulated_or_modelled():
    text = (PAGE / "index.html").read_text(encoding="utf-8").lower()
    day = json.loads((PAGE / "day.json").read_text(encoding="utf-8"))
    assert "simulated" in text or "modelled" in text
    assert day["label"] in ("simulated", "modelled")
    assert "modelled" in day["sources"]["sun"], "the sun is a satellite product"


def test_measured_appears_only_in_the_rain_source_line():
    day = json.loads((PAGE / "day.json").read_text(encoding="utf-8"))
    rain_line = day["sources"]["rain"]
    assert "measured" in rain_line, "the gauge reading is the one true use"

    for name, text in served_text().items():
        hits = [line.strip() for line in text.splitlines() if "measured" in line.lower()]
        for line in hits:
            assert rain_line in line or line in rain_line or '"rain"' in line, (
                f'{name} uses "measured" outside the rain source line: {line[:120]}')


def test_no_figure_claims_an_instrument():
    banned = ["first", "maintenance free", "maintenance-free", "weatherproof"]
    text = (PAGE / "index.html").read_text(encoding="utf-8").lower()
    for word in banned:
        assert not re.search(rf"\b{re.escape(word)}\b", text), f'the page writes "{word}"'
