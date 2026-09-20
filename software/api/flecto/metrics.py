"""The controlled registry of metrics a grower may put in the zone overview.

A review profile is a list of identifiers from this registry, in the grower's order.
It is never a formula and never arbitrary code: an identifier the registry does not
hold is refused with `metric_not_supported`, so nothing a grower types can reach the
deterministic engine.
"""

from .errors import MetricNotSupported

METRIC_DEFINITIONS = [
    {
        "id": "roof_position",
        "label": "Roof position",
        "help": "The modelled roof command for this zone at the shown hour.",
        "quantity": "text",
        "removable": False,
    },
    {
        "id": "control_state",
        "label": "Control state",
        "help": "Automatic, manual override, conflict, stale, or offline.",
        "quantity": "text",
        "removable": False,
    },
    {
        "id": "decision_reason",
        "label": "Decision reason",
        "help": "The deterministic rule that set the modelled roof position, in plain words.",
        "quantity": "text",
        "removable": False,
    },
    {
        "id": "rain_outcome",
        "label": "Rain admitted or excluded",
        "help": "Whether gauge-recorded rain reached this zone's modelled soil.",
        "quantity": "text",
        "removable": True,
    },
    {
        "id": "daily_light",
        "label": "Daily light against target",
        "help": "Modelled daily light integral so far against the crop's target.",
        "quantity": "daily_light",
        "removable": True,
    },
    {
        "id": "soil_water",
        "label": "Modelled soil water",
        "help": "Modelled root-zone water against the rain-request threshold.",
        "quantity": "depth",
        "removable": True,
    },
    {
        "id": "last_decision",
        "label": "Last decision",
        "help": "The modelled hour at which this zone last changed roof position.",
        "quantity": "text",
        "removable": True,
    },
    {
        "id": "next_action",
        "label": "Next expected action",
        "help": "The next modelled hour at which this zone is due to change.",
        "quantity": "text",
        "removable": True,
    },
    {
        "id": "data_timestamp",
        "label": "Data timestamp",
        "help": "The historical input hour the shown values were modelled from.",
        "quantity": "text",
        "removable": True,
    },
    {
        "id": "irrigation",
        "label": "Modelled irrigation added",
        "help": "Water the modelled grower added when the soil fell past the floor.",
        "quantity": "depth",
        "removable": True,
    },
]

BY_ID = {item["id"]: item for item in METRIC_DEFINITIONS}

REQUIRED_METRICS = tuple(item["id"] for item in METRIC_DEFINITIONS if not item["removable"])

# The console renders roof_position and control_state in the row's own header, so they
# are required but never repeated in the body. The data timestamp is the same hour for
# every zone and is on screen elsewhere, and the last decision is the first line of the
# selected zone's history, so neither is on by default. Both stay in the registry.
DEFAULT_PROFILE = [
    "roof_position", "control_state", "decision_reason", "rain_outcome",
    "daily_light", "soil_water", "next_action",
]


def validate_profile(metrics):
    """Return the cleaned profile, or refuse with a stable code."""
    seen, cleaned = set(), []
    for metric in metrics:
        if metric not in BY_ID:
            raise MetricNotSupported(
                f"{metric!r} is not a supported metric.",
                field="metrics",
                details={"supported": sorted(BY_ID)},
            )
        if metric in seen:
            continue
        seen.add(metric)
        cleaned.append(metric)

    missing = [metric for metric in REQUIRED_METRICS if metric not in seen]
    if missing:
        raise MetricNotSupported(
            "The overview must keep the roof position, the control state, and the reason.",
            field="metrics",
            details={"required": list(REQUIRED_METRICS), "missing": missing},
        )
    return cleaned
