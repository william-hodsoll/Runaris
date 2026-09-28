// Ports v1's Customize panel (reference/neural_mind.py ~L2646-2793). Every
// control writes straight to the store slice, live — no "Done" gating,
// matching v1. specs/11-customize-panel.md.
import { countByStatus } from '../model/insights';
import type { VisualSettings } from '../model/visualSettings';
import { useLibraryStore } from '../store/useLibraryStore';

const STATUS_CHIPS: { id: VisualSettings['statusFilter']; label: string }[] = [
  { id: 'all', label: 'All' },
  { id: 'reading', label: 'Reading' },
  { id: 'finished', label: 'Finished' },
  { id: 'unread', label: 'Unread' },
  { id: 'abandoned', label: 'Abandoned' },
];

function Slider({
  label,
  value,
  min,
  max,
  step,
  onChange,
  fmt,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (v: number) => void;
  fmt: (v: number) => string;
}) {
  return (
    <div style={{ marginBottom: 10 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12 }}>
        <span>{label}</span>
        <b>{fmt(value)}</b>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{ width: '100%' }}
      />
    </div>
  );
}

export function CustomizePanel({ onClose }: { onClose: () => void }) {
  const visual = useLibraryStore((s) => s.visual);
  const setVisual = useLibraryStore((s) => s.setVisual);
  const resetVisual = useLibraryStore((s) => s.resetVisual);
  const library = useLibraryStore((s) => s.library);
  const counts = countByStatus(library);

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
      <div
        style={{
          background: '#FDFAF4',
          borderRadius: 12,
          padding: 20,
          width: 340,
          maxHeight: '80vh',
          overflowY: 'auto',
          fontFamily: 'system-ui, sans-serif',
        }}
      >
        <div style={{ fontWeight: 700, marginBottom: 12 }}>Customize</div>

        <div style={{ fontSize: 12, color: '#6b6b63', marginBottom: 6 }}>Filter by reading status</div>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16 }}>
          {STATUS_CHIPS.map((chip) => (
            <button
              key={chip.id}
              onClick={() => setVisual({ statusFilter: chip.id })}
              style={{
                padding: '4px 10px',
                borderRadius: 999,
                fontSize: 12,
                cursor: 'pointer',
                border: '1px solid #d8d3c4',
                background: visual.statusFilter === chip.id ? '#EBEDE0' : 'transparent',
                fontWeight: visual.statusFilter === chip.id ? 700 : 400,
              }}
            >
              {chip.label} {chip.id !== 'all' ? (counts.get(chip.id) ?? 0) : library.stars.length}
            </button>
          ))}
        </div>

        <div style={{ fontSize: 12, color: '#6b6b63', marginBottom: 6 }}>Animation</div>
        <Slider
          label="Star brightness"
          value={visual.starBrightness}
          min={0.4}
          max={2}
          step={0.05}
          fmt={(v) => `${v.toFixed(2)}×`}
          onChange={(v) => setVisual({ starBrightness: v })}
        />
        <Slider
          label="Auto-rotate (whole cosmos)"
          value={visual.rotationSpeed}
          min={0}
          max={0.4}
          step={0.01}
          fmt={(v) => v.toFixed(2)}
          onChange={(v) => setVisual({ rotationSpeed: v })}
        />

        <div style={{ fontSize: 12, color: '#6b6b63', margin: '12px 0 6px' }}>Constellations</div>
        <Slider
          label="Gravity (cluster tightness)"
          value={visual.gravity}
          min={0.3}
          max={2.5}
          step={0.05}
          fmt={(v) => `${v.toFixed(2)}×`}
          onChange={(v) => setVisual({ gravity: v })}
        />
        <Slider
          label="Self-rotation speed"
          value={visual.constellationSpin}
          min={0}
          max={4}
          step={0.05}
          fmt={(v) => `${v.toFixed(2)}×`}
          onChange={(v) => setVisual({ constellationSpin: v })}
        />

        <div style={{ fontSize: 12, color: '#6b6b63', margin: '12px 0 6px' }}>Other</div>
        <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, marginBottom: 6 }}>
          <input
            type="checkbox"
            checked={visual.breathing}
            onChange={(e) => setVisual({ breathing: e.target.checked })}
          />
          Sphere breathes
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, marginBottom: 10 }}>
          <input
            type="checkbox"
            checked={visual.showSynapses}
            onChange={(e) => setVisual({ showSynapses: e.target.checked })}
          />
          Constellation synapses
        </label>

        <div style={{ fontSize: 12, color: '#6b6b63', marginBottom: 6 }}>Star palette</div>
        <select
          value={visual.paletteMode}
          onChange={(e) => setVisual({ paletteMode: e.target.value as VisualSettings['paletteMode'] })}
          style={{ width: '100%', padding: 6, borderRadius: 8, marginBottom: 16 }}
        >
          <option value="default">Default — full spectrum</option>
          <option value="warm">Warm — amber &amp; rose</option>
          <option value="cool">Cool — blues &amp; violets</option>
          <option value="mono">Monochrome — silver white</option>
        </select>

        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={onClose} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
            Close
          </button>
          <button onClick={resetVisual} style={{ padding: '6px 14px', borderRadius: 8, cursor: 'pointer' }}>
            Reset
          </button>
        </div>
      </div>
    </div>
  );
}
