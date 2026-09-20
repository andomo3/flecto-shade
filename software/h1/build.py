"""H1: zone targets, light, rain, and the soil bucket.

The heart of the louvre roof simulation.
Joins S1's 2023 sun for the Apopka area to the Orlando Executive Airport rain gauge for
the same year, then walks every hour of the year for three crop zones under nine
deterministic rules and writes what the roof did.

Sun and temperature are NASA POWER for 2023, modelled from satellite and reanalysis.
Rain is the Orlando Executive Airport gauge for 2023, measured. Same place, same year.

Everything it writes is simulated. Runs with the network off, identical bytes every run.
"""

import argparse
import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[2]
CROPS_PATH = REPO_ROOT / "data" / "crops.csv"
PROCESSED = REPO_ROOT / "data" / "processed"
RAIN_PATH = REPO_ROOT / "data" / "raw" / "isd-rain" / "72205312841-2023.csv"
LOCAL_TZ = ZoneInfo("America/New_York")

# --- light -------------------------------------------------------------------
# VERIFIED: 4.57 micromol per joule of photosynthetic light, and that light is 0.44 to
# 0.55 of global solar (Noriega Gardea et al. 2021). 0.45 is a choice inside that range,
# and the measured range is lower, so light sums may read 5 to 18 percent high.
PAR_FRACTION = 0.45
MICROMOL_PER_JOULE = 4.57
K = PAR_FRACTION * MICROMOL_PER_JOULE          # 2.0565 micromol per joule of global solar
T_STRUCT = 0.90                                # ASSUMED, the structure itself, no glazing
T_CLOSED = 0.0                                 # ASSUMED, a closed fin is opaque

# --- water -------------------------------------------------------------------
# Modified Makkink, de Bruin 1987, not Makkink 1957, which used 0.61 with an additive
# 0.12 mm/day term. RECALLED in the package, confirmed at source and recorded in
# data/README.md. Pressure is a constant from the gauge's elevation of 31.7 m.
MAKKINK_C = 0.65                               # RECALLED, confirmed: C3S/KNMI PET manual
LATENT_HEAT_MJ_PER_KG = 2.45                   # RECALLED, confirmed: FAO-56 chapter 3
ELEVATION_M = 31.7
PRESSURE_KPA = 101.3 * ((293 - 0.0065 * ELEVATION_M) / 293) ** 5.26   # 100.9258
GAMMA = 0.665e-3 * PRESSURE_KPA                                        # 0.067116

# --- the soil bucket, all ASSUMED --------------------------------------------
SOIL_CAPACITY = 60.0
SOIL_DRY_BELOW = 30.0
SOIL_FULL_AT = 54.0
SOIL_IRRIGATE_BELOW = 18.0
SOIL_START = 54.0

# --- rule constants ----------------------------------------------------------
HARD_RAIN_MM = 25.0                            # ASSUMED
DRYING_HOURS = 3                               # ASSUMED
HEAT_SHADE_C = 32.2                            # ASSUMED, the fact sheet's 90 F trigger
HEAT_SHADE_OPEN = 0.60

# Gate F6 reads this. Every named constant H1 marks ASSUMED or RECALLED appears here
# and in the "Assumptions" section of data/README.md, with the same value.
ASSUMED_CONSTANTS = {
    "PAR_FRACTION": PAR_FRACTION,
    "T_STRUCT": T_STRUCT,
    "T_CLOSED": T_CLOSED,
    "SOIL_CAPACITY": SOIL_CAPACITY,
    "SOIL_DRY_BELOW": SOIL_DRY_BELOW,
    "SOIL_FULL_AT": SOIL_FULL_AT,
    "SOIL_IRRIGATE_BELOW": SOIL_IRRIGATE_BELOW,
    "SOIL_START": SOIL_START,
    "HARD_RAIN_MM": HARD_RAIN_MM,
    "DRYING_HOURS": DRYING_HOURS,
    "HEAT_SHADE_C": HEAT_SHADE_C,
    "HEAT_SHADE_OPEN": HEAT_SHADE_OPEN,
}
RECALLED_CONSTANTS = {
    "MAKKINK_C": MAKKINK_C,
    "LATENT_HEAT_MJ_PER_KG": LATENT_HEAT_MJ_PER_KG,
}

