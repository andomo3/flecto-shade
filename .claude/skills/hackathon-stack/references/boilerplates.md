<!-- Extracted from `HackMit ;p.md` lines 5953 to 6515 by scripts/extract_playbook.py. Edit the playbook, not this file. -->

# Boilerplate

# 16. Boilerplates

Boilerplates reduce friction. They help teams start from structure instead of chaos.

## Working starters (verified Sept 2026)

- `nextjs-supabase/` — Next.js + Supabase auth, layout, deploy configs
- `flask-firebase/` — Flask + Firebase, minimal templates
- `fastapi-supabase/` — FastAPI + CORS + `/healthz` + fixture mode (`?demo=1`)

> The folder patterns below are starting sketches, not finished apps. Pick the closest working starter above, rename it, cut everything outside the golden-path demo.

## What this section includes (patterns)

- AI SaaS
- Dashboard
- Chat app
- Marketplace
- RAG app
- AI assistant
- College platform
- Resume analyzer
- Portfolio
- Auth starter

## Starter principles

- keep folder structure shallow,
- keep the first screen useful,
- keep the data model simple,
- keep deployment easy,
- and keep the demo obvious.

## Boilerplate folder patterns

### AI SaaS

ai-saas/

├── app/

├── components/

├── lib/

├── prompts/

├── public/

└── README.md

### Dashboard

dashboard/

├── app/

├── components/

├── data/

├── charts/

└── README.md

### Chat app

chat-app/

├── app/

├── components/

├── lib/

├── realtime/

└── README.md

### Marketplace

marketplace/

├── app/

├── components/

├── listings/

├── payments/

└── README.md

### RAG app

rag-app/

├── app/

├── components/

├── embeddings/

├── retrieval/

└── README.md

### AI assistant

ai-assistant/

├── app/

├── components/

├── agents/

├── memory/

└── README.md

### College platform

college-platform/

├── app/

├── components/

├── auth/

├── submissions/

└── README.md

### Resume analyzer

resume-analyzer/

├── app/

├── components/

├── parsing/

├── scoring/

└── README.md

### Portfolio

portfolio/

├── app/

├── components/

├── content/

└── README.md

### Auth starter

auth-starter/

├── app/

├── components/

├── auth/

└── README.md

## How to use boilerplates

1. Pick the closest starter.
2. Rename it to match the problem.
3. Remove features that do not help the demo.
4. Ship the core workflow first.
5. Add polish only after the workflow works.

# Boilerplate Checklist

Use this when setting up your project in the first 2 hours. Pick your stack from below, then check off every item before writing a single feature.

---

## Universal Setup Checklist

These apply to every stack regardless of framework.

1. Git repo initialized with `.gitignore` (Node, Python, or platform-appropriate)
2. `README.md` created with project title and one-line description
3. `.env.example` file created with all required variables (no real keys)
4. `.env` added to `.gitignore`
5. Folder structure created (see stack-specific sections below)
6. Linter/formatter configured (ESLint, Prettier, Ruff, etc.)
7. Pre-commit hook installed (optional but saves headaches)
8. License file added (MIT is the hackathon default)
9. Team members added as collaborators on the repo
10. Branch protection: no direct pushes to `main`

---

## Next.js / React Stack

### Minimum Viable Boilerplate

npx create-next-app@latest my-app --typescript --tailwind --app

### Folder Structure

my-app/

├── src/

│   ├── app/            # Pages and routes

│   │   ├── layout.tsx  # Root layout

│   │   ├── page.tsx    # Home page

│   │   └── api/        # API routes

│   ├── components/     # Reusable UI components

│   │   ├── ui/         # Button, Input, Card, etc.

│   │   └── features/   # Feature-specific components

│   ├── lib/            # Utilities, helpers, config

│   │   ├── utils.ts

│   │   └── api.ts

│   ├── hooks/          # Custom React hooks

│   ├── types/          # TypeScript type definitions

│   └── styles/         # Global styles (if not using Tailwind)

├── public/             # Static assets (images, icons)

├── prisma/             # Database schema (if using Prisma)

├── .env.example

├── .gitignore

├── next.config.js

├── tailwind.config.ts

├── tsconfig.json

└── package.json

### Checklist

 1. `create-next-app` with TypeScript and Tailwind
 2. `components/ui/` folder with at least: Button, Input, Card, Modal
 3. `lib/api.ts` with fetch wrapper and base URL config
 4. `lib/utils.ts` with common helpers (formatDate, classNames, etc.)
 5. `types/` folder with initial type definitions
 6. API route template in `app/api/`
 7. Tailwind config customized with your color palette
 8. `next.config.js` with image domains configured
 9. Vercel deployment configured (or Dockerfile if self-hosting)

---

## Flask / Python Stack

### Minimum Viable Boilerplate

mkdir my-app && cd my-app

python -m venv venv

source venv/bin/activate

pip install flask python-dotenv

### Folder Structure

my-app/

├── app/

│   ├── __init__.py      # App factory

│   ├── routes/          # Route handlers

│   │   ├── __init__.py

│   │   └── main.py

│   ├── models/          # Data models

│   │   └── __init__.py

│   ├── services/        # Business logic

│   │   └── __init__.py

│   ├── utils/           # Helpers

│   │   └── __init__.py

