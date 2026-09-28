# Spec: Keyboard controls

## Requirement
Global keyboard shortcuts for the canvas: Space freezes/unfreezes all animation (breathing, spin, auto-rotate, twinkle), Tab opens/closes the Customize panel, Escape closes whatever panel is open. Not a v1 feature — v1 only handles Escape inside its own modal (`neural_mind.py` L2465) and Enter/Escape while editing a tooltip note (L2042). New scope, added at user request.

## Design
- Store: `frozen: boolean` + `toggleFrozen()` on `useLibraryStore`, not persisted (matches v1's transient `app.frozen`, session-only).
- `CanvasHost`'s frame loop: `const dt = frozen ? 0 : Math.min(0.05, (now - last_t) / 1000)` — one change freezes `renderTime` (twinkle/breathing/spin) and the auto-rotate `camera.rotY` increment together, since both already derive from `dt`/`renderTime`. Picking/dragging still work while frozen.
- `Toolbar` owns a single `window.addEventListener('keydown', ...)` (it already owns panel-open state):
  - Guard: ignore when `document.activeElement` is an input/textarea/select or is `contentEditable` — sliders, text fields, and the ISBN/import forms keep normal Tab/Space behavior.
  - `' '` → `preventDefault()` (stop page scroll) + `toggleFrozen()`.
  - `'Tab'` → `preventDefault()` + toggle the Customize panel open/closed.
  - `'Escape'` → close whichever panel is open.
- No visual "frozen" indicator — matches v1's minimal chrome; the animation itself visibly stops.

## Test plan
- Unit: `toggleFrozen` flips the store flag.
- Typecheck clean, `vitest run` passing, `npm run build` succeeds.
- Browser smoke test: Space freezes the star field (position sampled twice is identical), Tab opens/closes Customize, Escape closes it, and typing in a Customize slider/select doesn't trigger the shortcuts.

## Rollback
New store field (default `false`) + one keydown listener — reverting the commit returns to no keyboard handling with no data impact.
