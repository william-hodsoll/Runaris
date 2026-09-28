// File-based import flow — per specs/05-csv-import.md. Shows a "N ready, M
// flagged" preview before committing, so a bad row is visible, not silent.
import { useState } from 'react';
import { importLibraryFile } from '../import/importLibrary';
import type { ImportResult } from '../import/importLibrary';
import { useLibraryStore } from '../store/useLibraryStore';

export function ImportLibrary({ onClose }: { onClose: () => void }) {
  const [result, setResult] = useState<ImportResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const addBooks = useLibraryStore((s) => s.addBooks);

  async function handleFile(file: File) {
    setError(null);
    try {
      const text = await file.text();
      setResult(importLibraryFile(text, file.name));
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Could not read that file.');
    }
  }

  function handleCommit() {
    if (!result) return;
    addBooks(result.books, result.flagged.length);
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
      <div style={{ background: '#FDFAF4', borderRadius: 12, padding: 20, width: 360, fontFamily: 'system-ui, sans-serif' }}>
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Import library</div>
        <div style={{ fontSize: 13, color: '#6b6b63', marginBottom: 10 }}>
          Drop a .csv or .json file — your own export, or a Goodreads export.
        </div>
        <input
          type="file"
          accept=".csv,.json,application/json,text/csv"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) void handleFile(file);
          }}
          style={{ marginBottom: 10 }}
        />
        {error && <div style={{ color: '#b4506a', fontSize: 13, marginBottom: 10 }}>{error}</div>}
        {result && (
          <div style={{ fontSize: 13, marginBottom: 10 }}>
            {result.books.length} ready, {result.flagged.length} flagged (missing a title)
          </div>
        )}
        <div style={{ display: 'flex', gap: 8 }}>
          <button
            onClick={handleCommit}
            disabled={!result || result.books.length === 0}
            style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}
          >
            Import {result ? result.books.length : ''} books
          </button>
          <button onClick={onClose} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
