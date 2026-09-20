"""H2: build `day.json`, the one small file the grower's console reads.

Reads package H1's output for one local day and writes it flat, with the crops table,
the regional statistics, and the rule constants the page needs to re-run the rules
itself when the grower changes the sky or takes a zone off rain.

It derives no physics of its own. Every baseline number here came out of H1.

Sun and temperature are NASA POWER for 2023, modelled from satellite and reanalysis.
Rain is the Orlando Executive Airport gauge for 2023, measured. Same place, same year.

Runs with the network off, and gives identical bytes on every run.
"""

import argparse
import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = REPO_ROOT / "data" / "processed"
CROPS_PATH = REPO_ROOT / "data" / "crops.csv"
H1_BUILD = REPO_ROOT / "software" / "h1" / "build.py"
OUT_PATH = Path(__file__).resolve().parent / "day.json"
LOCAL_TZ = ZoneInfo("America/New_York")

PLAY_SECONDS_LIT = 2.4
PLAY_SECONDS_DARK = 0.5

STATE_WORDS = {
    "NIGHT": "Night",
    "LIGHT_OPEN": "Open for light",
    "SHADE": "Shaded, target met",
    "HEAT_SHADE": "Shaded, heat",
    "RAIN_OPEN": "Open for rain",
    "RAIN_SHUT": "Shut against rain",
}
REASON_WORDS = {
    "opted_out": "this crop opts out of rain",
    "wet_enough": "its soil is wet enough",
    "no_drying_time": "no drying time left today",
    "hard_rain": "the rain is too hard",
}

BOTANICAL = {
    "boston fern": "Nephrolepis",
    "hydrangea": "Hydrangea macrophylla",
    "southern highbush blueberry": "Vaccinium corymbosum",
}

REGION_SOURCE = ("NOAA NCEI Integrated Surface Database, station 72205312841, 2023. "
                 "Normal is the 1991 to 2020 value for this station.")
NORMAL_MM = 1307
VS_NORMAL_PCT = 2.4


