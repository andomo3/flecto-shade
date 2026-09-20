"""Apply database migrations as an explicit deployment step.

    python software/api/migrate.py

A Function never migrates on its own in a deployed environment: set
FLECTO_AUTO_MIGRATE=0 there and run this from the deployment pipeline instead.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from flecto import seed, store  # noqa: E402


def main():
    db = store.open_database(auto_migrate=False)
    applied = store.migrate(db)
    zones = seed.seed_site(db)
    print(f"database {db.path}")
    print(f"migrations applied: {applied}")
    print(f"zones ready: {', '.join(zone['letter'] for zone in zones) or 'none'}")
    db.close()


if __name__ == "__main__":
    main()
