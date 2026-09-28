// Settings modal with tabs — ports v1's renderSettings()/renderTab*(). Profile
// and Social are disclosed as non-functional stubs per intent.md's decision;
// this replaces v1's "No tracking, no backend" About copy per the analytics
// decision. specs/08-insights-and-settings.md.
import { useState } from 'react';
import { isOptedOut, setOptOut } from '../analytics/analytics';
import { isSyncConfigured } from '../auth/supabaseClient';
import { downloadLibraryExport } from '../persistence/exportLibrary';
import { InsightsPanel } from './InsightsPanel';
import { useLibraryStore } from '../store/useLibraryStore';

type Tab = 'library' | 'insights' | 'app' | 'profile' | 'social' | 'about';

const TABS: { id: Tab; label: string }[] = [
  { id: 'library', label: 'Library' },
  { id: 'insights', label: 'Insights' },
  { id: 'app', label: 'App' },
  { id: 'profile', label: 'Profile' },
  { id: 'social', label: 'Social' },
  { id: 'about', label: 'About' },
];

const STUB_DISCLOSURE = 'This is a visual shell — it doesn\'t connect to anything yet.';

// Magic-link sign-in for cross-device sync (paid tier, once billing exists —
// spec 14 covers auth+sync only). Hides itself when Supabase isn't
// configured, same convention as analytics' opt-out toggle.
function ProfileTab() {
  const session = useLibraryStore((s) => s.session);
  const signIn = useLibraryStore((s) => s.signIn);
  const signOut = useLibraryStore((s) => s.signOut);
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'sending' | 'sent' | 'error'>('idle');
  const [error, setError] = useState('');

  if (!isSyncConfigured()) {
    return <div style={{ fontSize: 13, color: '#6b6b63' }}>{STUB_DISCLOSURE}</div>;
  }

  if (session) {
    return (
      <div style={{ fontSize: 13, display: 'flex', flexDirection: 'column', gap: 8 }}>
        <div>Signed in as {session.user.email}</div>
        <div style={{ color: '#6b6b63' }}>Your library syncs across devices.</div>
        <button onClick={() => void signOut()} style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer', alignSelf: 'flex-start' }}>
          Sign out
        </button>
      </div>
    );
  }

  if (status === 'sent') {
    return <div style={{ fontSize: 13, color: '#6b6b63' }}>Check your email for a sign-in link.</div>;
  }

  return (
    <div style={{ fontSize: 13, display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ color: '#6b6b63' }}>Sign in to sync your library across devices.</div>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
        style={{ padding: 8, borderRadius: 8, border: '1px solid #EBEDE0' }}
      />
      {status === 'error' && <div style={{ color: '#b4506a' }}>{error}</div>}
      <button
        onClick={async () => {
          setStatus('sending');
          const result = await signIn(email);
          if (result.ok) setStatus('sent');
          else {
            setStatus('error');
            setError(result.error);
          }
        }}
        disabled={status === 'sending' || !email.trim()}
        style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer', alignSelf: 'flex-start' }}
      >
        {status === 'sending' ? 'Sending…' : 'Send magic link'}
      </button>
    </div>
  );
}

export function SettingsModal({ initialTab = 'library', onClose }: { initialTab?: Tab; onClose: () => void }) {
  const [tab, setTab] = useState<Tab>(initialTab);
  const [optedOut, setOptedOutState] = useState(isOptedOut());
  const library = useLibraryStore((s) => s.library);

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(0,0,0,0.3)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 30,
      }}
    >
      <div
        style={{
          background: '#FDFAF4',
          borderRadius: 12,
          padding: 20,
          width: 380,
          fontFamily: 'system-ui, sans-serif',
        }}
      >
        <div style={{ display: 'flex', gap: 4, marginBottom: 16, flexWrap: 'wrap' }}>
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              style={{
                padding: '4px 10px',
                borderRadius: 8,
                cursor: 'pointer',
                fontSize: 12,
                fontWeight: tab === t.id ? 700 : 400,
                background: tab === t.id ? '#EBEDE0' : 'transparent',
                border: 'none',
              }}
            >
              {t.label}
            </button>
          ))}
        </div>

        <div style={{ minHeight: 120 }}>
          {tab === 'library' && (
            <div style={{ fontSize: 13, display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div>{library.stars.length} books in your cosmos.</div>
              <button
                onClick={() => downloadLibraryExport(library)}
                disabled={library.stars.length === 0}
                style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer', alignSelf: 'flex-start' }}
              >
                Export library
              </button>
            </div>
          )}

          {tab === 'insights' && <InsightsPanel />}

          {tab === 'app' && (
            <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13 }}>
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
          )}

          {tab === 'profile' && <ProfileTab />}

          {tab === 'social' && <div style={{ fontSize: 13, color: '#6b6b63' }}>{STUB_DISCLOSURE}</div>}

          {tab === 'about' && (
            <div style={{ fontSize: 13, color: '#6b6b63', display: 'flex', flexDirection: 'column', gap: 6 }}>
              <div>Runaris — a cosmos of every book you've read.</div>
              <div>
                Runaris collects anonymous usage and crash data to improve the app. Your library never leaves your
                device. Opt out any time in the App tab.
              </div>
            </div>
          )}
        </div>

        <button onClick={onClose} style={{ marginTop: 16, padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
          Close
        </button>
      </div>
    </div>
  );
}
