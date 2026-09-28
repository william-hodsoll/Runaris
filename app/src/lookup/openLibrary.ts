// Ports v1's OpenLibrary ISBN lookup to a typed adapter. Isolated here so a
// provider swap (e.g. Google Books) later doesn't touch UI code — see
// CLAUDE.md "External lookup" and specs/04-isbn-lookup.md.
import type { BookInput } from '../model/types';

type OpenLibraryAuthor = { name?: string };
type OpenLibraryCover = { large?: string; medium?: string };
type OpenLibraryBookData = {
  title?: string;
  authors?: OpenLibraryAuthor[];
  subjects?: { name: string }[];
  cover?: OpenLibraryCover;
  publish_date?: string;
  number_of_pages?: number;
};

function normaliseIsbn(isbn: string): string {
  return isbn.replace(/[^0-9Xx]/g, '');
}

export async function lookupByIsbn(rawIsbn: string): Promise<BookInput | null> {
  const isbn = normaliseIsbn(rawIsbn);
  if (!isbn) return null;

  const url = `https://openlibrary.org/api/books?bibkeys=ISBN:${encodeURIComponent(isbn)}&format=json&jscmd=data`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`OpenLibrary request failed with status ${res.status}`);
  }
  const data = (await res.json()) as Record<string, OpenLibraryBookData>;
  const entry = data[`ISBN:${isbn}`];
  if (!entry || !entry.title) return null;

  return {
    title: entry.title,
    author: entry.authors?.[0]?.name ?? 'Unknown',
    year: entry.publish_date,
    subjects: entry.subjects?.map((s) => s.name) ?? [],
    pages: entry.number_of_pages,
    coverUrl: entry.cover?.large ?? entry.cover?.medium,
    isbn,
  };
}
