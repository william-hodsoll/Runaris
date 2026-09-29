# Spec: Search + toolbar cleanup

## Requirement
User: after manually adding a book, needs a way to find it — plus clean up the
toolbar while adding it. Port v1's HUD search (`starMatchesSearch`,
neural_mind.py:1276; input at :995-997): case-insensitive substring match
across title/author/genre/subjects, dims everything else on the canvas (same
mechanism v1 uses for the status filter, already ported in spec 11's
`dimmedByFilter`). v1's separate alphabetical Library-list panel (searchable
list, :3124) is out of scope — no list/browse view exists yet in the rebuild
to attach it to; the cosmos-dimming half of search is the part that answers
"how do I find the book I just added."

## Design
- `model/search.ts`: pure `starMatchesSearch(star, query)`, ported verbatim
  from v1.
- Store: `searchQuery: string` (default `''`, not persisted — same treatment
  as `mode`/`frozen`) + `setSearchQuery`.
- `render/draw.ts`: `dimmedBySearch = query !== '' && !starMatchesSearch(star, query)`,
  OR'd into the existing `dimmed` alongside `dimmedByConnect`/`dimmedByFilter`.
  Same treatment for the synapse-web filter.
- Toolbar cleanup: the current 7-button row (Add a book / Scan barcode / Add
  by ISBN / Import library / Export / Customize / Settings) is the "clean up"
  target. Collapse the four add-flows into one "+ Add" dropdown (click to
  reveal 3 options + Import); add the search box as its own always-visible
  field, matching v1's HUD-search placement/intent (visible whenever the
  toolbar is, clears via an × button). Net result: `[+ Add ▾] [Search] [Export] [Customize] [Settings]`.

## Test plan
- Vitest: `starMatchesSearch` unit tests (title/author/genre/subject match,
  case-insensitivity, empty query matches everything).
- Browser smoke: add a book via the manual form, type part of its title into
  search, confirm other stars dim (pixel/alpha check) and the added one
  doesn't.

## Rollback
Revert `model/search.ts` (new), `store/useLibraryStore.ts`, `render/draw.ts`,
`components/Toolbar.tsx`. `searchQuery` isn't persisted, so no migration.
