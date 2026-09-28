import { beforeEach, describe, expect, it } from 'vitest';
import { DEFAULT_VISUAL_SETTINGS, loadVisualSettings, saveVisualSettings } from '../visualSettings';

describe('visualSettings persistence', () => {
  beforeEach(() => localStorage.clear());

  it('returns defaults when nothing is stored', () => {
    expect(loadVisualSettings()).toEqual(DEFAULT_VISUAL_SETTINGS);
  });

  it('round-trips a saved value', () => {
    saveVisualSettings({ ...DEFAULT_VISUAL_SETTINGS, gravity: 2, paletteMode: 'warm' });
    const loaded = loadVisualSettings();
    expect(loaded.gravity).toBe(2);
    expect(loaded.paletteMode).toBe('warm');
  });

  it('falls back to defaults on corrupt storage', () => {
    localStorage.setItem('neuralMind.visual.v1', '{not json');
    expect(loadVisualSettings()).toEqual(DEFAULT_VISUAL_SETTINGS);
  });
});
