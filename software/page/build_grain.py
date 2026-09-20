"""Generate the paper grain the console lays over everything, as a data URI.

The design the console follows calls for a paper texture, and the repository forbids
fetching anything at run time, so the grain is generated here and pasted into
style.css as a base64 PNG. An SVG data URI cannot be used for this: its xmlns is an
http address, and gate F3 fails the build on one.

Standard library only, and deterministic: the same seed gives the same bytes, so the
texture never changes underneath a commit.

    python software/page/build_grain.py

Prints the data URI. Paste it into the --grain custom property in style.css.
"""

import argparse
import base64
import struct
import zlib

SIZE = 64
SEED = 0x9E3779B9
LEVELS = 6          # quantised, so the noise compresses instead of bloating the file
LIGHTEST = 255
DARKEST = 214       # multiply at low opacity, so the speckle must stay very pale


def noise(size=SIZE, seed=SEED, levels=LEVELS):
    """A tileable field of pale grey speckle, from one linear congruential stream."""
    value = seed & 0xFFFFFFFF
    rows = []
    for _ in range(size):
        row = bytearray()
        for _ in range(size):
            value = (1664525 * value + 1013904223) & 0xFFFFFFFF
            step = (value >> 16) % levels
            row.append(DARKEST + round(step * (LIGHTEST - DARKEST) / (levels - 1)))
        rows.append(bytes(row))
    return rows


def chunk(kind, payload):
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body))


def grayscale_png(rows):
    size = len(rows)
    header = struct.pack(">IIBBBBB", size, size, 8, 0, 0, 0, 0)   # 8 bit, greyscale
    raw = b"".join(b"\x00" + row for row in rows)                  # filter 0 per scanline
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def data_uri(png):
    return "data:image/png;base64," + base64.b64encode(png).decode("ascii")


def main():
    parser = argparse.ArgumentParser(description="The console's paper grain.")
    parser.add_argument("--size", type=int, default=SIZE)
    parser.add_argument("--seed", type=lambda v: int(v, 0), default=SEED)
    args = parser.parse_args()

    png = grayscale_png(noise(args.size, args.seed))
    uri = data_uri(png)
    assert "//" not in uri.split(",", 1)[0], "the scheme must not look like an address"
    print(uri)
    print(f"\n{len(png)} bytes of PNG, {len(uri)} characters of data URI", flush=True)


if __name__ == "__main__":
    main()
