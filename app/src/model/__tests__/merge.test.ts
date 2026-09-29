// See specs/17-sync-integrity.md.
import { describe, expect, it, vi } from 'vitest';
import { addBook, removeBook } from '../addBook';
import { mergeLibraries, repairDuplicateIds } from '../merge';
import type { Library } from '../types';

const empty: Library = { version: 1, stars: [], constellations: [] };
const titles = (l: Library) => l.stars.map((s) => s.title).sort();

describe('P0-1: ids stay unique across page loads', () => {
  it('add -> reload -> add gives distinct ids; removing one keeps the other', async () => {
    vi.resetModules(); // fresh "page load" #1 (other tests may have advanced module state)
    const first = await import('../addBook');
    let lib = first.addBook(empty, { title: 'A', subjects: ['x'] }, 1);
    vi.resetModules(); // simulate a page reload
    const second = await import('../addBook');
    lib = second.addBook(lib, { title: 'B', subjects: ['y'] }, 2);
    expect(new Set(lib.stars.map((s) => s.id)).size).toBe(2);
    expect(titles(second.removeBook(lib, lib.stars[1].id))).toEqual(['A']);
  });

  it('repairs duplicate ids already saved by the old counter', () => {
    let lib = addBook(empty, { title: 'A', subjects: ['x'] }, 1);
    lib = addBook(lib, { title: 'B', subjects: ['y'] }, 2);
    // Recreate the old bug's saved shape: both stars and constellations collide.
    const dup: Library = {
      version: 1,
      stars: lib.stars.map((s, i) => ({ ...s, id: 'star-added-1', constellationId: 'const-added-1', subjects: [i ? 'y' : 'x'] })),
      constellations: lib.constellations.map((c) => ({ ...c, id: 'const-added-1' })),
    };
    const fixed = repairDuplicateIds(dup);
    expect(new Set(fixed.stars.map((s) => s.id)).size).toBe(2);
    expect(new Set(fixed.constellations.map((c) => c.id)).size).toBe(2);
    // Each star lands in the constellation matching its subject.
    for (const s of fixed.stars) {
      expect(fixed.constellations.find((c) => c.id === s.constellationId)?.subject).toBe(s.subjects[0]);
    }
    expect(titles(removeBook(fixed, fixed.stars[0].id))).toHaveLength(1);
  });

  it('leaves a clean library untouched (same object)', () => {
    const lib = addBook(empty, { title: 'A', subjects: ['x'] }, 1);
    expect(repairDuplicateIds(lib)).toBe(lib);
  });
});

describe('mergeLibraries (3-way by star id)', () => {
  const a = addBook(empty, { title: 'A', subjects: ['x'] }, 1);
  const ab = addBook(a, { title: 'B', subjects: ['x'] }, 2);
  const baseAB = new Set(ab.stars.map((s) => s.id));

  it('first sync on a device (no base) is a union — nothing dropped', () => {
    const local = addBook(empty, { title: 'Local', subjects: ['y'] }, 3);
    expect(titles(mergeLibraries(local, ab, null))).toEqual(['A', 'B', 'Local']);
  });

  it('keeps adds from both sides', () => {
    const local = addBook(ab, { title: 'C', subjects: ['z'] }, 3);
    const remote = addBook(ab, { title: 'D', subjects: ['x'] }, 4);
    expect(titles(mergeLibraries(local, remote, baseAB))).toEqual(['A', 'B', 'C', 'D']);
  });

  it('propagates deletes from either side', () => {
    const localDeletedA = removeBook(ab, ab.stars[0].id);
    expect(titles(mergeLibraries(localDeletedA, ab, baseAB))).toEqual(['B']);
    const remoteDeletedB = removeBook(ab, ab.stars[1].id);
    expect(titles(mergeLibraries(ab, remoteDeletedB, baseAB))).toEqual(['A']);
  });

  it('folds same-subject constellations created on two devices into one', () => {
    const local = addBook(ab, { title: 'C', subjects: ['new'] }, 3);
    const remote = addBook(ab, { title: 'D', subjects: ['new'] }, 4);
    const merged = mergeLibraries(local, remote, baseAB);
    const newConsts = merged.constellations.filter((c) => c.subject === 'new');
    expect(newConsts).toHaveLength(1);
    expect(newConsts[0].count).toBe(2);
    expect(merged.stars.filter((s) => s.subjects[0] === 'new').every((s) => s.constellationId === newConsts[0].id)).toBe(true);
  });
});
