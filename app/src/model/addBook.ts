// Ports addBookToMind() from reference/neural_mind.py: inserts one book into
// an existing Library live — finds or creates its constellation, places it,
// derives its size from the existing page-count range. Returns a NEW Library
// (immutable) rather than mutating in place, per CLAUDE.md model conventions.
import type { BookInput, BookStar, Constellation, Library } from './types';
import { makeRng, uniform } from './rng';

const PALETTE_POOL = [
  '#9bb5ff', '#7fe1d4', '#ff8a78', '#e8c97f', '#d4a5ff', '#a8e8a3',
  '#c8a4f0', '#ff9ab8', '#9eddff', '#ffd089',
];

// UUIDs, not a module counter: a counter restarts at 0 every page load and
// reissued ids already in the saved library (specs/17-sync-integrity.md P0-1).
function nextId(prefix: string): string {
  return `${prefix}-${crypto.randomUUID()}`;
}

export function addBook(library: Library, book: BookInput, seed?: number): Library {
  const rng = makeRng(seed ?? Date.now());
  const primary = book.subjects && book.subjects.length > 0 ? book.subjects[0] : 'general';

  let centre = library.constellations.find((c) => c.subject === primary);
  const constellations = library.constellations.slice();
  if (!centre) {
    const t = rng();
    const phi = Math.acos(1 - 2 * t);
    const theta = rng() * Math.PI * 2;
    const r = 320 + rng() * 50;
    const color = PALETTE_POOL[Math.floor(rng() * PALETTE_POOL.length)];
    const axU = rng() * 2 - 1;
    const axT = rng() * Math.PI * 2;
    const axS = Math.sqrt(Math.max(0, 1 - axU * axU));
    centre = {
      id: nextId('const'),
      subject: primary,
      position: {
        x: r * Math.sin(phi) * Math.cos(theta),
        y: r * Math.sin(phi) * Math.sin(theta),
        z: r * Math.cos(phi),
      },
      color,
      axis: { x: Math.cos(axT) * axS, y: Math.sin(axT) * axS, z: axU },
      spinSpeed: uniform(rng, 0.05, 0.18) * (rng() < 0.5 ? -1 : 1),
      spinPhase: rng() * Math.PI * 2,
      count: 0,
    };
    constellations.push(centre);
  }

  const u = rng() * 2 - 1;
  const th = rng() * Math.PI * 2;
  const s = Math.sqrt(Math.max(0, 1 - u * u));
  const dist = 60 * Math.pow(rng(), 1.3);
  const offset = { x: Math.cos(th) * s * dist, y: Math.sin(th) * s * dist, z: u * dist };

  const pages = book.pages || 0;
  let size: number;
  if (pages > 0) {
    const known = library.stars.map((st) => st.pages).filter((p) => p > 0);
    const pMin = known.length ? Math.min(...known) : Infinity;
    const pMax = known.length ? Math.max(...known) : 0;
    if (pMax > pMin) {
      const t = Math.max(0, Math.min(1, (pages - pMin) / (pMax - pMin)));
      size = 0.7 + t * 1.5 + (rng() * 0.16 - 0.08);
    } else {
      size = 1.0 + rng() * 0.4;
    }
  } else {
    size = 1.0 + rng() * 0.4;
  }

  const star: BookStar = {
    id: nextId('star'),
    title: book.title || 'Untitled',
    author: book.author || 'Unknown',
    year: book.year || '',
    genre: book.genre || '',
    subjects: book.subjects || [],
    pages,
    isbn: book.isbn,
    coverUrl: book.coverUrl,
    status: book.status,
    dateAdded: Date.now(),
    constellationId: centre.id,
    position: {
      x: centre.position.x + offset.x,
      y: centre.position.y + offset.y,
      z: centre.position.z + offset.z,
    },
    offset,
    size: Math.round(size * 1000) / 1000,
    color: centre.color,
    phase: rng() * 6.28,
    speed: 0.6 + rng() * 1.0,
  };

  const updatedConstellations: Constellation[] = constellations.map((c) =>
    c.id === centre!.id ? { ...c, count: c.count + 1 } : c,
  );

  return {
    version: 1,
    stars: [...library.stars, star],
    constellations: updatedConstellations,
  };
}

export function removeBook(library: Library, starId: string): Library {
  const star = library.stars.find((s) => s.id === starId);
  const stars = library.stars.filter((s) => s.id !== starId);
  if (!star) return { ...library, stars };
  const constellations = library.constellations
    .map((c) => (c.id === star.constellationId ? { ...c, count: Math.max(0, c.count - 1) } : c))
    .filter((c) => c.count > 0 || stars.some((s) => s.constellationId === c.id));
  return { version: 1, stars, constellations };
}
