// Ports pickStar() from reference/neural_mind.py: nearest projected star
// within a screen-space radius, preferring the closest (smallest depth) on
// a tie so overlapping stars resolve to the one nearest the camera.
export function pickStar(
  projected: Map<string, { sx: number; sy: number; depth: number }>,
  screenX: number,
  screenY: number,
  radiusPx = 14,
): string | null {
  let bestId: string | null = null;
  let bestDist = Infinity;
  for (const [id, p] of projected) {
    const d = Math.hypot(p.sx - screenX, p.sy - screenY);
    if (d <= radiusPx && d < bestDist) {
      bestDist = d;
      bestId = id;
    }
  }
  return bestId;
}
