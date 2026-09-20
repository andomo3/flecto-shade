"""The gate runner: one command that checks every fast gate in planning/plans/gates.md.

    python tools/gates.py [--package ID --allowed "path1,path2"] [--append] [--root DIR]

Each gate is one function returning (result, evidence), where result is one of
PASS, FAIL, or NOT YET.  NOT YET means the thing the gate checks does not exist
yet, and the evidence names the package that switches it on.  The exit code is
0 when no gate is FAIL.  Standard library only.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Callable
from urllib.request import ProxyHandler, build_opener

PASS = "PASS"
FAIL = "FAIL"
NOT_YET = "NOT YET"

EM_DASH = "\u2014"
BULKY_BYTES = 5 * 1024 * 1024
PYTEST_NO_TESTS = 5
YEAR_TESTS = (
    "software/tests/test_h1_year.py",
    "software/tests/test_headline_year.py",
)

BUILD_COMMANDS = [
    ("S1", "data/build_solar_2023.py", []),
    ("H1", "software/h1/build.py", ["--city", "apopka"]),
    ("H2", "software/page/build_day.py", ["--date", "2023-06-03"]),
    ("H3", "software/h3/build_headline.py", []),
]

OFFLINE_PRELUDE = (
    "import socket, sys, runpy\n"
    "def _refuse(*a, **k):\n"
    "    raise OSError('network is off for gate F2')\n"
    "socket.socket = _refuse\n"
    "socket.create_connection = _refuse\n"
    "socket.getaddrinfo = _refuse\n"
    "sys.argv = sys.argv[1:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n"
)

Gate = Callable[["Run"], tuple[str, str]]


class Run:
    def __init__(self, root: Path, package: str | None, allowed: list[str]) -> None:
        self.root = root
        self.package = package
        self.allowed = allowed
        self._changed: list[str] | None = None
        self._tracked: list[str] | None = None

    def git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True, text=True
        )

    def python(self, *args: str, timeout: float = 55) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def tracked(self) -> list[str]:
        if self._tracked is None:
            out = self.git("ls-files").stdout
            self._tracked = [line for line in out.splitlines() if line]
        return self._tracked

    def changed(self) -> list[str]:
        """Files that differ from the last merge: the working tree, the index,
        untracked files, and commits on this branch past origin/main."""
        if self._changed is not None:
            return self._changed
        files: set[str] = set()
        for line in self.git("status", "--porcelain", "--untracked-files=all").stdout.splitlines():
            if not line.strip():
                continue
            path = line[3:]
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            files.add(path.strip('"'))
        base = self.git("merge-base", "HEAD", "origin/main")
        if base.returncode == 0:
            diff = self.git("diff", "--name-only", base.stdout.strip(), "HEAD")
            files.update(line for line in diff.stdout.splitlines() if line)
        self._changed = sorted(files)
        return self._changed

    def files(self, *suffixes: str) -> list[Path]:
        found = []
        for path in self.root.rglob("*"):
            if not path.is_file() or path.suffix not in suffixes:
                continue
            parts = path.relative_to(self.root).parts
            if parts[0] in {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}:
                continue
            found.append(path)
        return sorted(found)


def _under(path: str, prefixes: list[str]) -> bool:
    path = path.replace("\\", "/")
    for prefix in prefixes:
        prefix = prefix.strip().replace("\\", "/")
        if not prefix:
            continue
        if prefix.endswith("/"):
            if path.startswith(prefix):
                return True
        elif path == prefix or path.startswith(prefix + "/"):
            return True
    return False


def _pytest(run: Run, *targets: str) -> tuple[str, str]:
    result = run.python("-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *targets)
    summary = ""
    for line in reversed(result.stdout.splitlines()):
        if line.strip():
            summary = line.strip()
            break
    if result.returncode == 0:
        return PASS, summary or "pytest exited 0"
    if result.returncode == PYTEST_NO_TESTS:
        return NOT_YET, "no tests collected; the first package with a test switches it on"
    return FAIL, summary or f"pytest exited {result.returncode}"


def _gate_test(gate_id: str, package: str) -> Gate:
    def check(run: Run) -> tuple[str, str]:
        tests = sorted((run.root / "software" / "tests").glob(f"test_gate_{gate_id.lower()}_*.py"))
        if not tests:
            return NOT_YET, f"no software/tests/test_gate_{gate_id.lower()}_*.py yet; {package} switches it on"
        return _pytest(run, *[str(t.relative_to(run.root)) for t in tests])

    return check


def f1_tests(run: Run) -> tuple[str, str]:
    return _pytest(run, *(f"--ignore={path}" for path in YEAR_TESTS))


def year_tests(run: Run) -> tuple[str, str]:
    present = [path for path in YEAR_TESTS if (run.root / path).is_file()]
    if not present:
        return NOT_YET, "no year test files yet; H1, then H3 switches them on"
    try:
        return _pytest(run, *present)
    except (OSError, subprocess.TimeoutExpired) as error:
        return FAIL, f"the year tests could not finish: {error}"


def check_local_page(page: Path) -> None:
    index = page / "index.html"
    if not index.is_file():
        raise ValueError("software/page/index.html is missing")
    handler = partial(SimpleHTTPRequestHandler, directory=str(page))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        worker = Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            opener = build_opener(ProxyHandler({}))
            with opener.open(f"http://127.0.0.1:{server.server_port}/", timeout=5) as response:
                if response.status != 200 or response.read() != index.read_bytes():
                    raise ValueError("the local page did not serve index.html")
        finally:
            server.shutdown()
            worker.join()


def f2_offline(run: Run) -> tuple[str, str]:
    present = [(pkg, script, args) for pkg, script, args in BUILD_COMMANDS if (run.root / script).exists()]
    page = run.root / "software" / "page"
    if not present and not page.is_dir():
        return NOT_YET, "no build command exists yet; S1 switches it on, then H2"
    evidence = []
    for pkg, script, args in present:
        try:
            result = run.python("-c", OFFLINE_PRELUDE, script, *args)
        except subprocess.TimeoutExpired:
            return FAIL, f"{script} did not finish in 55 s with the network off"
        if result.returncode != 0:
            last = (result.stderr.strip().splitlines() or ["no output"])[-1]
            return FAIL, f"{script} exited {result.returncode} with the network off: {last}"
    if present:
        ran = ", ".join(script for _, script, _ in present)
        evidence.append(f"ran with socket.socket patched to raise: {ran}")
    if page.is_dir():
        check_local_page(page)
        evidence.append("software/page/index.html answers HTTP 200 on loopback")
    return PASS, "; ".join(evidence)


_COMMENT_HTML = re.compile(r"<!--.*?-->", re.S)
_COMMENT_BLOCK = re.compile(r"/\*.*?\*/", re.S)
_COMMENT_LINE = re.compile(r"^\s*//.*$", re.M)
_EXTERNAL = re.compile(
    r"""(?:src|href)\s*=\s*["']?\s*(?:https?:)?//|url\(\s*["']?\s*(?:https?:)?//|import\s.*?["'](?:https?:)?//""",
    re.I,
)


