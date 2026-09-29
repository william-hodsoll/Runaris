// Toolbar chrome: the add-book entry points, library search, and settings
// panels. Add-flows collapsed into one dropdown and a search box added per
// specs/16-search-and-toolbar-cleanup.md (previously 4 separate add buttons).
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

const btnStyle = { padding: '6px 12px', borderRadius: 8, cursor: 'pointer' } as const;

// Ignore shortcuts while typing in a form control — see specs/12-keyboard-controls.md.
function isTypingTarget(el: EventTarget | null): boolean {
  if (!(el instanceof HTMLElement)) return false;
  return el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT' || el.isContentEditable;
}

export function Toolbar() {
  const [open, setOpen] = useState<Panel>(null);
  const [addMenuOpen, setAddMenuOpen] = useState(false);
  const library = useLibraryStore((s) => s.library);
  const toggleFrozen = useLibraryStore((s) => s.toggleFrozen);
  const searchQuery = useLibraryStore((s) => s.searchQuery);
  const setSearchQuery = useLibraryStore((s) => s.setSearchQuery);

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
        setAddMenuOpen(false);
      }
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [toggleFrozen]);

  function openPanel(panel: Panel) {
    setAddMenuOpen(false);
    setOpen(panel);
  }

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
          alignItems: 'center',
          fontFamily: 'system-ui, sans-serif',
          fontSize: 13,
          zIndex: 10,
        }}
      >
        <div style={{ position: 'relative' }}>
          <button onClick={() => setAddMenuOpen((v) => !v)} style={btnStyle}>
            + Add ▾
          </button>
          {addMenuOpen && (
            <div
              style={{
                position: 'absolute',
                top: '100%',
                left: 0,
                marginTop: 4,
                background: '#FDFAF4',
                border: '1px solid #EBEDE0',
                borderRadius: 8,
                padding: 4,
                display: 'flex',
                flexDirection: 'column',
                gap: 2,
                minWidth: 160,
              }}
            >
              <button onClick={() => openPanel('add')} style={{ ...btnStyle, textAlign: 'left' }}>
                Add a book
              </button>
              <button onClick={() => openPanel('isbn')} style={{ ...btnStyle, textAlign: 'left' }}>
                Add by ISBN
              </button>
              <button onClick={() => openPanel('scan')} style={{ ...btnStyle, textAlign: 'left' }}>
                Scan barcode
              </button>
              <button onClick={() => openPanel('import')} style={{ ...btnStyle, textAlign: 'left' }}>
                Import library
              </button>
            </div>
          )}
        </div>
        <div style={{ position: 'relative' }}>
          <input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.stopPropagation()}
            placeholder="Search your library"
            aria-label="Search your library"
            style={{ padding: '6px 12px', borderRadius: 8, border: '1px solid #EBEDE0', width: 180 }}
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              aria-label="Clear search"
              style={{ position: 'absolute', right: 4, top: 4, border: 'none', background: 'none', cursor: 'pointer' }}
            >
              ×
            </button>
          )}
        </div>
        <button
          onClick={() => downloadLibraryExport(library)}
          disabled={library.stars.length === 0}
          style={btnStyle}
        >
          Export
        </button>
        <button onClick={() => openPanel('customize')} style={btnStyle}>
          Customize
        </button>
        <button onClick={() => openPanel('settings')} style={btnStyle}>
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
