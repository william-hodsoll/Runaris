// Env-gated Supabase client — same convention as analytics.ts
// (VITE_POSTHOG_KEY/VITE_SENTRY_DSN): null with no keys, so sign-in UI hides
// itself and the app works with zero backend config. See specs/14-auth-and-sync.md.
import { createClient, type SupabaseClient } from '@supabase/supabase-js';

const url = import.meta.env.VITE_SUPABASE_URL;
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabase: SupabaseClient | null = url && anonKey ? createClient(url, anonKey) : null;

export function isSyncConfigured(): boolean {
  return supabase !== null;
}
