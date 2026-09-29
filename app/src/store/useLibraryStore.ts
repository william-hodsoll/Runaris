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
import { loadSyncBase, pullRemoteLibrary, pushLibrary, saveSyncBase } from '../persistence/sync';
import { mergeLibraries, repairDuplicateIds } from '../model/merge';
import { trackEvent } from '../analytics/analytics';
import { DEFAULT_VISUAL_SETTINGS, loadVisualSettings, saveVisualSettings, type VisualSettings } from '../model/visualSettings';
import { initSession, onSessionChange, signInWithMagicLink, signOut as signOutSession } from '../auth/session';
import type { Session } from '@supabase/supabase-js';

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
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  session: Session | null;
  signIn: (email: string) => Promise<{ ok: true } | { ok: false; error: string }>;
  signOut: () => Promise<void>;
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

type Set_ = (partial: Partial<LibraryStore>) => void;
type Get_ = () => LibraryStore;

function saveLocal(library: Library, set: Set_): void {
  void saveLibrary(library).then((result) => {
    if (!result.ok) set({ warning: `Could not save your library: ${result.error}` });
  });
}

// Debounced so a burst of local saves (e.g. a CSV import) is one sync.
let syncTimer: ReturnType<typeof setTimeout> | null = null;
function persist(library: Library, set: Set_, get: Get_): void {
  saveLocal(library, set);
  const session = get().session;
  if (!session) return;
  if (syncTimer) clearTimeout(syncTimer);
  syncTimer = setTimeout(() => void syncNow(session.user.id, get, set), 3000);
}

/** The one sync path: pull -> 3-way merge -> apply locally -> push -> record
 * base. Run on sign-in, after local edits, and on tab focus. See
 * specs/17-sync-integrity.md.
 * ponytail: two devices pushing within the same ~second can still race;
 * upgrade is optimistic concurrency on updated_at. */
let syncing = false;
let resyncQueued = false;
async function syncNow(userId: string, get: Get_, set: Set_): Promise<void> {
  if (syncing) {
    resyncQueued = true;
    return;
  }
  syncing = true;
  try {
    const pulled = await pullRemoteLibrary(userId);
    if (!pulled.ok) {
      set({ warning: `Could not sync your library: ${pulled.error}` });
      return;
    }
    const remote = pulled.library && repairDuplicateIds(pulled.library);
    const base = loadSyncBase();
    // Read local only after the await, and apply before the next await, so
    // an edit made mid-sync is never overwritten.
    const local = get().library;
    let merged: Library;
    if (!remote) merged = local; // nothing synced yet: upload
    else if (base && base.userId !== userId) merged = remote; // account switch: don't bleed the previous account's data in
    else merged = mergeLibraries(local, remote, base ? new Set(base.starIds) : null);

    if (JSON.stringify(merged) !== JSON.stringify(local)) {
      set({ library: merged, synapses: deriveSynapses(merged) });
      saveLocal(merged, set);
    }
    if (!remote || JSON.stringify(merged) !== JSON.stringify(remote)) {
      const pushed = await pushLibrary(userId, merged);
      if (!pushed.ok) {
        set({ warning: `Could not sync your library: ${pushed.error}` });
        return;
      }
    }
    saveSyncBase({ userId, starIds: merged.stars.map((s) => s.id) });
  } finally {
    syncing = false;
    if (resyncQueued) {
      resyncQueued = false;
      void syncNow(userId, get, set);
    }
  }
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
  searchQuery: '',
  setSearchQuery: (query) => set({ searchQuery: query }),

  session: null,
  signIn: (email) => signInWithMagicLink(email),
  signOut: () => signOutSession(),

  hydrate: async () => {
    const loaded = await loadLibrary();
    // Repair ids duplicated by the old per-page-load counter (spec 17 P0-1).
    const library = repairDuplicateIds(loaded.library);
    if (library !== loaded.library) saveLocal(library, set);
    set({ library, synapses: deriveSynapses(library), warning: loaded.warning ?? null, hydrated: true });

    const session = await initSession();
    set({ session });
    // Sign-in normally completes AFTER this initial hydrate (magic-link
    // redirect -> onSessionChange), so sync on every signed-out -> signed-in
    // transition, not only when a session already existed at load.
    onSessionChange((s) => {
      const wasSignedOut = get().session === null;
      set({ session: s });
      if (s && wasSignedOut) void syncNow(s.user.id, get, set);
    });
    // Pick up the other device's changes when this tab regains focus.
    document.addEventListener('visibilitychange', () => {
      const current = get().session;
      if (document.visibilityState === 'visible' && current) void syncNow(current.user.id, get, set);
    });
    if (session) await syncNow(session.user.id, get, set);
  },

  loadDemo: (books, seed) => {
    const library = buildLibrary(books, seed);
    set({ library, synapses: deriveSynapses(library), mode: { kind: 'idle' } });
    persist(library, set, get);
    trackEvent('demo_loaded', { count: books.length });
  },

  addBook: (book, source = 'manual') => {
    const library = addBookModel(get().library, book);
    set({ library, synapses: deriveSynapses(library) });
    persist(library, set, get);
    trackEvent('book_added');
    trackEvent(source === 'isbn' ? 'book_added_isbn' : 'book_added_manual');
  },

  addBooks: (books, flagged = 0) => {
    let library = get().library;
    for (const book of books) library = addBookModel(library, book);
    set({ library, synapses: deriveSynapses(library) });
    persist(library, set, get);
    trackEvent('import_completed', { count: books.length, flagged });
  },

  removeBook: (starId) => {
    const library = removeBookModel(get().library, starId);
    set({ library, synapses: deriveSynapses(library), mode: { kind: 'idle' } });
    persist(library, set, get);
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
