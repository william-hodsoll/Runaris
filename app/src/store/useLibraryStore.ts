// Zustand store — holds Library + UI mode for React chrome (tooltip, HUD).
// The render loop (CanvasHost) reads a snapshot via getState() each frame
// rather than subscribing through React, so 60fps isn't gated on React
// re-renders — see CLAUDE.md "Canvas" note.
import { create } from 'zustand';
import { addBook as addBookModel, removeBook as removeBookModel } from '../model/addBook';
import { buildLibrary } from '../model/buildLibrary';
import { deriveSynapses } from '../model/connections';
import type { BookInput, Library, Synapse } from '../model/types';
import { loadLibrary, saveLibrary } from '../persistence';
import { trackEvent } from '../analytics/analytics';
import { DEFAULT_VISUAL_SETTINGS, loadVisualSettings, saveVisualSettings, type VisualSettings } from '../model/visualSettings';

type Mode = { kind: 'idle' } | { kind: 'tooltip'; starId: string } | { kind: 'connect'; starId: string };
export type AddBookSource = 'manual' | 'isbn';

type LibraryStore = {
  library: Library;
  synapses: Synapse[];
  mode: Mode;
  warning: string | null;
  hydrated: boolean;
  timelapseCutoff: number | null;
  visual: VisualSettings;
  setVisual: (partial: Partial<VisualSettings>) => void;
  resetVisual: () => void;
  frozen: boolean;
  toggleFrozen: () => void;
  hydrate: () => Promise<void>;
  loadDemo: (books: BookInput[], seed?: number) => void;
  addBook: (book: BookInput, source?: AddBookSource) => void;
  addBooks: (books: BookInput[], flagged?: number) => void;
  removeBook: (starId: string) => void;
  selectStar: (starId: string) => void;
  enterConnectMode: (starId: string) => void;
  exitConnectMode: () => void;
  deselect: () => void;
  setTimelapseCutoff: (cutoff: number | null) => void;
  exitTimelapse: () => void;
};

function persist(library: Library, set: (partial: Partial<LibraryStore>) => void): void {
  void saveLibrary(library).then((result) => {
    if (!result.ok) set({ warning: `Could not save your library: ${result.error}` });
  });
}

export const useLibraryStore = create<LibraryStore>((set, get) => ({
  library: { version: 1, stars: [], constellations: [] },
  synapses: [],
  mode: { kind: 'idle' },
  warning: null,
  hydrated: false,
  timelapseCutoff: null,
  visual: loadVisualSettings(),

  setVisual: (partial) => {
    const visual = { ...get().visual, ...partial };
    set({ visual });
    saveVisualSettings(visual);
  },
  resetVisual: () => {
    set({ visual: { ...DEFAULT_VISUAL_SETTINGS } });
    saveVisualSettings(DEFAULT_VISUAL_SETTINGS);
  },
  frozen: false,
  toggleFrozen: () => set((s) => ({ frozen: !s.frozen })),

  hydrate: async () => {
    const { library, warning } = await loadLibrary();
    set({ library, synapses: deriveSynapses(library), warning: warning ?? null, hydrated: true });
  },

  loadDemo: (books, seed) => {
    const library = buildLibrary(books, seed);
    set({ library, synapses: deriveSynapses(library), mode: { kind: 'idle' } });
    persist(library, set);
    trackEvent('demo_loaded', { count: books.length });
  },

  addBook: (book, source = 'manual') => {
    const library = addBookModel(get().library, book);
    set({ library, synapses: deriveSynapses(library) });
    persist(library, set);
    trackEvent('book_added');
    trackEvent(source === 'isbn' ? 'book_added_isbn' : 'book_added_manual');
  },

  addBooks: (books, flagged = 0) => {
    let library = get().library;
    for (const book of books) library = addBookModel(library, book);
    set({ library, synapses: deriveSynapses(library) });
    persist(library, set);
    trackEvent('import_completed', { count: books.length, flagged });
  },

  removeBook: (starId) => {
    const library = removeBookModel(get().library, starId);
    set({ library, synapses: deriveSynapses(library), mode: { kind: 'idle' } });
    persist(library, set);
    trackEvent('book_removed');
  },

  selectStar: (starId) => set({ mode: { kind: 'tooltip', starId } }),
  enterConnectMode: (starId) => {
    set({ mode: { kind: 'connect', starId } });
    trackEvent('connect_mode_entered');
  },
  exitConnectMode: () => set({ mode: { kind: 'idle' } }),
  deselect: () => set({ mode: { kind: 'idle' } }),

  setTimelapseCutoff: (cutoff) => set({ timelapseCutoff: cutoff }),
  exitTimelapse: () => set({ timelapseCutoff: null }),
}));