# The nine rules produce exactly these states and no others. Gate F7 reads this.
STATES = ("NIGHT", "LIGHT_OPEN", "SHADE", "HEAT_SHADE", "RAIN_OPEN", "RAIN_SHUT")
REASONS = ("opted_out", "wet_enough", "no_drying_time", "hard_rain")

SIM_COLUMNS = ["hour", "time_utc", "zone", "crop", "open_fraction", "light_mol_so_far",
               "soil_mm", "rain_in_mm", "irrigation_mm", "state", "reason"]
SUMMARY_COLUMNS = ["zone", "crop", "scope", "month", "rain_in_mm", "irrigation_mm",
                   "days_target_met", "rain_share"]


def read_crops():
    with open(CROPS_PATH, newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["light_value"] = float(row["light_value"])
        row["kc"] = float(row["kc"])
        row["rain_ok"] = int(row["rain_ok"])
    rows.sort(key=lambda row: row["zone"])
    return rows


def read_year(city):
    path = PROCESSED / f"year-{city}-2023.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} is missing. It is written by package S1. If S1 is not merged yet, "
            "build it on its branch first; do not stand in for it."
        )
    rows = []
    with open(path, newline="") as handle:
        for row in csv.DictReader(handle):
            stamp = datetime.strptime(row["time_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            rows.append({
                "hour": int(row["hour"]), "time_utc": row["time_utc"], "ts": stamp,
                "month": int(row["month"]), "local_hour": int(row["local_hour"]),
                "local_date": stamp.astimezone(LOCAL_TZ).date(),
                "ghi": float(row["ghi"]), "dni": float(row["dni"]),
                "dhi": float(row["dhi"]), "t2m": float(row["t2m"]),
                "source_year": int(row["source_year"]),
            })
    return rows


def read_rain():
    """FM-15 rows only, AA1 period 01, depth not 9999, floored to the UTC hour,
    the last row in each hour, divided by 10. A missing hour becomes 0.

    The traps this avoids: FM-16 special reports repeat the running hourly total, which
    would treble the year; SOD rows hold 24 hour totals; a trace always has depth 0.
    """
    hourly, seen = {}, {}
    with open(RAIN_PATH, newline="") as handle:
        for row in csv.DictReader(handle):
            if row["REPORT_TYPE"].strip() != "FM-15":
                continue
            field = row.get("AA1", "")
            if not field:
                continue
            parts = field.split(",")
            if parts[0] != "01" or parts[1] == "9999":
                continue
            stamp = datetime.strptime(row["DATE"], "%Y-%m-%dT%H:%M:%S")
            stamp = stamp.replace(minute=0, second=0, tzinfo=timezone.utc)
            seen[stamp] = seen.get(stamp, 0) + 1
            hourly[stamp] = int(parts[1]) / 10.0      # the last row in the hour wins
    return hourly, seen


def reference_evaporation(ghi, t2m, scale=1.0):
    """Modified Makkink reference evaporation for one hour, in mm."""
    slope = 4098 * (0.6108 * math.exp(17.27 * t2m / (t2m + 237.3))) / (t2m + 237.3) ** 2
    radiation_mj = ghi * 3600 / 1e6
    return scale * MAKKINK_C * slope / (slope + GAMMA) * radiation_mj / LATENT_HEAT_MJ_PER_KG


def light_for_hour(ghi, open_fraction):
    transmitted = open_fraction + (1 - open_fraction) * T_CLOSED
    return ghi * K * 3600 / 1e6 * T_STRUCT * transmitted


