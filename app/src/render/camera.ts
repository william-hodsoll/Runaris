// Two-axis orbit camera — ports cam/project()/fitView() from
// reference/neural_mind.py. rotY = azimuth, rotX = elevation.
import type { Vec3 } from '../model/types';

export type Camera = { rotX: number; rotY: number; dist: number; scale: number };

export function makeCamera(): Camera {
  return { rotX: 0.18, rotY: 0.55, dist: 1500, scale: 1.0 };
}

export type Projected = { sx: number; sy: number; persp: number; depth: number };

export function project(p: Vec3, cam: Camera, viewportW: number, viewportH: number): Projected {
  const cy = Math.cos(cam.rotY);
  const sy = Math.sin(cam.rotY);
  const rx = p.x * cy - p.z * sy;
  const rz = p.x * sy + p.z * cy;

  const cx = Math.cos(cam.rotX);
  const sx = Math.sin(cam.rotX);
  const ry = p.y * cx - rz * sx;
  const rz2 = p.y * sx + rz * cx;

  const persp = cam.dist / Math.max(cam.dist + rz2, 1);
  return {
    sx: viewportW * 0.5 + rx * persp * cam.scale,
    sy: viewportH * 0.5 + ry * persp * cam.scale,
    persp,
    depth: rz2,
  };
}

/** Scales the camera so the whole sphere fits comfortably in view. */
export function fitView(cam: Camera, points: Vec3[], viewportW: number, viewportH: number): void {
  let maxR = 1;
  for (const p of points) {
    const r = Math.hypot(p.x, p.y, p.z);
    if (r > maxR) maxR = r;
  }
  const margin = Math.min(viewportW, viewportH) * 0.4;
  cam.scale = margin / maxR;
}
