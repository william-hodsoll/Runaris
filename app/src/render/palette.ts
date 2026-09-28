// Ports applyPalette()/PALETTE_MAPS from reference/neural_mind.py L4030-4051,
// as a pure per-frame lookup instead of a stateful mutation — no origColor
// field needed, 'default' just passes the stored color through.
import type { BookStar } from '../model/types';
import type { VisualSettings } from '../model/visualSettings';

const PALETTE_MAPS: Record<'warm' | 'cool' | 'mono', string[]> = {
  warm: ['#9A6C60', '#D4A93E', '#B99D84', '#5A3A2C', '#C4A398', '#898270', '#B08A67', '#8E7F78'],
  cool: ['#6F838C', '#5F6C78', '#45505A', '#2F3B4B', '#7A8078', '#8E9CA3', '#5A7340', '#414B38'],
  mono: ['#2F3B4B', '#45505A', '#5C635B', '#7A7F76', '#8E8E88', '#6B6B6B', '#4F4A45', '#A5A79A'],
};

export function paletteColor(star: BookStar, constellationIndex: number, mode: VisualSettings['paletteMode']): string {
  if (mode === 'default') return star.color;
  const pool = PALETTE_MAPS[mode];
  return pool[constellationIndex % pool.length];
}
