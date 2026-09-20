"""Seed the store from the committed simulation, so the demonstration opens ready.

The three zones the pitch shows are package H1's crops, read from the same day.json the
page reads. Seeding writes revision 1 of each zone and nothing else; every later change
is an ordinary revision, and the seed never runs twice.
"""

from . import store, weather

SOIL_REQUEST_DEFAULT = 30.0


def seed_site(db, site_id=store.DEFAULT_SITE):
    store.ensure_site(db)
    if store.all_zones(db, site_id):
        return store.active_zones(db, site_id)

    day = weather.load_day()
    for zone in day["zones"][:store.MAX_ACTIVE_ZONES]:
        store.create_zone(db, site_id, {
            "name": zone["crop"],
            "crop_profile_id": None,
            "crop_name": zone["crop"],
            "light_rule": zone["light_rule"],
            "light_target": float(zone["light_target"]),
            "soil_request_below_mm": float(
                day["constants"].get("SOIL_DRY_BELOW", SOIL_REQUEST_DEFAULT)),
            "rain_ok": bool(zone["rain_ok"]),
            "kc": float(zone.get("kc", 1.0)),
            "note": zone.get("note", "")[:400],
        })
    return store.active_zones(db, site_id)
