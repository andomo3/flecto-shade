"""Persistence: immutable configuration revisions, immutable runs, an append-only log.

SQLite is the local development and offline demonstration store. PostgreSQL is the
deployed store, reached through the same `Database` seam: every statement here is plain
SQL with positional parameters, and the only SQLite-specific piece is the connection.

Nothing in this module decides anything about the roof. It writes what the engine
produced and refuses what the rules of the product forbid, such as a fifth active zone.
"""

import json
import os
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .errors import (
    RevisionConflict, RunNotFound, StorageUnavailable, ZoneArchived,
    ZoneLimitReached, ZoneNotFound,
)
from . import metrics as metric_registry

MAX_ACTIVE_ZONES = 4
ZONE_LETTERS = ("A", "B", "C", "D")
DEFAULT_SITE = "apopka-demo"

MIGRATIONS = [
    (
        1,
        "initial schema",
        [
            """CREATE TABLE sites (
                 id TEXT PRIMARY KEY,
                 name TEXT NOT NULL,
                 timezone TEXT NOT NULL,
                 created_at TEXT NOT NULL
               )""",
            """CREATE TABLE crop_profiles (
                 id TEXT PRIMARY KEY,
                 site_id TEXT NOT NULL,
                 name TEXT NOT NULL,
                 botanical TEXT NOT NULL DEFAULT '',
                 light_rule TEXT NOT NULL,
                 light_target REAL NOT NULL,
                 kc REAL NOT NULL,
                 rain_ok INTEGER NOT NULL,
                 source_url TEXT NOT NULL DEFAULT '',
                 created_at TEXT NOT NULL
               )""",
            """CREATE TABLE zones (
                 id TEXT PRIMARY KEY,
                 site_id TEXT NOT NULL,
                 letter TEXT NOT NULL,
                 position INTEGER NOT NULL,
                 archived_at TEXT,
                 created_at TEXT NOT NULL,
                 current_revision INTEGER NOT NULL DEFAULT 1
               )""",
            """CREATE TABLE zone_config_revisions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 zone_id TEXT NOT NULL,
                 revision INTEGER NOT NULL,
                 name TEXT NOT NULL,
                 crop_profile_id TEXT,
                 crop_name TEXT NOT NULL,
                 light_rule TEXT NOT NULL,
                 light_target REAL NOT NULL,
                 soil_request_below_mm REAL NOT NULL,
                 rain_ok INTEGER NOT NULL,
                 kc REAL NOT NULL,
                 note TEXT NOT NULL DEFAULT '',
                 created_at TEXT NOT NULL,
                 created_by TEXT NOT NULL DEFAULT 'console',
                 UNIQUE (zone_id, revision)
               )""",
            """CREATE TABLE review_profiles (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 zone_id TEXT NOT NULL,
                 revision INTEGER NOT NULL,
                 metrics_json TEXT NOT NULL,
                 created_at TEXT NOT NULL,
                 UNIQUE (zone_id, revision)
               )""",
            """CREATE TABLE weather_input_snapshots (
                 id TEXT PRIMARY KEY,
                 date_local TEXT NOT NULL,
                 sha256 TEXT NOT NULL,
                 sources_json TEXT NOT NULL,
                 hours_json TEXT NOT NULL,
                 created_at TEXT NOT NULL
               )""",
            """CREATE TABLE simulation_runs (
                 id TEXT PRIMARY KEY,
                 site_id TEXT NOT NULL,
                 date_local TEXT NOT NULL,
                 weather_snapshot_id TEXT NOT NULL,
                 config_snapshot_json TEXT NOT NULL,
                 config_sha256 TEXT NOT NULL,
                 engine_version TEXT NOT NULL,
                 note TEXT NOT NULL DEFAULT '',
                 created_at TEXT NOT NULL
               )""",
            """CREATE TABLE zone_hour_results (
                 run_id TEXT NOT NULL,
                 zone_id TEXT NOT NULL,
                 local_hour INTEGER NOT NULL,
                 open_fraction REAL NOT NULL,
                 light_mol_so_far REAL NOT NULL,
                 soil_mm REAL NOT NULL,
                 rain_in_mm REAL NOT NULL,
                 irrigation_mm REAL NOT NULL,
                 state TEXT NOT NULL,
                 reason TEXT NOT NULL,
                 conflict INTEGER NOT NULL DEFAULT 0,
                 manual INTEGER NOT NULL DEFAULT 0,
                 PRIMARY KEY (run_id, zone_id, local_hour)
               )""",
            """CREATE TABLE control_events (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 zone_id TEXT NOT NULL,
                 site_id TEXT NOT NULL,
                 kind TEXT NOT NULL,
                 payload_json TEXT NOT NULL,
                 actor TEXT NOT NULL DEFAULT 'console',
                 idempotency_key TEXT,
                 created_at TEXT NOT NULL
               )""",
            """CREATE TABLE manual_overrides (
                 id TEXT PRIMARY KEY,
                 zone_id TEXT NOT NULL,
                 command TEXT NOT NULL,
                 duration TEXT NOT NULL,
                 from_hour INTEGER NOT NULL,
                 until_hour INTEGER NOT NULL,
                 reason TEXT NOT NULL DEFAULT '',
                 idempotency_key TEXT,
                 created_at TEXT NOT NULL,
                 released_at TEXT
               )""",
            "CREATE UNIQUE INDEX idx_override_key ON manual_overrides (zone_id, idempotency_key)",
            "CREATE INDEX idx_zone_site ON zones (site_id, archived_at)",
            "CREATE INDEX idx_events_zone ON control_events (zone_id, id)",
            "CREATE INDEX idx_results_run ON zone_hour_results (run_id, zone_id)",
        ],
    ),
]


