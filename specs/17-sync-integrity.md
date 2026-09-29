# Spec: Sync + ID integrity (design review of spec 14)

Opus design review of spec 14's last-write-wins sync, triggered by the
cross-device bug. Findings ranked by severity; all verified by reading the
code path, P0-1 reproduced in a test.

## Findings

**P0-1 — Duplicate IDs across page loads (shipped, sync-independent).**
`addBook.ts` / `buildLibrary.ts` generate ids from a module counter that
restarts at 0 every page load. After a reload, the next added book reuses an
id already in the saved library. Reproduced: add A → reload → add B → both are
`star-added-2`; **removing B deletes A too**. Constellations collide the same
way (`const-added-1`), mis-mapping stars to the wrong centre/colour. Also
makes any cross-device merge impossible.

**P0-2 — Whole-library last-write-wins = silent data loss.** On sign-in,
whichever side has the newer timestamp replaces the other *entirely*. If
device B did anything locally (loaded demo, added a book signed-out) more
recently than device A's last push, B's library overwrites the account; A
then pulls it and loses its books too. Plausible cause of the user's "test
book not visible" report alongside the listener gap already fixed.

**P1-3 — Timestamps from two different clocks.** `remote.updated_at` is the
*pushing* device's clock (set client-side in `pushLibrary`); `localUpdatedAt`
is this device's clock. Clock skew flips the LWW decision.

**P1-4 — Concurrent edits overwrite.** Pushes are blind upserts of the whole
library. Two open devices each pushing clobber each other's adds. An open
tab also never sees the other device's changes until reload/sign-in.

**P2-5 — Cross-account bleed on shared browsers.** Sign-out leaves the local
library and sync markers; the next account to sign in on that browser gets
the previous user's library pushed into it.

## Design

1. **Unique ids**: `crypto.randomUUID()` in both generators (stdlib). On load,
   a repair pass re-ids any duplicate star/constellation ids already saved
   (second occurrence gets a new UUID) — prevents P0-1 data loss on existing
   libraries. Ids stay strings: no schema/version change.
2. **3-way merge by star id, replacing timestamp LWW.** Per device, store a
   sync base: `{ userId, starIds[] }` = the id set at last successful sync
   (localStorage `neuralMind.syncBase.v1`). Merge rule:
   - in local, not in base → added here → keep
   - in base, not in local → deleted here → drop
   - in remote, not in base → added elsewhere → keep
   - in base, not in remote → deleted elsewhere → drop
   - no base (first sync on this device) → union, nothing dropped (safe default)
   Books aren't editable yet, so there are no field-level conflicts to
   resolve. Constellations: union by id, then fold duplicates of the same
   subject into one (keeps v1's one-constellation-per-subject metaphor),
   drop empty ones, recount. Timestamps (`lastModified`) are no longer used
   for decisions → P1-3 disappears; that code is deleted.
3. **One sync path**: `syncNow()` = pull → merge → apply locally if changed →
   push → update base. Used on sign-in, after local edits (debounced, as
   today), and on tab focus (`visibilitychange`) so an already-open browser
   picks up the other device's changes. Fixes P1-4 for the realistic case.
   `ponytail:` two devices pushing in the same ~second can still race;
   upgrade path is optimistic concurrency (`.eq('updated_at', seen)`).
4. **Account switch**: if the base belongs to a different user than the one
   signing in, take the remote library as-is (don't merge the previous
   account's local data into it). First-ever sign-in on a device (no base)
   still uploads the local library — that's the intended "sign in to back up"
   flow. Fixes P2-5.

## Test plan
- P0-1 regression: add → simulated reload (`vi.resetModules`) → add → ids
  differ; removing one keeps the other. Repair pass re-ids saved duplicates.
- Merge unit tests for every rule above, plus constellation subject-folding.
- Account-switch test; existing hydrate-sync regression test keeps passing.
- Typecheck, full suite, build; live re-test of the two-browser scenario.

## Rollback
Revert commit. No save-format change (ids remain strings; sync base is a new,
separate localStorage key that old code ignores). The remote row shape is
unchanged.
