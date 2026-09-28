# Spec: Camera barcode scan

## Requirement
v1 uses ZXing (dynamically loaded) for camera ISBN barcode scanning. This spec closes that gap, feeding the same `lookupByIsbn` adapter built in spec 04.

## Design decision
Use the native `BarcodeDetector` API (Chrome/Edge/Android; no dependency) instead of porting ZXing, with a capability check and a clear fallback to the existing text-entry flow when unsupported (Safari/Firefox as of this writing) — smaller bundle, no new dependency, matches CLAUDE.md's "port, don't redesign" only where v1's approach is still the best option; here it isn't, since v1 hand-rolls what the platform now offers natively. If `BarcodeDetector` coverage becomes a real blocker, ZXing is the documented fallback (v1 already proves it works) — not implemented here to avoid carrying a scanning library for browsers that will get the native API anyway.

- `scan/barcodeScanner.ts`: `isScanSupported(): boolean` (checks `'BarcodeDetector' in window`), `scanIsbnFromVideo(video: HTMLVideoElement): Promise<string | null>` — one-shot detect call against a live `<video>` frame, filtered to EAN-13 (ISBN-13 format).
- `components/ScanIsbn.tsx`: requests camera via `getUserMedia`, shows the video feed, polls `scanIsbnFromVideo` a few times a second, on a hit calls the same `lookupByIsbn` + preview/confirm UI as `AddByIsbn`. If `isScanSupported()` is false, shows "not supported on this browser, use Add by ISBN instead" and links there — never a dead button.
- Camera permission denial is handled distinctly from "unsupported" (different message: "camera access denied" vs "scanning not supported here").

## Test plan
1. `isScanSupported()` correctly reflects `BarcodeDetector` presence (mockable via a stubbed global)
2. `scanIsbnFromVideo` returns the decoded value on a mocked `BarcodeDetector.detect()` result, null on no detection
3. Component shows the unsupported-fallback message and a working link to `AddByIsbn` when `BarcodeDetector` is absent (no camera permission prompt attempted)
4. Camera permission denial shows a distinct, non-crashing error state

## Rollback
Entry point only — hidden/disabled if unsupported, and `AddByIsbn` (already shipped) remains the always-available path. No model changes.
