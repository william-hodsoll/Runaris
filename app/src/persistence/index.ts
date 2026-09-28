// IndexedDB-backed persistence — replaces localStorage.ts as the store's
// primary read/write path (localStorage.ts stays, for the migration source
// and its own tests). See specs/06-indexeddb-migration.md.
import type { Library } from '../model/types';
import { validateLibrary } from '../model/validate';
import { idbGet, idbSet } from './db';
import { loadLibrary as loadFromLocalStorage } from './localStorage';

const EMPTY: Library = { version: 1, stars: [], constellations: [] };

export async function saveLibrary(library: Library): Promise<{ ok: true } | { ok: false; error: string }> {
  try {
    await idbSet(library);
    return { ok: true };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e.message : 'Unknown storage error' };
  }
}

export async function loadLibrary(): Promise<{ library: Library; warning?: string }> {
  let existing: unknown;
  try {
    existing = await idbGet();
  } catch {
    return { library: EMPTY, warning: 'Could not read your library from storage; starting fresh.' };
  }

  if (existing !== undefined) {
    return validateLibrary(existing);
  }

  // Nothing in IndexedDB yet — migrate from the v1-parity localStorage key if
  // present. The localStorage copy is left in place (belt-and-suspenders),
  // not deleted, per specs/06-indexeddb-migration.md.
  const fromLocalStorage = loadFromLocalStorage();
  if (fromLocalStorage.library.stars.length > 0 || fromLocalStorage.library.constellations.length > 0) {
    await idbSet(fromLocalStorage.library).catch(() => {
      // Migration write failure isn't fatal — the library still loads from
      // localStorage for this session; it'll retry the migration next load.
    });
    return fromLocalStorage;
  }

  return { library: EMPTY };
}
