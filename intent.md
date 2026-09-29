# Intent: Runaris

**Status:** Rebuild — target defined against existing v1 (`neural_mind.py`)

## What
A "cosmos" of your personal book library: each book is a star, each subject is a constellation, positioned on a sphere and rendered as an interactive pseudo-3D scene (drag to rotate, scroll to zoom, tap a star to inspect). Not a generic mind map — the shape is fixed (star field / constellations), not freeform nodes-and-edges.

## Why
Existing library apps (Goodreads, StoryGraph, LibraryThing) show your books as a flat grid or list — sortable, filterable, but impersonal. They ignore the reader: why a book mattered, how it connects to others you've read, the shape of your own reading life. Runaris makes the map itself the personal artifact.

## Users
General consumers who track a personal book library and want to see it, not just list it.

## Baseline: what v1 (`neural_mind.py`) already does
Single Python script generates a self-contained HTML/PWA (vanilla JS, HTML5 Canvas2D, no framework, no build step). Confirmed working features to preserve in the rebuild:
- Book = star; primary subject = constellation centre; stars are positioned in a fuzzy ball around their constellation's centre on a sphere (Fibonacci lattice + shuffled radius so clusters don't correlate with input order)
- Star size scales with page count; each constellation has independent slow rotation (own axis + speed)
- Connections are **auto-computed**, not user-drawn: two books link if they share a subject, genre, or author. Within a constellation, a sparse "synapse" web (nearest 1-2 neighbors) is always faint-visible; the full shared-attribute graph is used for a "connect mode" that lights up everything related to a selected star
- Add a book: manual form, ISBN barcode scan (camera, via ZXing) + OpenLibrary lookup, or CSV/JSON import (own format + Goodreads-shaped columns)
- Cover art fetched from OpenLibrary by title/author or ISBN
- Timelapse: scrub/play through `dateAdded` to watch the cosmos form over time
- Insights view, library list view, search, status filter (reading status)
- Customize: palette; Export library (JSON)
- Settings tabs: profile, app, library, social, about
- Login and Social are **visual-only stubs** — no backend, do not actually authenticate or connect (kept as stubs in this rebuild too)
- Persistence: `localStorage` (key `neuralMind.v1`), no backend
- Ships as an installable PWA: manifest, hand-rolled service worker (cache-first for app shell, network-through for cover/OpenLibrary calls), SVG icon
- Explicit in-app claim (About tab): "No tracking, no backend" — **superseded by this rebuild's analytics decision below**

## MVP scope for the rebuild (in)
- Reimplement the full v1 feature set above on React + TypeScript + Vite
- Keep the star/constellation model and auto-computed connections (subject/genre/author) as-is — do not switch to user-drawn typed links
- Keep manual entry, ISBN scan + OpenLibrary lookup, CSV/Goodreads import, cover art, timelapse, insights, search/filter, customize/palette, export
- Keep Login/Social as visual stubs (no real backend/auth yet)
- Replace hand-rolled localStorage persistence with a versioned model + migration path (still local storage under the hood for v1, e.g. IndexedDB or localStorage — pick in Design)
- Add analytics (PostHog usage events + Sentry crash/perf) — remove or rewrite the "No tracking, no backend" claim in the About tab to reflect this
- Keep PWA installability (manifest, service worker, icon) — re-implement via Vite's PWA tooling rather than hand-rolled

## Out of scope (still)
- Real social features (Login stays a stub; Social panel stays a stub — accounts are now in scope for sync/billing, see below, but friend/social features are not)
- Real-time collaboration
- Changing the core visual metaphor (star field) to a freeform mind map

## Post-MVP: Commercial launch gaps (2026-09-28 gap analysis)
The rebuild is feature-complete against v1 and deployed, but not commercially shippable. Gaps, ranked by blocker severity:

**Engineering**
1. No accounts / no cross-device sync — library lives in one browser's IndexedDB only; reinstall or cleared storage loses it except via manual JSON export. Gates most items below.
2. No real backend — Login/Social are intentional stubs (see Out of scope); unshippable as-is, just a demo affordance
3. No privacy policy, ToS, or consent flow — required before PostHog/Sentry can legally collect from real users, and before app store listing
4. Analytics dashboards/alerts not configured — spec 13 wired the events, nobody's watching them yet (manual checklist, spec 13)
5. PWA offline/update-flow not verified under real offline use
6. No caching/rate-limit handling for OpenLibrary — a traffic spike risks third-party throttling with no fallback
7. No accessibility pass — canvas-only UI, minimal keyboard nav, no screen-reader path

