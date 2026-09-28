import type { BookInput } from '../model/types';
import { parseCsv } from './parseCsv';
import { normaliseBook } from './normaliseBook';

export type ImportResult = {
  books: BookInput[];
  flagged: { reason: string; raw: unknown }[];
};

function parseRawRows(text: string, isJson: boolean): Record<string, unknown>[] {
  if (isJson) {
    const data = JSON.parse(text);
    const list = Array.isArray(data) ? data : Array.isArray(data?.books) ? data.books : null;
    if (!list) throw new Error('JSON must be an array or { "books": [...] }');
    return list as Record<string, unknown>[];
  }
  return parseCsv(text);
}

/** Parses + normalizes an uploaded library file. Never silently drops a row —
 * every row ends up in `books` or `flagged`. See specs/05-csv-import.md. */
export function importLibraryFile(text: string, filename: string): ImportResult {
  const isJson = filename.toLowerCase().endsWith('.json');
  const rawRows = parseRawRows(text, isJson);

  const books: BookInput[] = [];
  const flagged: { reason: string; raw: unknown }[] = [];
  for (const raw of rawRows) {
    const result = normaliseBook(raw);
    if (result.ok) books.push(result.book);
    else flagged.push({ reason: result.reason, raw: result.raw });
  }
  return { books, flagged };
}
