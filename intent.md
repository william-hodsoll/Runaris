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
- Real backend auth / real social features (Login/Social stay stubs)
- Real-time collaboration
- Cloud sync of library data across devices
- Changing the core visual metaphor (star field) to a freeform mind map

## Constraints
- Platform: Web app first (PWA); desktop (Tauri) and mobile (Capacitor) wrap the same codebase later — one engine, three shells
- Stack: TypeScript + React + Vite (migrated from v1's vanilla JS). Canvas2D custom renderer carries over — this is a 3D-projected star field, not a graph-layout library (Konva/React Flow don't fit); render loop and camera/projection math port from v1 largely as-is, wrapped in React for state/UI chrome only. State via Zustand, kept out of the render loop (render loop reads refs, not React state, to hit 60fps)
- External data: OpenLibrary Search API + Books API (ISBN), both key-less — same as v1
- Data: Local-only for library content (no change from v1's local-only model); pick IndexedDB vs. localStorage in the Design spec — IndexedDB better fits larger libraries and cover-image caching
- Privacy: Analytics on by default, opt-out in settings, visible privacy notice on first run. Tracks product usage (feature/flow events, session counts) and performance/crash data — never book titles, authors, notes, or map content. Library data itself stays local-only, unaffected by analytics.
- Analytics stack: PostHog (product usage/events) + Sentry (crash reports, performance) — both third-party, both support scrubbing PII before send

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
