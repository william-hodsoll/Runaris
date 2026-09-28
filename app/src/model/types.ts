// Data model ported from reference/neural_mind.py's STARS/CENTRES/EDGES.
// See CLAUDE.md "Architecture" and specs/02-react-vite-port.md "Data model".

export type Vec3 = { x: number; y: number; z: number };

export type BookInput = {
  title: string;
  author?: string;
  year?: string;
  genre?: string;
  subjects?: string[];
  pages?: number;
  isbn?: string;
  coverUrl?: string;
  status?: string;
};

export type BookStar = {
  id: string;
  title: string;
  author: string;
  year: string;
  genre: string;
  subjects: string[];
  pages: number;
  isbn?: string;
  coverUrl?: string;
  status?: string;
  dateAdded: number; // ms epoch
  constellationId: string;
  position: Vec3;
  offset: Vec3; // displacement from constellation centre (ox/oy/oz in v1)
  size: number; // derived from pages, v1's size_from_pages()
  color: string;
  phase: number; // twinkle phase
  speed: number; // twinkle speed
};

export type Constellation = {
  id: string;
  subject: string;
  position: Vec3;
  color: string;
  axis: Vec3;
  spinSpeed: number;
  spinPhase: number;
  count: number;
};

export type Edge = { a: string; b: string }; // full shared-attribute graph (pulse pool)
export type Synapse = { a: string; b: string }; // sparse always-visible web

export type Library = {
  version: 1;
  stars: BookStar[];
  constellations: Constellation[];
};

export type LibraryDerived = {
  edges: Edge[];
  synapses: Synapse[];
};
