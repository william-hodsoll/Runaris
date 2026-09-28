// Customize-panel state — see specs/11-customize-panel.md. Not library data
// (no IndexedDB, no schema version): a small synchronous localStorage blob,
// same pattern as v1's `app.visual` but split from the async library store.
export type VisualSettings = {
  statusFilter: 'all' | 'reading' | 'finished' | 'unread' | 'abandoned';
  gravity: number;
  starBrightness: number;
  breathing: boolean;
  showSynapses: boolean;
  constellationSpin: number;
  rotationSpeed: number;
  paletteMode: 'default' | 'warm' | 'cool' | 'mono';
};

export const DEFAULT_VISUAL_SETTINGS: VisualSettings = {
  statusFilter: 'all',
  gravity: 1,
  starBrightness: 1,
  breathing: true,
  showSynapses: true,
  constellationSpin: 1,
  rotationSpeed: 0,
  paletteMode: 'default',
};

const STORAGE_KEY = 'neuralMind.visual.v1';

export function loadVisualSettings(): VisualSettings {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...DEFAULT_VISUAL_SETTINGS };
    return { ...DEFAULT_VISUAL_SETTINGS, ...JSON.parse(raw) };
  } catch {
    return { ...DEFAULT_VISUAL_SETTINGS };
  }
}

export function saveVisualSettings(settings: VisualSettings): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  } catch {
    // best-effort, matches localStorage.ts's saveLibrary fallback behavior
  }
}