def f3_no_fetch(run: Run) -> tuple[str, str]:
    software = run.root / "software"
    pages = [p for p in run.files(".html", ".css", ".js") if software in p.parents]
    if not pages:
        return NOT_YET, "no .html, .css, or .js under software/ yet; H2 switches it on"
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        text = _COMMENT_HTML.sub("", text)
        if page.suffix in {".css", ".js"}:
            text = _COMMENT_BLOCK.sub("", text)
        if page.suffix == ".js":
            text = _COMMENT_LINE.sub("", text)
        match = _EXTERNAL.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            return FAIL, f"{page.relative_to(run.root)} line {line} fetches an external address"
    return PASS, f"{len(pages)} page files under software/, no external address"


def f9_planning(run: Run) -> tuple[str, str]:
    touched = [f for f in run.changed() if _under(f, ["planning/"])]
    if touched:
        return FAIL, f"changed under planning/: {', '.join(touched[:3])}"
    return PASS, "nothing changed under planning/"


def f10_in_files(run: Run) -> tuple[str, str]:
    if not run.package or not run.allowed:
        return NOT_YET, "pass --package ID --allowed \"path1,path2\" to check it"
    allowed = list(run.allowed) + [f"gates-log/{run.package}.md"]
    outside = [f for f in run.changed() if not _under(f, allowed)]
    if outside:
        return FAIL, f"changed outside the allowed files: {', '.join(outside[:3])}"
    return PASS, f"{len(run.changed())} changed files, all within: {', '.join(run.allowed)}"


def f11_private(run: Run) -> tuple[str, str]:
    for path in run.tracked():
        name = Path(path).name
        if _under(path, ["data/raw/"]):
            return FAIL, f"tracked under data/raw/: {path}"
        if name == ".env" or name.startswith(".env."):
            return FAIL, f"tracked env file: {path}"
        full = run.root / path
        if full.exists() and full.stat().st_size > BULKY_BYTES:
            return FAIL, f"tracked file over 5 MB: {path}"
    return PASS, f"{len(run.tracked())} tracked files, none private or over 5 MB"


def f12_pinned(run: Run) -> tuple[str, str]:
    req = run.root / "software" / "requirements.txt"
    if not req.exists():
        return NOT_YET, "no software/requirements.txt yet; S1 switches it on"
    for number, line in enumerate(req.read_text(encoding="utf-8").splitlines(), 1):
        text = line.split("#", 1)[0].strip()
        if text and "==" not in text:
            return FAIL, f"software/requirements.txt line {number} is not pinned: {text}"
    return PASS, "every line of software/requirements.txt has =="


