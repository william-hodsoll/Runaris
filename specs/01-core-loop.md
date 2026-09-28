# Spec: Core loop — manual book entry, linking, canvas

## Requirement
From `intent.md` MVP scope, build order item 1: the app must let a user add books by hand, connect them with typed links, and pan/zoom the resulting map, with no external network calls. This is the foundation every later feature (ISBN lookup, import, personalization) builds on.

In scope for this spec:
- Add a BookNode via a form (title, author required; cover image upload optional)
- Edit / delete a BookNode
- Draw a Link between two BookNodes, choosing type: emotional | thematic | sequence | custom
- Edit / delete a Link
- Pan and zoom the canvas
- Save the map to IndexedDB (autosave) and export/import as JSON
- Empty-state UI (no books yet) and first-run privacy notice (analytics on-by-default, per `intent.md`)

Out of scope for this spec (later specs): ISBN lookup, CSV import, tags/mood/rating, color/size personalization, image export.

## Design

### Data model (from CLAUDE.md, this spec implements the subset it needs)
```ts
type BookNode = {
  id: string;          // uuid
  title: string;
  author: string;
  coverUrl?: string;    // local blob URL or data URL for MVP
  position: { x: number; y: number };
  createdAt: string;
  updatedAt: string;
};

type Link = {
  id: string;
  sourceId: string;
  targetId: string;
  type: 'emotional' | 'thematic' | 'sequence' | 'custom';
  label?: string;
  createdAt: string;
};

type Library = {
  version: 1;
  books: BookNode[];
  links: Link[];
};
```

### Layers
- `model/` — pure functions: addBook, updateBook, removeBook (cascades link removal), addLink, removeLink, validate(library). No React, no canvas.
- `store/` — Zustand store wrapping the model, single source of truth for UI + canvas.
- `render/` — Canvas2D renderer: draws nodes (title text, cover thumbnail if present, else placeholder), draws links (line + type-colored stroke), hit-testing for click/drag by position.
- `persistence/` — IndexedDB autosave (debounced, on every store change) + explicit JSON export/import.

### UI
- Canvas fills viewport. Toolbar: "Add book", zoom controls, export/import.
- Add/edit book: modal form.
- Create link: click-drag from one node to another; on drop, small popover to pick link type.
- Delete: select node/link, press Delete key or a context menu.
- Empty state: centered "Add your first book" CTA.
- First-run modal: one-time privacy notice (analytics on, link to opt-out in settings) — settings screen itself can be a stub for now (single toggle).

### Edge cases
- Deleting a book removes all links touching it (cascade, no orphan links — enforced in `model/`, covered by an invariant test).
- Duplicate titles are allowed (different editions, re-reads) — id is the only uniqueness constraint.
- Link cannot connect a node to itself.
- Cover image upload: cap size (e.g. 2MB) and downscale before storing, so IndexedDB doesn't bloat.
- Autosave failure (e.g. storage quota) surfaces a visible warning, not a silent drop.

## Test plan
Maps to the eval list in `docs/sdlc-playbook.md`:
1. Model invariants: no orphan links after book deletion; unique ids; self-links rejected — unit tests on `model/`.
2. Save/load round-trip: create N books + links, export JSON, reimport, deep-equal check (0 loss) — matches intent.md metric.
3. Render benchmark: synthetic library of 500 books, measure fps while panning — target 60fps / breach <30fps.
4. Manual add flow: time from canvas load to first book saved — target <15s (intent.md metric), measured via a scripted UI test, not a real user's typing speed.
5. Migration test placeholder: schema is version 1, no migration to test yet — add a stub test that fails loudly if `version` changes without a migration function.

## Rollback
This is the first feature; there's no prior version to roll back to. If the deploy gate fails (evals red), do not merge — fix forward on the branch. Once a v2 of this feature ships, rollback = redeploy the last tagged build with the v1 core loop and same IndexedDB schema version (no data migration needed since nothing shipped before it).
