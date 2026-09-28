import { beforeEach, describe, expect, it } from 'vitest';
import { initAnalytics, isOptedOut, markPrivacyNoticeSeen, hasSeenPrivacyNotice, setOptOut, trackEvent } from '../analytics';

describe('analytics adapter', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('does not throw when tracking with no SDKs configured (no env keys)', async () => {
    await initAnalytics();
    expect(() => trackEvent('app_opened')).not.toThrow();
  });

  it('opt-out flag defaults to false and persists when set', () => {
    expect(isOptedOut()).toBe(false);
    setOptOut(true);
    expect(isOptedOut()).toBe(true);
    setOptOut(false);
    expect(isOptedOut()).toBe(false);
  });

  it('privacy notice defaults to unseen and persists once marked seen', () => {
    expect(hasSeenPrivacyNotice()).toBe(false);
    markPrivacyNoticeSeen();
    expect(hasSeenPrivacyNotice()).toBe(true);
  });

  it('does not throw when tracking while opted out', () => {
    setOptOut(true);
    expect(() => trackEvent('book_added')).not.toThrow();
  });
});
