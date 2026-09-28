# Spec: Customize panel (status filter + visual controls)

## Requirement
Port v1's Customize panel (`neural_mind.py` ~L2646-2793, `app.visual`): reading-status filter and the live visual controls that already have a rendering hook in the rebuild. Last deferred item for full v1 baseline parity (intent.md decisions log, 2026-09-28).

**Scope cut vs. v1 (logged, not silent):** v1's nebula, pulse animation, and constellation labels are separate render layers that were never ported at all (pulses explicitly deferred in spec 02; nebula/labels never mentioned in any prior spec). Wiring settings controls to them now would mean building three new render features under a "settings" spec. This spec ports only the controls for render params that already exist in the port: status filter, gravity, star brightness, breathing toggle, synapse visibility, constellation self-spin multiplier, whole-mind auto-rotate, and palette mode. Nebula/pulses/labels stay out of scope until a future spec builds the layer itself.

## Design
**State** — new `visual` slice on `useLibraryStore` (not on `Library`/IndexedDB — this isn't library data, so no schema bump):
```ts
type VisualSettings = {
  statusFilter: 'all' | 'reading' | 'finished' | 'unread' | 'abandoned';
  gravity: number;          // 0.3–2.5, default 1
  starBrightness: number;   // 0.4–2, default 1
  breathing: boolean;       // default true
  showSynapses: boolean;    // default true
  constellationSpin: number;// 0–4, default 1 (multiplies each centre's own spinSpeed)
  rotationSpeed: number;    // 0–0.4 rad/s, default 0 (whole-mind auto-rotate)
  paletteMode: 'default' | 'warm' | 'cool' | 'mono';
};
```
Persisted synchronously to a plain `localStorage` key (`neuralMind.visual.v1`) on every change — separate from the async IndexedDB library store, same pattern v1 used for its `visual` blob but split out since our persistence layer already separates concerns.

**Palette recoloring** — pure function, not stored mutation (v1 mutates `star.color` and keeps `origColor` to reset; we don't need that field at all): `paletteColor(star, constellationIndex, mode)` in `render/palette.ts` returns the display color for the frame; `mode === 'default'` returns `star.color` unchanged. Same three pools as v1 (warm/cool/mono), cycled by constellation index like v1's `applyPalette`.

**Render wiring** (`draw.ts`, `liveStarPos.ts`, `CanvasHost.tsx`):
- `liveStarPos` gains `gravity` (already a param, just thread it from `visual.gravity` instead of the default) and a `breathing: boolean` param — skip `breathScale` when false.
- `draw()`'s `DrawState` gains `visual: VisualSettings`. Radius multiplies by `visual.starBrightness`. Synapse loop skipped entirely when `!visual.showSynapses`. Status filter dims non-matching stars the same way connect-mode dims non-lit ones (both must match for a synapse line to stay bright, matching v1 L1514-1515).
- `constellationSpin` multiplies `constellation.spinSpeed` inside `liveStarPos`'s angle calc.
- `rotationSpeed`: `CanvasHost`'s frame loop adds `visual.rotationSpeed * dt` to `camera.rotY` each frame (camera is already local/mutable there, matching v1's side-channel `autoRotate`).

**UI** — new `CustomizePanel.tsx`, opened from Toolbar next to Settings (v1 keeps it as its own top-level action, not buried in Settings). Status filter as chip row with live counts (`countByStatus` added to `model/insights.ts`); sliders for gravity/brightness/spin/rotation; checkboxes for breathing/synapses; select for palette. All controls write straight to the store slice — no local component state, no "Done" gating (matches v1: every control applies live).

## Test plan
- Unit: `countByStatus`, `paletteColor` (each mode returns expected pool color, default passthrough), `liveStarPos` with `breathing: false` returns unscaled position, `constellationSpin` multiplier changes angle.
- `visual` slice: default values, persists to and rehydrates from `localStorage`.
- Typecheck clean, `vitest run` all passing, `npm run build` succeeds.
- Browser smoke test: open Customize, toggle status filter (stars dim), drag gravity slider (cluster tightness visibly changes), toggle breathing/synapses, confirm settings survive a reload.

## Rollback
New slice + new component + render params with defaults matching current behavior (`gravity: 1`, `breathing: true`, etc.) — reverting the commit returns exactly to pre-spec rendering with no data migration needed.
