import { useEffect } from 'react';
import { initAnalytics, trackEvent } from './analytics/analytics';
import { CanvasHost } from './components/CanvasHost';
import { ConnectModeHUD } from './components/ConnectModeHUD';
import { EmptyState } from './components/EmptyState';
import { PrivacyNotice } from './components/PrivacyNotice';
import { TimelapseControls } from './components/TimelapseControls';
import { Toolbar } from './components/Toolbar';
import { Tooltip } from './components/Tooltip';
import { useLibraryStore } from './store/useLibraryStore';

export function App() {
  const hydrate = useLibraryStore((s) => s.hydrate);
  const warning = useLibraryStore((s) => s.warning);

  useEffect(() => {
    void hydrate();
    void initAnalytics();
    trackEvent('app_opened');
  }, [hydrate]);

  return (
    <>
      <CanvasHost />
      <Toolbar />
      <EmptyState />
      <Tooltip />
      <ConnectModeHUD />
      <TimelapseControls />
      <PrivacyNotice />
      {warning && (
        <div
          style={{
            position: 'fixed',
            top: 8,
            right: 8,
            background: '#ff9ab8',
            color: '#2b2b26',
            padding: '6px 10px',
            borderRadius: 8,
            fontFamily: 'system-ui, sans-serif',
            fontSize: 12,
          }}
        >
          {warning}
        </div>
      )}
    </>
  );
}
