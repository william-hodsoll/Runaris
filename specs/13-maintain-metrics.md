# Spec: Maintain-stage metrics wiring

## Requirement
First entry into the playbook's Maintain stage — until now every stage has been Build+Test+Deploy in isolation. intent.md's success-metrics table has four runtime metrics with no signal wired up at all: render fps, ISBN success rate, import round-trip, crash-free sessions. This spec wires each to the existing `analytics.ts` adapter (no new dependency, no new call sites outside it — CLAUDE.md's analytics rules still apply).

Out of scope: an actual PostHog/Sentry dashboard or alert that turns a breach into a new intent.md entry automatically — that's a one-time manual setup in each tool's UI (documented as a checklist item below, same treatment spec 10 gave GitHub Pages' manual step), not something this repo's code can do.

## Design
- **Crash-free sessions**: `@sentry/browser` alone doesn't catch React render errors (that needs the separate `@sentry/react` integration, which isn't installed and isn't warranted for this). Add a small `ErrorBoundary` component wrapping `<App>`'s tree in `main.tsx`: on catch, calls `captureError(error)` and `trackEvent('app_crashed')`, and renders a minimal "Something went wrong — reload" fallback instead of a blank white screen. This is the metric's only real signal source, and it also stops a render error from being a silent full crash.
- **ISBN lookup success rate**: `AddByIsbn.tsx` already has three outcomes (found / not found / request failed) with no tracking. Add `trackEvent('isbn_lookup_succeeded' | 'isbn_lookup_not_found' | 'isbn_lookup_failed')` at each branch. New entries in `AnalyticsEvent`.
- **Import round-trip**: `import_completed` already fires but only carries the added-book count. `ImportResult` already separates `books` from `flagged` (never silently drops a row, per CLAUDE.md) — just add `flagged: result.flagged.length` to the existing event's props so "100% mapped or flagged" is verifiable from event data instead of assumed from code review.
- **Render fps**: `CanvasHost`'s frame loop already computes `dt` every frame. Track a rolling average and fire `trackEvent('render_fps_sampled', { fps })` once every ~10s (not every frame — that would spam the event stream) rather than adding a new perf-monitoring layer.

## Test plan
- Unit: `ErrorBoundary` renders its fallback and calls the injected error handler when a child throws (React Testing Library not currently a dependency — test via `renderToStaticMarkup`-free manual render is overkill; cover it with the browser smoke test instead, consistent with how CanvasHost's own render loop has no unit test either).
- Typecheck clean, existing `vitest run` still passing, `npm run build` succeeds.
- Browser smoke test: a forced throw inside the tree renders the fallback (not a blank page) and calls the mocked error handler; ISBN lookup (success/not-found paths, both reachable without a live network call is hard — cover the not-found path against the real OpenLibrary API in the smoke test since it's already network-reachable in this environment) fires the right event; import fires `import_completed` with a `flagged` prop.

## Rollback
Purely additive: a new component (ErrorBoundary), three new closed-union event names, and two new props on an existing event. Reverting the commit removes the extra signal with no data-model or persistence impact.

## Manual checklist (not automatable from this repo)
- [ ] Set `VITE_POSTHOG_KEY` / `VITE_SENTRY_DSN` as GitHub Actions secrets (deploy.yml already reads them; unset today, so analytics currently no-ops on the deployed build)
- [ ] In Sentry: alert when session crash-free rate drops below 99% (intent.md breach trigger)
- [ ] In PostHog: dashboard/insight for `isbn_lookup_*` success rate below 75%, and `render_fps_sampled` median below 30
- [ ] A metric breach found this way gets a new intent.md entry per CLAUDE.md workflow rule 5 — not a quiet code fix
