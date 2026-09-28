import { describe, expect, it } from 'vitest';
import { buildLibrary } from '../../model/buildLibrary';
import { paletteColor } from '../palette';

describe('paletteColor', () => {
  const lib = buildLibrary([{ title: 'A', subjects: ['tech'] }], 1);
  const star = lib.stars[0];

  it('passes the stored color through unchanged for default mode', () => {
    expect(paletteColor(star, 0, 'default')).toBe(star.color);
  });

  it('returns a pool color for warm/cool/mono, cycled by constellation index', () => {
    const warm0 = paletteColor(star, 0, 'warm');
    const warm8 = paletteColor(star, 8, 'warm'); // pool has 8 entries, wraps to index 0
    expect(warm0).toBe(warm8);
    expect(warm0).not.toBe(star.color);
  });
});
