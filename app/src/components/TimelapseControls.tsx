// Slider + play/pause for the timelapse — ports startTimelapsePlay()/
// tlFormatDate() from reference/neural_mind.py. specs/07-timelapse.md.
import { useEffect, useRef, useState } from 'react';
import { formatTimelapseDate, timelapseBounds } from '../render/timelapse';
import { useLibraryStore } from '../store/useLibraryStore';

const PLAY_DURATION_MS = 12_000;

export function TimelapseControls() {
  const library = useLibraryStore((s) => s.library);
  const cutoff = useLibraryStore((s) => s.timelapseCutoff);
  const setCutoff = useLibraryStore((s) => s.setTimelapseCutoff);
  const exitTimelapse = useLibraryStore((s) => s.exitTimelapse);
  const [playing, setPlaying] = useState(false);
  const rafRef = useRef<number>();

  const bounds = timelapseBounds(library);

  useEffect(() => {
    if (!playing || !bounds) return;
    const start = performance.now();
    const startCutoff = cutoff ?? bounds.min;
    function tick(now: number) {
      const t = Math.min(1, (now - start) / PLAY_DURATION_MS);
      const value = startCutoff + t * (bounds!.max - startCutoff);
      setCutoff(value);
      if (t < 1) rafRef.current = requestAnimationFrame(tick);
      else setPlaying(false);
    }
    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing]);

  if (!bounds || library.stars.length === 0) return null;

  function handleOpen() {
    setCutoff(bounds!.max);
  }

  if (cutoff === null) {
    return (
      <button
        onClick={handleOpen}
        style={{ position: 'fixed', top: 16, right: 16, padding: '6px 12px', borderRadius: 8, cursor: 'pointer' }}
      >
        Timelapse
      </button>
    );
  }

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 16,
        left: 16,
        right: 16,
        maxWidth: 480,
        margin: '0 auto',
        background: '#FDFAF4',
        border: '1px solid #EBEDE0',
        borderRadius: 12,
        padding: 12,
        fontFamily: 'system-ui, sans-serif',
        fontSize: 13,
        zIndex: 15,
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <span>{formatTimelapseDate(cutoff)}</span>
        <button onClick={exitTimelapse} style={{ background: 'transparent', border: 'none', cursor: 'pointer' }}>
          Exit
        </button>
      </div>
      <input
        type="range"
        min={bounds.min}
        max={bounds.max}
        value={cutoff}
        onChange={(e) => setCutoff(Number(e.target.value))}
        style={{ width: '100%' }}
      />
      <button onClick={() => setPlaying((p) => !p)} style={{ marginTop: 6, padding: '4px 10px', borderRadius: 8, cursor: 'pointer' }}>
        {playing ? 'Pause' : 'Play'}
      </button>
    </div>
  );
}
