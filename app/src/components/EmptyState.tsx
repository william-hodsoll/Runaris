// Empty-library prompt — matches specs/02-react-vite-port.md edge case
// ("empty library: render an empty sphere / prompt state").
import { useLibraryStore } from '../store/useLibraryStore';
import demoBooks from '../data/demoBooks.json';
import type { BookInput } from '../model/types';

export function EmptyState() {
  const library = useLibraryStore((s) => s.library);
  const loadDemo = useLibraryStore((s) => s.loadDemo);

  if (library.stars.length > 0) return null;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 12,
        fontFamily: 'system-ui, sans-serif',
        pointerEvents: 'none',
      }}
    >
      <div style={{ fontSize: 20, color: '#2b2b26' }}>Your cosmos is empty</div>
      <button
        style={{ pointerEvents: 'auto', padding: '8px 16px', borderRadius: 8, cursor: 'pointer' }}
        onClick={() => loadDemo(demoBooks as BookInput[], 1)}
      >
        Load the demo library ({(demoBooks as BookInput[]).length} books)
      </button>
    </div>
  );
}
