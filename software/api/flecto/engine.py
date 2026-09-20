"""The deterministic day engine, kept apart from storage and from presentation.

It holds no rules of its own. The nine rules, the light model, and the reference
evaporation are imported from package H1, `software/h1/build.py`, so that the API can
never drift from the simulation the data packages wrote. What this module adds is the
hourly loop for one local day, a per-zone soil request threshold a grower may set, and
timed manual overrides, none of which H1's year-long loop needs.

Nothing here reads a database, a request, or a clock. Give it a weather snapshot and a
list of zone configurations and it returns the same hours every time.
"""

import hashlib
import importlib.util
import json
from pathlib import Path

ENGINE_VERSION = "day-engine-1"

_API_DIR = Path(__file__).resolve().parents[1]
_H1_CANDIDATES = (
    _API_DIR.parent / "h1" / "build.py",              # repository layout
    _API_DIR.parent.parent / "software" / "h1" / "build.py",
)


def _load_h1():
    for candidate in _H1_CANDIDATES:
        if candidate.exists():
            spec = importlib.util.spec_from_file_location("h1_build", candidate)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise RuntimeError(
        "package H1 (software/h1/build.py) was not found; the API holds no rules of its own"
    )


H1 = _load_h1()

RULES = {
    "K": round(H1.K, 4),
    "T_STRUCT": H1.T_STRUCT,
    "T_CLOSED": H1.T_CLOSED,
    "MAKKINK_C": H1.MAKKINK_C,
    "LATENT_HEAT": H1.LATENT_HEAT_MJ_PER_KG,
    "GAMMA": round(H1.GAMMA, 6),
    "SOIL_CAPACITY": H1.SOIL_CAPACITY,
    "SOIL_DRY_BELOW": H1.SOIL_DRY_BELOW,
    "SOIL_FULL_AT": H1.SOIL_FULL_AT,
    "SOIL_IRRIGATE_BELOW": H1.SOIL_IRRIGATE_BELOW,
    "SOIL_START": H1.SOIL_START,
    "HARD_RAIN_MM": H1.HARD_RAIN_MM,
    "DRYING_HOURS": H1.DRYING_HOURS,
    "HEAT_SHADE_C": H1.HEAT_SHADE_C,
    "HEAT_SHADE_OPEN": H1.HEAT_SHADE_OPEN,
}

STATES = H1.STATES + ("MANUAL_OPEN", "MANUAL_SHUT")
REASONS = H1.REASONS + ("manual_override",)


def snapshot_digest(hours, sources):
    """A stable sha256 over the weather a run used, so a run names its own inputs."""
    canonical = json.dumps(
        {"hours": hours, "sources": sources}, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def config_digest(configs):
    canonical = json.dumps(configs, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def override_at(overrides, hour):
    """The override covering this hour, if one does. Expiry is a plain hour bound."""
    for override in overrides or ():
        if override["from_hour"] <= hour < override["until_hour"]:
            return override
    return None


def run_zone(config, hours, overrides=()):
    """Walk one local day for one zone. Returns 24 hour records, in order."""
    soil = float(config.get("soil_start", H1.SOIL_START))
    request_below = float(config.get("soil_request_below_mm", H1.SOIL_DRY_BELOW))
    crop = {
        "rain_ok": 1 if config["rain_ok"] else 0,
        "light_rule": config["light_rule"],
        "light_value": float(config["light_target"]),
    }
    kc = float(config.get("kc", 1.0))

    light = 0.0
    want_rain = soil < request_below
    out = []

    for index, hour in enumerate(hours):
        if hour["local_hour"] == 0:
            light = 0.0
        if soil < request_below:
            want_rain = True
        elif soil >= H1.SOIL_FULL_AT:
            want_rain = False

        automatic = H1.decide(crop, hours, index, light, want_rain)
        open_fraction, state, reason = automatic
        conflict = False

        manual = override_at(overrides, hour["local_hour"])
        if manual is not None:
            wants_open = manual["command"] == "open"
            if wants_open and hour["rain_mm"] >= H1.HARD_RAIN_MM:
                # The hard-rain rule outranks a manual command; the console says so.
                open_fraction, state, reason, conflict = 0.0, "RAIN_SHUT", "hard_rain", True
            elif wants_open and hour["ghi"] <= 0:
                open_fraction, state, reason, conflict = 0.0, "NIGHT", "", True
            else:
                open_fraction = 1.0 if wants_open else 0.0
                state = "MANUAL_OPEN" if wants_open else "MANUAL_SHUT"
                reason = "manual_override"

        light += H1.light_for_hour(hour["ghi"], open_fraction)

        before = soil
        soil = min(H1.SOIL_CAPACITY, soil + hour["rain_mm"] * open_fraction)
        rain_in = soil - before
        used = kc * H1.reference_evaporation(hour["ghi"], hour["t2m"]) * open_fraction * H1.T_STRUCT
        soil = max(0.0, soil - used)

        irrigation = 0.0
        if soil < H1.SOIL_IRRIGATE_BELOW:
            irrigation = H1.SOIL_FULL_AT - soil
            soil = H1.SOIL_FULL_AT

        out.append({
            "local_hour": hour["local_hour"],
            "open_fraction": round(open_fraction, 4),
            "light_mol_so_far": round(light, 2),
            "soil_mm": round(soil, 2),
            "rain_in_mm": round(rain_in, 2),
            "irrigation_mm": round(irrigation, 2),
            "crop_use_mm": round(used, 3),
            "state": state,
            "reason": reason,
            "conflict": conflict,
            "manual": manual is not None,
        })
    return out


def run_day(configs, hours, overrides_by_zone=None):
    """Run every zone over one weather snapshot. Deterministic, with no shared state."""
    overrides_by_zone = overrides_by_zone or {}
    return {
        config["zone_id"]: run_zone(config, hours, overrides_by_zone.get(config["zone_id"], ()))
        for config in configs
    }
