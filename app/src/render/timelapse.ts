// Pure functions behind the timelapse feature — ports the bounds/filter
// logic from v1's tlBounds()/the dateAdded cutoff check in draw().
// specs/07-timelapse.md.
import type { Library } from '../model/types';

export function timelapseBounds(library: Library): { min: number; max: number } | null {
  if (library.stars.length === 0) return null;
  let min = Infinity;
  let max = -Infinity;
  for (const s of library.stars) {
    if (s.dateAdded < min) min = s.dateAdded;
    if (s.dateAdded > max) max = s.dateAdded;
  }
  return { min, max };
}

/** Stars visible at a given point in the timelapse (dateAdded <= cutoff). */
export function filterVisible(library: Library, cutoff: number): Set<string> {
  const visible = new Set<string>();
  for (const s of library.stars) {
    if (s.dateAdded <= cutoff) visible.add(s.id);
  }
  return visible;
}

export function formatTimelapseDate(timestamp: number): string {
  return new Date(timestamp).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
}