def now_iso():
    """Server-generated, never taken from a request."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def database_path():
    explicit = os.environ.get("FLECTO_DB")
    if explicit:
        return Path(explicit)
    if os.environ.get("VERCEL"):
        # A serverless filesystem is writable only under /tmp, and /tmp does not
        # outlive the instance. Deployed persistence belongs in PostgreSQL.
        return Path("/tmp/flecto.db")
    return Path(__file__).resolve().parents[1] / "var" / "flecto.db"


class Database:
    """The seam PostgreSQL slots into. SQLite is what the offline demonstration uses."""

    def __init__(self, path=None):
        url = os.environ.get("DATABASE_URL", "")
        if url.startswith("postgres"):
            raise StorageUnavailable(
                "DATABASE_URL names PostgreSQL, and no PostgreSQL driver is installed. "
                "Adding one is a named dependency decision for the backend work package."
            )
        self.path = Path(path) if path else database_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.path), timeout=5.0)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def query(self, sql, params=()):
        return [dict(row) for row in self.connection.execute(sql, params).fetchall()]

    def one(self, sql, params=()):
        rows = self.query(sql, params)
        return rows[0] if rows else None

    def execute(self, sql, params=()):
        return self.connection.execute(sql, params)

    def commit(self):
        self.connection.commit()


def migrate(db):
    """Applied by an explicit deployment step, never from inside a request handler."""
    db.execute("""CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    applied_at TEXT NOT NULL)""")
    applied = {row["version"] for row in db.query("SELECT version FROM schema_migrations")}
    for version, name, statements in MIGRATIONS:
        if version in applied:
            continue
        for statement in statements:
            db.execute(statement)
        db.execute("INSERT INTO schema_migrations (version, name, applied_at) VALUES (?, ?, ?)",
                   (version, name, now_iso()))
    db.commit()
    return sorted({row["version"] for row in db.query("SELECT version FROM schema_migrations")})


# --------------------------------------------------------------------------- zones

def ensure_site(db, site_id=DEFAULT_SITE, name="Apopka demonstration shade house"):
    site = db.one("SELECT * FROM sites WHERE id = ?", (site_id,))
    if site:
        return site
    db.execute("INSERT INTO sites (id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
               (site_id, name, "America/New_York", now_iso()))
    db.commit()
    return db.one("SELECT * FROM sites WHERE id = ?", (site_id,))


def active_zones(db, site_id):
    return db.query(
        "SELECT * FROM zones WHERE site_id = ? AND archived_at IS NULL ORDER BY position",
        (site_id,))


def all_zones(db, site_id):
    return db.query("SELECT * FROM zones WHERE site_id = ? ORDER BY archived_at IS NOT NULL, position",
                    (site_id,))


def get_zone(db, zone_id):
    zone = db.one("SELECT * FROM zones WHERE id = ?", (zone_id,))
    if not zone:
        raise ZoneNotFound(f"No zone {zone_id!r} exists.", details={"zone_id": zone_id})
    return zone


def current_config(db, zone_id):
    return db.one(
        "SELECT * FROM zone_config_revisions WHERE zone_id = ? ORDER BY revision DESC LIMIT 1",
        (zone_id,))


def config_at(db, zone_id, revision):
    return db.one("SELECT * FROM zone_config_revisions WHERE zone_id = ? AND revision = ?",
                  (zone_id, revision))


def review_profile(db, zone_id):
    row = db.one(
        "SELECT * FROM review_profiles WHERE zone_id = ? ORDER BY revision DESC LIMIT 1",
        (zone_id,))
    return json.loads(row["metrics_json"]) if row else list(metric_registry.DEFAULT_PROFILE)


def next_letter(db, site_id):
    taken = {row["letter"] for row in active_zones(db, site_id)}
    for letter in ZONE_LETTERS:
        if letter not in taken:
            return letter
    raise ZoneLimitReached(
        f"This site already has {MAX_ACTIVE_ZONES} active zones, the roof's limit. "
        "Archive a zone before adding another.",
        details={"limit": MAX_ACTIVE_ZONES, "active": len(taken)},
    )


def log_event(db, zone_id, site_id, kind, payload, idempotency_key=None, actor="console"):
    db.execute(
        """INSERT INTO control_events (zone_id, site_id, kind, payload_json, actor,
                                       idempotency_key, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (zone_id, site_id, kind, json.dumps(payload, sort_keys=True), actor,
         idempotency_key, now_iso()))


