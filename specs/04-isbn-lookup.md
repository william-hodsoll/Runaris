# Spec: ISBN lookup (OpenLibrary)

## Requirement
Port v1's OpenLibrary ISBN lookup (`fetchByIsbn` in `neural_mind.py`'s template JS) so a user can type/paste an ISBN and get a book pre-filled (title, author, cover) before adding it to the cosmos.

In scope: text-based ISBN entry, OpenLibrary Books API lookup, normalize result to `BookInput`, confirmation step before calling `addBook`, error state for an unknown ISBN.

Out of scope (deferred, not in this spec): camera barcode scanning (ZXing) — v1 has it, but it needs camera permission handling and a dedicated device-testing pass; text entry covers the same lookup path and unblocks the rest of the add-book flow now.

## Design
- `lookup/openLibrary.ts`: `lookupByIsbn(isbn: string): Promise<BookInput | null>` — hits `https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data`, maps response to `BookInput` (title, author from `authors[0].name`, cover from `cover.large`, subjects from `subjects[]` if present). Returns `null` on no match; throws only on network failure (caller shows a retry state, not a crash).
- `components/AddByIsbn.tsx`: input + "Look up" button, shows a preview card (cover, title, author) with Confirm/Cancel before calling `store.addBook`.
- Isolate the fetch behind the adapter so a provider swap (Google Books) later doesn't touch UI code — matches `CLAUDE.md`'s "External lookup" note.

## Test plan
1. `lookupByIsbn` maps a known-shape OpenLibrary response to the expected `BookInput` (mocked fetch)
2. Unknown ISBN returns `null`, UI shows "no record found", never a thrown error to the console
3. Network failure surfaces a retry affordance, not a silent failure
4. Confirm step calls `store.addBook` exactly once per confirmed lookup (no double-submit on repeated clicks)

## Rollback
Additive UI entry point; if the lookup adapter is flaky, hide the "Add by ISBN" door and fall back to manual entry (already shipped) with no model changes needed.
