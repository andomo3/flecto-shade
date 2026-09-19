"""``python -m canopy serve --source fixture``, which must always work."""

from __future__ import annotations

import argparse

import uvicorn

from canopy.app import DEFAULT_FIXTURE, create_app
from canopy.day import DEFAULT_DAY


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="canopy")
    sub = parser.add_subparsers(dest="command", required=True)

    serve = sub.add_parser("serve", help="serve the page")
    serve.add_argument("--source", default="fixture", choices=["fixture", "fake"])
    serve.add_argument("--fixture", default=str(DEFAULT_FIXTURE))
    serve.add_argument(
        "--day",
        default=str(DEFAULT_DAY),
        help="the day played to a live source, from data/processed",
    )
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument(
        "--autoplay",
        action="store_true",
        help="start the day without waiting for the Play button",
    )

    args = parser.parse_args(argv)
    if args.command == "serve":
        app = create_app(
            args.source,
            fixture=args.fixture,
            day=args.day,
            autoplay=args.autoplay,
        )
        uvicorn.run(app, host=args.host, port=args.port, log_level="info")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
