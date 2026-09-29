import { describe, expect, it } from 'vitest';
import { starMatchesSearch } from '../search';
import type { BookStar } from '../types';

const base: BookStar = {
  id: 's1',
  title: 'The Name of the Rose',
  author: 'Umberto Eco',
  year: '1980',
  genre: 'Mystery',
  subjects: ['semiotics', 'medieval'],
  pages: 500,
  dateAdded: 0,
  constellationId: 'c1',
  position: { x: 0, y: 0, z: 0 },
  offset: { x: 0, y: 0, z: 0 },
  size: 1,
  color: '#fff',
  phase: 0,
  speed: 1,
};

describe('starMatchesSearch', () => {
  it('matches an empty query against everything', () => {
    expect(starMatchesSearch(base, '')).toBe(true);
  });

  it('matches title, author, genre, and subjects case-insensitively', () => {
    expect(starMatchesSearch(base, 'name of the')).toBe(true);
    expect(starMatchesSearch(base, 'ECO')).toBe(true);
    expect(starMatchesSearch(base, 'mystery')).toBe(true);
    expect(starMatchesSearch(base, 'Semiotics')).toBe(true);
  });

  it('does not match unrelated text', () => {
    expect(starMatchesSearch(base, 'dune')).toBe(false);
  });
});
