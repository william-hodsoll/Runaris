// Maps a raw row (CSV object or JSON book) to BookInput. Recognizes both
// Runaris's own export shape and common Goodreads column names. A row
// missing a title is flagged, never silently dropped — see
// specs/05-csv-import.md and CLAUDE.md's import convention.
import type { BookInput } from '../model/types';

export type NormaliseResult = { ok: true; book: BookInput } | { ok: false; reason: string; raw: unknown };

function firstNonEmpty(...vals: (string | undefined)[]): string | undefined {
  return vals.find((v) => v !== undefined && v.trim() !== '');
}

function splitSubjects(raw: string | undefined): string[] | undefined {
  if (!raw) return undefined;
  return raw
    .split(/[,;]/)
    .map((s) => s.trim())
    .filter(Boolean);
}

export function normaliseBook(raw: Record<string, unknown>): NormaliseResult {
  const get = (key: string): string | undefined => {
    const v = raw[key];
    return typeof v === 'string' ? v : v != null ? String(v) : undefined;
  };

  // Runaris's own export uses lowercase keys; Goodreads exports use
  // Title-Case column names. Accept both.
  const title = firstNonEmpty(get('title'), get('Title'));
  if (!title) {
    return { ok: false, reason: 'Missing title', raw };
  }

  const author = firstNonEmpty(get('author'), get('Author'));
  const pagesRaw = firstNonEmpty(get('pages'), get('Number of Pages'));
  const pages = pagesRaw ? Number(pagesRaw) : undefined;
  const subjects =
    splitSubjects(get('subjects')) ??
    splitSubjects(get('Bookshelves')) ??
    (get('genre') || get('Genre') ? [get('genre') ?? get('Genre')!] : undefined);

  const book: BookInput = {
    title,
    author: author ?? 'Unknown',
    year: firstNonEmpty(get('year'), get('Year Published'), get('Original Publication Year')),
    genre: firstNonEmpty(get('genre'), get('Genre')),
    subjects: subjects ?? [],
    pages: Number.isFinite(pages) ? pages : undefined,
    isbn: firstNonEmpty(get('isbn'), get('ISBN13'), get('ISBN')),
  };
  return { ok: true, book };
}