def create_zone(db, site_id, data):
    ensure_site(db, site_id)
    if len(active_zones(db, site_id)) >= MAX_ACTIVE_ZONES:
        raise ZoneLimitReached(
            f"This site already has {MAX_ACTIVE_ZONES} active zones, the roof's limit. "
            "Archive a zone before adding another.",
            details={"limit": MAX_ACTIVE_ZONES, "active": len(active_zones(db, site_id))},
        )
    letter = next_letter(db, site_id)
    zone_id = new_id("zone")
    position = len(active_zones(db, site_id))
    stamp = now_iso()
    db.execute(
        """INSERT INTO zones (id, site_id, letter, position, archived_at, created_at,
                              current_revision)
           VALUES (?, ?, ?, ?, NULL, ?, 1)""",
        (zone_id, site_id, letter, position, stamp))
    write_revision(db, zone_id, 1, data, stamp)
    db.execute(
        "INSERT INTO review_profiles (zone_id, revision, metrics_json, created_at) VALUES (?, ?, ?, ?)",
        (zone_id, 1, json.dumps(list(metric_registry.DEFAULT_PROFILE)), stamp))
    log_event(db, zone_id, site_id, "zone_created", {"letter": letter, "revision": 1})
    db.commit()
    return get_zone(db, zone_id)


def write_revision(db, zone_id, revision, data, stamp=None):
    stamp = stamp or now_iso()
    db.execute(
        """INSERT INTO zone_config_revisions
             (zone_id, revision, name, crop_profile_id, crop_name, light_rule, light_target,
              soil_request_below_mm, rain_ok, kc, note, created_at, created_by)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'console')""",
        (zone_id, revision, data["name"], data.get("crop_profile_id"),
         data.get("crop_name") or data["name"], data["light_rule"],
         float(data["light_target"]), float(data["soil_request_below_mm"]),
         1 if data["rain_ok"] else 0, float(data.get("kc") or 1.0),
         data.get("note") or "", stamp))


