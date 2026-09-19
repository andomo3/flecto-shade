# Serial contract, version 2

Owner: the software and data role.
Implemented by the firmware role in `canopy/`, consumed by `software/canopy/`, recorded verbatim into `software/fixtures/`.
A change needs the firmware and software owners in the same conversation, bumps the version in the header line, updates the sample lines below, and passes the parser test in CI.

Version 2 follows the MVP in `../docs/meetings/2026-09-18.md`: an incident photoresistor that drives the leaves, a bench light sensor that gives the number, a flex sensor, two secondary temperature sensors, and an LED sun the laptop can dim and, when the servo mount exists, move.
Version 1 had an incident sensor and a bench sensor under each of two roofs, and no build ever implemented it.

## Link

- 115200 baud, 8N1, ASCII, every line ends in `\n`.
- One data line every 100 ms, ten hertz, whether or not anything changed.
- On the Uno R3 this is the USB port.
  On the UNO Q it is the D0 and D1 pins at 3.3 V, through the adapter described in `../hardware/electronics/README.md`.
- The board never waits for the laptop.
  If nothing is listening, it keeps logging.

## Board to laptop

A header line at boot and again every ten seconds, so a reader that connects late still knows the version:

```
# canopy v2
```

A data line, eleven comma separated fields, no spaces:

```
t_ms,light,bench,fixed,flex,temp_canopy,temp_open,angle,sun,led,override
```

| Field | Type | Range | Meaning |
|---|---|---|---|
| `t_ms` | unsigned integer | milliseconds since boot | The board clock, used for fixture replay timing |
| `light` | integer | 0 to 1000 | The incident photoresistor that drives the leaves, per mille of ADC full scale |
| `bench` | integer or empty | 0 to 1000 | The light sensor on the bench under the canopy, per mille of full scale, the primary number comes from here |
| `fixed` | integer or empty | 0 to 1000 | The bench sensor under the backup fixed roof, empty unless that roof is built |
| `flex` | integer or empty | 0 to 1000 | The flex sensor on the backbone, per mille of full scale, an indicator and never a control input |
| `temp_canopy` | integer or empty | tenths of a degree Celsius | The temperature sensor on the bench under the canopy, `253` is 25.3 degrees |
| `temp_open` | integer or empty | tenths of a degree Celsius | The temperature sensor at the open control spot |
| `angle` | integer | 0 to 180 | The leaf servo angle commanded on this tick, degrees |
| `sun` | integer or empty | 0 to 180 | The sun mount servo angle commanded on this tick, empty when the LED sits in the fixed mount |
| `led` | integer | 0 to 255 | The LED sun brightness commanded on this tick, the PWM duty |
| `override` | `0` or `1` | | `1` while the photoresistor is not in control of the leaves, from the button, `O 1`, or replay mode |

Per mille of full scale means the firmware maps the raw ADC reading to 0 to 1000 before printing, so the line means the same thing on the ten bit Uno and the twelve bit UNO Q.

A sensor that is not fitted yet, or that fails to read, prints an empty field, never a zero and never a made up value.
The flex sensor arrives at hour eight and the bench and temperature sensors by hour twelve, so early lines look like the first sample below and every reader must accept them.
If the team uses the thermal camera instead of the DS18B20s, both temperature fields stay empty for good.

A DS18B20 conversion takes up to 750 ms.
The firmware starts a conversion without waiting, prints the last good reading on every line in between, and never lets a temperature read delay the ten hertz line.

Sample lines, which the parser test uses:

```
# canopy v2
1200,212,,,,,,0,,40,0
1300,215,,,,,,0,,40,0
61000,790,190,,655,,,124,,255,0
61100,791,188,,660,253,268,125,90,255,0
61200,791,187,610,661,253,268,125,90,255,1
```

## Laptop to board

Optional.
The board runs the control law on its own with no laptop attached, and with no command received the LED sun follows its switch or its default brightness.
Commands are one letter, an optional argument, and `\n`.

| Command | Meaning |
|---|---|
| `O 1` and `O 0` | Override on and off, the same as holding the button |
| `L 0` to `L 255` | Set the LED sun brightness, the PWM duty. The app uses this to fast forward a day from the dataset |
| `A 0` to `A 180` | Set the sun mount servo angle. Ignored when the LED sits in the fixed mount |
| `S 0` to `S 180` | Replay mode, the pivot: set the leaf servo angle directly and turn the override on. `O 0` hands the leaves back to the photoresistor |
| `P` | Ping. The board answers with the header line |

Unknown commands and out of range arguments are ignored.
The board never prints anything except the header line and data lines, so the reader can parse every line by its first character.

In the normal demo the laptop never sends `S`.
The data moves the sun and only the photoresistor moves the leaves, so what the judge sees is the canopy responding to light and not to the app.
`S` exists for the hour twelve pivot, when the threshold is unreliable in the room, and the display shows replay mode in words whenever it is in use.

## What the laptop derives

- The number, light at the bench as a percent of the incident light: `bench / light * 100`, averaged separately over lines where the leaves are flared and lines where they are resting.
  With the backup roof built, `fixed / light * 100` is shown beside it.
- The secondary temperature difference: `(temp_open - temp_canopy) / 10` in degrees, shown only while both fields are present.
- The leaf state, flared or resting, from `angle`, with `flex` beside it as the evidence the bend happened.
- The cycle count for the backup number: one cycle is `light` crossing the threshold followed by `angle` reaching its flared value and later returning.
  The thresholds live in the software's config, copied from `canopy/config.h`.

## Fixtures

A fixture is this stream written to a file unchanged, header lines included, one line per row.
Replay uses `t_ms` to reproduce the original pacing.
The first clean run at the event is recorded and committed, see `../software/fixtures/README.md`.
