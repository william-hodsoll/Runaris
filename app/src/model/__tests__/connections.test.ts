import { describe, expect, it } from 'vitest';
import { buildLibrary } from '../buildLibrary';
import { deriveConnectionsFor, deriveEdges, deriveSynapses } from '../connections';
import type { BookInput } from '../types';

const fixture: BookInput[] = [
  { title: 'A', author: 'Shared Author', subjects: ['tech'], pages: 200 },
  { title: 'B', author: 'Shared Author', subjects: ['fiction'], pages: 250 }, // shares author with A
  { title: 'C', author: 'Other', subjects: ['tech'], pages: 300 }, // shares subject with A
  { title: 'D', author: 'Nobody', subjects: ['history'], pages: 150 }, // unrelated
];

describe('connections', () => {
  it('derives edges from shared subject or author, not unrelated books', () => {
    const lib = buildLibrary(fixture, 1);
    const [a, b, c, d] = lib.stars;
    const edges = deriveEdges(lib);
    const pairs = new Set(edges.map((e) => [e.a, e.b].sort().join('|')));
    expect(pairs.has([a.id, b.id].sort().join('|'))).toBe(true); // shared author
    expect(pairs.has([a.id, c.id].sort().join('|'))).toBe(true); // shared subject
    expect(pairs.has([a.id, d.id].sort().join('|'))).toBe(false); // unrelated
    expect(pairs.has([d.id, b.id].sort().join('|'))).toBe(false);
  });

  it('deriveConnectionsFor returns exactly the related set for a given star', () => {
    const lib = buildLibrary(fixture, 1);
    const [a, b, c, d] = lib.stars;
    const lit = deriveConnectionsFor(lib, a.id);
    expect(lit.has(b.id)).toBe(true);
    expect(lit.has(c.id)).toBe(true);
    expect(lit.has(d.id)).toBe(false);
  });

  it('deriveSynapses only links stars within the same constellation', () => {
    const lib = buildLibrary(fixture, 1);
    const synapses = deriveSynapses(lib);
    const idToConstellation = new Map(lib.stars.map((s) => [s.id, s.constellationId]));
    for (const s of synapses) {
      expect(idToConstellation.get(s.a)).toBe(idToConstellation.get(s.b));
    }
  });

  it('returns no synapses for a singleton constellation', () => {
    const lib = buildLibrary([{ title: 'Lonely', subjects: ['solo'] }], 1);
    expect(deriveSynapses(lib)).toHaveLength(0);
  });
});
