# Spec: IndexedDB migration

## Requirement
`intent.md` deferred the localStorage-vs-IndexedDB choice to Design. Deciding now: IndexedDB, because cover images (fetched in spec 04, stored as data URIs) will exceed localStorage's ~5-10MB ceiling once a library grows. Must not lose any data already saved under the v1-parity `neuralMind.v1` localStorage key from spec 02.

## Design
- `persistence/db.ts`: a tiny wrapper (no library — the schema is one object store, doesn't need one) around `indexedDB.open('runaris', 1)`, one object store `library` holding a single record keyed `'current'`.
- `persistence/migrateFromLocalStorage.ts`: on first IndexedDB read, if the store is empty AND `localStorage['neuralMind.v1']` exists, migrate it in, then leave the localStorage copy in place (don't delete — belt-and-suspenders until IndexedDB has been live for a release).
- `saveLibrary`/`loadLibrary` in `persistence/localStorage.ts` get IndexedDB-backed equivalents in a new `persistence/index.ts` that the store imports instead; old localStorage functions stay for the migration path and for tests, not removed.
- Store's `hydrate()` becomes async (IndexedDB is async); loading state shown briefly (empty-state already covers "no library yet" visually, reused for the brief hydrate window).

## Test plan
1. Fresh IndexedDB, no localStorage: hydrate returns an empty library, no throw (jsdom's IndexedDB via `fake-indexeddb` in tests)
2. Existing `neuralMind.v1` localStorage data migrates into IndexedDB on first hydrate, and localStorage is left intact (not deleted)
3. Save/load round-trip through IndexedDB matches the existing localStorage round-trip test's fidelity bar (0 loss)
4. Corrupt/foreign IndexedDB record falls back to empty + warning, same convention as localStorage's `validateLibrary`

## Rollback
If IndexedDB proves flaky in some browser, `persistence/localStorage.ts` still exists and works standalone; swapping the store's import back is a one-line change with no schema loss, since the localStorage copy is never deleted by the migration.
