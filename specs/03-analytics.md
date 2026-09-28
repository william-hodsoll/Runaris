# Spec: Analytics (PostHog + Sentry)

## Requirement
Per `intent.md`: analytics on by default, opt-out in settings, first-run privacy notice. Usage/perf events only — never book/library content. Single `analytics.ts` adapter; no direct SDK calls elsewhere (`CLAUDE.md` "Never").

In scope: adapter with a closed event catalog (no free-text event payloads), opt-out flag persisted alongside the library, first-run notice, PostHog init (usage events), Sentry init (errors + perf). Both SDKs are optional at runtime — if no project key is configured (e.g. local dev), the adapter no-ops instead of throwing, so the app works with zero analytics config.

Out of scope: an actual PostHog/Sentry project (needs real keys, supplied via env vars later, not generated here); a full settings screen (stub toggle only).

## Design
- `analytics.ts` exports `trackEvent(name: AnalyticsEvent, props?: Record<string, number | boolean>)` and `initAnalytics()`. `AnalyticsEvent` is a closed string-literal union (e.g. `'book_added'`, `'connect_mode_entered'`, `'demo_loaded'`) — no caller can pass a title/author/note as a value; `props` values are restricted to number/boolean, so a string leak isn't type-checkable.
- Opt-out stored in `localStorage` under `runaris.analyticsOptOut`, read once at init; toggling it live calls PostHog's opt-out API and stops future Sentry breadcrumbs from user actions.
- First-run notice: shown once (tracked via a separate `runaris.hasSeenPrivacyNotice` flag), dismissible, links to the opt-out toggle.
- PostHog and Sentry are loaded only if `VITE_POSTHOG_KEY` / `VITE_SENTRY_DSN` env vars are set; otherwise `initAnalytics()` is a no-op and `trackEvent` calls are swallowed silently (logged to console in dev only).

## Test plan
1. `trackEvent` with analytics uninitialized (no keys) does not throw
2. Opt-out flag blocks `trackEvent` from calling the underlying SDK (mock PostHog/Sentry, assert not called)
3. First-run notice shows once, not on subsequent loads, and dismissing persists the flag
4. Type-level check: attempting to pass a string library-content-shaped prop fails to compile (documented, not a runtime test)

## Rollback
Adapter is additive — no existing feature depends on it. Disabling is a one-line env var removal; no data migration involved.
