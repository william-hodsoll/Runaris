import { afterEach, describe, expect, it, vi } from 'vitest';
import { lookupByIsbn } from '../openLibrary';

describe('lookupByIsbn', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('maps a known-shape OpenLibrary response to a BookInput', async () => {
    const isbn = '9780132350884';
    const response = {
      [`ISBN:${isbn}`]: {
        title: 'Clean Code',
        authors: [{ name: 'Robert C. Martin' }],
        subjects: [{ name: 'Software engineering' }],
        cover: { large: 'https://covers.openlibrary.org/b/isbn/xyz-L.jpg' },
        number_of_pages: 464,
      },
    };
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: true, json: async () => response }),
    );

    const result = await lookupByIsbn(isbn);
    expect(result).toEqual({
      title: 'Clean Code',
      author: 'Robert C. Martin',
      year: undefined,
      subjects: ['Software engineering'],
      pages: 464,
      coverUrl: 'https://covers.openlibrary.org/b/isbn/xyz-L.jpg',
      isbn,
    });
  });

  it('returns null for an ISBN with no OpenLibrary record', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) }));
    const result = await lookupByIsbn('0000000000');
    expect(result).toBeNull();
  });

  it('throws on a network/HTTP failure so the caller can show a retry state', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 503 }));
    await expect(lookupByIsbn('9780132350884')).rejects.toThrow();
  });

  it('strips punctuation/whitespace from a pasted ISBN before querying', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) });
    vi.stubGlobal('fetch', fetchMock);
    await lookupByIsbn('978-0-13-235088-4');
    expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('ISBN:9780132350884'));
  });

  it('returns null for an empty/garbage input without calling fetch', async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    const result = await lookupByIsbn('   ');
    expect(result).toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
