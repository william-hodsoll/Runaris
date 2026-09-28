// Ports liveStarPos() / the position math inlined in draw() from
// reference/neural_mind.py: a star's on-screen position each frame is its
// constellation centre plus its offset, rotated around the constellation's
// own axis by spinSpeed*time, then scaled by the global "breathing" factor.
import type { BookStar, Constellation, Vec3 } from '../model/types';

function rotateAroundAxis(v: Vec3, axis: Vec3, angle: number): Vec3 {
  // Rodrigues' rotation formula.
  const cosA = Math.cos(angle);
  const sinA = Math.sin(angle);
  const dot = v.x * axis.x + v.y * axis.y + v.z * axis.z;
  const cross = {
    x: axis.y * v.z - axis.z * v.y,
    y: axis.z * v.x - axis.x * v.z,
    z: axis.x * v.y - axis.y * v.x,
  };
  return {
    x: v.x * cosA + cross.x * sinA + axis.x * dot * (1 - cosA),
    y: v.y * cosA + cross.y * sinA + axis.y * dot * (1 - cosA),
    z: v.z * cosA + cross.z * sinA + axis.z * dot * (1 - cosA),
  };
}

export function breathScale(t: number): number {
  return 1 + Math.sin(t * 0.5) * 0.045 + Math.sin(t * 1.7) * 0.012;
}

export function liveStarPos(
  star: BookStar,
  constellation: Constellation,
  renderTime: number,
  gravity = 1,
  breathing = true,
  constellationSpin = 1,
): Vec3 {
  const breath = breathing ? breathScale(renderTime) : 1;
  const angle = constellation.spinPhase + constellation.spinSpeed * constellationSpin * renderTime;
  const rotatedOffset = rotateAroundAxis(star.offset, constellation.axis, angle);
  const centre = constellation.position;
  return {
    x: (centre.x + rotatedOffset.x * gravity) * breath,
    y: (centre.y + rotatedOffset.y * gravity) * breath,
    z: (centre.z + rotatedOffset.z * gravity) * breath,
  };
}
