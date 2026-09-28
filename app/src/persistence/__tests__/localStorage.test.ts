import { beforeEach, describe, expect, it } from 'vitest';
import { buildLibrary } from '../../model/buildLibrary';
import { clearLibrary, loadLibrary, saveLibrary } from '../localStorage';

describe('localStorage persistence', () => {
  beforeEach(() => clearLibrary());

  it('round-trips a library with zero loss', () => {
    const original = buildLibrary(
      [
        { title: 'A', author: 'X', subjects: ['tech'], pages: 200 },
        { title: 'B', author: 'Y', subjects: ['fiction'], pages: 300 },
      ],
      7,
    );
    const result = saveLibrary(original);
    expect(result.ok).toBe(true);
    const { library, warning } = loadLibrary();
    expect(warning).toBeUndefined();
    expect(library).toEqual(original);
  });

  it('falls back to an empty library on corrupt data, with a warning', () => {
    localStorage.setItem('neuralMind.v1', '{not valid json');
    const { library, warning } = loadLibrary();
    expect(library.stars).toHaveLength(0);
    expect(warning).toBeTruthy();
  });

  it('falls back to an empty library on a foreign shape, with a warning', () => {
    localStorage.setItem('neuralMind.v1', JSON.stringify({ hello: 'world' }));
    const { library, warning } = loadLibrary();
    expect(library.stars).toHaveLength(0);
    expect(warning).toBeTruthy();
  });

  it('returns an empty library with no warning when nothing is stored yet', () => {
    const { library, warning } = loadLibrary();
    expect(library.stars).toHaveLength(0);
    expect(warning).toBeUndefined();
  });
});
