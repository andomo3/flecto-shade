# Deploying the console on Vercel, without breaking the laptop

The laptop copy is the demonstration.
Vercel is the live link for the README and the backup at the table.
Nothing in this file changes a rule in `AGENTS.md`: the page makes no outside request, no token or Vercel setting is committed, and everything still builds and runs with no network.

## The static demonstration

The page is a static directory.
It needs no build step, no Node, and no API.

Project settings on Vercel, set once by a person:

- Framework preset: Other.
- Root Directory: `software`.
- Build Command: leave empty.
- Output Directory: `page`, which `software/vercel.json` also declares as `"outputDirectory": "page"`.
- Install Command: leave empty.

`software/vercel.json` is the one active configuration.
There is no longer a `vercel.json` under `software/page/`; it was moved up so that the same file can carry the static headers and the API rewrite.

It sets:

- `no-store, must-revalidate` on HTML and on `/`, so a new deployment shows at once.
- `public, max-age=0, must-revalidate` on `day.json`, on every `.css`, and on every `.js`, because these assets do not use hashed file names and a stale copy would show an old simulated day.
- `no-store` on everything under `/api/`.
- A rewrite from `/api/(.*)` to `/api/index`, so one Python function serves every route.

What to check on the deployed address, in a private window:

- The page loads from a clean browser session, with the laptop's network otherwise unused.
- `day.json` returns 200 and the console plays the simulated day.
- The WebGL model draws, and orbit, pan, zoom, and the arrow keys all work.
- Direct navigation to the address works, not only a reload.
- The words "simulated" and "modelled" are visible, and the credit to ITKE at the University of Stuttgart with patent EP2320015 is in the footer.
- No secret, token, or connection string appears in the page source or in the deployment log.

## The Python API

The entry point is `software/api/index.py`, a `BaseHTTPRequestHandler` named `handler`, which Vercel's Python runtime calls.
Every rule, query, and conversion lives in `software/api/flecto/`, outside the request handler, so the same code runs locally with no network.

- Python 3.13, declared in `software/.python-version` and set in the project's settings.
- Runtime dependencies stay pinned in `software/requirements.txt`. The API adds none.
- `software/vercel.json` excludes tests, the local database, and bytecode from the function bundle.
- Routes are served under `/api`, errors are structured JSON with stable codes, and responses carrying configuration, overrides, or results are `no-store`.
- `/api/health` reports availability and nothing about credentials or internals.

## Production persistence

SQLite is for local development and the offline demonstration only.
A serverless filesystem is writable only under `/tmp`, and `/tmp` does not outlive the instance, so a deployed SQLite database is not persistence.

For a deployed store, use a PostgreSQL provider through the Vercel Marketplace, with:

- credentials only in Vercel environment variables, never in a file, a commit, a prompt, or a log,
- a pooled connection suitable for serverless execution,
- the Function region close to the database region,
- separate production and preview databases, or separate schemas with strict isolation,
- migrations applied by an explicit deployment step running `python software/api/migrate.py`, with `FLECTO_AUTO_MIGRATE=0` set so no function invocation migrates on its own.

A PostgreSQL driver is a dependency the repository has not approved yet.
Until a work package names it, `DATABASE_URL` pointing at PostgreSQL returns `storage_unavailable` with a clear message, and the console shows its offline state.

## Environment variables

| Name | Needed when |
|---|---|
| `DATABASE_URL` | A deployed store is connected |
| `APP_ENV` | Always, to tell production from preview in `/api/health` |
| `FLECTO_AUTO_MIGRATE` | Set to `0` in any deployed environment |
| `SESSION_SECRET` | Only if authentication is added |
| `ALLOWED_ORIGIN` | Only if the API is deployed apart from the page |

None of these belong in the repository.

## Workflow

- Preview deployments come from a feature or package branch, production only from `main`.
- A package whose tests or repository gates are failing is not deployed.
- The preview address is checked against the list above before it is promoted.
- After promoting, the same checks are run again on production.

## When the API is not there

That is a supported state, not a failure.
The console loads the static simulated day, plays it, and shows every zone decision in words.
The configuration workspace shows an explicit offline state, says that changes are held in the session only, and keeps working.
`software/tests/test_page.py` asserts that path, and it was walked in a browser against a plain static server with no API present.
