// Manual add-book form — fields ported 1:1 from v1's renderAddBook()
// (reference/neural_mind.py:2510). See specs/15-manual-add-and-remove.md.
import { useState } from 'react';
import type { BookInput } from '../model/types';
import { useLibraryStore } from '../store/useLibraryStore';
import { trackEvent } from '../analytics/analytics';

const GENRES = [
  'Fiction', 'Sci-Fi', 'Fantasy', 'Mystery', 'Horror', 'Romance', 'Philosophy',
  'Science', 'Non-Fiction', 'Poetry', 'History', 'Biography', 'Other',
];

export function AddBookManual({ onClose }: { onClose: () => void }) {
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [year, setYear] = useState('');
  const [pages, setPages] = useState('');
  const [genre, setGenre] = useState(GENRES[0]);
  const [subjects, setSubjects] = useState('');
  const [error, setError] = useState('');
  const addBook = useLibraryStore((s) => s.addBook);

  function handleSave() {
    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      setError('Title is required');
      return;
    }
    const book: BookInput = {
      title: trimmedTitle,
      author: author.trim() || 'Unknown',
      year: year.trim(),
      pages: parseInt(pages, 10) || 0,
      genre,
      subjects: subjects.split(',').map((s) => s.trim()).filter(Boolean),
    };
    addBook(book, 'manual');
    trackEvent('book_added_manual');
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
      <div style={{ background: '#FDFAF4', borderRadius: 12, padding: 20, width: 340, fontFamily: 'system-ui, sans-serif' }}>
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Add a book</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Title"
            style={{ padding: 8, borderRadius: 8, border: '1px solid #EBEDE0' }}
          />
          <input
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            placeholder="Author"
            style={{ padding: 8, borderRadius: 8, border: '1px solid #EBEDE0' }}
          />
          <div style={{ display: 'flex', gap: 8 }}>
            <input
              value={year}
              onChange={(e) => setYear(e.target.value)}
              placeholder="Year"
              style={{ flex: 1, padding: 8, borderRadius: 8, border: '1px solid #EBEDE0', minWidth: 0 }}
            />
            <input
              value={pages}
              onChange={(e) => setPages(e.target.value)}
              placeholder="Pages"
              style={{ flex: 1, padding: 8, borderRadius: 8, border: '1px solid #EBEDE0', minWidth: 0 }}
            />
          </div>
          <select
            value={genre}
            onChange={(e) => setGenre(e.target.value)}
            style={{ padding: 8, borderRadius: 8, border: '1px solid #EBEDE0' }}
          >
            {GENRES.map((g) => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select>
          <input
            value={subjects}
            onChange={(e) => setSubjects(e.target.value)}
            placeholder="Subjects (comma-separated)"
            style={{ padding: 8, borderRadius: 8, border: '1px solid #EBEDE0' }}
          />
          <div style={{ fontSize: 12, color: '#8a8a80' }}>
            First subject decides which constellation the star joins. Pages determines star size.
          </div>
        </div>
        {error && <div style={{ color: '#b4506a', fontSize: 13, marginTop: 8 }}>{error}</div>}
        <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
          <button onClick={handleSave} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
            Add to cosmos
          </button>
          <button onClick={onClose} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
