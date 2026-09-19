"""The numbers the app shares with the board.

The thresholds and the servo travel are copied from the firmware's
``config.h`` and must be changed in both places at once.
"""

from __future__ import annotations

# Ten hertz, one data line every 100 ms.
TICK_MS = 100

# The leaves bend above BEND_LIGHT and rest below REST_LIGHT, per mille of full
# scale. The gap between them is the hysteresis that stops a cloud edge from
# rattling the servo.
BEND_LIGHT = 620
REST_LIGHT = 480

# Servo travel, degrees.
ANGLE_RESTING = 0
ANGLE_BENT = 125

# The bend takes about four seconds, which is a pace a judge can follow.
BEND_SECONDS = 4.0
ANGLE_STEP_PER_TICK = (ANGLE_BENT - ANGLE_RESTING) / (BEND_SECONDS * 1000 / TICK_MS)

# A leaf is called bent once it is most of the way there.
ANGLE_BENT_ENOUGH = ANGLE_BENT * 0.8

# What the bench sees, as a fraction of the incident light, with the leaves
# resting and with them bent. Modelled, and only ever used by the fake board
# and the simulator: the real number comes off the bench sensor.
BENCH_FRACTION_RESTING = 0.82
BENCH_FRACTION_BENT = 0.18

# The backup fixed roof, when it exists, shades the bench by the same amount at
# every sun angle. That is the point of it.
BENCH_FRACTION_FIXED = 0.45
