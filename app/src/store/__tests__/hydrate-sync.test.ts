// Regression test for a real bug: signing in normally completes AFTER
// hydrate() has already run (via the magic-link redirect firing
// onSessionChange), not via a session that already existed at load time.
// The one-shot reconcile inside hydrate() only covered the latter case, so a
// book added on one browser never appeared after signing in on another. See
// specs/14-auth-and-sync.md and the intent.md decision fixing this.
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { buildLibrary } from '../../model/buildLibrary';
import type { Library } from '../../model/types';

let sessionListener: ((session: { user: { id: string } } | null) => void) | null = null;
let initialSession: { user: { id: string } } | null = null;

vi.mock('../../auth/session', () => ({
  initSession: vi.fn(async () => initialSession),
  onSessionChange: vi.fn((cb: (s: { user: { id: string } } | null) => void) => {
    sessionListener = cb;
    return () => {};
  }),
  signInWithMagicLink: vi.fn(),
  signOut: vi.fn(),
}));

const remoteLibrary: Library = buildLibrary([{ title: 'Synced From Other Browser', subjects: ['x'] }], 1);

vi.mock('../../persistence/sync', () => ({
  getLocalUpdatedAt: () => 0,
  markLocalUpdated: vi.fn(),
  pullRemoteLibrary: vi.fn(async () => ({ library: remoteLibrary, updatedAt: Date.now() })),
  pushLibrary: vi.fn(async () => ({ ok: true })),
  debouncedPush: vi.fn(),
}));

import { useLibraryStore } from '../useLibraryStore';

describe('hydrate + later sign-in reconciliation', () => {
  beforeEach(() => {
    sessionListener = null;
    initialSession = null;
    useLibraryStore.setState({
      library: { version: 1, stars: [], constellations: [] },
      synapses: [],
      session: null,
      hydrated: false,
    });
  });

  it('pulls the remote library when sign-in completes after hydrate (the magic-link redirect path)', async () => {
    await useLibraryStore.getState().hydrate();
    expect(useLibraryStore.getState().library.stars).toHaveLength(0);
    expect(sessionListener).not.toBeNull();

    // Simulate the magic-link redirect's onAuthStateChange firing later.
    sessionListener!({ user: { id: 'user-1' } });
    await vi.waitFor(() => {
      expect(useLibraryStore.getState().library.stars.map((s) => s.title)).toContain('Synced From Other Browser');
    });
  });
});
