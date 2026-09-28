// Thin session tracker over supabaseClient — no separate auth store, this
// app doesn't have enough auth surface to warrant one yet (see
// specs/14-auth-and-sync.md). Sign-in is magic-link only: no password to store.
import type { Session } from '@supabase/supabase-js';
import { supabase } from './supabaseClient';

let currentSession: Session | null = null;
let initialized = false;
const listeners = new Set<(session: Session | null) => void>();

export function getSession(): Session | null {
  return currentSession;
}

export function onSessionChange(listener: (session: Session | null) => void): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function setSession(session: Session | null): void {
  currentSession = session;
  for (const listener of listeners) listener(session);
}

/** Call once at app startup. No-ops if Supabase isn't configured. */
export async function initSession(): Promise<Session | null> {
  if (!supabase || initialized) return currentSession;
  initialized = true;
  const { data } = await supabase.auth.getSession();
  setSession(data.session);
  supabase.auth.onAuthStateChange((_event, session) => setSession(session));
  return currentSession;
}

export async function signInWithMagicLink(email: string): Promise<{ ok: true } | { ok: false; error: string }> {
  if (!supabase) return { ok: false, error: 'Sync is not configured.' };
  // Explicit redirect back to wherever the app is actually running (works
  // for GitHub Pages' /Runaris/ subpath and local dev alike) instead of
  // relying on Supabase's configured default Site URL.
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: { emailRedirectTo: window.location.origin + window.location.pathname },
  });
  if (error) return { ok: false, error: error.message };
  return { ok: true };
}

export async function signOut(): Promise<void> {
  await supabase?.auth.signOut();
  setSession(null);
}