def h1_constants():
    """The rule constants, taken from H1 itself so the page can never drift from it."""
    spec = importlib.util.spec_from_file_location("h1_build", H1_BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {
        "K": round(module.K, 4),
        "T_STRUCT": module.T_STRUCT,
        "T_CLOSED": module.T_CLOSED,
        "MAKKINK_C": module.MAKKINK_C,
        "LATENT_HEAT": module.LATENT_HEAT_MJ_PER_KG,
        "GAMMA": round(module.GAMMA, 6),
        "SOIL_CAPACITY": module.SOIL_CAPACITY,
        "SOIL_DRY_BELOW": module.SOIL_DRY_BELOW,
        "SOIL_FULL_AT": module.SOIL_FULL_AT,
        "SOIL_IRRIGATE_BELOW": module.SOIL_IRRIGATE_BELOW,
        "HARD_RAIN_MM": module.HARD_RAIN_MM,
        "DRYING_HOURS": module.DRYING_HOURS,
        "HEAT_SHADE_C": module.HEAT_SHADE_C,
        "HEAT_SHADE_OPEN": module.HEAT_SHADE_OPEN,
    }


def read_csv(path):
    if not path.exists():
        raise FileNotFoundError(
            f"{path} is missing. It is written by package H1. "
            "Run python software/h1/build.py --city apopka first."
        )
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def local_of(time_utc):
    return datetime.strptime(time_utc, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc).astimezone(LOCAL_TZ)


def build(city="apopka", date="2023-06-03", out_path=OUT_PATH):
    crops = sorted(read_csv(CROPS_PATH), key=lambda row: row["zone"])
    weather = read_csv(PROCESSED / f"weather-{city}.csv")
    sim = read_csv(PROCESSED / f"sim-{city}.csv")

    for row in weather:
        row["local"] = local_of(row["time_utc"])

    day_weather = sorted((row for row in weather if row["local"].strftime("%Y-%m-%d") == date),
                         key=lambda row: row["local"].hour)
    if len(day_weather) != 24:
        raise ValueError(f"{date} has {len(day_weather)} rows in weather-{city}.csv, expected 24")
    stamps = [row["time_utc"] for row in day_weather]

    by_zone = {}
    for row in sim:
        if row["time_utc"] in stamps:
            by_zone.setdefault(row["zone"], {})[row["time_utc"]] = row

    lit = sum(1 for row in day_weather if float(row["ghi"]) > 0)
    day_rain = sum(float(row["rain_mm"]) for row in day_weather)

    payload = {
        "label": "simulated",
        "date_local": date,
        "place": "Orlando Executive Airport gauge, near Apopka, Florida",
        "sources": {
            "sun": "NASA POWER, satellite product, hourly means, modelled",
            "rain": "NOAA ISD gauge 72205312841, measured",
        },
        "credit": "The fin is the Flectofin, by ITKE, University of Stuttgart, patented as EP2320015.",
        "from_package": "H1",
        "constants": h1_constants(),
        "day": {
            "lit_hours": lit,
            "rain_mm": round(day_rain, 1),
            "play_seconds": round(lit * PLAY_SECONDS_LIT + (24 - lit) * PLAY_SECONDS_DARK, 1),
            "peak_ghi": round(max(float(row["ghi"]) for row in day_weather), 2),
            "peak_t2m": round(max(float(row["t2m"]) for row in day_weather), 2),
        },
        "hours": [{
            "local_hour": row["local"].hour,
            "ghi": float(row["ghi"]),
            "rain_mm": round(float(row["rain_mm"]), 1),
            "t2m": float(row["t2m"]),
            "play_seconds": PLAY_SECONDS_LIT if float(row["ghi"]) > 0 else PLAY_SECONDS_DARK,
        } for row in day_weather],
        "zones": [],
        "region": region_stats(weather),
    }

    for crop in crops:
        rows = [by_zone[crop["zone"]][stamp] for stamp in stamps]
        payload["zones"].append({
            "zone": crop["zone"],
            "crop": crop["crop"].title() if crop["crop"].islower() else crop["crop"],
            "botanical": BOTANICAL.get(crop["crop"], ""),
            "light_rule": crop["light_rule"],
            "light_target": float(crop["light_value"]),
            "kc": float(crop["kc"]),
            "rain_ok": int(crop["rain_ok"]),
            "note": crop["note"],
            "soil_start": float(rows[0]["soil_mm"]),
            "hours": [{
                "open_fraction": float(row["open_fraction"]),
                "light_mol_so_far": round(float(row["light_mol_so_far"]), 2),
                "soil_mm": round(float(row["soil_mm"]), 2),
                "rain_in_mm": round(float(row["rain_in_mm"]), 2),
                "irrigation_mm": round(float(row["irrigation_mm"]), 2),
                "state": row["state"],
                "reason": row["reason"],
                "words": STATE_WORDS[row["state"]],
                "because": REASON_WORDS.get(row["reason"], ""),
            } for row in rows],
        })

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, indent=1, sort_keys=False) + "\n")
    return out_path, payload


def region_stats(weather):
    monthly = [0.0] * 12
    rain_hours = lit_hours = daylight_rain_hours = 0
    daylight_rain_mm = total = 0.0
    for row in weather:
        rain = float(row["rain_mm"])
        ghi = float(row["ghi"])
        monthly[int(row["month"]) - 1] += rain
        total += rain
        if rain > 0:
            rain_hours += 1
        if ghi > 0:
            lit_hours += 1
            if rain > 0:
                daylight_rain_hours += 1
                daylight_rain_mm += rain
    return {
        "year": 2023,
        "rain_mm": round(total, 1),
        "rain_hours": rain_hours,
        "lit_hours": lit_hours,
        "daylight_rain_hours": daylight_rain_hours,
        "daylight_rain_mm": round(daylight_rain_mm, 1),
        "normal_mm": NORMAL_MM,
        "vs_normal_pct": VS_NORMAL_PCT,
        "monthly_rain_mm": [round(value, 1) for value in monthly],
        "source": REGION_SOURCE,
    }


def main():
    parser = argparse.ArgumentParser(description="H2: the day the console plays.")
    parser.add_argument("--city", default="apopka")
    parser.add_argument("--date", default="2023-06-03")
    args = parser.parse_args()

    path, payload = build(args.city, args.date)
    print(f"wrote {path.relative_to(REPO_ROOT)}, read from package H1")
    print(f"  {args.date}: {payload['day']['lit_hours']} lit hours, "
          f"{payload['day']['rain_mm']} mm, plays in {payload['day']['play_seconds']} s")
    for zone in payload["zones"]:
        last = zone["hours"][-1]
        print(f"  {zone['zone']} {zone['crop'][:22]:<22} light {last['light_mol_so_far']:>6.2f} mol, "
              f"soil {zone['soil_start']:>5.2f} -> {last['soil_mm']:>5.2f} mm")


if __name__ == "__main__":
    main()