def f13_writing(run: Run) -> tuple[str, str]:
    for path in run.files(".md"):
        rel = path.relative_to(run.root).as_posix()
        if _under(rel, ["planning/", ".claude/"]):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if EM_DASH in text:
            line = text.count("\n", 0, text.index(EM_DASH)) + 1
            return FAIL, f"em dash in {rel} line {line}"
    return PASS, "no em dash in Markdown outside planning/ and .claude/"


GATES: list[tuple[str, str, Gate]] = [
    ("F1", "Every test that blocks passes", f1_tests),
    ("F2", "It runs with no network", f2_offline),
    ("F3", "The page fetches nothing from the internet", f3_no_fetch),
    ("F4", "Every output file has the schema its package gives", _gate_test("F4", "H1")),
    ("F5", "Nothing simulated is called measured", _gate_test("F5", "H2, then H3")),
    ("F6", "Every assumed constant is declared", _gate_test("F6", "H1")),
    ("F7", "The rules are deterministic, and only the rules act", _gate_test("F7", "H1")),
    ("F8", "The spoken numbers come from the code", _gate_test("F8", "H3")),
    ("F9", "The planning record is untouched", f9_planning),
    ("F10", "The package stayed in its files", f10_in_files),
    ("F11", "Nothing private or bulky is committed", f11_private),
    ("F12", "Every dependency is pinned", f12_pinned),
    ("F13", "The writing rules hold", f13_writing),
    ("F14", "Every sourced number has its source", _gate_test("F14", "H1")),
]


def run_gates(run: Run) -> list[tuple[str, str, str]]:
    rows = []
    for gate_id, _title, check in GATES:
        try:
            result, evidence = check(run)
        except Exception as error:  # a broken gate is a failed gate, never a silent one
            result, evidence = FAIL, f"the gate itself raised: {error}"
        rows.append((gate_id, result, evidence))
    return rows


def report(
    run: Run,
    rows: list[tuple[str, str, str]],
    exit_code: int,
    year: tuple[str, str],
) -> str:
    head = run.git("rev-parse", "--short", "HEAD")
    commit = head.stdout.strip() if head.returncode == 0 else "no commit"
    package = run.package or "none"
    command = "python tools/gates.py" + (f" --package {run.package}" if run.package else "")
    width = max(len(e) for _, _, e in rows)
    lines = [
        f"Package: {package}   Commit: {commit}   Command: {command}   Exit: {exit_code}",
        "",
        f"| Gate | Result  | {'Evidence'.ljust(width)} |",
    ]
    for gate_id, result, evidence in rows:
        lines.append(f"| {gate_id.ljust(4)} | {result.ljust(7)} | {evidence.ljust(width)} |")
    lines += [
        "",
        f"The year: {year[0]} - {year[1]} (nonblocking)",
        "",
        "Milestone gates M1 to M4 are checked by a person, see planning/plans/gates.md",
        "Regressions since the last report: [fill in]",
        "Milestone gates due next: [fill in]",
        "Anything in the demo, the pitch, or a checklist that this package makes harder: [fill in]",
    ]
    return "\n".join(lines)


def append_log(run: Run, text: str) -> Path:
    log = run.root / "gates-log" / f"{run.package}.md"
    log.parent.mkdir(exist_ok=True)
    head = run.git("rev-parse", "--short", "HEAD")
    commit = head.stdout.strip() if head.returncode == 0 else "no commit"
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    section = f"## {commit} at {stamp}\n\n```text\n{text}\n```\n"
    if log.exists():
        body = log.read_text(encoding="utf-8").rstrip("\n") + "\n\n" + section
    else:
        body = f"# Gate reports for {run.package}\n\n{section}"
    log.write_text(body, encoding="utf-8", newline="\n")
    return log


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", help="the work package ID, for example G1")
    parser.add_argument("--allowed", default="", help="comma separated files the package may change")
    parser.add_argument("--append", action="store_true", help="append the report to gates-log/ID.md")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="the repo root")
    args = parser.parse_args(argv)

    if args.append and not args.package:
        print("--append needs --package ID, so the report has a file of its own to go in.")
        return 2

    allowed = [a for a in args.allowed.split(",") if a.strip()]
    run = Run(Path(args.root).resolve(), args.package, allowed)
    rows = run_gates(run)
    exit_code = 1 if any(result == FAIL for _, result, _ in rows) else 0
    text = report(run, rows, exit_code, year_tests(run))
    print(text)
    if args.append:
        log = append_log(run, text)
        print(f"\nappended to {log.relative_to(run.root).as_posix()}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
