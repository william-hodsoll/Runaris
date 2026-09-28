# Spec: Deploy stage (CI + GitHub Pages)

## Requirement
Move from local-only build+test to the playbook's Deploy stage: every push/PR runs the same gate this session has been running by hand (typecheck, unit tests, build), and `main` auto-deploys to GitHub Pages. Repo: `william-hodsoll/Runaris`.

In scope: `.github/workflows/ci.yml` (typecheck + test + build, on push and PR), `.github/workflows/deploy.yml` (build + publish `app/dist` to GitHub Pages on push to `main`). Repo root holds `intent.md`, `CLAUDE.md`, `docs/`, `specs/`, `reference/`, and the Vite project under `app/`.

Out of scope: a PR-review bot/hook gate (CLAUDE.md's "Agent review, then human review for data model/persistence/security" stays a human process for now, not automated here); custom domain; Vercel/Netlify (Pages was the chosen target).

## Design
- CI runs `npm ci && npm run typecheck && npm test && npm run build` with `working-directory: app` (project lives in a subfolder, not repo root).
- Deploy job depends on CI passing, builds again (or reuses the CI build artifact — reuse is simpler, one build not two), uploads `app/dist` via `actions/upload-pages-artifact`, publishes via `actions/deploy-pages`.
- `vite.config.ts`'s `base: './'` already produces subpath-relative asset URLs, so no change needed for GitHub Pages serving from `/Runaris/` — confirmed by the same reasoning that made it work for artifact publishing (spec 02's preview).
- One manual, one-time step outside this repo's code: the repo owner enables Pages with source "GitHub Actions" in repo Settings → Pages. Not automatable from here without repo-admin API scope; documented as a checklist item, not skipped silently.

## Test plan
1. CI workflow YAML is valid (actionlint or GitHub's own syntax check on push)
2. A push with a failing test fails the CI job (verified by intentionally breaking a test once, then reverting — or trusting the existing local gate, since the steps are identical to what's already been run locally)
3. First successful deploy: the Pages URL serves the app and the demo library loads (manual check once Pages is live)

## Rollback
Both workflows are additive to the repo; deleting them returns to local-only build with no code impact. A bad deploy is fixed by pushing a revert to `main` — Pages always serves the latest successful deploy.
