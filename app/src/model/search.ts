// Ported verbatim from v1's starMatchesSearch (reference/neural_mind.py:1276).
// Case-insensitive substring match across title, author, genre, subjects.
import type { BookStar } from './types';

export function starMatchesSearch(star: BookStar, query: string): boolean {
  if (!query) return true;
  const q = query.toLowerCase();
  if (star.title.toLowerCase().includes(q)) return true;
  if (star.author.toLowerCase().includes(q)) return true;
  if (star.genre.toLowerCase().includes(q)) return true;
  return star.subjects.some((s) => s.toLowerCase().includes(q));
}
