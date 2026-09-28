# Spec: CSV/JSON import

## Requirement
Port v1's `parseCSV`/`normaliseBook`/import flow: drop or pick a `.csv` or `.json` file, map rows to `BookInput[]`, add them all to the library. Must never silently drop a row (`CLAUDE.md` "Never" / `intent.md` import metric).

In scope: CSV parsing (including a Goodreads-shaped column set: `Title`, `Author`, `My Rating`, `Bookshelves`, `Number of Pages`), JSON array import (own export format round-trips here too), per-row validation with a flagged/skipped list shown to the user, batch add to the library.

Out of scope: de-duplication against existing library entries (first pass just appends; dedupe is a fast-follow once this ships).

## Design
- `import/parseCsv.ts`: minimal CSV line splitter (ports v1's `splitCSVLine`, handles quoted commas) — no external CSV library needed for this column count/shape.
- `import/normaliseBook.ts`: maps a raw row (CSV object or JSON book) to `BookInput`; recognizes both Runaris's own export shape and common Goodreads column names; a row missing `title` is flagged, not dropped.
- `components/ImportLibrary.tsx`: file input (`accept=".csv,.json"`), preview list showing "N books ready, M flagged" before committing, commit button calls `store.addBook` per row (or a new `store.addBooks(batch)` for one persist/analytics-event instead of N).
- Analytics: one `import_completed` event with counts only (rows imported, rows flagged) — no titles/content, per the analytics spec's closed event catalog.

## Test plan
1. `parseCsv` handles quoted fields containing commas correctly
2. `normaliseBook` maps Goodreads column names (`Title`, `Author`, `Number of Pages`) to `BookInput`
3. A row with no title is flagged, included in the "flagged" count, and not silently dropped from the report
4. Round-trip: export the library to JSON (already shipped), reimport it, resulting library is equivalent (title/author/subjects preserved) — this is the `intent.md` "Import round-trip" metric
5. Committing a batch triggers exactly one `import_completed` analytics event with correct counts

## Rollback
Additive; if import breaks, manual entry and ISBN lookup remain the way to add books. No schema change, so no migration risk.
