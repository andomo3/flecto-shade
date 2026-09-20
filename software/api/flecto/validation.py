"""Pydantic-style request validation, written against the standard library.

The repository pins three dependencies and adds none without a work package naming
them, so this module gives the shape a Pydantic model gives and nothing more: a
declarative field list, coercion, bounds, and one structured error listing every
problem at once, each with the field path and a stable code.

Replacing it with Pydantic later is a matter of rewriting the `Model` subclasses; the
router only ever sees `Model.parse(payload)` and `ValidationFailed`.
"""

from .errors import ValidationFailed

MISSING = object()


class Field:
    def __init__(self, kind, *, required=True, default=None, minimum=None, maximum=None,
                 choices=None, max_length=None, min_length=None, item=None):
        self.kind = kind
        self.required = required
        self.default = default
        self.minimum = minimum
        self.maximum = maximum
        self.choices = choices
        self.max_length = max_length
        self.min_length = min_length
        self.item = item

    def coerce(self, name, value, problems):
        if self.kind == "str":
            if not isinstance(value, str):
                return self.fail(name, "type_error", "This must be text.", problems)
            value = value.strip()
            if self.min_length is not None and len(value) < self.min_length:
                return self.fail(name, "too_short",
                                 f"Use at least {self.min_length} characters.", problems)
            if self.max_length is not None and len(value) > self.max_length:
                return self.fail(name, "too_long",
                                 f"Use at most {self.max_length} characters.", problems)
        elif self.kind == "int":
            if isinstance(value, bool) or not isinstance(value, int):
                return self.fail(name, "type_error", "This must be a whole number.", problems)
        elif self.kind == "float":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return self.fail(name, "type_error", "This must be a number.", problems)
            value = float(value)
        elif self.kind == "bool":
            if not isinstance(value, bool):
                return self.fail(name, "type_error", "This must be true or false.", problems)
        elif self.kind == "list":
            if not isinstance(value, list):
                return self.fail(name, "type_error", "This must be a list.", problems)
            if self.max_length is not None and len(value) > self.max_length:
                return self.fail(name, "too_long",
                                 f"Use at most {self.max_length} entries.", problems)
            if self.item is not None:
                cleaned = []
                for index, entry in enumerate(value):
                    cleaned.append(self.item.coerce(f"{name}[{index}]", entry, problems))
                value = cleaned
        elif self.kind == "dict":
            if not isinstance(value, dict):
                return self.fail(name, "type_error", "This must be an object.", problems)

        if self.choices is not None and value not in self.choices:
            allowed = ", ".join(str(choice) for choice in self.choices)
            return self.fail(name, "not_a_choice", f"Choose one of: {allowed}.", problems,
                             {"allowed": list(self.choices)})
        if self.minimum is not None and isinstance(value, (int, float)) and value < self.minimum:
            return self.fail(name, "below_minimum", f"This must be at least {self.minimum}.",
                             problems, {"minimum": self.minimum})
        if self.maximum is not None and isinstance(value, (int, float)) and value > self.maximum:
            return self.fail(name, "above_maximum", f"This must be at most {self.maximum}.",
                             problems, {"maximum": self.maximum})
        return value

    @staticmethod
    def fail(name, code, message, problems, details=None):
        problem = {"field": name, "code": code, "message": message}
        if details:
            problem["details"] = details
        problems.append(problem)
        return MISSING


class Model:
    """Subclasses declare `fields` and get `parse` and `parse_partial`."""

    fields = {}

    @classmethod
    def parse(cls, payload, *, partial=False):
        if payload is None:
            payload = {}
        if not isinstance(payload, dict):
            raise ValidationFailed([{
                "field": "body", "code": "type_error",
                "message": "The request body must be a JSON object.",
            }])

        problems, out = [], {}
        unknown = sorted(set(payload) - set(cls.fields))
        for name in unknown:
            problems.append({
                "field": name, "code": "unknown_field",
                "message": "This field is not part of the request.",
            })

        for name, field in cls.fields.items():
            if name not in payload:
                if partial:
                    continue
                if field.required:
                    problems.append({
                        "field": name, "code": "required",
                        "message": "This field is required.",
                    })
                else:
                    out[name] = field.default
                continue
            value = payload[name]
            if value is None and not field.required:
                out[name] = field.default
                continue
            coerced = field.coerce(name, value, problems)
            if coerced is not MISSING:
                out[name] = coerced

        if problems:
            raise ValidationFailed(problems)
        return out

    @classmethod
    def parse_partial(cls, payload):
        return cls.parse(payload, partial=True)


LIGHT_RULES = ("dli", "shade_pct")
OVERRIDE_COMMANDS = ("open", "closed")
OVERRIDE_DURATIONS = ("one_hour", "end_of_day")


class ZoneCreate(Model):
    fields = {
        "name": Field("str", min_length=1, max_length=60),
        "crop_profile_id": Field("str", required=False, default=None, max_length=64),
        "crop_name": Field("str", required=False, default=None, max_length=80),
        "light_rule": Field("str", choices=LIGHT_RULES),
        "light_target": Field("float", minimum=0.0, maximum=80.0),
        "soil_request_below_mm": Field("float", minimum=0.0, maximum=60.0),
        "rain_ok": Field("bool"),
        "kc": Field("float", required=False, default=1.0, minimum=0.1, maximum=2.0),
        "note": Field("str", required=False, default="", max_length=400),
    }


class ZonePatch(Model):
    fields = dict(ZoneCreate.fields)
    fields["expected_revision"] = Field("int", minimum=1)


class ReviewProfilePut(Model):
    fields = {
        "metrics": Field("list", item=Field("str", max_length=48), max_length=12),
        "expected_revision": Field("int", required=False, default=None, minimum=1),
    }


class OverrideCreate(Model):
    fields = {
        "command": Field("str", choices=OVERRIDE_COMMANDS),
        "duration": Field("str", choices=OVERRIDE_DURATIONS),
        "from_hour": Field("int", minimum=0, maximum=23),
        "reason": Field("str", required=False, default="", max_length=200),
        "idempotency_key": Field("str", required=False, default=None, max_length=80),
        "acknowledged_review": Field("bool", required=False, default=False),
    }


class RunCreate(Model):
    fields = {
        "date_local": Field("str", required=False, default=None, min_length=10, max_length=10),
        "note": Field("str", required=False, default="", max_length=200),
    }
