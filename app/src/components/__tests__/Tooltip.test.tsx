// Remove-flow test: canvas click hit-testing isn't practical to drive from a
// browser smoke test (star position depends on the 3D projection), so this
// exercises the Tooltip's confirm/remove wiring directly against the real
// store, same pattern as ErrorBoundary.test.tsx. See specs/15-manual-add-and-remove.md.
import { act } from 'react';
import { createRoot } from 'react-dom/client';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { Tooltip } from '../Tooltip';
import { useLibraryStore } from '../../store/useLibraryStore';

describe('Tooltip remove flow', () => {
  let container: HTMLDivElement;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
  });

  afterEach(() => {
    container.remove();
  });

  it('confirms and removes the selected star via the store', () => {
    const { addBook, selectStar } = useLibraryStore.getState();
    addBook({ title: 'Smoke Test Book' }, 'manual');
    const starId = useLibraryStore.getState().library.stars[0].id;
    selectStar(starId);

    const root = createRoot(container);
    act(() => {
      root.render(<Tooltip />);
    });
    expect(container.textContent).toContain('Smoke Test Book');

    const removeBtn = Array.from(container.querySelectorAll('button')).find((b) => b.textContent === 'Remove')!;
    act(() => removeBtn.click());
    const yesBtn = Array.from(container.querySelectorAll('button')).find((b) => b.textContent === 'Yes')!;
    act(() => yesBtn.click());

    expect(useLibraryStore.getState().library.stars.find((s) => s.id === starId)).toBeUndefined();
    expect(useLibraryStore.getState().mode).toEqual({ kind: 'idle' });

    act(() => root.unmount());
  });
});
