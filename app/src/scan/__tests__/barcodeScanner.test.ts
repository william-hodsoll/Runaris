import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { _resetDetectorForTests, isScanSupported, scanIsbnFromVideo } from '../barcodeScanner';

describe('barcodeScanner', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    _resetDetectorForTests();
  });

  it('reports unsupported when BarcodeDetector is absent', () => {
    vi.stubGlobal('BarcodeDetector', undefined);
    expect(isScanSupported()).toBe(false);
  });

  it('reports supported when BarcodeDetector is present', () => {
    vi.stubGlobal('BarcodeDetector', class {});
    expect(isScanSupported()).toBe(true);
  });

  describe('with a mocked detector', () => {
    beforeEach(() => {
      class MockDetector {
        detect = vi.fn();
      }
      vi.stubGlobal('BarcodeDetector', MockDetector);
    });

    it('returns the decoded ISBN-13 value on a hit', async () => {
      vi.stubGlobal(
        'BarcodeDetector',
        class {
          detect = vi.fn().mockResolvedValue([{ rawValue: '9780132350884', format: 'ean_13' }]);
        },
      );
      const result = await scanIsbnFromVideo({} as HTMLVideoElement);
      expect(result).toBe('9780132350884');
    });

    it('returns null when nothing is detected', async () => {
      vi.stubGlobal(
        'BarcodeDetector',
        class {
          detect = vi.fn().mockResolvedValue([]);
        },
      );
      const result = await scanIsbnFromVideo({} as HTMLVideoElement);
      expect(result).toBeNull();
    });

    it('ignores a detected barcode that is not a 13-digit ISBN shape', async () => {
      vi.stubGlobal(
        'BarcodeDetector',
        class {
          detect = vi.fn().mockResolvedValue([{ rawValue: 'not-an-isbn', format: 'qr_code' }]);
        },
      );
      const result = await scanIsbnFromVideo({} as HTMLVideoElement);
      expect(result).toBeNull();
    });
  });
});
