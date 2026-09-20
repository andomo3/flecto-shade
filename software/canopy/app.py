"""C5: the server.

One event stream and the source control commands.
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
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from canopy import config, contract
from canopy.day import DEFAULT_DAY, DayPlayer, load_day
from canopy.recorder import Recorder
from canopy.sources import Source, open_source
from canopy.state import State

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
DEFAULT_FIXTURE = FIXTURES / "synthetic-day.csv"


class Runner:
    """Pumps one source into one state, and lets the page drive it."""

    def __init__(
        self,
        source: Source,
        *,
        autoplay: bool = False,
        player: DayPlayer | None = None,
    ) -> None:
        self.source = source
        self.player = player
        self.state = State()
        self.playing = autoplay
        self._resumed = asyncio.Event()
        self._tick = asyncio.Event()
        self._tasks: list[asyncio.Task] = []
        if autoplay:
            self._resumed.set()

    def start(self) -> None:
        if self._tasks:
            return
        self._tasks.append(asyncio.create_task(self._pump()))
        if self.player is not None:
            self._tasks.append(asyncio.create_task(self._play_day()))

    async def stop(self) -> None:
        for task in self._tasks:
            task.cancel()
        for task in self._tasks:
            with contextlib.suppress(asyncio.CancelledError):
                await task
        self._tasks = []
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

    async def _play_day(self) -> None:
        """The day drives the light; the source decides what the leaves do."""
        assert self.player is not None
        while True:
            await self._resumed.wait()
            self.player.send_step(self.player.now)
            self.player.index += 1
            await asyncio.sleep(config.TICK_MS / 1000)

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
        if self.player is not None:
            self.player.index = 0
            self.player.replay_mode = False
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
        data["day"] = None
        if self.player is not None:
            step = self.player.now
            data["day"] = {
                "city": self.player.day.city,
                "date": self.player.day.date,
                "local_time": step.local_time[11:16],
                "ghi": step.ghi,
                "t2m": step.t2m,
                "elevation": step.elevation,
                "step": step.step,
                "steps": len(self.player.day.steps),
            }
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
    day: str | Path | None = None,
    record: str | Path | None = None,
    autoplay: bool = False,
    **source_kwargs,
) -> FastAPI:
    source = open_source(
        source_name, fixture=fixture or DEFAULT_FIXTURE, **source_kwargs
    )
    recorder = Recorder(record).attach(source) if record else None
    # A fixture already holds a whole day; anything live needs one played to it.
    player = (
        None
        if source_name == "fixture"
        else DayPlayer(source, load_day(day or DEFAULT_DAY))
    )
    runner = Runner(source, autoplay=autoplay, player=player)

    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        runner.start()
        try:
            yield
        finally:
            await runner.stop()
            if recorder is not None:
                recorder.close()

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
        if runner.player is not None:
            runner.player.replay_mode = body.on
        if body.on:
            runner.send(contract.leaf_angle(body.angle or config.ANGLE_BENT))
        else:
            runner.send(contract.override(False))
        runner.state.replay_mode = body.on
        return runner.snapshot()

    return app
