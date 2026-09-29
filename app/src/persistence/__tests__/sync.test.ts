// Mocks the Supabase client entirely — no real network in unit tests. See
// specs/17-sync-integrity.md.
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { buildLibrary } from '../../model/buildLibrary';

const state: { row: { library: unknown } | null; fail: boolean } = { row: null, fail: false };

vi.mock('../../auth/supabaseClient', () => ({
  supabase: {
    from: () => ({
      select: () => ({
        eq: () => ({
          maybeSingle: async () =>
            state.fail ? { data: null, error: { message: 'network down' } } : { data: state.row, error: null },
        }),
      }),
      upsert: async (row: { library: unknown }) => {
        state.row = { library: row.library };
        return { error: null };
      },
    }),
  },
}));

import { loadSyncBase, pullRemoteLibrary, pushLibrary, saveSyncBase } from '../sync';

describe('sync I/O', () => {
  beforeEach(() => {
    state.row = null;
    state.fail = false;
    localStorage.clear();
  });

  it('distinguishes "nothing synced yet" from a failed pull', async () => {
    expect(await pullRemoteLibrary('u')).toEqual({ ok: true, library: null });
    state.fail = true;
    expect((await pullRemoteLibrary('u')).ok).toBe(false);
  });

  it('push then pull round-trips the library', async () => {
    const lib = buildLibrary([{ title: 'A', subjects: ['x'] }], 1);
    expect((await pushLibrary('u', lib)).ok).toBe(true);
    expect(await pullRemoteLibrary('u')).toEqual({ ok: true, library: lib });
  });

  it('rejects a malformed remote library instead of merging it', async () => {
    state.row = { library: { nonsense: true } };
    expect((await pullRemoteLibrary('u')).ok).toBe(false);
  });

  it('sync base persists per device', () => {
    expect(loadSyncBase()).toBeNull();
    saveSyncBase({ userId: 'u', starIds: ['a'] });
    expect(loadSyncBase()).toEqual({ userId: 'u', starIds: ['a'] });
  });
});