│   └── templates/       # Jinja2 templates (if server-rendered)

├── static/              # CSS, JS, images

├── tests/               # Test files

├── .env.example

├── .gitignore

├── requirements.txt

├── run.py               # Entry point

└── README.md

### Checklist

 1. Virtual environment created and activated
 2. `requirements.txt` with all dependencies
 3. App factory pattern in `__init__.py`
 4. Blueprint structure for routes
 5. `run.py` with `if __name__ == "__main__"` guard
 6. CORS configured (if API serves a separate frontend)
 7. Error handlers for 404, 500
 8. `static/` folder with favicon and placeholder CSS
 9. `.env.example` with all required environment variables
10. Gunicorn in `requirements.txt` for production deployment

---

## FastAPI / Python Stack

### Minimum Viable Boilerplate

mkdir my-app && cd my-app

python -m venv venv

source venv/bin/activate

pip install fastapi uvicorn python-dotenv pydantic

### Folder Structure

my-app/

├── app/

│   ├── __init__.py

│   ├── main.py          # FastAPI app instance

│   ├── routes/          # Route handlers

│   │   └── v1/          # Versioned routes

│   │       └── endpoints.py

│   ├── models/          # Pydantic models

│   │   └── schemas.py

│   ├── services/        # Business logic

│   ├── core/            # Config, security, dependencies

│   │   ├── config.py

│   │   └── deps.py

│   └── utils/

├── tests/

├── alembic/             # Database migrations (if using SQL)

├── .env.example

├── .gitignore

├── requirements.txt

├── Dockerfile

└── README.md

### Checklist

 1. FastAPI app created in `main.py`
 2. Pydantic models for request/response in `models/schemas.py`
 3. CORS middleware configured
 4. Health check endpoint at `/health`
 5. API versioning structure (v1, v2, etc.)
 6. Error handling middleware
 7. `Dockerfile` with multi-stage build
 8. `requirements.txt` pinned versions
 9. OpenAPI docs accessible at `/docs`
10. Uvicorn configured for production (workers, host, port)

---

## Flutter / Dart Stack

### Minimum Viable Boilerplate

flutter create my_app

cd my_app

### Folder Structure

my_app/

├── lib/

│   ├── main.dart

│   ├── app.dart            # App widget and routing

│   ├── screens/            # Page-level widgets

│   │   └── home_screen.dart

│   ├── widgets/            # Reusable widgets

│   │   └── custom_button.dart

│   ├── models/             # Data models

│   ├── services/           # API calls, storage

│   ├── providers/          # State management

│   ├── utils/              # Helpers, constants

│   └── theme/              # Colors, typography

├── assets/                 # Images, fonts, JSON

├── android/

├── ios/

├── test/

├── pubspec.yaml

└── README.md

### Checklist

 1. Project created with `flutter create`
 2. `pubspec.yaml` with all dependencies (http, provider/bloc, etc.)
 3. State management setup (Provider, Riverpod, or Bloc)
 4. `screens/` folder with at least a home screen
 5. `widgets/` folder with reusable components
 6. `models/` folder with data classes
 7. `services/` folder with API client
 8. Theme defined in `theme/` (colors, text styles)
 9. Assets folder configured in `pubspec.yaml`
10. Android and iOS builds tested

---

## React Native / Expo Stack

### Minimum Viable Boilerplate

npx create-expo-app my-app --template blank-typescript

### Checklist

 1. Expo project with TypeScript
 2. Navigation setup (React Navigation)
 3. `src/screens/` with at least home and detail screens
 4. `src/components/` with reusable UI elements
 5. `src/services/` with API client
 6. `src/context/` or state management (Zustand, Redux)
 7. `app.json` configured (name, icon, splash screen)
 8. Tested on both iOS simulator and Android emulator

---

## Environment Variable Checklist

Every project needs these documented. Add to your `.env.example`:

### Universal Variables

# App

APP_ENV=development

APP_PORT=3000

APP_URL=<http://localhost:3000>

# Database

DATABASE_URL=your_database_url_here

# Auth

JWT_SECRET=your_jwt_secret_here

NEXTAUTH_SECRET=your_nextauth_secret_here

# External APIs

OPENAI_API_KEY=your_openai_key_here

### Platform-Specific Additions

| Platform | Additional Variables |
| :---- | :---- |
| **Vercel** | `VERCEL_URL`, `VERCEL_ENV` |
| **AWS** | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` |
| **Firebase** | `FIREBASE_API_KEY`, `FIREBASE_AUTH_DOMAIN`, `FIREBASE_PROJECT_ID` |
| **Stripe** | `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET` |
| **Supabase** | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` |

---

## Deployment Readiness Check

Run this before submitting. Every box must be checked.

 1. All environment variables are set in production
 2. No secrets in client-side code (check with `grep -r "sk_" src/` and similar)
 3. Database is accessible from production server
 4. CORS is configured for production domain only
 5. HTTPS is enabled
 6. Error pages return proper status codes (not blank 500s)
 7. Static assets are served from CDN or optimized
 8. API rate limiting is in place (even basic)
 9. App loads in under 3 seconds on 3G
10. No console.log statements with sensitive data
11. Health check endpoint returns 200 OK
12. Database migrations are applied
13. Favicon and title are set (not default)
14. README has live demo link
