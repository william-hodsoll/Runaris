// Camera scan flow — per specs/09-camera-scan.md. Falls back to a link to
// AddByIsbn when BarcodeDetector isn't supported, and distinguishes
// "unsupported" from "camera permission denied".
import { useEffect, useRef, useState } from 'react';
import type { BookInput } from '../model/types';
import { lookupByIsbn } from '../lookup/openLibrary';
import { isScanSupported, scanIsbnFromVideo } from '../scan/barcodeScanner';
import { useLibraryStore } from '../store/useLibraryStore';

type Status =
  | { kind: 'unsupported' }
  | { kind: 'requesting' }
  | { kind: 'denied' }
  | { kind: 'scanning' }
  | { kind: 'looking-up' }
  | { kind: 'preview'; book: BookInput }
  | { kind: 'error'; message: string };

export function ScanIsbn({ onClose, onUseTextEntry }: { onClose: () => void; onUseTextEntry: () => void }) {
  const [status, setStatus] = useState<Status>(isScanSupported() ? { kind: 'requesting' } : { kind: 'unsupported' });
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const addBook = useLibraryStore((s) => s.addBook);

  useEffect(() => {
    if (status.kind !== 'requesting') return;
    let cancelled = false;
    navigator.mediaDevices
      ?.getUserMedia({ video: { facingMode: 'environment' } })
      .then((stream) => {
        if (cancelled) {
          stream.getTracks().forEach((t) => t.stop());
          return;
        }
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          void videoRef.current.play();
        }
        setStatus({ kind: 'scanning' });
      })
      .catch(() => setStatus({ kind: 'denied' }));
    return () => {
      cancelled = true;
    };
  }, [status.kind]);

  useEffect(() => {
    if (status.kind !== 'scanning') return;
    let cancelled = false;
    const interval = setInterval(async () => {
      if (cancelled || !videoRef.current) return;
      try {
        const isbn = await scanIsbnFromVideo(videoRef.current);
        if (isbn && !cancelled) {
          setStatus({ kind: 'looking-up' });
          const book = await lookupByIsbn(isbn);
          if (cancelled) return;
          if (book) setStatus({ kind: 'preview', book });
          else setStatus({ kind: 'error', message: 'No record found for that ISBN.' });
        }
      } catch {
        if (!cancelled) setStatus({ kind: 'error', message: 'Scan failed. Try again.' });
      }
    }, 400);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [status.kind]);

  useEffect(() => {
    return () => {
      streamRef.current?.getTracks().forEach((t) => t.stop());
    };
  }, []);

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
        <div style={{ fontWeight: 600, marginBottom: 10 }}>Scan a barcode</div>

        {status.kind === 'unsupported' && (
          <div style={{ fontSize: 13, marginBottom: 10 }}>
            Scanning isn't supported on this browser.{' '}
            <button onClick={onUseTextEntry} style={{ textDecoration: 'underline', cursor: 'pointer', border: 'none', background: 'none' }}>
              Use Add by ISBN instead
            </button>
            .
          </div>
        )}
        {status.kind === 'denied' && (
          <div style={{ fontSize: 13, marginBottom: 10, color: '#b4506a' }}>
            Camera access was denied.{' '}
            <button onClick={onUseTextEntry} style={{ textDecoration: 'underline', cursor: 'pointer', border: 'none', background: 'none' }}>
              Use Add by ISBN instead
            </button>
            .
          </div>
        )}
        {(status.kind === 'requesting' || status.kind === 'scanning' || status.kind === 'looking-up') && (
          <>
            <video ref={videoRef} style={{ width: '100%', borderRadius: 8, marginBottom: 10 }} muted playsInline />
            <div style={{ fontSize: 13, color: '#6b6b63' }}>
              {status.kind === 'looking-up' ? 'Looking up…' : 'Point the camera at a barcode.'}
            </div>
          </>
        )}
        {status.kind === 'error' && <div style={{ fontSize: 13, color: '#b4506a', marginBottom: 10 }}>{status.message}</div>}
        {status.kind === 'preview' && (
          <div style={{ fontSize: 13, marginBottom: 10 }}>
            <div style={{ fontWeight: 600 }}>{status.book.title}</div>
            <div style={{ color: '#6b6b63' }}>{status.book.author}</div>
          </div>
        )}

        <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
          {status.kind === 'preview' && (
            <button onClick={handleConfirm} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
              Add to cosmos
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
