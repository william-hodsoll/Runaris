// Minimal toolbar exposing the add-book entry points shipped so far. Not a
// full nav system (out of scope) — just enough chrome to reach the features
// built across specs 02-09.
import { useEffect, useState } from 'react';
import { useLibraryStore } from '../store/useLibraryStore';
import { downloadLibraryExport } from '../persistence/exportLibrary';
import { AddBookManual } from './AddBookManual';
import { AddByIsbn } from './AddByIsbn';
import { CustomizePanel } from './CustomizePanel';
import { ImportLibrary } from './ImportLibrary';
import { ScanIsbn } from './ScanIsbn';
import { SettingsModal } from './SettingsModal';

type Panel = 'add' | 'isbn' | 'import' | 'scan' | 'settings' | 'customize' | null;

// Ignore shortcuts while typing in a form control — see specs/12-keyboard-controls.md.
function isTypingTarget(el: EventTarget | null): boolean {
  if (!(el instanceof HTMLElement)) return false;
  return el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT' || el.isContentEditable;
}

export function Toolbar() {
  const [open, setOpen] = useState<Panel>(null);
  const library = useLibraryStore((s) => s.library);
  const toggleFrozen = useLibraryStore((s) => s.toggleFrozen);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (isTypingTarget(e.target)) return;
      if (e.key === ' ') {
        e.preventDefault();
        toggleFrozen();
      } else if (e.key === 'Tab') {
        e.preventDefault();
        setOpen((prev) => (prev === 'customize' ? null : 'customize'));
      } else if (e.key === 'Escape') {
        setOpen(null);
      }
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [toggleFrozen]);

  return (
    <>
      <div
        style={{
          position: 'fixed',
          top: 16,
          left: 16,
          display: 'flex',
          gap: 8,
          flexWrap: 'wrap',
          fontFamily: 'system-ui, sans-serif',
          fontSize: 13,
          zIndex: 10,
        }}
      >
        <button onClick={() => setOpen('add')} style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer' }}>
          + Add a book
        </button>
        <button onClick={() => setOpen('scan')} style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer' }}>
          Scan barcode
        </button>
        <button onClick={() => setOpen('isbn')} style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer' }}>
          + Add by ISBN
        </button>
        <button onClick={() => setOpen('import')} style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer' }}>
          Import library
        </button>
        <button
          onClick={() => downloadLibraryExport(library)}
          disabled={library.stars.length === 0}
          style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer' }}
        >
          Export
        </button>
        <button onClick={() => setOpen('customize')} style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer' }}>
          Customize
        </button>
        <button onClick={() => setOpen('settings')} style={{ padding: '6px 12px', borderRadius: 8, cursor: 'pointer' }}>
          Settings
        </button>
      </div>
      {open === 'add' && <AddBookManual onClose={() => setOpen(null)} />}
      {open === 'isbn' && <AddByIsbn onClose={() => setOpen(null)} />}
      {open === 'import' && <ImportLibrary onClose={() => setOpen(null)} />}
      {open === 'scan' && <ScanIsbn onClose={() => setOpen(null)} onUseTextEntry={() => setOpen('isbn')} />}
      {open === 'customize' && <CustomizePanel onClose={() => setOpen(null)} />}
      {open === 'settings' && <SettingsModal onClose={() => setOpen(null)} />}
    </>
  );
}
