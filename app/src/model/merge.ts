// Pure library merge + id repair — see specs/17-sync-integrity.md.
import type { BookStar, Constellation, Library } from './types';

const primarySubject = (s: BookStar) => s.subjects[0] ?? 'general';

/** Fold same-subject constellations into one (v1: one constellation per
 * subject), re-point their stars, drop empty constellations, recount. */
function normalize(stars: BookStar[], constellations: Constellation[]): Library {
  const keeperBySubject = new Map<string, Constellation>();
  const remap = new Map<string, Constellation>();
  for (const c of constellations) {
    const keeper = keeperBySubject.get(c.subject);
    if (keeper) remap.set(c.id, keeper);
    else keeperBySubject.set(c.subject, c);
  }
  const outStars = stars.map((s) => {
    const keeper = remap.get(s.constellationId);
    return keeper ? { ...s, constellationId: keeper.id, color: keeper.color } : s;
  });
  const counts = new Map<string, number>();
  for (const s of outStars) counts.set(s.constellationId, (counts.get(s.constellationId) ?? 0) + 1);
  const outConstellations = [...keeperBySubject.values()]
    .filter((c) => counts.has(c.id))
    .map((c) => (c.count === counts.get(c.id) ? c : { ...c, count: counts.get(c.id)! }));
  return { version: 1, stars: outStars, constellations: outConstellations };
}

/** Re-id duplicate star/constellation ids left by the old per-page-load
 * counter, so Remove can't delete two books at once. */
export function repairDuplicateIds(library: Library): Library {
  const variantsById = new Map<string, Constellation[]>();
  const constellations = library.constellations.map((c) => {
    const variants = variantsById.get(c.id);
    if (!variants) {
      variantsById.set(c.id, [c]);
      return c;
    }
    const renamed = { ...c, id: `const-${crypto.randomUUID()}` };
    variants.push(renamed);
    return renamed;
  });

  const seenStars = new Set<string>();
  let changed = constellations.some((c, i) => c !== library.constellations[i]);
  const stars = library.stars.map((s) => {
    let out = s;
    if (seenStars.has(s.id)) out = { ...out, id: `star-${crypto.randomUUID()}` };
    seenStars.add(out.id);
    const variants = variantsById.get(s.constellationId);
    if (variants && variants.length > 1) {
      const match = variants.find((c) => c.subject === primarySubject(s)) ?? variants[0];
      if (match.id !== out.constellationId) out = { ...out, constellationId: match.id };
    }
    if (out !== s) changed = true;
    return out;
  });

  return changed ? normalize(stars, constellations) : library;
}

/** 3-way merge by star id against the id set at last successful sync.
 * No base (first sync on this device) = union, nothing dropped. */
export function mergeLibraries(local: Library, remote: Library, baseIds: Set<string> | null): Library {
  const localIds = new Set(local.stars.map((s) => s.id));
  const remoteIds = new Set(remote.stars.map((s) => s.id));
  // In base but missing on one side = deleted on that side.
  const keep = (id: string) => !baseIds?.has(id) || (localIds.has(id) && remoteIds.has(id));

  const stars = [
    ...local.stars.filter((s) => keep(s.id)),
    ...remote.stars.filter((s) => !localIds.has(s.id) && keep(s.id)),
  ];
  const localConstIds = new Set(local.constellations.map((c) => c.id));
  const constellations = [
    ...local.constellations,
    ...remote.constellations.filter((c) => !localConstIds.has(c.id)),
  ];
  return normalize(stars, constellations);
}
