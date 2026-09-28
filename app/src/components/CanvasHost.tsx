// Owns the <canvas> element and the RAF draw loop — ports resize()/the
// interaction handlers/the draw(now) loop from reference/neural_mind.py.
// Reads the store via getState() inside the loop (not useLibraryStore(...))
// so canvas rendering isn't coupled to React's render cycle.
import { useEffect, useRef } from 'react';
import { makeCamera } from '../render/camera';
import { deriveConnectionsFor } from '../model/connections';
import { draw, projectAll } from '../render/draw';
import { pickStar } from '../render/pick';
import { filterVisible } from '../render/timelapse';
import { useLibraryStore } from '../store/useLibraryStore';
import { trackEvent } from '../analytics/analytics';

export function CanvasHost() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const camera = makeCamera();
    let w = 0;
    let h = 0;
    let dpr = 1;

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas!.width = window.innerWidth * dpr;
      h = canvas!.height = window.innerHeight * dpr;
      canvas!.style.width = `${window.innerWidth}px`;
      canvas!.style.height = `${window.innerHeight}px`;
    }
    resize();
    window.addEventListener('resize', resize);

    let dragging = false;
    let moved = false;
    let last = { x: 0, y: 0 };
    let hoveredId: string | null = null;

    function toCanvasCoords(clientX: number, clientY: number) {
      return { x: clientX * dpr, y: clientY * dpr };
    }

    function onPointerDown(e: PointerEvent) {
      dragging = true;
      moved = false;
      last = { x: e.clientX, y: e.clientY };
    }
    function onPointerMove(e: PointerEvent) {
      if (dragging) {
        const dx = e.clientX - last.x;
        const dy = e.clientY - last.y;
        if (Math.abs(dx) + Math.abs(dy) > 3) moved = true;
        camera.rotY += dx * 0.005;
        camera.rotX = Math.max(-1.4, Math.min(1.4, camera.rotX + dy * 0.005));
        last = { x: e.clientX, y: e.clientY };
        return;
      }
      const { x, y } = toCanvasCoords(e.clientX, e.clientY);
      const state = useLibraryStore.getState();
      const projected = projectAll(state.library, camera, renderTime, w, h, state.visual);
      hoveredId = pickStar(projected, x, y, 14 * dpr);
    }
    function onPointerUp(e: PointerEvent) {
      dragging = false;
      if (moved) return; // was a drag, not a tap
      const { x, y } = toCanvasCoords(e.clientX, e.clientY);
      const state = useLibraryStore.getState();
      const projected = projectAll(state.library, camera, renderTime, w, h, state.visual);
      const hitId = pickStar(projected, x, y, 14 * dpr);
      if (!hitId) {
        state.deselect();
        return;
      }
      if (state.mode.kind === 'tooltip' && state.mode.starId === hitId) {
        state.enterConnectMode(hitId);
      } else if (state.mode.kind === 'connect') {
        state.exitConnectMode();
      } else {
        state.selectStar(hitId);
      }
    }
    function onWheel(e: WheelEvent) {
      e.preventDefault();
      const factor = Math.exp(-e.deltaY * 0.001);
      camera.scale = Math.max(0.2, Math.min(5, camera.scale * factor));
    }

    canvas.addEventListener('pointerdown', onPointerDown);
    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerup', onPointerUp);
    canvas.addEventListener('wheel', onWheel, { passive: false });

    let raf = 0;
    let renderTime = 0;
    let last_t = performance.now();
    let fpsFrames = 0;
    let fpsWindowStart = last_t;

    function frame(now: number) {
      const state = useLibraryStore.getState();
      const dt = state.frozen ? 0 : Math.min(0.05, (now - last_t) / 1000);
      last_t = now;
      renderTime += dt;

      // Sample average fps once every ~10s — see specs/13-maintain-metrics.md.
      fpsFrames++;
      if (now - fpsWindowStart >= 10000) {
        trackEvent('render_fps_sampled', { fps: Math.round((fpsFrames * 1000) / (now - fpsWindowStart)) });
        fpsFrames = 0;
        fpsWindowStart = now;
      }

      if (!dragging) camera.rotY += state.visual.rotationSpeed * dt;
      const connectLit =
        state.mode.kind === 'connect' ? deriveConnectionsFor(state.library, state.mode.starId) : null;
      const selectedId =
        state.mode.kind === 'tooltip' || state.mode.kind === 'connect' ? state.mode.starId : null;
      const visibleIds =
        state.timelapseCutoff !== null ? filterVisible(state.library, state.timelapseCutoff) : null;

      draw(ctx!, w, h, {
        library: state.library,
        synapses: state.synapses,
        camera,
        renderTime,
        hoveredId,
        selectedId,
        connectLit,
        visibleIds,
        visual: state.visual,
      });

      raf = requestAnimationFrame(frame);
    }
    raf = requestAnimationFrame(frame);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', resize);
      canvas.removeEventListener('pointerdown', onPointerDown);
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('pointerup', onPointerUp);
      canvas.removeEventListener('wheel', onWheel);
    };
  }, []);

  return <canvas ref={canvasRef} style={{ display: 'block', touchAction: 'none' }} />;
}
