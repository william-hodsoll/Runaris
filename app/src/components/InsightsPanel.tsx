import { averagePages, topSubjects, totalPages } from '../model/insights';
import { useLibraryStore } from '../store/useLibraryStore';

export function InsightsPanel() {
  const library = useLibraryStore((s) => s.library);

  if (library.stars.length === 0) {
    return <div style={{ fontSize: 13, color: '#6b6b63' }}>Add some books to see insights.</div>;
  }

  const top = topSubjects(library, 5);

  return (
    <div style={{ fontSize: 13, display: 'flex', flexDirection: 'column', gap: 8 }}>
      <Row label="Books" value={String(library.stars.length)} />
      <Row label="Constellations" value={String(library.constellations.length)} />
      <Row label="Total pages" value={totalPages(library).toLocaleString()} />
      <Row label="Average book length" value={`${Math.round(averagePages(library))} pages`} />
      <div>
        <div style={{ color: '#6b6b63', marginBottom: 4 }}>Top subjects</div>
        {top.map(([subject, count]) => (
          <Row key={subject} label={subject} value={String(count)} />
        ))}
      </div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      <span>{label}</span>
      <span style={{ fontWeight: 600 }}>{value}</span>
    </div>
  );
}
