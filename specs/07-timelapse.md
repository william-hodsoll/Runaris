# Spec: Timelapse

## Requirement
Port v1's timelapse: scrub/play through `dateAdded` so the cosmos visibly forms over time, star by star.

## Design
- `render/timelapse.ts`: given a timestamp cutoff, filters which stars are "visible" (`star.dateAdded <= cutoff`) — pure function, testable without canvas.
- `draw()` in `render/draw.ts` gains an optional `visibleIds: Set<string> | null` param; when set, stars/synapses/edges outside it are skipped entirely (not dimmed — matches v1's "forms from nothing" effect, distinct from connect-mode dimming).
- `components/TimelapseControls.tsx`: a slider (min = earliest `dateAdded`, max = latest) + play/pause button. Play advances the cutoff on a timer (ports `startTimelapsePlay`/`tlValueToTimestamp`/`tlFormatDate`).
- Store gains `timelapseCutoff: number | null` (null = show everything, the default/non-timelapse state) and `setTimelapseCutoff`/`exitTimelapse`.

## Test plan
1. `filterVisible(library, cutoff)` returns only stars with `dateAdded <= cutoff`, empty set for a cutoff before the earliest book
2. Slider bounds computed correctly from a library's min/max `dateAdded` (matches `tlBounds()`)
3. Draw with a non-null `visibleIds` renders none of the excluded stars' synapses (no orphan half-edges)
4. Exiting timelapse (`timelapseCutoff = null`) restores full rendering

## Rollback
Purely additive rendering/UI; `visibleIds = null` is the existing behavior, so this can't regress anything already shipped even if the feature itself is buggy.