def update_zone(db, zone_id, data):
    """A change writes a new revision. Earlier revisions are never rewritten."""
    zone = get_zone(db, zone_id)
    if zone["archived_at"]:
        raise ZoneArchived("This zone is archived. Restore it before changing it.",
                           details={"zone_id": zone_id})
    current = current_config(db, zone_id)
    expected = data.pop("expected_revision")
    if expected != current["revision"]:
        raise RevisionConflict(
            "This zone changed while the form was open. Reload it and review the change again.",
            details={"expected_revision": expected, "current_revision": current["revision"]},
        )
    revision = current["revision"] + 1
    merged = {
        "name": data.get("name", current["name"]),
        "crop_profile_id": data.get("crop_profile_id", current["crop_profile_id"]),
        "crop_name": data.get("crop_name", current["crop_name"]),
        "light_rule": data.get("light_rule", current["light_rule"]),
        "light_target": data.get("light_target", current["light_target"]),
        "soil_request_below_mm": data.get("soil_request_below_mm",
                                          current["soil_request_below_mm"]),
        "rain_ok": data.get("rain_ok", bool(current["rain_ok"])),
        "kc": data.get("kc", current["kc"]),
        "note": data.get("note", current["note"]),
    }
    write_revision(db, zone_id, revision, merged)
    db.execute("UPDATE zones SET current_revision = ? WHERE id = ?", (revision, zone_id))
    log_event(db, zone_id, zone["site_id"], "config_revised",
              {"revision": revision, "changed": sorted(data)})
    db.commit()
    return get_zone(db, zone_id)


def archive_zone(db, zone_id):
    """Archiving hides a zone from the roof. Every run it appears in stays readable."""
    zone = get_zone(db, zone_id)
    if zone["archived_at"]:
        return zone
    db.execute("UPDATE zones SET archived_at = ? WHERE id = ?", (now_iso(), zone_id))
    log_event(db, zone_id, zone["site_id"], "zone_archived", {"revision": zone["current_revision"]})
    db.commit()
    return get_zone(db, zone_id)


def restore_zone(db, zone_id):
    zone = get_zone(db, zone_id)
    if not zone["archived_at"]:
        return zone
    site_id = zone["site_id"]
    if len(active_zones(db, site_id)) >= MAX_ACTIVE_ZONES:
        raise ZoneLimitReached(
            f"This site already has {MAX_ACTIVE_ZONES} active zones, the roof's limit.",
            details={"limit": MAX_ACTIVE_ZONES},
        )
    db.execute("UPDATE zones SET archived_at = NULL WHERE id = ?", (zone_id,))
    log_event(db, zone_id, site_id, "zone_restored", {})
    db.commit()
    return get_zone(db, zone_id)


def set_review_profile(db, zone_id, wanted):
    zone = get_zone(db, zone_id)
    cleaned = metric_registry.validate_profile(wanted)
    row = db.one("SELECT MAX(revision) AS top FROM review_profiles WHERE zone_id = ?", (zone_id,))
    revision = (row["top"] or 0) + 1
    db.execute(
        "INSERT INTO review_profiles (zone_id, revision, metrics_json, created_at) VALUES (?, ?, ?, ?)",
        (zone_id, revision, json.dumps(cleaned), now_iso()))
    log_event(db, zone_id, zone["site_id"], "review_profile_set", {"metrics": cleaned})
    db.commit()
    return cleaned


# ----------------------------------------------------------------------- overrides

def active_overrides(db, zone_id):
    return db.query(
        "SELECT * FROM manual_overrides WHERE zone_id = ? AND released_at IS NULL ORDER BY id",
        (zone_id,))


def override_by_key(db, zone_id, key):
    if not key:
        return None
    return db.one("SELECT * FROM manual_overrides WHERE zone_id = ? AND idempotency_key = ?",
                  (zone_id, key))


def create_override(db, zone_id, data):
    """Idempotent: the same key returns the override the key already made."""
    zone = get_zone(db, zone_id)
    if zone["archived_at"]:
        raise ZoneArchived("This zone is archived and takes no commands.",
                           details={"zone_id": zone_id})
    existing = override_by_key(db, zone_id, data.get("idempotency_key"))
    if existing:
        return existing, True

    from_hour = int(data["from_hour"])
    until_hour = from_hour + 1 if data["duration"] == "one_hour" else 24
    override_id = new_id("ovr")
    stamp = now_iso()
    for row in active_overrides(db, zone_id):
        db.execute("UPDATE manual_overrides SET released_at = ? WHERE id = ?", (stamp, row["id"]))
    db.execute(
        """INSERT INTO manual_overrides
             (id, zone_id, command, duration, from_hour, until_hour, reason,
              idempotency_key, created_at, released_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)""",
        (override_id, zone_id, data["command"], data["duration"], from_hour, until_hour,
         data.get("reason") or "", data.get("idempotency_key"), stamp))
    log_event(db, zone_id, zone["site_id"], "manual_override_applied", {
        "command": data["command"], "duration": data["duration"],
        "from_hour": from_hour, "until_hour": until_hour,
    }, idempotency_key=data.get("idempotency_key"))
    db.commit()
    return db.one("SELECT * FROM manual_overrides WHERE id = ?", (override_id,)), False


