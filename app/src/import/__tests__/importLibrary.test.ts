import { describe, expect, it } from 'vitest';
import { importLibraryFile } from '../importLibrary';
import { buildLibrary } from '../../model/buildLibrary';

describe('importLibraryFile', () => {
  it('parses a Goodreads-shaped CSV, flagging rows with no title', () => {
    const csv = 'Title,Author,Number of Pages\nDune,Frank Herbert,412\n,Nobody,100';
    const result = importLibraryFile(csv, 'goodreads_library_export.csv');
    expect(result.books).toHaveLength(1);
    expect(result.books[0].title).toBe('Dune');
    expect(result.flagged).toHaveLength(1);
    expect(result.flagged[0].reason).toBe('Missing title');
  });

  it('parses a JSON array export', () => {
    const json = JSON.stringify([{ title: 'Dune', author: 'Frank Herbert' }]);
    const result = importLibraryFile(json, 'library.json');
    expect(result.books).toHaveLength(1);
    expect(result.flagged).toHaveLength(0);
  });

  it('round-trips a library exported to JSON: reimporting preserves title/author/subjects', () => {
    const original = buildLibrary(
      [
        { title: 'Dune', author: 'Frank Herbert', subjects: ['sci-fi'] },
        { title: '1984', author: 'George Orwell', subjects: ['classic'] },
      ],
      3,
    );
    const exported = JSON.stringify(original.stars);
    const result = importLibraryFile(exported, 'export.json');
    expect(result.flagged).toHaveLength(0);
    expect(result.books.map((b) => [b.title, b.author, b.subjects])).toEqual(
      original.stars.map((s) => [s.title, s.author, s.subjects]),
    );
  });

  it('throws a clear error for malformed JSON shape', () => {
    expect(() => importLibraryFile(JSON.stringify({ nope: true }), 'x.json')).toThrow();
  });
});
