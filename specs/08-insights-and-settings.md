# Spec: Insights view + Settings tabs

## Requirement
Port v1's insights (aggregate stats over the library) and the settings modal's tabs (profile, app, library, social, about). Login/Social remain non-functional stubs per `intent.md`'s decision — this spec builds their UI shell only, no backend.

## Design
- `model/insights.ts`: pure functions over `Library` — `countBySubject`, `countByGenre`, `totalPages`, `booksPerYear` (from `dateAdded`). No rendering; feeds both the Insights panel and could feed a future chart.
- `components/InsightsPanel.tsx`: simple stat rows (ports `renderInsights`) — total books, top subjects, total pages, average book size.
- `components/SettingsModal.tsx` with tabs:
  - **Library**: add-book/import entry points (already built — this tab just surfaces them in one place), export button.
  - **App**: analytics opt-out toggle (already built in `PrivacyNotice`; surfaced again here per v1's `renderTabApp`), palette placeholder (color picker deferred — v1's `applyPalette` is cosmetic-only, not required for parity of function).
  - **Profile**: stub, same disclosure text as v1's login screen ("visual shell — doesn't connect to anything yet").
  - **Social**: stub, same disclosure.
  - **About**: version, link to `reference/neural_mind.py` lineage note, updated privacy copy (replaces v1's "No tracking, no backend" — see `intent.md` decision).

## Test plan
1. `countBySubject`/`countByGenre`/`totalPages`/`booksPerYear` produce correct aggregates on a known fixture
2. Insights panel renders without throwing on an empty library (0 books)
3. Settings modal tab switch shows the right content, doesn't lose state when switching back and forth
4. Profile/Social tabs show the stub disclosure text, contain no functional auth call

## Rollback
Additive UI; no model/persistence changes. Removing the modal removes the feature with no data impact.
