// Ports the "connect-hint"/"connect-count" HUD from reference/neural_mind.py.
import { deriveConnectionsFor } from '../model/connections';
import { useLibraryStore } from '../store/useLibraryStore';

export function ConnectModeHUD() {
  const mode = useLibraryStore((s) => s.mode);
  const library = useLibraryStore((s) => s.library);
  const exitConnectMode = useLibraryStore((s) => s.exitConnectMode);

  if (mode.kind !== 'connect') return null;
  const count = deriveConnectionsFor(library, mode.starId).size;

  return (
    <div
      style={{
        position: 'fixed',
        top: 16,
        left: '50%',
        transform: 'translateX(-50%)',
        background: 'rgba(45,45,40,0.85)',
        color: '#FDFAF4',
        borderRadius: 999,
        padding: '8px 16px',
        fontFamily: 'system-ui, sans-serif',
        fontSize: 13,
        display: 'flex',
        alignItems: 'center',
        gap: 10,
      }}
    >
      <span>{count} connected book{count === 1 ? '' : 's'}</span>
      <button
        onClick={exitConnectMode}
        style={{ background: 'transparent', border: 'none', color: 'inherit', cursor: 'pointer' }}
      >
        Exit
      </button>
    </div>
  );
}
