// Store-level sync behavior — see specs/14-auth-and-sync.md and
// specs/17-sync-integrity.md. Supabase I/O is mocked; merge logic is real.
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { buildLibrary } from '../../model/buildLibrary';
import type { Library } from '../../model/types';
import type { SyncBase } from '../../persistence/sync';

type FakeSession = { user: { id: string } } | null;
let sessionListener: ((session: FakeSession) => void) | null = null;
let initialSession: FakeSession = null;

vi.mock('../../auth/session', () => ({
  initSession: vi.fn(async () => initialSession),
  onSessionChange: vi.fn((cb: (s: FakeSession) => void) => {
    sessionListener = cb;
    return () => {};
  }),
  signInWithMagicLink: vi.fn(),
  signOut: vi.fn(),
}));

const io: {
  local: Library;
  remote: Library | null;
  pullFails: boolean;
  base: SyncBase | null;
  pushed: Library[];
} = { local: { version: 1, stars: [], constellations: [] }, remote: null, pullFails: false, base: null, pushed: [] };

vi.mock('../../persistence/sync', () => ({
  pullRemoteLibrary: vi.fn(async () => (io.pullFails ? { ok: false, error: 'down' } : { ok: true, library: io.remote })),
  pushLibrary: vi.fn(async (_u: string, lib: Library) => {
    io.pushed.push(lib);
    io.remote = lib;
    return { ok: true };
  }),
  loadSyncBase: () => io.base,
  saveSyncBase: (b: SyncBase) => {
    io.base = b;
  },
}));

vi.mock('../../persistence', () => ({
  loadLibrary: async () => ({ library: io.local }),
  saveLibrary: async (lib: Library) => {
    io.local = lib;
    return { ok: true };
  },
}));

import { useLibraryStore } from '../useLibraryStore';

const titles = () => useLibraryStore.getState().library.stars.map((s) => s.title).sort();

describe('store sync', () => {
  beforeEach(() => {
    sessionListener = null;
    initialSession = null;
    io.local = { version: 1, stars: [], constellations: [] };
    io.remote = buildLibrary([{ title: 'From Other Browser', subjects: ['x'] }], 1);
    io.pullFails = false;
    io.base = null;
    io.pushed = [];
    useLibraryStore.setState({
      library: { version: 1, stars: [], constellations: [] },
      synapses: [],
      session: null,
      warning: null,
      hydrated: false,
    });
  });

  it('pulls the remote library when sign-in completes after hydrate (magic-link redirect path)', async () => {
    await useLibraryStore.getState().hydrate();
    expect(titles()).toEqual([]);
    sessionListener!({ user: { id: 'u1' } });
    await vi.waitFor(() => expect(titles()).toEqual(['From Other Browser']));
  });

  it('first sign-in on a device with local books uploads them instead of overwriting either side', async () => {
    io.local = buildLibrary([{ title: 'Local Only', subjects: ['y'] }], 2);
    initialSession = { user: { id: 'u1' } };
    await useLibraryStore.getState().hydrate();
    expect(titles()).toEqual(['From Other Browser', 'Local Only']);
    expect(io.remote!.stars.map((s) => s.title).sort()).toEqual(['From Other Browser', 'Local Only']);
  });

  it('a failed pull never drops local books', async () => {
    io.local = buildLibrary([{ title: 'Local Only', subjects: ['y'] }], 2);
    io.pullFails = true;
    io.base = { userId: 'u1', starIds: ['something-else'] };
    initialSession = { user: { id: 'u1' } };
    await useLibraryStore.getState().hydrate();
    expect(titles()).toEqual(['Local Only']);
    expect(useLibraryStore.getState().warning).toMatch(/Could not sync/);
    expect(io.pushed).toHaveLength(0);
  });

  it('account switch takes the new account as-is, without bleeding the previous account in', async () => {
    io.local = buildLibrary([{ title: 'Previous Account Book', subjects: ['y'] }], 3);
    io.base = { userId: 'previous-user', starIds: [] };
    initialSession = { user: { id: 'u2' } };
    await useLibraryStore.getState().hydrate();
    expect(titles()).toEqual(['From Other Browser']);
    expect(io.pushed.every((l) => !l.stars.some((s) => s.title === 'Previous Account Book'))).toBe(true);
  });
});
