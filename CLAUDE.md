# Runaris: Claude Context

A "cosmos" visualization of a personal book library: books as stars, subjects as constellations, auto-connected by shared subject/genre/author. Rebuild of existing `neural_mind.py` (vanilla JS/Canvas2D) onto React + TypeScript + Vite. See `intent.md` for scope, baseline feature list, and metrics; `docs/sdlc-playbook.md` for process.

**Source of truth for behavior:** `neural_mind.py` (the shipped v1). When in doubt about what a feature should do, that file is the spec — the rebuild ports its behavior, it does not redesign it, except where `intent.md`'s decisions log says otherwise (analytics, stack).

## Commands
- Install: `npm install`
- Dev: `npm run dev`
- Test: `npm test`
- Lint / typecheck: `npm run lint && npm run typecheck`
- Build: `npm run build`
[TBD: confirm once package.json scripts exist — these are the planned names]

## Architecture
- Data model (ports v1's STARS/CENTRES/EDGES):
  - `BookStar`: id, title, author, year?, genre?, subjects[], pages?, isbn?, coverUrl?, status?, dateAdded, position {x,y,z}, offset {ox,oy,oz} from its constellation centre, constellationId, size (derived from pages), color
  - `Constellation`: id, subject, position {x,y,z}, color, rotation axis {ax,ay,az}, spinSpeed, spinPhase
  - Connections are **derived, not stored as user data**: recompute from shared subject/genre/author whenever the library changes (matches v1's `computeConnections`); a sparse "synapse" subset (nearest neighbors per constellation) is precomputed for the always-visible web
- Separate layers: model (pure — placement math, connection derivation, no rendering) / render (Canvas2D projection + draw loop) / persistence / external lookup (ISBN/OpenLibrary) / import (CSV/Goodreads)
- Frontend: TypeScript + React + Vite
- Canvas: Canvas2D, custom 3D-to-2D projection carried over from v1 (`project()`, camera rotation, breathing/gravity animation) — this is not a graph-layout library use case; the render loop reads from refs/a non-React store, not React state, to hold 60fps
- State: Zustand (or similar) for UI/app state; render loop bypasses React reconciliation entirely
- Persistence: pick IndexedDB vs. localStorage in the Design spec for this feature (v1 used localStorage under key `neuralMind.v1`); JSON export unchanged
- External lookup: OpenLibrary Search API (title/author) + Books API (ISBN) — same endpoints as v1, isolated behind an adapter
- ISBN scan: camera barcode scan via ZXing (dynamically loaded, as in v1)
- Import: CSV/JSON importer, Goodreads column mapping — port v1's `parseCSV`/`normaliseBook` logic, keep the flag-don't-drop behavior for unmapped rows
- Analytics: PostHog for product usage/events, Sentry for crash reports + performance. On by default, opt-out in settings, first-run privacy notice. Isolated behind a single `analytics.ts` adapter — every call site goes through it, nothing calls PostHog/Sentry directly. This replaces v1's "No tracking, no backend" claim — update that copy in the About/settings tab
- Login/Social: keep as visual-only stubs, same as v1 (no backend calls, no real auth) — carry forward the "visual shells" disclosure text
- PWA: manifest + service worker + icon, same installability goal as v1, but generated via Vite's PWA plugin instead of hand-rolled files
- Packaging (post-MVP): Tauri for desktop, Capacitor for mobile, same web codebase

## Conventions
- Model logic (placement, connection derivation, import parsing) is pure and unit-tested; UI/render never mutates model directly
- Every schema change bumps a version and ships a migration
- One feature = one branch = one spec in `specs/`
- Small diffs; no unrelated refactors
- Port, don't redesign: when porting a v1 feature, match its behavior first; propose changes as a separate decision, not silently during the port

## Workflow (mandatory)
1. Start from `intent.md`; write `specs/<feature>.md` (requirements + design) before code
2. Plan mode first for anything touching >3 files
3. Tests + evals pass before commit
4. Agent review, then human review for: data model, persistence, security
5. Breached metric -> new intent entry, not a quiet fix
6. Every scope, architecture, or process decision (made by the user, or by Claude and confirmed) is appended to the Decisions log in `intent.md` in the same turn it's made — no separate ask, no batching for later

## Known pitfalls
- [TBD: add each recurring agent mistake here as it happens]
- v1's render loop depends on live/mutable arrays (STARS/CENTRES/EDGES) read every frame outside React state — don't route this through React state/props or perf will regress
- A misnamed GitHub Actions secret reference (`${{ secrets.TYPO_NAME }}`) silently resolves to an empty string — no error, no warning, build succeeds with blank env vars. When a deployed feature that depends on a secret doesn't work despite the workflow being green, verify the secret NAME character-by-character on the repo's Settings → Secrets and variables → Actions page before assuming a code bug (bit us with `VITTE_SUPABASE_*` vs `VITE_SUPABASE_*`)
- CI's `node-version:` in a workflow file must track the strictest `engines.node` of any devDependency (check `node_modules/<pkg>/package.json`), not just whatever runs locally. jsdom 30 requires Node ^22.22/^24.15/>=26; CI was pinned to Node 20, so every single CI run failed on `npm test` from the very first commit — invisible locally because the sandbox already runs Node 22. A red "CI" check next to an otherwise-fine deploy is a version-pin mismatch to check before assuming a code/test bug. `app/package.json` now declares `engines.node` as a tripwire

## Specs
- Template: `specs/_template.md`
- One spec per feature branch, written and approved before code
- `specs/01-core-loop.md` is stale (pre-dates the pivot to rebuilding around v1) — do not build from it; superseded, pending a new spec for the React/Vite port

## Never
- Commit secrets or `.env`
- Push to `main` directly
- Change save-file format without migration + round-trip test
- Send book/author/note/tag content, or any library data, through the analytics adapter — usage events carry event names and counts only, never user content
- Call PostHog/Sentry directly outside `analytics.ts`
- Silently change v1's visual metaphor (star field/constellations) or its auto-connection logic during the port — that's a product decision, not a refactor
