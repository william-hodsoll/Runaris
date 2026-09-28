// First-run notice — shown once, per specs/03-analytics.md. Links straight
// to the opt-out toggle so the decision is one click away, not buried in a
// settings screen (settings UI itself is out of scope for this spec).
import { useState } from 'react';
import { hasSeenPrivacyNotice, isOptedOut, markPrivacyNoticeSeen, setOptOut } from '../analytics/analytics';

export function PrivacyNotice() {
  const [dismissed, setDismissed] = useState(hasSeenPrivacyNotice());
  const [optedOut, setOptedOutState] = useState(isOptedOut());

  if (dismissed) return null;

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 16,
        left: 16,
        right: 16,
        maxWidth: 420,
        margin: '0 auto',
        background: '#FDFAF4',
        border: '1px solid #EBEDE0',
        borderRadius: 12,
        padding: 16,
        fontFamily: 'system-ui, sans-serif',
        fontSize: 13,
        color: '#2b2b26',
        zIndex: 20,
      }}
    >
      <div style={{ marginBottom: 8 }}>
        Runaris collects anonymous usage and crash data to improve the app. Your
        library — titles, authors, notes — never leaves your device.
      </div>
      <label style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
        <input
          type="checkbox"
          checked={optedOut}
          onChange={(e) => {
            setOptedOutState(e.target.checked);
            setOptOut(e.target.checked);
          }}
        />
        Opt out of usage/crash analytics
      </label>
      <button
        onClick={() => {
          markPrivacyNoticeSeen();
          setDismissed(true);
        }}
        style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}
      >
        Got it
      </button>
    </div>
  );
}
