// Text-entry ISBN lookup flow — per specs/04-isbn-lookup.md. Camera barcode
// scan is deferred; this covers the same OpenLibrary lookup path.
import { useState } from 'react';
import type { BookInput } from '../model/types';
import { lookupByIsbn } from '../lookup/openLibrary';
import { useLibraryStore } from '../store/useLibraryStore';

type Status = { kind: 'idle' } | { kind: 'loading' } | { kind: 'error'; message: string } | { kind: 'preview'; book: BookInput };

export function AddByIsbn({ onClose }: { onClose: () => void }) {
  const [isbn, setIsbn] = useState('');
  const [status, setStatus] = useState<Status>({ kind: 'idle' });
  const addBook = useLibraryStore((s) => s.addBook);

  async function handleLookup() {
    setStatus({ kind: 'loading' });
    try {
      const book = await lookupByIsbn(isbn);
      if (!book) {
        setStatus({ kind: 'error', message: 'No record found for that ISBN.' });
        return;
      }
      setStatus({ kind: 'preview', book });
    } catch {
      setStatus({ kind: 'error', message: 'Lookup failed. Check your connection and try again.' });
    }
  }

  function handleConfirm() {
    if (status.kind !== 'preview') return;
    addBook(status.book, 'isbn');
    onClose();
  }

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
      <div style={{ background: '#FDFAF4', borderRadius: 12, padding: 20, width: 320, fontFamily: 'system-ui, sans-serif' }}>
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Add by ISBN</div>
        <input
          value={isbn}
          onChange={(e) => setIsbn(e.target.value)}
          placeholder="978-0-13-235088-4"
          style={{ width: '100%', padding: 8, borderRadius: 8, border: '1px solid #EBEDE0', marginBottom: 10 }}
        />
        {status.kind === 'error' && (
          <div style={{ color: '#b4506a', fontSize: 13, marginBottom: 10 }}>{status.message}</div>
        )}
        {status.kind === 'preview' && (
          <div style={{ marginBottom: 10, fontSize: 13 }}>
            <div style={{ fontWeight: 600 }}>{status.book.title}</div>
            <div style={{ color: '#6b6b63' }}>{status.book.author}</div>
          </div>
        )}
        <div style={{ display: 'flex', gap: 8 }}>
          {status.kind === 'preview' ? (
            <>
              <button onClick={handleConfirm} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
                Add to cosmos
              </button>
              <button onClick={() => setStatus({ kind: 'idle' })} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
                Try another
              </button>
            </>
          ) : (
            <button
              onClick={handleLookup}
              disabled={status.kind === 'loading' || !isbn.trim()}
              style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}
            >
              {status.kind === 'loading' ? 'Looking up…' : 'Look up'}
            </button>
          )}
          <button onClick={onClose} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
