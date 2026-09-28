// Ports saveState()/loadState() from reference/neural_mind.py. Same storage
// key and shape as v1 for this spec — see intent.md "pick IndexedDB vs.
// localStorage in the Design spec" (deferred; this is the parity baseline).
import type { Library } from '../model/types';
import { validateLibrary } from '../model/validate';

const STORAGE_KEY = 'neuralMind.v1';

export function saveLibrary(library: Library): { ok: true } | { ok: false; error: string } {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(library));
    return { ok: true };
  } catch (e) {
    // Surfaced to the UI as a visible warning, never a silent drop —
    // CLAUDE.md "Never ... silently" convention.
    return { ok: false, error: e instanceof Error ? e.message : 'Unknown storage error' };
  }
}

export function loadLibrary(): { library: Library; warning?: string } {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { library: { version: 1, stars: [], constellations: [] } };
    return validateLibrary(JSON.parse(raw));
  } catch {
    return {
      library: { version: 1, stars: [], constellations: [] },
      warning: 'Stored library was corrupt and could not be read; starting fresh.',
    };
  }
}

export function clearLibrary(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // best-effort, matches v1's clearPersistedState()
  }
}
