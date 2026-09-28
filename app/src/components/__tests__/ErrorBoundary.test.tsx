// Verifies the catch path directly, since React error boundaries only catch
// render/lifecycle errors — the app's own render loop runs in rAF, outside
// React, so this can't be exercised through a browser smoke test at all (see
// specs/13-maintain-metrics.md). No new dependency: react-dom is already used.
import { act } from 'react';
import { createRoot } from 'react-dom/client';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { ErrorBoundary } from '../ErrorBoundary';

vi.mock('../../analytics/analytics', () => ({
  captureError: vi.fn(),
  trackEvent: vi.fn(),
}));
import { captureError, trackEvent } from '../../analytics/analytics';

function Thrower(): never {
  throw new Error('boom');
}

describe('ErrorBoundary', () => {
  let container: HTMLDivElement;

  afterEach(() => {
    container?.remove();
    vi.clearAllMocks();
  });

  it('renders a fallback and reports the error instead of crashing the page', () => {
    container = document.createElement('div');
    document.body.appendChild(container);
    const root = createRoot(container);

    act(() => {
      root.render(
        <ErrorBoundary>
          <Thrower />
        </ErrorBoundary>,
      );
    });

    expect(container.textContent).toContain('Something went wrong');
    expect(captureError).toHaveBeenCalledTimes(1);
    expect(trackEvent).toHaveBeenCalledWith('app_crashed');
  });
});
