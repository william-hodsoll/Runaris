// Closed event catalog — the only way to call trackEvent(). A caller cannot
// pass a title/author/note as an event name or a string prop, which is the
// structural enforcement behind CLAUDE.md's "Never send book/library content
// through the analytics adapter" rule.
export type AnalyticsEvent =
  | 'app_opened'
  | 'demo_loaded'
  | 'book_added'
  | 'book_added_manual'
  | 'book_added_isbn'
  | 'book_removed'
  | 'connect_mode_entered'
  | 'import_completed'
  | 'analytics_opt_out'
  | 'analytics_opt_in';

// Values are restricted to number/boolean so a string (which could carry a
// title, author, or note) is not even type-checkable as a prop value.
export type AnalyticsProps = Record<string, number | boolean>;
