// Ports exportLibrary() from reference/neural_mind.py — downloads the
// current library as JSON. Uses the stars array directly (title/author/
// subjects/etc.), matching the shape importLibrary.ts expects back in.
import type { Library } from '../model/types';

export function exportLibraryToJson(library: Library): string {
  return JSON.stringify(library.stars, null, 2);
}

export function downloadLibraryExport(library: Library): void {
  const blob = new Blob([exportLibraryToJson(library)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'runaris-library.json';
  a.click();
  URL.revokeObjectURL(url);
}
