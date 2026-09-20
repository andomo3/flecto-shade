# Deploy the shade-house demo

Deploy `software/page` as a static site. No Docker, frontend build, API keys,
database, or Python server is needed on the host.

| Route | Available on a static host |
|---|---|
| `/` or `/index.html` | Farmer-selected CAD watering, rain events, flap animation and JSON export |
| `/console.html` | Secondary weather and zone console; configuration stays in the browser session |
| `/replay.html` | Redirects to the secondary console |

The pages use separate renderers and stylesheets. Only the secondary console
attempts to use `/api`; its offline state is expected on static hosting.
Changes to console configuration do not persist across reloads without the API.
The primary watering flow does not need the API.

## Vercel: recommended setup

1. [Import the GitHub repository](https://vercel.com/new).
2. Set **Root Directory** to **`software/page`**, **Framework Preset** to
   **Other**, and **Production Branch** to **`main`**.
3. Deploy. `software/page/vercel.json` sets an empty build command, an empty
   install command, output directory `.`, and `no-store` caching so edits
   cannot be hidden by stale unversioned assets.

There are no environment variables to add. The allowlist in `.vercelignore`
includes browser assets and excludes the Python asset generators and caches.
Do not select `software` as the root for this static-only project: that selects
the separate optional API configuration.

While the integration PR is open, deploy its branch as a preview. Once reviewed
and merged, Vercel's Git integration can publish subsequent `main` updates.
Require the GitHub `Checks` status before merging; the Vercel Git integration
itself is not a replacement for the test gate.

Provider references: [build settings](https://vercel.com/docs/builds/configure-a-build),
[configuration](https://vercel.com/docs/project-configuration/vercel-json),
[file exclusions](https://vercel.com/docs/deployments/vercel-ignore).

## Portable bundle

Every successful GitHub Actions `CI` run attaches a `flecto-shade-static`
artifact, retained for 14 days. Download it from the run's summary and extract
the enclosed `flecto-shade-static.zip`. Publish the directory containing
`index.html`, not a parent directory containing only the zip.

Create the same zip locally from a committed revision, with Git installed:

```bash
git archive --format=zip --output=flecto-shade-static.zip HEAD:software/page '*.html' '*.css' '*.js' '*.json' '*.svg' .vercelignore
```

Run this from the repository root. The command packages **HEAD**, so commit
intended edits first. The zip includes the checked-in model, controller map,
weather day, JavaScript and styles. It excludes Python, SQLite, weather source
downloads, credentials and caches. Do not commit the generated zip.

The extracted files work with any ordinary static host that serves `index.html`
at `/` and preserves explicit `.html` paths. There is no SPA fallback or API
rewrite to configure. A host other than Vercel should disable long-lived caching
for these unversioned files.

To rehearse the extracted bundle with Python:

```bash
python -m http.server --directory path/to/extracted/site 8000
```

Open `http://localhost:8000`; opening `index.html` directly as a file will not
support the JSON fetches.

## Verify the published URL

- Open `/` in a fresh browser session. Check that the CAD roof and soil grid load.
- Select the two-footprint example and run rain: 42/42 targets, 21.1 mL selected
  delivery, zero outside delivery and overflow; flaps animate and close.
- Export JSON, reset, and check selection edits and shortfall/spill cases.
- Follow the console link, play its weather day, and exercise the camera.
- Confirm the console reports offline/session-only configuration; an unavailable
  `/api` is expected for this deployment.
- Open `/console.html` and `/replay.html` directly; follow the return link.
- Check a narrow viewport and look for unexpected runtime errors or missing
  scripts, styles, `model.json`, `controller-map.json`, or `day.json`.
- Add the actual URL to the README only after checking it.

Automated tests do not establish deployed browser acceptance, physical rain
delivery, crop performance, soil restoration or water savings at farm scale.
The default water volumes are simulated at the approximately 129 × 304 mm CAD scale.

## Optional local API

The API is useful for local console persistence, but is not part of the static
release:

```bash
python software/api/local_server.py --port 8000
```

This serves watering at `/`, the console at `/console.html`, and health at
`/api/health`. See [API setup](api/README.md) for SQLite storage configuration.

`software/vercel.json` remains a separate experimental API deployment
configuration, selected only when the project root is `software`. It rewrites
`/api/(.*)` to `api/index.py` and outputs `page`. Do not use it to promise durable
production storage: the repository has no PostgreSQL driver, and serverless
local files are not a persistent database. A PostgreSQL `DATABASE_URL` currently
returns `storage_unavailable`.

Before a future API release, implement and test persistent storage, provision
separate production/preview data, keep credentials in provider environment
variables, set `FLECTO_AUTO_MIGRATE=0`, and apply migrations explicitly. Use a
separate hosting project so that API work cannot disrupt the static demo.
