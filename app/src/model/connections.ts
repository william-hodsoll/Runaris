// Ports the connection logic from reference/neural_mind.py: `computeConnections`
// (full shared-subject/genre/author graph, used for connect-mode + the pulse
// pool) and the per-constellation nearest-neighbor "synapse" web built in
// build_mind(). Connections are always DERIVED, never stored — see
// specs/02-react-vite-port.md "Data model".
import type { BookStar, Edge, Library, Synapse } from './types';

function shareSubject(a: BookStar, b: BookStar): boolean {
  const aSubs = new Set(a.subjects.map((s) => s.toLowerCase()));
  return b.subjects.some((s) => aSubs.has(s.toLowerCase()));
}

function shares(a: BookStar, b: BookStar): boolean {
  if (shareSubject(a, b)) return true;
  if (a.genre && a.genre.toLowerCase() === b.genre.toLowerCase()) return true;
  if (a.author && a.author.toLowerCase() === b.author.toLowerCase()) return true;
  return false;
}

/** Full shared-attribute graph — the pool pulses are drawn from. */
export function deriveEdges(library: Library): Edge[] {
  const { stars } = library;
  const edges: Edge[] = [];
  for (let i = 0; i < stars.length; i++) {
    for (let j = i + 1; j < stars.length; j++) {
      if (shares(stars[i], stars[j])) {
        edges.push({ a: stars[i].id, b: stars[j].id });
      }
    }
  }
  return edges;
}

/** Everything connected to `sourceId` — powers connect mode. */
export function deriveConnectionsFor(library: Library, sourceId: string): Set<string> {
  const lit = new Set<string>();
  const src = library.stars.find((s) => s.id === sourceId);
  if (!src) return lit;
  for (const s of library.stars) {
    if (s.id === sourceId) continue;
    if (shares(src, s)) lit.add(s.id);
  }
  return lit;
}

/** Sparse always-visible web: each star links to its 1-2 nearest neighbors
 * in the same constellation (Euclidean, on the static placement position). */
export function deriveSynapses(library: Library): Synapse[] {
  const byConstellation = new Map<string, BookStar[]>();
  for (const s of library.stars) {
    const list = byConstellation.get(s.constellationId) ?? [];
    list.push(s);
    byConstellation.set(s.constellationId, list);
  }

  const seen = new Set<string>();
  const synapses: Synapse[] = [];
  for (const group of byConstellation.values()) {
    const m = group.length;
    if (m < 2) continue;
    const k = m <= 3 ? 1 : 2;
    for (let ai = 0; ai < m; ai++) {
      const a = group[ai];
      const dists = group
        .map((b, bi) => ({ b, bi }))
        .filter(({ bi }) => bi !== ai)
        .map(({ b }) => ({
          b,
          d2:
            (a.position.x - b.position.x) ** 2 +
            (a.position.y - b.position.y) ** 2 +
            (a.position.z - b.position.z) ** 2,
        }))
        .sort((x, y) => x.d2 - y.d2);
      for (const { b } of dists.slice(0, k)) {
        const [x, y] = a.id < b.id ? [a.id, b.id] : [b.id, a.id];
        const key = `${x}|${y}`;
        if (seen.has(key)) continue;
        seen.add(key);
        synapses.push({ a: x, b: y });
      }
    }
  }
  return synapses;
}
