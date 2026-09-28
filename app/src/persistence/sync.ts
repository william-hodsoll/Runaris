// Additive sync layer over the local IndexedDB store — IndexedDB stays the
// source of truth for rendering/offline use in both signed-in and
// signed-out states (CLAUDE.md: render loop must never block on network).
// Last-write-wins by timestamp; real conflict merge is a documented MVP
// limitation. See specs/14-auth-and-sync.md.
import { supabase } from '../auth/supabaseClient';
import type { Library } from '../model/types';

const LAST_MODIFIED_KEY = 'neuralMind.lastModified.v1';

export function getLocalUpdatedAt(): number {
  const raw = localStorage.getItem(LAST_MODIFIED_KEY);
  return raw ? Number(raw) : 0;
}

export function markLocalUpdated(at = Date.now()): void {
  try {
    localStorage.setItem(LAST_MODIFIED_KEY, String(at));
  } catch {
    // best-effort, matches persistence layer's convention elsewhere
  }
}

export async function pullRemoteLibrary(userId: string): Promise<{ library: Library; updatedAt: number } | null> {
  if (!supabase) return null;
  const { data, error } = await supabase
    .from('libraries')
    .select('library, updated_at')
    .eq('user_id', userId)
    .maybeSingle();
  if (error || !data) return null;
  return { library: data.library as Library, updatedAt: new Date(data.updated_at as string).getTime() };
}

export async function pushLibrary(userId: string, library: Library): Promise<{ ok: true } | { ok: false; error: string }> {
  if (!supabase) return { ok: false, error: 'Sync is not configured.' };
  const { error } = await supabase
    .from('libraries')
    .upsert({ user_id: userId, library, updated_at: new Date().toISOString() });
  if (error) return { ok: false, error: error.message };
  return { ok: true };
}

// Debounced push so a burst of local saves (e.g. a CSV import) doesn't fire
// one network request per book.
let pushTimer: ReturnType<typeof setTimeout> | null = null;
export function debouncedPush(userId: string, library: Library, onError: (message: string) => void, delayMs = 3000): void {
  if (pushTimer) clearTimeout(pushTimer);
  pushTimer = setTimeout(() => {
    void pushLibrary(userId, library).then((result) => {
      if (!result.ok) onError(`Could not sync your library: ${result.error}`);
    });
  }, delayMs);
}