def return_to_automatic(db, zone_id, at_hour=None):
    zone = get_zone(db, zone_id)
    stamp = now_iso()
    released = []
    for row in active_overrides(db, zone_id):
        db.execute("UPDATE manual_overrides SET released_at = ? WHERE id = ?", (stamp, row["id"]))
        released.append(row["id"])
    log_event(db, zone_id, zone["site_id"], "returned_to_automatic",
              {"released": released, "at_hour": at_hour})
    db.commit()
    return released


def effective_overrides(db, zone_id):
    """Overrides the engine should honour: still held, and not past their expiry hour."""
    return [
        {"id": row["id"], "command": row["command"], "duration": row["duration"],
         "from_hour": row["from_hour"], "until_hour": row["until_hour"]}
        for row in active_overrides(db, zone_id)
    ]


def control_events(db, zone_id, limit=50):
    return db.query(
        "SELECT * FROM control_events WHERE zone_id = ? ORDER BY id DESC LIMIT ?",
        (zone_id, int(limit)))


# ----------------------------------------------------------------------------- runs

def save_weather_snapshot(db, date_local, hours, sources, digest):
    existing = db.one("SELECT * FROM weather_input_snapshots WHERE sha256 = ?", (digest,))
    if existing:
        return existing
    snapshot_id = new_id("wx")
    db.execute(
        """INSERT INTO weather_input_snapshots
             (id, date_local, sha256, sources_json, hours_json, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (snapshot_id, date_local, digest, json.dumps(sources, sort_keys=True),
         json.dumps(hours, sort_keys=True), now_iso()))
    db.commit()
    return db.one("SELECT * FROM weather_input_snapshots WHERE id = ?", (snapshot_id,))


def save_run(db, site_id, date_local, snapshot_id, configs, config_sha, engine_version,
             results, note=""):
    run_id = new_id("run")
    db.execute(
        """INSERT INTO simulation_runs
             (id, site_id, date_local, weather_snapshot_id, config_snapshot_json,
              config_sha256, engine_version, note, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (run_id, site_id, date_local, snapshot_id,
         json.dumps(configs, sort_keys=True), config_sha, engine_version, note, now_iso()))
    for zone_id, hours in results.items():
        for hour in hours:
            db.execute(
                """INSERT INTO zone_hour_results
                     (run_id, zone_id, local_hour, open_fraction, light_mol_so_far, soil_mm,
                      rain_in_mm, irrigation_mm, state, reason, conflict, manual)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (run_id, zone_id, hour["local_hour"], hour["open_fraction"],
                 hour["light_mol_so_far"], hour["soil_mm"], hour["rain_in_mm"],
                 hour["irrigation_mm"], hour["state"], hour["reason"],
                 1 if hour["conflict"] else 0, 1 if hour["manual"] else 0))
    db.commit()
    return get_run(db, run_id)


def get_run(db, run_id):
    run = db.one("SELECT * FROM simulation_runs WHERE id = ?", (run_id,))
    if not run:
        raise RunNotFound(f"No simulation run {run_id!r} exists.", details={"run_id": run_id})
    return run


def run_results(db, run_id):
    return db.query(
        "SELECT * FROM zone_hour_results WHERE run_id = ? ORDER BY zone_id, local_hour",
        (run_id,))


def list_runs(db, site_id, limit=20):
    return db.query(
        "SELECT * FROM simulation_runs WHERE site_id = ? ORDER BY created_at DESC, id DESC LIMIT ?",
        (site_id, int(limit)))


def weather_snapshot(db, snapshot_id):
    return db.one("SELECT * FROM weather_input_snapshots WHERE id = ?", (snapshot_id,))


def open_database(path=None, auto_migrate=None):
    db = Database(path)
    if auto_migrate is None:
        auto_migrate = os.environ.get("FLECTO_AUTO_MIGRATE", "1") != "0"
    if auto_migrate:
        for attempt in range(3):
            try:
                migrate(db)
                break
            except sqlite3.OperationalError:
                if attempt == 2:
                    raise
                time.sleep(0.05)
    return db
