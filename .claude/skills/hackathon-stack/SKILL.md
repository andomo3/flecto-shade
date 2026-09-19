---
name: hackathon-stack
description: Choose and set up a hackathon tech stack, deploy it, and pick its APIs using the HackMIT playbook - the stack decision tree by project type, backend and database and auth questions, the $0 deployment options, the "if you already know X" shortcuts, the team size paths, the emergency fallback stacks, the platform quickstarts for Vercel, Railway, Render, Firebase, and Supabase, the environment variable and deployment readiness checklists, the universal and per stack boilerplate checklists, the free API selection rules, rate limits, fallbacks, and the API failure modes that kill demos. Use this whenever the user asks what stack or framework to use, how or where to deploy, about environment variables, hosting, a live URL, a boilerplate or starter, which API or free tier to use, rate limits, or says "we can't deploy" or "the backend is broken", even mid hackathon. Built from the Stack Decision Tree, Deployment Mastery, Boilerplates, and Free APIs sections of the playbook.
---

# Hackathon stack

The best stack is the one the team already knows.
A hackathon is not the time to learn a framework, and deployment should never be the part that ruins the demo.
This skill walks the playbook's decision tree, sets up the boilerplate, deploys early, and picks APIs by job rather than hype.

| Need | Read |
|---|---|
| The decision tree from project type through backend, database, auth, real time, and deployment budget, the quick pick tables, the shortcuts, the budget and team size paths, the emergency fallbacks | `references/stack-decision-tree.md` |
| The platform guide and quickstarts, the deployment workflow, common failures and the debugging flow, the env var checklist, the demo day backup plan, the pre-submit verification | `references/deployment.md` |
| The starter principles, the folder patterns, the universal setup checklist, and the per stack checklists for Next.js, Flask, FastAPI, Flutter, and React Native, the env var template, the deployment readiness check | `references/boilerplates.md` |
| The API selection rules, the mega list, the combination recipes, the rate limit cheat sheet, fallbacks, the integration checklist, the seven failure modes, the cost math | `references/free-apis.md` |

## Pick the stack, ten minutes

Walk the tree honestly and write the answer down in one line.

1. **What are you building?** Web app, mobile app, CLI or backend service, or hardware, IoT, and AR.
   Hardware with sensors is Arduino plus PlatformIO plus an MQTT broker in the playbook; a Raspberry Pi project is Python plus FastAPI for the control interface.
2. **Web app questions.** Server side rendering needed, then Next.js. A backend needed and simple, then Supabase or Firebase. Team comfort with React decides Next.js against SvelteKit or Nuxt.
3. **Backend and data.** Simple CRUD or PostgreSQL via Supabase for anything with joins. Redis or Upstash for key value. Auth only if the demo needs accounts, and then Supabase Auth or Clerk. Real time only if the demo shows it.
4. **Deployment budget.** At $0: Vercel or Netlify for frontends, Railway or Fly.io for a backend that must run all the time, Render with its cold starts, GitHub Pages for static only.

Shortcuts when the tree is overkill: know React, then Next.js plus Tailwind plus Supabase plus Vercel; know Python, then FastAPI plus Supabase plus Railway; know nothing, then Next.js plus Supabase plus Vercel because the tutorial ecosystem is largest.
Four or more people: define the API contracts in the first hour, no guessing.

## Set up the boilerplate, first two hours

Before writing a feature, the universal checklist: git initialised with the right `.gitignore`, a README with a title and one line, `.env.example` with every variable and no values, `.env` ignored, the folder structure, a linter, a license (MIT), collaborators added, and no direct pushes to main.
Then the per stack checklist from the boilerplates reference; the FastAPI one, for instance, wants CORS, a `/health` endpoint, pinned requirements, and error handling middleware before anything else.

Keep the folder structure shallow, the first screen useful, the data model simple, and the demo obvious.
Pick the closest starter, rename it, and cut everything outside the golden path.

## Deploy early

Push to GitHub, connect the deploy service, set the environment variables, configure auth callbacks, test the core flow, save the live URL, keep a backup deployment.
Do this at hour three, before the app does anything interesting, because a working live link reduces risk more than almost anything else.

When a deploy fails, follow the playbook's tree: build error, then read the logs; runtime error, then check env vars and API calls; otherwise auth callbacks and routes.
The failures that recur: missing env vars, wrong redirect URLs, CORS, database connection strings, incompatible dependencies, secrets leaking into the client, local only paths.

Before submitting, the readiness check: every variable set in production, no secrets in client code, HTTPS, proper error pages, a health check returning 200, favicon and title set, the README carrying the live link, and the live URL loading in incognito with no console errors on the golden path.

## Pick APIs by job

Use the simplest API that solves the core problem, prefer one strong API over three weak ones, never add one to look advanced, check the free tier before the event, and keep a fallback.
Start with one API, save its output, show the result immediately, add a second layer only if it strengthens the demo.

Before relying on any API, check the rate limit sheet in the free APIs reference.
Twenty demos need twenty times a single call's quota, and metered model APIs burn a small credit fast, so use a cheaper model and cap tokens.
For every live call in the golden path keep a cached fixture, because the seven failure modes, the silent timeout, the rate limit surprise, the env var ghost, CORS, key exposure, the data shape mismatch, and the free tier cliff, are all survivable with a mocked fallback and fatal without one.

Two hours before presenting, run the API integration checklist: real endpoints work, production env vars set, rate limits safe for a five minute demo, errors handled, loading states exist, no keys in the frontend, fallback data ready, responses under three seconds, CORS right, tested on a different network.

## Emergencies

- Behind and need to ship something: Next.js plus Supabase plus Vercel, a template, a CRUD app in thirty minutes.
- Backend broken and unfixable: Supabase for everything.
- Cannot deploy: Replit or CodeSandbox.
- No time for UI: v0 for components, shadcn/ui to paste.

The API is plumbing, not the product.
Boring, reliable, and well understood beats cutting edge every time.
