// Sole signal source for the "crash-free sessions" metric — @sentry/browser
// alone doesn't catch React render errors without the separate @sentry/react
// integration, which isn't warranted here. See specs/13-maintain-metrics.md.
import { Component, type ErrorInfo, type ReactNode } from 'react';
import { captureError, trackEvent } from '../analytics/analytics';

type Props = { children: ReactNode };
type State = { hasError: boolean };

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: unknown, info: ErrorInfo): void {
    captureError(error);
    trackEvent('app_crashed');
    if (import.meta.env.DEV) {
      // eslint-disable-next-line no-console
      console.error('[ErrorBoundary]', error, info.componentStack);
    }
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column',
            gap: 12,
            fontFamily: 'system-ui, sans-serif',
            background: '#F7F1E8',
          }}
        >
          <div>Something went wrong.</div>
          <button onClick={() => window.location.reload()} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
            Reload
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
