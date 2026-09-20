"""Each test builds a small git repo in a temporary directory and runs the gate
runner against it, so nothing here depends on the state of this repo."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
GATES = TOOLS / "gates.py"
EM_DASH = "\u2014"


def git(repo: Path, *args: str) -> None:
    env = os.environ | {
        "GIT_AUTHOR_NAME": "gates",
        "GIT_AUTHOR_EMAIL": "gates@test",
        "GIT_COMMITTER_NAME": "gates",
        "GIT_COMMITTER_EMAIL": "gates@test",
    }
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    (tmp_path / "README.md").write_text("# a repo\n", encoding="utf-8")
    (tmp_path / "planning").mkdir()
    (tmp_path / "planning" / "plan.md").write_text("a plan\n", encoding="utf-8")
    git(tmp_path, "add", "README.md", "planning/plan.md")
    git(tmp_path, "commit", "-q", "-m", "start")
    return tmp_path


def gates(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GATES), "--root", str(repo), *args],
        capture_output=True,
        text=True,
        timeout=120,
    )


def result_of(output: str, gate: str) -> str:
    for line in output.splitlines():
        cells = [c.strip() for c in line.split("|")]
        if len(cells) > 2 and cells[1] == gate:
            return cells[2]
    raise AssertionError(f"no row for {gate} in:\n{output}")


def test_empty_repo_prints_fourteen_rows_and_exits_zero(repo: Path) -> None:
    run = gates(repo)
    rows = [line for line in run.stdout.splitlines() if line.startswith("| F")]
    assert len(rows) == 14
    assert "FAIL" not in run.stdout
    assert run.returncode == 0
    assert "Milestone gates M1 to M4 are checked by a person" in run.stdout


def test_changed_planning_file_fails_f9(repo: Path) -> None:
    (repo / "planning" / "plan.md").write_text("changed\n", encoding="utf-8")
    run = gates(repo)
    assert result_of(run.stdout, "F9") == "FAIL"
    assert run.returncode == 1


def test_change_outside_allowed_fails_f10(repo: Path) -> None:
    (repo / "tools").mkdir()
    (repo / "tools" / "x.py").write_text("", encoding="utf-8")
    (repo / "stray.txt").write_text("", encoding="utf-8")
    run = gates(repo, "--package", "X1", "--allowed", "tools/")
    assert result_of(run.stdout, "F10") == "FAIL"
    assert "stray.txt" in run.stdout
    (repo / "stray.txt").unlink()
    run = gates(repo, "--package", "X1", "--allowed", "tools/")
    assert result_of(run.stdout, "F10") == "PASS"


def test_f10_is_not_yet_without_a_package(repo: Path) -> None:
    assert result_of(gates(repo).stdout, "F10") == "NOT YET"


def test_tracked_raw_data_fails_f11(repo: Path) -> None:
    (repo / "data" / "raw").mkdir(parents=True)
    (repo / "data" / "raw" / "big.csv").write_text("1\n", encoding="utf-8")
    git(repo, "add", "-f", "data/raw/big.csv")
    assert result_of(gates(repo).stdout, "F11") == "FAIL"


def test_tracked_env_file_fails_f11(repo: Path) -> None:
    (repo / ".env").write_text("KEY=x\n", encoding="utf-8")
    git(repo, "add", ".env")
    assert result_of(gates(repo).stdout, "F11") == "FAIL"


def test_tracked_file_over_five_megabytes_fails_f11(repo: Path) -> None:
    (repo / "blob.bin").write_bytes(b"\0" * (5 * 1024 * 1024 + 1))
    git(repo, "add", "blob.bin")
    assert result_of(gates(repo).stdout, "F11") == "FAIL"


def test_em_dash_outside_planning_fails_f13_and_inside_does_not(repo: Path) -> None:
    (repo / "planning" / "plan.md").write_text(f"fine {EM_DASH} here\n", encoding="utf-8")
    git(repo, "commit", "-q", "-am", "planning may use it")
    assert result_of(gates(repo).stdout, "F13") == "PASS"
    (repo / "README.md").write_text(f"not {EM_DASH} here\n", encoding="utf-8")
    assert result_of(gates(repo).stdout, "F13") == "FAIL"


def test_unpinned_requirement_fails_f12(repo: Path) -> None:
    assert result_of(gates(repo).stdout, "F12") == "NOT YET"
    req = repo / "software" / "requirements.txt"
    req.parent.mkdir()
    req.write_text("pandas==2.2.3\npytest\n", encoding="utf-8")
    assert result_of(gates(repo).stdout, "F12") == "FAIL"
    req.write_text("pandas==2.2.3\npytest==9.0.2\n", encoding="utf-8")
    assert result_of(gates(repo).stdout, "F12") == "PASS"


def test_external_script_fails_f3_but_not_in_a_comment(repo: Path) -> None:
    assert result_of(gates(repo).stdout, "F3") == "NOT YET"
    page = repo / "software" / "page" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text('<script src="https://cdn.example/x.js"></script>\n', encoding="utf-8")
    assert result_of(gates(repo).stdout, "F3") == "FAIL"
    page.write_text('<!-- <script src="https://cdn.example/x.js"></script> -->\n<p>hi</p>\n', encoding="utf-8")
    assert result_of(gates(repo).stdout, "F3") == "PASS"
    css = page.parent / "style.css"
    css.write_text("body { background: url(//cdn.example/a.png); }\n", encoding="utf-8")
    assert result_of(gates(repo).stdout, "F3") == "FAIL"


def test_failing_test_fails_f1_and_no_tests_is_not_yet(repo: Path) -> None:
    assert result_of(gates(repo).stdout, "F1") == "NOT YET"
    tests = repo / "software" / "tests"
    tests.mkdir(parents=True)
    (tests / "test_bad.py").write_text("def test_bad():\n    assert False\n", encoding="utf-8")
    run = gates(repo)
    assert result_of(run.stdout, "F1") == "FAIL"
    assert run.returncode == 1
    (tests / "test_bad.py").write_text("def test_good():\n    assert True\n", encoding="utf-8")
    assert result_of(gates(repo).stdout, "F1") == "PASS"


def test_gate_test_files_are_found_by_name(repo: Path) -> None:
    assert result_of(gates(repo).stdout, "F4") == "NOT YET"
    tests = repo / "software" / "tests"
    tests.mkdir(parents=True)
    (tests / "test_gate_f4_schema.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    assert result_of(gates(repo).stdout, "F4") == "PASS"


@pytest.mark.parametrize("filename", ["test_h1_year.py", "test_headline_year.py"])
def test_year_failure_is_reported_without_blocking_f1(repo: Path, filename: str) -> None:
    tests = repo / "software" / "tests"
    tests.mkdir(parents=True)
    (tests / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")
    (tests / filename).write_text("def test_year():\n    assert False\n", encoding="utf-8")
    run = gates(repo, "--package", "X1", "--allowed", "software/", "--append")
    assert result_of(run.stdout, "F1") == "PASS"
    assert "The year: FAIL" in run.stdout
    assert run.returncode == 0
    assert "The year: FAIL" in (repo / "gates-log" / "X1.md").read_text(encoding="utf-8")


def test_both_year_files_run_and_passing_year_cannot_hide_demo_failure(repo: Path) -> None:
    tests = repo / "software" / "tests"
    tests.mkdir(parents=True)
    for filename in ("test_h1_year.py", "test_headline_year.py"):
        (tests / filename).write_text("def test_year():\n    assert True\n", encoding="utf-8")
    (tests / "test_demo.py").write_text("def test_demo():\n    assert False\n", encoding="utf-8")
    run = gates(repo)
    assert result_of(run.stdout, "F1") == "FAIL"
    assert "FAILED software/tests/test_demo.py::test_demo" in run.stdout
    assert "The year: PASS - 2 passed" in run.stdout
    assert run.returncode == 1


def test_only_year_checks_leave_f1_not_yet(repo: Path) -> None:
    tests = repo / "software" / "tests"
    tests.mkdir(parents=True)
    (tests / "test_h1_year.py").write_text("def test_year():\n    assert False\n", encoding="utf-8")
    run = gates(repo)
    assert result_of(run.stdout, "F1") == "NOT YET"
    assert "The year: FAIL" in run.stdout
    assert run.returncode == 0


def test_missing_year_is_reported_not_yet(repo: Path) -> None:
    run = gates(repo)
    assert "The year: NOT YET" in run.stdout
    assert run.returncode == 0


def test_year_collection_error_does_not_hide_demo_tests(repo: Path) -> None:
    tests = repo / "software" / "tests"
    tests.mkdir(parents=True)
    (tests / "test_h1_year.py").write_text("raise RuntimeError('broken year')\n", encoding="utf-8")
    (tests / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")
    run = gates(repo)
    assert result_of(run.stdout, "F1") == "PASS"
    assert "The year: FAIL" in run.stdout
    assert run.returncode == 0


def test_offline_build_cannot_open_a_socket(repo: Path) -> None:
    data = repo / "data"
    data.mkdir()
    (data / "build_solar_2023.py").write_text("import socket\nsocket.socket()\n", encoding="utf-8")
    run = gates(repo)
    assert result_of(run.stdout, "F2") == "FAIL"
    assert "network is off for gate F2" in run.stdout
    assert run.returncode == 1


def test_offline_page_builder_and_local_server(repo: Path) -> None:
    page = repo / "software" / "page"
    page.mkdir(parents=True)
    (page / "build_day.py").write_text(
        "import sys\nfrom pathlib import Path\n"
        "assert sys.argv[1:] == ['--date', '2023-06-03']\n"
        "Path(__file__).with_name('index.html').write_text('<h1>simulated shade house</h1>')\n",
        encoding="utf-8",
    )
    run = gates(repo)
    assert result_of(run.stdout, "F2") == "PASS"
    assert "HTTP 200 on loopback" in run.stdout
    assert run.returncode == 0


def test_missing_page_entrypoint_fails_f2(repo: Path) -> None:
    page = repo / "software" / "page"
    page.mkdir(parents=True)
    (page / "app.js").write_text("", encoding="utf-8")
    run = gates(repo)
    assert result_of(run.stdout, "F2") == "FAIL"
    assert "index.html is missing" in run.stdout
    assert run.returncode == 1


def test_append_twice_writes_two_sections_to_the_package_file(repo: Path) -> None:
    before = set(p.relative_to(repo) for p in repo.rglob("*") if ".git" not in p.parts)
    gates(repo, "--package", "X1", "--allowed", "gates-log/", "--append")
    gates(repo, "--package", "X1", "--allowed", "gates-log/", "--append")
    log = repo / "gates-log" / "X1.md"
    text = log.read_text(encoding="utf-8")
    assert text.count("\n## ") == 2
    assert text.count("Package: X1") == 2
    after = set(p.relative_to(repo) for p in repo.rglob("*") if ".git" not in p.parts)
    assert after - before == {Path("gates-log"), Path("gates-log") / "X1.md"}


def test_append_without_package_is_refused(repo: Path) -> None:
    run = gates(repo, "--append")
    assert run.returncode == 2
    assert "--append needs --package" in run.stdout
    assert not (repo / "gates-log").exists()
