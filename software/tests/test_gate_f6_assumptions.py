"""Gate F6: every assumed constant is declared.

Every named constant the packages mark ASSUMED or RECALLED appears in the section
"Assumptions" of data/README.md with its value. Asserts that and nothing else.
"""

import importlib.util
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
README = REPO_ROOT / "data" / "README.md"
BUILD = REPO_ROOT / "software" / "h1" / "build.py"


def assumptions_section():
    text = README.read_text(encoding="utf-8")
    start = text.index("## Assumptions")
    rest = text[start + len("## Assumptions"):]
    end = rest.find("\n## ")
    return rest if end == -1 else rest[:end]


def load_build():
    spec = importlib.util.spec_from_file_location("h1_build", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def declared(section, name, value):
    """The constant's name and its value both appear in the same row of the table."""
    for line in section.splitlines():
        if f"`{name}`" not in line:
            continue
        numbers = re.findall(r"-?\d+(?:\.\d+)?", line)
        if isinstance(value, str):
            return value in line
        return any(abs(float(found) - float(value)) < 1e-9 for found in numbers)
    return False


def test_the_section_exists():
    assert "## Assumptions" in README.read_text(encoding="utf-8")
    assert assumptions_section().strip(), "the Assumptions section is empty"


def test_every_assumed_and_recalled_constant_is_declared_with_its_value():
    build = load_build()
    section = assumptions_section()
    missing = []
    for name, value in {**build.ASSUMED_CONSTANTS, **build.RECALLED_CONSTANTS}.items():
        if not declared(section, name, value):
            missing.append(f"{name} = {value}")
    assert not missing, "not declared in data/README.md with their values: " + ", ".join(missing)


def test_every_constant_carries_its_label():
    section = assumptions_section()
    build = load_build()
    for name in build.ASSUMED_CONSTANTS:
        row = next(line for line in section.splitlines() if f"`{name}`" in line)
        assert "ASSUMED" in row, f"{name} has no label"
    for name in build.RECALLED_CONSTANTS:
        row = next(line for line in section.splitlines() if f"`{name}`" in line)
        assert "RECALLED" in row, f"{name} has no label"
