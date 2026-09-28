// Reads the store through the normal React hook (fine here — this is UI
// chrome, not the 60fps render loop). Cover art fetch is out of scope for
// this spec; the cover slot is a stub per specs/02-react-vite-port.md.
import { useLibraryStore } from '../store/useLibraryStore';

export function Tooltip() {
  const mode = useLibraryStore((s) => s.mode);
  const library = useLibraryStore((s) => s.library);

  if (mode.kind !== 'tooltip') return null;
  const star = library.stars.find((s) => s.id === mode.starId);
  if (!star) return null;

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 24,
        left: '50%',
        transform: 'translateX(-50%)',
        background: '#FDFAF4',
        border: '1px solid #EBEDE0',
        borderRadius: 12,
        padding: '12px 16px',
        maxWidth: 320,
        fontFamily: 'system-ui, sans-serif',
      }}
    >
      <div style={{ fontWeight: 600 }}>{star.title}</div>
      <div style={{ color: '#6b6b63', fontSize: 14 }}>{star.author}</div>
      {star.subjects.length > 0 && (
        <div style={{ marginTop: 6, fontSize: 12, color: '#8a8a80' }}>{star.subjects.join(', ')}</div>
      )}
      <div style={{ marginTop: 8, fontSize: 12, color: '#8a8a80' }}>Tap again to see connections</div>
    </div>
  );
}
