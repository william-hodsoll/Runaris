// Single adapter for all analytics — see CLAUDE.md "Never call PostHog/Sentry
// directly outside analytics.ts". No-ops cleanly if no project keys are
// configured (VITE_POSTHOG_KEY / VITE_SENTRY_DSN), so the app works with
// zero analytics config in local dev.
import type { AnalyticsEvent, AnalyticsProps } from './types';

const OPT_OUT_KEY = 'runaris.analyticsOptOut';
const SEEN_NOTICE_KEY = 'runaris.hasSeenPrivacyNotice';

type PostHogLike = {
  init: (key: string, opts: Record<string, unknown>) => void;
  capture: (event: string, props?: AnalyticsProps) => void;
  opt_out_capturing: () => void;
  opt_in_capturing: () => void;
};
type SentryLike = {
  init: (opts: Record<string, unknown>) => void;
  captureException: (e: unknown) => void;
  addBreadcrumb: (b: { category: string; message: string; data?: AnalyticsProps }) => void;
};

let posthog: PostHogLike | null = null;
let sentry: SentryLike | null = null;
let initialized = false;

function readFlag(key: string): boolean {
  try {
    return localStorage.getItem(key) === 'true';
  } catch {
    return false;
  }
}

function writeFlag(key: string, value: boolean): void {
  try {
    localStorage.setItem(key, String(value));
  } catch {
    // best-effort; matches persistence layer's convention
  }
}

export function isOptedOut(): boolean {
  return readFlag(OPT_OUT_KEY);
}

export function hasSeenPrivacyNotice(): boolean {
  return readFlag(SEEN_NOTICE_KEY);
}

export function markPrivacyNoticeSeen(): void {
  writeFlag(SEEN_NOTICE_KEY, true);
}

export async function initAnalytics(): Promise<void> {
  if (initialized) return;
  initialized = true;

  const posthogKey = import.meta.env.VITE_POSTHOG_KEY as string | undefined;
  const sentryDsn = import.meta.env.VITE_SENTRY_DSN as string | undefined;

  if (posthogKey) {
    const mod = await import('posthog-js');
    posthog = mod.default as unknown as PostHogLike;
    posthog.init(posthogKey, { api_host: 'https://us.i.posthog.com', capture_pageview: false });
    if (isOptedOut()) posthog.opt_out_capturing();
  }

  if (sentryDsn) {
    const mod = await import('@sentry/browser');
    sentry = mod as unknown as SentryLike;
    sentry.init({ dsn: sentryDsn, tracesSampleRate: 0.1 });
  }
}

export function setOptOut(optOut: boolean): void {
  writeFlag(OPT_OUT_KEY, optOut);
  if (optOut) posthog?.opt_out_capturing();
  else posthog?.opt_in_capturing();
  trackEvent(optOut ? 'analytics_opt_out' : 'analytics_opt_in');
}

export function trackEvent(event: AnalyticsEvent, props?: AnalyticsProps): void {
  if (isOptedOut()) return;
  try {
    posthog?.capture(event, props);
    sentry?.addBreadcrumb({ category: 'usage', message: event, data: props });
  } catch {
    if (import.meta.env.DEV) {
      // eslint-disable-next-line no-console
      console.debug('[analytics] swallowed error while tracking', event);
    }
  }
}

export function captureError(error: unknown): void {
  try {
    sentry?.captureException(error);
  } catch {
    // never let analytics failure cascade into a second error
  }
}
