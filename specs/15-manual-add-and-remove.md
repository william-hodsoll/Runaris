# Spec: Manual add-book form + remove-book UI

## Requirement
User report: no way to add a book except ISBN lookup, and no way to remove one, despite
`addBook`/`removeBook` already existing in the store. Port v1's manual-add fields
(`renderAddBook`, neural_mind.py:2510) and remove-star confirm flow (`removeStarFromMind`,
neural_mind.py:3758) as UI-only additions — no model/store changes needed, both actions
are already implemented and unused.

## Design
- `AddBookManual.tsx`: same modal shape as `AddByIsbn.tsx`. Fields match v1 1:1: title
  (required), author, year, pages, genre (select, same option list as v1), subjects
  (comma-separated). Submit calls `addBook(book, 'manual')`; tracks `book_added_manual`
  (already in the closed event catalog, unused until now).
- Toolbar: add "+ Add a book" button next to "Add by ISBN", opens the new panel.
- `Tooltip.tsx`: add a "Remove" button below the existing content. Click -> inline
  confirm ("Remove?" / "Yes" / "Cancel"), matching v1's `confirm()` gate but in-panel
  since this is a tooltip not a native dialog. Confirm calls `removeBook(star.id)`
  (already resets `mode` to idle) and tracks `book_removed`.
- No new store/model code: `addBook`, `removeBook`, both analytics events already exist.

## Test plan
- Vitest: none needed at model layer (untouched). Component-level smoke via Playwright:
  add a manual book, confirm a new star renders; select a star, remove it, confirm it's
  gone and tooltip closes.

## Rollback
Revert the three files (`AddBookManual.tsx` new, `Toolbar.tsx`, `Tooltip.tsx`) — no
persisted-data shape change, nothing to migrate.
