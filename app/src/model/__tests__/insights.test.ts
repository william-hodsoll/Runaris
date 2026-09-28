import { describe, expect, it } from 'vitest';
import { buildLibrary } from '../buildLibrary';
import { averagePages, countByGenre, countByStatus, countBySubject, topSubjects, totalPages } from '../insights';

const fixture = buildLibrary(
  [
    { title: 'A', subjects: ['tech', 'ai'], genre: 'Science', pages: 200 },
    { title: 'B', subjects: ['tech'], genre: 'Science', pages: 400 },
    { title: 'C', subjects: ['fiction'], genre: 'Fiction', pages: 300 },
  ],
  1,
);

describe('insights', () => {
  it('counts books by subject, including books with multiple subjects', () => {
    const counts = countBySubject(fixture);
    expect(counts.get('tech')).toBe(2);
    expect(counts.get('ai')).toBe(1);
    expect(counts.get('fiction')).toBe(1);
  });

  it('counts books by genre', () => {
    const counts = countByGenre(fixture);
    expect(counts.get('Science')).toBe(2);
    expect(counts.get('Fiction')).toBe(1);
  });

  it('sums total pages across the library', () => {
    expect(totalPages(fixture)).toBe(900);
  });

  it('computes average pages only over books that have a page count', () => {
    expect(averagePages(fixture)).toBe(300);
  });

  it('returns 0 average for an empty library, no divide-by-zero', () => {
    expect(averagePages({ version: 1, stars: [], constellations: [] })).toBe(0);
  });

  it('ranks top subjects by count, descending', () => {
    const top = topSubjects(fixture, 2);
    expect(top[0][0]).toBe('tech');
    expect(top[0][1]).toBe(2);
  });

  it('counts books by reading status, ignoring books with no status', () => {
    const lib = buildLibrary(
      [
        { title: 'A', subjects: ['x'], status: 'reading' },
        { title: 'B', subjects: ['x'], status: 'reading' },
        { title: 'C', subjects: ['x'], status: 'finished' },
        { title: 'D', subjects: ['x'] },
      ],
      1,
    );
    const counts = countByStatus(lib);
    expect(counts.get('reading')).toBe(2);
    expect(counts.get('finished')).toBe(1);
    expect(Array.from(counts.values()).reduce((a, b) => a + b, 0)).toBe(3);
  });
});
