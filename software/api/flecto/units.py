"""Canonical internal units, converted only at the API boundary.

Inside the engine and the store every depth is millimetres, every temperature is
degrees Celsius, every irradiance is watts per square metre, and daily light is moles
of photosynthetic photons per square metre per day. A response converts once, on the
way out, and says in the payload which system it used.
"""

CANONICAL = {
    "depth": "mm",
    "temperature": "degC",
    "irradiance": "W m-2",
    "daily_light": "mol m-2 d-1",
}

SYSTEMS = ("metric", "us")

DISPLAY = {
    "metric": dict(CANONICAL),
    "us": {
        "depth": "in",
        "temperature": "degF",
        "irradiance": "W m-2",
        "daily_light": "mol m-2 d-1",
    },
}

MM_PER_INCH = 25.4


def convert(quantity, value, system):
    """Convert one canonical value into the display system. Returns a float or None."""
    if value is None:
        return None
    if system == "metric":
        return round(float(value), 4)
    if quantity == "depth":
        return round(float(value) / MM_PER_INCH, 4)
    if quantity == "temperature":
        return round(float(value) * 9.0 / 5.0 + 32.0, 4)
    return round(float(value), 4)


def resolve(system):
    return system if system in SYSTEMS else "metric"


def unit_block(system):
    system = resolve(system)
    return {"system": system, "canonical": dict(CANONICAL), "display": dict(DISPLAY[system])}
