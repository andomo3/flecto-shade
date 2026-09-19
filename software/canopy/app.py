"""C5: the server.

One page, one event stream, and the handful of commands the drawer can send.
It starts with no serial port and no network: ``--source fixture`` always
works, because that is what stands between a dead cable and a lost demo.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import AsyncIterator
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

from canopy import config, contract
from canopy.sources import Source, open_source
from canopy.state import State

STATIC = Path(__file__).resolve().parent / "static"
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
DEFAULT_FIXTURE = FIXTURES / "synthetic-day.csv"


class Runner:
    """Pumps one source into one state, and lets the page drive it."""

    def __init__(self, source: Source, *, autoplay: bool = False) -> None:
        self.source = source
        self.state = State()
        self.playing = autoplay
        self._resumed = asyncio.Event()
        self._tick = asyncio.Event()
        self._task: asyncio.Task | None = None
        if autoplay:
            self._resumed.set()

    def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._pump())

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None
        await self.source.close()

    async def _pump(self) -> None:
        async for reading in self.source.readings():
            await self._resumed.wait()
            self.state.update(reading)
            self._tick.set()
            self._tick.clear()
        self.state.day_finished = True
        self._tick.set()
        self._tick.clear()

    def play(self) -> None:
        self.playing = True
        self._resumed.set()

    def pause(self) -> None:
        self.playing = False
        self._resumed.clear()

    def reset(self) -> None:
        self.pause()
        self.state.reset()
        self.state.replay_mode = False
        self.source.send(contract.override(False))
        self.source.send(contract.led(0))

    def send(self, command: str) -> None:
        self.source.send(command)

    async def snapshots(self) -> AsyncIterator[dict]:
        """The state now, and then the state on every reading."""
        yield self.snapshot()
        while True:
            await self._tick.wait()
            yield self.snapshot()

    def snapshot(self) -> dict:
        data = self.state.snapshot()
        data["source"] = self.source.name
        data["playing"] = self.playing
        return data


class Duty(BaseModel):
    duty: int = Field(ge=0, le=255)


class Angle(BaseModel):
    angle: int = Field(ge=0, le=180)


class ReplayMode(BaseModel):
    on: bool
    angle: int | None = Field(default=None, ge=0, le=180)


def create_app(
    source_name: str = "fixture",
    *,
    fixture: str | Path | None = None,
    autoplay: bool = False,
    **source_kwargs,
) -> FastAPI:
    source = open_source(
        source_name, fixture=fixture or DEFAULT_FIXTURE, **source_kwargs
    )
    runner = Runner(source, autoplay=autoplay)

    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        runner.start()
        try:
            yield
        finally:
            await runner.stop()

    app = FastAPI(title="flecto-stop", lifespan=lifespan)
    app.state.runner = runner

    @app.get("/health")
    async def health() -> dict:
        return {
            "status": "ok",
            "source": runner.source.name,
            "playing": runner.playing,
            "contract": contract.VERSION,
        }

    @app.get("/")
    async def page() -> FileResponse:
        return FileResponse(STATIC / "index.html")

    @app.get("/events")
    async def events() -> StreamingResponse:
        async def stream() -> AsyncIterator[bytes]:
            async for snapshot in runner.snapshots():
                yield f"data: {json.dumps(snapshot)}\n\n".encode()

        return StreamingResponse(
            stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"},
        )

    @app.post("/play")
    async def play() -> dict:
        runner.play()
        return runner.snapshot()

    @app.post("/pause")
    async def pause() -> dict:
        runner.pause()
        return runner.snapshot()

    @app.post("/reset")
    async def reset() -> dict:
        runner.reset()
        return runner.snapshot()

    @app.post("/led")
    async def led(body: Duty) -> dict:
        runner.send(contract.led(body.duty))
        return runner.snapshot()

    @app.post("/sun")
    async def sun(body: Angle) -> dict:
        runner.send(contract.sun_angle(body.angle))
        return runner.snapshot()

    @app.post("/replay-mode")
    async def replay_mode(body: ReplayMode) -> dict:
        if body.on:
            runner.send(contract.leaf_angle(body.angle or config.ANGLE_BENT))
        else:
            runner.send(contract.override(False))
        runner.state.replay_mode = body.on
        return runner.snapshot()

    return app
