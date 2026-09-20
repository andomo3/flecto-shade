"""C5: the server answers with no serial port and no network."""

from __future__ import annotations

import asyncio
import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

from canopy import config
from canopy.app import create_app


def client() -> TestClient:
    return TestClient(create_app("fixture", autoplay=True))


async def first_events(app: FastAPI, count: int) -> tuple[dict, list[dict]]:
    """Drive the ASGI app by hand: the event stream never ends, so no test
    client can buffer it."""
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "path": "/events",
        "raw_path": b"/events",
        "query_string": b"",
        "root_path": "",
        "scheme": "http",
        "headers": [(b"host", b"test")],
        "client": ("test", 1),
        "server": ("test", 80),
    }
    start: dict = {}
    payloads: list[dict] = []
    enough = asyncio.Event()

    async def receive() -> dict:
        await enough.wait()
        return {"type": "http.disconnect"}

    async def send(message: dict) -> None:
        if message["type"] == "http.response.start":
            start.update(message)
        elif message["type"] == "http.response.body":
            for chunk in message.get("body", b"").decode().split("\n\n"):
                if chunk.startswith("data: "):
                    payloads.append(json.loads(chunk[6:]))
            if len(payloads) >= count:
                enough.set()

    runner = app.state.runner
    runner.start()
    task = asyncio.create_task(app(scope, receive, send))
    try:
        await asyncio.wait_for(enough.wait(), timeout=10)
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await runner.stop()
    return start, payloads


def test_health_is_200_and_names_the_source():
    with client() as api:
        response = api.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.json()["source"] == "fixture"
        assert response.json()["contract"] == 2


def test_events_streams_snapshots():
    app = create_app("fixture", autoplay=True)
    start, payloads = asyncio.run(first_events(app, 3))
    headers = {key.decode(): value.decode() for key, value in start["headers"]}
    assert start["status"] == 200
    assert headers["content-type"].startswith("text/event-stream")
    assert payloads[0]["source"] == "fixture"
    assert "leaves" in payloads[-1]
    assert payloads[-1]["t_ms"] is not None


def test_play_and_pause_flip_the_flag():
    with client() as api:
        assert api.post("/pause").json()["playing"] is False
        assert api.post("/play").json()["playing"] is True


def test_reset_clears_the_run_and_stops_it():
    with client() as api:
        api.post("/play")
        snapshot = api.post("/reset").json()
        assert snapshot["playing"] is False
        assert snapshot["waiting"] is True
        assert snapshot["cycles"] == 0


def test_the_drawer_commands_are_accepted_and_bounded():
    with client() as api:
        assert api.post("/led", json={"duty": 120}).status_code == 200
        assert api.post("/led", json={"duty": 900}).status_code == 422
        assert api.post("/sun", json={"angle": 90}).status_code == 200
        assert api.post("/sun", json={"angle": -1}).status_code == 422


def test_replay_mode_is_a_state_the_page_can_see():
    with client() as api:
        on = api.post("/replay-mode", json={"on": True, "angle": 90}).json()
        assert on["replay_mode"] is True
        off = api.post("/replay-mode", json={"on": False}).json()
        assert off["replay_mode"] is False


def test_replay_mode_defaults_to_the_bent_angle():
    app = create_app("fake", autoplay=True)
    with TestClient(app) as api:
        api.post("/replay-mode", json={"on": True})
        assert app.state.runner.source.commanded_angle == config.ANGLE_BENT
