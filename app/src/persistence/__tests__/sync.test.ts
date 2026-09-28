// Mocks the Supabase client entirely — no real network in unit tests, same
// pattern as indexeddb.test.ts mocking fake-indexeddb. See
// specs/14-auth-and-sync.md.
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { buildLibrary } from '../../model/buildLibrary';

const state: { row: { library: unknown; updated_at: string } | null; upserts: unknown[] } = {
  row: null,
  upserts: [],
};

vi.mock('../../auth/supabaseClient', () => ({
  supabase: {
    from: () => ({
      select: () => ({
        eq: () => ({
          maybeSingle: async () => (state.row ? { data: state.row, error: null } : { data: null, error: null }),
        }),
      }),
      upsert: async (row: { user_id: string; library: unknown; updated_at: string }) => {
        state.upserts.push(row);
        state.row = { library: row.library, updated_at: row.updated_at };
        return { error: null };
      },
    }),
  },
}));

import { pullRemoteLibrary, pushLibrary, getLocalUpdatedAt, markLocalUpdated } from '../sync';

describe('sync', () => {
  beforeEach(() => {
    state.row = null;
    state.upserts = [];
    localStorage.clear();
  });

  it('pullRemoteLibrary returns null when nothing is synced yet', async () => {
    expect(await pullRemoteLibrary('user-1')).toBeNull();
  });

  it('pushLibrary then pullRemoteLibrary round-trips the library and a comparable timestamp', async () => {
    const lib = buildLibrary([{ title: 'A', subjects: ['x'] }], 1);
    const result = await pushLibrary('user-1', lib);
    expect(result.ok).toBe(true);

    const pulled = await pullRemoteLibrary('user-1');
    expect(pulled?.library).toEqual(lib);
    expect(pulled?.updatedAt).toBeGreaterThan(0);
  });

  it('local-updated-at persistence: defaults to 0, then reflects markLocalUpdated', () => {
    expect(getLocalUpdatedAt()).toBe(0);
    markLocalUpdated(12345);
    expect(getLocalUpdatedAt()).toBe(12345);
  });
});
