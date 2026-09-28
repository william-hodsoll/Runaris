import { beforeEach, describe, expect, it } from 'vitest';
import { buildLibrary } from '../../model/buildLibrary';
import { loadLibrary, saveLibrary } from '../index';
import { idbClear } from '../db';
import { clearLibrary as clearLocalStorage, saveLibrary as saveToLocalStorage } from '../localStorage';

describe('IndexedDB-backed persistence', () => {
  beforeEach(async () => {
    await idbClear();
    clearLocalStorage();
  });

  it('returns an empty library when nothing is stored anywhere', async () => {
    const { library, warning } = await loadLibrary();
    expect(library.stars).toHaveLength(0);
    expect(warning).toBeUndefined();
  });

  it('round-trips a library through IndexedDB with zero loss', async () => {
    const original = buildLibrary([{ title: 'Dune', author: 'Frank Herbert', subjects: ['sci-fi'] }], 5);
    const result = await saveLibrary(original);
    expect(result.ok).toBe(true);
    const { library, warning } = await loadLibrary();
    expect(warning).toBeUndefined();
    expect(library).toEqual(original);
  });

  it('migrates existing localStorage data into IndexedDB on first hydrate, without deleting it', async () => {
    const legacy = buildLibrary([{ title: '1984', author: 'George Orwell', subjects: ['classic'] }], 9);
    saveToLocalStorage(legacy);

    const { library } = await loadLibrary();
    expect(library).toEqual(legacy);

    // Second load should now come from IndexedDB directly (localStorage untouched either way).
    const second = await loadLibrary();
    expect(second.library).toEqual(legacy);
    expect(localStorage.getItem('neuralMind.v1')).not.toBeNull();
  });

  it('falls back to an empty library with a warning on a foreign record shape', async () => {
    await saveLibrary({ nonsense: true } as never);
    const { library, warning } = await loadLibrary();
    expect(library.stars).toHaveLength(0);
    expect(warning).toBeTruthy();
  });
});
