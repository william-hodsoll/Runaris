import { describe, expect, it } from 'vitest';
import { buildLibrary } from '../../model/buildLibrary';
import { filterVisible, timelapseBounds } from '../timelapse';

describe('timelapse', () => {
  it('returns null bounds for an empty library', () => {
    expect(timelapseBounds({ version: 1, stars: [], constellations: [] })).toBeNull();
  });

  it('computes min/max dateAdded across the library', () => {
    const lib = buildLibrary(
      [
        { title: 'A', subjects: ['x'] },
        { title: 'B', subjects: ['x'] },
        { title: 'C', subjects: ['x'] },
      ],
      1,
    );
    const bounds = timelapseBounds(lib)!;
    const dates = lib.stars.map((s) => s.dateAdded);
    expect(bounds.min).toBe(Math.min(...dates));
    expect(bounds.max).toBe(Math.max(...dates));
  });

  it('filterVisible returns an empty set for a cutoff before the earliest book', () => {
    const lib = buildLibrary([{ title: 'A', subjects: ['x'] }], 1);
    const bounds = timelapseBounds(lib)!;
    expect(filterVisible(lib, bounds.min - 1).size).toBe(0);
  });

  it('filterVisible returns everything for a cutoff at or after the latest book', () => {
    const lib = buildLibrary(
      [
        { title: 'A', subjects: ['x'] },
        { title: 'B', subjects: ['y'] },
      ],
      1,
    );
    const bounds = timelapseBounds(lib)!;
    expect(filterVisible(lib, bounds.max).size).toBe(lib.stars.length);
  });

  it('filterVisible only includes stars added at or before the cutoff', () => {
    const lib = buildLibrary([{ title: 'A', subjects: ['x'] }], 1);
    const star = lib.stars[0];
    expect(filterVisible(lib, star.dateAdded).has(star.id)).toBe(true);
    expect(filterVisible(lib, star.dateAdded - 1).has(star.id)).toBe(false);
  });
});
