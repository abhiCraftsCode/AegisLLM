# AegisLLM Dashboard

Production V1 frontend for **AegisLLM** — an LLM security gateway. Built with React, TypeScript, Vite, React Router, and Tailwind CSS, wired directly against the FastAPI backend contract in `allroutes.txt` / `allschemas.txt`.

## Getting started

This sandbox has no network access, so dependencies could not be installed or the build verified here. On your machine:

```bash
npm install
cp .env.example .env   # then fill in VITE_API_BASE_URL (and OAuth client IDs if you use them)
npm run dev
```

```bash
npm run build   # production build (tsc -b && vite build)
```

## Environment variables

| Variable | Purpose |
|---|---|
| `VITE_API_BASE_URL` | Base URL of the FastAPI backend (no trailing slash). |
| `VITE_GOOGLE_CLIENT_ID` / `VITE_GITHUB_CLIENT_ID` | OAuth client IDs for the two providers the backend supports (`OAuthProvider.GOOGLE` / `.GITHUB`). Leave blank to disable that button — it renders disabled rather than faking a login. |
| `VITE_OAUTH_REDIRECT_URI` | Must exactly match the redirect URI registered with each provider, e.g. `https://your-domain/oauth/callback`. |

## Two things worth knowing before you deploy

1. **OAuth exchange.** The frontend performs the authorization-code redirect for Google/GitHub and lands on `/oauth/callback`, which posts `{ provider, code }` to `POST /auth/oauth`. It does not know your registered redirect URI or client IDs — set those via the env vars above so they match what's registered with each provider and what your backend expects when exchanging the code.

2. **Inspector authentication.** `POST /chat/inspections` authenticates via `get_current_api_key` (a hashed API key secret), not the dashboard session JWT used everywhere else. Since a key's raw secret is only ever shown once at creation and is never retrievable afterward, the Inspector page asks the user to paste an API key secret into a dedicated field to authenticate each test call. That secret is kept only in component state for the session — never persisted, never sent anywhere except that one request.

## What's intentionally not built

Per the product spec: no notification center, no fake data anywhere, no Inspector history/LLM-config panel, no audit-log filtering beyond pagination, no key reactivation, no command palette, no billing/teams/workspaces. See the spec document for the full list.

## Structure

Feature-oriented under `src/features/*` (API modules + feature components), shared UI in `src/components/{ui,common,layout,auth}`, routed pages in `src/pages`, app wiring in `src/app` (providers, router, route guards).
