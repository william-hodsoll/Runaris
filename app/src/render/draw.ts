// Core draw loop — ports the essentials of draw() from
// reference/neural_mind.py: clear, breathe, project every star, draw the
// synapse web, draw stars (twinkle), highlight connect-mode set. Pulses and
// other decorative layers are deferred to a later spec (out of scope per
// specs/02-react-vite-port.md).
import type { Library } from '../model/types';
import type { VisualSettings } from '../model/visualSettings';
import { starMatchesSearch } from '../model/search';
import type { Camera } from './camera';
import { project } from './camera';
import { liveStarPos } from './liveStarPos';
import { paletteColor } from './palette';

export type DrawState = {
  library: Library;
  synapses: { a: string; b: string }[];
  camera: Camera;
  renderTime: number;
  hoveredId: string | null;
  selectedId: string | null;
  connectLit: Set<string> | null; // non-null while in connect mode
  visibleIds: Set<string> | null; // non-null while scrubbing the timelapse
  visual: VisualSettings;
  searchQuery: string;
};

const BG = '#F7F1E8';

export function draw(ctx: CanvasRenderingContext2D, w: number, h: number, state: DrawState): void {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, w, h);

  const { visual } = state;
  const constellationIndexById = new Map(state.library.constellations.map((c, i) => [c.id, i]));
  const constellationById = new Map(state.library.constellations.map((c) => [c.id, c]));
  const projectedById = new Map<string, { sx: number; sy: number; persp: number; depth: number }>();
  const starById = new Map(state.library.stars.map((s) => [s.id, s]));

  const filterOn = visual.statusFilter !== 'all';
  const matchesFilter = (starId: string) => starById.get(starId)?.status === visual.statusFilter;
  const searchOn = state.searchQuery !== '';
  const matchesSearch = (starId: string) => {
    const s = starById.get(starId);
    return !!s && starMatchesSearch(s, state.searchQuery);
  };

  for (const star of state.library.stars) {
    if (state.visibleIds && !state.visibleIds.has(star.id)) continue;
    const centre = constellationById.get(star.constellationId);
    if (!centre) continue;
    const live = liveStarPos(star, centre, state.renderTime, visual.gravity, visual.breathing, visual.constellationSpin);
    projectedById.set(star.id, project(live, state.camera, w, h));
  }

  // Synapse web — faint lines within each constellation. Skipped entirely
  // (not dimmed) for stars outside the timelapse cutoff — the cosmos should
  // look like it hasn't happened yet, not like a connect-mode fade.
  if (visual.showSynapses) {
    ctx.lineWidth = 1;
    for (const syn of state.synapses) {
      const a = projectedById.get(syn.a);
      const b = projectedById.get(syn.b);
      if (!a || !b) continue;
      if (filterOn && !(matchesFilter(syn.a) && matchesFilter(syn.b))) continue;
      if (searchOn && !(matchesSearch(syn.a) && matchesSearch(syn.b))) continue;
      const inConnectMode = state.connectLit !== null;
      ctx.strokeStyle = inConnectMode ? 'rgba(0,0,0,0.03)' : 'rgba(0,0,0,0.08)';
      ctx.beginPath();
      ctx.moveTo(a.sx, a.sy);
      ctx.lineTo(b.sx, b.sy);
      ctx.stroke();
    }
  }

  // Connect-mode highlight lines from the selected star to everything lit.
  if (state.connectLit && state.selectedId) {
    const src = projectedById.get(state.selectedId);
    if (src) {
      ctx.strokeStyle = 'rgba(90,115,64,0.55)';
      ctx.lineWidth = 1.4;
      for (const id of state.connectLit) {
        const p = projectedById.get(id);
        if (!p) continue;
        ctx.beginPath();
        ctx.moveTo(src.sx, src.sy);
        ctx.lineTo(p.sx, p.sy);
        ctx.stroke();
      }
    }
  }

  // Stars, back-to-front by depth so nearer ones draw on top.
  const ordered = state.library.stars
    .map((s) => ({ star: s, proj: projectedById.get(s.id) }))
    .filter((x): x is { star: typeof state.library.stars[number]; proj: NonNullable<typeof x.proj> } => !!x.proj)
    .sort((x, y) => y.proj.depth - x.proj.depth);

  for (const { star, proj } of ordered) {
    const twinkle = 0.85 + 0.15 * Math.sin(state.renderTime * star.speed + star.phase);
    const dimmedByConnect = state.connectLit !== null && !state.connectLit.has(star.id) && star.id !== state.selectedId;
    const dimmedByFilter = filterOn && !matchesFilter(star.id);
    const dimmedBySearch = searchOn && !matchesSearch(star.id);
    const dimmed = dimmedByConnect || dimmedByFilter || dimmedBySearch;
    const radius = Math.max(1, star.size * 3.2 * proj.persp * visual.starBrightness);
    const constellationIndex = constellationIndexById.get(star.constellationId) ?? 0;

    ctx.globalAlpha = dimmed ? 0.15 : twinkle;
    ctx.fillStyle =
      star.id === state.hoveredId || star.id === state.selectedId
        ? '#2b2b26'
        : paletteColor(star, constellationIndex, visual.paletteMode);
    ctx.beginPath();
    ctx.arc(proj.sx, proj.sy, radius, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
}

/** Attaches projected screen positions for hit-testing — call once per
 * frame and reuse for both draw() and pickStar() to avoid re-projecting. */
export function projectAll(
  library: Library,
  camera: Camera,
  renderTime: number,
  w: number,
  h: number,
  visual?: VisualSettings,
): Map<string, { sx: number; sy: number; depth: number }> {
  const constellationById = new Map(library.constellations.map((c) => [c.id, c]));
  const out = new Map<string, { sx: number; sy: number; depth: number }>();
  for (const star of library.stars) {
    const centre = constellationById.get(star.constellationId);
    if (!centre) continue;
    const live = liveStarPos(star, centre, renderTime, visual?.gravity, visual?.breathing, visual?.constellationSpin);
    const p = project(live, camera, w, h);
    out.set(star.id, { sx: p.sx, sy: p.sy, depth: p.depth });
  }
  return out;
}