**Marketing**
1. No validated positioning/messaging — concept only, no landing page or waitlist signal
2. No monetization model decided — blocks whether accounts/sync is "nice to have" or load-bearing
3. No onboarding funnel — no one-click Goodreads-style import hook for acquisition
4. No app store presence — PWA-only, Tauri/Capacitor deferred, limits discoverability
5. No brand assets (logo, screenshots, store copy) or competitive teardown vs. Goodreads/StoryGraph/LibraryThing

**Decided 2026-09-28:** Backend/auth stack — **Supabase** (Postgres + auth + storage). Monetization — **freemium**: local-only (today's app) stays free forever; a paid tier unlocks cross-device cloud sync, accounts, and unlimited books. This moves "real backend auth" and "cloud sync" from Out of scope (above) into scope, gated by tier.

## Constraints
- Platform: Web app first (PWA); desktop (Tauri) and mobile (Capacitor) wrap the same codebase later — one engine, three shells
- Stack: TypeScript + React + Vite (migrated from v1's vanilla JS). Canvas2D custom renderer carries over — this is a 3D-projected star field, not a graph-layout library (Konva/React Flow don't fit); render loop and camera/projection math port from v1 largely as-is, wrapped in React for state/UI chrome only. State via Zustand, kept out of the render loop (render loop reads refs, not React state, to hit 60fps)
- External data: OpenLibrary Search API + Books API (ISBN), both key-less — same as v1
- Data: Local-only for library content (no change from v1's local-only model); pick IndexedDB vs. localStorage in the Design spec — IndexedDB better fits larger libraries and cover-image caching
- Privacy: Analytics on by default, opt-out in settings, visible privacy notice on first run. Tracks product usage (feature/flow events, session counts) and performance/crash data — never book titles, authors, notes, or map content. Library data itself stays local-only, unaffected by analytics.
- Analytics stack: PostHog (product usage/events) + Sentry (crash reports, performance) — both third-party, both support scrubbing PII before send
- Backend (2026-09-28): Supabase — Postgres for accounts/library sync, Supabase Auth for login, Supabase Storage for cover-image caching (post-MVP, not this spec). Free tier stays fully local/IndexedDB, unaffected; sync is additive, not a replacement — local-only must keep working with zero backend calls
- Monetization (2026-09-28): freemium — free tier is local-only (current app, unchanged); paid tier gates cross-device sync/accounts/unlimited books. Billing/Stripe integration is separate scope from the auth+sync foundation (spec 14 below covers auth+sync only, not billing)

## Success metrics (control bands)
| Metric | Target | Breach trigger |
|---|---|---|
| Feature parity vs. v1 | 100% of listed v1 features working | any dropped silently |
| Render at library size in v1 demo (232 books) | 60 fps | < 30 fps |
| ISBN scan + lookup success rate | > 90% of valid ISBNs | < 75% |
| CSV/Goodreads import round-trip | 100% of rows mapped or flagged | any silent drop |
| Crash-free sessions | 99.5% | < 99% |
| Save/load round-trip fidelity | 100% | any loss |
| Analytics event content check | 0 events carrying book/library content | any 1 event |

## Decisions log
| Date | Decision | Reason |
|---|---|---|
| 2026-09-27 | Adopt AI-native SDLC playbook | Agent-written code; humans govern |
| 2026-09-27 | Pivot from generic mind-mapping to a personal book-library map | Differentiate from grid-based library apps (Goodreads, StoryGraph, LibraryThing) by making the map itself the personal artifact |
| 2026-09-27 | Add analytics (PostHog + Sentry), on by default with opt-out | Product usage + crash/perf visibility; scoped to never touch book/library content |
| 2026-09-27 | First spec written: `specs/01-core-loop.md` (manual entry + linking + canvas) | Covers MVP build-order item 1; gates start of Build stage — **superseded, see next entries** |
| 2026-09-27 | Design the rebuild directly around the existing `neural_mind.py` v1, not a fresh generic mind map | User has a working version; playbook applies to hardening/scaling it, not reinventing the concept |
| 2026-09-27 | Rebuild's connection model is auto-computed (shared subject/genre/author), matching v1 — user-drawn typed links from the earlier spec are dropped | v1 already implements and ships this; changing it would be a product regression, not a rebuild |
| 2026-09-27 | Analytics decision confirmed over v1's own "No tracking, no backend" claim; that UI copy will be rewritten | User chose to keep analytics despite the conflict |
| 2026-09-27 | Stack migrates from v1's vanilla JS/HTML5 Canvas to React + TypeScript + Vite | User's explicit choice; render loop/projection math ports over, wrapped for state/UI |
| 2026-09-27 | Login/Social remain non-functional visual stubs in the rebuild | No backend auth work scoped yet; revisit after core rebuild is hardened |
| 2026-09-27 | Second spec written: `specs/02-react-vite-port.md` — foundation port (model, canvas render, core interactions, localStorage parity) before layering analytics/import/scan/etc. | Verify the hardest part (render loop performance/parity) before building features on top of it |
| 2026-09-27 | Spec 02 built and verified: model layer (13 unit tests passing), Canvas2D render/camera/pick ported, Zustand store, localStorage persistence, empty-state + demo-load flow. Typecheck, production build, and a headless browser smoke test (load demo, tap stars, enter/exit connect mode) all pass with no app errors. | Closes the Build+Test stages for the foundation spec; ISBN scan, CSV import, analytics wiring, timelapse, insights, settings are still stubs/unbuilt, scoped to later specs |
| 2026-09-27 | Wrote specs 03-05: analytics adapter, ISBN lookup (text entry, camera scan deferred), CSV/JSON import | Next build-order slice after the foundation port |
| 2026-09-27 | Camera barcode scanning (ZXing) deferred out of spec 04; text-based ISBN entry ships first | Unblocks the OpenLibrary lookup path without a device-testing pass for camera permissions |
| 2026-09-27 | Specs 03-05 built and verified: analytics adapter (closed event catalog, opt-out, first-run notice), ISBN lookup via OpenLibrary (text entry), CSV/JSON import (Goodreads column mapping, flag-don't-drop). 34 unit tests passing, typecheck clean, production build succeeds, browser smoke test confirms all three new UI flows (ISBN dialog, import dialog, export) open and close without errors. | Closes Build+Test for the second slice of MVP scope; camera scan, timelapse, insights, settings, IndexedDB migration remain unbuilt |
| 2026-09-27 | Wrote specs 06-09: IndexedDB migration, timelapse, insights+settings, camera scan | Closes the remaining v1 baseline feature gap |
| 2026-09-27 | Camera scan (spec 09) uses the native BarcodeDetector API instead of porting v1's ZXing dependency, with a text-entry fallback where unsupported | Smaller bundle, no new dependency, native API covers the same case on supporting browsers |
| 2026-09-27 | Specs 06-09 built and verified: IndexedDB persistence with automatic one-way migration from v1's localStorage key, timelapse scrubbing, insights stats + settings modal (Library/Insights/App/Profile/Social/About tabs, Profile+Social disclosed as stubs), camera barcode scan with graceful unsupported/denied fallbacks. 54 unit tests passing, typecheck clean, production build succeeds, browser smoke test confirms timelapse, settings tabs, and the scan fallback path all work with zero app errors. | This closes every item in the v1 baseline feature list carried into MVP scope |
| 2026-09-28 | v1's Customize/palette panel (personalization: reading-status filter, animation/gravity/nebula controls, star palette) deferred, not built | User chose to move to the Deploy stage instead |
| 2026-09-28 | Moved to Deploy stage: wrote specs/10-deploy.md, added CI (typecheck+test+build) and GitHub Pages deploy workflows, git-initialized the repo and committed everything. Target repo: william-hodsoll/Runaris | First time this project reaches Deploy, not just Build+Test in isolation |
| 2026-09-28 | Push blocked: this session has no GitHub account linked (add_repo returned permission_denied) | User needs to connect GitHub in claude.ai Settings → Connectors before the commit can be pushed |
| 2026-09-28 | Pushed to github.com/william-hodsoll/Runaris (main, 2 commits) once GitHub access was confirmed | CI and Pages-deploy workflows are now live in the repo |
| 2026-09-28 | Deploy fixed and live at william-hodsoll.github.io/Runaris | Root cause: repo Settings → Pages → Source was never set to "GitHub Actions", so `actions/deploy-pages` 404'd creating the deployment even though CI/build succeeded; fixed by setting the source and re-running the failed job, no code change needed |
| 2026-09-28 | Wrote spec 11 (Customize panel: status filter, gravity, star brightness, breathing, synapse visibility, constellation spin, auto-rotate, palette mode) | Last deferred item for full v1 baseline parity |
| 2026-09-28 | Spec 11 excludes v1's nebula, pulse animation, and constellation labels | Those are entire render layers never ported in any prior spec (pulses explicitly deferred in spec 02); wiring a settings panel to features that don't render yet isn't a settings job — scoped as future spec(s) that build the layer itself, not a silent drop |
| 2026-09-28 | Spec 11 built and verified: Customize panel (status filter with live counts, gravity, star brightness, breathing toggle, synapse visibility, constellation self-spin, whole-cosmos auto-rotate, palette mode), persisted separately from library data in `localStorage`. 63 unit tests passing (was 54), typecheck clean, production build succeeds, browser smoke test confirms every control applies live and survives a reload with no app errors. | Closes v1 baseline feature parity — every item in intent.md's baseline list is now built except nebula/pulses/labels (never-ported render layers, logged above as out of scope for this spec) |
| 2026-09-28 | Wrote spec 12: keyboard controls (Space freezes animation, Tab opens Customize, Escape closes panels) | New scope beyond v1 baseline, added at user request — v1 has no equivalent global shortcuts |
| 2026-09-28 | Spec 12 built and verified: Space/Tab/Escape wired, guarded so typing in a form control isn't hijacked. Typecheck clean, 63 tests passing (no new unit test added — store has no existing test file, single boolean toggle verified via smoke test instead), production build succeeds, browser smoke test confirms Tab opens/Escape closes the panel and Space freezes/unfreezes the canvas (pixel-identical while frozen, differs once resumed). | Closes spec 12 |
| 2026-09-28 | Wrote spec 13: first Maintain-stage work — wire render fps, ISBN success rate, import round-trip, and crash-free sessions to the analytics adapter; document the PostHog/Sentry dashboard setup as a manual checklist item, same treatment as spec 10's Pages-enable step | intent.md's success-metrics table has had four runtime metrics with zero signal since it was written |
| 2026-09-28 | Spec 13 built and verified: `ErrorBoundary` (crash-free signal + graceful fallback, since @sentry/browser alone doesn't catch React render errors), ISBN lookup success/not-found/failed events, import round-trip's `flagged` count added to `import_completed`, render fps sampled every ~10s. 64 unit tests passing (added a direct render-and-throw test for ErrorBoundary — its catch path can't be reached via the browser smoke test since the render loop runs in rAF, outside React's error-boundary scope). Typecheck clean, build succeeds, browser smoke test confirms the ISBN error path and the import ready/flagged split both render correctly. PostHog/Sentry secrets + dashboard alerts remain a manual checklist item (spec 13), not yet done. | Closes spec 13; first Maintain-stage code in the project |
| 2026-09-28 | Ran a commercial-launch gap analysis (engineering + marketing); logged as new intent.md section "Post-MVP: Commercial launch gaps" | Project is feature-complete against v1 and deployed but not commercially shippable — no accounts/sync, no backend, no legal, no monetization, no GTM; recorded as scope rather than acted on silently |
| 2026-09-28 | Backend/auth stack: Supabase. Monetization: freemium (free = local-only unchanged; paid = cross-device sync/accounts). "Real backend auth" and "cloud sync" moved from Out of scope into scope, gated by tier | User's explicit choice between Supabase/Firebase/custom/stay-local and freemium/one-time/free/undecided |
| 2026-09-28 | Wrote spec 14: Supabase auth + library sync foundation, scoped to auth+sync only — billing/tier-gating enforcement is separate future scope, not this spec | Foundation must exist before a paid tier can gate anything; billing integration (Stripe) is its own build with its own risk surface |
| 2026-09-28 | User created the Supabase project, ran the `libraries` table + RLS SQL, confirmed Email OTP is enabled, and provided the project URL + anon key (stored in `app/.env`, gitignored, not committed) | Unblocks spec 14 Build — same manual-step pattern as spec 10's Pages-enable step |
| 2026-09-28 | Spec 14 built: `@supabase/supabase-js` client (env-gated, no-ops without keys), magic-link auth (`auth/session.ts`), additive sync layer (`persistence/sync.ts`, last-write-wins by timestamp, IndexedDB stays source of truth for rendering/offline), Profile tab in Settings now a real sign-in flow instead of a stub. 67 unit tests passing (added sync-layer tests against a mocked Supabase client — real reconciliation glue in the store is exercised by the browser smoke test instead, same treatment as the render loop's own untested glue). Typecheck clean, build succeeds (bundle grew ~211KB→441KB gzipped from the Supabase client — noted, not addressed, not a blocker for MVP). Full magic-link round-trip **could not be verified this session**: this sandbox's egress proxy blocks `supabase.co` outright (confirmed via direct `curl`, "organization policy" 403) for both the shell and the headless browser — confirmed this is a sandbox network restriction, not an app bug, and doesn't affect real users since GitHub Pages visitors don't route through this proxy. | Closes spec 14's Build stage; **Test stage open item**: verify the magic-link round-trip end-to-end from outside this sandbox (the live deployed site, or a local dev machine) before calling spec 14 done |
| 2026-09-28 | Bug found in Deploy: `deploy.yml`'s build step never passed `VITE_SUPABASE_URL`/`VITE_SUPABASE_ANON_KEY` as env vars — the two repo secrets existed but weren't wired to the workflow, so the deployed build kept showing the Profile stub even after secrets were added. Fixed by adding both to the `env:` block, same as the existing PostHog/Sentry secrets | User confirmed via screenshot that Settings → Profile still showed the stub after adding secrets and re-running the workflow — caught before declaring spec 14 done |
| 2026-09-28 | Real root cause found after the above fix still didn't work: the repo secrets were saved as `VITTE_SUPABASE_URL`/`VITTE_SUPABASE_ANON_KEY` (typo'd double-T), not matching the workflow's `VITE_SUPABASE_*` names — GitHub silently resolves an unmatched `secrets.X` reference to an empty string rather than erroring, so the build succeeded with blank env vars every time. Diagnosed via a temporary debug step confirming `${{ secrets.VITE_SUPABASE_URL }}` itself evaluated to empty at the Actions-expression level (not a shell or Vite bug); a screenshot of the repo's Secrets and variables → Actions page then showed the actual typo. Fixed by the user recreating both secrets with correct names; debug step removed | A silent-empty-string failure mode is worth remembering — GitHub Actions gives zero error signal for a misnamed secret reference, so a wrong name looks identical to a working no-op |
| 2026-09-28 | Second Deploy bug found and fixed: `signInWithOtp` had no explicit `emailRedirectTo`, so it fell back to Supabase's default Site URL (`localhost:3000`) instead of the live site — magic link emails sent users to a dead address. Fixed by passing `window.location.origin + window.location.pathname` explicitly; also required the user to add the live URL under Supabase's Authentication → URL Configuration → Redirect URLs allowlist | Confirmed by user: sign-in now correctly shows "Signed in as [email]" in Settings → Profile after clicking a fresh magic link |
| 2026-09-28 | Spec 14's Test stage closed: magic-link sign-in verified working end-to-end on the live deployed site | Auth path confirmed; cross-device library sync round-trip still to be manually verified next |
| 2026-09-28 | Gap found: no UI for manual add-book or remove-book, despite `addBook('manual')`/`removeBook` already implemented in the store and unused. Wrote spec 15, UI-only (no model/store change) | User report: "there is no functionality to remove books or add them manually outside the ISBN option" |
| 2026-09-28 | Spec 15 built and verified: `AddBookManual.tsx` (v1 field-for-field port) wired into Toolbar; `Tooltip.tsx` got an inline confirm-then-remove control. Typecheck clean, 68 tests passing (added a direct component test for the remove flow — canvas click hit-testing isn't practical to drive from a Playwright smoke test since star screen position depends on the 3D projection; browser smoke did confirm the add form works end-to-end), production build succeeds | Closes spec 15 |
