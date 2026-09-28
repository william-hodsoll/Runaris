# Spec: Supabase auth + library sync (foundation)

## Requirement
Foundation for the freemium paid tier: accounts + cross-device library sync, gated behind sign-in. Per intent.md's 2026-09-28 decisions — Supabase for backend/auth, freemium for monetization. Explicitly scoped to auth+sync only: billing/tier enforcement (who's actually paid) is separate future scope, not built here. Signed-out use stays exactly as it is today — 100% local, zero backend calls, no regression risk to the free tier.

Out of scope for this spec: Stripe/billing, actually gating sync behind "paid" (everyone who signs in gets sync for now — the paywall is a follow-up spec once this foundation works), real-time multi-device conflict resolution (last-write-wins is the MVP behavior, documented as a known limitation), Social features (stays a stub per intent.md).

## Design
**Schema** (Supabase Postgres) — one row per user, whole `Library` object as `jsonb`, not normalized into per-book tables. Matches the existing local `Library` shape exactly (see `model/types.ts`) so the sync layer is a serialize/deserialize, not a schema translation:
```sql
create table libraries (
  user_id uuid primary key references auth.users(id) on delete cascade,
  library jsonb not null,
  updated_at timestamptz not null default now()
);
alter table libraries enable row level security;
create policy "users manage their own library" on libraries
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
```
Normalizing into real tables is a later migration if per-book queries (server-side search, etc.) are ever needed — YAGNI for now, this is sync, not a new query surface.

**Auth**: email magic-link via `supabase-js` (`signInWithOtp`) — no password to store, matches the low-friction bar of a personal-library app. New `auth/supabaseClient.ts` (env-gated exactly like `analytics.ts`: `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY`, no-ops/hides sign-in UI entirely if unset, same convention as PostHog/Sentry).

**Sync layer**: additive to `persistence/index.ts`, not a replacement — IndexedDB stays the source of truth for rendering and offline use in both signed-in and signed-out states (CLAUDE.md pitfall: render loop must never block on a network round-trip). When a session exists: on `hydrate()`, pull the Supabase row and take it if its `updated_at` is newer than the local copy's (last-write-wins); on every local save, debounce-push the current `Library` to Supabase (a few seconds, not per-keystroke) after the existing `idbSet` succeeds. A push/pull failure surfaces the existing `warning` banner — never a silent drop, per CLAUDE.md.

**UI**: `SettingsModal`'s Profile tab (currently a stub disclosure) becomes real: email input → "send magic link" → a "check your email" state → once a session exists, shows the signed-in email + "Sign out". Social tab is untouched, stays a stub. No new top-level nav — this lives where Profile already was.

**Store**: `useLibraryStore` gains `session: Session | null` and `signIn(email)`/`signOut()`, mirroring the existing `hydrated`/`warning` pattern — no separate auth store, this app doesn't have enough auth surface to warrant one yet.

## Blocking manual step (cannot be done from this session)
A Supabase project must exist before any of this can be built against something real — same category as spec 10's "repo owner enables Pages" step. Needed from the user before Build starts:
1. Create a free Supabase project (supabase.com)
2. Run the `libraries` table + RLS policy SQL above in its SQL editor
3. Enable Email OTP (magic link) in Authentication → Providers (on by default, just confirm)
4. Provide the project URL and anon (public) key — these go in `.env`/GitHub Actions secrets as `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY`, same pattern as the existing PostHog/Sentry keys

## Test plan
- Unit: sync-layer merge logic (`newer local wins`, `newer remote wins`, `remote missing → push local`) tested against a mocked Supabase client — no real network in unit tests, same pattern as `indexeddb.test.ts` mocking `fake-indexeddb`.
- Signed-out path: existing 64 tests must keep passing unmodified — proves zero behavior change when no session exists.
- Typecheck clean, build succeeds.
- Browser smoke test (once real credentials exist): sign in via magic link, confirm library round-trips through the `libraries` table, sign out returns to pure local behavior with no errors.

## Rollback
Additive: new table (RLS-scoped, no effect on anything else in the Supabase project), new env-gated module that no-ops without keys, sync layer wraps existing persistence without changing its local-only path. Reverting the commit removes the sync layer; the `libraries` table can stay unused with no code impact.
