import { describe, expect, it } from 'vitest';
import { parseCsv } from '../parseCsv';

describe('parseCsv', () => {
  it('parses simple rows into header-keyed objects', () => {
    const rows = parseCsv('Title,Author\nDune,Frank Herbert\n1984,George Orwell');
    expect(rows).toEqual([
      { Title: 'Dune', Author: 'Frank Herbert' },
      { Title: '1984', Author: 'George Orwell' },
    ]);
  });

  it('handles quoted fields containing commas', () => {
    const rows = parseCsv('Title,Author\n"Smith, John: A Life",Jane Doe');
    expect(rows[0].Title).toBe('Smith, John: A Life');
    expect(rows[0].Author).toBe('Jane Doe');
  });

  it('handles escaped double quotes inside a quoted field', () => {
    const rows = parseCsv('Title,Note\n"He said ""hi""",fine');
    expect(rows[0].Title).toBe('He said "hi"');
  });

  it('returns an empty array for empty input', () => {
    expect(parseCsv('')).toEqual([]);
  });
});