def decide(crop, weather, index, light_so_far, want_rain):
    """The nine rules, priority night, then rain, then light.

    Decided from the state at the end of the hour before.
    """
    hour = weather[index]
    ghi, rain_mm, t2m = hour["ghi"], hour["rain_mm"], hour["t2m"]

    # 3. Rain is never admitted at night.
    if ghi <= 0:
        return 0.0, "NIGHT", ""

    if rain_mm > 0:
        # 4, and 5 for every way it can fail. The reason order is fixed by the package.
        if not crop["rain_ok"]:
            return 0.0, "RAIN_SHUT", "opted_out"
        if not want_rain:
            return 0.0, "RAIN_SHUT", "wet_enough"
        later = index + DRYING_HOURS
        if later >= len(weather) or weather[later]["ghi"] <= 0:
            return 0.0, "RAIN_SHUT", "no_drying_time"
        if rain_mm >= HARD_RAIN_MM:
            return 0.0, "RAIN_SHUT", "hard_rain"
        return 1.0, "RAIN_OPEN", ""

    # 6. A daily light crop.
    if crop["light_rule"] == "dli":
        if light_so_far < crop["light_value"]:
            return 1.0, "LIGHT_OPEN", ""
        return 0.0, "SHADE", ""

    # 7. A shade share crop.
    if t2m >= HEAT_SHADE_C:
        return HEAT_SHADE_OPEN, "HEAT_SHADE", ""
    return 1.0, "LIGHT_OPEN", ""


def simulate(weather, crop, et_scale=1.0):
    """Walk the year for one zone, carrying the soil and the want_rain latch."""
    soil = SOIL_START
    light_so_far = 0.0
    want_rain = soil < SOIL_DRY_BELOW
    out = []

    for index, hour in enumerate(weather):
        # 1. The daily light sum resets at local midnight.
        if hour["local_hour"] == 0:
            light_so_far = 0.0

        # 2. The latch, read from the state at the end of the hour before.
        if soil < SOIL_DRY_BELOW:
            want_rain = True
        elif soil >= SOIL_FULL_AT:
            want_rain = False

        open_fraction, state, reason = decide(crop, weather, index, light_so_far, want_rain)
        light_so_far += light_for_hour(hour["ghi"], open_fraction)

        # 8. Rain in and capped, then the crop's use, then the grower's own water.
        before = soil
        soil = min(SOIL_CAPACITY, soil + hour["rain_mm"] * open_fraction)
        rain_in = soil - before
        used = crop["kc"] * reference_evaporation(hour["ghi"], hour["t2m"], et_scale) * open_fraction * T_STRUCT
        soil = max(0.0, soil - used)

        irrigation = 0.0
        if soil < SOIL_IRRIGATE_BELOW:
            irrigation = SOIL_FULL_AT - soil
            soil = SOIL_FULL_AT

        out.append({
            "open_fraction": open_fraction, "state": state, "reason": reason,
            "light_mol_so_far": light_so_far, "soil_mm": soil,
            "rain_in_mm": rain_in, "irrigation_mm": irrigation, "crop_use_mm": used,
        })
    return out


