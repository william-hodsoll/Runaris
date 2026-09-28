import { describe, expect, it } from 'vitest';
import { normaliseBook } from '../normaliseBook';

describe('normaliseBook', () => {
  it('maps Goodreads-shaped columns to BookInput', () => {
    const result = normaliseBook({
      Title: 'Dune',
      Author: 'Frank Herbert',
      'Number of Pages': '412',
      Bookshelves: 'sci-fi, favorites',
    });
    expect(result).toEqual({
      ok: true,
      book: {
        title: 'Dune',
        author: 'Frank Herbert',
        year: undefined,
        genre: undefined,
        subjects: ['sci-fi', 'favorites'],
        pages: 412,
        isbn: undefined,
      },
    });
  });

  it('maps Runaris export-shaped columns to BookInput', () => {
    const result = normaliseBook({ title: 'Dune', author: 'Frank Herbert', subjects: 'sci-fi' });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.book.title).toBe('Dune');
      expect(result.book.subjects).toEqual(['sci-fi']);
    }
  });

  it('flags a row with no title instead of dropping it', () => {
    const result = normaliseBook({ Author: 'Nobody' });
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.reason).toBe('Missing title');
      expect(result.raw).toEqual({ Author: 'Nobody' });
    }
  });

  it('defaults a missing author to Unknown rather than failing', () => {
    const result = normaliseBook({ Title: 'Anonymous Work' });
    expect(result.ok).toBe(true);
    if (result.ok) expect(result.book.author).toBe('Unknown');
  });
});
