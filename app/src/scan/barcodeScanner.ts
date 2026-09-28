// Native BarcodeDetector-based ISBN scanning — see specs/09-camera-scan.md
// for why this replaces v1's ZXing dependency.
export function isScanSupported(): boolean {
  return typeof window !== 'undefined' && typeof window.BarcodeDetector !== 'undefined';
}

let detector: BarcodeDetector | null = null;
function getDetector(): BarcodeDetector {
  if (!detector) detector = new BarcodeDetector({ formats: ['ean_13'] });
  return detector;
}

/** One-shot scan of a live video frame. Returns the decoded ISBN-13 digits,
 * or null if nothing was detected in this frame. */
export async function scanIsbnFromVideo(video: HTMLVideoElement): Promise<string | null> {
  const barcodes = await getDetector().detect(video);
  const hit = barcodes.find((b) => /^\d{13}$/.test(b.rawValue));
  return hit ? hit.rawValue : null;
}

/** Reset the cached detector — used in tests so each test gets a fresh mock. */
export function _resetDetectorForTests(): void {
  detector = null;
}