def write_csv(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(",".join(columns) + "\n")
        for row in rows:
            handle.write(",".join(row) + "\n")


def fmt(value, places):
    text = f"{float(value) + 0.0:.{places}f}"
    return "0." + "0" * places if text.startswith("-0.") and float(text) == 0 else text


def build(city="apopka", et_scale=1.0, write=True):
    crops = read_crops()
    weather = read_year(city)
    rain, _ = read_rain()
    for hour in weather:
        hour["rain_mm"] = rain.get(hour["ts"], 0.0)

    runs = {crop["zone"]: simulate(weather, crop, et_scale) for crop in crops}

    if write:
        write_csv(PROCESSED / f"weather-{city}.csv",
                  ["hour", "time_utc", "month", "source_year", "local_hour",
                   "ghi", "dni", "dhi", "t2m", "rain_mm"],
                  [[str(h["hour"]), h["time_utc"], str(h["month"]), str(h["source_year"]),
                    str(h["local_hour"]), fmt(h["ghi"], 2), fmt(h["dni"], 2),
                    fmt(h["dhi"], 2), fmt(h["t2m"], 2), fmt(h["rain_mm"], 1)]
                   for h in weather])

        sim_rows = []
        for crop in crops:
            series = runs[crop["zone"]]
            for hour, row in zip(weather, series):
                sim_rows.append([
                    str(hour["hour"]), hour["time_utc"], crop["zone"], crop["crop"],
                    fmt(row["open_fraction"], 2), fmt(row["light_mol_so_far"], 3),
                    fmt(row["soil_mm"], 3), fmt(row["rain_in_mm"], 3),
                    fmt(row["irrigation_mm"], 3), row["state"], row["reason"],
                ])
        write_csv(PROCESSED / f"sim-{city}.csv", SIM_COLUMNS, sim_rows)
        write_csv(PROCESSED / f"sim-summary-{city}.csv", SUMMARY_COLUMNS,
                  summary_rows(crops, weather, runs))

    return crops, weather, runs


def summary_rows(crops, weather, runs):
    rows = []
    for crop in crops:
        series = runs[crop["zone"]]
        by_month = {m: [0.0, 0.0] for m in range(1, 13)}
        met_by_month = {m: 0 for m in range(1, 13)}

        days = {}
        for hour, row in zip(weather, series):
            month = hour["local_date"].month
            by_month[month][0] += row["rain_in_mm"]
            by_month[month][1] += row["irrigation_mm"]
            day = days.setdefault(hour["local_date"], {"peak": 0.0, "rows": 0})
            day["peak"] = max(day["peak"], row["light_mol_so_far"])
            day["rows"] += 1

        # Every local date in 2023, all 365. The UTC file opens at local 19:00 on
        # 2022-12-31, so that fragment is dropped; 2023-12-31 lacks only dark evening
        # hours and counts whole, and the two daylight-saving days count as themselves.
        year_met = 0
        for date, day in days.items():
            if date.year != 2023:
                continue
            if crop["light_rule"] == "dli" and day["peak"] >= crop["light_value"]:
                met_by_month[date.month] += 1
                year_met += 1

        rain_total = sum(value[0] for value in by_month.values())
        irr_total = sum(value[1] for value in by_month.values())
        share = rain_total / (rain_total + irr_total) if (rain_total + irr_total) else 0.0

        for month in range(1, 13):
            rows.append([crop["zone"], crop["crop"], "month", str(month),
                         fmt(by_month[month][0], 1), fmt(by_month[month][1], 1),
                         str(met_by_month[month]), ""])
        rows.append([crop["zone"], crop["crop"], "year", "",
                     fmt(rain_total, 1), fmt(irr_total, 1), str(year_met), fmt(share, 3)])
    return rows


def main():
    parser = argparse.ArgumentParser(description="H1: the zones, the rules, the year.")
    parser.add_argument("--city", default="apopka")
    args = parser.parse_args()

    crops, weather, runs = build(args.city)
    print(f"wrote weather-{args.city}.csv, sim-{args.city}.csv, sim-summary-{args.city}.csv")
    print(f"  modelled, from {len(weather)} hours and {len(crops)} zones")
    for crop in crops:
        series = runs[crop["zone"]]
        states = {}
        for row in series:
            states[row["state"]] = states.get(row["state"], 0) + 1
        rain_in = sum(row["rain_in_mm"] for row in series)
        irr = sum(row["irrigation_mm"] for row in series)
        use = sum(row["crop_use_mm"] for row in series)
        share = rain_in / (rain_in + irr) if (rain_in + irr) else 0.0
        soils = [row["soil_mm"] for row in series]
        print(f"  {crop['zone']} {crop['crop'][:12]:<12} "
              f"rain in {rain_in:>6.1f}  irrigation {irr:>6.1f}  use {use:>6.1f}  "
              f"share {share:.3f}  soil {min(soils):>5.2f} to {max(soils):>5.2f}")
        print(f"      {', '.join(f'{k} {v}' for k, v in sorted(states.items()))}")


if __name__ == "__main__":
    main()
