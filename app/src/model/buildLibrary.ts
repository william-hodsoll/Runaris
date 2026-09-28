// Ports build_mind() from reference/neural_mind.py: groups books by primary
// subject into constellations distributed over a sphere (Fibonacci lattice +
// shuffled radius so cluster size doesn't correlate with input order), then
// scatters each book as a star in a fuzzy ball around its constellation.
import type { BookInput, BookStar, Constellation, Library } from './types';
import { makeRng, shuffle, uniform } from './rng';

const SPHERE_R = 380;
const DRIFT = 60;
const GOLDEN = Math.PI * (1 + Math.sqrt(5));

const EARTH_COLORS = [
  '#5A7340', '#9A6C60', '#6F838C', '#D4A93E', '#414B38', '#8E7F78',
  '#5F6C78', '#B99D84', '#5A3A2C', '#7A8078', '#4D6142', '#898270',
];

function sizeFromPages(pages: number, pMin: number, pMax: number, rng: () => number): number {
  if (!pages || pMax === pMin) return uniform(rng, 1.0, 1.4);
  const t = (pages - pMin) / (pMax - pMin);
  const base = 0.7 + t * 1.5;
  return base + uniform(rng, -0.08, 0.08);
}

let idCounter = 0;
function nextId(prefix: string): string {
  idCounter += 1;
  return `${prefix}-${idCounter}`;
}

export function buildLibrary(books: BookInput[], seed?: number): Library {
  const rng = makeRng(seed ?? Date.now());

  const bySubject = new Map<string, BookInput[]>();
  for (const b of books) {
    const primary = b.subjects && b.subjects.length > 0 ? b.subjects[0] : 'general';
    const list = bySubject.get(primary) ?? [];
    list.push(b);
    bySubject.set(primary, list);
  }

  const subjects = Array.from(bySubject.keys());
  const nSubj = subjects.length;
  if (nSubj === 0) return { version: 1, stars: [], constellations: [] };

  const radialBins = shuffle(
    rng,
    Array.from({ length: nSubj }, (_, i) => (i + 0.5) / nSubj),
  );
  const latticeSlots = shuffle(rng, Array.from({ length: nSubj }, (_, i) => i));

  const constellations: Constellation[] = subjects.map((subject, i) => {
    const slot = latticeSlots[i];
    let tLat = (slot + 0.5) / nSubj;
    let phi = Math.acos(1 - 2 * tLat);
    let theta = GOLDEN * slot;
    phi += uniform(rng, -0.06, 0.06);
    theta += uniform(rng, -0.06, 0.06);

    let radialT = 0.2 + 0.78 * radialBins[i];
    radialT += uniform(rng, -0.05, 0.05);
    radialT = Math.max(0.18, Math.min(1.0, radialT));
    const r = SPHERE_R * radialT;

    const position = {
      x: r * Math.sin(phi) * Math.cos(theta),
      y: r * Math.sin(phi) * Math.sin(theta),
      z: r * Math.cos(phi),
    };
    const color = EARTH_COLORS[i % EARTH_COLORS.length];

    const axPhi = uniform(rng, 0, Math.PI);
    const axTheta = uniform(rng, 0, 2 * Math.PI);
    const axis = {
      x: Math.sin(axPhi) * Math.cos(axTheta),
      y: Math.sin(axPhi) * Math.sin(axTheta),
      z: Math.cos(axPhi),
    };
    const spinSpeed = uniform(rng, 0.05, 0.18) * (rng() < 0.5 ? -1 : 1);
    const spinPhase = uniform(rng, 0, 2 * Math.PI);

    return {
      id: nextId('const'),
      subject,
      position,
      color,
      axis,
      spinSpeed,
      spinPhase,
      count: bySubject.get(subject)!.length,
    };
  });

  const allPages = books
    .map((b) => b.pages)
    .filter((p): p is number => typeof p === 'number' && p > 0);
  const pMin = allPages.length ? Math.min(...allPages) : 0;
  const pMax = allPages.length ? Math.max(...allPages) : 0;

  const stars: BookStar[] = [];
  subjects.forEach((subject, ci) => {
    const centre = constellations[ci];
    for (const b of bySubject.get(subject)!) {
      const u = uniform(rng, -1, 1);
      const theta = uniform(rng, 0, 2 * Math.PI);
      const sqrt1mu2 = Math.sqrt(Math.max(0, 1 - u * u));
      const dx = Math.cos(theta) * sqrt1mu2;
      const dy = Math.sin(theta) * sqrt1mu2;
      const dz = u;
      const r = DRIFT * Math.pow(rng(), 1.3);
      const offset = { x: dx * r, y: dy * r, z: dz * r };
      const position = {
        x: centre.position.x + offset.x,
        y: centre.position.y + offset.y,
        z: centre.position.z + offset.z,
      };

      stars.push({
        id: nextId('star'),
        title: b.title || 'Untitled',
        author: b.author || 'Unknown',
        year: b.year || '',
        genre: b.genre || '',
        subjects: b.subjects || [],
        pages: b.pages || 0,
        isbn: b.isbn,
        coverUrl: b.coverUrl,
        status: b.status,
        dateAdded: 0, // filled below
        constellationId: centre.id,
        position,
        offset,
        size: sizeFromPages(b.pages || 0, pMin, pMax, rng),
        color: centre.color,
        phase: uniform(rng, 0, 2 * Math.PI),
        speed: uniform(rng, 0.6, 1.6),
      });
    }
  });

  // Synthesize dateAdded spread across the last 5 years, oldest first, so a
  // timelapse (future spec) can scrub from a single star to the full cosmos.
  const nowMs = Date.now();
  const fiveYearsMs = 5 * 365 * 24 * 60 * 60 * 1000;
  const n = stars.length;
  stars.forEach((star, i) => {
    const frac = (i + 1) / Math.max(1, n);
    const jitter = uniform(rng, -3, 3) * 24 * 60 * 60 * 1000;
    star.dateAdded = nowMs - Math.floor(fiveYearsMs * (1 - frac)) - Math.floor(jitter);
  });

  return { version: 1, stars, constellations };
}
