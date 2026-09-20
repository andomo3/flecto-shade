"""Structured errors with stable codes, so the console can explain a refusal.

Every failure the API can return is one of these codes. The console maps the code to a
state and a sentence; it never parses the message text.
"""


class ApiError(Exception):
    """A refusal the interface is expected to explain to a grower."""

    status = 400
    code = "bad_request"

    def __init__(self, message, *, code=None, status=None, field=None, details=None):
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code
        if status is not None:
            self.status = status
        self.field = field
        self.details = details or {}

    def payload(self):
        body = {"code": self.code, "message": self.message}
        if self.field:
            body["field"] = self.field
        if self.details:
            body["details"] = self.details
        return {"error": body}


class ValidationFailed(ApiError):
    status = 422
    code = "validation_failed"

    def __init__(self, problems):
        count = len(problems)
        noun = "field" if count == 1 else "fields"
        super().__init__(
            f"{count} {noun} in this request could not be accepted.",
            details={"problems": problems},
        )


class NotFound(ApiError):
    status = 404
    code = "not_found"


class ZoneNotFound(NotFound):
    code = "zone_not_found"


class RunNotFound(NotFound):
    code = "simulation_run_not_found"


class ZoneLimitReached(ApiError):
    status = 409
    code = "zone_limit_reached"


class ZoneArchived(ApiError):
    status = 409
    code = "zone_archived"


class RevisionConflict(ApiError):
    status = 409
    code = "revision_conflict"


class MetricNotSupported(ApiError):
    status = 422
    code = "metric_not_supported"


class SafetyRuleBlocked(ApiError):
    status = 409
    code = "safety_rule_blocked"


class MethodNotAllowed(ApiError):
    status = 405
    code = "method_not_allowed"


class StorageUnavailable(ApiError):
    status = 503
    code = "storage_unavailable"
