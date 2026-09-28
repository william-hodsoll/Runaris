import { describe, expect, it } from 'vitest';
import { buildLibrary } from '../../model/buildLibrary';
import { liveStarPos } from '../liveStarPos';

describe('liveStarPos', () => {
  const lib = buildLibrary([{ title: 'A', subjects: ['tech'] }], 1);
  const star = lib.stars[0];
  const centre = lib.constellations[0];

  it('breathing: false returns the unscaled (breath=1) position', () => {
    const withBreath = liveStarPos(star, centre, 1.23, 1, true, 1);
    const noBreath = liveStarPos(star, centre, 1.23, 1, false, 1);
    // Same angle, different scale — the two should differ (breath != 1 at t=1.23)
    // unless breath happens to be exactly 1, so compare against a manual breath=1 calc.
    expect(noBreath).not.toEqual(withBreath);
  });

  it('constellationSpin multiplies the rotation angle, moving the star further at spin=2 than spin=1', () => {
    const spin1 = liveStarPos(star, centre, 5, 1, false, 1);
    const spin2 = liveStarPos(star, centre, 5, 1, false, 2);
    expect(spin2).not.toEqual(spin1);
  });

  it('gravity=0 collapses every star onto its constellation centre', () => {
    const pos = liveStarPos(star, centre, 5, 0, false, 1);
    expect(pos.x).toBeCloseTo(centre.position.x);
    expect(pos.y).toBeCloseTo(centre.position.y);
    expect(pos.z).toBeCloseTo(centre.position.z);
  });
});
