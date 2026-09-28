// Pure aggregate stats over a Library — ports renderInsights() from
// reference/neural_mind.py. No rendering; feeds InsightsPanel.
import type { Library } from './types';

export function countBySubject(library: Library): Map<string, number> {
  const counts = new Map<string, number>();
  for (const s of library.stars) {
    for (const subj of s.subjects) {
      counts.set(subj, (counts.get(subj) ?? 0) + 1);
    }
  }
  return counts;
}

export function countByGenre(library: Library): Map<string, number> {
  const counts = new Map<string, number>();
  for (const s of library.stars) {
    if (!s.genre) continue;
    counts.set(s.genre, (counts.get(s.genre) ?? 0) + 1);
  }
  return counts;
}

export function countByStatus(library: Library): Map<string, number> {
  const counts = new Map<string, number>();
  for (const s of library.stars) {
    if (!s.status) continue;
    counts.set(s.status, (counts.get(s.status) ?? 0) + 1);
  }
  return counts;
}

export function totalPages(library: Library): number {
  return library.stars.reduce((sum, s) => sum + (s.pages || 0), 0);
}

export function averagePages(library: Library): number {
  const withPages = library.stars.filter((s) => s.pages > 0);
  if (withPages.length === 0) return 0;
  return totalPages({ ...library, stars: withPages }) / withPages.length;
}

export function booksPerYear(library: Library): Map<number, number> {
  const counts = new Map<number, number>();
  for (const s of library.stars) {
    const year = new Date(s.dateAdded).getFullYear();
    counts.set(year, (counts.get(year) ?? 0) + 1);
  }
  return counts;
}

function topN(counts: Map<string, number>, n: number): [string, number][] {
  return Array.from(counts.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, n);
}

export function topSubjects(library: Library, n = 5): [string, number][] {
  return topN(countBySubject(library), n);
}
