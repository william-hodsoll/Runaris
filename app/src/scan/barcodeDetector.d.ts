// Ambient types for the native BarcodeDetector API — not yet in TS's DOM lib.
interface BarcodeDetectorOptions {
  formats?: string[];
}
interface DetectedBarcode {
  rawValue: string;
  format: string;
}
declare class BarcodeDetector {
  constructor(options?: BarcodeDetectorOptions);
  static getSupportedFormats(): Promise<string[]>;
  detect(source: CanvasImageSource): Promise<DetectedBarcode[]>;
}
interface Window {
  BarcodeDetector?: typeof BarcodeDetector;
}
