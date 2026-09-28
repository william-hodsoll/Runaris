# Spec: React/Vite port of the v1 cosmos

## Requirement
Port `reference/neural_mind.py`'s generated app (vanilla JS/Canvas2D, single file) to React + TypeScript + Vite, preserving every listed baseline feature in `intent.md`, with no product-behavior changes except the two already decided: analytics added, PWA tooling re-implemented via Vite. This is the foundation spec — later specs (analytics wiring, IndexedDB migration, PWA polish) build on it.

In scope for this spec:
- Project scaffold (Vite + React + TS)
- Model layer: BookStar / Constellation types, placement math, connection derivation — ported from `build_mind()` / `addBookToMind()` / `computeConnections()`
- Render layer: Canvas2D projection + draw loop — ported from `project()`, `draw()`, camera/rotation/breathing math
- Persistence: localStorage parity first (same shape as v1's `neuralMind.v1` key), so this spec is a pure port with no data-model change yet
- Core interactions: drag-rotate, scroll/pinch-zoom, tap-to-inspect (tooltip), connect mode
- Load the v1 demo library as fixture data for parity testing

Out of scope for this spec (separate specs): ISBN scan/OpenLibrary, CSV/Goodreads import, timelapse, insights, customize/palette, settings tabs, analytics wiring, IndexedDB migration, Vite PWA plugin setup, Login/Social stub screens. These port in the same pattern once this foundation is verified — sequencing is in `intent.md`'s decisions log intent (port v1 behavior first, then layer the two approved changes on top).

## Design

### Data model
```ts
type BookStar = {
  id: string;
  title: string;
  author: string;
  year?: string;
  genre?: string;
  subjects: string[];
  pages?: number;
  isbn?: string;
  coverUrl?: string;
  status?: string;
  dateAdded: number;          // ms epoch, matches v1
  constellationId: string;
  position: { x: number; y: number; z: number };
  offset: { x: number; y: number; z: number };  // ox/oy/oz in v1
  size: number;                // derived from pages, v1's size_from_pages()
  color: string;
  phase: number;                // twinkle phase
  speed: number;                // twinkle speed
};

type Constellation = {
  id: string;
  subject: string;
  position: { x: number; y: number; z: number };
  color: string;
  axis: { x: number; y: number; z: number };
  spinSpeed: number;
  spinPhase: number;
  count: number;
};

type Library = {
  version: 1;
  stars: BookStar[];
  constellations: Constellation[];
};
```
Connections (edges + synapses) are NOT persisted — derive on load and on every mutation, exactly as v1's `computeConnections`/synapse-build does. Storing them would let them drift from the source data.

### Layers
- `model/` — pure TS: `buildLibrary(books)` (placement, ports `build_mind`), `addBook(library, book)` (ports `addBookToMind`), `deriveConnections(library, sourceId)` (ports `computeConnections`), `deriveSynapses(library)`. No DOM, no canvas, unit-testable in isolation.
- `render/` — Canvas2D: `project(point, camera)`, `draw(ctx, library, camera, time)` main loop, hit-testing (`pickStar`) for click/tap. Reads from a ref/store snapshot each frame, never from React props/state directly, matching v1's global-array approach — ports `project()`, `draw()`, `pickStar()`, `liveStarPos()`, camera tween logic.
- `store/` — Zustand: holds the Library, camera state, UI mode (idle/connect-mode/tooltip-open). React components read from it for UI chrome (tooltip contents, HUD); the render loop reads the underlying mutable snapshot directly for performance, same tradeoff v1 makes with its global arrays.
- `persistence/` — localStorage save/load, same key shape as v1 for this spec (`saveState`/`loadState` port), versioned so a later IndexedDB migration has a clean cutover point.
- `components/` — React: Canvas host component (owns the `<canvas>` element and RAF loop), Tooltip, ConnectModeHUD, top-level App shell. Everything else (import, scan, settings, etc.) is out of scope here — stub routes only, to be filled by later specs.

### Interactions ported in this spec
- Drag to rotate camera (pointer events -> camera rotation, matches v1's rotate handling)
- Scroll/pinch to zoom
- Tap/click a star -> tooltip with title/author/cover placeholder (cover fetch is out of scope here, stub the slot)
- Tap a star while another is selected -> enter connect mode, highlight derived connections, exit on tap-away (ports `enterConnectMode`/`exitConnectMode`)

### Edge cases
- Empty library (no books yet): render an empty sphere / prompt state, no divide-by-zero in placement math (v1 already guards `n_subj === 0`; carry the guard forward)
- Library loaded from a corrupt/foreign localStorage value: validate on load, fall back to empty library with a visible warning rather than throwing
- Very large libraries (test with v1's 232-book demo set as the floor, and a synthetic 1000-book fixture as the perf check)

## Test plan
1. Model unit tests: placement determinism given a fixed seed (matches v1's `seed` param), connection derivation matches expected shared-subject/genre/author pairs on a small fixture, empty-library guard
2. Visual parity check: render the v1 demo library (232 books) in both the old HTML and the new React app side by side, confirm same constellation count, same star count, same connection count (values, not pixel-perfect position, since v1's RNG and the port's RNG won't match seed-for-seed unless deliberately ported)
3. Perf: RAF loop holds 60fps with 232 books; synthetic 1000-book fixture — record fps, compare to the `intent.md` breach threshold (<30fps)
4. Interaction tests: drag-rotate changes camera angle; tap selects correct star (hit-test); connect mode highlights the right set on a fixture with known shared attributes
5. Save/load round-trip: build library, save to localStorage, reload, deep-equal (matches `intent.md` fidelity metric)

## Rollback
`reference/neural_mind.py` still generates the working v1 HTML independently — it is not deleted or modified by this port. If the React/Vite build breaks or underperforms, v1 remains usable as-is with zero rollback action needed. Once the React app is the shipped version, rollback = redeploy the last tagged React build; no data migration risk in this spec since the localStorage shape is unchanged from v1.
