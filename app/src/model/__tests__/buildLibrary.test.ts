import { describe, expect, it } from 'vitest';
import { buildLibrary } from '../buildLibrary';
import type { BookInput } from '../types';

const fixture: BookInput[] = [
  { title: 'A', author: 'X', subjects: ['tech'], pages: 200 },
  { title: 'B', author: 'Y', subjects: ['tech'], pages: 400 },
  { title: 'C', author: 'Z', subjects: ['fiction'], pages: 300 },
];

describe('buildLibrary', () => {
  it('returns an empty library for no books (no divide-by-zero)', () => {
    const lib = buildLibrary([], 1);
    expect(lib.stars).toHaveLength(0);
    expect(lib.constellations).toHaveLength(0);
  });

  it('groups books into one constellation per primary subject', () => {
    const lib = buildLibrary(fixture, 1);
    expect(lib.constellations).toHaveLength(2); // tech, fiction
    expect(lib.stars).toHaveLength(3);
  });

  it('is deterministic given the same seed', () => {
    const a = buildLibrary(fixture, 42);
    const b = buildLibrary(fixture, 42);
    expect(a.constellations.map((c) => c.position)).toEqual(b.constellations.map((c) => c.position));
    expect(a.stars.map((s) => s.position)).toEqual(b.stars.map((s) => s.position));
  });

  it('scales star size with page count within a subject', () => {
    const lib = buildLibrary(fixture, 1);
    const [a, b] = lib.stars.filter((s) => s.subjects.includes('tech'));
    // A has 200 pages, B has 400 — B should render larger.
    expect(b.size).toBeGreaterThan(a.size);
  });

  it('defaults an untitled/unauthored book without throwing', () => {
    const lib = buildLibrary([{ title: '' }], 1);
    expect(lib.stars[0].title).toBe('Untitled');
    expect(lib.stars[0].author).toBe('Unknown');
  });
});
