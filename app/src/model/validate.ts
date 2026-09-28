import type { Library } from './types';

/** Guards a Library loaded from an untrusted source (localStorage, import).
 * Returns an empty library rather than throwing — matches CLAUDE.md's
 * "flag/fall back, never silently drop or crash" convention. */
export function validateLibrary(value: unknown): { library: Library; warning?: string } {
  const empty: Library = { version: 1, stars: [], constellations: [] };
  if (!value || typeof value !== 'object') {
    return { library: empty, warning: 'Stored library was not an object; starting fresh.' };
  }
  const v = value as Partial<Library>;
  if (v.version !== 1 || !Array.isArray(v.stars) || !Array.isArray(v.constellations)) {
    return { library: empty, warning: 'Stored library had an unexpected shape; starting fresh.' };
  }
  return { library: v as Library };
}
