// Sync I/O over the local IndexedDB store — IndexedDB stays the source of
// truth for rendering/offline use (CLAUDE.md: render loop never blocks on
// network). Decisions are a 3-way merge against a per-device sync base, not
// timestamps (two devices' clocks aren't comparable). See
// specs/17-sync-integrity.md; orchestration lives in the store's syncNow().
import { supabase } from '../auth/supabaseClient';
import type { Library } from '../model/types';
import { validateLibrary } from '../model/validate';

const BASE_KEY = 'neuralMind.syncBase.v1';

/** Star ids the remote held after this device's last successful sync, and
 * which account that was. */
export type SyncBase = { userId: string; starIds: string[] };

export function loadSyncBase(): SyncBase | null {
  try {
    const raw = localStorage.getItem(BASE_KEY);
    return raw ? (JSON.parse(raw) as SyncBase) : null;
  } catch {
    return null;
  }
}

export function saveSyncBase(base: SyncBase): void {
  try {
    localStorage.setItem(BASE_KEY, JSON.stringify(base));
  } catch {
    // best-effort; worst case next sync treats this device as first-sync (union, no drops)
  }
}

/** A failed pull must never look like "remote is empty" — with a base, that
 * would read as "every book was deleted elsewhere". */
export async function pullRemoteLibrary(
  userId: string,
): Promise<{ ok: true; library: Library | null } | { ok: false; error: string }> {
  if (!supabase) return { ok: false, error: 'Sync is not configured.' };
  const { data, error } = await supabase
    .from('libraries')
    .select('library')
    .eq('user_id', userId)
    .maybeSingle();
  if (error) return { ok: false, error: error.message };
  if (!data) return { ok: true, library: null };
  const { library, warning } = validateLibrary(data.library);
  if (warning) return { ok: false, error: 'Synced library had an unexpected shape.' };
  return { ok: true, library };
}

export async function pushLibrary(userId: string, library: Library): Promise<{ ok: true } | { ok: false; error: string }> {
  if (!supabase) return { ok: false, error: 'Sync is not configured.' };
  const { error } = await supabase
    .from('libraries')
    .upsert({ user_id: userId, library, updated_at: new Date().toISOString() });
  if (error) return { ok: false, error: error.message };
  return { ok: true };
}
