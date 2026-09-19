---
title: What does the HackMIT 2026 hardware list give us and what is missing
type: research
status: done   # open | in-progress | done | dropped
owner: abba   # one word handle of the teammate doing the research
updated: 2026-09-02
---

# What does the HackMIT 2026 hardware list give us and what is missing

## Answer

The list covers sensing, compute, actuation, and low-force mechanical basics, but it has no 3D printer, filament, directional dry adhesive, rigid sheet stock, calibrated non-restricted mass, scale, pulley, spring, or confirmed passive piezo sensor.
Because this team cannot bring project items, every critical design must use only listed non-restricted components.

## Findings

- Force and load sensing is well covered: square and Ohmite force sensitive resistors, flex sensors, Velostat, pressure sensors, and 5 kg strain-gauge load cells with HX711 amplifiers.
- Motion sensing is well covered: 3-axis accelerometer and gyro, 9 DOF IMU, MPU-6050, MPU-9250, BNO055, BNO085.
- Actuation is well covered: SG90 and MG996R class servos, smart serial servos with position feedback, PCA9685 16-channel servo drivers, Pololu micro gearmotors with encoders, steppers.
- Compute is well covered: Arduino Uno, Mega, Nano, GIGA, ESP32 variants, Raspberry Pi 4 and 5, Pico, Jetson Nano and Orin Nano, Teensy 4.1.
- Mechanical basics are covered: M3 and M4 hardware, standoffs, zip ties, Velcro, gaffer and electrical tape, foam board.
- Restricted but available on request: neodymium magnets, the 1 inch tungsten cube demonstration mass, RealSense depth cameras, OAK-D Lite, RPLIDAR, desktop robotic arms.
- Wearable angle: Meta Ray-Ban AI glasses and the Ray-Ban Display with Neural Band are on the restricted list, as are non-prescription eyeglass frames as wearable platforms.
- Missing: no 3D printer, filament, or TPU anywhere on the list.
- Piezo: no passive piezo sensor is listed, and the `piezo buzzers` entry does not say whether the stocked part is an external-drive diaphragm or a buzzer with an oscillator.
- Fast sampling: the HX711 supports 10 or 80 samples per second, but the exact breakout may default to 10 and may require unlisted rework to reach 80.
- Force-sensitive resistors: the exact part, dimensions, range, hysteresis, and saturation behavior are unspecified, so they are qualitative until calibrated in the final mechanism.
- Servo power: the list has `MG995 / MG996R class` servos and suitable-looking 5 V supplies, but exact servo current and USB-C or barrel current-path ratings still need confirmation.
- Biosignal sensors are restricted and governed by a separate protocol; none deliver current to the body.

## Implications for the build

- The impact insert and gecko foot must assume no printer and no printable material unless organizers add them in writing, see [3D printing access](3d-printing-access.md).
- The gecko foot should use its IMU as the only critical-path transient sensor and omit the unverified piezo.
- Load cells with HX711 are appropriate for quasi-static load after exact geometry and calibration are confirmed, but not for fast slip or impact onset.
- The tungsten cube and magnets are restricted, so a drop rig or pendulum demo needs the request made early.
- The gecko foot uses electrical-tape adhesive and backing faces as ordinary contact conditions, not directional dry adhesive.
- Its direct-pull gauge reports normalized HX711 load unless the restricted tungsten cube has a documented mass and is approved for optional calibration.
- Its stationary foam-board panel, Velcro tether, listed wheel, event Raspberry Pi, IMU, webcam, and threshold detector keep unlisted and restricted parts off the critical path.

## Sources

- [HackMIT 2026 hardware list](../sources/hackmit-2026-hardware-list.md), pasted 2026-09-02.
- [Load Paths artifact](../sources/2026-09-02-load-paths-artifact.md), constraints 02 and 03 and the bring-your-own list.
